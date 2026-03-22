# ADR-0005: Full Replace PUT, No PATCH

Date: 2026-03-21

## Status

Accepted. Partial update support via PATCH is under consideration —
tracked in issue #461.

## Context

HTTP defines two semantics for updating a resource:

- **PUT** — full replacement; the request body represents the complete
  new state of the resource. Fields absent from the body are
  overwritten with their zero/null values.
- **PATCH** — partial update; the request body contains only the fields
  to change. Requires a patch format (JSON Merge Patch, JSON Patch) or
  a convention for interpreting absent fields.

Both are common in REST APIs. The choice affects the Pydantic model
design (all fields required vs optional), the service layer logic
(overwrite all vs merge), and the client contract (must send all fields
vs only changed fields).

The current implementation uses a single `PlayerRequestModel` where all
domain fields are required. The service's
`update_by_squad_number_async` overwrites every field on the existing
record using the request body values.

## Decision

We will implement PUT as a full replacement operation only, with no
PATCH endpoint.

Full replace is simpler to implement correctly: no merge logic, no
ambiguity about what an absent field means, and a single request model
covers both POST and PUT. For a PoC with a small, flat domain model
(10 fields), requiring the full resource on update is not a meaningful
burden for clients.

## Consequences

**Positive:**
- Simple, unambiguous semantics: the request body is the new state.
- No additional Pydantic model or merge logic required.
- No need to decide on a patch format (JSON Merge Patch vs JSON Patch).

**Negative:**
- Clients must send the full resource even to change a single field,
  which is verbose and risks accidental data loss if a field is omitted.
- Not suitable for resources with many fields, binary data, or
  frequently partial updates.
- Issue #461 tracks the addition of PATCH for partial updates, which
  would require an optional-fields model and merge logic in the service
  layer.
