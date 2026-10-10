# Mission: Enterprise Refit — Working Plan

Last updated: 2026-10-10

## Purpose and intended outcomes

Investigate how human expertise, transformation tools, and AI agents can modernize legacy enterprise Java. Compare approaches through explicit migration contracts and inspectable evidence, and turn supported findings into a practical guide, toolbox, or reusable instructions. [README.md](README.md) describes the project and its research questions.

The project also serves as a portfolio for prospective employers: it should show how the author uses AI to understand problems, make decisions, carry out work, validate results, and maintain direction. The collaboration process is part of the evidence, including corrections, unsuccessful attempts, and human judgment.

The author has identified a tendency to become absorbed in details and lose sight of the larger goal. AI assistance will also be used to maintain perspective and continuity. Record concrete examples of how this helps, where it fails, and how the working method changes. Agents can lose perspective too; this is a shared working practice whose effectiveness remains to be assessed.

## Current position

- The README establishes the investigation; this plan and [AGENTS.md](AGENTS.md) establish the working agreements.
- All eight public subject, reference, and evaluation submodules are populated at initial pinned revisions. [docs/submodules.md](docs/submodules.md) records the commits, selection rule, license evidence, and unresolved license terms for the Spring Boot example and ScarfBench.
- DayTrader now uses the author's fork, `middlewareman/sample.daytrader3`, at the unchanged original pin. [The proposed subject branch convention](docs/subject-branches.md) separates build restoration, focused tooling upgrades, and migration experiments while preserving the fork's default branch as an upstream mirror. No work branches have been created.
- DayTrader's unchanged source compiled and produced its EAR with Gradle 4.10.3 and installed Java 8 in a disposable source copy. [The feasibility assessment](docs/daytrader-feasibility.md) records commands, packaging/bytecode evidence, and remaining runtime prerequisites. No full lifecycle build, runtime baseline, migration, or behavior result has been established.
- The Theseus chronology is internal and private. The questions, original author answer, and agent-written summary are private for now and retained in ignored local storage. The [initial account](docs/theseus-initial-reasoning.md) also requires disclosure review. Source fidelity and anonymized names do not establish permission to publish client information.
- DayTrader 3 and deftERP are prospective subjects. Earlier observations about them need verification against pinned revisions.
- The author now requests getting DayTrader running and prefers Gradle. Establishing its runtime baseline is the immediate direction; migration target stack and experiment contract remain undecided.

## Current focus and next action

**Current focus (milestone 2):** assess DayTrader runtime feasibility. The Gradle build-path question is answered: unchanged sources compile/package with Gradle 4.10.3 and Java 8. Next verify a pinned Liberty runtime compatible with the supplied server features. Keep baseline repairs, tooling upgrades, and migration results distinguishable. Theseus disclosure review stays pending alongside this public work.

**Completion criteria:** the bounded [feasibility note](docs/daytrader-feasibility.md) now records the pinned source, prerequisites, existing checks, executed packaging command, and runtime gaps. The build-tool assessment is complete. Continue the author's runtime objective by checking a pinned server and attempting deployment/startup on an explicit restoration branch; milestone 3 still requires repeatable fixtures and behavioral evidence.

**Recommended next action:** select and verify a pinned Liberty runtime against the existing server feature list on a restoration branch, then deploy/start using Gradle 4.10.3 and Java 8. Agent recommendation: establish the original runtime baseline before an optional Gradle upgrade; packaging proves an upgrade is not required for compilation. Incorporate the author's recollection and review into the Theseus account when available; keep deeper reference study separate until the initial account is reviewed.

**Author contribution:** the author supplied private context and requested a history investigation. The chronology, questions, and answers are private for now. Further author context is maintained in private notes.

**Next decision:** which pinned Liberty distribution/version can run the existing DayTrader feature combination? A migration question and target remain to be chosen after baseline evidence exists.

## Working roadmap

This sequence is a working proposal derived from the README. Refine it as evidence arrives; record the reason for material changes. Keep one main milestone active.

| Milestone | Outcome and completion evidence | Status |
|---|---|---|
| 1. Preserve initial reasoning | Private evidence retained; any public account contains only material suitable for disclosure, with hypotheses and limitations accurately attributed. | Chronology, questions, and answers private; related account review pending |
| 2. Assess subject feasibility | Selected public sources are pinned; prerequisites and licenses are recorded; build/run attempts and blockers support a subject recommendation. | Active: unchanged DayTrader compiles/packages with Gradle 4.10.3 / Java 8; pinned runtime selection and startup remain |
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
| 2026-10-09 | Author: create questions about Theseus. Agents: prepare a questionnaire for gathering author context. | Gather useful context in manageable batches; clarify the public name and scope. |
| 2026-10-09 | Author: supply initial answers and invite follow-ups; use only the Theseus alias publicly. Agents: preserve the original privately and prepare an anonymized draft. | Distinguish retrospective recollection from demonstrated results. Publication suitability remains subject to review. |
| 2026-10-09 | Author: use Git history rather than remembered dates. Agents: reconstruct selected milestones and initially prepare an anonymized chronology for the public document area. | The later privacy correction supersedes that placement; the chronology is retained internally. |
| 2026-10-10 | Author: keep the chronology internal and private; publication of questions and answers is undecided. Agent: move the chronology into ignored storage, remove copied timeline details and links, and unstage undecided drafts. | Anonymization and factual accuracy are insufficient disclosure checks. Record the publication boundary in AGENTS.md so later sessions preserve it. |
| 2026-10-10 | Author: keep the questions and answer private for now. Agent: move the questionnaire and answer summary into ignored private storage, preserving the original response and earlier snapshots. | All versions and their contents stay out of public documents and commits unless the author explicitly changes this decision. |
| 2026-10-10 | Author: use the DayTrader fork and develop a convention separating build repairs, tooling upgrades, and migrations. Agent: change the submodule URL while preserving its pin, retain the original as a local upstream remote, and propose `restore/*`, `tooling/*`, and `experiment/*` branches. | Permit assigned work branches in author-controlled subject forks at existing paths. Exact names are an agent proposal; target versions and experiment scope remain undecided. |
| 2026-10-10 | Author: get the existing DayTrader running, prefer Gradle, and assess an old Gradle versus upgrading. Agent: verify unchanged-source compilation/EAR packaging with Gradle 4.10.3 and installed Java 8 in temporary storage; recommend restoring runtime first. | A build-tool upgrade is optional for compilation. Runtime/version pinning and behavioral checks remain; the sequencing recommendation is not an accepted upgrade decision. [Evidence and remaining steps](docs/daytrader-feasibility.md). |

Record later material decisions here with their origin, rationale, and relevant evidence. Keep recommendations distinguishable from accepted decisions.

## Parked work

These ideas can be revisited when they serve a concrete milestone:

- A broad comparison of servers, target frameworks, or every reference repository: revisit when choosing an experiment or comparator.
- Framework replacement and structural cleanup: revisit after baseline evidence and an explicit migration contract exist.
- Modern Gradle/Liberty-plugin upgrade: revisit after DayTrader startup and representative behavior are established, or if a demonstrated runtime blocker requires tooling changes. Original compilation/packaging already works, so upgrading now would expand the baseline task.
- Sophisticated planning automation or a custom planning skill: revisit if these two documents prove insufficient in practice.

## Session handoff

- **Completed:** [DayTrader feasibility assessment](docs/daytrader-feasibility.md), comparing original-toolchain restoration with a Gradle upgrade. Gradle 4.10.3 downloaded into temporary storage; unchanged source copied by `git archive` and compiled/packaged successfully. Subject checkout, original pin, and gitlink retained; no work branch created. Earlier fork/IDE setup remains in place; Theseus material remains private.
- **Validation:** Gradle distribution checksum verified; `help` and targeted EAR/Derby-copy commands returned exit code 0. EAR member names and Java EE 6 descriptor inspected; class headers confirm EJB Java 7 and web/REST Java 8 bytecode. [Logs and artifact inspection](experiments/daytrader3-feasibility/2026-10-10). Documentation links and whitespace reviewed. No full `build`, test execution, Liberty install/startup, database initialization, behavior check, or Gradle upgrade was performed. Passing packaging is not a runtime baseline. The author requested committing the public setup and feasibility evidence; no push was requested.
- **Open:** compatible pinned Liberty distribution/version and feature installation, reproducible runtime/fixtures, behavior checks, optional tooling target, migration contract, and branch naming review; disclosure review of the Theseus account; unresolved license terms for the Spring Boot example and ScarfBench.
- **Next:** verify a pinned Liberty runtime against the existing features on a restoration branch and attempt deployment/startup with Gradle 4.10.3 / Java 8. Temporary build files may disappear; durable commands/logs are linked above. Keep private Theseus material excluded from public work.
- **Resume prompt:** "Read README.md, PLAN.md, and AGENTS.md. Summarize the current focus, check it against the workspace, and continue with the next action. Help me maintain perspective and flag work that loses its connection to the goal."
