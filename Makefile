# Automation of various common tasks

# Format all source code
.PHONY: format
format:
	black src/mlte/
	black test/
	black setup.py

# Lint all source code
.PHONY: lint
lint:
	flake8 src/mlte/
	flake8 test/
	flake8 setup.py

# Run unit tests with tox
.PHONY: test
test:
	tox
