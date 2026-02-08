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

### Deprecated

### Removed

### Fixed

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
