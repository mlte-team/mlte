# `MLTE`: Machine Learning Test and Evaluation

<img src="https://raw.githubusercontent.com/mlte-team/mlte/master/assets/MLTE_Logo_Color.svg" alt="mlte_logo" width="150"/>

`MLTE` (pronounced "melt") is a framework and infrastructure for evaluating machine learning models and systems. To get started with the `MLTE` Python package, continuing reading below. The `MLTE` framework can be found in the <a href="https://mlte.readthedocs.io/en/latest/" target="_blank">documentation</a>, along with a more in-depth guide to <a href="https://mlte.readthedocs.io/en/latest/using_mlte/" target="_blank">using `MLTE`</a> that expands on the quick start guide below. For examples of use cases, see the <a href="https://github.com/mlte-team/mlte/tree/master/demo" target="_blank">demo folder</a>. 

![Version Badge](https://img.shields.io/badge/release-v2.0.0-e19b38)
[![Python](https://img.shields.io/pypi/pyversions/mlte.svg)](https://badge.fury.io/py/mlte)
[![Code Style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Tests](https://github.com/mlte-team/mlte/actions/workflows/ci.yaml/badge.svg)](https://github.com/mlte-team/mlte/actions/workflows/ci.yaml)
[![Documentation Status](https://readthedocs.org/projects/mlte/badge/?version=latest)](https://mlte.readthedocs.io/en/latest/?badge=latest)

## Quick Start

The `MLTE` Python package is available on <a href="https://pypi.org/project/mlte/" target="_blank">PyPI</a>, and the `MLTE` framework is described in our <a href="https://mlte.readthedocs.io/en/latest/" target="_blank">documentation</a>. Install the latest version of the package with pip or conda:

```bash
$ pip install mlte
```

### Running `MLTE`

The `MLTE` web-based user interface (UI) allows you to create/edit system artifacts and review existing models and test catalogs. To access the UI, first start the backend server with the following command:

```bash
$ mlte backend
```

There are a number of flags that can be used to specify parameters; see the backend section of the <a href="https://mlte.readthedocs.io/en/latest/using_mlte/" target="_blank">using `MLTE`</a> page for details. The default artifact store puts artifacts into a non-persistent, in-memory store. For example, running the backend with a store located in a folder called `store` relative to the folder where you are running `MLTE` would use the following command:

  ```bash
    $ mlte backend --store-uri fs://store
  ```

Once the backend is running, you can run the UI with the following command:

```bash
$ mlte ui
```

After this, go to the hosted address (defaults to `http://localhost:8000`) to view the `MLTE` UI homepage. You will need to log in to access the functionality in the UI, which you can do by using the default user. You can later use the UI to set up new users as well.

**NOTE**: you should change the default user's password as soon as you can, if you are not on a local setup.

* Default user: admin
* Default password: admin1234

### Setting up a `MLTE` session

Before most operations can be done on `MLTE`, a context and artifact store need to be set via ``set_context("model_name", "model_version")`` and ``set_store("store_uri")``, which can be imported as follows:

```python
from mlte.session import set_context, set_store
```
``set_context()`` indicates the model and version being used for the script, and can be any string. ``set_store()`` indicates the location of the artifact store being used, with four store type options described in the <a href="https://mlte.readthedocs.io/en/latest/using_mlte/" target="_blank">documentation</a>. The MLTE context and artifact store can alternatively be set by environment variables before starting the script (``MLTE_CONTEXT_MODEL``, ``MLTE_CONTEXT_VERSION``, ``MLTE_ARTIFACT_STORE_URI``, and ``MLTE_CUSTOM_LIST_STORE_URI_VAR``), and can later be overridden using the set methods above.

## Next Steps

The `MLTE` Python package is best used in conjunction with the <a href="https://mlte.readthedocs.io/en/latest/" target="_blank">framework</a>. For more details on using the package, see our documentation page on <a href="https://mlte.readthedocs.io/en/latest/using_mlte/" target="_blank">using `MLTE`</a>.

### Citing This Work

If you're interested in learning more about this work, you can read our <a href="https://ieeexplore.ieee.org/document/10173876" target="_blank">paper</a>. While not required, it is highly encouraged and greatly appreciated if you cite our paper when you use `MLTE` for academic research.

```
@INPROCEEDINGS{10173876,
  author={Maffey, Katherine R. and Dotterrer, Kyle and Niemann, Jennifer and Cruickshank, Iain and Lewis, Grace A. and Kästner, Christian},
  booktitle={2023 IEEE/ACM 45th International Conference on Software Engineering: New Ideas and Emerging Results (ICSE-NIER)}, 
  title={MLTEing Models: Negotiating, Evaluating, and Documenting Model and System Qualities}, 
  year={2023},
  volume={},
  number={},
  pages={31-36},
  keywords={Measurement;Machine learning;Production;Organizations;Software;Stakeholders;Software engineering;machine learning;test and evaluation;machine learning evaluation;responsible AI},
  doi={10.1109/ICSE-NIER58687.2023.00012}
}
```