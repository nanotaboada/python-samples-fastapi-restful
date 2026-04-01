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
