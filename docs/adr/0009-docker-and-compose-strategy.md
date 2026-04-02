# ADR-0009: Docker and Compose Strategy

Date: 2026-04-02

## Status

Accepted

## Context

The project needs to run in a self-contained environment for demos, CI,
and as a reference point in the cross-language comparison. Two concerns
apply:

1. **Image size and security**: a naive build installs all dependencies
   including C build tools (required for native extensions such as
   `greenlet` and `aiosqlite`) into the final image, increasing its
   size and attack surface.
2. **Local orchestration**: contributors should be able to start the
   application with a single command, without installing Python or `uv`,
   configuring environment variables, or managing a database file manually.

Dependency resolution strategies considered:

- **Single-stage build with pip**: simplest, but requires `build-essential`,
  `gcc`, `libffi-dev`, and `libssl-dev` in the final image to compile
  native extensions at install time.
- **Multi-stage with virtualenv**: builder creates a `.venv`; runtime
  copies it. Works for pure-Python projects but is fragile when native
  extensions reference absolute paths baked in during compilation.
- **Multi-stage with pre-built wheels**: builder resolves dependencies via
  `uv export` and pre-compiles them into `.whl` files (`pip wheel`);
  runtime installs from the local wheelhouse with `--no-index`. Build
  tools stay in the builder stage; the final image needs only `pip install`.

## Decision

We will use a multi-stage Docker build where the builder stage pre-compiles
all dependency wheels, and Docker Compose to orchestrate the application
locally.

- **Builder stage** (`python:3.13.3-slim-bookworm`): installs
  `build-essential`, `gcc`, `libffi-dev`, and `libssl-dev`; uses
  `uv export --frozen --no-dev --no-hashes` to produce a pinned,
  reproducible dependency list from `uv.lock`, then compiles every
  package into a `.whl` file via `pip wheel`. The wheelhouse is written
  to `/app/wheelhouse/`.
- **Runtime stage** (`python:3.13.3-slim-bookworm`): installs `curl` only
  (for the health check); copies the pre-built wheels from the builder;
  installs them with `--no-index --find-links` (no network access, no
  build tools required); removes the wheelhouse after installation.
- **Entrypoint script**: on first start, copies the pre-seeded database
  from the image's read-only `hold/` directory to the writable named
  volume at `/storage/`, then runs both seed scripts to ensure the schema
  and data are up to date. On subsequent starts, the volume file is
  preserved and seed scripts run again (they are idempotent).
- **Compose (`compose.yaml`)**: defines a single service with port
  mapping (`9000`), a named volume (`storage`), and environment variables
  (`STORAGE_PATH`, `PYTHONUNBUFFERED=1`). Health checks are declared in
  the Dockerfile (`GET /health`); Compose relies on that declaration.
- A non-root `fastapi` user is created in the runtime stage following the
  principle of least privilege.

## Consequences

**Positive:**
- Build tools (`gcc`, `libffi-dev`) are confined to the builder stage and
  never reach the runtime image — smaller attack surface and faster pulls.
- Offline installation (`--no-index`) eliminates network-related
  non-determinism during the runtime image build.
- `uv.lock` pins every transitive dependency; the builder produces the
  same wheels regardless of upstream index state.
- `docker compose up` is a complete local setup with no prerequisites
  beyond Docker.
- The named volume preserves data across restarts; `docker compose down -v`
  resets it cleanly.

**Negative:**
- Multi-stage builds are more complex to read and maintain than
  single-stage builds.
- The wheelhouse is an intermediate artifact: if a wheel cannot be
  pre-built (e.g. binary-only distributions without a source distribution),
  the builder stage will fail.
- The seed scripts run on every container start. They are idempotent but
  add latency to startup and must remain so as the project evolves.
- The SQLite database file is versioned and bundled, meaning schema changes
  require a Docker image rebuild.

**When to revisit:**

- If a dependency ships only as a binary wheel for the target platform,
  the `pip wheel` step may need to be replaced with a direct `pip install`
  in the builder stage.
- If a second service (e.g. PostgreSQL) is added, Compose will need a
  dedicated network and dependency ordering.
