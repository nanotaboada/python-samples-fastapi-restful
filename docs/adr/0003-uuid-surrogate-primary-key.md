# ADR-0003: UUID Surrogate Primary Key with v4/v5 Split

Date: 2026-03-21

## Status

Accepted

## Context

A primary key strategy was required for the `players` table. The
candidates considered were:

- **Auto-increment integer** — simple, compact, sequential; but leaks
  row count and insertion order to clients, and integer IDs are
  predictable, which can be a security concern for resource enumeration.
- **UUID v4** — randomly generated, opaque, non-sequential; no
  information leaked; standard for API-created resources.
- **UUID v7 / ULID** — time-ordered UUIDs; better index locality than
  v4 but add a dependency and are less universally supported.
- **Natural key (`squad_number`)** — human-readable, but not stable
  across squads or seasons; unsuitable as a surrogate.

An additional constraint was seeded data: the project ships 26
pre-seeded players that must have stable, reproducible primary keys
across environments so that tests can reference them by ID.

UUID v4 (random) cannot satisfy this: regenerating the seed would
produce different IDs each time. UUID v5 (deterministic, derived from
a namespace and a name) produces the same UUID for the same input,
making seeded records reproducible.

## Decision

We will use a UUID surrogate primary key stored as a hyphenated string
(`HyphenatedUUID` custom SQLAlchemy type). API-created records receive
a UUID v4 (random); migration-seeded records receive a UUID v5
(deterministic, derived from the player's squad number).

The v4/v5 split preserves the benefits of each approach in its context:
randomness for API-created records (opaque, non-predictable), and
determinism for seeded records (stable across environments, safe for
test fixtures).

The UUID is intentionally opaque to external clients. It is exposed
only via `GET /players/{player_id}` and `POST /players/` responses.
All mutation endpoints (PUT, DELETE) use `squad_number` as the
identifier — see ADR-0004.

## Consequences

**Positive:**
- UUIDs are opaque; no information about row count or insertion order
  is exposed to clients.
- The v5/v4 split means seeded records have stable IDs across
  environments, safe to hard-code in tests.
- `HyphenatedUUID` stores IDs as standard hyphenated strings in SQLite,
  readable without special tooling.

**Negative:**
- UUIDs are larger than integers (36 chars as strings), which has a
  minor storage and index performance cost — acceptable at PoC scale.
- The v4/v5 distinction is non-obvious; developers unfamiliar with the
  codebase may not know why seeded records have deterministic IDs.
- Clients cannot use the UUID to infer insertion order or paginate
  reliably by ID (UUID v4 is random).
