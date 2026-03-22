# ADR-0007: Integration-Only Test Strategy

Date: 2026-03-21

## Status

Accepted. Unit tests with mocking for the service and route layers are
under consideration — tracked in issue #490.

## Context

The test suite could be structured in several ways:

- **Unit tests with mocks** — each layer (routes, services) is tested
  in isolation with its dependencies mocked. Fast, focused, but
  requires maintaining mock objects that can diverge from real
  behaviour.
- **Integration tests against a real database** — tests run against the
  actual application stack, including the SQLite database. Slower per
  test but exercises the full request/response cycle and catches
  interaction bugs that mocks would miss.
- **Mixed** — unit tests for complex business logic, integration tests
  for the HTTP layer.

The project uses a pre-seeded SQLite database file committed to the
repository. FastAPI's `TestClient` (backed by `httpx`) allows
synchronous integration tests that exercise the full stack — routing,
dependency injection, service logic, ORM queries, and the database —
without a running server process.

All tests live in a single test module under `tests/`, use a stubs
module for consistent test data, and rely on a `function`-scoped
`client` fixture in `conftest.py` for per-test isolation.

## Decision

We will use integration tests only, exercising the full stack via
`TestClient` against the real pre-seeded SQLite database. No mocking.

For a thin CRUD API where the business logic is primarily data
transformation and persistence, integration tests provide the highest
confidence per line of test code. The pre-seeded SQLite database is
fast enough for a small dataset, and `TestClient` makes the tests
synchronous and straightforward to write. Mocks would require
maintaining fake implementations of the service and ORM layers that
could silently diverge from reality.

## Consequences

**Positive:**
- Tests exercise the full stack; interaction bugs between layers are
  caught.
- No mock infrastructure to maintain; tests remain valid as the
  implementation evolves.
- `TestClient` makes tests synchronous and easy to read despite the
  async application stack.
- 100% coverage is achievable and meaningful — covered lines are
  exercised against a real database.

**Negative:**
- Tests depend on the state of the pre-seeded database; a corrupted or
  out-of-date database file breaks the suite.
- No isolation between application layers in tests; a failure does not
  pinpoint which layer is responsible without further investigation.
- As business logic grows more complex, the absence of unit tests for
  the service layer becomes a gap. Issue #490 tracks the addition of
  unit tests with mocking for service and route layers.
