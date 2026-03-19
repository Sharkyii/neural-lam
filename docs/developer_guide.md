# Developer Guide

Neural-LAM is a repository of graph-based neural weather prediction models for Limited Area Modeling (LAM).
Global forecasting is also possible on a [separate branch](https://github.com/mllam/neural-lam/tree/prob_model_global).
The code uses [PyTorch](https://pytorch.org/) and [PyTorch Lightning](https://lightning.ai/pytorch-lightning).
GNNs are implemented with [PyG](https://pyg.org/) and logging via [Weights & Biases](https://wandb.ai/).

The repository contains LAM versions of:

- The graph-based model from [Keisler (2022)](https://arxiv.org/abs/2202.07575)
- GraphCast by [Lam et al. (2023)](https://arxiv.org/abs/2212.12794)
- The hierarchical model from [Oskarsson et al. (2023)](https://arxiv.org/abs/2309.17370)

---

## Publications

*If you use Neural-LAM in your work, please cite the relevant paper(s).*

### Graph-based Neural Weather Prediction for Limited Area Modeling

[arxiv.org/abs/2309.17370](https://arxiv.org/abs/2309.17370)

```bibtex
@inproceedings{oskarsson2023graphbased,
    title={Graph-based Neural Weather Prediction for Limited Area Modeling},
    author={Oskarsson, Joel and Landelius, Tomas and Lindsten, Fredrik},
    booktitle={NeurIPS 2023 Workshop on Tackling Climate Change with Machine Learning},
    year={2023}
}
```

See branch [`ccai_paper_2023`](https://github.com/joeloskarsson/neural-lam/tree/ccai_paper_2023) for the code that reproduces this paper.

### Probabilistic Weather Forecasting with Hierarchical Graph Neural Networks

[arxiv.org/abs/2406.04759](https://arxiv.org/abs/2406.04759)

```bibtex
@inproceedings{oskarsson2024probabilistic,
  title = {Probabilistic Weather Forecasting with Hierarchical Graph Neural Networks},
  author = {Oskarsson, Joel and Landelius, Tomas and Deisenroth, Marc Peter and Lindsten, Fredrik},
  booktitle = {Advances in Neural Information Processing Systems},
  volume = {37},
  year = {2024},
}
```

See branches [`prob_model_lam`](https://github.com/mllam/neural-lam/tree/prob_model_lam) and
[`prob_model_global`](https://github.com/mllam/neural-lam/tree/prob_model_global) for reproducibility.

---

## Modularity

Neural-LAM is designed to modularize models, graphs, and data so components can be swapped independently.

Restrictions to keep in mind:

- The graph must be compatible with the model (e.g. hierarchical model requires a hierarchical graph)
- Both graph and data are specific to the limited area under consideration

---

## Installation

### From PyPI

```bash
python -m pip install neural_lam
```

### From Source — using `uv` (recommended)

```bash
# 1. Clone the repo
git clone https://github.com/mllam/neural-lam
cd neural-lam

# 2. (Optional) install a specific torch variant first
uv pip install torch --index-url https://download.pytorch.org/whl/cpu
# or for CUDA 11.1:
uv pip install torch --index-url https://download.pytorch.org/whl/cu111

# 3. Install neural-lam (editable + dev deps recommended for contributors)
uv pip install --group dev -e .
```

### From Source — using `pip`

```bash
# 1. Clone the repo
git clone https://github.com/mllam/neural-lam
cd neural-lam

# 2. (Optional) install a specific torch variant first
python -m pip install torch --index-url https://download.pytorch.org/whl/cpu

# 3. Install
python -m pip install --group dev -e .
```

See [`.github/workflows/`](https://github.com/mllam/neural-lam/tree/main/.github/workflows) for all CI install variants as reference.

---

## Configuration

Every Neural-LAM command takes a `--config_path` pointing to a `config.yaml`. The parent directory of
that file becomes the root directory for all relative paths (graphs, datastore outputs, etc.).

Typical layout:

```
data/
├── config.yaml              # Neural-LAM config
├── danra.datastore.yaml     # Datastore config (referenced from config.yaml)
└── graphs/                  # Generated graph files
```

Example `config.yaml`:

```yaml
datastore:
  kind: mdp
  config_path: danra.datastore.yaml
training:
  state_feature_weighting:
    __config_class__: ManualStateFeatureWeighting
    weights:
      u100m: 1.0
      v100m: 1.0
      t2m: 1.0
      r2m: 1.0
  output_clamping:
    lower:
      t2m: 0.0
      r2m: 0
    upper:
      r2m: 1.0
```

The config controls:

1. Which datastore to use and where its config lives
2. Per-feature loss weighting (defaults to equal weights)
3. Output clamping ranges per feature (defaults to `]-∞, ∞[`)

---

## Data — Datastores and WeatherDataset

Data loading is split into two layers:

1. **Datastore** ({py:class}`~neural_lam.datastore.base.BaseDatastore`) — loads a category
   (`state`, `forcing`, `static`) and split (`train`/`val`/`test`) from disk, returning an
   `xr.DataArray` with a flat `grid_index` dimension and a `{category}_feature` dimension.
   Also provides variable names, units, boundary mask, normalisation stats, and grid info.

2. **WeatherDataset** ({py:class}`~neural_lam.weather_dataset.WeatherDataset`) — a
   `torch.utils.data.Dataset` that samples time windows from the datastore, normalises values,
   and returns `torch.Tensor` objects ready for training.

### MDPDatastore

Uses datasets prepared by [mllam-data-prep](https://github.com/mllam/mllam-data-prep) in zarr format.
All variable stacking, coordinate flattening, and normalisation stats are computed by `mllam-data-prep`.

Run preprocessing:

```bash
python -m mllam_data_prep --config data/danra.datastore.yaml
```

For large datasets (≥ 10 GB), parallelise with Dask:

```bash
python -m mllam_data_prep --config data/danra.datastore.yaml --dask-distributed-local-core-fraction 0.5
```

### NpyFilesDatastoreMEPS

Reads MEPS data from `.npy` files (the format from neural-lam `v0.1.0`).
Full MEPS dataset available [here](https://nextcloud.liu.se/s/meps).
A tiny example subset (`meps_example`) is in `example_data.zip` on
[Google Drive](https://drive.google.com/drive/folders/1N6ZT_mkfbdVloVsNs9T5YOrMtxd3jG-j?usp=sharing)
— useful for verifying your environment without training a real model.

After placing data, compute normalisation stats:

```bash
python -m neural_lam.datastore.npyfilesmeps.compute_standardization_stats <path-to-datastore-config>
```

Example datastore config for MEPS:

```yaml
# meps.datastore.yaml
dataset:
  name: meps_example
  num_forcing_features: 16
  var_names: [pres_0g, pres_0s, nlwrs_0, nswrs_0, r_2, r_65, t_2, t_65,
              t_500, t_850, u_65, u_850, v_65, v_850, wvint_0, z_1000, z_500]
  num_timesteps: 65
  step_length: 3
grid_shape_state: [268, 238]
projection:
  class_name: LambertConformal
  kwargs:
    central_latitude: 63.3
    central_longitude: 15.0
    standard_parallels: [63.3, 63.3]
```

### Custom Datastores

Subclass {py:class}`~neural_lam.datastore.base.BaseRegularGridDatastore` (regular grid) or
{py:class}`~neural_lam.datastore.base.BaseDatastore` (irregular) and implement the abstract methods:

```python
@property
def boundary_mask(self) -> xr.DataArray: ...

def get_dataarray(self, category: str, split: str) -> xr.DataArray: ...

def get_standardization_dataarray(self, category: str) -> xr.DataArray: ...

@property
def grid_shape_state(self) -> tuple[int, int]: ...

def get_xy(self, category: str, stacked: bool) -> np.ndarray: ...
```

See {py:class}`~neural_lam.datastore.mdp.MDPDatastore` for a complete reference implementation.

---

## Graph Creation

Graphs define the message-passing topology. Generate them with:

```bash
# GC-LAM (multiscale)
python -m neural_lam.create_graph --config_path data/config.yaml --name multiscale

# Hi-LAM / Hi-LAM-Parallel (hierarchical)
python -m neural_lam.create_graph --config_path data/config.yaml --name hierarchical --hierarchical

# L1-LAM (single level)
python -m neural_lam.create_graph --config_path data/config.yaml --name 1level --levels 1
```

### Graph Directory Format

```
graphs/
└── graph_name/
    ├── m2m_edge_index.pt       # Mesh-to-mesh edges
    ├── g2m_edge_index.pt       # Grid-to-mesh edges
    ├── m2g_edge_index.pt       # Mesh-to-grid edges
    ├── m2m_features.pt         # Static mesh edge features
    ├── g2m_features.pt         # Static g2m edge features
    ├── m2g_features.pt         # Static m2g edge features
    └── mesh_features.pt        # Static mesh node features
```

For hierarchical graphs (`L > 1`), additional files are included:

```
    ├── mesh_up_edge_index.pt   # Upward inter-level edges (list of length L-1)
    ├── mesh_down_edge_index.pt # Downward inter-level edges (list of length L-1)
    ├── mesh_up_features.pt
    └── mesh_down_features.pt
```

`m2m_edge_index.pt`, `m2m_features.pt`, and `mesh_features.pt` are lists of length `L`
(one entry per mesh level). Index 0 = lowest level.

---

## Training Models

```bash
python -m neural_lam.train_model --config_path data/config.yaml --model <model> --graph <graph> [options]
```

Key options:

| Flag | Description |
|---|---|
| `--model` | Model to train: `graph_lam`, `hi_lam`, `hi_lam_parallel` |
| `--graph` | Graph name (must match a directory under `graphs/`) |
| `--epochs` | Number of training epochs |
| `--processor_layers` | Number of GNN layers in the processing block |
| `--ar_steps_train` | AR unroll steps during training |
| `--ar_steps_eval` | AR unroll steps during validation |

Checkpoints are saved to `saved_models/`.

### Graph-LAM

Encode-process-decode with a mesh graph. Used for both L1-LAM and GC-LAM (different graphs only).

```bash
python -m neural_lam.train_model --model graph_lam --graph 1level ...
python -m neural_lam.train_model --model graph_lam --graph multiscale ...
```

### Hi-LAM

Hierarchical mesh graph with sequential up/down message passing.

```bash
python -m neural_lam.train_model --model hi_lam --graph hierarchical ...
```

### Hi-LAM-Parallel

Same as Hi-LAM but up-sweep, process, and down-sweep run in parallel.

```bash
python -m neural_lam.train_model --model hi_lam_parallel --graph hierarchical ...
```

### Multi-GPU / HPC

Neural-LAM uses PyTorch Lightning's DDP backend. On SLURM:

```bash
#!/bin/bash -l
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=4
#SBATCH --gres:gpu=4

srun -ul python -m neural_lam.train_model \
    --config_path /path/to/config.yaml \
    --num_nodes $SLURM_JOB_NUM_NODES
```

Without SLURM, select GPUs with `--devices 0 1`.

---

## Evaluating Models

```bash
python -m neural_lam.train_model --config_path data/config.yaml --eval val --load path/to/model.ckpt
python -m neural_lam.train_model --config_path data/config.yaml --eval test --load path/to/model.ckpt
```

Key eval options:

| Flag | Description |
|---|---|
| `--load` | Path to `.ckpt` checkpoint file |
| `--eval` | `val` or `test` |
| `--n_example_pred` | Number of example predictions to plot |
| `--ar_steps_eval` | AR unroll steps during evaluation |

```{note}
Use a single GPU for evaluation. Multi-GPU evaluation with `DistributedSampler` can replicate
samples and produce unreliable metrics.
```

---

## Logging

### Weights & Biases

W&B is the default logger. Training config, metrics, and plots are sent to W&B servers.

```bash
wandb login   # enable W&B
wandb off     # log locally only (saved to wandb/dryrun...)
```

Change the project name via `--wandb_project` in the training command.

### MLFlow

Switch to MLFlow with `--logger mlflow`. Set the tracking URI:

```bash
MLFLOW_TRACKING_URI=http://localhost:5000 python -m neural_lam.train_model \
    --config_path data/config.yaml --logger mlflow
```

---

## Development Setup

```bash
git clone https://github.com/mllam/neural-lam
cd neural-lam
uv pip install --group dev -e .

# Install pre-commit hooks
pre-commit install
```

### Running Tests

```bash
pdm run pytest
pdm run pytest tests/test_datasets.py -v
pdm run pytest --cov=neural_lam --cov-report=term-missing
```

### Code Style

| Tool | What it checks |
|---|---|
| `black` | Formatting (line length 80) |
| `isort` | Import ordering |
| `flake8` | Style and lint |
| `mypy` | Type annotations |
| `pydocstyle` | Docstring style (NumPy convention) |
| `interrogate` | Docstring coverage (≥ 50%) |

```bash
pre-commit run --all-files
```

Any push or PR to `main` triggers these checks automatically. Failures reject the push.

---

## Writing Docstrings

Neural-LAM uses **NumPy-style** docstrings. Napoleon parses them into the API reference automatically.

### Function

```python
def compute_loss(pred: torch.Tensor, target: torch.Tensor) -> torch.Tensor:
    """Compute weighted MSE loss between prediction and target.

    Parameters
    ----------
    pred : torch.Tensor
        Predicted values, shape (B, N_grid, d_state).
    target : torch.Tensor
        Ground-truth values, shape (B, N_grid, d_state).

    Returns
    -------
    torch.Tensor
        Scalar loss value.
    """
```

### Class

```python
class MyDatastore(BaseRegularGridDatastore):
    """Custom datastore backed by NetCDF files.

    Parameters
    ----------
    path : str
        Root directory containing the NetCDF files.
    config : NeuralLAMConfig
        Parsed configuration object.
    """
```

### With Raises and Examples

```python
def get_dataarray(self, category: str, split: str):
    """Return an xarray DataArray for the requested category and split.

    Parameters
    ----------
    category : str
        One of ``"state"``, ``"forcing"``, or ``"static"``.
    split : str
        One of ``"train"``, ``"val"``, or ``"test"``.

    Returns
    -------
    xr.DataArray
        Array with dimensions ``(time, grid_index, feature)``.

    Raises
    ------
    ValueError
        If ``category`` or ``split`` is not recognised.

    Examples
    --------
    >>> ds = MyDatastore("data/", config)
    >>> da = ds.get_dataarray("state", "train")
    >>> da.dims
    ('time', 'grid_index', 'state_feature')
    """
```

Validate locally:

```bash
pdm run pydocstyle neural_lam/ --convention=numpy --add-ignore=D100,D104,D105
pdm run interrogate neural_lam/ --fail-under 50 --verbose
```

---

## Adding a New Model

1. Subclass {py:class}`~neural_lam.models.base_graph_model.BaseGraphModel`
2. Override `_build_graph_model()` to wire up your GNN layers
3. The base class handles graph loading, output clamping, and the AR loop

For hierarchical models, subclass {py:class}`~neural_lam.models.base_hi_graph_model.BaseHiGraphModel`
and implement the up/down sweep methods.

```{mermaid}
graph TD
    subgraph ModelHierarchy["Model Class Hierarchy"]
        LM["pytorch_lightning.LightningModule"]
        AR["ARModel<br/>training_step, validation_step"]
        BG["BaseGraphModel<br/>predict_step, graph loading"]
        BH["BaseHiGraphModel<br/>up/down sweep helpers"]
        GL["GraphLAM"]
        HL["HiLAM"]
        HP["HiLAMParallel"]
        AR --> LM
        BG --> AR
        BH --> BG
        GL --> BG
        HL --> BH
        HP --> BH
    end
    style ModelHierarchy fill:#f5f5f5
```

---

## Adding a New Metric or Loss

Add to {py:mod}`neural_lam.metrics` following the existing pattern, then register in `get_metric()`:

```python
def my_metric(pred, target, pred_std, mask=None, average_grid=True, sum_vars=True):
    """Compute my custom metric.

    Parameters
    ----------
    pred : torch.Tensor
        Shape ``(..., N, d_state)``.
    target : torch.Tensor
        Shape ``(..., N, d_state)``.
    pred_std : torch.Tensor
        Shape ``(..., N, d_state)`` or ``(d_state,)``.
    mask : torch.Tensor or None
        Boolean interior mask, shape ``(N,)``.

    Returns
    -------
    torch.Tensor
        Reduced metric value.
    """
    ...
```

---

## Building Docs Locally

```bash
jupyter-book build docs/
xdg-open docs/_build/html/index.html   # Linux
open docs/_build/html/index.html       # macOS
```

---

## CI Pipeline

```{mermaid}
graph TD
    subgraph CI["GitHub Actions"]
        PR["Pull Request / Push"]
        subgraph BuildDocs["docs.yaml"]
            Lint["interrogate + pydocstyle"]
            Validate["validate_docs.py"]
            Build["jupyter-book build"]
            Upload["Upload artifact"]
            Lint --> Validate --> Build --> Upload
        end
        subgraph Deploy["deploy-docs (main only)"]
            Pages["Deploy to GitHub Pages"]
        end
        subgraph Tests["install-and-test.yml"]
            PyTest["pytest"]
        end
        PR --> BuildDocs
        PR --> Tests
        Upload --> Deploy
    end
    style CI fill:#e3f2fd
    style BuildDocs fill:#e8f5e9
    style Deploy fill:#f3e5f5
    style Tests fill:#fff9c4
```

---

## Project Layout

```
neural-lam/
├── neural_lam/
│   ├── datastore/
│   │   ├── base.py              # Abstract datastore interfaces
│   │   ├── mdp.py               # MDPDatastore (zarr / mllam-data-prep)
│   │   └── npyfilesmeps/        # MEPS numpy-file datastore
│   ├── models/
│   │   ├── ar_model.py          # ARModel LightningModule
│   │   ├── base_graph_model.py  # Encode-process-decode scaffold
│   │   ├── base_hi_graph_model.py
│   │   ├── graph_lam.py
│   │   ├── hi_lam.py
│   │   └── hi_lam_parallel.py
│   ├── config.py                # Pydantic config schemas
│   ├── interaction_net.py       # InteractionNet GNN module
│   ├── metrics.py               # Loss and metric functions
│   ├── train_model.py           # Training entry point
│   ├── utils.py                 # Shared helpers
│   └── weather_dataset.py       # WeatherDataset
├── docs/
│   ├── _config.yml
│   ├── _toc.yml
│   ├── intro.md
│   ├── architecture.md
│   ├── developer_guide.md
│   ├── tutorials/
│   └── scripts/
├── tests/
├── .github/workflows/
│   └── docs.yaml
└── pyproject.toml
```

---

## Contact

- [mllam Slack](https://join.slack.com/t/ml-lam/shared_invite/zt-2t112zvm8-Vt6aBvhX7nYa6Kbj_LkCBQ) — open to anyone
- [GitHub Issues](https://github.com/mllam/neural-lam/issues)
