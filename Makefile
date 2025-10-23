# Automation of various common tasks

# -----------------------------------------------------------------------------
# Python env setup.
# -----------------------------------------------------------------------------

.PHONY: venv-clean
venv-clean:
	rm -rf ./.venv

.PHONY: venv
venv:
	python -m venv .venv && \
	poetry lock && \
	poetry install --with dev,demo --all-extras

.PHONY: venv-redo
venv-redo: venv-clean venv

# -----------------------------------------------------------------------------
# Schema Generation / Vetting
# -----------------------------------------------------------------------------

.PHONY: schema
schema:
	poetry run python tools/schema.py generate mlte --verbose

.PHONY: check-schema
check-schema:
	poetry run python tools/schema.py vet mlte --verbose

# -----------------------------------------------------------------------------
# Doc building/checking.
# -----------------------------------------------------------------------------

# Doc generation.
.PHONY: docs
docs:
	cd docs && poetry run mkdocs build --strict

# -----------------------------------------------------------------------------
# QA
# -----------------------------------------------------------------------------

.PHONY: isort
isort:	
	poetry run isort mlte/
	poetry run isort test/
	poetry run isort demo/
	poetry run isort tools/

.PHONY: check-isort
check-isort:
	poetry run isort --check mlte/
	poetry run isort --check test/
	poetry run isort --check demo/
	poetry run isort --check tools/

# Format all source code
.PHONY: format
format:
	poetry run black mlte/
	poetry run black test/
	poetry run black demo/
	poetry run black tools/

.PHONY: check-format 
check-format:
	poetry run black --check mlte/
	poetry run black --check test/
	poetry run black --check demo/
	poetry run black --check tools/

# Lint all source code
.PHONY: lint
lint:
	poetry run flake8 mlte/
	poetry run flake8 test/
	poetry run flake8 tools/

# Typecheck all source code
.PHONY: typecheck
typecheck:
	poetry run mypy mlte/
	poetry run mypy test/
	poetry run mypy tools/

# Clean demo notebooks of temporary outputs.
.PHONY: clean-demo
clean-demo:
	cd demo && bash clean_all_nbs.sh

# QA for Python bits.
.PHONY: qa-python
qa-python: schema isort format lint typecheck clean-demo docs

# Check all QA tasks for Python.
.PHONY: check-qa-python
check-qa-python: check-schema check-isort check-format lint typecheck docs

# -----------------------------------------------------------------------------
# Frontend QA
# -----------------------------------------------------------------------------

# Setup frontend env.
.PHONY: frontend-env
frontend-env:
	cd mlte/frontend/nuxt-app && \
	npm install && \
	npx gulp init

.PHONY: frontend-env-clean
frontend-env-clean:
	rm -rf mlte/frontend/nuxt-app/node_modules
	rm -rf mlte/frontend/nuxt-app/.nuxt
	rm -rf mlte/frontend/nuxt-app/.output
	rm -rf mlte/frontend/nuxt-app/assets/uswds

# Lint frontend source code
.PHONY: lint-frontend
lint-frontend:
	cd mlte/frontend/nuxt-app && npx eslint --fix .

.PHONY: check-lint-frontend
check-lint-frontend:
	cd mlte/frontend/nuxt-app && npx eslint .

# Typecheck frontend source code
.PHONY: typecheck-frontend
typecheck-frontend:
	cd mlte/frontend/nuxt-app && npx vue-tsc

# QA for frontend (node.js) bits.
.PHONY: qa-frontend
qa-frontend: lint-frontend typecheck-frontend

# Check all QA tasks for frontend
.PHONY: check-qa-frontend
check-qa-frontend: check-lint-frontend typecheck-frontend

# -----------------------------------------------------------------------------
# Unit Tests
# -----------------------------------------------------------------------------

# Run unit tests with pytest
.PHONY: test
test:
	poetry run pytest --cov=mlte -W ignore::pytest.PytestCollectionWarning test 

# Demo Jupyter Notebook tests
.PHONY: demo-test
demo-test:
	cd demo && bash test.sh simple scenarios

# -----------------------------------------------------------------------------
# Shorthand actions and checks needed to update and review for pushing.
# -----------------------------------------------------------------------------

# All quality assurance, as well as schema generation
.PHONY: qa
qa: qa-python qa-frontend

# Check all QA tasks
.PHONY: check-qa
check-qa: check-qa-python check-qa-frontend

# Clean cache files
.PHONY: clean
clean: frontend-env-clean
	rm -r -f .mypy_cache .pytest_cache default_store/

# This is basically equivalent to what the CI server will do.
.PHONY: ci
ci: clean venv frontend-env check-qa test demo-test

# -----------------------------------------------------------------------------
# Build commands to update versions.
# -----------------------------------------------------------------------------

.PHONY: bump-patch
bump-patch:
	poetry run bumpversion patch --allow-dirty
	$(MAKE) frontend-env

.PHONY: bump-minor
bump-minor:
	poetry run bumpversion minor --allow-dirty
	$(MAKE) frontend-env

.PHONY: bump-major
bump-major:
	poetry run bumpversion major --allow-dirty
	$(MAKE) frontend-env

# -----------------------------------------------------------------------------
# Build commands to create a packaged wheel.
# -----------------------------------------------------------------------------

.PHONY: build-local
build-local:
	bash build_local.sh

.PHONY: build-in-docker
build-in-docker:
	bash build_in_docker.sh
