# Poetry Guide for Python Projects

## Installation Guide

### macOS Installation
```bash
# Install Poetry using curl (recommended)
curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to your PATH (for macOS/Linux)
export PATH="/Users/$USER/.local/bin:$PATH"

# Add this line to your ~/.zshrc or ~/.bash_profile to make it permanent
echo 'export PATH="/Users/$USER/.local/bin:$PATH"' >> ~/.zshrc  # for zsh
# OR
echo 'export PATH="/Users/$USER/.local/bin:$PATH"' >> ~/.bash_profile  # for bash

# Reload your shell configuration
source ~/.zshrc  # for zsh
# OR
source ~/.bash_profile  # for bash

# Verify installation
poetry --version
```

### Windows Installation
```powershell
# Using PowerShell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -

# Add Poetry to your PATH
# System Settings -> Advanced -> Environment Variables -> Path -> Add
# Add this path: %APPDATA%\Python\Scripts
```

### Linux Installation
```bash
# Install using curl
curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to PATH
export PATH="/home/$USER/.local/bin:$PATH"
echo 'export PATH="/home/$USER/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

## Getting Started

### Initialize a New Project
```bash
# Create new project
poetry new my-project
cd my-project

# OR initialize in existing project
cd existing-project
poetry init
```

### Basic Usage

#### Managing Dependencies
```bash
# Install dependencies
poetry install

# Add a package
poetry add requests

# Add development dependencies
poetry add --group dev pytest

# Remove a package
poetry remove requests

# Update all dependencies
poetry update

# Show dependency tree
poetry show --tree
```

#### Virtual Environment Management
```bash
# Create/activate virtual environment
poetry shell

# Run a command in the virtual environment
poetry run python your_script.py

# Show virtual environment information
poetry env info

# List all virtual environments
poetry env list
```

## Project Structure Example
```
my-project/
├── pyproject.toml          # Project configuration
├── poetry.lock            # Lock file with exact versions
├── README.md
├── my_project/
│   ├── __init__.py
│   └── main.py
└── tests/
    └── test_main.py
```

## Configuration File (pyproject.toml) Example
```toml
[tool.poetry]
name = "my-project"
version = "0.1.0"
description = "Your project description"
authors = ["Your Name <your.email@example.com>"]

[tool.poetry.dependencies]
python = "^3.9"
requests = "^2.28.0"

[tool.poetry.group.dev.dependencies]
pytest = "^7.0.0"
black = "^22.0.0"

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"
```

## Common Issues and Solutions

### Poetry Command Not Found
```bash
# Check if Poetry is in PATH
which poetry

# If not found, add to PATH
export PATH="/Users/$USER/.local/bin:$PATH"  # macOS/Linux
# OR add to your shell's config file

# Alternatively, reinstall Poetry
curl -sSL https://install.python-poetry.org | python3 -
```

### Virtual Environment Issues
```bash
# Configure Poetry to create virtualenvs in project directory
poetry config virtualenvs.in-project true

# Clear Poetry cache
poetry cache clear . --all

# Recreate virtual environment
poetry env remove python3.9
poetry env use python3.9
poetry install
```

## Best Practices

1. **Version Control**
   - Commit both `pyproject.toml` and `poetry.lock`
   - Add `.venv/` to `.gitignore`

2. **Dependency Management**
   - Use caret (^) for flexible versions in development
   - Use exact versions (=) for critical production dependencies
   - Regularly update dependencies with `poetry update`

3. **Environment Management**
   - Use `poetry shell` for development
   - Use `poetry run` for single commands
   - Keep virtual environments in project with `virtualenvs.in-project true`

4. **Project Organization**
   - Use src layout for packages
   - Keep tests separate from source code
   - Document dependencies in README.md

## Docker Integration

### Example Dockerfile with Poetry
```dockerfile
FROM python:3.9-slim

# Install poetry
RUN pip install poetry

# Copy project files
COPY pyproject.toml poetry.lock ./

# Install dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

# Copy application code
COPY . .

# Run the application
CMD ["poetry", "run", "python", "my_project/main.py"]
```

## Additional Commands

### Dependency Information
```bash
# List installed packages
poetry show

# Show outdated packages
poetry show --outdated

# Export requirements.txt
poetry export -f requirements.txt --output requirements.txt
```

### Project Publishing
```bash
# Build package
poetry build

# Publish to PyPI
poetry publish

# Build and publish
poetry publish --build
```