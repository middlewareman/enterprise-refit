# ADR 0003: Relocate the detailed README before rewriting the entry point

- Date: 2026-10-11
- Status: Relocation accepted; README overview subsequently authorized for local commit
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
the relocation commit. At that checkpoint, a portfolio introduction, case-study
summary and further reorganization remained recommendations for a subsequent milestone.

This updates the README responsibility in [ADR 0001](0001-documentation-and-checkpoints.md):
README is the public entry point; the guide carries the detailed purpose,
vocabulary, method and evidence requirements. Other document responsibilities
remain as recorded there. At relocation, the guide and planning reflection retained
their earlier artifact tables; updating those descriptions belonged to the editorial step.

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

## README overview follow-up

The relocation is committed locally as `72d1c07`. The author subsequently requested
the public README introduction and supplied personal motivation, learning style
and the central strategy: restore with minimal changes, add reasonable coverage,
transform boldly in steps, then review the plan and build knowledge between steps.

The README is an agent-written overview. Its first-person motivation and learning
account paraphrase only the author's newly supplied context. The original wording
was preserved in ignored private storage before drafting; client chronology and
previously withheld Theseus material were not copied into public documentation.
The DayTrader result and limitations come from the linked migration/repair records.
The guide's responsibility table now reflects the README/guide split; the earlier
planning reflection remains a historical account.

Overview document review passes: the README is 461 whitespace-delimited words;
Python checks resolve 64 local links and three heading anchors across the five
changed Markdown files. The DayTrader/test/performance claims were reviewed
against the migration and separate repair records. `git diff --check` passes,
and `git check-ignore` plus `git ls-files` confirm the private source is ignored
and untracked. No application tests ran for this documentation-only change.
The author subsequently requested committing the overview as a separate local
editorial milestone. Publication was not requested.
