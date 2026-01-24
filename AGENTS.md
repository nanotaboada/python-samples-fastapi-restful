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

**Coverage requirement**: Tests must maintain coverage. The CI pipeline enforces this with `.coveragerc` configuration.

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
1. Run `flake8 .` - must pass with no errors
2. Run `black --check .` - must pass with no formatting changes needed (or run `black .` to auto-fix)
3. Run `pytest --cov=./ --cov-report=term` - all tests must pass

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

## CI/CD Pipeline

### Continuous Integration (python-ci.yml)

**Trigger**: Push to `master` or PR to `master`

**Jobs**:
1. **Lint**: Commit messages (commitlint) → Flake8 → Black check
2. **Test**: pytest with verbose output → coverage report generation
3. **Coverage**: Upload to Codecov and Codacy (requires secrets)

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

```
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
Open http://localhost:9000/docs - Interactive Swagger UI with "Try it out" buttons

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

## Important Notes

- **Never commit secrets**: No API keys, tokens, or credentials in code
- **Test coverage**: Maintain existing coverage levels (currently high)
- **Commit messages**: Follow conventional commits (enforced by commitlint)
- **Python version**: Must use 3.13.3 for consistency with CI/CD
- **Dependencies**: Keep requirements files in sync with actual usage
- **Database**: SQLite is for demo/development only - not production-ready
