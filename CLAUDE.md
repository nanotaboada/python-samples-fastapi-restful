# CLAUDE.md

## Claude Code

- Run `/pre-commit` to execute the full pre-commit checklist for this project.
- Run `/pre-release` before tagging a release.
- See `.claude/skills/create-issue/SKILL.md` for the SDD issue workflow, and
  `.claude/skills/add-endpoint/SKILL.md` for the endpoint/schema workflows.

## Structure

**Layer rule**: `Routes → Services → SQLAlchemy → SQLite`. Routes handle HTTP
concerns only; business logic belongs in services. Never skip a layer.
`tools/` is legacy (superseded by Alembic migrations); `gunicorn.conf.py` is
used by the Docker entrypoint.

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
- **Tests**: integration tests against the real SQLite DB (seeded via
  Alembic migrations) via `TestClient` — no mocking. Naming pattern
  `test_request_{method}_{resource}_{context}_response_{outcome}`;
  docstrings single-line, concise; `tests/player_fake.py` for test data;
  `tests/conftest.py` provides a `function`-scoped `client` fixture for
  isolation; `tests/test_main.py` excluded from Black;
  `tests/test_migrations.py` covers Alembic downgrade paths
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

# Apply migrations (required once before first run, and after down -v)
uv run alembic upgrade head

# Run application
uv run uvicorn main:app --reload --port 9000       # http://localhost:9000/docs

# Run tests
uv run pytest                                      # run tests
uv run pytest --cov=./ --cov-report=term           # with coverage (target >=80%)

# Migration workflow
uv run alembic upgrade head                        # apply all pending migrations
uv run alembic downgrade -1                        # roll back last migration
uv run alembic revision --autogenerate -m "desc"   # generate migration from schema

# Docker
docker compose up
docker compose down -v
```

### Commits

Format: `type(scope): description (#issue)` — max 80 chars
Types: `feat` `fix` `chore` `docs` `test` `refactor` `ci` `perf`
Example: `feat(api): add player stats endpoint (#42)`

### Releases

Tags follow the format `v{MAJOR}.{MINOR}.{PATCH}-{COACH}` (e.g.
`v2.0.0-capello`). Valid coach names (A–Z) are maintained in `CHANGELOG.md`'s
naming-convention table — the same table `/pre-release` reads. Never suggest
a release tag with a coach name not in that table.

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

- Database schema (`schemas/player_schema.py`) and Alembic migrations
  (`alembic/versions/`) — schema changes require a new migration file;
  seed data changes require updating the relevant migration and any test
  fixtures that reference specific UUIDs
- `models/player_model.py` design decisions — especially splitting or merging
  request/response models; discuss the rationale before restructuring
- Dependencies (`pyproject.toml` with PEP 735 dependency groups)
- CI/CD configuration (`.github/workflows/`)
- Docker setup (`Dockerfile`, `compose.yaml`, `scripts/`)
- Breaking API contract changes (field renames, type changes, removing fields)
- Global error handling middleware
- HTTP status codes assigned to existing error conditions

### Never modify

- `.env` files (secrets)
- `alembic/versions/` migration files once merged to `master` — migrations
  are append-only; fix forward with a new migration, never edit history
- Production configurations

### Creating Issues

Spec-Driven Development (SDD): discuss in Plan mode first, create a GitHub
Issue as the spec artifact, then implement. Always offer to draft an issue
before writing code. See `.claude/skills/create-issue/SKILL.md` for the
feature/bug issue templates.

### Key workflows

See `.claude/skills/add-endpoint/SKILL.md` for the "add an endpoint" and
"modify schema" recipes.

**After completing work**: Propose a branch name and commit message for user
approval. Do not create a branch, commit, or push until the user explicitly
confirms.

## Invariants (never change without explicit discussion)

- **Port**: 9000
- **API contract**: endpoints, HTTP status codes, and response shapes are fixed;
  do not change them without explicit discussion
- **Commit format**: `type(scope): description (#issue)` — max 80 chars
- **Conventional Commits types**: `feat` `fix` `chore` `docs` `test` `refactor` `ci` `perf`
- **CHANGELOG.md**: `[Unreleased]` section must be updated before every commit

## Architecture Decision Records

Significant architectural decisions are documented in `docs/adr/` (ADR-0001–0013).
Load these before proposing structural changes. When a proposal would change an
accepted decision, create a new ADR rather than editing the existing one.
