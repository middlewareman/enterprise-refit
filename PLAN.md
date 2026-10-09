# Mission: Enterprise Refit — Working Plan

Last updated: 2026-10-09

## Purpose and intended outcomes

Investigate how human expertise, transformation tools, and AI agents can modernize legacy enterprise Java. Compare approaches through explicit migration contracts and inspectable evidence, and turn supported findings into a practical guide, toolbox, or reusable instructions. [README.md](README.md) describes the project and its research questions.

The project also serves as a portfolio for prospective employers: it should show how the author uses AI to understand problems, make decisions, carry out work, validate results, and maintain direction. The collaboration process is part of the evidence, including corrections, unsuccessful attempts, and human judgment.

The author has identified a tendency to become absorbed in details and lose sight of the larger goal. AI assistance will also be used to maintain perspective and continuity. Record concrete examples of how this helps, where it fails, and how the working method changes. Agents can lose perspective too; this is a shared working practice whose effectiveness remains to be assessed.

## Current position

- The README establishes the investigation; this plan and [AGENTS.md](AGENTS.md) establish the working agreements.
- All eight public subject, reference, and evaluation submodules are populated at initial pinned revisions. [docs/submodules.md](docs/submodules.md) records the commits, selection rule, license evidence, and unresolved license terms for the Spring Boot example and ScarfBench.
- No local build, runtime baseline, migration, or reproduction result has been established.
- A [provisional account of Theseus's initial reasoning](docs/theseus-initial-reasoning.md) now records reviewed early documentation, current method observations, and hypotheses for public experiments. Private source references are retained locally; author recollection, prior-exposure chronology, and shareable outcome evidence remain incomplete.
- DayTrader 3 and deftERP are prospective subjects. Earlier observations about them need verification against pinned revisions.
- Inspecting DayTrader first was an agent recommendation. Subject selection, target stack, and experiment contract remain undecided.

## Current focus and next action

**Current task (draft prepared):** document Theseus's initial reasoning before deeper reference study.

**Completion criteria:** a public account distinguishes early documented choices, current observations, intended benefits, and unverified outcomes; raw private material and customer-specific content are excluded; historical gaps and the author's review status are explicit. The draft is available, but author context and review remain pending.

**Recommended next action:** create `docs/daytrader-feasibility.md` with the pinned revision, prerequisites, upstream build/run instructions, existing checks, environment gaps, and a proposed first build command. Stop when the note supports a decision to attempt that build or inspect deftERP. This is a proposed first inspection, not final subject selection. Incorporate the author's recollection and review into the Theseus account when available; keep deeper reference study separate until the initial account is reviewed.

**Next decision:** which subject and migration question provide a useful, feasible first experiment? Buildability and behavioral evidence should inform that decision. DayTrader is a provisional first inspection candidate.

## Working roadmap

This sequence is a working proposal derived from the README. Refine it as evidence arrives; record the reason for material changes. Keep one main milestone active.

| Milestone | Outcome and completion evidence | Status |
|---|---|---|
| 1. Preserve initial reasoning | A reviewed, public account of Theseus's hypotheses and limitations; any unavailable or private evidence is identified. | Draft prepared from early and current documents; author context and review pending |
| 2. Assess subject feasibility | Selected public sources are pinned; prerequisites and licenses are recorded; build/run attempts and blockers support a subject recommendation. | In progress: public sources pinned; prerequisites and feasibility remain to be assessed |
| 3. Establish a baseline | A selected subject has repeatable build/run instructions, controlled fixtures, and executed behavioral checks. Restoration patches are recorded separately. If restoration is infeasible, document the evidence and revisit subject selection. | Planned |
| 4. Define and execute an experiment | A source state, compatible target stack, permitted changes, and acceptance checks are recorded; bounded transformations produce inspectable commits and validation results. | Planned |
| 5. Evaluate and compare | Results, gaps, failures, and human effort are reported. Compare another approach where feasible, or explicitly state why comparison is limited. Extract practices supported by the evidence. | Planned |

## How we keep direction

At the start of a substantial work session, identify the active milestone, the intended outcome, and why the next task contributes to it. A detailed question can be answered without silently replacing the project objective.

At natural checkpoints, ask: What have we learned? Does this still advance the milestone? Do we have enough evidence to decide? Recommend continuing, changing direction, or parking the investigation. Useful triggers include repeated blockers, expanding scope, and a discovery that changes an assumption.

Exploration is welcome. Give it a question, a concrete result, and a stopping condition. If it grows, state the cost to the current milestone and recommend a choice. Do not invent time or cost budgets; record agreed limits when supplied.

Before ending a substantive work session, update this file with verified progress, unresolved issues, and one concrete next action. Link detailed evidence rather than copying it here. Keep maintenance brief enough to support the work.

## Decision log

| Date | Decision and origin | Reason or implication |
|---|---|---|
| 2026-10-09 | Author: maintain project documentation in English. | Make the work accessible to the widest audience. |
| 2026-10-09 | Author: use the project to show prospective employers how AI and agents support engineering and maintaining focus. | Preserve an honest account of collaboration, self-awareness, and judgment alongside technical results. |
| 2026-10-09 | Author: create PLAN.md and AGENTS.md following the discussion of continuity across chats. | Store the plan and working agreements in the repository so future sessions can resume from explicit context. |
| 2026-10-09 | Author: create the directory structure and `.gitignore`. | Keep private material and local IDE files out of version control and leave submodule locations available. |
| 2026-10-09 | Author: add the Git submodules. Agent implementation: add all eight public repositories listed in the README at their default-branch HEADs and record license observations. | Populate the workspace ahead of the proposed Theseus account; keep deeper reference study separate from preserving initial reasoning. Theseus remains outside the public manifest. |
| 2026-10-09 | Author: perform the next step. Agents: draft the Theseus account from selected early and current private method documents, with source references kept locally and historical gaps explicit. | Preserve an initial account without inventing recollections or outcomes. Public feasibility work can continue while author context is pending. |

Record later material decisions here with their origin, rationale, and relevant evidence. Keep recommendations distinguishable from accepted decisions.

## Parked work

These ideas can be revisited when they serve a concrete milestone:

- A broad comparison of servers, target frameworks, or every reference repository: revisit when choosing an experiment or comparator.
- Framework replacement and structural cleanup: revisit after baseline evidence and an explicit migration contract exist.
- Sophisticated planning automation or a custom planning skill: revisit if these two documents prove insufficient in practice.

## Session handoff

- **Completed:** provisional Theseus account drafted; early documentation distinguished from current methods and new hypotheses. Private source-review notes retained outside version control; README and plan updated. No implementation changes were made.
- **Validation:** early claims checked against two historical documents; current method claims reviewed against selected documentation and scripts. Two additional agents reviewed provenance wording and change-transfer claims; their wording corrections were applied. Local links, table structure, selected private identifiers, ignored review-note paths, and whitespace were checked. The private checkout remains unchanged. These checks support the draft's accuracy, not migration outcomes or a complete disclosure audit. No private scripts or application checks were executed.
- **Open:** author recollection and review of the Theseus account; subject feasibility; subject selection; target stack; baseline and behavioral checks; unresolved license terms for the Spring Boot example and ScarfBench.
- **Next:** create the bounded DayTrader feasibility note while awaiting author context on Theseus.
- **Resume prompt:** "Read README.md, PLAN.md, and AGENTS.md. Summarize the current focus, check it against the workspace, and continue with the next action. Help me maintain perspective and flag work that loses its connection to the goal."
