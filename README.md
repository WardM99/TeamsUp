# Teams Up

[![codecov](https://codecov.io/gh/WardM99/TeamsUp/branch/master/graph/badge.svg?token=CIKDMCEBZQ)](https://codecov.io/gh/WardM99/TeamsUp)
[![CodeFactor](https://www.codefactor.io/repository/github/wardm99/teamsup/badge)](https://www.codefactor.io/repository/github/wardm99/teamsup)

## Backend

### Setup

- Install ```python 3.10```
- Create virtual environment
- Install poetry and the dependencies

```shell
# Navigate to this directory
cd backend

# Create a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Poetry
pip3 install poetry

# Install all dependencies and dev dependencies
poetry install
```

### Setup backend server

```shell
uvicorn src.app.app:app
```
