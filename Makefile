# Makefile for SentinelOwl project

# Variables
PYTHON = python3
PIP = pip3
VENV = venv
ACTIVATE = . $(VENV)/bin/activate
PIP = $(VENV)/bin/pip
PIP_COMPILE = $(VENV)/bin/pip-compile
PIP_SYNC = $(VENV)/bin/pip-sync
REQUIREMENTS_DIR = requirements
BASE_REQS = $(REQUIREMENTS_DIR)/base.in
DEV_REQS = $(REQUIREMENTS_DIR)/dev.in
BASE_TXT = $(REQUIREMENTS_DIR)/base.txt
DEV_TXT = $(REQUIREMENTS_DIR)/dev.txt

# Targets
.PHONY: init activate install test lint format clean

# Initialize the project
init:
	@echo "Creating virtual environment..."
	$(PYTHON) -m venv $(VENV)
	@echo "Installing base dependencies..."
	$(MAKE) install

# Activate virtual environment (manual step)
activate:
	@echo "Run the following command to activate the virtual environment:"
	@echo "source $(VENV)/bin/activate  # Linux/macOS"
	@echo "$(VENV)\\Scripts\\activate   # Windows"

# Install dependencies
install: $(BASE_TXT) $(DEV_TXT)
	@echo "Syncing dependencies..."
	$(PIP) install pip-tools
	$(PIP) install -r $(DEV_TXT)

# Compile base requirements
$(BASE_TXT): $(BASE_REQS)
	@echo "Compiling base requirements..."
	$(PIP) install pip-tools
	$(ACTIVATE) && $(PIP_COMPILE) $(BASE_REQS) --output-file $(BASE_TXT)

# Compile dev requirements
$(DEV_TXT): $(DEV_REQS) $(BASE_TXT)
	@echo "Compiling dev requirements..."
	$(ACTIVATE) && $(PIP_COMPILE) $(DEV_REQS) --output-file $(DEV_TXT)

# Run tests
test:
	@echo "Running tests..."
	PYTHONPATH=$PYTHONPATH:. $(ACTIVATE) && pytest tests/ --cov=sentinelowl --cov-report=term-missing

# Lint the code
lint:
	@echo "Running linter..."
	$(ACTIVATE) && flake8 sentinelowl/ tests/

# Format the code
format:
	@echo "Formatting code..."
	$(ACTIVATE) && black sentinelowl/ tests/

# Clean up
clean:
	@echo "Cleaning up..."
	rm -rf $(VENV)
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf __pycache__
	rm -rf sentinelowl/__pycache__
	rm -rf tests/__pycache__
	find . -type f -name '*.pyc' -delete

ci-test:
	@pytest tests/ --cov=sentinelowl --cov-report=xml

ci-lint:
	@flake8 sentinelowl/ tests/
	@black --check sentinelowl/ tests/