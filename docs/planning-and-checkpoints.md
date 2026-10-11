# Reflection: planning, steps and commits

Recorded 2026-10-11 during the author's engineering pause. This is an agent
assessment for discussion, not an accepted change to the working agreements.
The question is whether our planning and checkpoint method makes the DayTrader
work easier to continue, review and compare without obscuring the evidence.
The stopping condition is a bounded assessment of this case and two pinned
references, with concrete recommendations; no new migration run is required.

## What the workspace demonstrates

At inspection, root HEAD was `c6d4022` and the clean DayTrader checkout was
`6e6cfa7` on `experiment/001/jakarta-ee11`, matching its gitlink. These observations
confirm revision/status, not a fresh execution of the reported application checks.

The separation of restoration `37a8fac`, tooling `a73e1ef`, failing concurrency
checks `7a4b337`, repair `f43c5f2`, enriched input `d25398b` and migration `6e6cfa7`
has concrete value. A reader can distinguish a recovered environment, a discovered
financial defect, an intentional behavior correction and a compatibility migration.
In particular, the repair becomes an explicit input to migration rather than a
hidden improvement attributed to the new platform. The
[experiment records](../experiments/) retain failures and corrections alongside
successful results.

The [contract](daytrader-jakarta-contract.md), frozen tests and recorded workload
thresholds also made completion assessable. Functional acceptance and the unresolved
performance result remain distinct. That is stronger evidence than a task list
whose final item says only “migration complete.” It does not prove that this
planning method caused the successful result or saved effort; those comparisons
were not measured.

The checked-in context supports resumption: this reflection began by reading
README, PLAN and AGENTS and comparing their claims with Git. It also exposed a
maintenance problem. PLAN had 174 lines and 4,423 whitespace-delimited words before
this update, including a decision log and a historical session handoff. One old
“Open” bullet still listed target validation as outstanding despite the later
migration outcome. The current section correctly described the result, but a new
reader or agent had to decide which duplicated status to trust. Marking history
as superseded helps; avoiding duplicate current-status statements would help more.

## Steps, validation checkpoints and commits serve different purposes

A step bounds work; a validation checkpoint records what was checked on a specific
state; a commit preserves a reviewable change. They need not occur at the same
frequency. Several edits and targeted diagnostic checks can lead to one validated
subject commit. Several subject commits can belong to one root milestone containing
the selected gitlink, contract and evidence. The
[coordinated workflow](subject-branches.md#coordinated-milestone-commits-and-publication)
already permits this. Root commits `6c83bb6` and `0da7a65` contain baseline/migration
evidence and their selected subject revisions, rather than only pointer changes.

The failing concurrency commit is a useful exception to a simple “every commit
must pass” rule: its purpose was to preserve a reproducible defect, and the record
labels the red suite. An intermediate broken transformation can likewise be a
recovery checkpoint if labeled clearly; it must not be represented as an accepted
working migration. README's working-state checkpoints remain a useful goal for
completed transformation steps, not a description of every diagnostic attempt.

The final migration commit is costly to review: Git reports 93 changed files,
9,238 insertions and 9,098 deletions. With `--ignore-all-space`, it reports 1,740
insertions and 1,600 deletions across the same 93 files. This shows substantial
whitespace churn; it does not isolate semantic changes or prove that all omitted
differences are harmless formatting. The migration record separately documents
token review and provider/REST/Faces changes. IDEA formatting was required, but
that requirement does not force all formatting and functional changes into one
commit. A future coherent milestone could contain separately reviewable formatted
changes, with appropriate checks on the final state. Do not rewrite this preserved
history just to make it resemble the proposed method.

## Comparison with two reference approaches

This reflection contributes a small descriptive comparison to the project's
research goal: it examines how two previously collected approaches organize work
and preserve decisions or execution evidence. The sources below are linked at
the exact inspected revisions so readers can inspect them without relying on our
current checkout or a moving default branch. Local links provide the same material
in this workspace. Inspection was read-only; neither approach was executed and
no reference application target was inspected.

### 1. AI-assisted code migration: phase commits and human review

Reference: **rmadabusiml/ai-assisted-code-migration**, the Claude Code / Bank of
Anthos demonstration listed in [README](../README.md#reference-approaches-and-evaluation-resources).
Inspected revision: `62e3394379a69a153aef8508c0229070148d98d0`.

- **Source:** [Core Migration checkpoint, pinned MIGRATION.md](https://github.com/rmadabusiml/ai-assisted-code-migration/blob/62e3394379a69a153aef8508c0229070148d98d0/MIGRATION.md#L253-L326)
  ([local copy](../references/ai-assisted-code-migration/MIGRATION.md#phase-2-core-migration)).
  It prescribes an initial migration commit and explicitly allows that checkpoint
  not to compile; compilation fixes follow in another phase.
- **Source:** [Documentation of Review Decisions, pinned README](https://github.com/rmadabusiml/ai-assisted-code-migration/blob/62e3394379a69a153aef8508c0229070148d98d0/README.md#L496-L503)
  ([local copy](../references/ai-assisted-code-migration/README.md#documentation-of-review-decisions)).
  It prescribes recording what was reviewed, the decision, rationale, reviewer
  and timestamp.

**What this contributes:** a concrete example of separating a recovery commit
from a validated outcome, and a concise structure for decision provenance. This
supports considering explicitly labeled incomplete checkpoints and retaining who
decided what and why. Our red concurrency checkpoint serves a different purpose:
it preserves a demonstrated defect rather than an incomplete transformation.

**Limit:** these are documented prescriptions. Inspection does not verify that
the advertised migration followed them or that they improve outcomes. Its later
test-generation phase also differs from our pre-transformation frozen evaluation.

### 2. Amazon JavaMigration: experiment identity and execution evidence

Reference: **amazon-science/JavaMigration**, the research agent implementation
listed in [README](../README.md#reference-approaches-and-evaluation-resources).
Inspected revision: `35b1dce3a5698cde62916ef0312a43f9b0895de9`.

- **Source:** [Repository implementation at the inspected revision](https://github.com/amazon-science/JavaMigration/blob/35b1dce3a5698cde62916ef0312a43f9b0895de9/src/java_migration_agent/core/repository.py)
  ([local copy](../references/java-migration/src/java_migration_agent/core/repository.py)).
  It records the starting HEAD and can generate a diff from that revision.
- **Source:** [Base agent lifecycle and result saving at the inspected revision](https://github.com/amazon-science/JavaMigration/blob/35b1dce3a5698cde62916ef0312a43f9b0895de9/src/java_migration_agent/core/base_agent.py)
  ([local copy](../references/java-migration/src/java_migration_agent/core/base_agent.py)).
  It runs the agent, evaluates the result and saves success flags plus the message
  trajectory under an experiment ID.
- **Source:** [MessageLimitHook at the inspected revision](https://github.com/amazon-science/JavaMigration/blob/35b1dce3a5698cde62916ef0312a43f9b0895de9/src/java_migration_agent/hooks/agent_hooks.py#L86-L115)
  ([local copy](../references/java-migration/src/java_migration_agent/hooks/agent_hooks.py)).
  It implements a configurable message limit.

**What this contributes:** source-level examples of experiment identity, bounded
execution and result capture. These reinforce keeping exact inputs and executed
evidence in experiment records while a shorter PLAN directs current work. The
recommendation to shorten PLAN comes from our observed duplication; this reference
does not itself demonstrate that a short Markdown plan works better.

**Limit:** the inspected lifecycle does not establish a phase-commit or
Architecture Decision Record (ADR) workflow. It also does not establish that every
subclass or saved run used identical practices. These functions were read, not run.

Together, these references offer complementary practices: one describes human
review and phase boundaries; the other implements execution and result capture.
They inform our recommendations without establishing a best practice or ranking.
Our collaborative enterprise-platform case differs from a batch Java upgrade
benchmark. A wider reference survey is unnecessary for this reflection.

## Recommended arrangement for the next experiment

| Artifact or practice | Recommended responsibility |
|---|---|
| README | Stable purpose, vocabulary and evidence requirements. |
| AGENTS | Stable operating rules, privacy boundaries and commit/publication constraints. |
| PLAN | One active milestone, current verified state and revision, unresolved issue, one next action, and a short parked list. Link history rather than repeating it. |
| Experiment record | Input/contract, executed checkpoints, failures, interventions, commands and outcomes. A concise result leads to detailed logs. |
| Decision record | Keep local decisions with their experiment. Use a small Architecture Decision Record (ADR: context, alternatives, decision/status, consequences) when a consequential choice governs multiple experiments. Attribute proposals and accepted decisions separately. |
| Issue board | Consider when concurrent contributors or independent work streams need ownership and dependencies. For the present single active milestone it adds another status surface to maintain. |
| Commits | Group by a reviewable purpose and evidence boundary. Separate an intentional repair from migration; keep coupled compatibility changes together when needed. Label incomplete checkpoints and record what passed. Preserve subject/root publication ordering. |

The immediate recommendation is to shorten PLAN and move its historical log and
handoff into an explicitly historical record, preserving the decisions and links.
This is a proposal awaiting discussion; that restructuring has not been applied.
No new board, ADR system or planning skill is needed to test the smaller change.

For the next engineering milestone, define its question, expected evidence and
stopping condition before execution; use targeted checks during diagnosis and
the required acceptance checks at the completed milestone. Keep checkpoint evidence
without committing each attempt. Assess the method by whether a fresh session can
identify the active objective, exact accepted state, remaining gap and next action
without reconciling contradictory summaries. This is a proposed criterion, not
a completed comparative evaluation.

Inspection used Git status/log/show/diff, Markdown reads, and source reads through
Codex (GPT-6). No agents were delegated, application tests run, reference revisions
advanced, private Theseus material read, commits made or publication performed.
Token usage, cost and total effort are unknown.
