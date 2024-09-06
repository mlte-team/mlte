# Development

This document describes some of the development practices used within `MLTE`.

## Quickstart

Use `poetry` to create a Python virtual environment and install the required runtime and development packages. This requires you to install `poetry` on your system first. Once it is installed, you can set up your environment like this:

```bash
$ python -m venv .venv
$ source .venv/bin/activate
$ poetry install
```

Instead of activating the environment, you can also choose to use `poetry run` to run specific commands.

Now you are ready to start working on `MLTE`!

## Project Development Commands

You can run most project commands (to format sources, lint, etc.), in two ways: using the commands in the included Makefile, or running things manually. Using the Makefile works on UNIX-like systems (or anywhere `make` is available), and is shorter to type. Alternatively, you can run each command manually. The sections below describe how to run commands in both ways.

Also, the commands below do not assume that you have your virtual environment enabled. Calling `poetry run` ensures things run in the current virtual environment even if it is not activated. If you manually activate your virtual environment with `source .venv/bin/activate` (see above), you can run all the commands below without the `poetry run` prefix.

### Import Sorting

We sort all Python imports code in this project with <a href="https://github.com/PyCQA/isort" target="_blank">`isort`</a>. Assuming you have followed the instructions in the [Quickstart](#quickstart), you can run this locally with:

```bash
$ poetry run make isort
```

Alternatively, you can run `isort` manually from the project root:

```bash
$ poetry run isort mlte/
$ poetry run isort test/
```

Code that does not satisfy the formatter will be rejected from pull requests.

### Source Formatting

We format all Python code in this project with the <a href="https://github.com/psf/black" target="_blank">`black`</a> source formatter. Assuming you have followed the instructions in the [Quickstart](#quickstart), you can run the formatter locally with:

```bash
$ poetry run make format
```

Alternatively, you can run `black` manually from the project root:

```bash
$ poetry run black mlte/
$ poetry run black test/
```

Code that does not satisfy the formatter will be rejected from pull requests.

### Source Linting

We lint all Python code in this project with the <a href="https://flake8.pycqa.org/en/latest/" target="_blank">`flake8`</a> source linter. Assuming you have followed the instructions in the [Quickstart](#quickstart), you can run the linter locally with:

```bash
$ poetry run make lint
```

Alternatively, you can run `flake8` manually from the project root:

```bash
$ poetry run flake8 mlte/
$ poetry run flake8 test/
```

Code that does not satisfy the linter will be rejected from pull requests.

### Static Type Checking

We run static type-checking with <a href="http://mypy-lang.org/" target="_blank">`mypy`</a>. Assuming you have followed the instructions in the [Quickstart](#quickstart), you can run the type-checker locally with:

```bash
$ poetry run make typecheck
```

Alternatively, you can run `mypy` manually from the project root:

```bash
$ poetry run mypy mlte/
$ poetry run mypy test/
```

Code that does not satisfy static type-checking will be rejected from pull requests.

### Unit Tests

We unit test the `MLTE` library with the <a href="https://docs.pytest.org/en/7.0.x/contents.html" target="_blank">`pytest`</a> package, a test-runner for Python. Assuming you have followed the instructions in the [Quickstart](#quickstart), you can run unit tests locally with:

```bash
$ poetry run make test
```

Alternatively, you can run the tests manually from the project root:

```bash
$ poetry run pytest test
```

Unit tests failures result in build failures in CI.

### Model Schema Generation

The artifacts used by `MLTE` have schemas that are used to validate them. These schemas need to be updated if their internal structure (code) changes. Assuming you have followed the instructions in the [Quickstart](#quickstart), you can do this locally with:

```bash
$ poetry run make gen
```

Alternatively, you can run this manually from the project root:

```bash
$ poetry run python tools/schema.py generate mlte --verbose
```

Unit test failures result in build failures in CI.

### Make Shorthand Commands

There are a couple of shorthand commands in the Makefile to run several of the above commands at the same time. The most useful ones include:

* `poetry run make qa`: execues the source sorting, formatting, source linting, and static type checking commands.
* `poetry run make ci`: execues the same commands as `qa`, but also runs `gen` to generate updated schemas if needed, and runs `test` to execute the unit tests.


## Front End

Front end development requires Node.js. The front end was developed using v20.11.0; the latest LTS version can be found <a href="https://nodejs.org/en" target="_blank">here</a>.

To initialize the development environment for the front end, navigate to the subfolder `./mlte/frontend/nuxt-app` and run:

```bash
$ npm install
$ npx gulp compile
$ npx gulp init
```

If there are issues with `npm install`, try this instead:

```bash
$ npm install --ignore-scripts
$ npm install
$ npx gulp compile
$ npx gulp init
```

Now the environment is set up and the front end can be run with the following command:

```bash
$ npm run dev
```

This will run the front end at `http://localhost:3000` so be sure to specify that as an allowed origin when running the backend. The backend can be run with a command like this one (using a file system store, in the local ./store folder):

```bash
$ mlte backend --store-uri fs://store --allowed-origins http://localhost:3000
```

### Front End Formatting and Linting

We format and lint all .vue, .js, and .ts files with <a href="https://eslint.org/" target="_blank">ESLint</a>, which can be run locally from the root of the nuxt application.

```bash
$ npm run lint
```

### Front End Static Type Checking
All typescript code takes advantage of static typing. This type checking can be done by running the following command:

```bash
$ npx vue-tsc
```

## Continuous Integration

We utilize <a href="https://docs.github.com/en/actions" target="_blank">GitHub Actions</a> for continuous integration.

## Documentation

We build documentation with <a href="https://www.mkdocs.org" target="_blank">`mkdocs`</a> and host documentation on <a href="https://readthedocs.org/" target="_blank">ReadTheDocs</a>. A webhook is set up in the MLTE repository to trigger an integration effect on ReadTheDocs when certain changes to the repo are made.

We maintain a separate set of requirements for building the documentation under `docs/requirements.txt`. To build the documentation locally, create a new virtual environment and install the requirements from this listing:

```bash
$ cd docs
$ python -m venv .venv
$ source ./.venv/bin/activate
$ pip install -r requirements.txt
```

Now you can build and serve the documentation with:

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

where `patch` may be replaced with `minor` or `major` as appropriate for the release. You may need to use:

```bash
$ bumpversion --allow-dirty patch
```

### Publishing

We publish the `MLTE` package on <a href="https://pypi.org/" target="_blank">PyPi</a>. Ensure you have properly incremented the version for the new release, as described in [Versioning](#versioning).

To build the frontend and then the whole package, it is enough to execute the following command from the main repo folder:
```bash
$ bash build.sh
```

You can also do this manually:
1. Build the static distribution for the front end; the command below assumes that you have the dependencies for frontend builds installed:

```bash
$ cd mlte/frontend/nuxt-app && npm run build
```

2. Create the source distribution and wheel from the main repo folder:

```bash
$ poetry build
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

This exposes the backend on the host at `localhost:8080`, and the frontend at `localhost:8080`. By default, PostgreSQL database is used in a container, and the data is mapped to the local `./pgdata` folder.

You can CTRL+C to stop seeing the output in the console, but the containers will continue running. You can check back the current logs at any time with:

```bash
# From inside the docker/deployment folder
bash logs.sh
```

Stop the containers with:

```bash
# From inside the docker/deployment folder
bash stop.sh
```

## Python Version Support

Currently, `MLTE` supports the following Python versions:

- `3.9`
- `3.10`
- `3.11`

<a href="https://github.com/pyenv/pyenv" target="_blank">`pyenv`</a> can be used to manage multiple Python versions locally. The following procedure can be used to ensure you are running the Python version you need. This procedure only needs to be performed once, during initial version establishment, meaning you _probably_ don't need to be repeating this step in order to contribute to `MLTE`.

### Establishing Depdencies for a Particular Python Version

Install the desired version with:

```bash
export VERSION=3.9

# Install the desired version
pyenv install $VERSION
# Activate the desired version
pyenv local $VERSION
# Confirm the version
python --version
Python 3.9.16
```

With the proper version activated, use `poetry` as described in [QuickStart](#quickstart) to create a virtual environment and install dependencies.

```bash
# Check QA mechanisms
make check
# Run tests
make test
```

Once all QA checks and unit tests pass, we can be assured that the environment dependencies are properly specified.

## Contributing

To contribute to `MLTE`, check out our <a href="https://github.com/mlte-team/mlte" target="_blank">GitHub</a>!
