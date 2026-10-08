# Migration Lab

A workspace for investigating and demonstrating the modernization of legacy Java enterprise applications using AI coding agents such as Codex.

The aim is to develop a reusable migration method: give agents enough context to make coherent changes, preserve that context across sessions, and verify that the resulting application still does what it is supposed to do. Prompts, scripts, agent instructions, decisions, failed experiments, and human interventions are part of the deliverable alongside the migrated code.

This superproject brings together application sources, migration tools, research benchmarks, and documented case studies through Git submodules. It is initially a research and experiment scaffold; no migration or reproduction result is claimed yet.

## Vocabulary

| Term | Meaning in this project |
|---|---|
| **Migration subject** | An application selected for modernization. Before selection, a **prospective migration subject**. |
| **Reference approach** | An existing tool, method, research implementation, or case study that informs our work. Inclusion does not imply that its claims have been independently verified. |
| **Evaluation framework** | Tests, fixtures, and tooling used to assess the result, separately from the approach that produces it. |
| **Migration experiment** | A particular subject, source revision, target stack, approach, and evaluation contract. |
| **Baseline** | The pinned original application and its documented behavior in a reproducible environment, with any necessary restoration patches recorded separately. |
| **Migration contract** | What must change, what must be preserved, what may intentionally differ, and how those conditions will be checked. |

“Reference approaches” replaces “solution candidates” or “published attempts”: these materials serve different purposes, and some are benchmarks rather than solutions. Once a method is actually run against a subject, its execution becomes a migration experiment.

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

### deftERP

[medbounaga/deftERP](https://github.com/medbounaga/deftERP) is our proposed subject for exploring accumulated complexity in business application code.

The earlier repository inspection identified a Java 8 / Java EE 7 application with JSF, PrimeFaces, EclipseLink, and JasperReports, covering orders, inventory, invoicing, and accounting. It reported large controllers combining business logic, persistence, and report generation, and no discovered test sources. These are preliminary findings to recheck against the pinned revision, not a completed build or runtime assessment.

A useful first behavioral slice is **order → invoice → payment**, including the resulting persisted state and accounting entries. Buildability, usable sample data, and available infrastructure must be established before committing to that scope. The immediate task may be baseline restoration rather than migration.

This subject is attractive for studying how agents understand tangled business logic and how we establish a behavioral baseline where tests are sparse. We have not established production usage or reproduced an existing AI migration of it.

### DayTrader 3

[WASdev/sample.daytrader3](https://github.com/WASdev/sample.daytrader3) is our proposed subject for enterprise platform and framework migration.

It is an archived Java EE 6 stock-trading benchmark with login, quotes, portfolios, and share purchases/sales. Its repository includes enterprise modules, server configuration, and JMeter workload material. The upstream README describes both end-to-end workloads and functional/performance primitives.

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
| Theseus | Internal reference approach | Existing prompts, scripts, agent instructions, and accumulated migration knowledge. Identify transferable methods and test them on public subjects. Its current contents are not suitable for publication as-is. |

For each reference, record its pinned revision, prerequisites, license, claimed scope, available evidence, and what we actually reproduce. Some will inform our method without being executable competitors.

### Theseus and publishable evidence

Keep the current Theseus checkout optional and private, outside the public submodule manifest. Removing customer-code submodules does not establish that the remaining prompts, documentation, configuration, or Git history are publishable.

Derive public instructions and examples from reviewed, non-customer-specific methods and validate them on the public subjects. Describe these as new demonstrations. Their provenance should remain accurate; a later public experiment does not retrospectively change the circumstances of earlier work.

## Superproject layout

The following paths are a proposed layout, not files already present:

| Path | Purpose |
|---|---|
| `subjects/upstream/deftERP/` | Pinned upstream submodule, used as an untouched source baseline. |
| `subjects/upstream/sample.daytrader3/` | Pinned upstream submodule, used as an untouched source baseline. |
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

Run these examples from the root of an initialized superproject when ready to populate it:

```bash
git submodule add https://github.com/medbounaga/deftERP.git subjects/upstream/deftERP
git submodule add https://github.com/WASdev/sample.daytrader3.git subjects/upstream/sample.daytrader3
git submodule add https://github.com/konveyor/kai.git references/kai
git submodule add https://github.com/amazon-science/JavaMigration.git references/java-migration
git submodule add https://github.com/rmadabusiml/ai-assisted-code-migration.git references/ai-assisted-code-migration
git submodule add https://github.com/alexmanrique/spring-boot-application-example.git references/spring-boot-example
git submodule add https://github.com/scarfbench/benchmark.git evaluation/scarfbench
git submodule add https://github.com/amazon-science/MigrationBench.git evaluation/migrationbench
```

Review and select each revision, then commit `.gitmodules` and the submodule pointers in the superproject. For an existing checkout:

```bash
git submodule update --init --recursive
git submodule status --recursive
```

Submodules normally initialize at a detached HEAD. Perform editable experiments on explicit branches in forks or independent checkouts. Push implementation commits before updating and committing their superproject pointers so collaborators can fetch them. Keep reference updates separate from experiment runs; avoid automatically advancing to upstream HEAD during evaluation.

Add `/local-private/` to the superproject's ignore rules before using it. Public instructions and recursive cloning must work without Theseus credentials. Each submodule retains its own license and attribution requirements; this superproject's license does not replace them.

## Experiment workflow

1. **Inventory and pin.** Select a source revision, inspect the stack and business flows, and record environment requirements, missing artifacts, and uncertainty.
2. **Restore a runnable baseline.** Reconstruct the original build/runtime environment. Record dependency-resolution fixes or minimal repairs separately from migration. If the original cannot run, state the limitation and identify which claims can still be tested.
3. **Characterize behavior.** Use controlled fixtures and scenarios covering responses, persisted state, side effects, errors, and relevant concurrency. Review generated tests against original behavior and domain expectations; tests written by an agent are not automatically a trustworthy oracle.
4. **Define the contract and plan.** Select target versions and compatible components, permitted changes, excluded scope, checkpoints, and rollback strategy. Bundle changes only where compatibility requires it.
5. **Execute in reviewable steps.** Give the agent bounded tasks and allow it to inspect, edit, build, run tests, and diagnose failures. Combine deterministic transformations with agent reasoning where useful. Save decisions and unresolved issues in the repository.
6. **Evaluate independently.** Run the preserved baseline suite and target checks. Review diffs for disabled features, weakened tests, hidden fallback paths, and unintended behavior changes. For schema changes, test existing-data conversion and recovery.
7. **Report and generalize.** Record failures and human interventions, compare against the baseline, and extract reusable instructions only after they have worked on concrete cases.

A first sequence could be baseline restoration → JVM/build compatibility → selected dependencies → enterprise platform/server upgrade. Framework replacement and structural cleanup can become subsequent experiments with their own contracts. This ordering is a hypothesis to validate against each subject's compatibility constraints, not a universal recipe.

## Agent context and verification

Durable project knowledge should explain the current architecture, build/run commands, known quirks, chosen target stack, decisions, and exact evidence required for completion. Keep it versioned and concise enough to remain useful across sessions and tool changes.

For Codex, a root `AGENTS.md` can define workspace boundaries and subject-specific instructions can refine them. Check instruction discovery and precedence for each agent/tool; merely placing instructions in the superproject does not ensure every invocation uses them.

- Keep upstream and reference checkouts untouched; write implementation changes only to the assigned experiment checkout.
- Give the migration agent approved context. When measuring independent performance, exclude reference target implementations and held-out tests from its accessible workspace. Instructions alone are not an access boundary. Runs that consult reference solutions should be labeled **reference-assisted**.
- Keep evaluation expectations under separate control. Test-porting changes may be necessary, but weakening an assertion or changing its meaning needs explicit review and a recorded reason.
- Require executed validation and inspectable artifacts for completion. A successful build or the agent's assertion of success is insufficient.
- Record human decisions, corrections, and effort. Autonomy is something to measure, not assume from the presence of agent-generated code.

Initially target reproducible tasks driven by prompts, scripts, and checkpoints, with human supervision. Fully autonomous migration is a possible later experiment. The strongest demonstration is a traceable result and a clear account of where engineering judgment was necessary.

## Evidence and comparison

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

1. Populate public submodules and record the selected revisions and licenses.
2. Inspect both subjects and establish which can be built and run with reasonable effort.
3. Select the first subject and freeze a small but substantive behavioral slice.
4. Inspect Kai, ScarfBench, and MigrationBench first; document which ideas or checks transfer to our scope.
5. Run a bounded Codex migration and publish its contract, commits, executed checks, failures, and human interventions.
6. Repeat on another slice or subject, then distill the method into a reusable migration skill.

The eventual portfolio artifact should make the source state, target state, process, and evidence easy to inspect. Public experiments can demonstrate technical competence directly without depending on publication of customer work.
