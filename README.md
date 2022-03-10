## `mlte`: Machine Learning Testing and Evaluation

`mlte` (pronounced "melt") is a toolkit for machine learning testing and evaluation.

[![Tests](https://github.com/turingcompl33t/mlte/actions/workflows/tests.yaml/badge.svg)](https://github.com/turingcompl33t/mlte/actions/workflows/tests.yaml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

### Installation

```bash
$ pip install mlte-python
```

### Usage

A simple example that measures the CPU utilization of a local model training process:

```python
from mlte.properties.cpu import ProcessLocalCPUUtilization

pid = spawn_training_process()
cpu = ProcessLocalCPUUtilization()

metrics = cpu(pid)
print(metrics)
```
