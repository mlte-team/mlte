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
	poetry run black demo/simple/*.ipynb
	poetry run black demo/scenarios/*.ipynb
	poetry run black tools/

.PHONY: check-format 
check-format:
	poetry run black --check mlte/
	poetry run black --check test/
	poetry run black --check demo/
	poetry run black --check demo/simple/*.ipynb
	poetry run black --check demo/scenarios/*.ipynb
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

# -----------------------------------------------------------------------------
# Frontend QA
# -----------------------------------------------------------------------------

# Setup frontend env.
.PHONY: frontend-env
frontend-env:
	cd mlte/frontend/nuxt-app && \
	npm install && \
	npx gulp init

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
	bash demo/simple/test.sh demo/simple
	bash demo/scenarios/test.sh demo/scenarios

# -----------------------------------------------------------------------------
# Shorthand actions and checks needed to update and review for pushing.
# -----------------------------------------------------------------------------

# All quality assurance, as well as schema generation
.PHONY: qa
qa: schema isort format lint lint-frontend typecheck docs

# Check all QA tasks
.PHONY: check-qa
check-qa: check-schema check-isort check-format lint check-lint-frontend typecheck docs

# Clean cache files
.PHONY: clean
clean: 
	rm -r -f .mypy_cache .pytest_cache

.PHONY: ci
ci: clean venv frontend-env check-qa test
