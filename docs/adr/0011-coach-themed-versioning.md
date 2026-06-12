# ADR-0011: Use Coach-Themed Semantic Versioning

Date: 2026-06-10

## Status

Accepted

## Context

The project uses Semantic Versioning (MAJOR.MINOR.PATCH). Purely numeric tags
are accurate but forgettable. The project is football-themed and part of a
cross-language comparison set where each repo adopts a different
football-domain naming convention. Several well-known projects use alphabetical
codename conventions (Ubuntu, Android).

This repo uses famous football managers/coaches as codenames. Release tags
follow the format `v{MAJOR}.{MINOR}.{PATCH}-{coach}`, where the coach name is
drawn from the fixed list below, assigned A→Z sequentially:

| Letter | Coach Name | Country/Notable Era | Tag Name |
| ------ | ---------- | ------------------- | -------- |
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

## Decision

Every release tag appends an alphabetically ordered football coach surname to
the Semantic Version. Format: `v{MAJOR}.{MINOR}.{PATCH}-{coach}`. Names are
drawn from the fixed list above, assigned A→Z sequentially. The CD pipeline
validates the coach name against this list before publishing.

## Consequences

**Positive:**

- Release names are memorable and human-friendly.
- Alphabetical ordering provides an implicit sequence visible in `git tag`.
- The naming scheme is deterministic — the next name is always the next letter.
- Reinforces the football theme across the cross-language comparison set.

**Negative:**

- Non-standard tag format; may confuse new contributors unfamiliar with the
  convention.
- The list is finite — 26 slots before the sequence must restart or be
  extended.
- CD validation adds a small amount of pipeline complexity.

**Neutral:**

- The full list is documented in `CLAUDE.md` and `CHANGELOG.md`; the current
  position is always the last released tag.
