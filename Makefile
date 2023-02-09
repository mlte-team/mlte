# Automation of various common tasks

# -----------------------------------------------------------------------------
# QA
# -----------------------------------------------------------------------------

# Sort imports
# TODO(Kyle): This currently introduces a circular-import
# error; we need to dig into this to address the root cause
# rather than continuing to shift imports around...

# .PHONY: isort
# isort:
# 	isort src/
# 	isort test/
# 	isort testbed/
# 	isort demo/*.py

# .PHONY: check-isort
# check-isort:
# 	isort --check src/
# 	isort --check test/
# 	isort --check testbed/
# 	isort --check demo/*.py

# Format all source code
.PHONY: format
format:
	black src/
	black test/
	black testbed/
	black demo/*.py

.PHONY: check-format 
check-format:
	black --check src/
	black --check test/
	black --check testbed/
	black --check demo/*.py

# Lint all source code
.PHONY: lint
lint:
	flake8 src/
	flake8 test/

.PHONY: check-lint
check-lint:
	flake8 src/
	flake8 test/

# Typecheck all source code
.PHONY: typecheck
typecheck:
	mypy src/
	mypy test/

.PHONY: check-typecheck
check-typecheck:
	mypy src/
	mypy test/

# All quality assurance
.PHONY: qa
qa: format lint typecheck

# Check all QA tasks
.PHONY: check
check: check-format check-lint check-typecheck

# -----------------------------------------------------------------------------
# Unit Tests
# -----------------------------------------------------------------------------

# Run unit tests with tox
# NOTE: Only runs 3.8 environment (for speed)
.PHONY: test
test:
	tox --develop -e py38
