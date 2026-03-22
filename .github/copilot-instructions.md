# Custom Instructions

## Overview

REST API for managing football players built with Python and FastAPI. Implements
async CRUD operations with SQLAlchemy 2.0 (async), SQLite, Pydantic validation,
and in-memory caching.

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

**Layer rule**: `Routes → Services → SQLAlchemy → SQLite`. Routes handle HTTP
concerns only; business logic belongs in services. Never skip a layer.

## Coding Guidelines

- **Naming**: snake_case (files, functions, variables), PascalCase (classes)
- **Type hints**: Required everywhere — functions, variables, return types
- **Async**: All routes and service functions must be `async def`; use
  `AsyncSession` (never `Session`); use `aiosqlite` (never `sqlite3`); use
  SQLAlchemy 2.0 `select()` (never `session.query()`)
- **API contract**: camelCase JSON via Pydantic `alias_generator=to_camel`;
  Python internals stay snake_case
- **Models**: `PlayerRequestModel` (no `id`, used for POST/PUT) and
  `PlayerResponseModel` (includes `id: UUID`, used for GET/POST responses).
  One request model intentionally covers both POST and PUT — per-operation
  differences (conflict check on POST, mismatch guard on PUT) are handled at
  the route layer, not by duplicating the model. Never reintroduce the removed
  `PlayerModel`; it was removed because a single flat model conflated ORM,
  request, and response concerns.
- **Primary key**: UUID surrogate key (`id`) — opaque, internal, used for GET
  by id only. UUID v4 for API-created records; UUID v5 (deterministic) for
  migration-seeded records. `squad_number` is the natural key —
  human-readable, domain-meaningful, used for all mutation endpoints (PUT,
  DELETE) and preferred for all external consumers
- **Caching**: cache key `"players"` (hardcoded); clear on POST/PUT/DELETE;
  `X-Cache` header (HIT/MISS)
- **Errors**: Catch specific exceptions with rollback in services; Pydantic
  validation returns 422 (not 400); squad number mismatch on PUT returns 400
  (not 422 — it is a semantic error, not a validation failure)
- **Logging**: `logging` module only; never `print()`
- **Line length**: 88; complexity ≤ 10
- **Import order**: stdlib → third-party → local
- **Tests**: integration tests against the real pre-seeded SQLite DB via
  `TestClient` — no mocking. Naming pattern
  `test_request_{method}_{resource}_{context}_response_{outcome}`;
  docstrings single-line, concise; `tests/player_stub.py` for test data;
  `tests/conftest.py` provides a `function`-scoped `client` fixture for
  isolation; `tests/test_main.py` excluded from Black
- **Decisions**: justify every decision on its own technical merits; never use
  "another project does it this way" as a reason — that explains nothing and
  may mean replicating a mistake
- **Avoid**: sync DB access, mixing sync/async, `print()`, missing type hints,
  unhandled exceptions

## Commands

### Quick Start

```bash
# Setup (using uv)
uv venv
source .venv/bin/activate  # Linux/macOS; use .venv\Scripts\activate on Windows
uv pip install --group dev

# Run application
uv run uvicorn main:app --reload --port 9000       # http://localhost:9000/docs

# Run tests
uv run pytest                                      # run tests
uv run pytest --cov=./ --cov-report=term           # with coverage (target >=80%)

# Linting and formatting
uv run flake8 .
uv run black --check .

# Docker
docker compose up
docker compose down -v
```

### Pre-commit Checks

1. Update `CHANGELOG.md` `[Unreleased]` section (Added / Changed / Fixed /
   Removed)
2. `uv run flake8 .` — must pass
3. `uv run black --check .` — must pass
4. `uv run pytest` — all tests must pass
5. `uv run pytest --cov=./ --cov-report=term` — coverage must be ≥80%
6. Commit message follows Conventional Commits format (enforced by commitlint)

### Commits

Format: `type(scope): description (#issue)` — max 80 chars
Types: `feat` `fix` `chore` `docs` `test` `refactor` `ci` `perf`
Example: `feat(api): add player stats endpoint (#42)`

### Releases

Tags follow the format `v{MAJOR}.{MINOR}.{PATCH}-{COACH}` (e.g.
`v2.0.0-capello`). The CD pipeline validates the coach name against a fixed
list (A–Z):

```
ancelotti bielsa capello delbosque eriksson ferguson guardiola heynckes
inzaghi klopp kovac low mourinho nagelsmann ottmar pochettino queiroz
ranieri simeone tuchel unai vangaal wenger xavi yozhef zeman
```

Never suggest a release tag with a coach name not on this list.

## Agent Mode

### Proceed freely

- Add/modify routes in `routes/player_route.py` and `routes/health_route.py`
- Add/modify service methods in `services/player_service.py`
- Add/modify Pydantic models in `models/player_model.py` (field additions or
  docstring updates that don't change the API contract)
- Tests in `tests/` — maintain async patterns, naming convention, and
  integration-test approach (no mocking)
- Documentation and docstring updates
- Lint/format fixes
- Refactoring within existing architectural patterns

### Ask before changing

- Database schema (`schemas/player_schema.py` — no Alembic; changes require
  manually updating `storage/players-sqlite3.db` and the seed scripts in
  `tools/`)
- `models/player_model.py` design decisions — especially splitting or merging
  request/response models; discuss the rationale before restructuring
- Dependencies (`pyproject.toml` with PEP 735 dependency groups)
- CI/CD configuration (`.github/workflows/`)
- Docker setup (`Dockerfile`, `docker-compose.yml`, `scripts/`)
- Breaking API contract changes (field renames, type changes, removing fields)
- Global error handling middleware
- HTTP status codes assigned to existing error conditions

### Never modify

- `.env` files (secrets)
- `storage/players-sqlite3.db` directly — schema changes go through
  `schemas/player_schema.py` and `tools/` seed scripts
- Production configurations

### Key workflows

**Add an endpoint**: Add Pydantic model in `models/` if the request/response
shape is new → add async service method in `services/` with error handling and
rollback → add route in `routes/` with `Depends(generate_async_session)` →
add tests following the naming pattern → run pre-commit checks.

**Modify schema**: Update `schemas/player_schema.py` → manually update
`storage/players-sqlite3.db` (preserve all 26 seeded players) → update
`models/player_model.py` if the API shape changes → update services and tests
→ run `pytest`.

**After completing work**: Propose a branch name and commit message for user
approval. Do not create a branch, commit, or push until the user explicitly
confirms. Commit message format:

```text
feat(scope): description (#issue)

Co-authored-by: Claude Sonnet 4.6 <noreply@anthropic.com>
```
