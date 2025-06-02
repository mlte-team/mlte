# Development

This document describes some of the development practices used in `MLTE`.

## Setup

### Python Version Support

Currently, `MLTE` supports Python versions between `3.9` and `3.12`, both included.

If you do not have one of these versions installed, or you want to target a specific version that is not your default, `pyenv` can be used to manage multiple Python versions locally. Note that this is optional, and only needed if you have a not-supported default Python version. To set up a specific version of Python with `pyenv`:

- Install `pyenv` as described in this link: https://github.com/pyenv/pyenv
- Install the desired Python version (in this example, 3.9):

```bash
$ pyenv install 3.9
```

- While inside the root repository folder, run this command to set that Python version to be used when executed in that folder:

```bash
$ pyenv local 3.9
```

- You can use `python --version` to check if it worked.

### Requirements

 - `MLTE` uses `poetry` (v 2.0.1 or higher) to handle the required runtime and development packages. You can install `poetry` on your system with the instructions available here: https://python-poetry.org/docs/#installation
 - You also need to set up a virtual Python environment where `poetry` will work. While inside the root of the repository, execute this command:

```bash
$ python -m venv .venv
```

### Dev Environment Setup

Once poetry and the virtual env are setup, you can set up dev dependencies like this, from the root of the repository:

```bash
$ poetry install --with dev --all-extras
```

You can also run the following make command to install the same dependencies, plus the demo ones (see below):

```bash
$ make venv
```

Now you are ready to start working on `MLTE`!

### Demos

There are several demos available in the `demo\` folder, as Jupyter notebooks. To run them, you need to install their dependencies first. This can be done from the root of the repository with:

```bash
$ poetry install --with demo
```

NOTE: The demo will only work on its entirety with python versions up to 3.12, since requires tensorflow, which is not currently supported in newer python versions.

## Project Development Commands

You can run most project commands (e.g., format sources, lint) in two ways: using the commands in the included Makefile, or running things manually. Using the Makefile works on UNIX-like systems (or anywhere `make` is available), and is shorter to type. Alternatively, you can run each command manually. The sections below describe how to run commands in both ways.

Also, the commands below do not assume that you have your virtual environment enabled. Calling `poetry run` ensures things run in the current virtual environment even if it is not activated. If you manually activate your virtual environment you can run all the commands below without the `poetry run` prefix. 

To manually activate your environment, run:

```bash
$ source .venv/bin/activate
```

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

### Make Shorthand Commands

There are a couple of shorthand commands in the Makefile to run several of the above commands at the same time. The most useful ones include:

* `make qa`: executes the schema generation, doc check, source sorting, formatting, linting, and static type checking commands.
* `make check-qa`: executes the schema check, doc check, source sorting check, formatting check, linting check, and static type checking commands.
* `make ci`: executes the same commands as `check-qa`, but also runs `test` to execute the unit tests, cleaning caches first to better simulate execution in a CI environment.


## Front End

Front end development requires Node.js. The front end was developed using v20.11.0; the latest LTS version can be found <a href="https://nodejs.org/en" target="_blank">here</a>.

To initialize the development environment for the front end, navigate to the subfolder `./mlte/frontend/nuxt-app` and run:

```bash
$ npm install
$ npx gulp compile
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
$ bumpversion patch
```

where `patch` may be replaced with `minor` or `major` as appropriate for the release. Be sure to have no other pending changes or this may fail. Also, bupmversion will change all instances of the current version to the new one in the files it has been configured to do so, so if you have other text in these files which happens to match the current version, it will be incorrectly changed. Manually inspect changes after running this tool, and discard any incorrect ones.

### Publishing

We publish the `MLTE` package on <a href="https://pypi.org/" target="_blank">PyPi</a>. Ensure you have properly incremented the version for the new release, as described in [Versioning](#versioning).

To build the frontend and then the whole package, it is enough to execute the following command from the main repo folder:
```bash
$ bash build.sh
```

Once the package is built, publish the package to `PyPi` using a PyPi API token:

```bash
$ poetry publish --username __token__ --password <TOKEN>
```

## Docker Integration

We package the `MLTE` backend as a set of Docker container images. To build the image from the source repository, run:

```bash
# From inside the docker/ folder
bash build.sh
```

Run the containers with:

```bash
# From inside the docker/deployment folder
bash start.sh
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
