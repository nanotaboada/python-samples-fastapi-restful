# AGENTS.md

> **⚡ Token Efficiency Note**: This file contains complete operational instructions (~2,500 tokens).
> **Auto-loaded**: NO (load explicitly with `#file:AGENTS.md` when you need detailed procedures)
> **When to load**: Complex workflows, troubleshooting, CI/CD setup, detailed architecture questions
> **Related files**: See `#file:.github/copilot-instructions.md` for quick context (auto-loaded, ~500 tokens)

---

## Quick Start

```bash
# Install all dependencies
pip install -r requirements.txt
pip install -r requirements-lint.txt
pip install -r requirements-test.txt

# Start development server
uvicorn main:app --reload --port 9000

# View API documentation
# Open http://localhost:9000/docs in browser
```

## Python Version

This project requires **Python 3.13.3** (specified in `.python-version`).

If using pyenv, asdf, or mise, the correct version activates automatically. Otherwise, ensure Python 3.13.3 is installed before running any commands.

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

## Development Workflow

### Running Tests

```bash
# Run all tests with verbose output
pytest -v

# Run tests with coverage report (matches CI)
pytest --cov=./ --cov-report=xml --cov-report=term

# Run specific test file
pytest tests/test_main.py -v

# Run specific test function
pytest tests/test_main.py::test_health_check -v
```

**Coverage requirement**: Tests must maintain 80% coverage. Local coverage measurement uses `.coveragerc` configuration, while the CI-enforced 80% target is defined in `codecov.yml`.

### Code Quality

```bash
# Lint code (must pass before committing)
flake8 .

# Check code formatting (must pass before committing)
black --check .

# Auto-format code
black .
```

**Pre-commit checklist**:

1. Update CHANGELOG.md `[Unreleased]` section with your changes (Added/Changed/Deprecated/Removed/Fixed/Security)
2. Run `flake8 .` - must pass with no errors
3. Run `black --check .` - must pass with no formatting changes needed (or run `black .` to auto-fix)
4. Run `pytest --cov=./ --cov-report=term` - all tests must pass
5. Follow conventional commit format (enforced by commitlint)

**Style rules** (enforced by Black + Flake8):

- Line length: 88 characters
- Target: Python 3.13
- Black configuration in `pyproject.toml`
- Flake8 configuration in `.flake8`

### Database Management

```bash
# Database auto-initializes on first app startup via lifespan handler in main.py
# Pre-seeded database ships in storage/players.db

# To reset database to seed state (local development)
rm storage/players.db
# Next app startup will recreate from seed data

# Docker: Reset database by removing volume
docker compose down -v
# Next startup will reinitialize from built-in seed
```

**Important**: The database is SQLite stored in `storage/players.db`. It auto-seeds with football player data on first run.

## Docker Workflow

```bash
# Build container image
docker compose build

# Start application in container
docker compose up

# Start in detached mode (background)
docker compose up -d

# View logs
docker compose logs -f

# Stop application
docker compose down

# Stop and remove database volume (full reset)
docker compose down -v

# Health check (when running)
curl http://localhost:9000/health
```

**First run behavior**: Container copies pre-seeded SQLite database into persistent volume. Subsequent runs reuse that volume to preserve data.

## Release Management

### CHANGELOG Maintenance

**Important**: Update CHANGELOG.md continuously as you work, not just before releases.

**For every meaningful commit**:

1. Add your changes to the `[Unreleased]` section in CHANGELOG.md
2. Categorize under the appropriate heading:
   - **Added**: New features
   - **Changed**: Changes in existing functionality
   - **Deprecated**: Soon-to-be removed features
   - **Removed**: Removed features
   - **Fixed**: Bug fixes
   - **Security**: Security vulnerability fixes
3. Use clear, user-facing descriptions (not just commit messages)
4. Include PR/issue numbers when relevant (#123)

**Example**:

```markdown
## [Unreleased]

### Added
- User authentication with JWT tokens (#145)
- Rate limiting middleware for API endpoints

### Deprecated
- Legacy authentication endpoint /api/v1/auth (use /api/v2/auth instead)

### Fixed
- Null reference exception in player service (#147)

### Security
- Fix SQL injection vulnerability in search endpoint (#148)
```

### Creating a Release

When ready to release:

1. **Update CHANGELOG.md**: Move items from `[Unreleased]` to a new versioned section, then commit and push:

   ```markdown
   ## [1.1.0 - bielsa] - 2026-02-15
   ```

   ```bash
   git add CHANGELOG.md
   git commit -m "docs: prepare changelog for v1.1.0-bielsa release"
   git push
   ```

2. **Create and push tag**:

   ```bash
   git tag -a v1.1.0-bielsa -m "Release 1.1.0 - Bielsa"
   git push origin v1.1.0-bielsa
   ```

3. **CD workflow runs automatically** to publish Docker images and create GitHub Release

See [CHANGELOG.md](CHANGELOG.md#how-to-release) for complete release instructions and coach naming convention.

## CI/CD Pipeline

### Continuous Integration (python-ci.yml)

**Trigger**: Push to `master` or PR to `master`

**Jobs**:

1. **Lint**: Commit messages (commitlint) → Flake8 → Black check
2. **Test**: pytest with verbose output → coverage report generation
3. **Coverage**: Upload to Codecov (requires secrets)

**Local validation** (run this before pushing):

```bash
# Matches CI exactly
flake8 . && \
black --check . && \
pytest -v && \
pytest --cov=./ --cov-report=xml --cov-report=term
```

### Continuous Deployment (python-cd.yml)

**Trigger**: Version tags in format `v{MAJOR}.{MINOR}.{PATCH}-{COACH}`

Example:

```bash
git tag -a v1.0.0-ancelotti -m "Release 1.0.0 - Ancelotti"
git push origin v1.0.0-ancelotti
```

**Pipeline automatically**:

- Runs full test suite with coverage
- Builds multi-stage Docker image
- Pushes to GHCR with multiple tags (version, coach name, latest)
- Generates changelog from commits
- Creates GitHub Release with auto-generated notes

**Coach naming convention**: Famous football coaches A-Z (see README.md for full list)

## Project Architecture

**Structure**: Layered architecture (Routes → Services → Database)

```text
routes/          # FastAPI endpoints with caching
  ├── player_route.py    # CRUD endpoints
  └── health_route.py    # Health check

services/        # Business logic layer
  └── player_service.py  # Async database operations

databases/       # Database setup
  └── player_database.py # SQLAlchemy engine, session, Base

schemas/         # ORM models
  └── player_schema.py   # Player table definition

models/          # API models
  └── player_model.py    # Pydantic validation (camelCase)

tests/           # Test suite
  ├── conftest.py        # Fixtures (TestClient)
  ├── test_main.py       # Endpoint tests
  └── player_stub.py     # Test data
```

**Key patterns**:

- Dependency injection: `AsyncSession` via `Depends(generate_async_session)`
- Async everywhere: SQLAlchemy async, aiocache, FastAPI async endpoints
- Pydantic validation: Request/response with camelCase aliasing
- In-memory caching: aiocache on GET endpoints
- Lifespan handler: DB initialization on app startup

## API Endpoints

| Method | Path                                 | Description                  | Cache |
|--------|--------------------------------------|------------------------------|-------|
| GET    | `/health`                            | Health check                 | No    |
| GET    | `/players/`                          | Get all players              | Yes   |
| GET    | `/players/{player_id}`               | Get player by ID             | No    |
| GET    | `/players/squadnumber/{squad_number}`| Get player by squad number   | No    |
| POST   | `/players/`                          | Create new player            | Clears|
| PUT    | `/players/{player_id}`               | Update existing player       | Clears|
| DELETE | `/players/{player_id}`               | Delete player                | Clears|

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

## Troubleshooting

### Port already in use

```bash
# Kill process on port 9000
lsof -ti:9000 | xargs kill -9
```

### Module import errors

```bash
# Ensure all dependencies installed
pip install -r requirements.txt -r requirements-lint.txt -r requirements-test.txt

# Verify Python version
python --version  # Should be 3.13.3
```

### Database locked errors

```bash
# Stop all running instances
pkill -f uvicorn

# Reset database
rm storage/players.db
```

### Docker issues

```bash
# Clean slate
docker compose down -v
docker compose build --no-cache
docker compose up
```

## Testing the API

### Using FastAPI Docs (Recommended)

Open <http://localhost:9000/docs> - Interactive Swagger UI with "Try it out" buttons

### Using Postman

Pre-configured collection available in `postman_collections/`

### Using curl

```bash
# Health check
curl http://localhost:9000/health

# Get all players
curl http://localhost:9000/players

# Get player by ID
curl http://localhost:9000/players/1

# Create player
curl -X POST http://localhost:9000/players \
  -H "Content-Type: application/json" \
  -d '{"firstName":"Pele","lastName":"Nascimento","club":"Santos","nationality":"Brazil","dateOfBirth":"1940-10-23"}'

# Update player
curl -X PUT http://localhost:9000/players/1 \
  -H "Content-Type: application/json" \
  -d '{"firstName":"Diego","lastName":"Maradona","club":"Napoli","nationality":"Argentina","dateOfBirth":"1960-10-30"}'

# Delete player
curl -X DELETE http://localhost:9000/players/1
```

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
- **FastAPI Docs**: <https://fastapi.tiangolo.com/>
- **SQLAlchemy 2.0**: <https://docs.sqlalchemy.org/en/20/>
- **Conventional Commits**: <https://www.conventionalcommits.org/>

## Important Notes

- **CHANGELOG maintenance**: Update CHANGELOG.md `[Unreleased]` section with every meaningful change
- **Never commit secrets**: No API keys, tokens, or credentials in code
- **Test coverage**: Maintain existing coverage levels (currently high)
- **Commit messages**: Follow conventional commits (enforced by commitlint)
- **Python version**: Must use 3.13.3 for consistency with CI/CD
- **Dependencies**: Keep requirements files in sync with actual usage
- **Database**: SQLite is for demo/development only - not production-ready
