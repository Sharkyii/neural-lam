# Neural-LAM Documentation

Neural-LAM is a repository of graph-based neural weather prediction models for Limited Area Modeling (LAM).
Built on [PyTorch](https://pytorch.org/), [PyTorch Lightning](https://lightning.ai/pytorch-lightning), and [PyG](https://pyg.org/).

---

## Navigate the Docs

::::{grid} 2
:::{grid-item-card} Architecture
:link: architecture
:link-type: doc
System overview, datastore hierarchy, graph construction, encode-process-decode, HiLAM, and the full tensor contract.
:::
:::{grid-item-card} Developer Guide
:link: developer_guide
:link-type: doc
Installation, configuration, datastores, graph creation, training, evaluation, logging, and contributing.
:::
:::{grid-item-card} Tutorials
:link: tutorials/01_getting_started
:link-type: doc
Step-by-step notebooks: getting started, data preparation, graph creation, and advanced training.
:::
:::{grid-item-card} API Reference
:link: autoapi/index
:link-type: doc
Auto-generated docs for every public module, class, and function in `neural_lam`.
:::
::::

---

## Quick Start

```bash
pip install neural-lam
```

For development:

```bash
git clone https://github.com/mllam/neural-lam
cd neural-lam
uv pip install --group dev -e .
```

Train a model:

```bash
python -m neural_lam.create_graph --config_path data/config.yaml --name multiscale
python -m neural_lam.train_model --config_path data/config.yaml --model graph_lam --graph multiscale
```

---

## Tutorials

- {doc}`tutorials/01_getting_started`
- {doc}`tutorials/02_data_preparation`
- {doc}`tutorials/03_graph_creation`
- {doc}`tutorials/04_training_advanced`

---

## Source

[github.com/mllam/neural-lam](https://github.com/mllam/neural-lam)
