# Automation of various common tasks

# -----------------------------------------------------------------------------
# QA
# -----------------------------------------------------------------------------

.PHONY: isort
isort:	
	poetry run isort mlte/
	poetry run isort test/
	poetry run isort testbed/
	poetry run isort demo/
	poetry run isort tools/

.PHONY: check-isort
check-isort:
	poetry run isort --check mlte/
	poetry run isort --check test/
	poetry run isort --check testbed/
	poetry run isort --check demo/
	poetry run isort --check tools/

# Format all source code
.PHONY: format
format:
	poetry run black mlte/
	poetry run black test/
	poetry run black testbed/
	poetry run black demo/
	poetry run black demo/simple/*.ipynb
	poetry run black demo/scenarios/*.ipynb
	poetry run black tools/

.PHONY: check-format 
check-format:
	poetry run black --check mlte/
	poetry run black --check test/
	poetry run black --check testbed/
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

# Clean cache files
.PHONY: clean
clean: 
	rm -r -f .mypy_cache .pytest_cache

# All quality assurance
.PHONY: qa
qa: isort format lint typecheck

# Check all QA tasks
.PHONY: check
check: check-isort check-format check-lint check-typecheck

# -----------------------------------------------------------------------------
# Unit Tests
# -----------------------------------------------------------------------------

# Run unit tests with pytest
.PHONY: test
test:
	poetry run pytest --cov=mlte test 

# Open coverage results in a browser
.PHONY: cov-results
cov-results:
	coverage html && open htmlcov/index.html

# -----------------------------------------------------------------------------
# Schema Generation / Vetting
# -----------------------------------------------------------------------------

.PHONY: gen
gen:
	poetry run python tools/schema.py generate mlte --verbose

.PHONY: vet
vet:
	poetry run python tools/schema.py vet mlte --verbose


# -----------------------------------------------------------------------------
# All actions and checks needed to update and review for pushing.
# -----------------------------------------------------------------------------
.PHONY: ci
ci: clean gen qa test
