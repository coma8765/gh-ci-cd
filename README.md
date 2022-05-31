# FastAPI app with GitHub CI CD integration
[![test-application](https://github.com/coma8765/gh-ci-cd/actions/workflows/github-action-test.yml/badge.svg)](https://github.com/coma8765/gh-ci-cd/actions/workflows/github-action-test.yml)
## Require
* Python 3.10

## Prepare

### Install Pipenv
```shell
pip install pipenv
```

### Install dependencies
```shell
pipenv install
```

#### *for dev env:*
```shell
pipenv install --dev
```

## Run
```shell
pipenv run python -m app 
```

## Testing
```shell
pipenv run pytest -v
```

## Workflows
* **test:** on push, pull_request, issues and dispatch call
