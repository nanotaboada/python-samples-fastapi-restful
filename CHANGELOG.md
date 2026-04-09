# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Release Naming Convention ♟️

This project uses famous football coaches as release codenames, following an A-Z naming pattern.

| Letter | Coach Name | Country/Notable Era | Tag Name |
|--------|-----------|---------------------|----------|
| A | Ancelotti (Carlo) | Italy | `ancelotti` |
| B | Bielsa (Marcelo) | Argentina | `bielsa` |
| C | Capello (Fabio) | Italy | `capello` |
| D | Del Bosque (Vicente) | Spain | `delbosque` |
| E | Eriksson (Sven-Göran) | Sweden | `eriksson` |
| F | Ferguson (Alex) | Scotland | `ferguson` |
| G | Guardiola (Pep) | Spain | `guardiola` |
| H | Heynckes (Jupp) | Germany | `heynckes` |
| I | Inzaghi (Simone) | Italy | `inzaghi` |
| J | Klopp (Jürgen) | Germany | `klopp` |
| K | Kovač (Niko) | Croatia | `kovac` |
| L | Löw (Joachim) | Germany | `low` |
| M | Mourinho (José) | Portugal | `mourinho` |
| N | Nagelsmann (Julian) | Germany | `nagelsmann` |
| O | Ottmar Hitzfeld | Germany/Switzerland | `ottmar` |
| P | Pochettino (Mauricio) | Argentina | `pochettino` |
| Q | Queiroz (Carlos) | Portugal | `queiroz` |
| R | Ranieri (Claudio) | Italy | `ranieri` |
| S | Simeone (Diego) | Argentina | `simeone` |
| T | Tuchel (Thomas) | Germany | `tuchel` |
| U | Unai Emery | Spain | `unai` |
| V | Van Gaal (Louis) | Netherlands | `vangaal` |
| W | Wenger (Arsène) | France | `wenger` |
| X | Xavi Hernández | Spain | `xavi` |
| Y | Yozhef Sabo | Ukraine | `yozhef` |
| Z | Zeman (Zdeněk) | Czech Republic | `zeman` |

---

## [Unreleased]

### Added

- `alembic/`: Alembic migration support for async SQLAlchemy — `env.py`
  configured for async execution with `render_as_batch=True` (SQLite/PostgreSQL
  compatible); three migrations: `001` creates the `players` table, `002` seeds
  11 Starting XI players, `003` seeds 15 Substitute players (all with
  deterministic UUID v5 values); `alembic upgrade head` applied by
  `entrypoint.sh` (Docker) or manually for local development (#2)
- `alembic==1.18.4`, `asyncpg==0.31.0` added to dependencies (#2)
- `tests/test_migrations.py`: integration tests for migration downgrade paths —
  verifies each step removes only its seeded rows and restores correctly (#2)
- `codecov.yaml`: excludes `alembic/env.py` from coverage (offline mode is
  tooling infrastructure, not application logic) (#2)
- `.sonarcloud.properties`: SonarCloud Automatic Analysis configuration —
  sources, tests, coverage exclusions aligned with `codecov.yml` (#554)
- `.dockerignore`: added `.claude/`, `CLAUDE.md`, `.coderabbit.yaml`,
  `.sonarcloud.properties`, `CHANGELOG.md`, `README.md` (#554)
- CD workflow now verifies tag commit is reachable from `master` before
  proceeding with build and publish steps (#549)

### Changed

- `databases/player_database.py`: extracted `get_database_url()` helper
  (reads `DATABASE_URL`, falls back to `STORAGE_PATH`, SQLite default);
  `connect_args` made conditional on SQLite dialect (#2)
- `alembic/env.py`: removed duplicated DATABASE_URL construction; now calls
  `get_database_url()` from `databases.player_database` (#2)
- `main.py`: removed `_apply_migrations` from lifespan — migrations are a
  one-shot step, not a per-process startup concern; lifespan now logs startup
  only (#2)
- `Dockerfile`: removed `COPY storage/ ./hold/` and its associated comment;
  added `COPY alembic.ini` and `COPY alembic/` (#2)
- `scripts/entrypoint.sh`: runs `alembic upgrade head` before launching the
  app; replaces hold→volume copy and manual seed script pattern (#2)
- `compose.yaml`: replaced `STORAGE_PATH` with `DATABASE_URL` pointing to the
  SQLite volume path (#2)
- `.gitignore`: added `*.db`; `storage/players-sqlite3.db` removed from git
  tracking; `storage/` directory deleted (#2)
- `tests/player_stub.py` renamed to `tests/player_fake.py`; class docstring
  updated to reflect fake (not stub) role; module-level docstring added
  documenting the three-term data-state vocabulary (`existing`, `nonexistent`,
  `unknown`); imports in `conftest.py` and `test_main.py` updated accordingly;
  `test_request_get_player_id_nonexistent_response_status_not_found` renamed to
  `test_request_get_player_id_unknown_response_status_not_found` (#559)
- `GET /players/` cache check changed from `if not players` to
  `if players is None` so that an empty collection is cached correctly
  instead of triggering a DB fetch on every request (#530)
- `POST /players/` 409 response now includes a human-readable `detail`
  message: "A Player with this squad number already exists." (#530)

### Fixed

- `POST /players/` 201 response now includes a `Location` header
  pointing to the created resource at
  `/players/squadnumber/{squad_number}` per RFC 7231 §7.1.2 (#530)

### Removed

---

## [2.1.0 - Del Bosque] - 2026-03-31

### Added

- Architecture Decision Records (ADRs) in `docs/adr/` documenting key
  decisions: SQLite, no Alembic, UUID primary key, squad number as
  mutation key, full replace PUT, in-memory caching, integration-only
  tests (#482)

### Changed

- Normalize player dataset: add Lo Celso (squad 27) as test fixture,
  add Almada (squad 16) as seeded substitute, correct
  Martínez/Fernández/Mac Allister/Messi field values, replace
  pre-computed UUIDs with canonical UUID v5 values (namespace
  `FIFA_WORLD_CUP_QATAR_2022_ARGENTINA_SQUAD`); bundled
  `storage/players-sqlite3.db` rebuilt from seed scripts — Docker
  deployments with a persisted volume will continue to use the old
  database until the volume is recreated (`docker compose down -v &&
  docker compose up --build`) (#543)
- Align CRUD test fixtures: Lo Celso (squad 27) for Create and Delete,
  Messi (squad 10) for Retrieve, Damián Martínez (squad 23) for Update
  (#543)

---

## [2.0.0 - Capello] - 2026-03-17

### Changed

- **BREAKING**: `PUT /players/{player_id}` replaced by `PUT /players/squadnumber/{squad_number}` — mutation endpoints now use Squad Number (natural key) instead of UUID (surrogate key), consistent with `GET /players/squadnumber/{squad_number}` (#521)
- **BREAKING**: `DELETE /players/{player_id}` replaced by `DELETE /players/squadnumber/{squad_number}` — same rationale as above (#521)
- `update_async` and `delete_async` (UUID-based) replaced by `update_by_squad_number_async` and `delete_by_squad_number_async` in `services/player_service.py` (#521)

### Fixed

- Removed stale `assets/` folder references from `Dockerfile`,
  `codecov.yml`, and `.coderabbit.yaml` after the folder was deleted
  when the README was migrated to Mermaid diagrams

---

## [1.1.0 - Bielsa] - 2026-03-02

### Added

- `rest/players.rest` file covering all CRUD operations, compatible with the VS Code REST Client extension (#493)
- `humao.rest-client` added to `.vscode/extensions.json` recommendations (#493)
- UUID v4 primary key for the `players` table, replacing the previous integer PK (#66)
- `PlayerRequestModel` Pydantic model for POST/PUT request bodies (no `id` field) (#66)
- `PlayerResponseModel` Pydantic model for GET/POST response bodies (includes `id: UUID`) (#66)
- `tools/seed_001_starting_eleven.py`: standalone seed script populating 11 starting-eleven players with deterministic UUID v5 PKs (#66)
- `tools/seed_002_substitutes.py`: standalone seed script populating 14 substitute players with deterministic UUID v5 PKs (#66)

### Changed

- `PlayerModel` split into `PlayerRequestModel` and `PlayerResponseModel` in `models/player_model.py` (#66)
- All route path parameters and service function signatures updated from `int` to `uuid.UUID` (#66)
- POST conflict detection changed from ID lookup to `squad_number` uniqueness check (#66)
- `pyproject.toml` migrated to full PEP 735 format: `[project]` (with `dependencies` field) and `[dependency-groups]` (`test`, `lint`, `dev`) (#447)
- GitHub Actions CI/CD (`python-ci.yml`, `python-cd.yml`) updated to install and run via `uv` instead of `pip` (#447)
- Dockerfile updated: builder stage uses `uv export | pip wheel` for reproducible offline wheel builds; runtime installs from pre-built wheels with no network access (#447)
- `uv.lock` added for fully pinned, reproducible dependency resolution across all environments (#447)

### Removed

- `postman_collections/` directory replaced by `rest/players.rest` (#493)
- `requirements.txt`, `requirements-lint.txt`, `requirements-test.txt` replaced by `pyproject.toml` with PEP 735 dependency groups (#447)

### Fixed

- POST/PUT/DELETE routes now raise `HTTP 500` on DB failure instead of silently returning success (#66)
- Cache cleared only after confirmed successful create, update, or delete (#66)

---

## [1.0.0 - Ancelotti] - 2026-01-24

Initial release. See [README.md](README.md) for complete feature list and documentation.

---

## How to Release

To create a new release, follow these steps in order:

### 1. Update CHANGELOG.md

Move items from the `[Unreleased]` section to a new release section using the template format provided at the bottom of this file (see the commented template).

**Important:** Commit and push this change before creating the tag.

### 2. Create and Push Version Tag

```bash
git tag -a vX.Y.Z-coach -m "Release X.Y.Z - Coach"
git push origin vX.Y.Z-coach
```

Example:

```bash
git tag -a v1.0.0-ancelotti -m "Release 1.0.0 - Ancelotti"
git push origin v1.0.0-ancelotti
```

### 3. Automated CD Workflow

The CD workflow automatically:

- ✅ Validates the coach name against the A-Z list
- ✅ Builds and tests the project with coverage
- ✅ Publishes Docker images to GHCR with three tags (`:X.Y.Z`, `:coach`, `:latest`)
- ✅ Creates a GitHub Release with auto-generated notes from commits

### Pre-Release Checklist

- [ ] CHANGELOG.md updated with release notes
- [ ] CHANGELOG.md changes committed and pushed
- [ ] Tag created with correct format: `vX.Y.Z-coach`
- [ ] Coach name is valid (A-Z from table above)
- [ ] Tag pushed to trigger CD workflow

<!-- Template for new releases:

## [X.Y.Z - COACH_NAME] - YYYY-MM-DD

### Added
- New features

### Changed
- Changes in existing functionality

### Deprecated
- Soon-to-be removed features

### Removed
- Removed features

### Fixed
- Bug fixes

### Security
- Security vulnerability fixes

-->

---

[unreleased]: https://github.com/nanotaboada/python-samples-fastapi-restful/compare/v2.0.0-capello...HEAD
[2.0.0 - Capello]: https://github.com/nanotaboada/python-samples-fastapi-restful/compare/v1.1.0-bielsa...v2.0.0-capello
[1.1.0 - Bielsa]: https://github.com/nanotaboada/python-samples-fastapi-restful/compare/v1.0.0-ancelotti...v1.1.0-bielsa
[1.0.0 - Ancelotti]: https://github.com/nanotaboada/python-samples-fastapi-restful/releases/tag/v1.0.0-ancelotti
