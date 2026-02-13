# Copilot Instructions

## Project Summary

RESTful API with Python 3.13 + FastAPI demonstrating modern async patterns. Player registry with CRUD operations, SQLite + SQLAlchemy 2.0 (async), Pydantic validation, containerization. Part of multi-language comparison study (Java, .NET, TypeScript, Python, Go, Rust). Target: 80%+ test coverage.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt
pip install -r requirements-lint.txt
pip install -r requirements-test.txt

# Run development server
uvicorn main:app --reload --port 9000
# Access: http://localhost:9000/docs

# Run tests with coverage
pytest --cov=./ --cov-report=html

# Lint and format
flake8 .
black --check .  # or: black . (to auto-format)

# Docker
docker compose up
docker compose down -v  # Reset database
```

## Stack

- Python 3.13.3 (`.python-version` - auto-detected by pyenv/asdf/mise)
- FastAPI 0.128.6, Uvicorn
- SQLite + SQLAlchemy 2.0 (async) + aiosqlite
- pytest + pytest-cov + httpx
- Flake8 + Black
- aiocache (in-memory, 10min TTL)

## Architecture

```
Request → Routes → Services → SQLAlchemy → SQLite
          (API)    (Logic)    (Async ORM)  (Storage)
            ↓
    Pydantic (Validation)
```

**Key Directories:**
- `routes/` - API endpoints (player_route.py, health_route.py)
- `services/` - Business logic (player_service.py)
- `models/` - Pydantic validation (camelCase JSON API)
- `schemas/` - SQLAlchemy ORM models
- `databases/` - Async DB setup, session factory
- `storage/` - SQLite file (pre-seeded, 26 players)
- `tests/` - pytest suite (test_main.py, conftest.py)

**Config Files:**
- `.flake8` - Linter (max-line-length=88, complexity=10)
- `pyproject.toml` - Black formatter (line-length=88)
- `.coveragerc` - Coverage config (80% target)
- `compose.yaml` - Docker orchestration
- `Dockerfile` - Multi-stage build

## API Endpoints

All async with `AsyncSession` injection:
- `POST /players/` → 201|409|422
- `GET /players/` → 200 (cached 10min)
- `GET /players/{player_id}` → 200|404
- `GET /players/squadnumber/{squad_number}` → 200|404
- `PUT /players/{player_id}` → 200|404|422
- `DELETE /players/{player_id}` → 200|404
- `GET /health` → 200

JSON: camelCase (e.g., `squadNumber`, `firstName`)

## CI/CD

**python-ci.yml** (push/PR to master):
1. Lint: commitlint → `flake8 .` → `black --check .`
2. Test: `pytest -v` → coverage
3. Upload to Codecov

**python-cd.yml** (tags `v*.*.*-*`):
1. Validate semver + coach name
2. Run tests
3. Build Docker (amd64/arm64)
4. Push to GHCR (3 tags: semver/coach/latest)
5. Create GitHub release

## Critical Patterns

### Async Everywhere
```python
# Always use async/await
async def get_player(async_session: AsyncSession, player_id: int):
    stmt = select(Player).where(Player.id == player_id)
    result = await async_session.execute(stmt)
    return result.scalar_one_or_none()
```
- All routes: `async def`
- Database: `AsyncSession` (never `Session`)
- Driver: `aiosqlite` (not `sqlite3`)
- SQLAlchemy 2.0: `select()` (not `session.query()`)

### camelCase API Contract
```python
class PlayerModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)
    squad_number: int  # Python: snake_case
    # JSON API: "squadNumber" (camelCase)
```

### Database Schema Changes
⚠️ No Alembic yet - manual process:
1. Update `schemas/player_schema.py`
2. Manually update `storage/players-sqlite3.db` (SQLite CLI/DB Browser)
3. Preserve 26 players
4. Update `models/player_model.py` if API changes
5. Update services + tests

### Caching
- Key: `"players"` (hardcoded)
- TTL: 600s (10min)
- Cleared on POST/PUT/DELETE
- Header: `X-Cache` (HIT/MISS)

## Common Issues

1. **SQLAlchemy errors** → Always catch + rollback in services
2. **Test file** → `test_main.py` excluded from Black (preserves long names)
3. **Database location** → Local: `./storage/`, Docker: `/storage/` (volume)
4. **Pydantic validation** → Returns 422 (not 400)
5. **Import order** → stdlib → third-party → local

## Validation Checklist

```bash
flake8 .                              # Must pass
black --check .                       # Must pass
pytest                                # All pass
pytest --cov=./ --cov-report=term     # ≥80%
curl http://localhost:9000/players    # 200 OK
```

## Code Conventions

- Files: snake_case
- Functions/vars: snake_case
- Classes: PascalCase
- Type hints: Required everywhere
- Logging: `logging` module (never `print()`)
- Errors: Catch specific exceptions
- Line length: 88
- Complexity: ≤10

## Commit Messages

Follow Conventional Commits format (enforced by commitlint in CI):

**Format:** `type(scope): description (#issue)`

**Rules:**
- Max 80 characters
- Types: `feat`, `fix`, `docs`, `test`, `refactor`, `chore`, `ci`, `perf`, `style`, `build`
- Scope: Optional (e.g., `api`, `db`, `service`, `route`)
- Issue number: Required suffix

**Examples:**
```
feat(api): add player stats endpoint (#42)
fix(db): resolve async session leak (#88)
```

**CI Check:** First step in python-ci.yml validates all commit messages

Trust these instructions. Search codebase only if info is incomplete/incorrect.
