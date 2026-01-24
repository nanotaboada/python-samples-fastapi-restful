# GitHub Copilot Instructions

> **⚡ Token Efficiency Note**: This is a minimal pointer file (~500 tokens, auto-loaded by Copilot).  
> For complete operational details, reference: `#file:AGENTS.md` (~2,500 tokens, loaded on-demand)  
> For specialized knowledge, use: `#file:SKILLS/<skill-name>/SKILL.md` (loaded on-demand when needed)

## 🎯 Quick Context

**Project**: FastAPI REST API demonstrating modern Python async patterns  
**Stack**: Python 3.13 • FastAPI • SQLAlchemy (async) • SQLite • Docker • pytest  
**Pattern**: Routes → Services → Database (layered architecture)  
**Philosophy**: Learning-focused PoC emphasizing async/await and type safety

## 📐 Core Conventions

- **Naming**: snake_case for functions/variables, PascalCase for classes
- **Type Hints**: Mandatory throughout (enforced by mypy if enabled)
- **Async**: All I/O operations use `async`/`await`
- **Testing**: pytest with fixtures and async support
- **Formatting**: black (opinionated), flake8 (linting)

## 🏗️ Architecture at a Glance

```
Route → Service → Database
  ↓         ↓
Cache    Session
```

- **Routes**: FastAPI endpoints with dependency injection
- **Services**: Async database operations via SQLAlchemy
- **Database**: SQLite with async support (`aiosqlite`)
- **Models**: Pydantic for validation, SQLAlchemy for ORM
- **Cache**: aiocache SimpleMemoryCache (10min/1hr TTL)

## ✅ Copilot Should

- Generate idiomatic async FastAPI code with proper type hints
- Use SQLAlchemy async APIs (`select()`, `scalars()`, `session.commit()`)
- Follow dependency injection pattern with `Depends()`
- Write tests with pytest async fixtures
- Apply Pydantic models for request/response validation
- Use structured logging (avoid print statements)
- Implement proper HTTP status codes and responses

## 🚫 Copilot Should Avoid

- Synchronous database operations
- Mixing sync and async code
- Missing type hints on functions
- Using `print()` instead of logging
- Creating routes without caching consideration
- Ignoring Pydantic validation

## ⚡ Quick Commands

```bash
# Run with hot reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Test with coverage
pytest --cov=. --cov-report=term-missing

# Docker
docker compose up

# Swagger: http://localhost:8000/docs
```

## 📚 Need More Detail?

**For operational procedures**: Load `#file:AGENTS.md`  
**For Docker expertise**: *(Planned)* `#file:SKILLS/docker-containerization/SKILL.md`  
**For testing patterns**: *(Planned)* `#file:SKILLS/testing-patterns/SKILL.md`

---

💡 **Why this structure?** Copilot auto-loads this file on every chat (~500 tokens). Loading `AGENTS.md` or `SKILLS/` explicitly gives you deep context only when needed, saving 80% of your token budget!
5. **Caching**: In-memory cache (10 min TTL) with `X-Cache` headers (HIT/MISS)
6. **Async/Await**: All database operations are async

## Coding Guidelines

### Python Style (Strict Enforcement)

- **Formatter**: Black (line length: 88, target: Python 3.13)
- **Linter**: flake8 (max-complexity: 10, ignores: E203, W503)
- **Run Before Commit**: `black .` and `flake8`
- **Imports**: SQLAlchemy 2.0+ style (use `select()` not legacy `Query`)
- **Docstrings**: Google-style docstrings for all modules, classes, and functions
- **Type Hints**: Use type annotations for function parameters and return values

### File Exclusions

Black and flake8 exclude:
- `.venv`, `.git`, `.github`, `.pytest_cache`, `__pycache__`
- `assets/`, `htmlcov/`, `postman_collections/`, `scripts/`, `storage/`
- Exception: `tests/test_main.py` allows E501 (long lines for test names)

### Commit Conventions

Follow **Conventional Commits** (enforced by commitlint):
- `feat:` for new features
- `fix:` for bug fixes
- `chore:` for maintenance/tooling
- Max header length: 80 characters
- Max body line length: 80 characters

## Common Commands

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt
pip install -r requirements-lint.txt
pip install -r requirements-test.txt

# IMPORTANT: Activate virtual environment before running commands
source .venv/bin/activate

# Start server (auto-reload on port 9000)
uvicorn main:app --reload --port 9000

# Access interactive API docs
# http://localhost:9000/docs

# Format code (must run from venv)
black .

# Lint code (must run from venv)
flake8 .

# Run tests
pytest -v

# Run tests with coverage
pytest --cov=./ --cov-report=xml --cov-report=term
```

### Docker

```bash
# Build image
docker compose build

# Start app (initializes DB from seed on first run)
docker compose up

# Stop app
docker compose down

# Reset database (removes volume)
docker compose down -v
```

## Database Details

- **Path**: Controlled by `STORAGE_PATH` env var (default: `./storage/players-sqlite3.db`)
- **Docker Volume**: Persistent volume at `/storage/` in container
- **Initialization**: On first Docker run, `entrypoint.sh` copies seed DB from `/app/hold/` to `/storage/`
- **Schema**: Single `players` table with columns: id (PK), firstName, middleName, lastName, dateOfBirth, squadNumber (unique), position, abbrPosition, team, league, starting11

## API Endpoints

| Method | Path                                | Description                  | Cache |
|--------|-------------------------------------|------------------------------|-------|
| GET    | `/health`                           | Health check                 | No    |
| GET    | `/players/`                         | Get all players              | Yes   |
| GET    | `/players/{player_id}`              | Get player by ID             | No    |
| GET    | `/players/squadnumber/{squad_number}` | Get player by squad number | No    |
| POST   | `/players/`                         | Create new player            | Clears|
| PUT    | `/players/{player_id}`              | Update existing player       | Clears|
| DELETE | `/players/{player_id}`              | Delete player                | Clears|

**Cache Notes**:
- Cache key: `"players"`, TTL: 600s (10 min)
- Cache is cleared on POST/PUT/DELETE operations
- Response header `X-Cache: HIT` or `MISS` indicates cache status

## Testing

- **Framework**: pytest with `TestClient` from FastAPI
- **Fixture**: `client` fixture in `conftest.py` (function scope for test isolation)
- **Coverage Target**: 80% (configured in `codecov.yml`)
- **Test Data**: Use stubs from `tests/player_stub.py`
- **Warnings**: DeprecationWarning from httpx is suppressed in conftest

## CI/CD Pipeline

GitHub Actions workflow (`.github/workflows/python-app.yml`):
1. **Lint Job**: Commitlint → Flake8 → Black (check mode)
2. **Test Job**: pytest with coverage report generation
3. **Coverage Job**: Upload to Codecov and Codacy (only for same-repo PRs)

**All PRs must pass CI checks before review.**

## Common Pitfalls & Solutions

1. **Virtual Environment**: Always activate `.venv` before running black, flake8, or pytest:
   ```bash
   source .venv/bin/activate
   ```

2. **FastAPI Route Ordering**: Static routes MUST be defined before dynamic path parameters. Place `/players/statistics` before `/players/{player_id}`, or FastAPI will try to parse "statistics" as a player_id.
   ```python
   # CORRECT order:
   @api_router.get("/players/statistics")  # Static route first
   @api_router.get("/players/{player_id}") # Dynamic route after
   ```

3. **SQLAlchemy 2.0 Migration**: Use `select()` not `session.query()`. Example:
   ```python
   statement = select(Player).where(Player.id == player_id)
   result = await async_session.execute(statement)
   ```

4. **Async Session Usage**: Always use `Depends(generate_async_session)` in routes, never create sessions manually.

5. **Cache Invalidation**: Remember to call `await simple_memory_cache.clear(CACHE_KEY)` after mutations (POST/PUT/DELETE).

6. **Pydantic Model Conversion**: Use `player_model.model_dump()` to convert Pydantic to dict for SQLAlchemy:
   ```python
   player = Player(**player_model.model_dump())
   ```

7. **Database Path in Docker**: Use `STORAGE_PATH` env var, not hardcoded paths.

8. **Port Conflicts**: Default port is 9000. If occupied, use `--port` flag with uvicorn.

## VS Code Configuration

Recommended extensions (`.vscode/extensions.json`):
- `ms-python.python`, `ms-python.flake8`, `ms-python.black-formatter`
- `github.vscode-pull-request-github`, `github.vscode-github-actions`
- `ms-azuretools.vscode-containers`, `sonarsource.sonarlint-vscode`

Settings (`.vscode/settings.json`):
- Auto-format on save with Black
- Pytest enabled (not unittest)
- Flake8 integration with matching CLI args
- Editor ruler at column 88

## Additional Resources

- **Postman Collection**: `postman_collections/python-samples-fastapi-restful.postman_collection.json`
- **Architecture Diagram**: `assets/images/structure.svg`
- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **SQLAlchemy 2.0**: https://docs.sqlalchemy.org/en/20/
- **Conventional Commits**: https://www.conventionalcommits.org/
