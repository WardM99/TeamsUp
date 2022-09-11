# Backend

## Setting up a venv and installing dependencies

Create a venv, install Poetry, and then install the dependencies:

```shell
# Navigate to this directory
cd backend

# Create a virtual environment
python3 -m venv venv

# Make "pip3" and "python3" refer to the custom Python version in your venv
# PyCharm does this automatically, so this is only required if you're using another IDE
source venv/bin/activate

# Install Poetry
pip3 install poetry

# Install all dependencies and dev dependencies
poetry install

# Use the existing venv instead of creating a new one
poetry config virtualenvs.create false
poetry config virtualenvs.in-project true
```
