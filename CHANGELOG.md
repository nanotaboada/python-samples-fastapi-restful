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

- UUID v4 primary key for the `players` table, replacing the previous integer PK (#66)
- `PlayerRequestModel` Pydantic model for POST/PUT request bodies (no `id` field) (#66)
- `PlayerResponseModel` Pydantic model for GET/POST response bodies (includes `id: UUID`) (#66)
- `tools/seed_001_starting_eleven.py`: standalone seed script populating 11 starting-eleven players with deterministic UUID v5 PKs (#66)
- `tools/seed_002_substitutes.py`: standalone seed script populating 14 substitute players with deterministic UUID v5 PKs (#66)
- `HyphenatedUUID` custom `TypeDecorator` in `schemas/player_schema.py` storing UUIDs as hyphenated `CHAR(36)` strings in SQLite, returning `uuid.UUID` objects in Python (#66)

### Changed

- `PlayerModel` split into `PlayerRequestModel` and `PlayerResponseModel` in `models/player_model.py` (#66)
- All route path parameters and service function signatures updated from `int` to `uuid.UUID` (#66)
- POST conflict detection changed from ID lookup to `squad_number` uniqueness check (#66)
- `tests/player_stub.py` updated with UUID-based test fixtures (#66)
- `tests/test_main.py` updated to assert UUID presence and format in API responses (#66)
- `PlayerResponseModel` redeclared with `id` as first field to control JSON serialization order (#66)
- `HyphenatedUUID` methods now have full type annotations and Google-style docstrings; unused `dialect` params renamed to `_dialect` (#66)
- Service logger changed from `getLogger("uvicorn")` to `getLogger("uvicorn.error")`, aligned with `main.py` (#66)
- `logger.error(f"...")` replaced with `logger.exception("...: %s", error)` in all `SQLAlchemyError` handlers (#66)
- EN dashes replaced with ASCII hyphens in `seed_002` log and argparse strings (#66)
- `logger.error` replaced with `logger.exception` in `sqlite3.Error` handlers in `seed_001` and `seed_002` (#66)

### Deprecated

### Removed

### Fixed

- POST/PUT/DELETE routes now raise `HTTP 500` on DB failure instead of silently returning success (#66)
- Cache cleared only after confirmed successful create, update, or delete (#66)
- DELETE test is now self-contained; no longer depends on POST test having run first (#66)
- UUID assertion in GET all test replaced with explicit `_is_valid_uuid()` validator (#66)
- Emiliano Martínez `middleName` corrected from `""` to `None` in `seed_001` (#66)

### Security

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

[unreleased]: https://github.com/nanotaboada/python-samples-fastapi-restful/compare/v1.0.0-ancelotti...HEAD
[1.0.0 - Ancelotti]: https://github.com/nanotaboada/python-samples-fastapi-restful/releases/tag/v1.0.0-ancelotti
