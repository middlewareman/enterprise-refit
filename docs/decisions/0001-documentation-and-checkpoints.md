# ADR 0001: Separate current planning from historical evidence

- Date: 2026-10-11
- Status: Accepted by the author
- Origin: The author requested committing the planning reflection, then implementing
  its document split and updating the working instructions.

The README's purpose/method responsibility was subsequently relocated to the
[project guide](../project-guide.md) under [ADR 0003](0003-readme-relocation.md).
The original decision and its validation below are retained as historical evidence.

## Context

PLAN.md accumulated current status, a decision log, superseded handoffs and a
reflection agenda. The [assessment](../planning-and-checkpoints.md) found duplicated
status and an old open item contradicted by the later migration result. We need
continuity and an honest portfolio without making each session reconcile history.
Two pinned reference inspections inform checkpoint and evidence practices; their
outcomes have not been reproduced.

## Alternatives

- Retain all planning and history in PLAN.md: fewer files, but repeated status
  remains harder to maintain and read.
- Separate current state, history and execution evidence in repository Markdown:
  preserves revision-linked context and fits the present single active milestone.
- Introduce an issue board or planning automation: could help with concurrent
  ownership, but adds another status surface before that need is demonstrated.

## Decision

Use README for stable project purpose and method, AGENTS for operating rules,
and PLAN for one active milestone, verified state/revision, unresolved issues,
one concrete next action and a short parked list. Keep earlier project decisions
and handoffs in project-history.md, remaining reflection topics in
reflection-agenda.md, and execution details in their experiment records.

Record experiment-local decisions with the experiment. Create a short ADR only
for consequential choices governing multiple experiments, with context,
alternatives, decision/status and consequences. Attribute proposals and author
acceptance separately; do not retrospectively convert old recommendations into
accepted decisions.

Work steps, validation checkpoints and commits need not have equal frequency.
Use targeted checks during diagnosis and required acceptance checks on the final
milestone state. Commit by reviewable purpose; explicitly label incomplete or
failing recovery checkpoints. Preserve IDEA formatting requirements, original
failure evidence, subject/root milestone grouping and publication ordering.

## Consequences and validation

PLAN becomes easier to scan; moving history requires preserving text and fixing
relative links. History is read when relevant, not treated as a second task list.
No board, planning skill or automation is introduced. Future sessions still must
verify instruction discovery and compare the plan with the workspace.

Implementation review passed: 84 local links, including 10 Markdown section
anchors, resolve; all 27 earlier decision entries and 18 checkpoint bullets are
retained after adjusting their relative links. PLAN was reduced from 4,574 to
450 whitespace-delimited words. Authored whitespace checks and a consistency
review of README/PLAN/AGENTS pass. The subject remains clean at `6e6cfa7` with
its gitlink unchanged. No application tests ran; no reference revisions advanced
or private material was consulted. Improved efficiency remains a hypothesis to
assess in subsequent sessions.
