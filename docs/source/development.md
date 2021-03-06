# Development

This document describes some of the development practices used within `mlte`.

## Quickstart

Create a Python virtual environment and install the required development packages:

```bash
$ python -m venv env
$ source ./env/bin/activate
$ pip install -r requirements_dev.txt
```

Now you are ready to start working on `mlte`!

## Source Formatting

We format all Python code in this project with the [`black`](https://github.com/psf/black) source formatter. Assuming you have followed the instructions in the [Quickstart](#quickstart), you can run the formatter locally with:

```bash
$ make format
```

This works on UNIX-like systems (or anywhere `make` is available). Alternatively, you can run `black` manually from the project root:

```bash
$ black src/
$ black test/
```

Code that does not satisfy the formatter will be rejected from pull requests.

## Source Linting

We lint all Python code in this project with the [`flake8`](https://flake8.pycqa.org/en/latest/) source linter. Assuming you have followed the instructions in the [Quickstart](#quickstart), you can run the linter locally with:

```bash
$ make lint
```

This works on UNIX-like systems (or anywhere `make` is available). Alternatively, you can run `flake8` manually from the project root:

```bash
$ flake8 src/
$ flake8 test/
```

Code that does not satisfy the linter will be rejected from pull requests.

## Static Type Checking

We run static type-checking with [`mypy`](http://mypy-lang.org/). Assuming you have followed the instructions in the [Quickstart](#quickstart), you can run the type-checker locally with:

```bash
$ make typecheck
```

This works on UNIX-like systems (or anywhere `make` is available). Alternatively, you can run `mypy` manually from the project root:

```bash
$ mypy src/
$ mypy test/
```

Code that does not satisfy static type-checking will be rejected from pull requests.

## Unit Tests

We unit test the `mlte` library with the [`pytest`](https://docs.pytest.org/en/7.0.x/contents.html) package and [`tox`](https://tox.wiki/en/latest/). The former is a test-runner for Python while the latter is a tool for environment isolation and automation. Assuming you have followed the instructions in the [Quickstart](#quickstart), you can run unit tests locally with:

```bash
$ make test
```

This works on UNIX-like systems (or anywhere `make` is available). Alternatively, you can run `tox` manually from the project root:

```bash
$ tox --develop
```

Unit tests failures result in build failures in CI.

## Continuous Integration

We utilize [Github Actions](https://docs.github.com/en/actions) for continuous integration.

## Documentation

We build documentation with [`sphinx`](https://www.sphinx-doc.org/en/master/) and host documentation on [ReadTheDocs](https://readthedocs.org/).

We maintain a separate set of requirements for building the documentation under `docs/requirements.txt`. To build the documentation locally, create a new virtual environment and install the requirements from this listing:

```bash
$ cd docs
$ python -m venv env
$ source ./env/bin/activate
$ pip install -r requirements.txt
```

Now you can build the documentation with:

```bash
$ make html
```

## Versioning

We follow semantic versioning when versioning the `mlte` package. We use [`bump2version`](https://github.com/c4urself/bump2version) to consistently update versions across the project. A configuration file is provided in `.bumpversion.cfg` at the root of the project.

Bumping the version for a new release can be accomplished with:

```bash
$ bumpversion patch
```

where `patch` may be replaced with `minor` or `major` as appropriate for the release.

## Publishing

We publish the `mlte` package on [PyPi](https://pypi.org/). The current procedure we follow for publication is described below.

Ensure you have properly incremented the version for the new release, as described in Versioning above.

Create the source distribution and the wheel:

```bash
$ python setup.py sdist bdist_wheel
```

Check the package contents with `twine`:

```bash
twine check dist/*
```

Manually check the contents of the source distribution (optional):

```bash
$ cd dist/
$ tar tzf mlte-0.0.0.tar.gz
```

Upload the package to [`TestPyPi`](https://test.pypi.org/) to verify that the package appears as expected:

```bash
$ twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```

Finally, upload the package to `PyPi`:

```
$ twine upload dist/*
```
