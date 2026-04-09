# 🧪 RESTful API with Python 3 and FastAPI

[![Python CI](https://github.com/nanotaboada/python-samples-fastapi-restful/actions/workflows/python-ci.yml/badge.svg)](https://github.com/nanotaboada/python-samples-fastapi-restful/actions/workflows/python-ci.yml)
[![Python CD](https://github.com/nanotaboada/python-samples-fastapi-restful/actions/workflows/python-cd.yml/badge.svg)](https://github.com/nanotaboada/python-samples-fastapi-restful/actions/workflows/python-cd.yml)
[![CodeQL Advanced](https://github.com/nanotaboada/python-samples-fastapi-restful/actions/workflows/codeql.yml/badge.svg)](https://github.com/nanotaboada/python-samples-fastapi-restful/actions/workflows/codeql.yml)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=nanotaboada_python-samples-fastapi-restful&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=nanotaboada_python-samples-fastapi-restful)
[![codecov](https://codecov.io/gh/nanotaboada/python-samples-fastapi-restful/branch/master/graph/badge.svg?token=A1WNZPRQEJ)](https://codecov.io/gh/nanotaboada/python-samples-fastapi-restful)
[![CodeFactor](https://www.codefactor.io/repository/github/nanotaboada/python-samples-fastapi-restful/badge)](https://www.codefactor.io/repository/github/nanotaboada/python-samples-fastapi-restful)
[![License: MIT](https://img.shields.io/badge/License-MIT-3DA639.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![Dependabot](https://img.shields.io/badge/Dependabot-contributing-025E8C?logo=dependabot&logoColor=white&labelColor=181818)
![Copilot](https://img.shields.io/badge/Copilot-contributing-8662C5?logo=githubcopilot&logoColor=white&labelColor=181818)
![Claude](https://img.shields.io/badge/Claude-contributing-D97757?logo=claude&logoColor=white&labelColor=181818)
![CodeRabbit](https://img.shields.io/badge/CodeRabbit-reviewing-FF570A?logo=coderabbit&logoColor=white&labelColor=181818)

Proof of Concept for a RESTful Web Service built with **FastAPI** and **Python 3.13**. This project demonstrates best practices for building a layered, testable, and maintainable API implementing CRUD operations for a Players resource (Argentina 2022 FIFA World Cup squad).

## Features

- 🏗️ **Async Architecture** - Async/await throughout with SQLAlchemy 2.0 and dependency injection via FastAPI's `Depends()`
- 📚 **Interactive Documentation** - Auto-generated Swagger UI with VS Code and JetBrains REST Client support
- ⚡ **Performance Caching** - In-memory caching with aiocache and async SQLite operations
- ✅ **Input Validation** - Pydantic models enforce request/response schemas with automatic error responses
- 🐳 **Containerized Deployment** - Production-ready Docker setup with migration-based database initialization
- 🔄 **Automated Pipeline** - Continuous integration with Black, Flake8, and automated testing

## Tech Stack

| Category | Technology |
| -------- | ---------- |
| **Language** | [Python 3.13](https://www.python.org/) |
| **Web Framework** | [FastAPI](https://fastapi.tiangolo.com/) + [Uvicorn](https://www.uvicorn.org/) |
| **ORM** | [SQLAlchemy 2.0 (async)](https://docs.sqlalchemy.org/en/20/) + [aiosqlite](https://github.com/omnilib/aiosqlite) |
| **Database** | [SQLite](https://www.sqlite.org/) |
| **Validation** | [Pydantic](https://docs.pydantic.dev/) |
| **Caching** | [aiocache](https://github.com/aio-libs/aiocache) (in-memory, 10-minute TTL) |
| **Testing** | [pytest](https://pytest.org/) + [pytest-cov](https://github.com/pytest-dev/pytest-cov) + [httpx](https://www.python-httpx.org/) |
| **Linting / Formatting** | [Flake8](https://flake8.pycqa.org/) + [Black](https://black.readthedocs.io/) |
| **Containerization** | [Docker](https://www.docker.com/) & [Docker Compose](https://docs.docker.com/compose/) |

## Architecture

Layered architecture with dependency injection via FastAPI's `Depends()` mechanism and Pydantic for request/response validation.

```mermaid
%%{init: {
  "theme": "default",
  "themeVariables": {
    "fontFamily": "Fira Code, Consolas, monospace",
    "textColor": "#555",
    "lineColor": "#555"
  }
}}%%

graph RL

    tests[tests]

    main[main]
    routes[routes]
    fastapi[FastAPI]
    aiocache[aiocache]

    services[services]

    models[models]
    pydantic[Pydantic]

    schemas[schemas]

    databases[databases]
    sqlalchemy[SQLAlchemy]

    %% Strong dependencies

    routes --> main
    fastapi --> main

    fastapi --> routes
    aiocache --> routes
    services --> routes
    models --> routes
    databases --> routes

    schemas --> services
    models --> services
    sqlalchemy --> services
    pydantic --> models

    databases --> schemas
    sqlalchemy --> schemas
    sqlalchemy --> databases

    %% Soft dependencies

    sqlalchemy -.-> routes
    main -.-> tests

    %% Node styling with stroke-width
    classDef core fill:#b3d9ff,stroke:#6db1ff,stroke-width:2px,color:#555,font-family:monospace;
    classDef deps fill:#ffcccc,stroke:#ff8f8f,stroke-width:2px,color:#555,font-family:monospace;
    classDef test fill:#ccffcc,stroke:#53c45e,stroke-width:2px,color:#555,font-family:monospace;

    class main,routes,services,schemas,databases,models core
    class fastapi,sqlalchemy,pydantic,aiocache deps
    class tests test
```

> *Arrows follow the injection direction (A → B means A is injected into B). Solid = runtime dependency, dotted = structural. Blue = core domain, red = third-party, green = tests.*

Significant architectural decisions are documented in [`docs/adr/`](docs/adr/).

## API Reference

Interactive API documentation is available via Swagger UI at `http://localhost:9000/docs` when the server is running.

| Method | Endpoint | Description | Status |
| ------ | -------- | ----------- | ------ |
| `GET` | `/players/` | List all players | `200 OK` |
| `GET` | `/players/{player_id}` | Get player by ID | `200 OK` |
| `GET` | `/players/squadnumber/{squad_number}` | Get player by squad number | `200 OK` |
| `POST` | `/players/` | Create new player | `201 Created` |
| `PUT` | `/players/squadnumber/{squad_number}` | Update player by squad number | `204 No Content` |
| `DELETE` | `/players/squadnumber/{squad_number}` | Remove player by squad number | `204 No Content` |
| `GET` | `/health` | Health check | `200 OK` |

Error codes: `400 Bad Request` (squad number mismatch on `PUT`) · `404 Not Found` (player not found) · `409 Conflict` (duplicate squad number on `POST`) · `422 Unprocessable Entity` (schema validation failed)

For complete endpoint documentation with request/response schemas, explore the [interactive Swagger UI](http://localhost:9000/docs).

Alternatively, use [`rest/players.rest`](rest/players.rest) with the [REST Client](https://marketplace.visualstudio.com/items?itemName=humao.rest-client) extension for VS Code, or the built-in HTTP Client in JetBrains IDEs (IntelliJ IDEA, PyCharm, WebStorm).

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.13+** — uses `.python-version` for automatic activation with [pyenv](https://github.com/pyenv/pyenv), [asdf](https://asdf-vm.com/), or [mise](https://mise.jdx.dev/)
- **[uv](https://docs.astral.sh/uv/)** (recommended) — fast Python package and project manager
- **Docker & Docker Compose** (optional, for containerized deployment)

## Quick Start

### Clone

```bash
git clone https://github.com/nanotaboada/python-samples-fastapi-restful.git
cd python-samples-fastapi-restful
```

### Install

Dependencies are defined in `pyproject.toml` using [PEP 735](https://peps.python.org/pep-0735/) dependency groups.

```bash
# Install uv (if you haven't already)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create a virtual environment and install all dependencies
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install --group dev
```

| Command | Description |
| ------- | ----------- |
| `uv pip install` | Production dependencies only |
| `uv pip install --group test` | Test dependencies |
| `uv pip install --group lint` | Linting dependencies |
| `uv pip install --group dev` | All (test + lint + production) |

### Run

```bash
# Apply database migrations (required once before the first run, and after
# docker compose down -v)
uv run alembic upgrade head

uv run uvicorn main:app --reload --port 9000
```

### Access

Once the application is running, you can access:

- **API Server**: `http://localhost:9000`
- **Swagger UI**: `http://localhost:9000/docs`
- **Health Check**: `http://localhost:9000/health`

## Containers

### Build and Start

```bash
docker compose up
```

> 💡 **Note:** On first run, the entrypoint applies Alembic migrations (`alembic upgrade head`), which creates the database and seeds all 26 players. On subsequent runs, migrations are a no-op and the volume data is preserved.

### Stop

```bash
docker compose down
```

### Reset Database

To remove the volume and re-apply migrations from scratch on next start:

```bash
docker compose down -v
```

### Pull Docker Images

Each release publishes multiple tags for flexibility:

```bash
# By semantic version (recommended for production)
docker pull ghcr.io/nanotaboada/python-samples-fastapi-restful:1.0.0

# By coach name (memorable alternative)
docker pull ghcr.io/nanotaboada/python-samples-fastapi-restful:ancelotti

# Latest release
docker pull ghcr.io/nanotaboada/python-samples-fastapi-restful:latest
```

## Environment Variables

```bash
# Full async database URL (SQLite default, PostgreSQL compatible)
# SQLite (local/test):
DATABASE_URL=sqlite+aiosqlite:///./players-sqlite3.db
# PostgreSQL (Docker/production):
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/playersdb

# Legacy: SQLite file path — used only when DATABASE_URL is not set
STORAGE_PATH=./players-sqlite3.db

# Python output buffering: set to 1 for real-time logs in Docker
PYTHONUNBUFFERED=1
```

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details on:

- Code of Conduct
- Development workflow and best practices
- Commit message conventions (Conventional Commits)
- Pull request process and requirements

**Key guidelines:**

- Follow [Conventional Commits](https://www.conventionalcommits.org/) for commit messages
- Ensure all tests pass (`uv run pytest`)
- Run `uv run black .` before committing
- Keep changes small and focused
- Review `.github/copilot-instructions.md` for architectural patterns

**Testing:**

Run the test suite with pytest:

```bash
# Run all tests
uv run pytest

# Run tests with coverage report
uv run pytest --cov=./ --cov-report=term
```

## Command Summary

| Command | Description |
| ------- | ----------- |
| `uv run uvicorn main:app --reload --port 9000` | Start development server |
| `uv pip install --group dev` | Install all dependencies |
| `uv run pytest` | Run all tests |
| `uv run pytest --cov=./ --cov-report=term` | Run tests with coverage |
| `uv run flake8 .` | Lint code |
| `uv run black --check .` | Check formatting |
| `uv run black .` | Auto-format code |
| `docker compose build` | Build Docker image |
| `docker compose up` | Start Docker container |
| `docker compose down` | Stop Docker container |
| `docker compose down -v` | Stop and remove Docker volume |
| **AI Commands** | |
| `/pre-commit` | Runs linting, tests, and quality checks before committing |
| `/pre-release` | Runs pre-release validation workflow |

## Legal

This project is provided for educational and demonstration purposes and may be used in production at your own discretion. All trademarks, service marks, product names, company names, and logos referenced herein are the property of their respective owners and are used solely for identification or illustrative purposes.
