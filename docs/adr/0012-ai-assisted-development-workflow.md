# ADR-0012: Adopt AI-Assisted Development Workflow

Date: 2026-06-10

## Status

Accepted

## Context

Software development has historically relied on three successive layers
of knowledge:

1. **Official documentation** — authoritative but static; describes the
   intended API but not how real projects apply it
2. **Community collaboration** — Stack Overflow, GitHub Discussions, blog
   posts; describes how practitioners actually solve problems, but requires
   the developer to synthesize and apply that knowledge themselves
3. **AI synthesis** — models trained on both layers above, capable of
   applying idiomatic, stack-specific knowledge directly to a given
   codebase

Agentic AI tools represent a qualitative shift: instead of consulting
knowledge and applying it manually, the developer delegates implementation
to an agent that has absorbed the collective idioms of a stack — "the
Microsoft way", "the FastAPI way" — and can apply them consistently.

For a cross-language REST API comparison project, this matters
particularly: each implementation should reflect how an experienced
practitioner in that stack would structure the same problem, not a
generic approach that happens to compile.

Prior to Claude Code, AI assistance was used ad-hoc — pasting code into
web interfaces (ChatGPT, DeepSeek) or via IDE-integrated assistants
(GitHub Copilot). Both approaches lack persistent codebase context and
the ability to act autonomously across a project.

## Decision

We adopt Claude Code as the primary development workflow tool for this
project.

A `CLAUDE.md` file at the repository root serves as the workflow
specification: it documents architecture, coding conventions, invariants,
and explicit boundaries for autonomous operation — what the agent may do
freely, what requires human approval, and what must never be changed.

CodeRabbit provides an additional automated code review layer
independent of the primary workflow.

## Consequences

**Positive:**

- Stack-specific idioms are enforced by the agent's collective knowledge
  rather than individual developer discipline
- `CLAUDE.md` is living architectural documentation: it must stay
  accurate for the workflow to function, creating a natural incentive to
  keep it current
- Explicit autonomy boundaries make human oversight intentional rather
  than incidental

**Negative:**

- Token economics: long-running work may exceed context limits, requiring
  active session management and continuation prompts to resume work
  across sessions
- The global `~/.claude/CLAUDE.md` and per-repo `CLAUDE.md` must stay
  aligned; drift between them produces inconsistent agent behavior

**Neutral:**

- Development workflow moves to the terminal/CLI rather than an IDE;
  this has no impact on the codebase itself
- `CLAUDE.md` is specific to Claude Code; a different tool would require
  a different workflow specification format
