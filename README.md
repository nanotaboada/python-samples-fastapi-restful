# 🧪 RESTful API with Python 3 and FastAPI

## Status

[![Python CI](https://github.com/nanotaboada/python-samples-fastapi-restful/actions/workflows/python-ci.yml/badge.svg)](https://github.com/nanotaboada/python-samples-fastapi-restful/actions/workflows/python-ci.yml)
[![Python CD](https://github.com/nanotaboada/python-samples-fastapi-restful/actions/workflows/python-cd.yml/badge.svg)](https://github.com/nanotaboada/python-samples-fastapi-restful/actions/workflows/python-cd.yml)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=nanotaboada_python-samples-fastapi-restful&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=nanotaboada_python-samples-fastapi-restful)
[![codecov](https://codecov.io/gh/nanotaboada/python-samples-fastapi-restful/branch/master/graph/badge.svg?token=A1WNZPRQEJ)](https://codecov.io/gh/nanotaboada/python-samples-fastapi-restful)
[![CodeFactor](https://www.codefactor.io/repository/github/nanotaboada/python-samples-fastapi-restful/badge)](https://www.codefactor.io/repository/github/nanotaboada/python-samples-fastapi-restful)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## About

Proof of Concept for a RESTful API made with [Python 3](https://www.python.org/) and [FastAPI](https://fastapi.tiangolo.com/).

## Features

- 🏗️ **Modern async architecture** - Async/await throughout, Pydantic validation, and SQLAlchemy 2.0+ patterns
- 📚 **Interactive API exploration** - Auto-generated OpenAPI docs with FastAPI's built-in Swagger UI
- ⚡ **Performance optimizations** - Async SQLAlchemy, in-memory caching with aiocache, and efficient database operations
- 🧪 **High test coverage** - Pytest suite with 80% minimum coverage and automated reporting to Codecov
- 📖 **Token-efficient documentation** - AGENTS.md + auto-loaded Copilot instructions for AI-assisted development
- 🐳 **Full containerization** - Production-ready Docker setup with Docker Compose orchestration
- 🔄 **Complete CI/CD pipeline** - Automated linting (Black/Flake8), testing, Docker publishing, and GitHub releases
- ♟️ **Coach-themed semantic versioning** - Memorable, alphabetical release names honoring legendary football coaches

## Structure

![Simplified, conceptual project structure and main application flow](assets/images/structure.svg)

_Figure: Simplified, conceptual project structure and main application flow. Not all dependencies are shown._

## Python Version Management

This project uses `.python-version` to specify the required Python version. If you use [pyenv](https://github.com/pyenv/pyenv), [asdf](https://asdf-vm.com/), or [mise](https://mise.jdx.dev/), the correct Python version will be automatically activated when you enter the project directory.

Alternatively, ensure you have Python 3.13.3 (or the version specified in `.python-version`) installed.

## Install

```console
pip install -r requirements.txt
pip install -r requirements-lint.txt
pip install -r requirements-test.txt
```

## Start

```console
uvicorn main:app --reload --port 9000
```

## Docs

```console
http://localhost:9000/docs
```

![API Documentation](assets/images/swagger.png)

## HTTP Requests

The [`rest/players.rest`](rest/players.rest) file covers all CRUD operations and can be run directly in VS Code with the [REST Client](https://marketplace.visualstudio.com/items?itemName=humao.rest-client) extension.

## Container

### Docker Compose

This setup uses [Docker Compose](https://docs.docker.com/compose/) to build and run the app and manage a persistent SQLite database stored in a Docker volume.

#### Build the image

```bash
docker compose build
```

#### Start the app

```bash
docker compose up
```

> On first run, the container copies a pre-seeded SQLite database into a persistent volume
> On subsequent runs, that volume is reused and the data is preserved

#### Stop the app

```bash
docker compose down
```

#### Optional: database reset

```bash
docker compose down -v
```

> This removes the volume and will reinitialize the database from the built-in seed file the next time you `up`.

## Releases

This project uses famous football coaches as release names ♟️

### Create a Release

To create a new release, follow this workflow:

#### 1. Update CHANGELOG.md

First, document your changes in [CHANGELOG.md](CHANGELOG.md):

```bash
# Move items from [Unreleased] to new release section
# Example: [1.0.0 - Ancelotti] - 2026-02-15
git add CHANGELOG.md
git commit -m "docs: prepare changelog for v1.0.0-ancelotti release"
git push
```

#### 2. Create and Push Tag

Then create and push the version tag:

```bash
git tag -a v1.0.0-ancelotti -m "Release 1.0.0 - Ancelotti"
git push origin v1.0.0-ancelotti
```

#### 3. Automated CD Workflow

This triggers the CD workflow which automatically:

1. Validates the coach name
2. Builds and tests the project with coverage
3. Publishes Docker images to GitHub Container Registry with three tags
4. Creates a GitHub Release with auto-generated changelog from commits

> 💡 Always update CHANGELOG.md before creating the tag. See [CHANGELOG.md](CHANGELOG.md#how-to-release) for detailed release instructions.

### Pull Docker Images

Official releases are published to GitHub Container Registry (GHCR):

```bash
# By semantic version (recommended)
docker pull ghcr.io/nanotaboada/python-samples-fastapi-restful:1.0.0

# By coach name
docker pull ghcr.io/nanotaboada/python-samples-fastapi-restful:ancelotti

# Latest
docker pull ghcr.io/nanotaboada/python-samples-fastapi-restful:latest
```

> 💡 See [CHANGELOG.md](CHANGELOG.md) for the complete coach list (A-Z) and release history.

## Credits

The solution has been coded using [Visual Studio Code](https://code.visualstudio.com/) with the official [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python) extension.

## Terms

All trademarks, registered trademarks, service marks, product names, company names, or logos mentioned on this repository are the property of their respective owners. All usage of such terms herein is for identification purposes only and constitutes neither an endorsement nor a recommendation of those items. Furthermore, the use of such terms is intended to be for educational and informational purposes only.
