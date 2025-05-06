# Perplexity CLI Project Restructuring

This document outlines the changes made to transform the original `perplexity_cli` script into a proper Python package with best practices.

## Changes Made

1. **Package Structure**
   - Created a proper Python package structure with `perplexity_cli` as the main package
   - Separated code into logical modules:
     - `__init__.py`: Package metadata and version
     - `config.py`: Configuration handling
     - `models.py`: Model information
     - `api.py`: API interaction
     - `cli.py`: Command-line interface
     - `__main__.py`: Entry point for running as a module

2. **Installation**
   - Added `setup.py`, `setup.cfg`, and `pyproject.toml` for proper packaging
   - Created entry point for command-line usage

3. **Testing**
   - Added unit tests for all modules
   - Set up pytest configuration

4. **Documentation**
   - Added docstrings to all functions and modules
   - Maintained the original README.md with usage instructions
   - Added LICENSE file

5. **Development Tools**
   - Added configuration for code formatting (black)
   - Added configuration for import sorting (isort)
   - Added configuration for linting (flake8)
   - Added configuration for type checking (mypy)

6. **Best Practices**
   - Improved error handling
   - Added proper type hints
   - Separated concerns into different modules
   - Made functions more testable
   - Added proper logging

## Project Structure

```
perplexity-cli/
├── LICENSE
├── MANIFEST.in
├── README.md
├── perplexity_cli/
│   ├── __init__.py
│   ├── __main__.py
│   ├── api.py
│   ├── cli.py
│   ├── config.py
│   └── models.py
├── pyproject.toml
├── setup.cfg
├── setup.py
└── tests/
    ├── __init__.py
    ├── test_api.py
    ├── test_cli.py
    └── test_config.py
```

## How to Use

The package can be installed and used in the same way as described in the original README.md:

```bash
# Install from source
pip install -e .

# Use the command-line interface
perplexity-cli -q "What is the distance between the Sun and Earth?"
```

## Development

For development, install the package with development dependencies:

```bash
pip install -e ".[dev]"
```

Run tests:

```bash
pytest
```

Format code:

```bash
black perplexity_cli tests
isort perplexity_cli tests
```

Check types:

```bash
mypy perplexity_cli
```
