# Agent Instructions

## Autonomy Guidelines

### Proceed Freely

- Add/modify routes and endpoints
- Implement service layer logic
- Write tests (maintain async patterns)
- Update docs (README, docstrings)
- Fix lint/format errors
- Refactor within architectural patterns
- Optimize queries

### Ask First

- Database schema (no Alembic - manual updates)
- Dependencies (requirements*.txt)
- CI/CD (.github/workflows/)
- Docker (Dockerfile, compose.yaml)
- Environment variables
- API contracts (breaking changes)
- Global error handling

### Never Change

- .env files (secrets)
- Production configs (without approval)
- Core architecture (layered pattern)
- Async/await patterns (mandatory)
- Type hints (mandatory)

## Workflow: Add Endpoint

1. Pydantic model (`models/player_model.py`):

```python
class PlayerStatsModel(MainModel):
    wins: int
    losses: int
```

1. Service method (`services/player_service.py`):

```python
async def get_player_stats_async(
    async_session: AsyncSession,
    player_id: int
) -> PlayerStatsModel:
    # Logic with error handling
    ...
```

1. Route (`routes/player_route.py`):

```python
@api_router.get(
    "/players/{player_id}/stats",
    response_model=PlayerStatsModel,
    status_code=200
)
async def get_stats(
    player_id: int,
    async_session: AsyncSession = Depends(generate_async_session)
):
    return await player_service.get_player_stats_async(
        async_session, player_id
    )
```

1. Tests (`tests/test_main.py`):

```python
def test_request_get_player_id_existing_stats_response_status_ok(client):
    """GET /players/{player_id}/stats with existing ID returns 200 OK"""
    ...
```

1. Validate: `flake8 .` → `black .` → `pytest`

## Workflow: Modify Schema

No Alembic migrations:

1. Update `schemas/player_schema.py` (SQLAlchemy ORM)
2. Manually update `storage/players-sqlite3.db`
3. Preserve 26 players
4. Update `models/player_model.py` if API changes
5. Update services
6. Add tests

## Design Philosophy

### Layered Architecture

- Routes: HTTP concerns (validation, status codes)
- Services: Business logic, transactions
- Separation: Test logic without HTTP

### Async Throughout

- FastAPI: Concurrent requests
- SQLAlchemy: Non-blocking I/O
- Never mix sync/async DB access

### camelCase JSON

- API: JavaScript conventions
- Python: snake_case (Pythonic)
- Consistency across comparison repos

## Testing Strategy

**Naming Pattern:**

```text
test_request_{method}_{resource}_{param_or_context}_response_{outcome}
```

- `players` (collection) vs `player` (single resource)
- Examples: `test_request_get_players_response_status_ok`, `test_request_post_player_body_empty_response_status_unprocessable`

**Guidelines:**

- Use `tests/player_stub.py` for data
- Test real DB (fixtures handle setup)
- Cover: happy paths + errors + edges
- Cache tests: verify `X-Cache` header
- Docstrings: Single-line, concise, no "Expected:" prefix

## Planning Tips

1. Check `.github/copilot-instructions.md` for commands
2. Read existing tests for behavior patterns
3. Consider cache invalidation (player data changes)
4. Remember: 80% coverage requirement
5. Schema changes = manual DB updates

## Common Gotchas

- Query results: `.scalars()` for ORM objects
- Cache key: `"players"` (hardcoded)
- `test_main.py`: Excluded from Black
- SQLAlchemy errors: Catch + rollback in services
- Validation errors: 422 (not 400)
- Test naming: `test_request_{method}_{resource}_{context}_response_{outcome}` pattern

## Cross-Tool Notes

For comprehensive onboarding, see `.github/copilot-instructions.md` (auto-loaded). This file provides agent-specific autonomy boundaries and workflows.
