# Automation of various common tasks

# -----------------------------------------------------------------------------
# QA
# -----------------------------------------------------------------------------

# Sort imports
# TODO(Kyle): This currently introduces a circular-import
# error; we need to dig into this to address the root cause
# rather than continuing to shift imports around...
#
# NOTE(Kyle): I am trying to gradually add these in.

.PHONY: isort
isort:	
	poetry run isort src/mlte/artifact
	poetry run isort src/mlte/negotiation
	poetry run isort src/mlte/value
	poetry run isort src/mlte/web/
	
	poetry run isort test/
	poetry run isort testbed/
	poetry run isort demo/*.py
	poetry run isort tools/

# .PHONY: check-isort
# check-isort:
# 	isort --check src/
# 	isort --check test/
# 	isort --check testbed/
# 	isort --check demo/*.py

# Format all source code
.PHONY: format
format:
	poetry run black mlte/
	poetry run black test/
	poetry run black testbed/
	poetry run black demo/*.py
	poetry run black tools/

.PHONY: check-format 
check-format:
	poetry run black --check mlte/
	poetry run black --check test/
	poetry run black --check testbed/
	poetry run black --check demo/*.py
	poetry run black --check tools/

# Lint all source code
.PHONY: lint
lint:
	poetry run flake8 mlte/
	poetry run flake8 test/
	poetry run flake8 tools/

.PHONY: check-lint
check-lint: lint

# Typecheck all source code
.PHONY: typecheck
typecheck:
	poetry run mypy mlte/
	poetry run mypy test/
	poetry run mypy tools/

.PHONY: check-typecheck
check-typecheck: typecheck

# All quality assurance
.PHONY: qa
qa: isort format lint typecheck

# Check all QA tasks
.PHONY: check
check: check-format check-lint check-typecheck

# -----------------------------------------------------------------------------
# Unit Tests
# -----------------------------------------------------------------------------

# Run unit tests with tox
# NOTE: Only runs 3.10 environment (for speed)
.PHONY: test
test:
	poetry run pytest test

# -----------------------------------------------------------------------------
# Schema Generation / Vetting
# -----------------------------------------------------------------------------

.PHONY: gen
gen:
	PYTHONPATH=src python tools/schema.py generate src/mlte --verbose

.PHONY: vet
vet:
	PYTHONPATH=src python tools/schema.py vet src/mlte --verbose
