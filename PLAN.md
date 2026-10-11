# Mission: Enterprise Refit — Working Plan

Last updated: 2026-10-11

## Purpose and intended outcomes

Investigate how human expertise, transformation tools, and AI agents can modernize legacy enterprise Java. Compare approaches through explicit migration contracts and inspectable evidence, and turn supported findings into a practical guide, toolbox, or reusable instructions. [README.md](README.md) describes the project and its research questions.

The project also serves as a portfolio for prospective employers: it should show how the author uses AI to understand problems, make decisions, carry out work, validate results, and maintain direction. The collaboration process is part of the evidence, including corrections, unsuccessful attempts, and human judgment.

The author has identified a tendency to become absorbed in details and lose sight of the larger goal. AI assistance will also be used to maintain perspective and continuity. Record concrete examples of how this helps, where it fails, and how the working method changes. Agents can lose perspective too; this is a shared working practice whose effectiveness remains to be assessed.

## Current position

- The public workspace contains eight pinned submodules; reference implementations remain untouched. Theseus history, questions and answers remain private. Disclosure and selected reference-license questions are parked.
- DayTrader's original source `a2d61af`, restoration `37a8fac`, Gradle-only `0894dc9`, tooling upgrade `a73e1ef`, failing concurrency harness `7a4b337` and intentional account repair `f43c5f2` remain separate evidence.
- The frozen migration input is `d25398b`: all 52 legacy cases pass, including three added JSF/REST cases. Six longer baseline workload fixtures pass; comparison thresholds were recorded before target measurements. Root prerequisite commit is `6c83bb6`.
- Subject commit `6e6cfa7` on `experiment/001/jakarta-ee11` contains the authorized Java 21 / Jakarta EE 11 migration. It passes two shell suites with all 52 frozen cases and unchanged test-source hashes. A clean build installs Open Liberty 26.0.0.9 separately, and all 77 application classes use Java 21 bytecode. IDEA passes 44 fresh integration cases with eight unit results up to date.
- All six target workload fixtures preserve HTTP/SQL financial invariants. Throughput is 95.0%/93.5% of baseline at one/four workers; median run p95 is 122.9%/161.6%, crossing both investigation thresholds. Initial request/GC/resource review does not establish the cause. [Migration evidence](experiments/daytrader3-jakarta-migration/2026-10-11/README.md).
- This is a collaborative engineering case study. No reference target was consulted, but no independent-agent access boundary was established. Passing the scoped suite does not establish universal equivalence or production readiness.
- The author-requested [isolated debug setup](docs/daytrader-debugging.md) is implemented in root `.run/` configurations and an opt-in Gradle adapter. IDEA Start/Attach/Stop, login/quote logpoint observation, pre-task active-server refusal and failed-start cleanup pass. Interactive/acceptance database hashes and frozen tests are unchanged; the subject remains clean at `6e6cfa7`. The server is stopped and agent probes removed. [Setup evidence and correction](experiments/daytrader3-debug-setup/2026-10-11/README.md). This root-only enablement milestone groups the IDEA account, stable-JDK follow-up, debug tooling and evidence; no subject pointer update or publication is needed.

## Current focus and next action

**Current focus (author-requested pause and reflection):** examine how the collaboration worked while keeping migration/performance engineering paused. The explicitly requested reusable isolated debug setup is now complete; return to reflection. Milestone 4's bounded functional result is preserved in root `0da7a65` and subject `6e6cfa7`; the performance gap remains open. The debug follow-up supports repeatable diagnosis without starting another migration iteration.

**Completion evidence:** two fresh 52-case shell suites, clean compilation/packaging and portable target installation, Java 21 bytecode/dependency inventory, frozen test hashes, IDEA integration execution/shutdown, six matching target workloads and an initial threshold investigation. Functional acceptance is demonstrated; steady-state performance acceptance remains unresolved. Startup of the original interactive configuration, complete UI/REST behavior, CI's two-JDK configuration and broader concurrency/JMS failures remain outside the demonstrated result. The separate debug setup now verifies its own startup and login/quote smoke only.

**Publication checkpoint:** the author pushed DayTrader. `git ls-remote origin refs/heads/experiment/001/jakarta-ee11` verifies exact remote tip `6e6cfa787553e918e5c90edfd1e8882ce2c84d54`. The coordinated root milestone includes this fetchable gitlink with its evidence. Root publication has not been requested.

**Next action:** discuss the [planning and checkpoint assessment](docs/planning-and-checkpoints.md), especially shortening PLAN to current state and moving its history into a separate record. This remains an agent recommendation, not an accepted restructuring. The assessment reviews DayTrader's actual revision/commit boundaries and two pinned reference approaches without executing them. The [IDEA-use account](docs/idea-agent-workflow.md) and [debug guide](docs/daytrader-debugging.md) preserve the earlier reflection. Exact plugin/connection/skill-installation details remain awaiting author input. Resume migration/performance engineering only when the author asks.

**Environment/IDE state:** Gradle 8.14.3 / Liberty plugin 3.10.0 are retained. Application/unit/server use pinned Temurin 21.0.12.1+1; external HTTP/fixture/SQL tools retain Zulu 8u504. The author has now installed the matching Java 21 version at a stable system path and registered `temurin-21` in IDEA. Gradle toolchain inspection under Java 8 and Java 21 succeeds without a path override; the agent removed the temporary override from local DayTrader Build. The earlier acceptance context remains unchanged. Gradle JVM remains Java 8 and root project SDK remains 25; reimport and startup of the original interactive configuration remain unverified. [Setup follow-up](experiments/daytrader3-jakarta-migration/2026-10-11/target-idea-build/jdk-registration-followup.txt). The ignored old `build/wlp` was overlaid during an invalid attempt and must be replaced before legacy reuse. Accepted target installations are separate and clean; interactive data was not reset.

## Reflection agenda

Author topics to follow up at suitable points; these are questions for discussion,
not authorization for new migration work or claims that comparative research has run.

- **IDEA and tool choice:** how edits, formatting, run configurations and debugger
  probes were performed; what each gained, failed to achieve or could disturb;
  what the author enabled; what a shell-only workflow would require instead.
  Project import, run configurations and code style are visible. The exact plugin
  installation/connection steps behind the supplied MCP tools/skill are unverified.
  Initial explanation and evidence are now in [How the agent used IDEA](docs/idea-agent-workflow.md).
  The author completed stable pinned-JDK installation/IDEA registration; discovery
  inspection verified it and the temporary build override was removed. Reusable
  isolated debug setup was then explicitly requested and is now implemented and
  checked; its guide and evidence are linked above. Semantic tools are already
  exposed and do not need extra installation; migration/performance work remains paused.
- **Planning, steps and commits:** assess the checked-in plan/status and separated
  restoration, tooling, repair, baseline and migration milestones. Consider a
  shorter current-state plan with history in experiment records, ADRs for decisions,
  issue boards and different commit/checkpoint choices. Study how selected reference
  approaches handle this before calling their practices observed or best practice.
  The [bounded assessment](docs/planning-and-checkpoints.md) now records benefits,
  duplicated/stale status, migration review cost and two reference inspections.
  It recommends a shorter PLAN, selective ADRs and commits by evidence boundary;
  no history restructuring or new planning system has been adopted.
  The comparison now identifies AI-assisted code migration and Amazon JavaMigration
  separately, with revision-pinned source links and an explicit explanation of
  how each informs the recommendations. README links to this comparison.
  The debug XML change is now included in amended enablement commit `9a6cde6`,
  separate from this reflection. It adds runner settings and removes `factoryName`,
  with formatting changes. Both XML versions parse, but the recorded validation
  hash describes the earlier version; no new attachment test was run in this review.
- **Knowledge and provenance:** inventory project documents, application/test
  evidence, skills, official documentation and general model knowledge. For the
  DayTrader migration, workspace context included README/PLAN/AGENTS, the contract,
  subject code, frozen tests and earlier experiment records. The IDEA integration
  supplied the `ij-debugger` skill; official Jakarta/Liberty/Gradle/provider material
  informed platform choices and diagnosis. Private Theseus material and reference
  target implementations were not consulted for this migration. Public project
  descriptions of Theseus were present in context; earlier private-history work
  is a separate activity. Individual pretrained knowledge sources are not traceable.

Initial agent assessment: checked-in context and milestone boundaries support
continuity, review and accurate attribution. PLAN.md accumulated historical status
and superseded next actions, creating maintenance and drift risk. Prefer one short
current state/next action with links to detailed evidence. The large final migration
diff also combines required namespace changes with IDEA formatting; assess its
review cost rather than assuming either smaller commits or fewer commits are always better.

## Working roadmap

This sequence is a working proposal derived from the README. Refine it as evidence arrives; record the reason for material changes. Keep one main milestone active.

| Milestone | Outcome and completion evidence | Status |
|---|---|---|
| 1. Preserve initial reasoning | Private evidence retained; any public account contains only material suitable for disclosure, with hypotheses and limitations accurately attributed. | Chronology, questions, and answers private; related account review pending |
| 2. Assess subject feasibility | Selected public sources are pinned; prerequisites and licenses are recorded; build/run attempts and blockers support a subject recommendation. | Complete for DayTrader: build, pinned runtime startup, and first synchronous trading check pass |
| 3. Establish a baseline | A selected subject has repeatable build/run instructions, controlled fixtures, and executed behavioral checks. Restoration patches are recorded separately. If restoration is infeasible, document the evidence and revisit subject selection. | Complete for the bounded contract: 52 cases, repeated workload and predefined investigation thresholds |
| 4. Define and execute an experiment | A source state, compatible target stack, permitted changes, and acceptance checks are recorded; bounded transformations produce inspectable commits and validation results. | Complete for bounded functional scope; performance limitation recorded |
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
| 2026-10-10 | Author: accept runtime restoration and configure IDEA first with the correct SDK. Agent: create `restore/runtime`, add the Gradle 4.10.3 wrapper, select installed Zulu Java 8 in IDEA, and pin IBM Liberty 24.0.0.9 for runtime verification. | IDEA import, compilation, and packaging pass. Open Liberty archive lacked six requested legacy features; IBM installation, full IDEA build, and synchronous runtime smoke passed. [Restoration evidence](experiments/daytrader3-restoration/2026-10-10/README.md). |
| 2026-10-10 | Author: establish test success, coverage, and performance baselines before refitting DayTrader. Agent: inventory tests/JMeter and propose a staged baseline protocol. | Existing test/FVT tasks have no test sources; coverage and performance are unmeasured. Start with controlled fixtures and state assertions, then coverage and validated repeated workloads. [Baseline plan](docs/daytrader-baseline.md). |
| 2026-10-10 | Author: prioritize Jakarta EE 11 because it is closest to Theseus; potentially try Spring Boot and Quarkus later. Prefer tests that remain unchanged across migration. | Keep one baseline milestone active. Build external, framework-independent characterization tests first; target environments and tooling still need pinning. |
| 2026-10-10 | Author: remove Maven support before adding tests. Agent: isolate the change on `tooling/gradle-only`, retain Gradle/runtime/dependency versions, and verify packaging plus the inherited build lifecycle in disposable copies. | Gradle is the sole maintained test/build path; Maven Central remains a dependency repository. Tooling changes are separate from restoration and application migration. |
| 2026-10-10 | Author: implement tests. Agent: add independent JUnit HTTP/restart/SQL verification, deterministic fixtures, focused units, isolated build lifecycle, and JaCoCo on the pinned runtime. | First slice exposed a restart UI-history mismatch while SQL persistence passed. Later runtime diagnosis identified a harness configuration omission and corrected it without weakening assertions or changing application source. [Results and limitations](experiments/daytrader3-baseline/2026-10-10/README.md). |
| 2026-10-10 | Author: diagnose and fix before committing. Agent: use non-suspending IDEA debugger logpoints to confirm default `longRun=true` suppresses UI orders after restart; reapply the same functional profile in restart setup. | Corrected the earlier premature legacy-defect label. Strict assertions remain unchanged; two normal builds pass with 44 cases. The proposed assertion review is obsolete because no meaning changed. [Diagnosis and evidence](experiments/daytrader3-baseline/2026-10-10/README.md). |
| 2026-10-11 | Author: commit and push DayTrader, then commit Enterprise Refit with its pointer. Agent: commit the validated harness as `fd8c371`, push `tooling/baseline-tests`, and verify the exact remote tip before staging the gitlink. | Record the published harness, passing results, coverage, original failure and corrected diagnosis together. Enterprise Refit is committed locally; its push was not requested. |
| 2026-10-11 | Author: apply IDEA formatting to agent-written code, or let the author format it, before committing; reduce root commits used only to synchronize submodules. | Record formatting in AGENTS.md and use coordinated milestone commits: subject commit(s), then one related root documentation/gitlink commit. Local commits can be prepared together; publish and verify subject commits before pushing the root. Agents handle ordering when publication is authorized. |

| 2026-10-11 | Author: perform the next two iterations independently and commit each. Agent: select Gradle 8.14.3 / Liberty plugin 3.10.0, preserve Java 8/IBM Liberty and validate clean packaging and unchanged tests. | First iteration is local subject commit `a73e1ef`; second is bounded concurrency coverage. Two root milestone commits group each subject pin with its evidence. No push requested. |

| 2026-10-11 | Agent outcome of the second assigned iteration: add strict concurrent purchase/restart/SQL checks and correct full-build shutdown ordering; commit the failing result as `7a4b337` on a separate harness branch. | Two fixtures lose opposite debits while both purchases persist. No application repair or weaker assertion was introduced. A separate baseline repair contract is recommended; an application behavior change is not yet an author decision. [Evidence](experiments/daytrader3-concurrency/2026-10-11/README.md). |

| 2026-10-11 | Author: fix the discovered defects and prepare for upgrade/migration, using bounded documented steps and updating the plan after each step. | Authorizes an intentional concurrency behavior correction before migration. Supersedes the agent's suggestion to carry the defect forward. Preserve the original failing result and record repair evidence separately. |

| 2026-10-11 | Author: go ahead with the proposed migration after discussing Java 21, EclipseLink, preserved interfaces/tests and performance reporting. | Authorizes the combined target-stack migration as a collaborative case study. Preserve financial assertions and record provider-related failures; finish baseline prerequisites before transformation. |

| 2026-10-11 | Author: pause engineering to reflect on IDEA use/enablement, checked-in planning and commit boundaries, alternatives and knowledge/skill provenance. Permit staging pointers before they are fetchable, with explicit publication status. | Preserve the reflection agenda; supersede the earlier supplied fetchability-before-staging restriction. Local staging/commits need no extra permission; subject publication/verification must precede root publication. |

| 2026-10-11 | Author: implement recommendation 2, a reusable isolated debug configuration. | Bounded setup work during reflection; root-only Start/Attach/Stop configurations reuse the existing deterministic fixture in separate storage. Agent improved reset refusal to run before provisioning, preserved its earlier verification-ordering failure and completed setup checks. No new migration/performance acceptance claim. |

Record later material decisions here with their origin, rationale, and relevant evidence. Keep recommendations distinguishable from accepted decisions.

## Parked work

These ideas can be revisited when they serve a concrete milestone:

- A broad comparison of servers, target frameworks, or every reference repository: revisit when choosing an experiment or comparator.
- Spring Boot and Quarkus comparisons, framework replacement, and structural cleanup: revisit after baseline evidence and the primary Jakarta EE 11 migration contract exist. The author may want all three paths; they are not concurrent active milestones.
- Longer alternating baseline/target workload measurements with stabilization and
  aligned diagnostics: revisit when the author resumes engineering. Both p95
  investigation thresholds remain crossed; preserve thresholds and correctness
  settings, and stop once evidence supports an optimization or a stated limitation.
- REST single-address XML defect: revisit after the migration; legacy GET without Content-Type returns 415 and its media-type comparison appears incorrect. JSON search is characterized.
- Broad JMS fault injection/redelivery testing: revisit when defining asynchronous guarantees in the migration contract, or if the bounded baseline scenarios reveal a messaging defect. Preserve the existing asynchronous happy-path checks; avoid an open-ended failure-testing campaign before the tooling upgrade.
- Sophisticated planning automation or a custom planning skill: revisit if these two documents prove insufficient in practice.

## Session handoff

The bullets below retain historical checkpoints. Use Current position/focus above
and the final migration outcome below for the current next action.

- **Completed:** prior feasibility/setup committed as `892d2bc`. `restore/runtime` created at the original source pin; Gradle 4.10.3 wrapper and IDEA instructions added. IDEA now imports all DayTrader modules, selects Zulu Java 8, and passes delegated compilation and the **DayTrader Package** configuration. Local IDEA build/start/stop configurations added; Liberty output now stays in ignored build storage and upstream-tracked generated state is restored. DayTrader restoration is committed and published as `37a8fac`; superproject commit `c6c9c88` recorded the restoration gitlink. The later Gradle-only commit `0894dc9` is now published on `tooling/gradle-only` and selected by this milestone. Workspace was clean at the start of the baseline inventory. The earlier publication/pointer blocker is resolved.
- **Validation:** wrapper packaging passed with ten executed tasks; IDEA packaging passed with ten up-to-date tasks. IBM Liberty 24.0.0.9 archive checksum verified, Gradle runtime installation passed, and exact Java EE 6 features were installed and signature/product-validated in a temporary runtime. Gradle startup/EAR deployment and the Full EJB3/synchronous smoke check passed; holdings changed 5 → 6 → 5, both new orders closed, and fresh logins preserved state. [Detailed restoration record](experiments/daytrader3-restoration/2026-10-10/README.md). The full IDEA EAR-module build also passed; inherited test/FVT tasks were NO-SOURCE. The restoration session left the server running from IDEA; availability was not rechecked during this documentation/inventory task. The current inventory found no files under `src/test`; JMeter XML supplies workflow requests and five text assertions, with mismatched documented/default thread count. No new tests, coverage collection, or performance runs were executed.
- **Documentation audit:** at the earlier audit checkpoint, checked all nine superproject Markdown documents at HEAD and in the working tree: 69 committed-version and 72 working-version local links resolve to committed files/directories or files in the pinned submodule revisions. No unresolved local links or existing local-only file references in inline code spans were found. Direct Git inspection confirms artifact-inspection.txt was committed in `892d2bc` and exists in HEAD. The two edited plan documents already existed in HEAD; the audit distinguished uncommitted edits from uncommitted target files. This was a repository-reference check, not an application test. Java 8 selection was also rechecked against upstream CI (`openjdk8`), mixed Java 7/8 bytecode evidence, and the selected Liberty runtime requirements; Java 7 execution remains untested.
- **New baseline progress:** published `fd8c371` on `tooling/baseline-tests` contains the implemented fixture, units, HTTP/restart/SQL suite and server coverage. 8 unit, 15 HTTP, 12 restart and 9 SQL cases pass; two ordinary builds pass from reset fixtures after the restart-profile correction. Matching runtime coverage classes resolve OpenJPA warnings; source coverage is 1713/4784 lines and 342/1085 branches. Finalizers stopped the server after real and deliberately selected test failures. [Evidence](experiments/daytrader3-baseline/2026-10-10/README.md). Earlier NO-SOURCE observations above describe the restoration/inventory checkpoint.
- **Workspace review (2026-10-11):** superproject `2ca7cca` pins subject `1c43422` on `tooling/baseline-tests`; both working trees are clean at inspection. The intervening author commits establish IDEA code style and reformat new harness code. Existing passing evidence still describes `fd8c371`; no new build or test was run during this recommendation review. The wrapper remains Gradle 4.10.3 and the Liberty plugin remains 2.4. Modernization of dependency configurations, archive/report APIs, plugin tasks and explicit JVM selection is required for a modern Gradle upgrade; changing only the wrapper URL is insufficient.
- **Baseline refresh (2026-10-11):** ordinary offline build at `1c43422` passes with Gradle 4.10.3 / plugin 2.4 / IBM Liberty 24.0.0.9. The 36 HTTP/restart/SQL cases ran; the eight up-to-date unit cases were then rerun successfully in a separate command. All 44 fresh results have zero failures/errors/skips. Source-line coverage remains 1713/4784; branches are 341/1085, with the one-branch difference at the random quote-change sign choice. The installed/runtime JDK is now Zulu `8u504`, distinct from the earlier recorded `8u282`. Initial sandbox socket denial was diagnosed and resolved through approved execution access. The isolated server is confirmed stopped. Compilation/packaging were incremental, not clean. Subject source and gitlink remain unchanged. [Commands, environment, results and limits](experiments/daytrader3-baseline/2026-10-11/README.md).
- **Tooling iteration completed:** local `a73e1ef` upgrades Gradle/plugin, applies IDEA formatting and pins Java 8 toolchains. Clean old/new builds both pass 44 cases; all 452 expanded EAR entries and application bytecode targets match. Failure-cleanup probe passes. Modern Gradle's JUnit/Java 7 classpath rejection required explicit Java 8 test compilation and attributes; stale IDEA documents initially reverted three edits and were corrected through the IDE patch API. Existing Gradle 9/configuration-cache warnings remain. Interactive startup was checked only by dry-run; IDEA execution is unverified. [Evidence](experiments/daytrader3-gradle-upgrade/2026-10-11/README.md).
- **Concurrency iteration completed:** local `7a4b337` adds five strict cases, preserves the original 44 and applies IDEA formatting. Full EJB/synchronous concurrent purchases persist both orders/holdings but lose one debit in two fresh fixtures: expected cash 29597.10; actual 29835.05 and 29762.05. SQL confirms both, restart confirms the first. Exact read/modify/write interleaving remains a source-supported hypothesis; the financial mismatch is verified. Initial unauthenticated observer and a skipped full-build finalizer were harness errors and were corrected. Shutdown runs after subsequent HTTP/restart failures; final server status is stopped. The new 49-case suite is red; source coverage remains 35.8%. Root tooling milestone is `2a44608`; the second root milestone groups this harness pin with its evidence. Neither iteration is pushed. [Results and limitations](experiments/daytrader3-concurrency/2026-10-11/README.md).
- **Account repair completed:** `f43c5f2` refreshes/locks mutable Full EJB accounts within the existing transaction. IDEA logpoints confirmed stale balance reads; two shell suites and one IDEA integration run pass without assertion changes. See the separate repair record.
- **Historical open issues at the repair checkpoint:** broader rollback/JMS failures, sustained performance/resource measurements/tolerances, target application validation and interactive startup. The later migration outcome resolves bounded target validation and defines comparison thresholds; steady-state performance and broader failures remain open. The separate debug setup validates its own isolated startup. Theseus disclosure and reference license questions remain parked/pending.
- **Workload preparation completed:** six uninstrumented reset runs pass financial/order/holding checks; raw request, resource and GC records retained. Short windows establish a runnable workload only; sustained performance and tolerances remain open.
- **Target preparation completed:** checksum-pinned Temurin 21.0.12.1+1 / Open Liberty 26.0.0.9 validate; direct Derby fixture load passes; corrected EE 11 plus XML Binding feature startup is clean. First full-platform startup revealed explicit LTPA/keystore configuration needs. No target application deployment occurred. See the migration contract and readiness evidence.
- **Historical next action (superseded):** lengthen workload windows, define comparison tolerances and create the migration branch. These prerequisites and the functional transformation are now complete.
- **Resume prompt:** "Read README.md, PLAN.md, and AGENTS.md. Summarize the current focus, check it against the workspace, and continue with the next action. Help me maintain perspective and flag work that loses its connection to the goal."

- **Migration input enrichment:** `d25398b` adds three JSF/REST characterization cases; all 52 pass on the legacy stack. The initial speculative XML success expectation failed with 415 and was corrected to observed baseline behavior before freezing evaluation. Original 49 assertions remain unchanged. All six longer workload runs pass HTTP/SQL invariants; input is frozen at `d25398b`. [Checkpoint evidence](experiments/daytrader3-jakarta-migration/2026-10-11/README.md).

- **Baseline prerequisite complete:** six reset workloads pass; comparison thresholds were defined before target results. The input manifests and raw measurements are recorded in the migration experiment. The transformation and frozen 52-case validation subsequently completed.

- **Migration deployment checkpoint:** source compiles/packages on Java 21; provider collection cast corrected; three EJB history failures diagnosed as stale cached inverse collections with correct cash/holdings. Explicit shared-cache policy fixes the strict suite. Invalid mixed-runtime attempts remain separately recorded.
- **Migration outcome:** two shell suites pass all 52 frozen cases, including independent concurrent purchase schedules, restart and SQL. Portable target installation and Java 21 bytecode/dependency checks pass. IDEA reruns 44 integration cases and stops the server; eight units are up to date. All six target workloads pass financial checks, but p95 crosses the predefined threshold at one/four workers. Initial diagnostics do not establish causation. Recommended next action: longer alternating measurements with stabilization and aligned diagnostics, before optional optimization.
