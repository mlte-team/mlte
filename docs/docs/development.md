# Development

This document describes some of the development practices used within `MLTE`.

## Quickstart

Use Poetry to create a Python virtual environment and install the required runtime and development packages. This requires you to install `poetry` on your system first. Once it is installed, you can set up your environment like this:

```bash
$ python -m venv .venv
$ source .venv/bin/activate
$ poetry install
```

Instead of activating the environment, you can also choose to use `poetry run` to run specific commands.

Now you are ready to start working on `MLTE`!

## Source Formatting

We format all Python code in this project with the <a href="https://github.com/psf/black" target="_blank">`black`</a> source formatter. Assuming you have followed the instructions in the [Quickstart](#quickstart), you can run the formatter locally with:

```bash
$ poetry run make format
```

This works on UNIX-like systems (or anywhere `make` is available). Alternatively, you can run `black` manually from the project root:

```bash
$ poetry run black mlte/
$ poetry run black test/
```

Code that does not satisfy the formatter will be rejected from pull requests.

## Source Linting

We lint all Python code in this project with the <a href="https://flake8.pycqa.org/en/latest/" target="_blank">`flake8`</a> source linter. Assuming you have followed the instructions in the [Quickstart](#quickstart), you can run the linter locally with:

```bash
$ make lint
```

This works on UNIX-like systems (or anywhere `make` is available). Alternatively, you can run `flake8` manually from the project root:

```bash
$ poetry run flake8 mlte/
$ poetry run flake8 test/
```

Code that does not satisfy the linter will be rejected from pull requests.

## Static Type Checking

We run static type-checking with <a href="http://mypy-lang.org/" target="_blank">`mypy`</a>. Assuming you have followed the instructions in the [Quickstart](#quickstart), you can run the type-checker locally with:

```bash
$ poetry run make typecheck
```

This works on UNIX-like systems (or anywhere `make` is available). Alternatively, you can run `mypy` manually from the project root:

```bash
$ mypy mlte/
$ mypy test/
```

Code that does not satisfy static type-checking will be rejected from pull requests.

## Unit Tests

We unit test the `MLTE` library with the <a href="https://docs.pytest.org/en/7.0.x/contents.html" target="_blank">`pytest`</a> package, a test-runner for Python. Assuming you have followed the instructions in the [Quickstart](#quickstart), you can run unit tests locally with:

```bash
$ make test
```

This works on UNIX-like systems (or anywhere `make` is available). Alternatively, you can run the tests manually from the project root:

```bash
$ poetry run pytest test
```

Unit tests failures result in build failures in CI.

## Front End

Front end development requires Node.js. The front end was developed using v20.11.0; the latest LTS version can be found <a href="https://nodejs.org/en" target="_blank">here</a>.

To initialize the development environment for the front end, navigate to `mlte/frontend/nuxt-app` and run:

```bash
$ npm install
$ npx gulp compile
$ npx gulp init
```

If there are issues with `npm install`, try this instead:

```bash
$ npm i --ignore-scripts
$ npm install
$ npx gulp compile
$ npx gulp init
```

Now the environment is set up and the front end can be run with the following command:

```bash
$ npm run dev
```

This will run the front end at `http://localhost:3000` so be sure to specify that as an allowed origin when running the store:

```bash
$ mlte store --backend-uri fs://store --allowed-origins http://localhost:3000
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

We build documentation with <a href="https://www.mkdocs.org" target="_blank">`mkdocs`</a> and host documentation on <a href="https://readthedocs.org/" target="_blank">ReadTheDocs</a>.

We maintain a separate set of requirements for building the documentation under `docs/requirements.txt`. To build the documentation locally, create a new virtual environment and install the requirements from this listing:

```bash
$ cd docs
$ python -m venv env
$ source ./env/bin/activate
$ pip install -r requirements.txt
```

Now you can build the documentation with:

```bash
$ mkdocs serve
```

## Versioning

We follow semantic versioning when versioning the `MLTE` package. We use <a href="https://github.com/c4urself/bump2version" target="_blank">`bump2version`</a> to consistently update versions across the project. A configuration file is provided in `.bumpversion.cfg` at the root of the project.

Bumping the version for a new release can be accomplished with:

```bash
$ bumpversion patch
```

where `patch` may be replaced with `minor` or `major` as appropriate for the release. You may need to use:

```bash
$ bumpversion --allow-dirty patch
```

## Publishing

We publish the `MLTE` package on <a href="https://pypi.org/" target="_blank">PyPi</a>. Ensure you have properly incremented the version for the new release, as described in Versioning above.

Build the static distribution for the front end; the command below assumes that you have the dependencies for front end builds installed:

```bash
$ cd mlte/frontend/nuxt-app && npm run build
```

If publishing on MacOS, you'll need to remove the node_modules directory before building the package (they can be reinstalled afterwards using `npm install`):

```bash
$ rm -rf mlte/frontend/nuxt-app/node_modules
```

Create the source distribution and wheel:

```bash
$ poetry build
```

Publish the package to `PyPi` using a PyPi API token:

```bash
$ poetry publish --username __token__ --password <TOKEN>
```

### Docker Integration

We package the `MLTE` artifact store as a Docker container image. To build the image from the source repository, run:

```bash
# From the repository root
docker build . -f docker/Dockerfile.store -t mlte-store
```

Run the container with:

```bash
docker run --rm -p 8080:8080 mlte-store
```

This binds the artifact store to the address `0.0.0.0:8080` within the container, and exposes it on the host at `localhost:8080`. By default, a local filesystem backend is used for storage. The artifact store implementation writes data to `/mnt/store` within the container. We can utilize a <a href="https://docs.docker.com/storage/bind-mounts/" target="_blank">bind mount</a> to extend the life of this data beyond the life of the container:

```bash
docker run --rm -p 8080:8080 -v /host/path/to/store:/mnts/store mlte-store
```

## Development Dependencies

Currently, `MLTE` supports the following Python versions:

- `3.8`
- `3.9`
- `3.10`

<a href="https://github.com/pyenv/pyenv" target="_blank">`pyenv`</a> can be used to manage multiple Python versions locally. The following procedure can be used to ensure you are running the Python version you need. This procedure only needs to be performed once, during initial version establishment, meaning you _probably_ don't need to be repeating this step in order to contribute to `MLTE`.

**Establishing Depdencies for a Particular Python Version**

Install the desired version with:

```bash
export VERSION=3.8

# Install the desired version
pyenv install $VERSION
# Activate the desired version
pyenv local $VERSION
# Confirm the version
python --version
Python 3.8.16
```

With the proper version activated, use `poetry` as described in the QuickStart to create a virtual environment and install dependencies.

```bash
# Check QA mechanisms
make check
# Run tests
make test
```

Once all QA checks and unit tests pass, we can be assured that the environment dependencies are properly specified.

## Contributing

To contribute to `MLTE`, check out our <a href="https://github.com/mlte-team/mlte" target="_blank">GitHub</a>!
