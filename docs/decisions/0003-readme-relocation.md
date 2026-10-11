# ADR 0003: Relocate the detailed README before rewriting the entry point

- Date: 2026-10-11
- Status: Relocation accepted by the author; portfolio rewrite remains proposed
- Origin: The author requested considering repository accessibility for prospective
  clients, asked about separate commits for traceability, then instructed:
  "Do the move and commit".

## Context and alternatives

The README at root revision `b44a5d4aed411c10a0f4a8e29008fa7cd789ee1f`
contains 271 lines and roughly 4,600 words. It combines the project introduction,
method, vocabulary, workspace instructions and detailed results. The agent
recommended a concise portfolio entry point linked to a detailed guide and a
featured case study. Alternatives were adding an abstract to the existing README
or splitting and rewriting its sections immediately.

## Decision

Move the entire original README to [docs/project-guide.md](../project-guide.md),
changing only relative link destinations. Leave a minimal root
[README](../../README.md) pointing to the guide. Update incoming navigation and
[AGENTS](../../AGENTS.md) so new sessions explicitly load the guide.

Keep relocation and editorial work in separate commits. The author authorized
this relocation commit. A portfolio introduction, case-study summary and further
reorganization remain recommendations for a subsequent milestone.

This updates the README responsibility in [ADR 0001](0001-documentation-and-checkpoints.md):
README is the public entry point; the guide carries the detailed purpose,
vocabulary, method and evidence requirements. Other document responsibilities
remain as recorded there. The preserved guide and planning reflection retain their
earlier artifact tables; updating those descriptions belongs to the editorial step.

## Consequences and validation

The original prose and section anchors remain available at one inspectable path.
Moving the content before rewriting it separates preservation from editorial
judgment and helps Git infer the relocation from content similarity. The guide
still contains the original progress narrative; its editorial cleanup is pending.

Executed document checks:

- Python comparison against `git show b44a5d4:README.md` passes: all 271 lines
  are preserved exactly except the 29 rebased relative link destinations.
- Python path/heading review passes: 126 local links, including 10 heading
  anchors, resolve across the 11 changed Markdown files. No authored Markdown
  heading links still target the shortened root README. External URLs are
  unchanged; network availability and IDEA preview navigation were not checked.
- `git diff --check` passes. Diff review confirms navigation and documentation
  changes only; the subject gitlink remains `6e6cfa7`.
- `git diff --cached -B -M --summary` identifies the preserved guide as an
  86%-similar copy of the old README; the root path remains as the short entry
  point. Staged whitespace checks pass. The first staging attempt was denied
  access to `.git/index.lock` by the filesystem sandbox; authorized escalation
  succeeded without changing the commit scope.

No application tests ran, no reference revisions advanced and no subject files
changed. No private material was consulted or added. The author requested a local
commit; publication was not requested.
