# GitHub Copilot Instructions

## Overview

REST API for managing football players built with Python and FastAPI. Implements async CRUD operations with SQLAlchemy 2.0 (async), SQLite, Pydantic validation, and in-memory caching. Part of a cross-language comparison study (.NET, Go, Java, Rust, TypeScript).

## Tech Stack

- **Language**: Python 3.13
- **Framework**: FastAPI + Uvicorn
- **ORM**: SQLAlchemy 2.0 (async) + aiosqlite
- **Database**: SQLite
- **Validation**: Pydantic
- **Caching**: aiocache (in-memory, 10-minute TTL)
- **Testing**: pytest + pytest-cov + httpx
- **Linting/Formatting**: Flake8 + Black
- **Containerization**: Docker

## Structure

```text
main.py         — application entry point: FastAPI setup, router registration
routes/         — HTTP route definitions + dependency injection     [HTTP layer]
services/       — async business logic + cache management           [business layer]
schemas/        — SQLAlchemy ORM models (database schema)           [data layer]
databases/      — async SQLAlchemy session setup
models/         — Pydantic models for request/response validation
storage/        — SQLite database file (players-sqlite3.db, pre-seeded)
scripts/        — shell scripts for Docker (entrypoint.sh, healthcheck.sh)
tools/          — standalone seed scripts (run manually, not via Alembic)
tests/          — pytest integration tests
```

**Layer rule**: `Routes → Services → SQLAlchemy → SQLite`. Routes handle HTTP concerns only; business logic belongs in services.

## Coding Guidelines

- **Naming**: snake_case (files, functions, variables), PascalCase (classes)
- **Type hints**: Required everywhere — functions, variables, return types
- **Async**: All routes and service functions must be `async def`; use `AsyncSession` (never `Session`); use `aiosqlite` (never `sqlite3`); use SQLAlchemy 2.0 `select()` (never `session.query()`)
- **API contract**: camelCase JSON via Pydantic `alias_generator=to_camel`; Python internals stay snake_case
- **Models**: `PlayerRequestModel` (no `id`, used for POST/PUT) and `PlayerResponseModel` (includes `id: UUID`, used for GET/POST responses); never use the removed `PlayerModel`
- **Primary key**: UUID surrogate key (`id`) — opaque, internal, used for all CRUD operations. UUID v4 for API-created records; UUID v5 (deterministic) for migration-seeded records. `squad_number` is the natural key — human-readable, domain-meaningful, preferred lookup for external consumers
- **Caching**: cache key `"players"` (hardcoded); clear on POST/PUT/DELETE; `X-Cache` header (HIT/MISS)
- **Errors**: Catch specific exceptions with rollback in services; Pydantic validation returns 422 (not 400)
- **Logging**: `logging` module only; never `print()`
- **Line length**: 88; complexity ≤ 10
- **Import order**: stdlib → third-party → local
- **Tests**: naming pattern `test_request_{method}_{resource}_{context}_response_{outcome}`; docstrings single-line, concise; `tests/player_stub.py` for test data; `tests/test_main.py` excluded from Black
- **Avoid**: sync DB access, mixing sync/async, `print()`, missing type hints, unhandled exceptions

## Commands

### Quick Start

```bash
pip install -r requirements.txt
pip install -r requirements-test.txt
pip install -r requirements-lint.txt
uvicorn main:app --reload --port 9000       # http://localhost:9000/docs
pytest                                      # run tests
pytest --cov=./ --cov-report=term           # with coverage (target >=80%)
flake8 .
black --check .
docker compose up
docker compose down -v
```

### Pre-commit Checks

1. Update `CHANGELOG.md` `[Unreleased]` section (Added / Changed / Fixed / Removed)
2. `flake8 .` — must pass
3. `black --check .` — must pass
4. `pytest` — all tests must pass
5. `pytest --cov=./ --cov-report=term` — coverage must be >=80%
6. Commit message follows Conventional Commits format (enforced by commitlint)

### Commits

Format: `type(scope): description (#issue)` — max 80 chars
Types: `feat` `fix` `chore` `docs` `test` `refactor` `ci` `perf`
Example: `feat(api): add player stats endpoint (#42)`

## Agent Mode

### Proceed freely

- Add/modify routes and endpoints
- Service layer logic and cache management
- Tests (maintain async patterns and naming convention)
- Documentation and docstring updates
- Lint/format fixes
- Refactoring within existing architectural patterns

### Ask before changing

- Database schema (`schemas/player_schema.py` — no Alembic, use tools/ seed scripts manually)
- Dependencies (`requirements*.txt`)
- CI/CD configuration (`.github/workflows/`)
- Docker setup
- API contracts (breaking Pydantic model changes)
- Global error handling

### Never modify

- `.env` files (secrets)
- Production configurations
- Async/await patterns (mandatory throughout)
- Type hints (mandatory throughout)
- Core layered architecture

### Key workflows

**Add an endpoint**: Add Pydantic model in `models/` → add async service method in `services/` with error handling → add route in `routes/` with `Depends(generate_async_session)` → add tests following naming pattern → run pre-commit checks.

**Modify schema**: Update `schemas/player_schema.py` → manually update `storage/players-sqlite3.db` (preserve 26 players) → update `models/player_model.py` if API changes → update services and tests → run `pytest`.

**After completing work**: Suggest a branch name (e.g. `feat/add-player-stats`) and a commit message following Conventional Commits including co-author line:

```text
feat(scope): description (#issue)

Co-authored-by: Copilot <175728472+Copilot@users.noreply.github.com>
```
