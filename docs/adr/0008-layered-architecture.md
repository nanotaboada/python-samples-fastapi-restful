# ADR-0008: Layered Architecture with FastAPI Dependency Injection

Date: 2026-04-02

## Status

Accepted

## Context

Python and FastAPI impose no project structure. The common alternatives
for a single-domain REST API are:

- **Flat structure**: all application code in one or a few modules at the
  root. Simplest to start, but HTTP handling, business logic, ORM queries,
  and Pydantic models quickly intermingle, making the code hard to test
  or reason about in isolation.
- **Repository pattern**: a dedicated repository layer between the service
  and the ORM. Common in Java/Spring Boot; adds a class hierarchy and
  interface contracts that duplicate what SQLAlchemy already provides for
  a CRUD project.
- **Hexagonal / clean architecture**: ports and adapters with abstract
  interfaces for every external dependency. Maximum decoupling, but
  significant boilerplate for a single-domain PoC.
- **Layered architecture with FastAPI's native DI**: three functional
  layers (routes, services, database) with FastAPI's `Depends()` mechanism
  for async session injection. No custom DI container; the framework
  handles construction and lifecycle of session objects.

An additional constraint: SQLAlchemy ORM models (the database schema) and
Pydantic models (the API contract) serve different purposes and must be
kept separate to avoid coupling the wire format to the storage schema.

## Decision

We will use a three-layer architecture where each layer has a single,
explicit responsibility, and async SQLAlchemy sessions are injected via
FastAPI's `Depends()` mechanism.

```text
routes/ → services/ → schemas/ (SQLAlchemy) → SQLite via aiosqlite
```

- **`routes/`** (HTTP layer): FastAPI `APIRouter` definitions. Each route
  function handles HTTP concerns only — parameter extraction, status codes,
  and dispatching to a service function. Routes receive an `AsyncSession`
  via `Annotated[AsyncSession, Depends(generate_async_session)]`; session
  management (commit, rollback, close) is handled inside the service or
  via the session context manager.
- **`services/`** (business layer): module-level async functions, not
  classes. Each function accepts an `AsyncSession` as its first parameter
  and owns all business logic — existence checks, conflict detection,
  cache management, and ORM interactions. Services have no knowledge of
  HTTP types.
- **`schemas/`** (data layer): SQLAlchemy 2.0 `DeclarativeBase` models
  that define the database schema. These are never serialised directly
  to API responses.
- **`models/`**: Pydantic models (`PlayerRequestModel`,
  `PlayerResponseModel`) for request validation and response serialisation.
  Kept strictly separate from the ORM schema to avoid coupling the API
  contract to storage column names or types.
- **`databases/`**: async session factory (`generate_async_session`) used
  as the `Depends()` target. The engine and session configuration live here
  and nowhere else.

Services are implemented as plain functions (not classes with injected
interfaces) because FastAPI's `Depends()` already provides lifecycle
management for the session, and functional composition is idiomatic in
Python for stateless service logic.

## Consequences

**Positive:**
- Each layer has a single, testable responsibility. Route tests via
  `TestClient` exercise the full stack; session injection is transparent.
- FastAPI handles session construction, teardown, and error propagation
  through `Depends()` — no composition root or manual wiring is required.
- The ORM/Pydantic split prevents accidental leakage of column names or
  ORM-specific types into the API contract.
- The functional service style is idiomatic Python: functions are easy to
  call directly in tests without instantiating a class.

**Negative:**
- Service functions cannot be replaced with test doubles via interface
  injection — there are no interface contracts. Testing error branches
  requires either fault injection at the database level or patching with
  `unittest.mock`.
- The `AsyncSession` parameter must be threaded through every service
  function call; adding a new database operation always requires touching
  the route signature and the service signature together.
- Contributors familiar with class-based service layers (Spring Boot,
  ASP.NET Core, Gin) may expect a similar structure; the functional
  approach deviates from the pattern used in the other repos in this
  comparison.
