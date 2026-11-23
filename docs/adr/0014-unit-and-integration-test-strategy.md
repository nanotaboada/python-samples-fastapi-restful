# ADR-0014: Unit and Integration Test Strategy

Date: 2026-10-26

## Status

Accepted. Supersedes [ADR-0007](0007-integration-only-test-strategy.md).

## Context

ADR-0007 established integration tests only: every test exercises the
full stack via `TestClient` against the real SQLite database, with no
mocking. Its consequences already flagged two gaps, tracked in issue
#490:

- **Unreachable error paths** — the `SQLAlchemyError` handlers in
  `services/player_service.py` and the HTTP 500 branches in
  `routes/player_route.py` cannot be triggered against a healthy
  SQLite database. They are excluded from coverage with
  `# pragma: no cover`, so the reported coverage says nothing about
  them.
- **No layer isolation** — an integration test failure does not
  pinpoint whether the route, the service, or the database is at
  fault.

`unittest.mock.AsyncMock` with `spec=AsyncSession` produces a mock
whose async methods (`commit`, `refresh`, `execute`, `delete`) are
awaitable and whose sync methods (`add`) are not, matching the real
`AsyncSession` interface. Route functions are plain `async def`
callables and can be invoked directly with their dependencies passed
as arguments, bypassing FastAPI's dependency injection.

## Alternatives Considered

- **Keep integration-only (ADR-0007)** — the error paths stay
  untested and excluded from coverage. Simulating database failures
  against SQLite (corrupting the file, revoking permissions) is
  fragile and platform-dependent.
- **Fault injection via dependency overrides** — override
  `generate_async_session` in `TestClient` with a session that raises
  on `commit`. This covers the error paths through HTTP but couples
  the tests to the full stack anyway and still offers no layer
  isolation.
- **Replace integration tests with unit tests** — fast and isolated,
  but mocks can silently diverge from real behavior; ADR-0007's
  argument for exercising the real database still holds for the happy
  paths and the HTTP contract.

## Decision

We will maintain two test tiers:

- **Integration tests** in `tests/` (`test_main.py`,
  `test_migrations.py`) remain the authority for the API contract:
  status codes, headers, response shapes, and real database
  behavior. No mocking.
- **Unit tests** in `tests/unit/` test the route and service layers in
  isolation. Service tests mock `AsyncSession`
  (`AsyncMock(spec=AsyncSession)`); route tests mock the
  `player_service` functions and the cache. Unit tests do not apply
  Alembic migrations (`tests/unit/conftest.py` overrides the
  session-scoped `apply_migrations` fixture).

Naming conventions:

- Route unit tests follow the integration pattern
  `test_request_{method}_{resource}_{context}_response_{outcome}`,
  since they verify the same HTTP-level outcomes.
- Service unit tests use `test_{function}_{context}_returns_{outcome}`
  (e.g. `test_create_async_commit_error_returns_none`), since there is
  no HTTP request involved.

Error branches covered by unit tests must not carry
`# pragma: no cover`; the marker is reserved for code that no test
tier can reach.

This keeps the integration suite as the source of truth for
observable behavior while giving the error paths real, counted
coverage.

## Consequences

**Positive:**

- Error-handling paths (rollback on `SQLAlchemyError`, HTTP 500
  responses) are exercised and counted in coverage.
- Unit test failures pinpoint the failing layer.
- Unit tests need no database or migrations and run fast.

**Negative:**

- Mocks encode assumptions about `AsyncSession` and the service API;
  if either changes, unit tests may keep passing while integration
  tests fail, or the reverse. Both tiers must be updated together.
- Two naming conventions and two fixture setups to maintain.
- Route unit tests call route functions directly, so they do not
  verify FastAPI wiring (path parameters, dependency injection,
  response model serialization). That remains the integration suite's
  job.
