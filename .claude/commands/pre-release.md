# Pre-release checklist

Run the pre-release checklist for this project.

**Working style**: propose before acting at every step — do not commit, push,
open PRs, or create tags until I explicitly confirm.

---

## Phase 1 — Determine next release

1. **Verify working tree**: Confirm we are on `master` with a clean working
   tree. If behind the remote, propose `git pull` and wait for confirmation
   before pulling.

2. **Detect current release and propose next**: Read `CHANGELOG.md` for the
   coach naming convention (A–Z table) and the most recent release heading.
   Run `git tag --sort=-v:refname` to confirm the latest tag. Then:

   - **Next codename**: next letter in the A–Z sequence after the current one.
     Use lowercase with no spaces for the tag (e.g. `eriksson`);
     Title Case for the CHANGELOG heading (e.g. `Eriksson`).
   - **Version bump** — infer from `[Unreleased]`:

     | Condition | Bump |
     |---|---|
     | Any entry marked BREAKING | MAJOR |
     | Entries under Added | MINOR |
     | Only Changed / Fixed / Removed | PATCH |

   - If `[Unreleased]` has no entries, stop and warn — there is nothing to release.

   Present a summary before proceeding:

   ```text
   Current:  v2.1.0-delbosque
   Proposed: v2.2.0-eriksson  (MINOR — new features in Added)
   Branch:   release/v2.2.0-eriksson
   Tag:      v2.2.0-eriksson
   ```

---

## Phase 2 — Prepare release branch

3. **Create release branch**: `release/vX.Y.Z-{codename}`.

4. **Update CHANGELOG.md**: Move all content under `[Unreleased]` into a new
   versioned heading `[X.Y.Z - Codename] - {today's date}`. Replace
   `[Unreleased]` with a fresh empty template:

   ```markdown
   ## [Unreleased]

   ### Added

   ### Changed

   ### Fixed

   ### Removed
   ```

5. **Propose commit**: `docs(changelog): release vX.Y.Z Codename`

6. **After confirmation**: commit. Then run steps 2–4 of `/pre-commit` (linting,
   formatting, tests — the CHANGELOG step is already handled). Push the branch
   and open a PR into `master` only once all checks pass.

---

## Phase 3 — Tag and release

7. **Stop and wait** for confirmation that:
   - All CI checks have passed
   - The PR has been merged into `master`

8. **Pull `master`**, then propose the annotated tag:
   - Tag name: `vX.Y.Z-{codename}`
   - Message:  `Release X.Y.Z - Codename`

9. **After confirmation**: create and push the tag. The CD pipeline triggers
   automatically.
