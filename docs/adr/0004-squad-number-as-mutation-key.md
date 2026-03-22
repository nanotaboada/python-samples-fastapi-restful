# ADR-0004: Squad Number as the Mutation Key

Date: 2026-03-21

## Status

Accepted

## Context

The API exposes two identifiers for a player:

- **UUID** (`id`) — surrogate key; opaque, server-generated, stable.
  See ADR-0003.
- **Squad number** (`squad_number`) — natural key; human-readable,
  domain-meaningful (e.g. number 10 = Messi), unique within a squad.

A design choice was required for which identifier mutation endpoints
(PUT, DELETE) and secondary GET endpoints should use as their path
parameter. The candidates were:

- **UUID for all endpoints** — consistent use of the surrogate key;
  clients must store UUIDs after POST or GET to perform mutations.
- **Squad number for mutations** — uses the natural, human-meaningful
  key for the operations that domain users care about; UUID remains
  available for internal/service-to-service use via
  `GET /players/{player_id}`.

Up to v1.x, the API used UUID for PUT and DELETE. Version 2.0.0
(Capello) changed mutation endpoints to use squad number, introduced
`GET /players/squadnumber/{squad_number}` as a lookup alternative, and
retained `GET /players/{player_id}` for UUID-based lookup.

## Decision

We will use `squad_number` as the path parameter for all mutation
endpoints (`PUT /players/squadnumber/{squad_number}`,
`DELETE /players/squadnumber/{squad_number}`) and for the secondary
GET endpoint (`GET /players/squadnumber/{squad_number}`).

Squad number is the identifier that domain users reason about. Requiring
clients to store and re-use a UUID to update or delete a player they
identified by squad number adds unnecessary indirection. Keeping UUID
lookup available (`GET /players/{player_id}`) preserves
service-to-service use cases where a stable opaque key is preferred.

As a consequence of using squad number on PUT, the request body's
`squad_number` field must match the path parameter. A mismatch returns
HTTP 400; the path parameter is always authoritative.

## Consequences

**Positive:**
- Mutation endpoints are intuitive for domain users:
  `PUT /players/squadnumber/10` clearly targets Messi's record.
- Clients do not need to perform a GET to obtain a UUID before mutating.
- UUID remains available for stable, opaque internal references.

**Negative:**
- Squad numbers can change (a player re-assigned to a different number
  requires a careful update sequence). The API has no special handling
  for squad number changes — it is treated as any other field update.
- Two lookup endpoints (`/players/{id}` and
  `/players/squadnumber/{squad_number}`) increase surface area slightly.
- The mismatch guard on PUT (body squad number must equal path
  parameter) is an additional contract constraint clients must respect.
