# Automation of various common tasks

# Format all source code
.PHONY: format
format:
	black src/
	black test/
	black testbed/
	black demo/*.py

# Lint all source code
.PHONY: lint
lint:
	flake8 src/
	flake8 test/

# Typecheck all source code
.PHONY: typecheck
typecheck:
	mypy src/
	mypy test/

# Run unit tests with tox
# NOTE: Only runs 3.8 environment (for speed)
.PHONY: test
test:
	tox --develop -e py38
