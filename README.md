# Mission: Enterprise Refit

Exploring approaches to modernizing legacy enterprise Java.

*To boldly build what nobody has built in years.*

A workspace for exploring and comparing ways to modernize legacy Java enterprise applications, combining human expertise, transformation tools, and AI coding agents such as Codex.

The aim is to understand how different approaches tackle migration, what assumptions they make, where they need help, and what evidence supports their results. Reusable practices may emerge from that comparison. Prompts, scripts, documentation, decisions, failed experiments, and human interventions are part of the result alongside the migrated code.

This superproject brings together application sources, migration tools, research benchmarks, and documented case studies through Git submodules. It remains a research and experiment scaffold. [DayTrader's unchanged-source compilation and packaging](docs/daytrader-feasibility.md) and [first restored runtime smoke check](experiments/daytrader3-restoration/2026-10-10/README.md) have been checked. IDEA builds with Gradle 4.10.3 / Java 8, and Full EJB3/synchronous login, quote, buy/sell, and portfolio persistence pass on pinned Liberty. The [new baseline suite](experiments/daytrader3-baseline/2026-10-10/README.md) has 44 passing cases and 35.8% source-line coverage. Two ordinary builds pass after correcting a restart-test configuration omission; application source and assertions are unchanged. A [separate tooling upgrade](experiments/daytrader3-gradle-upgrade/2026-10-11/README.md) to Gradle 8.14.3 / Liberty plugin 3.10.0 also passes the unchanged 44 cases after clean compilation, with all expanded EAR entries unchanged. The [concurrency extension](experiments/daytrader3-concurrency/2026-10-11/README.md) now exposes a durable lost debit in two reset-fixture runs: both orders/holdings persist, but cash reflects one purchase. The separate [account repair](experiments/daytrader3-account-repair/2026-10-11/README.md) now passes the unchanged 49-case suite in two shell builds and the integration phases through IDEA. The original failing revision remains recorded. A [bounded uninstrumented workload](experiments/daytrader3-workload/2026-10-11/README.md) passes six fresh fixtures with financial/SQL checks; its short windows are smoke measurements, not a steady-state performance baseline. [Target preparation](experiments/daytrader3-migration-readiness/2026-10-11/README.md) validates a checksum-pinned Java 21 / Open Liberty Jakarta EE 11 environment and records a [migration contract](docs/daytrader-jakarta-contract.md). The [Java 21 / Jakarta EE 11 migration](experiments/daytrader3-jakarta-migration/2026-10-11/README.md) now passes two shell suites with all 52 frozen cases, clean portable installation/bytecode checks and IDEA integration execution. All six matching workloads preserve financial invariants; p95 latency exceeds the predefined investigation threshold at one and four workers. Functional migration is validated within the contract; steady-state performance and reference-method reproduction remain unverified.

A useful outcome could be a practical guide, a toolbox, or a method that engineers apply manually or with agent assistance. The degree of automation can vary across steps and evolve as agents improve. We assess an approach by the quality of its results, the confidence in its validation, and the effort required to use it.

## What we want to compare

| Dimension | Questions |
|---|---|
| Migration scope | Which changes does the approach address, and what does it assume is already working? |
| Application understanding | How does it discover architecture, business rules, dependencies, and constraints? |
| Transformation strategy | How does it combine human judgment, deterministic tools, and agent reasoning? |
| Context and continuity | What knowledge does it retain, and how does work continue across sessions and tools? |
| Human involvement | Where are planning, review, correction, and specialist knowledge needed? |
| Validation and outcomes | What was demonstrated, what remains uncertain, and what time and effort were required? |

Comparison includes both studying documented approaches and conducting local experiments where suitable. Some references contribute techniques or evaluation tools; others offer experience we can learn from. Each can inform the investigation in its own way.

## Vocabulary

| Term | Meaning in this project |
|---|---|
| **Migration subject** | An application, or a selected part of one, used to investigate a migration question. Before selection, a **prospective migration subject**. |
| **Reference material** | A tool, method, implementation, case study, or evaluation resource that informs our work. Inclusion does not imply that its claims have been independently verified. |
| **Reference approach** | A migration method or strategy we want to understand and compare, whether independently developed or described in reference material. |
| **Evaluation framework** | Tests, fixtures, and tooling used to assess the result, separately from the approach that produces it. |
| **Migration experiment** | A particular subject, source revision, target stack, approach, and evaluation contract. |
| **Baseline** | The pinned original application and its documented behavior in a reproducible environment, with any necessary restoration patches recorded separately. |
| **Migration contract** | What must change, what must be preserved, what may intentionally differ, and how those conditions will be checked. |

“Reference materials” is the umbrella term for the resources collected here; “reference approaches” identifies the methods and strategies they describe. Once a method is actually run against a subject, its execution becomes a migration experiment.

## What does migration mean?

Migration is a controlled transition from a defined source state to a defined target state under an explicit behavioral contract. **Modernization** is the broader program that may combine several migrations, refactorings, and operational improvements.

A target is a vector of choices rather than simply “newer Java.” These dimensions can be explored separately, although compatibility constraints may require some changes to be bundled.

| Dimension | Possible change | What needs checking |
|---|---|---|
| JVM runtime | Run existing binaries on a later JVM, initially retaining their existing bytecode level. | Removed runtime components, reflective access, JVM flags, encoding, TLS, memory use, and performance. |
| JDK and compilation target | Build with a newer JDK and choose a newer release/bytecode target. | Compiler and plugin compatibility; bytecode and API requirements; the actual deployment JVM. A newer build JDK alone does not imply newer bytecode. |
| Java source language | Raise the source level; optionally adopt records, text blocks, pattern matching, or other language features. | Required compilation level and semantic differences introduced by rewrites. Syntax modernization is optional, not a prerequisite for a runtime upgrade. |
| Enterprise specification | Move between Java EE/Jakarta EE generations and their constituent APIs. | API and descriptor changes, implementation support, dependency scopes, and container-provided services. Jakarta EE 8 still uses `javax` enterprise namespaces; the major namespace change comes with Jakarta EE 9. Not every `javax.*` package moves. |
| Application server | Upgrade an existing server or move to another compatible implementation. | Supported specifications/JVMs, JNDI resources, datasource configuration, security realms, deployment descriptors, messaging, and transaction behavior. |
| Framework generation | Upgrade within a framework family, such as an older Spring Boot generation to a newer one, or an older JSF/Faces stack to a newer stack. | Removed APIs, configuration defaults, extension libraries, authentication, rendering, and integration behavior. |
| Framework replacement | Replace Java EE container mechanisms with Spring or Quarkus equivalents. | Dependency injection, scopes, interceptors, EJB semantics, timers, async work, JMS/MDBs, and transaction boundaries. This is a substantially different experiment from a version upgrade. |
| Libraries and providers | Upgrade dependencies or replace an abandoned library; optionally switch JPA provider. | API compatibility and less visible changes in SQL, lazy loading, serialization, reports, rounding, and exception behavior. |
| Build and packaging | Upgrade Maven/Gradle and plugins; replace repository configuration; change EAR/WAR packaging or introduce an executable application. | Dependency resolution, reproducible builds, resource/class loading, provided dependencies, and deployment assumptions. |
| Data platform | Upgrade a database or driver, change database engine, or evolve the schema. | Constraints, sequences, SQL dialects, isolation, locking, data conversion, rollback, and integrity of existing data. |
| Deployment and operations | Introduce containers, CI, externalized configuration, health checks, observability, or new infrastructure. | Startup, readiness, secrets, persistent state, shutdown, resource limits, and operational recovery. Containerization alone does not modernize application semantics. |
| Internal structure | Extract services from controllers, clarify module boundaries, or remove duplication. | Behavioral equivalence and maintainability. Treat this as refactoring with its own evidence, rather than silently including it in a platform upgrade. |
| Product behavior | Correct defects, change monetary representation, redesign workflows, or replace a UI/API. | Explicitly revised requirements and tests. These are intentional behavior changes, not behavior-preserving migration. |

Success need not mean adopting the latest version of every component. Choose a coherent, supported target stack and record why it was selected. Framework migrations do not inherently require microservices, a frontend rewrite, or a new database.

Two useful scopes are **minimal compatibility migration**, which changes enough to run correctly on the target platform, and **expanded modernization**, which includes selected dependency, structural, or operational improvements. Define our scope explicitly; similarly named scopes in research benchmarks may have different acceptance rules.

## Prospective migration subjects

deftERP and DayTrader 3 are initial examples of the kinds of legacy code we might want to modernize. The selection is open to additions and substitutions as we identify useful migration questions. Subjects should expose relevant challenges, such as sparse tests, intertwined business logic, container services, or difficult build environments. One application can support several experiments with different scopes and target stacks.

### deftERP

[medbounaga/deftERP](https://github.com/medbounaga/deftERP) is our proposed subject for exploring accumulated complexity in business application code.

The earlier repository inspection identified a Java 8 / Java EE 7 application with JSF, PrimeFaces, EclipseLink, and JasperReports, covering orders, inventory, invoicing, and accounting. It reported large controllers combining business logic, persistence, and report generation, and no discovered test sources. These are preliminary findings to recheck against the pinned revision, not a completed build or runtime assessment.

A useful first behavioral slice is **order → invoice → payment**, including the resulting persisted state and accounting entries. Buildability, usable sample data, and available infrastructure must be established before committing to that scope. The immediate task may be baseline restoration rather than migration.

This subject is attractive for studying how agents understand tangled business logic and how we establish a behavioral baseline where tests are sparse. We have not established production usage or reproduced an existing AI migration of it.

### DayTrader 3

[middlewareman/sample.daytrader3](https://github.com/middlewareman/sample.daytrader3), forked from [WASdev/sample.daytrader3](https://github.com/WASdev/sample.daytrader3), is our proposed subject for enterprise platform and framework migration. The submodule uses the author's fork, with the original source revision and restoration result recorded separately.

The original repository is an archived Java EE 6 stock-trading benchmark with login, quotes, portfolios, and share purchases/sales. Its sources include enterprise modules, server configuration, and JMeter workload material. The upstream README describes both end-to-end workloads and functional/performance primitives.

The earlier code inspection identified EJB/JPA and JDBC paths, JMS/MDB mechanisms, and EAR packaging. Recheck which paths and deployment modes are runnable in the baseline. Initial scenarios should cover login, a quote lookup, a purchase, a sale, and consistent portfolio/order state; include asynchronous completion, rollback, and concurrent access where the selected mode uses them.

DayTrader gives us a stronger starting point for examining transactions, container services, and performance. Its workload material is useful but does not replace application-specific assertions. ScarfBench's DayTrader variants are related reference material, not interchangeable copies of this older repository.

Both subjects are from the Java EE era after the formal J2EE naming period. “Legacy enterprise Java” is the more accurate umbrella term.

## Reference approaches and evaluation resources

The following are starting points for investigation. Repository documentation and published accounts establish what their authors describe; we have not reproduced their results. Avoid comparing reported success rates without matching task scope, subject selection, test criteria, agent versions, and budgets.

| Resource | Role | What to investigate |
|---|---|---|
| [Konveyor AI / Kai](https://github.com/konveyor/kai) | Migration tooling and reusable knowledge | Static-analysis-guided LLM work, migration scenarios, and storage/retrieval of previously solved examples. The current repository contains backend components; its README links to the IDE extension separately. Inspect the Java EE → Quarkus/Coolstore material discussed in the initial research. |
| [ScarfBench](https://github.com/scarfbench/benchmark) | Cross-framework benchmark and reference implementations | Jakarta EE, Spring, and Quarkus variants; runtime and behavioral evaluation; whole-application examples including DayTrader. Study test quality, architecture constraints, and failure modes before adapting its harness. See the [paper](https://arxiv.org/abs/2605.06754). |
| [Amazon JavaMigration](https://github.com/amazon-science/JavaMigration) | Research agent implementation | Java 8 → 17/21 strategies: direct prompting, enhanced instructions, dependency information retrieval, and dependency preprocessing. Inspect saved traces and how the agent reacts to build failures. |
| [Amazon MigrationBench](https://github.com/amazon-science/MigrationBench) | Dataset and evaluation framework | Build/test success, compiled bytecode level, preservation of test methods and test counts, and dependency criteria for its minimal/maximal scopes. These checks approximate equivalence; they do not establish that untested business behavior is preserved. |
| [AI-assisted code migration](https://github.com/rmadabusiml/ai-assisted-code-migration) | Demonstration and case study | Claude Code modernization of Bank of Anthos's Transaction History Service, including Java and Spring upgrades, agent instructions, and human review checkpoints. Inspect the actual changes and validation rather than adopting its outcome claims. |
| [Alex Manrique's migration account](https://alexmanrique.com/blog/development/2026/02/19/migrating-to-java17-and-spring-boot-335-using-claude-code-and-cursor.html) and [example repository](https://github.com/alexmanrique/spring-boot-application-example) | Practitioner case study | Reported Java 8 / Spring Boot 1.4.3 → Java 17 / Boot 3.3.5 work using Claude Code and Cursor. Review planning, tests, incremental commits, and continuity across tool changes. The article is a reference link; the repository can be a submodule. |
| Theseus | Independently developed internal approach | Markdown documentation for humans and agents, transformation scripts, and accumulated migration knowledge. Examine its assumptions and techniques alongside other approaches, and test which parts transfer to public subjects. Its current contents are not suitable for publication as-is. |

For each reference, record its pinned revision, prerequisites, license, claimed scope, available evidence, and what we actually reproduce. Some will inform our method without being executable competitors.

The [planning and checkpoint reflection](docs/planning-and-checkpoints.md#comparison-with-two-reference-approaches)
compares specific practices in the pinned AI-assisted code migration documentation
and Amazon JavaMigration source with our DayTrader experience. It links the inspected
sources and distinguishes their contribution to our recommendations from unverified
outcome claims. This is a descriptive comparison; neither reference approach was run.

### Theseus: an independent starting point

Theseus has a special place in this investigation because it was developed iteratively by the project's author while working through migration problems, before stepping back to survey existing approaches. It preserves an independent first attempt, with room for both naive assumptions and original ideas.

Theseus is the public alias for a private effort. Its retrospective account and supporting material require disclosure review; the questions and author answers are private for now.

There is value in giving a problem a sustained attempt before studying how others have solved it. That lets initial ideas develop on their own terms. Existing work can then illuminate gaps and suggest better techniques, while also shaping the possibilities we consider. Keeping the original reasoning visible helps us examine what we discovered independently, what others add, and what deserves revision.

Theseus combines Markdown documentation intended to be read by both humans and agents with scripts that perform parts of the transformations. The documentation explains what we want to achieve and how to approach parts of the work; the scripts make selected changes repeatable. We will examine how these pieces support each other, where they depend on human judgment, and which ideas transfer to other applications. Theseus contributes experience and hypotheses to the comparison, with its assumptions and results open to the same scrutiny as those of other approaches.

A [provisional account of Theseus's initial reasoning](docs/theseus-initial-reasoning.md) distinguishes author recollections, documented choices, current method observations, and questions for public experiments. Client-history chronology is retained privately. The account remains subject to disclosure review, and outcome evidence remains incomplete.

### Theseus and publishable evidence

Keep the current Theseus checkout optional and private, outside the public submodule manifest. Removing customer-code submodules does not establish that the remaining prompts, documentation, configuration, or Git history are publishable.

Derive public instructions and examples from reviewed, non-customer-specific methods and validate them on the public subjects. Describe these as new demonstrations. Their provenance should remain accurate; a later public experiment does not retrospectively change the circumstances of earlier work.

## Superproject layout

The public directories and eight submodules below are in place. Initial revisions and license observations are recorded in [docs/submodules.md](docs/submodules.md). `.gitkeep` placeholders retain empty public directories; keep placeholders outside submodule checkouts.

| Path | Purpose |
|---|---|
| `subjects/upstream/deftERP/` | Pinned upstream submodule, used as an untouched source baseline. |
| `subjects/upstream/sample.daytrader3/` | Author-controlled subject fork; preserve the original source pin and use assigned branches for restoration, tooling, and migration work. |
| `references/kai/`, `references/java-migration/` | Pinned reference approach submodules. |
| `references/ai-assisted-code-migration/`, `references/spring-boot-example/` | Pinned case-study code submodules. |
| `evaluation/scarfbench/`, `evaluation/migrationbench/` | Pinned evaluation/reference resources. |
| `experiments/` | Experiment manifests, plans, decisions, and result summaries. |
| `implementations/` | Editable forks or independent checkouts for particular experiments; add as submodules when ready to record published results. |
| `harness/` | Our fixtures, behavioral checks, adapters, and comparison tools. |
| `prompts/`, `scripts/`, `docs/` | Shared instructions, automation, and durable project knowledge. |
| `local-private/` | Optional, ignored local Theseus checkout and other private material; absent from public setup and CI. |

The superproject owns orchestration and experiment metadata. Each application or reference repository retains its own history. Submodules pin exact commits, making source revisions explicit; they do not pin downloaded dependencies, container images, datasets, or model services. Those need separate records.

### Initial public submodules

The eight public submodules are populated. The following commands use their current configured URLs and can be used in a new initialized superproject. DayTrader now uses the author's fork; its initial revision is unchanged:

```bash
git submodule add https://github.com/medbounaga/deftERP.git subjects/upstream/deftERP
git submodule add https://github.com/middlewareman/sample.daytrader3.git subjects/upstream/sample.daytrader3
git submodule add https://github.com/konveyor/kai.git references/kai
git submodule add https://github.com/amazon-science/JavaMigration.git references/java-migration
git submodule add https://github.com/rmadabusiml/ai-assisted-code-migration.git references/ai-assisted-code-migration
git submodule add https://github.com/alexmanrique/spring-boot-application-example.git references/spring-boot-example
git submodule add https://github.com/scarfbench/benchmark.git evaluation/scarfbench
git submodule add https://github.com/amazon-science/MigrationBench.git evaluation/migrationbench
```

The initial pins capture upstream default-branch snapshots; assess their suitability before selecting experiment revisions. Commit `.gitmodules` and the submodule pointers in the superproject to share them. For an existing checkout:

```bash
git submodule update --init --recursive
git submodule status --recursive
```

Submodules normally initialize at a detached HEAD. Perform editable experiments on explicit branches in forks or independent checkouts. Group related subject work and root documentation/pointer updates into meaningful milestones; the repositories still require separate commits. Local staging and root commits can reference unpublished subject commits; explicitly report the exact revision and branch still needing publication. Before publishing the root commit, push the referenced subject commits and verify that collaborators can fetch them. See [the coordinated workflow](docs/subject-branches.md#coordinated-milestone-commits-and-publication). Keep reference updates separate from experiment runs; avoid automatically advancing to upstream HEAD during evaluation.

[The proposed subject branch convention](docs/subject-branches.md) separates `restore/*`, `tooling/*`, and `experiment/*` in author-controlled forks. The fork's default branch preserves upstream history; experiment records identify exact starting and result commits. Fork-backed subjects may be edited on assigned branches at their existing paths. Other original upstream and reference checkouts remain untouched.

The root `.gitignore` excludes `/local-private/`, local IntelliJ configuration, and macOS directory metadata. `local-private/` is an optional local directory and is absent from public clones. Public instructions and recursive cloning must work without Theseus credentials. Each submodule retains its own license and attribution requirements; this superproject's license does not replace them.

## Experiment workflow

The following is a starting hypothesis for a useful migration method. Planning, task decomposition, checkpoints, and recovery are themselves part of what we want to compare. For comparable experiments, agree on the starting state, requested change, and acceptance evidence, then record how each approach organizes the work and what adaptation it requires.

1. **Inventory and pin.** Select a source revision, inspect the stack and business flows, and record environment requirements, missing artifacts, and uncertainty.
2. **Restore a runnable baseline.** Reconstruct the original build/runtime environment. Record dependency-resolution fixes or minimal repairs separately from migration. If the original cannot run, state the limitation and identify which claims can still be tested.
3. **Establish verification baselines.** Preserve existing tests and add missing coverage using controlled fixtures and scenarios covering responses, persisted state, side effects, errors, and relevant concurrency. Record test identities/results and scoped line/branch coverage. Capture performance and resource use with a validated workload, fixed environments, warm-up, repeated runs, and recorded variability before selecting regression tolerances. Review generated characterization tests against original behavior and domain expectations. [DayTrader baseline plan](docs/daytrader-baseline.md).
4. **Define the contract and plan.** Select target versions and compatible components, permitted changes, excluded scope, checkpoints, and rollback strategy. Bundle changes only where compatibility requires it.
5. **Transform incrementally.** Apply bounded changes using manual work, scripts, agents, or a combination. Use targeted checks during diagnosis and the required acceptance checks at completed milestones. Aim to start each completed transformation step from a validated working state; interdependent changes may need to form one step. Work steps, validation checkpoints and commits need not occur at equal frequency. Preserve explicitly labeled failing or incomplete recovery checkpoints without presenting them as accepted working migrations. Group commits by reviewable purpose and save decisions and unresolved issues in their designated records.
6. **Evaluate independently.** Run the preserved baseline suite and target checks. Review diffs for disabled features, weakened tests, hidden fallback paths, and unintended behavior changes. For schema changes, test existing-data conversion and recovery.
7. **Report, learn, and refine.** Record failures and human interventions, compare against the baseline, and extract reusable instructions after they have worked on concrete cases. Use necessary manual fixes to improve documentation, scripts, tests, and subsequent agent-driven transformations.

A practical deliverable may be a document that guides an engineer through making the original application build and run, generating and reviewing missing tests, and applying transformations step by step, leaving a running application at each checkpoint. Scripts and agent instructions can support individual steps. As agents become more capable, they may take responsibility for longer parts of this chain while preserving the same observable checkpoints.

After establishing the baseline and tests, a first transformation sequence could be JVM/build compatibility → selected dependencies → enterprise platform/server upgrade. Framework replacement and structural cleanup can become subsequent experiments with their own contracts. This ordering is a hypothesis to validate against each subject's compatibility constraints, not a universal recipe.

## Shared context and verification

Durable project knowledge should explain the current architecture, build/run commands, known quirks, chosen target stack, decisions, and exact evidence required for completion. Write it for both humans and agents, and keep it versioned and concise enough to remain useful across sessions and tool changes. Markdown documentation can provide a shared account of the intent and procedure, while scripts make repeatable operations executable.

The author accepted the [documentation arrangement in ADR 0001](docs/decisions/0001-documentation-and-checkpoints.md)
following the [planning reflection](docs/planning-and-checkpoints.md). Keep each
artifact responsible for a distinct kind of context:

| Artifact | Responsibility |
|---|---|
| README | Stable purpose, vocabulary, method and evidence requirements. |
| [AGENTS.md](AGENTS.md) | Operating rules, privacy boundaries and coordinated commit/publication constraints. |
| [PLAN.md](PLAN.md) | One active milestone, current verified state/revision, unresolved issues, one next action and a short parked list. Replace status rather than append handoffs. |
| [Project history](docs/project-history.md) | Earlier project decisions, corrections and historical checkpoints; not a live task list. |
| [Reflection agenda](docs/reflection-agenda.md) | Collaboration questions and links to their assessments. PLAN selects the active topic. |
| [Experiment records](experiments/) | Contracts, inputs, executed checks, failures, interventions and outcomes. Keep local decisions with their experiment. |
| [Architecture Decision Records](docs/decisions/) | Short records of consequential choices affecting multiple experiments, with alternatives, acceptance/status and consequences. |

Read history and detailed records when they serve the current task. Preserve
evidence by linking it, rather than maintaining duplicate current-status accounts.
An issue board or planning automation remains conditional on a demonstrated need.

[How the agent used IntelliJ IDEA](docs/idea-agent-workflow.md) records concrete
formatting, editing, debugger and build-tool use in DayTrader, the supplied skill,
GUI limitations, author contributions and alternatives. It distinguishes observed
capabilities from setup details and potential features that remain unverified.
The [isolated DayTrader debug guide](docs/daytrader-debugging.md) explains the
shared Start/Attach/Stop configurations, disposable fixture and cleanup;
[setup evidence](experiments/daytrader3-debug-setup/2026-10-11/README.md) records
IDEA attachment, reset refusal, fixture preservation and failed-start cleanup.

For Codex, a root `AGENTS.md` can define workspace boundaries and subject-specific instructions can refine them. Check instruction discovery and precedence for each agent/tool; merely placing instructions in the superproject does not ensure every invocation uses them.

- Keep original upstream and reference checkouts untouched; write application changes only to assigned work branches in author-controlled forks or assigned implementation checkouts. Preserve original source pins and distinguish restoration, tooling, and migration revisions.
- Give the migration agent approved context. When measuring independent performance, exclude reference target implementations and held-out tests from its accessible workspace. Instructions alone are not an access boundary. Runs that consult reference solutions should be labeled **reference-assisted**.
- Keep evaluation expectations under separate control. Test-porting changes may be necessary, but weakening an assertion or changing its meaning needs explicit review and a recorded reason.
- Require executed validation and inspectable artifacts for completion. A successful build or the agent's assertion of success is insufficient.
- Record human decisions, corrections, and effort. Autonomy is something to measure, not assume from the presence of agent-generated code.

Human intervention is an accepted part of the method. Record what required help, why it was necessary, and how the correction can inform future work. Where possible, turn a manual fix into a clarified instruction, a repeatable transformation, or a regression check. This feedback can improve agent-driven work over time. Fully autonomous migration remains one possible experiment; a well-documented method used by an engineer is also a useful result.

## Evidence and comparison

Descriptive comparisons should distinguish an approach's claims, available artifacts, and our own observations. Local experiments support stronger comparisons when they share a suitable subject, scope, and evaluation contract. Record differences in setup, supplied knowledge, and adaptation effort; resources with different roles can contribute to the study without all being run against every subject.

Every experiment should record:

- Source, baseline-restoration, implementation, harness, and reference commit IDs.
- Target JVM/JDK, language/bytecode level, framework, server, libraries, database, and packaging choices.
- Build commands, environment/image identifiers, dependency inputs, fixtures, and evaluation contract.
- Agent/tool and model identifiers, date, configuration, context supplied, prompts, budgets, and relevant logs.
- Validation outcomes: build, deployment/startup, behavioral scenarios, persistence/side effects, and relevant failure/concurrency checks.
- Changes to tests, intentional behavior differences, known gaps, failures, and human interventions.
- Elapsed time, human effort, model usage/cost where available, and performance measurements where relevant.

For performance comparisons, hold hardware, resource limits, data, workload, warm-up, and measurement procedures constant, and repeat measurements. Source changes and environment changes otherwise become confounding factors.

Do not call passing tests a proof of universal equivalence. State the behaviors and conditions actually checked. If an old defect is corrected, document that as a separate accepted difference rather than silently moving the baseline. Repeat agent runs when comparing approaches because one successful run does not establish reliability; model-backed work may remain nondeterministic even with recorded inputs.

## Initial milestones

1. Document Theseus's initial reasoning and compare its assumptions and techniques with selected reference approaches and evaluation resources.
2. Populate the relevant public submodules and record the selected revisions and licenses.
3. Inspect initial subjects and establish which can be built and run with reasonable effort; revise the selection where useful.
4. Select a concrete migration question, a suitable subject or behavioral slice, and the evidence needed to evaluate it.
5. Run a bounded migration using the chosen combination of human work, scripts, and agents. Publish its contract, commits, executed checks, failures, and human interventions.
6. Compare with another approach where feasible, or explore another scope or subject. Distill supported findings into a practical guide, toolbox, or reusable agent instructions.

The published results should make the source state, target state, process, and evidence easy to inspect, including what people needed to do and how the approach improved through that experience. Public experiments can demonstrate transferable methods without depending on publication of customer work.
