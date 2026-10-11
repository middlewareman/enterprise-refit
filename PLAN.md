# Mission: Enterprise Refit — Working Plan

Last updated: 2026-10-11

## Active milestone and next action

**Milestone 5 — evaluate and compare, through collaboration reflection.**
Migration/performance engineering remains paused by author request. The planning
reflection and two pinned reference inspections are committed in `f69cae4`;
the author has accepted the documentation split in [ADR 0001](docs/decisions/0001-documentation-and-checkpoints.md).
The [knowledge/provenance inventory](docs/daytrader-knowledge-provenance.md) now
links source categories, concrete migration decisions and recorded checks, with
traceability limits and later reflection sources distinguished. [ADR 0002](docs/decisions/0002-knowledge-and-evidence-provenance.md)
captures standing attribution requirements. This supports the project's comparison
and portfolio goals while retaining corrections and evidence.

**Next action:** complete the IDEA installation/connection and skill-origin fields
in the provenance inventory from the author's setup account, distinguishing
recollection from verified configuration. Retain unknowns where details cannot be
recovered; resume engineering only at the author's request.

## Verified state and evidence

- Root planning reflection: `f69cae4`; documentation split: `935a656` (including
  the corrected history table); debug enablement: `9a6cde6`. The provenance
  follow-up is documentation-only; no application check was rerun.
- DayTrader is pinned at `6e6cfa787553e918e5c90edfd1e8882ce2c84d54` on
  `experiment/001/jakarta-ee11`, with frozen input `d25398b`. The
  [migration record](experiments/daytrader3-jakarta-migration/2026-10-11/README.md)
  reports two passing 52-case shell suites, unchanged test hashes, portable
  installation, Java 21 bytecode checks and IDEA integration execution.
- All six matching workloads preserve financial invariants. Median run p95 is
  122.9%/161.6% of baseline at one/four workers, crossing both investigation
  thresholds; causation and steady-state performance acceptance remain unresolved.
  This is a collaborative case study without an independent-agent access boundary.
- [Debug setup evidence](experiments/daytrader3-debug-setup/2026-10-11/README.md)
  records isolated Start/Attach/Stop and login/quote smoke. The amended Attach XML
  differs from the recorded validation hash; XML parses, but attachment was not
  rerun for that serialization. [Environment handoff](docs/project-history.md#environment-handoff-at-the-documentation-split)
  retains JDK/IDE details and the mixed legacy runtime cleanup caveat.
- Subject publication at this revision was previously verified and is recorded in
  the migration evidence. Root publication has not been requested. No gitlink or
  reference revision changes are part of this documentation milestone.

## Unresolved issues

- Exact IDEA plugin/connection/skill-installation provenance awaits author input.
- Functional evidence is bounded: full UI/REST behavior, original interactive
  startup, CI's two-JDK setup and broader concurrency/JMS failures are unverified.
- Theseus disclosure and selected reference-license questions remain pending;
  private chronology, questions and answers stay in ignored storage.

## Parked work

- Longer alternating performance measurements: revisit when engineering resumes;
  retain correctness settings and the predefined thresholds.
- Spring Boot/Quarkus, framework replacement, broader subject/reference comparison:
  revisit when selecting the next comparator under an explicit contract.
- REST XML defect and broad JMS fault injection: revisit when defining that
  behavioral scope or diagnosing a concrete failure.
- Boards or planning automation: revisit if concurrent ownership or repeated
  continuity problems demonstrate a need.

Earlier decisions and checkpoints are in [project history](docs/project-history.md).
The [reflection agenda](docs/reflection-agenda.md) links completed assessments and
remaining questions. [README](README.md) and [AGENTS](AGENTS.md) define the stable
method and working agreements; update this plan by replacing current status,
not appending a session transcript.
