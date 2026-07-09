# Automation of various common tasks.

# -----------------------------------------------------------------------------
# Python Venv and Cache
# -----------------------------------------------------------------------------

# Remove actual underlying venv.
.PHONY: python-venv-remove
python-venv-remove:
	rm -rf ./.venv

# Create venv through uv, with all dependencies.
.PHONY: python-venv
python-venv:
	uv lock && \
	uv sync --group dev --group demo --all-extras

# Delete and recreate venv.
.PHONY: python-venv-redo
python-venv-redo: python-venv-remove python-venv

# Clean python cache files/folders, without touching venv.
.PHONY: python-env-clean
python-env-clean:
	rm -r -f .mypy_cache .pytest_cache default_store/

# -----------------------------------------------------------------------------
# Schema Generation / Vetting
# -----------------------------------------------------------------------------

# Create updated schemas.
.PHONY: schema
schema:
	uv run python tools/schema.py generate mlte --verbose

# Check if schemas are up to date.
.PHONY: check-schema
check-schema:
	uv run python tools/schema.py vet mlte --verbose

# -----------------------------------------------------------------------------
# Doc Building/Serving
# -----------------------------------------------------------------------------

# Doc generation.
.PHONY: docs
docs:
	cd docs && uv run properdocs build --strict

# Local doc serving.
.PHONY: docs-serve
docs-serve:
	cd docs && uv run properdocs serve

# -----------------------------------------------------------------------------
# Python Lowl-Level QA and Testing
# -----------------------------------------------------------------------------

# Lint/check all source code.
.PHONY: lint
lint:
	uv run ruff check --fix .

.PHONY: check-lint 
check-lint:
	uv run ruff check .

# Format/check all source code.
.PHONY: format
format:
	uv run ruff format .

.PHONY: check-format 
check-format:
	uv run ruff format --check .

# Typecheck all source code (except for demo).
.PHONY: typecheck
typecheck:
	uv run mypy . --exclude "demo/"

# Run unit tests with pytest.
.PHONY: test
test:
	uv run pytest --cov=mlte -W ignore::pytest.PytestCollectionWarning test 

# -----------------------------------------------------------------------------
# Demo and Sample Catalog QA and Generation
# -----------------------------------------------------------------------------

# Clean demo notebooks of temporary outputs.
.PHONY: demo-clean
demo-clean:
	cd demo && bash clean_all_nbs.sh simple GardenBuddy ReviewPro GradientClimber

# Typecheck demo code.
.PHONY: demo-typecheck
demo-typecheck:
	uv run mypy demo/

# Demo Jupyter Notebook tests.
.PHONY: demo-test
demo-test:
	cd demo && bash test.sh simple GardenBuddy ReviewPro GradientClimber

# Generate sample catalog entries.
.PHONY: build-sample-catalog
build-sample-catalog:
	cd demo && bash catalog_entries.sh build GardenBuddy ReviewPro GradientClimber

# Check sample catalog entries.
.PHONY: check-sample-catalog
check-sample-catalog:
	cd demo && bash catalog_entries.sh check GardenBuddy ReviewPro GradientClimber

# -----------------------------------------------------------------------------
# Python High Level QA and CI
# -----------------------------------------------------------------------------

# QA for Python bits.
.PHONY: qa-python
qa-python: schema lint format typecheck demo-clean demo-typecheck docs build-sample-catalog

# QA for Python bits, ran within a docker container.
.PHONY: qa-python-docker
qa-python-docker:
	cd docker && sh run_python_ops.sh qa-python

# Check all QA tasks for Python.
.PHONY: check-qa-python
check-qa-python: check-schema check-lint check-format typecheck demo-typecheck docs check-sample-catalog

# CI for Python bits.
.PHONY: ci-python
ci-python: python-env-clean python-venv check-qa-python test demo-test

# CI for Python bits ran within a docker container.
.PHONY: ci-python-docker
ci-python-docker:
	cd docker && sh run_python_ops.sh ci-python

# -----------------------------------------------------------------------------
# Frontend Low-level Env and QA
# -----------------------------------------------------------------------------

# Setup frontend env.
.PHONY: frontend-env
frontend-env:
	cd mlte/frontend/nuxt-app && \
	npm install && \
	npx gulp init

# Delete frontend env (basically cached folders).
.PHONY: frontend-env-remove
frontend-env-remove:
	rm -rf mlte/frontend/nuxt-app/node_modules
	rm -rf mlte/frontend/nuxt-app/.nuxt
	rm -rf mlte/frontend/nuxt-app/.output
	rm -rf mlte/frontend/nuxt-app/assets/uswds

# Lint/check frontend source code.
.PHONY: lint-frontend
lint-frontend:
	cd mlte/frontend/nuxt-app && npx eslint --fix .

.PHONY: check-lint-frontend
check-lint-frontend:
	cd mlte/frontend/nuxt-app && npx eslint .

# Typecheck frontend source code.
.PHONY: typecheck-frontend
typecheck-frontend:
	cd mlte/frontend/nuxt-app && npx vue-tsc

# -----------------------------------------------------------------------------
# Frontend High-level QA and CI
# -----------------------------------------------------------------------------

# QA for frontend (node.js) bits.
.PHONY: qa-frontend
qa-frontend: lint-frontend typecheck-frontend

# QA for the frontend (node.js) bits, ran within a docker container.
.PHONY: qa-frontend-docker
qa-frontend-docker:
	cd docker && bash run_frontend_ops.sh qa-frontend

# Check all QA tasks for frontend.
.PHONY: check-qa-frontend
check-qa-frontend: check-lint-frontend typecheck-frontend

# CI for frontend (node.js) bits.
.PHONY: ci-frontend
ci-frontend: frontend-env-remove frontend-env check-qa-frontend

# CI for frontend (node.js) bits, ran within a docker container.
.PHONY: ci-frontend-docker
ci-frontend-docker:
	cd docker && bash run_frontend_ops.sh ci-frontend

# -----------------------------------------------------------------------------
# Combined Python/Frontend QA and CI
# -----------------------------------------------------------------------------

# All quality assurance, as well as schema generation and sample catalog generation.
.PHONY: qa
qa: qa-python qa-frontend

# Check all QA tasks.
.PHONY: check-qa
check-qa: check-qa-python check-qa-frontend

# Clean all cache files.
.PHONY: clean
clean: frontend-env-remove python-env-clean

# This is basically equivalent to what the CI server will do.
.PHONY: ci
ci: ci-python ci-frontend

# -----------------------------------------------------------------------------
# Version updating
# -----------------------------------------------------------------------------

.PHONY: bump-patch
bump-patch:
	uv run bumpversion patch --allow-dirty
	$(MAKE) frontend-env

.PHONY: bump-minor
bump-minor:
	uv run bumpversion minor --allow-dirty
	$(MAKE) frontend-env

.PHONY: bump-major
bump-major:
	uv run bumpversion major --allow-dirty
	$(MAKE) frontend-env

# -----------------------------------------------------------------------------
# Build commands to create a packaged wheel
# -----------------------------------------------------------------------------

# Build using locally installed envs, output i /dist.
.PHONY: build-local
build-local:
	bash build_local.sh

# Build fully inside a docker container, but output ends up in /dist as well.
.PHONY: build-in-docker
build-in-docker:
	bash build_in_docker.sh
