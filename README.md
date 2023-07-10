## `mlte`: Machine Learning Test and Evaluation

`mlte` (pronounced "melt") is a toolkit for machine learning testing and evaluation.

[![Tests](https://github.com/turingcompl33t/mlte/actions/workflows/ci.yaml/badge.svg)](https://github.com/turingcompl33t/mlte/actions/workflows/ci.yaml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

### Getting Started

`mlte` is available on [PyPI](https://pypi.org/project/mlte-python/). Install the latest version with:

```bash
$ pip install mlte-python
```

Read the [documentation](https://mlte.readthedocs.io/en/latest/) for more details on getting started with `mlte`.

### Working Notes

07/10/2023

- Today I refactored the management of the MLTE context. I made the context itself a plain old data structure and then set up the global state management system to manage a singleton instance of this context. I want to make it such that, wherever possible, this context is merely injected into individual artifacts (classes) instead of being access directly within the class instance itself (e.g. within methods). This will improve the overall engineering quality of the library and make testing easier.
- Tomorrow I don't want to get bogged down in refactoring all of the existing code to this new injection system. Instead, I need to work on the artifact protocol itself. Getting this ironed out will elide much of the refactor that needs to happen. I need to establish the manner in which artifact-specific data is injected into the overall serialization logic for the artifact.
