# Contributing

Thank you for improving this project! We value small, precise changes that solve real problems.
We value **incremental, detail‑first contributions** over big rewrites or abstractions.

## 1. Philosophy

> "Nobody should start to undertake a large project. You start with a small _trivial_ project, and you should never expect it to get large. If you do, you'll just overdesign and generally think it is more important than it likely is at that stage. Or worse, you might be scared away by the sheer size of the work you envision. So start small, and think about the details. Don't think about some big picture and fancy design. If it doesn't solve some fairly immediate need, it's almost certainly over-designed. And don't expect people to jump in and help you. That's not how these things work. You need to get something half-way _useful_ first, and then others will say "hey, that _almost_ works for me", and they'll get involved in the project." — [Linus Torvalds](https://web.archive.org/web/20050404020308/http://www.linuxtimes.net/modules.php?name=News&file=article&sid=145)

## 2. Code & Commit Conventions

- **Conventional Commits**
  Follow <https://www.conventionalcommits.org/en/v1.0.0/>:
  - `feat: ` for new features
  - `fix: ` for bug fixes
  - `chore: ` for maintenance or tooling
  - `docs: ` for documentation changes
  - `test: ` for test additions or corrections
  - `refactor: ` for code changes that neither fix a bug nor add a feature
  - `ci: ` for CI/CD pipeline changes
  - `perf: ` for performance improvements

- **Logical Commits**
  Group changes by purpose. Multiple commits are fine, but avoid noise. Squash when appropriate.

- **Python Formatting & Style**
  - Use **[Black](https://black.readthedocs.io/)** for consistent code formatting.
    - Black is opinionated: don't argue with it, just run it.
    - Line length is set to **88**, matching the default.
  - Use **[flake8](https://flake8.pycqa.org/en/latest/)** for static checks.
    - Line length also set to 88.
    - Some flake8 warnings are disabled (e.g. `E203`, `W503`) to avoid conflicts with Black.
  - Run `uv run black .` and `uv run flake8 .` before submitting.
  - Use Python **3.13.x** for local testing and formatting.

- **Testing**
  - Run `pytest` before pushing.
  - Ensure coverage isn’t regressing.

## 3. Architecture Decision Records

Significant architectural decisions are documented as ADRs in
`docs/adr/`. Before changing or replacing a decision captured in an
ADR, write a new ADR that supersedes it — do not edit the original.

**When to write an ADR:** apply the three-part test:
1. A real fork existed — a genuine alternative was considered and
   rejected.
2. The code doesn't explain the why — a new contributor reading the
   source cannot infer the reasoning.
3. Revisiting it would be costly — changing it requires significant
   rework.

All three must be true. Process conventions (commit format, branch
naming) and project principles (audience, tone) do not belong in ADRs.

ADRs are append-only. To change a decision: write a new ADR with
status `SUPERSEDED by ADR-NNNN` on the old one.

## 4. Pull Request Workflow

- **One logical change per PR.**
- **Rebase or squash** before opening to keep history clean.
- **Title & Description**
  - Use Conventional Commit format.
  - Explain _what_ and _why_ concisely in the PR body.

## 5. Issue Reporting

- Search open issues before creating a new one.
- Include clear steps to reproduce and environment details.
- Prefer **focused** issues—don’t bundle multiple topics.

## 6. Automation & Checks

All PRs and pushes go through CI:

- **Commitlint** for commit style
- **Black** for formatting
- **flake8** for static checks
- **pytest** with coverage

PRs must pass all checks to be reviewed.

## 7. Code of Conduct & Support

- See `CODE_OF_CONDUCT.md` for guidelines and reporting.
- For questions or planning, open an issue and use the `discussion` label, or mention a maintainer.

---

Thanks again for helping keep this project small, sharp, and focused.
