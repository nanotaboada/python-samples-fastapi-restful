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

### Changed

### Fixed

### Removed

---

## [1.0.0 - Ancelotti] - TBD

### Added

- Initial stable release
- Player CRUD operations with FastAPI
- SQLite database with SQLAlchemy (async)
- Docker support with Docker Compose
- In-memory caching with aiocache (10 min TTL)
- Comprehensive pytest test suite with coverage reporting
- Health check endpoint
- CI/CD pipeline with tag-based releases
- Famous coaches release naming convention ♟️

### Changed

- N/A

### Fixed

- N/A

### Removed

- N/A

---

## How to Release

1. Update this CHANGELOG.md with the new version details
2. Create a tag with the format `v{MAJOR}.{MINOR}.{PATCH}-{COACH}`
3. Push the tag to trigger the CD pipeline

```bash
# Example: Creating the first release (Ancelotti)
git tag -a v1.0.0-ancelotti -m "Release 1.0.0 - Ancelotti"
git push origin v1.0.0-ancelotti
```

The CD pipeline will automatically:

- Run tests and generate coverage reports
- Build and push Docker images with multiple tags (`:1.0.0`, `:ancelotti`, `:latest`)
- Generate a changelog from git commits
- Create a GitHub Release with auto-generated notes

## Version History

<!--
Add release summaries here as they are published:

### [1.0.0 - Ancelotti] (2026-XX-XX)
- Initial stable release with core functionality
-->
