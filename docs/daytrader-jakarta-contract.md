# First DayTrader Jakarta EE 11 migration contract

Prepared 2026-10-11 after the author chose to repair discovered defects before
migration. This is an agent-prepared experiment contract and target proposal;
no application transformation or target-platform acceptance run has occurred.

## Question and input

Can the repaired legacy EAR retain its trading behavior on Jakarta EE 11 and
Java 21, with the same external scenario/assertion source and explicit platform
adapters? Preserve the enterprise architecture and HTML trading interface.

Source: subject commit `f43c5f2` on `repair/concurrent-account-updates`;
[repair evidence](../experiments/daytrader3-account-repair/2026-10-11/README.md).
Keep original `a2d61af`, restored `37a8fac`, tooling `a73e1ef` and known failing
`7a4b337` as separate evidence. The account correction is an intentional input
change, not a migration result.

Freeze application, harness, workload and environment at their exact final
commits/checksums before the transformation. Use a separate experiment branch
from this repaired source. Reference target implementations must be excluded by
an enforced access boundary if the run is to assess independent agent performance.
No such independent run or boundary has been established in this preparation.

## Proposed target and compatibility evidence

| Dimension | Proposed choice | Evidence and unresolved work |
|---|---|---|
| JVM/compiler | Temurin 21.0.12.1+1, archive/checksum pinned | Provisioned in isolated temporary storage; Java 21/Liberty startup and direct Derby fixture load pass. The global workstation JDKs remain unchanged. Use the pinned archive manifest; do not silently use 25. |
| Enterprise platform/server | Open Liberty 26.0.0.9, `jakartaee-11.0` | [Versioned feature documentation](https://openliberty.io/docs/26.0.0.9/reference/feature/jakartaee-11.0.html) lists Java 21 and platform features; [release record](https://openliberty.io/blog/2026/09/08/26.0.0.9.html). This changes both the IBM baseline runtime/version and the enterprise API generation. It is a coherent proposed target, not an assertion that every application dependency is compatible. |
| Build | Retain Gradle 8.14.3 / Liberty plugin 3.10.0 initially | [Gradle Java 21 support](https://docs.gradle.org/8.5/release-notes.html). The first migration does not require Gradle 9. Target-server installation/plugin behavior still needs execution. |
| Persistence | Jakarta Persistence 3.2, target default EclipseLink | [Versioned provider documentation](https://openliberty.io/docs/26.0.0.9/reference/feature/persistence-3.2.html). OpenJPA changes to EclipseLink: lazy loading, SQL, cache/locking, generated IDs and enhancement are material evaluation risks. |
| Messaging | Retain embedded Liberty messaging and MDB architecture | [Messaging server](https://openliberty.io/docs/26.0.0.9/reference/feature/messagingServer-3.0.html) and [client](https://openliberty.io/docs/26.0.0.9/reference/feature/messagingClient-3.0.html) support Jakarta messaging and the same style of engine/resources. Verify bindings, JNDI and two-phase transactions; no broker replacement is proposed. |
| Database/schema | Retain Derby 10.10.1.1 and schema initially | Driver/JDK/provider compatibility requires an actual target probe. If blocked, record a separate driver/platform decision and test existing-data compatibility; do not bundle a database replacement. |
| Test tools | Retain JUnit 5.10.3, Jsoup 1.17.2 and JaCoCo 0.8.12 initially | External HTTP tests can retain Java 8 independently. Unit tests that load target application bytecode need a compatible runner (Java 21). Coverage uses matching target runtime classes, not baseline OpenJPA-enhanced dumps. |

Official pages were consulted on 2026-10-11; documentation support is not
reproduced deployment evidence. Exact binaries are now checksum-verified, product validation passes, and a
corrected application-free feature/resource-configuration probe starts cleanly.
[Probe evidence and initial LTPA failure](../experiments/daytrader3-migration-readiness/2026-10-11/README.md).
Application compatibility and plugin integration remain unexecuted.

## Permitted changes and invariants

Permit necessary enterprise namespace/API, deployment descriptor, server feature,
resource binding, dependency-scope and toolchain changes. Set target application
bytecode deliberately to Java 21; avoid optional language rewrites. Retain EAR
modules, servlet/JSP/JSF interfaces, synchronous/JDBC/session-to-JDBC profiles,
asynchronous two-phase mode, fee/pricing rules and the repaired account invariant.
Change adapter/lifecycle/coverage configuration only as required by the target.

Preserve the 49 named test cases, assertions and independently calculated monetary
expectations. Unknown-quote HTTP 500 and rollback remain characterized behavior;
correcting the error interface is outside this migration. Preserve random
post-trade quote changes: compare state using pre-operation execution quotes.
Neither new order IDs nor random price sequences need equal the baseline run.
Keep business ownership, links, quantities, fees, completion and cash consistent.
No permitted weakening of financial, restart or persisted-state checks.

Do not globally replace every `javax` prefix. `javax.naming`, `javax.sql` and other
Java SE packages stay. Enterprise JAXB imports in the REST module require their
own API/runtime check. Inventory source, JSP/tag libraries, XML namespaces, JNDI
bindings and provider-specific APIs before transformation. Legacy API jars must
not leak into target deployment; use container-provided dependency scopes.

No frontend rewrite, microservice split, schema redesign, Spring/Quarkus conversion,
new database/broker, unrelated refactoring or extra defect hunt in this experiment.
Any newly discovered issue is classified as prerequisite, target regression or
baseline defect and recorded before deciding whether to expand scope.

## Acceptance and reporting

1. Clean target compilation/package checks, intended bytecode, dependency inventory
   and exact server/JDK/configuration recorded.
2. Ordinary target build passes all 49 cases from a reset fixture, including the
   concurrent account invariant, fresh sessions, restart, SQL and failure cleanup.
   Repeat the bounded concurrency scenario; record attempted/passed schedules.
3. Run the same external workload and business-state checks under equivalent
   fixture/heap/load conditions. Compare raw per-run latency/throughput/resources;
   acknowledge changed JVM/provider and short baseline measurement windows.
   Set performance acceptance criteria before looking at target results; none
   have yet been accepted. Correctness success can be reported separately from
   an incomplete or inconclusive performance comparison.
4. Verify IDEA build execution and isolated server shutdown. Interactive startup
   is a separate check; protect the author's existing database.
5. Publish exact outcomes, failures, source/test changes, human interventions,
   known gaps and model/tool identifiers with coordinated subject/root commits.

Existing limitations include broader rollback/JMS redelivery, concurrent sells
and mixed JDBC/EJB contention, JSF/browser behavior and REST address-book behavior.
The suite proves the named scenarios, not full application equivalence; successful
deployment of those modules alone does not establish their untested functionality.

## Next bounded iteration

First lengthen the baseline workload windows and establish comparison criteria.
Then create a separate experiment branch from `f43c5f2`, inventory the necessary
source/descriptor changes, and compile/package against the pinned Java 21 /
Open Liberty target without weakening tests. Then deploy/run the strict suite.
The probe revealed explicit keystore/LTPA configuration and XML Binding feature
requirements; include those in the isolated target adapter. Source code is still
untransformed. Use the [target artifact manifest](../experiments/daytrader3-migration-readiness/2026-10-11/artifact-manifest.json)
to reprovision temporary binaries when necessary. Resolve sustained performance
acceptance before reporting a completed performance comparison.
