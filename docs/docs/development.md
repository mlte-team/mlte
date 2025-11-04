# Development

This document describes some of the development practices used in `MLTE`.

## Quick Start

The best examples of how to use MLTE are contained with in the [Demos](#demos). If looking to get started on development, these are the best place to start to get a feel for how the tool works. The code within the demos walks through the MLTE library IMT process. These can be ran after making a virtual environment and installing `MLTE` along with the demo dependencies.

```bash
$ pyenv install 3.12
$ pyenv local 3.12
$ make venv
```

The other part of MLTE is the frontend and backend. These are used for the SDMT process, and visualing results from the IMT process. This can be setup as explained in the demo section by using the `demo/run_environment.sh` script. This will start `MLTE` as 3 docker containers with an RDBS based backend. The frontend will be available at `localhost:8000` and will include a sample model, version, and negotiation card.

```bash
cd demo && bash run_environment.sh
```

All issue tracking for MLTE is done in this <a href="https://github.com/orgs/mlte-team/projects/5" target="_blank">Github Project</a> [Github Project].

Once changes have been made, `make qa` and `make test` should be ran to ensure that code fits QA standards and all unit tests pass. If just making python changes, `make qa-python` can be used to instead of `make qa` to reduce runtime by not running QA on the frontend.

## Setup

### Python Version Support

Currently, `MLTE` supports Python versions between `3.9` and `3.12`, both included.

If you do not have one of these versions installed, or you want to target a specific version that is not your default, `pyenv` can be used to manage multiple Python versions locally. Note that this is optional, and only needed if you have a not-supported default Python version. To set up a specific version of Python with `pyenv`:

- Install `pyenv` as described in this link: https://github.com/pyenv/pyenv
- Install the desired Python version (in this example, 3.12):

```bash
$ pyenv install 3.12
```

- While inside the root repository folder, run this command to set that Python version to be used when executed in that folder:

```bash
$ pyenv local 3.12
```

- You can use `python --version` to check if it worked.

### Requirements

 - `MLTE` uses `poetry` (v 2.0.1 or higher) to handle the required runtime and development packages. You can install `poetry` on your system with the instructions available here: https://python-poetry.org/docs/#installation

### Dev Environment Setup

You will need to set up a virtual Python environment where `poetry` will work, and install all dependencies there. The easiest way to do this, installing all dependencies, is to run this command:

```bash
$ make venv
```

If you want more control over what is being installed, you can do it manually instead. While inside the root of the repository, execute these commands (which do not install the demo dependencies):

```bash
$ python -m venv .venv
$ poetry install --with dev --all-extras
```

Now you are ready to start working on `MLTE`!

### Demos

There are several demos available in the `demo\` folder, as Jupyter notebooks. To run them, you need to install their dependencies first if you created the environment manually; otherwise they have already been installed for you. To install them manually. run:

```bash
$ poetry install --with demo
```

You can go to the Jupyter notebooks in the subfolders inside the `demo\` folder and try them out in order to see how MLTE works. This assumes you are running the Jupyter notebooks from the same virtual environment that was just set up in the step above.

If you want to run the frontend UI and backend in an environment that will allow you to see the results of the artifacts created by the demos, you can run the following script, which will run them inside a container and point them to the proper store:

```bash
$ cd demo
$ bash run_environment.sh
```

#### Creating a new Demo

A demo is a set of Jupyter notebooks that walk through the MLTE IMT process. Demos are to be named and populated as follows. The number naming is used to signify the order in which the notebooks should be ran.

0. `all notebooks`
    - All notebooks will have to connect setup the `MLTE` context before their operation. This is done by importing the session module, `from demo.scenarios.session import *`
    - All files outside of notebooks including data, or re-used functionality should be included within the demo folder
1. `1_requirements.ipynb`
    - Defines the  `MLTE` [Negotiation Card](negotiation_card.md), an example card can be found at `./demo/sample_store/models/OxfordFlower/card.default.json`
    - Defines the `TestSuite`, more `TestSuite` information can be found in [Using `MLTE`](using_mlte.md#testing-models-with-`mlte`-(imt-and-sdmt))
2. `2a_evidence_<quality_attribute> - 2<x>_evidence_<quality_atribute>`
    - Naming of match the scheme, for example `2a_evidence_fairness`, `2b_evidence_robustness`, `2c_evidence_performance`.
    - Gather the evidence for all `TestCase` in the `TestSuite`. Each notebook should gather evidence for all of the `TestCase`s that relate to the quality attribute in the name of the notebook.
    - Each of these notebooks will be used as an entry in the Sample Test Catalog to give an example of the `Test Case`s evaluated in the notebook. The second cell must contain a JSON block with information that will be used to populate the Test Catalog entry. All fields are required.
        ```json
        {
            "tags": ["General"],
            "quality_attribute": "Detect OOD inputs and shifts in output",
            "description": "During normal operation, the ML pipeline will log errors when out of distribution data is observed. The ML pipeline will create a log entry with a tag. During normal operation, ML pipeline will log errors when the output distribution changes. The ML pipeline will create a log entry with a tag.",
            "inputs": "Existing ML model, sample image data that has out of bounds input, and that produces output confidence error",
            "output": "Log with input issues tagged",
        }
        ```
3. `3_report.ipynb`
    - Create a `TestSuiteValidator` and validate the evidence collected.
    - Generate a report to communicate the results of the evaluation.

All other files related to the new demo including data 

#### Populating the Test Catalog

When demo notebooks have been created or edited and need to be added to the sample test catalog, it can be done automatically with the following command. This requires the demo dependencies to be installed and will go through all demos to update the entire sample catalog.

```bash
$ make build-sample-catalog
```

## Project Development Commands

You can run most project commands (e.g., format sources, lint) in two ways: using the commands in the included Makefile, or running things manually. Using the Makefile works on UNIX-like systems (or anywhere `make` is available), and is shorter to type. Alternatively, you can run each command manually. The sections below describe how to run commands in both ways.

Also, the commands below do not assume that you have your virtual environment enabled. Calling `poetry run` ensures things run in the current virtual environment even if it is not activated. If you manually activate your virtual environment you can run all the commands below without the `poetry run` prefix. 

To manually activate your environment, run:

```bash
$ source .venv/bin/activate
```

### Make Overview

There are a couple of shorthand commands in the Makefile to run several of the below commands at the same time. The most useful ones include:

* `make qa`: executes the schema generation, doc check, source sorting, formatting, linting, and static type checking commands of frontend and backend.
* `make check-qa`: executes the schema check, doc check, source sorting check, formatting check, linting check, and static type checking commands of frontend and backend.
* `make ci`: executes the same commands as `check-qa`, but also runs `test` to execute the unit tests, cleaning caches first to better simulate execution in a CI environment.

`make qa` and `make test` should be ran before every push to ensure that the changes made adhere to the QA standards and will pass the unit tests. These two encapsulate all of the commands below that are generally applicable.

### Import Sorting

We sort all Python import code in this project with <a href="https://github.com/PyCQA/isort" target="_blank">`isort`</a>. You can run this locally with:

```bash
$ make isort
```

If you just want to check the sorting of the imports, without making any changes, you can run this:

```bash
$ make check-isort
```

Code that does not satisfy the sorter will be rejected from pull requests.

### Source Formatting

We format all Python code in this project with the <a href="https://github.com/psf/black" target="_blank">`black`</a> source formatter. You can run the formatter locally with:

```bash
$ make format
```

If you just want to check the format, without making any changes, you can run this:

```bash
$ make check-format
```

Code that does not satisfy the formatter will be rejected from pull requests.

### Source Linting

We lint all Python code in this project with the <a href="https://flake8.pycqa.org/en/latest/" target="_blank">`flake8`</a> source linter. You can run the linter locally with:

```bash
$ make lint
```

Code that does not satisfy the linter will be rejected from pull requests.

### Static Type Checking

We run static type-checking with <a href="http://mypy-lang.org/" target="_blank">`mypy`</a>. You can run the type-checker locally with:

```bash
$ make typecheck
```

Code that does not satisfy static type-checking will be rejected from pull requests.

### Doc Generation

More details in the [Documentation](#documentation) section, but to run document generation from the make command, run this: 

```bash
$ make docs
```

### Unit Tests

We unit test the `MLTE` library with the <a href="https://docs.pytest.org/en/7.0.x/contents.html" target="_blank">`pytest`</a> package, a test runner for Python. You can run unit tests locally with:

```bash
$ make test
```

Unit test failures result in build failures in CI.

To test the Juypter notebooks present in the demo folders, run:

```bash
$ make demo-test
```

### Model Schema Generation

The artifacts used by `MLTE` have schemas that are used to validate them. These schemas need to be updated if their internal structure (code) changes. You can do this locally with:

```bash
$ make schema
```

If you just want to check the schemas, without making any changes, you can run this:

```bash
$ make check-schema
```

Schema failures result in build failures in CI.

### Front End Formatting and Linting

We format and lint all .vue, .js, and .ts files with <a href="https://eslint.org/" target="_blank">ESLint</a>, which can be run from the root of the repository with:

```bash
$ make lint-frontend
```

Or manually from the root of the nuxt application:

```bash
$ npm run lint
```

### Front End Static Type Checking
All typescript code takes advantage of static typing. This type checking can be done by running the following command from the root of the repository:

```bash
$ make typecheck-frontend
```

Or manually from the root of the nuxt application:

```bash
$ npx vue-tsc
```

## Front End

Front end development requires Node.js. The front end was developed using v20.11.0; the latest LTS version can be found <a href="https://nodejs.org/en" target="_blank">here</a>.

To initialize the development environment for the front end, navigate to the subfolder `./mlte/frontend/nuxt-app` and run:

```bash
$ npm install
$ npx gulp init
```

You can also run the following make command:

```bash
$ make frontend-env
```

Now the environment is set up and the front end can be run with the following command:

```bash
$ npm run dev
```

This will run the front end at `http://localhost:3000`. The backend can be run with a command like this one (using a file system store, in the local ./store folder):

```bash
$ mlte backend --store-uri fs://store
```

## Continuous Integration

We utilize <a href="https://docs.github.com/en/actions" target="_blank">GitHub Actions</a> for continuous integration.

## Documentation

We build documentation with <a href="https://www.mkdocs.org" target="_blank">`mkdocs`</a> and host documentation on <a href="https://readthedocs.org/" target="_blank">ReadTheDocs</a>. A webhook is set up in the `MLTE` repository to trigger an integration effect on ReadTheDocs when certain changes to the repo are made.

You can build and serve the documentation with the following command, when run from inside the `docs/` folder:

```bash
$ mkdocs serve
```

You can preview the documentation accessing <a href="http://127.0.0.1:8000/" target="_blank">http://127.0.0.1:8000/</a> on your browser.

## Versioning and Publishing

### Versioning

We follow semantic versioning when versioning the `MLTE` package. We use <a href="https://github.com/c4urself/bump2version" target="_blank">`bump2version`</a> to consistently update versions across the project. A configuration file is provided in `.bumpversion.cfg` at the root of the project.

Bumping the version for a new release can be accomplished with:

```bash
$ make bump-patch
```

or

```bash
$ make bump-minor
```

or

```bash
$ make bump-major
```

depending on whether you want to update the `patch`,`minor` or `major` version as appropriate for the release. NOTE: bumpversion will change all instances of the current version's text to the new version's text in the files it has been configured to do so, so if you have other text in these files which happens to match the current version's, it will be incorrectly changed. Manually inspect changes after running this tool, and discard any incorrect ones.

### Publishing

We publish the `MLTE` package on <a href="https://pypi.org/" target="_blank">PyPi</a>. Ensure you have properly incremented the version for the new release, as described in [Versioning](#versioning).

To build the frontend and then the whole package, it is enough to execute the following command from the main repo folder. Note that you need to have the venv and node environments properly setup before this will work.
```bash
$ make build-local
```

To build it in a Docker environment, instead of your local environment:
```bash
$ make build-in-docker
```

Once the package is built, publish the package to `PyPi` using a PyPi API token:

```bash
$ poetry publish --username __token__ --password <TOKEN>
```

## Docker Integration

We package the `MLTE` backend and frontend as a set of Docker container images. To build and run these from the source repository, run:

```bash
# From inside the docker/deployment folder
bash rebuild_and_restart.sh
```

This exposes the backend on the host at `localhost:8080`, and the frontend at `localhost:8000`. By default, PostgreSQL database is used in a container, and the data is mapped to the local `./pgdata` folder.

You can CTRL+C to stop seeing the output in the console, but the containers will continue running. You can check the current logs at any time with:

```bash
# From inside the docker/deployment folder
bash logs.sh
```

Stop the containers with:

```bash
# From inside the docker/deployment folder
bash stop.sh
```

## Contributing

To contribute to `MLTE`, check out our <a href="https://github.com/mlte-team/mlte" target="_blank">GitHub</a> repository!
