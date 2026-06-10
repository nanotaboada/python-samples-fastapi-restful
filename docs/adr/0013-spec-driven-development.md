# ADR-0013: Adopt Spec-Driven Development (SDD)

Date: 2026-06-10

## Status

Accepted

## Context

In an agentic development workflow, it is easy to begin implementation
before requirements are fully understood. An AI assistant will produce
working code from a vague prompt — but working and correct are not the
same thing. Without a forcing function that requires requirements to be
stated explicitly before implementation begins, scope creep, rework, and
misaligned implementations are likely outcomes.

GitHub Issues provide a natural spec artifact: persistent, linkable,
and — critically — they survive session boundaries. In a workflow where
context is lost between sessions, an Issue that captures the agreed
approach and acceptance criteria before implementation begins serves as
the durable contract between intent and implementation.

## Decision

All new features and non-trivial changes follow a three-step workflow:

1. **Discuss** — describe the requirement in Claude Code Plan mode;
   explore alternatives and consequences before committing to an approach
2. **Specify** — create a GitHub Issue as the spec artifact, capturing
   the agreed approach, acceptance criteria, and any constraints
3. **Implement** — work against the Issue; commits reference it via
   the `(#issue)` suffix in the Conventional Commits format

Trivial changes (documentation updates, formatting fixes, dependency
bumps) may skip the Issue step at the developer's discretion.

## Consequences

**Positive:**

- Requirements are stated explicitly before implementation; the agent
  works against a written spec rather than an interpreted prompt
- Issues survive session boundaries — a new session can resume from
  the Issue rather than reconstructing intent from scratch
- The implementation trail (Issue → branch → PR → commit) is traceable
  without relying on session memory

**Negative:**

- Adds upfront overhead for changes that feel small; the Issue step can
  seem bureaucratic for straightforward work
- The line between "spec-worthy" and "trivial" is judgment-dependent
  and not enforced by tooling

**Neutral:**

- GitHub Issues double as the project backlog; SDD and backlog
  management share the same artifact
- Plan mode discussion is ephemeral — not persisted outside the session;
  the Issue is the only durable record of the pre-implementation reasoning
