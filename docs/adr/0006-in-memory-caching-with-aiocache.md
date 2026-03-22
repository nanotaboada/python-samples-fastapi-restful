# ADR-0006: In-Memory Caching with aiocache

Date: 2026-03-21

## Status

Accepted

## Context

The `GET /players/` endpoint retrieves all players on every request.
With a fixed dataset and no real-time update requirements, repeated
database reads for the same data are unnecessary. The caching
strategies considered were:

- **No cache** — simplest; every request hits the database. Acceptable
  for a PoC but leaves an obvious optimization undemonstrated.
- **HTTP cache headers** (`Cache-Control`, `ETag`, `Last-Modified`) —
  standard HTTP caching; delegates caching to the client or a reverse
  proxy. Requires no server-side storage but adds response header logic
  and shifts responsibility to the client.
- **In-process memory cache** — stores serialized results in the server
  process memory; fast, zero infrastructure, invalidated explicitly on
  write operations.
- **Distributed cache (Redis, Memcached)** — shares cache across
  multiple server instances; requires additional infrastructure and a
  client library.

The project is a single-instance PoC with no horizontal scaling
requirement. The dataset is small (26 players) and changes only via the
API, making explicit cache invalidation straightforward.

## Decision

We will use `aiocache` with `SimpleMemoryCache` for in-process caching
of the `GET /players/` response, with a 10-minute TTL and explicit
cache invalidation on POST, PUT, and DELETE.

`aiocache` is async-native and integrates cleanly with the FastAPI/
async stack. `SimpleMemoryCache` requires no external service. The
single cache key (`"players"`) is sufficient for a flat collection
endpoint with no filtering or pagination. The `X-Cache: HIT/MISS`
response header makes cache behaviour observable to clients and
useful for testing.

## Consequences

**Positive:**
- Zero infrastructure: no Redis or Memcached service required.
- Async-native: no blocking I/O in the cache layer.
- Explicit invalidation on writes keeps cache consistency simple and
  predictable.
- `X-Cache` header makes cache behaviour transparent and testable.

**Negative:**
- In-process cache is not shared across multiple instances. A
  horizontal scaling deployment would serve stale data from some
  instances until their TTL expires or a write invalidates their local
  cache.
- Cache is lost on process restart; the first request after restart
  always hits the database.
- Only `GET /players/` (the full collection) is cached. Individual
  player lookups (`GET /players/{id}`,
  `GET /players/squadnumber/{n}`) are not cached.
