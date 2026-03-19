# Architecture

Neural-LAM is a modular framework for graph-based neural weather prediction over Limited Area Models (LAM).
It separates data ingestion, graph construction, and model training into independent, swappable components.

```{note}
Tensor shape notation: **(B, T, N_grid, d)** —
B = batch · T = timesteps · N_grid = flattened spatial grid nodes · N_mesh = mesh nodes · d = feature width.
```

---

## 1. Full Pipeline Overview

The end-to-end pipeline spans four stages: **data loading → graph construction → model forward pass → loss and logging**.

```{mermaid}
graph TD
    subgraph Sources["Data Sources"]
        MDP["MDP Dataset<br/>(mllam-data-prep zarr)"]
        NPY["NPY Files<br/>(MEPS format)"]
    end

    subgraph Datastores["Datastore Layer"]
        MDPStore["MDPDatastore"]
        NpyStore["NpyFilesDatastoreMEPS"]
        BaseDS["BaseDatastore<br/>(abstract interface)"]
        MDPStore --> BaseDS
        NpyStore --> BaseDS
    end

    subgraph Arrays["Raw xr.DataArrays"]
        State["state<br/>(time, grid_index, state_feature)"]
        Forcing["forcing<br/>(time, grid_index, forcing_feature)"]
        Static["static<br/>(grid_index, static_feature)"]
    end

    subgraph WDS["WeatherDataset.__getitem__"]
        Slice["_slice_state_time()<br/>_slice_forcing_time()"]
        Window["Window forcing<br/>past + current + future"]
        Stack["Stack features<br/>→ torch.Tensor"]
    end

    subgraph Batch["Batched Tensors (DataLoader)"]
        BI["init_states (B,2,N_grid,d_state)"]
        BT["target_states (B,ar_steps,N_grid,d_state)"]
        BF["forcing (B,ar_steps,N_grid,d_forcing)"]
        BTm["target_times (B,ar_steps)"]
    end

    subgraph Graphs["Graph Files (graphs/)"]
        G2M["g2m_edge_index.pt"]
        M2M["m2m_edge_index.pt"]
        M2G["m2g_edge_index.pt"]
        MeshFeat["mesh_features.pt"]
    end

    subgraph Model["Model (ARModel → BaseGraphModel)"]
        Norm["on_after_batch_transfer()<br/>normalise state + forcing"]
        Unroll["unroll_prediction()<br/>AR loop"]
        PredStep["predict_step()<br/>encode → process → decode"]
        Output["new_state = prev + delta<br/>+ boundary mask"]
    end

    subgraph LossLog["Loss & Logging"]
        Loss["metrics.get_metric()<br/>MSE / wMSE / NLL / CRPS"]
        WandB["W&B / MLflow<br/>train_loss, val_loss, spatial maps"]
    end

    MDP --> MDPStore
    NPY --> NpyStore
    MDPStore --> State & Forcing & Static
    NpyStore --> State & Forcing & Static
    State & Forcing & Static --> Slice
    Slice --> Window --> Stack
    Stack --> BI & BT & BF & BTm
    BI & BT & BF & BTm --> Norm
    Graphs --> PredStep
    Norm --> Unroll --> PredStep --> Output
    Output --> Loss --> WandB

    style Sources fill:#e1f5ff
    style Datastores fill:#f3e5f5
    style Arrays fill:#fff3e0
    style WDS fill:#fce4ec
    style Batch fill:#e0f2f1
    style Graphs fill:#e8f5e9
    style Model fill:#f5f5f5
    style LossLog fill:#f0f4c3
```

**Batch contract** — every model receives a 4-tuple:

| Tensor | Shape | Notes |
|---|---|---|
| `init_states` | `(B, 2, N_grid, d_state)` | Two consecutive normalised states to warm-start the rollout |
| `target_states` | `(B, ar_steps, N_grid, d_state)` | Future trajectory used for loss computation |
| `forcing` | `(B, ar_steps, N_grid, d_forcing)` | Windowed forcing — `num_past + 1 + num_future` steps per AR step, static covariates stacked in |
| `target_times` | `(B, ar_steps)` | Epoch-ns timestamps for each target step |

---

## 2. Datastore Class Hierarchy

The datastore abstraction decouples data format from model training.
All datastores expose the same interface regardless of whether data lives in zarr, numpy files, or NetCDF.

```{mermaid}
graph TD
    subgraph Hierarchy["Datastore Hierarchy"]
        BaseDS["BaseDatastore<br/>─────────────────────<br/>+ root_path, config, step_length<br/>+ get_dataarray(category, split)<br/>+ get_standardization_dataarray()<br/>+ get_vars_names/units/long_names()<br/>+ boundary_mask, num_grid_points<br/>+ expected_dim_order()<br/>+ get_xy(), get_xy_extent()"]

        BaseReg["BaseRegularGridDatastore<br/>─────────────────────<br/>+ grid_shape_state<br/>+ stack_grid_coords()<br/>+ unstack_grid_coords()"]

        MDP["MDPDatastore<br/>─────────────────────<br/>Reads mllam-data-prep zarr<br/>+ coords_projection()<br/>+ state_feature_weights_values"]

        NPY["NpyFilesDatastoreMEPS<br/>─────────────────────<br/>Reads MEPS .npy files<br/>+ _calc_datetime_forcing_features()<br/>+ compute_standardization_stats"]

        BaseReg --> BaseDS
        MDP --> BaseReg
        NPY --> BaseReg
    end

    style Hierarchy fill:#f3e5f5
```

**Key data contract** — `get_dataarray()` always returns:

| Category | Dimensions | Notes |
|---|---|---|
| `state` | `(time, grid_index, state_feature)` | Normalised on request via `standardize=True` |
| `forcing` | `(time, grid_index, forcing_feature)` | Includes datetime encodings in MEPS |
| `static` | `(grid_index, static_feature)` | Time-invariant; `split=None` allowed |

The `grid_index` dimension is a flat index over all spatial points.
`BaseRegularGridDatastore` adds `stack_grid_coords()` / `unstack_grid_coords()` to convert between
flat `grid_index` and 2D `(x, y)` grids.

**API:** {py:class}`~neural_lam.datastore.base.BaseDatastore` · {py:class}`~neural_lam.datastore.base.BaseRegularGridDatastore` · {py:class}`~neural_lam.datastore.mdp.MDPDatastore`

---

## 3. WeatherDataset — Time Sampling

{py:class}`~neural_lam.weather_dataset.WeatherDataset` bridges the datastore and the model.
It handles time-window slicing, forcing windowing, and tensor conversion.

```{mermaid}
graph TD
    subgraph WDS["WeatherDataset.__getitem__(idx)"]
        SliceState["_slice_state_time(idx, ar_steps)<br/>→ (2+ar_steps, N_grid, d_state)"]
        SliceForcing["_slice_forcing_time(idx, ar_steps)<br/>→ (ar_steps, N_grid, window, d_forcing)"]
        StackWindow["stack forcing window<br/>forcing_feature × window → d_forcing_windowed"]
        Split["split init / target<br/>init = time[0:2]<br/>target = time[2:]"]
        ToTensor["→ torch.Tensor (float32)"]
    end

    SliceState --> Split
    SliceForcing --> StackWindow --> ToTensor
    Split --> ToTensor

    style WDS fill:#fce4ec
```

**Forcing window** — for each AR step `t`, the forcing tensor includes:
`[t - num_past_forcing_steps, ..., t, ..., t + num_future_forcing_steps]`
stacked along the feature dimension. Default: 1 past + 1 future = window size 3.

**Dataset length** (analysis mode):
```
n_samples = len(time) - ar_steps - max(2, num_past_forcing_steps) - num_future_forcing_steps
```

Normalisation happens **on GPU** in `ARModel.on_after_batch_transfer()`, not in the dataset.

**API:** {py:class}`~neural_lam.weather_dataset.WeatherDataset` · {py:class}`~neural_lam.weather_dataset.WeatherDataModule`

---

## 4. Graph Construction

Graphs are built once from the datastore's grid coordinates and saved as `.pt` files.
The `create_graph.py` CLI uses `scipy.spatial.KDTree` and `networkx` to build the topology,
then converts to PyG format.

```{mermaid}
graph TD
    subgraph Build["create_graph.py"]
        GetXY["datastore.get_xy(stacked=False)<br/>→ xy (Nx, Ny, 2)"]
        MkMesh["mk_2d_graph(xy, n, n)<br/>grid + diagonal edges<br/>→ networkx.DiGraph"]
        MultiScale["Multi-scale levels<br/>nx=3 children per node<br/>nlev = log_3(max(Nx,Ny))"]
        G2MEdges["Grid→Mesh edges<br/>KDTree radius = 0.67 × mesh_spacing"]
        M2GEdges["Mesh→Grid edges<br/>4 nearest mesh neighbours per grid node"]
        SavePT["torch.save() → graphs/name/*.pt"]
        GetXY --> MkMesh --> MultiScale
        MultiScale --> G2MEdges & M2GEdges
        G2MEdges & M2GEdges --> SavePT
    end

    subgraph Files["Output Files"]
        F1["g2m_edge_index.pt  (2, N_g2m)"]
        F2["g2m_features.pt    (N_g2m, 3)  ← len, vdiff_x, vdiff_y"]
        F3["m2g_edge_index.pt  (2, N_m2g)"]
        F4["m2g_features.pt    (N_m2g, 3)"]
        F5["m2m_edge_index.pt  list[L] of (2, N_m2m_l)"]
        F6["m2m_features.pt    list[L] of (N_m2m_l, 3)"]
        F7["mesh_features.pt   list[L] of (N_mesh_l, 2)  ← x, y"]
    end

    subgraph HierFiles["Additional for --hierarchical"]
        H1["mesh_up_edge_index.pt    list[L-1]"]
        H2["mesh_down_edge_index.pt  list[L-1]"]
        H3["mesh_up_features.pt      list[L-1]"]
        H4["mesh_down_features.pt    list[L-1]"]
    end

    SavePT --> Files
    SavePT --> HierFiles

    style Build fill:#e8f5e9
    style Files fill:#f1f8e9
    style HierFiles fill:#e0f7fa
```

Edge features are 3-dimensional: `[edge_length, vdiff_x, vdiff_y]` (normalised by grid extent).
Mesh node features are 2-dimensional: `[x, y]` (normalised by `pos_max`).

**API:** {py:mod}`neural_lam.create_graph`

---

## 5. Model Class Hierarchy

All models share the same AR training loop from `ARModel` and the same encode-process-decode
scaffold from `BaseGraphModel`. Only `process_step()` differs between model variants.

```{mermaid}
graph TD
    subgraph MH["Model Hierarchy"]
        LM["pl.LightningModule"]
        AR["ARModel<br/>─────────────────────<br/>training_step / validation_step / test_step<br/>unroll_prediction()<br/>on_after_batch_transfer() — normalise<br/>configure_optimizers() — AdamW<br/>aggregate_and_plot_metrics()"]
        BG["BaseGraphModel<br/>─────────────────────<br/>predict_step() — full encode→process→decode<br/>get_clamped_new_state() — softplus/sigmoid clamp<br/>prepare_clamping_params()<br/>Loads graph buffers from .pt files"]
        BH["BaseHiGraphModel<br/>─────────────────────<br/>embedd_mesh_nodes() — per-level<br/>get_num_mesh() — sum across levels<br/>process_step() → hi_processor_step()"]
        GL["GraphLAM<br/>─────────────────────<br/>process_step() — N × InteractionNet<br/>pyg.nn.Sequential processor"]
        HL["HiLAM<br/>─────────────────────<br/>hi_processor_step()<br/>mesh_down_step() + mesh_up_step()<br/>Sequential down then up"]
        HP["HiLAMParallel<br/>─────────────────────<br/>hi_processor_step()<br/>Parallel down + up + same-level"]
        AR --> LM
        BG --> AR
        BH --> BG
        GL --> BG
        HL --> BH
        HP --> BH
    end

    style MH fill:#f5f5f5
```

**API:** {py:class}`~neural_lam.models.ar_model.ARModel` · {py:class}`~neural_lam.models.base_graph_model.BaseGraphModel` · {py:class}`~neural_lam.models.base_hi_graph_model.BaseHiGraphModel`

---

## 6. Encode → Process → Decode (GraphLAM)

`BaseGraphModel.predict_step()` implements the full forward pass for one AR step.

```{mermaid}
graph TD
    subgraph EPD["predict_step() — one AR step"]
        Input["prev_state (B,N_grid,d_state)<br/>prev_prev_state (B,N_grid,d_state)<br/>forcing (B,N_grid,d_forcing)<br/>grid_static_features (N_grid,d_static)"]

        subgraph Encode["ENCODE"]
            Cat["torch.cat → grid_features (B,N_grid,grid_dim)<br/>grid_dim = 2×d_state + d_static + d_forcing×window"]
            GridEmb["grid_embedder MLP<br/>→ grid_emb (B,N_grid,d_h)"]
            G2MEmb["g2m_embedder MLP<br/>→ g2m_emb (M_g2m,d_h)"]
            MeshEmb["embedd_mesh_nodes()<br/>→ mesh_emb (N_mesh,d_h)"]
            G2MGNN["g2m_gnn InteractionNet<br/>grid_emb → mesh_rep (B,N_mesh,d_h)"]
            GridMLP["encoding_grid_mlp + residual<br/>→ grid_rep (B,N_grid,d_h)"]
            Cat --> GridEmb --> G2MGNN
            G2MEmb --> G2MGNN
            MeshEmb --> G2MGNN
            GridEmb --> GridMLP
        end

        subgraph Process["PROCESS (GraphLAM: N × InteractionNet)"]
            M2MGNN["m2m_gnn × processor_layers<br/>mesh_rep → mesh_rep (B,N_mesh,d_h)"]
        end

        subgraph Decode["DECODE"]
            M2GEmb["m2g_embedder MLP<br/>→ m2g_emb (M_m2g,d_h)"]
            M2GGNN["m2g_gnn InteractionNet<br/>mesh_rep → grid_rep (B,N_grid,d_h)"]
            OutMap["output_map MLP (no LayerNorm)<br/>→ net_output (B,N_grid,d_grid_out)"]
        end

        Rescale["× diff_std + diff_mean<br/>→ rescaled_delta"]
        Clamp["get_clamped_new_state()<br/>new_state = prev_state + delta<br/>sigmoid clamp ]a,b[ or softplus clamp ]a,∞["]

        Input --> Cat
        G2MGNN --> M2MGNN
        GridMLP --> M2GGNN
        M2MGNN --> M2GGNN
        M2GEmb --> M2GGNN
        M2GGNN --> OutMap --> Rescale --> Clamp
    end

    style EPD fill:#f5f5f5
    style Encode fill:#e8f5e9
    style Process fill:#fff9c4
    style Decode fill:#e3f2fd
```

| Tensor | Shape | Description |
|---|---|---|
| `grid_features` | `(B, N_grid, grid_dim)` | Concatenation of prev/prev_prev state, forcing, static features |
| `grid_emb` | `(B, N_grid, d_h)` | Grid nodes projected to hidden dim |
| `mesh_rep` | `(B, N_mesh, d_h)` | Mesh latent after g2m encoding |
| `mesh_rep` (processed) | `(B, N_mesh, d_h)` | After N rounds of m2m message passing |
| `grid_rep` | `(B, N_grid, d_h)` | Grid features after m2g decoding |
| `rescaled_delta` | `(B, N_grid, d_state)` | Residual scaled by `diff_std + diff_mean` |
| `new_state` | `(B, N_grid, d_state)` | `prev_state + delta`, clamped to valid range |

```{note}
The model predicts a **residual delta** — `new_state = prev_state + delta`.
Output clamping uses **sigmoid** for bounded features (e.g. `r2m ∈ [0,1]`) and
**softplus** for lower/upper-only bounds (e.g. `t2m ≥ 0`).
Clamping is applied in the inverse-transformed space so the model learns unconstrained residuals.
```

**API:** {py:class}`~neural_lam.models.graph_lam.GraphLAM` · {py:class}`~neural_lam.interaction_net.InteractionNet`

---

## 7. Autoregressive Unrolling

`ARModel.unroll_prediction()` drives the AR loop. Boundary nodes are always overwritten with
ground-truth values to prevent error accumulation at the domain edges.

```{mermaid}
graph TD
    subgraph AR["unroll_prediction()"]
        Init["prev_prev = init_states[:,0]<br/>prev = init_states[:,1]"]
        Loop["for i in range(ar_steps)"]
        Forcing["forcing = forcing_features[:,i]"]
        Border["border_state = true_states[:,i]"]
        Pred["predict_step(prev, prev_prev, forcing)<br/>→ pred_state, pred_std"]
        Mask["new_state = boundary_mask × border_state<br/>         + interior_mask × pred_state"]
        Update["prev_prev = prev<br/>prev = new_state"]
        Collect["prediction_list.append(new_state)"]
        Stack["torch.stack → (B,ar_steps,N_grid,d_f)"]

        Init --> Loop --> Forcing & Border
        Forcing & Border --> Pred --> Mask --> Update --> Loop
        Mask --> Collect --> Stack
    end

    subgraph Loss["training_step / validation_step"]
        LossFn["self.loss(prediction, target, pred_std,<br/>mask=interior_mask_bool)<br/>→ scalar (mean over B and T)"]
        LogDict["log_dict: train_loss, val_loss_unrollN"]
    end

    Stack --> LossFn --> LogDict

    style AR fill:#fff9c4
    style Loss fill:#ffebee
```

**API:** {py:class}`~neural_lam.models.ar_model.ARModel` · {py:mod}`neural_lam.metrics`

---

## 8. HiLAM — Hierarchical Processing

HiLAM replaces the flat `process_step()` with a sequential down-then-up sweep through mesh levels.

```{mermaid}
graph TD
    subgraph HiProc["hi_processor_step() — repeated processor_layers times"]
        subgraph Down["mesh_down_step() — L → 0"]
            SameL["same_gnn[L](mesh_rep[L])<br/>intra-level at top"]
            DownL["down_gnn[l](mesh_rep[l+1] → mesh_rep[l])<br/>for l = L-1 … 0"]
            SameDown["same_gnn[l](mesh_rep[l])<br/>intra-level after each down step"]
            SameL --> DownL --> SameDown
        end

        subgraph Up["mesh_up_step() — 0 → L"]
            Same0["same_gnn[0](mesh_rep[0])<br/>intra-level at bottom"]
            UpL["up_gnn[l-1](mesh_rep[l-1] → mesh_rep[l])<br/>for l = 1 … L"]
            SameUp["same_gnn[l](mesh_rep[l])<br/>intra-level after each up step"]
            Same0 --> UpL --> SameUp
        end

        Down --> Up
    end

    style HiProc fill:#f5f5f5
    style Down fill:#e8f5e9
    style Up fill:#e3f2fd
```

| Tensor | Shape | Description |
|---|---|---|
| `mesh_rep[0]` | `(B, N_mesh_L0, d_h)` | Finest mesh level (output of g2m encoder) |
| `mesh_rep[l]` | `(B, N_mesh_Ll, d_h)` | Level `l` activations; coarser at higher `l` |
| `mesh_same_rep[l]` | `(B, M_same_l, d_h)` | Intra-level edge representations |
| `mesh_up/down_rep[l]` | `(B, M_up/down_l, d_h)` | Inter-level edge representations |

```{note}
{py:class}`~neural_lam.models.hi_lam_parallel.HiLAMParallel` uses the same graph files but runs
down, up, and same-level GNNs **in parallel** rather than sequentially.
Same architecture, different execution order.
```

**API:** {py:class}`~neural_lam.models.hi_lam.HiLAM` · {py:class}`~neural_lam.models.hi_lam_parallel.HiLAMParallel` · {py:class}`~neural_lam.models.base_hi_graph_model.BaseHiGraphModel`

---

## 9. InteractionNet — Message Passing Primitive

All GNN layers (g2m, m2m, m2g, up, down, same) use the same
{py:class}`~neural_lam.interaction_net.InteractionNet` building block.

```{mermaid}
graph TD
    subgraph IN["InteractionNet.forward(send_rep, rec_rep, edge_rep)"]
        Cat["torch.cat(edge_rep, x_j, x_i)<br/>→ edge_mlp → new_edge_rep"]
        Aggr["aggregate (sum/mean) new_edge_rep<br/>→ edge_rep_aggr (N_rec, d_h)"]
        NodeUp["torch.cat(rec_rep, edge_rep_aggr)<br/>→ aggr_mlp → rec_diff"]
        Res["rec_rep = rec_rep + rec_diff  (residual)"]
        Cat --> Aggr --> NodeUp --> Res
    end

    style IN fill:#ede7f6
```

- `edge_mlp`: `[3×d_h] → [d_h] × (hidden_layers+1)` with LayerNorm
- `aggr_mlp`: `[2×d_h] → [d_h] × (hidden_layers+1)` with LayerNorm
- Residual connections on both node and edge representations
- Optional `SplitMLPs` for chunked edge/node representations (used in HiLAM)

---

## 10. Loss Functions and Metrics

All metrics follow the same signature and are selected via `metrics.get_metric(name)`.

| Metric | Key | Formula |
|---|---|---|
| MSE | `mse` | `mean((pred - target)²)` |
| Weighted MSE | `wmse` | `mean((pred - target)² / σ²)` |
| MAE | `mae` | `mean(|pred - target|)` |
| Weighted MAE | `wmae` | `mean(|pred - target| / σ)` |
| NLL (Gaussian) | `nll` | `-log N(target; pred, σ²)` |
| CRPS (Gaussian) | `crps_gauss` | Closed-form Gaussian CRPS |

All metrics support:
- `mask` — boolean `(N_grid,)` to exclude boundary nodes
- `average_grid` — reduce over spatial dimension
- `sum_vars` — reduce over feature dimension

**API:** {py:mod}`neural_lam.metrics` · {py:mod}`neural_lam.loss_weighting`

---

## 11. Extension Points

| What to add | Where | Base class |
|---|---|---|
| New datastore (e.g. NetCDF) | `datastore/` — subclass and implement abstract methods | {py:class}`~neural_lam.datastore.base.BaseRegularGridDatastore` |
| Custom time sampling | `weather_dataset.py` — override `_slice_state_time` | `torch.utils.data.Dataset` |
| New flat model | `models/` — override `process_step()` | {py:class}`~neural_lam.models.base_graph_model.BaseGraphModel` |
| New hierarchical model | `models/` — override `hi_processor_step()` | {py:class}`~neural_lam.models.base_hi_graph_model.BaseHiGraphModel` |
| New loss / metric | `metrics.py` + register in `get_metric()` | — |
| New graph topology | `create_graph.py` or `weather-model-graphs` repo | — |

---

## 12. File Map

| Module | Description |
|---|---|
| {py:mod}`neural_lam.config` | Pydantic config schemas (`NeuralLAMConfig`, clamping, weighting) |
| {py:mod}`neural_lam.create_graph` | CLI — builds grid/mesh graphs from a datastore |
| {py:mod}`neural_lam.interaction_net` | `InteractionNet` and `SplitMLPs` message-passing primitives |
| {py:mod}`neural_lam.loss_weighting` | Per-variable and spatial loss-weight utilities |
| {py:mod}`neural_lam.metrics` | Metric factory — MSE, MAE, wMSE, wMAE, NLL, CRPS |
| {py:mod}`neural_lam.train_model` | Lightning training entry point |
| {py:mod}`neural_lam.utils` | MLP builders, graph loading, `rank_zero_print`, inverse activations |
| {py:mod}`neural_lam.vis` | Prediction and spatial-error visualisation |
| {py:mod}`neural_lam.weather_dataset` | `WeatherDataset` and `WeatherDataModule` |
| {py:mod}`neural_lam.datastore.base` | `BaseDatastore` and `BaseRegularGridDatastore` |
| {py:mod}`neural_lam.datastore.mdp` | `MDPDatastore` — mllam-data-prep zarr wrapper |
| {py:mod}`neural_lam.models.ar_model` | `ARModel` — base LightningModule, AR loop, loss, logging |
| {py:mod}`neural_lam.models.base_graph_model` | `BaseGraphModel` — encode-process-decode + output clamping |
| {py:mod}`neural_lam.models.base_hi_graph_model` | `BaseHiGraphModel` — hierarchical mesh embedding |
| {py:mod}`neural_lam.models.graph_lam` | `GraphLAM` — flat multi-scale model |
| {py:mod}`neural_lam.models.hi_lam` | `HiLAM` — sequential hierarchical model |
| {py:mod}`neural_lam.models.hi_lam_parallel` | `HiLAMParallel` — parallel hierarchical model |
