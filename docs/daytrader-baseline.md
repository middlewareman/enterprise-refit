# DayTrader baseline before migration

The author requested correctness, test-coverage, and performance baselines before
refitting DayTrader. This is the proposed measurement contract and implementation
sequence. The initial inventory was followed by an implemented Gradle/JUnit suite
and server coverage. [Execution record](../experiments/daytrader3-baseline/2026-10-10/README.md):
44 cases pass in two ordinary builds, including strict restart order history
and SQL persistence. An initial harness configuration mismatch was diagnosed
with runtime debugger evidence and corrected without changing assertions. No load runs have been
executed; numerical performance limits and the migration contract remain open.

## Frozen application and current evidence

Use restoration commit `37a8facf9729f271160aabc02dcf312fff7e0fc9`, preserving original
source `a2d61af8c75c771fe4c9ad3f101bbdef08046c1a`. The fork's `restore/runtime`
branch is fetchable, and superproject commit `c6c9c88` records its gitlink. Keep
application changes separate from baseline harness, fixture, and instrumentation
changes; record their own revisions and configuration. The harness is now
published as `fd8c371a1bd5dbb26c28b7bbd5216de50a181660` on
`tooling/baseline-tests`, based on Gradle-only tooling `0894dc9`; this milestone
pins it in the superproject. Application Java sources remain unchanged.

The established environment is Gradle 4.10.3, Liberty plugin 2.4, Zulu Java
1.8.0_282/aarch64, IBM Liberty 24.0.0.9 with the original Java EE 6 features,
and embedded Derby 10.10.1.1. [Executed restoration evidence](../experiments/daytrader3-restoration/2026-10-10/README.md).

Java 8 is the restored build and application JVM, consistent with upstream
`.travis.yml` (`openjdk8`) and the selected Liberty runtime's stated minimum JVM.
The EJB module explicitly sets `sourceCompatibility = 1.7`; its observed Java 7
bytecode runs on Java 8. Web/REST modules use the Java 8 compiler defaults. Neither
Java EE 6 nor Java 7 bytecode requires a Java 7 runtime. Java 7 execution/API
compatibility was not tested; the recorded bootstrap-classpath warning means
Java 7 class-file output alone is insufficient evidence of Java 7 API compatibility.

| Baseline dimension | Verified so far | Evidence still needed |
|---|---|---|
| Build/deployment | IDEA compilation, EAR packaging, full EAR-module build, server readiness | Repeatable setup and dependency/artifact identities for later comparisons |
| Test success | JUnit: 8 unit, 15 HTTP, 12 restart, and 9 SQL cases pass; two ordinary builds pass | Extend concurrency/failure checks and retain the corrected restart profile |
| Test coverage | Server/unit JaCoCo: 1713/4784 source lines (35.8%), 342/1085 source branches; module and key-class counts recorded | Broader failure, concurrency, and messaging scenarios; review critical uncovered branches |
| Performance/resources | No measured result | Latency distribution, successful throughput, errors, CPU, memory, GC, startup, and asynchronous completion where applicable |

The original absence of tests was not a measured 0% coverage result. `TestServlet.java` is
an application servlet, not a discovered automated unit-test suite. A passing
build with `NO-SOURCE` test tasks does not establish test success.

## Correctness and fixtures first

Start with Full EJB3/synchronous ordering. Add the JDBC path and asynchronous
ordering as separately named profiles if they are within the migration contract;
do not combine their results. Asynchronous behavior is an important proposed
profile for DayTrader's transaction/JMS investigation. Include REST and JSF when
those interfaces are in scope; primitive pages are supplementary diagnostics.

Create controlled accounts, quotes, starting cash, holdings, and order state.
The current ten-user/100-quote population is randomly generated and suitable for
smoke testing; it is not a reproducible comparison fixture. Use deterministic
fixture loading or a checksummed database snapshot created with the server stopped.
Capture its schema, expected values, reset procedure, and any generators/seeds.
Restore the same starting state before independent runs. Stop Derby before copying
its embedded database. Use a separate measured workload fixture at a recorded scale.

Build externally driven characterization tests with explicit expectations for:

- Valid/invalid login, logout, session isolation, and quote lookup.
- Buy/sell quantities, holding creation/removal, order transitions, fees, and cash
  movements, using decimal monetary comparisons and the observed pricing rules.
- Persisted state after fresh login and server restart, checked against database
  state through a controlled inspection mechanism, not only rendered page text.
- Failure paths and rollback: record the actual legacy result, including partial
  effects or defects, before deciding what a migration may intentionally change.
- Asynchronous orders: enqueue, bounded completion, durable state, and failure/
  retry outcomes without duplicate financial effects, where the profile uses JMS.
- Concurrent operations: explicit invariants and contention cases, with reproducible
  accounts and a recorded schedule; keep these separate from throughput tests.

Review assertions against observed legacy behavior and domain expectations. Label
known defects and proposed corrections separately. Preserve test identities and
expected outcomes; any porting or changed assertion needs review and provenance.
Keep evaluation expectations under separate control during independent migration
runs and enforce the access boundary required by AGENTS.md.

The author subsequently requested removing Maven support before tests. The
`tooling/gradle-only` branch derives from the restored revision and retains the
application/runtime/tool versions. Tooling commit `0894dc9` is published on the
fork; `git ls-remote` verified its tip. Archive contents match the restoration
build and an isolated Gradle build lifecycle passed.
[Tooling change and validation](../experiments/daytrader3-gradle-only/2026-10-10/README.md).
The restored commit remains the comparison reference; this milestone selects the
fetchable tooling commit in the superproject gitlink.

## Reusable tests and Gradle integration

The author requires meaningful coverage and tests executed by the Gradle build,
while minimizing test changes during migration. Keep scenario definitions, fixtures,
and business assertions independent of application classes and framework annotations.
Use test-owned value objects and a small adapter for login, quote lookup, purchase,
sale, order/portfolio inspection, fixture reset, and persisted-state inspection.
The legacy adapter can drive the existing servlet/HTML interface; a migrated adapter
can drive the retained interface or an explicitly accepted replacement. The existing
REST module is an address-book sample, not a trading API.

Adapters may translate transport formats and environment details. They must not
supply expected outcomes, suppress failures, or normalize meaningful differences.
Preserve scenario identities and assertions across implementations. Changes to
behavior, test expectations, or verification strength require explicit review.
Keep a small set of HTTP/session/UI contract tests alongside the reusable business
scenarios so adapter reuse does not hide interface regressions. Database inspection
and fixture loading are environment-specific adapters too; transaction assertions
must exercise the real deployed application and its persistence/messaging services.

Implemented choice: JUnit Jupiter 5.10.3 with Jsoup 1.17.2 and JaCoCo 0.8.12
on Java 8 / Gradle 4.10.3. The dedicated verification module owns the isolated
fixture/server, HTTP/restart/SQL tasks and coverage; EAR `fvt` aliases its `check`.
Normal builds package the EAR and drive this server. The suite has no application
classpath dependency. [Usage and reports](../subjects/upstream/sample.daytrader3/docs/Testing.md).

Proposed build contract: `build` invokes `check`; `check` runs unit tests and the
bounded functional suite against an isolated test server and fixture. Functional
execution includes deployment/readiness, fixture reset, named assertions, coverage
capture/reporting, and cleanup after failures. Prevent cached/up-to-date test results
from masquerading as a fresh check against mutable external server/database state.
The suite must not consume or reset the author's interactive server/database.
Keep long load runs behind an explicit performance task, outside ordinary builds.

Add focused unit tests for stable calculations and rules where useful. Avoid making
framework mocks the primary assurance for EJB/JPA/JMS transaction behavior. Server
integration tests can exercise substantial application code without importing it.
A Gradle JaCoCo agent on the test JVM alone does not measure the Liberty JVM;
instrument the application process and aggregate reports from matching deployed
module classes. Set coverage requirements after the first measurement, identifying
critical uncovered branches rather than inventing a whole-project percentage.

## Test implementation options on the restored platform

The [artifact inspection](../experiments/daytrader3-feasibility/2026-10-10/artifact-inspection.txt)
records an EAR containing `dt-ejb.jar`, `web.war`, and `Rest.war`; original packaged
EJB classes use Java 7 bytecode and the WAR classes use Java 8 bytecode. These are
packaging facts from that feasibility run, not coverage measurements. The restored
server provides EJB/JTA/JPA/JMS behavior; tests can run outside it regardless of the
application bytecode level or future enterprise API namespace.

| Implementation | What it can verify | Likely changes during migration |
|---|---|---|
| External Java HTTP tests using JUnit 4.13.2 or a pinned Java 8-compatible JUnit 5.x release | Real servlet/session behavior, EJB/JPA trading state, and JMS effects through selected scenarios; combine with persisted-state checks | Low if the interface contract stays stable. Keep the client free of enterprise APIs and application classes; adjust launch/fixture/coverage configuration for each environment. |
| External Python tests using pytest | Similar HTTP/business scenarios, building on the existing Python smoke client; produce JUnit XML through pytest and invoke from Gradle | Low application coupling, but adds a separately pinned Python environment and custom Gradle execution/report handling. |
| Browser tests using Selenium or Playwright | Rendered UI, navigation, session behavior, JSF form/view state, and JavaScript behavior where present | No enterprise namespace coupling, but selectors and browser/tool versions need maintenance; use a small representative suite. |
| In-container tests using Arquillian or a test-only service bridge | Direct access to container-managed services, internal failure paths, transaction boundaries, and messaging setup | Higher: compatible container adapter, test deployment, enterprise APIs, and injected dependencies require porting. A bridge can isolate changes but introduces test-only deployment code. |
| Ordinary JUnit unit tests, with limited mocking | Pure calculations, formatting, and isolated branches such as `FinancialUtils` | Often reusable if signatures and dependencies stay stable; tests importing application beans or mocking persistence/container interfaces can require changes. They do not establish real transaction behavior. |
| Existing JMeter workload with stronger assertions | Repeated end-to-end requests, supplementary functional cases, and performance measurement | Workload parameters and response extraction can survive platform changes; current generic assertions are insufficient for financial correctness. Not recommended as the primary correctness suite. |

The proposed default is external Java/JUnit tests, a small set of pure unit tests,
and a small browser suite only when required by interface scope. JUnit 4.13.2 is
an option for minimal runner setup; JUnit 5.x offers useful parameterization and
organization and is preferred if its selected Java 8-compatible dependencies work
in the existing build. Neither requires migrating the application first. No runner
had been selected or tested at the initial discussion; the implementation now uses JUnit Jupiter 5.10.3.

Keep reusable tests in their own module with no dependency on the EJB/web artifacts.
The existing EAR `fvt` task can instead host external tests initially, provided its
test classpath remains independent of application/framework classes. A separate
pinned runner JVM/build is also possible: the test client can remain on Java 8
while the deployed application moves to a newer JVM. This avoids tying test-runtime
upgrades to application-runtime upgrades; Gradle orchestration may still change.

Distinguish unchanged scenario/assertion source from unchanged test dependencies,
runner, fixture driver, server lifecycle, and coverage agent. Test source can often
remain unchanged for an interface-preserving Jakarta migration; no approach can
promise that every tool and adapter remains unchanged across all three frameworks.
Coverage agents in particular must support the target class-file version.

For embedded Derby, a second process cannot simply attach to Liberty's live embedded
database. Options include inspecting it after a clean shutdown, explicitly configuring
network access, or using an isolated test-only inspection bridge. Record any such
configuration/deployment difference and retain independent monetary/state assertions.
Expand HTTP scenarios into failures, rollback, async completion, and concurrency;
use the first server-JVM coverage report to identify what requires narrower tests.

## When to upgrade Gradle

Agent recommendation: first make a small, useful characterization suite pass under
Gradle 4.10.3 / Java 8, including controlled fixtures and server-side coverage.
Then upgrade Gradle and the Liberty build plugin as a separate tooling change,
rerun those unchanged tests against the same Java EE 6 application/runtime, and
only then start the Java/Jakarta EE 11 transformation. A complete performance
campaign or exhaustive coverage is not a prerequisite for that tooling change;
finish the comparison baseline and contract before application transformation.
Record both build environments and preserve the restored revision as reproducible.

The current Gradle can run JUnit 4.13.2 and Java 8-compatible JUnit 5.x through
JUnit Platform; the latter needs `useJUnitPlatform()` on both relevant `Test`
tasks and aligned API/engine dependencies. Pin compatible HTTP/parser/assertion
libraries too. A newer framework release with a higher JVM requirement cannot
be assumed to work in this Java 8 build. JUnit 6 requires Java 17 or newer;
using it would require a compatible runner/build setup, not a Java EE namespace
migration of external test source. Python/browser runners can be invoked by
Gradle but have their own dependency/runtime compatibility requirements.

The framework choice need not track the application framework. The test client
can retain its own pinned JVM and JUnit release when Liberty moves to a newer JVM.
Upgrade server launch/fixture/coverage integration as necessary while preserving
scenario assertions. Modern Gradle toolchains make these JVM roles explicit:
Gradle daemon, compiler, test runner, and deployed application are separate choices.
Gradle 4.10.3 cannot run on Java 21; newer-JDK compilation also needs compatible
build support. Do not merely change IDEA's Gradle JVM on the old wrapper.

The [feasibility assessment](daytrader-feasibility.md#what-upgrading-gradle-would-require)
records the known legacy APIs and previously consulted compatibility guidance.
A modern wrapper requires script changes and a compatible Liberty plugin, not
only a distribution URL change. Select the exact Gradle/plugin/build-JDK tuple
by compatibility and validate preserved packaging/bytecode, deployment, readiness,
functional outcomes, and cleanup. New plugin defaults must not silently substitute
Open Liberty for the pinned IBM Liberty baseline. No tooling upgrade has been performed. The subsequent baseline execution
verified JUnit Jupiter 5.10.3 on the pinned Java 8 / Gradle 4.10.3 build.

## Migration direction and candidate platforms

The author selects Jakarta EE 11 as the primary migration direction because it
is closest to Theseus, and may later try Spring Boot and Quarkus. This establishes
priority, not a completed migration contract or pinned environment. The intended
question is how each path renovates the same baseline while preserving the trading
behavior assessed by the same evaluation suite.

| Candidate | Fit and migration implications |
|---|---|
| Java 21 LTS, Jakarta EE 11 on a compatible Liberty release | Primary direction selected by the author, retaining the enterprise architecture where supported. Retain enterprise beans, persistence, messaging, and server-rendered interfaces where supported. Namespace/API/descriptor changes and removed APIs still require work; verify the complete feature set and provider compatibility. Jakarta EE 10 is a possible intermediate target only if a concrete compatibility reason warrants it. |
| Java 21 LTS, a supported Spring Boot release, modern Gradle; JPA/Hibernate, PostgreSQL, and a JMS broker such as ActiveMQ Artemis | Possible later framework comparison: one deployable application with clear internal modules. EJB services, transaction boundaries, MDBs, security/session integration, and packaging require deliberate replacement. Preserve necessary cross-resource transaction semantics or explicitly review their redesign. PostgreSQL and broker replacement are separate migrations, not baseline prerequisites. |
| Java 21 LTS, Quarkus | Useful later comparator for framework replacement. Existing EJB/MDB mechanisms and JSP/JSF interfaces do not transfer directly; evaluate supported equivalents and interface scope before selecting it. |

Java 25 LTS is another candidate if the chosen framework, server, build tools,
providers, and operational environment support it. Java 21 is the conservative
proposal, not a claim about the latest release. Exact framework/server/JDK/Gradle
versions and support lifetimes still need verification against official release
and compatibility documentation. Public documentation retrieval was unavailable
in this discussion; no current compatibility matrix has been reproduced.

Preserve the current trading interface for the first transformation where practical.
Spring Boot does not provide a direct EJB/MDB or JSF replacement. Keeping JSPs needs
compatible servlet-container/packaging choices (for example a supported Tomcat WAR
arrangement); keeping JSF requires explicit integration. Do not bundle a frontend
rewrite, microservice split, or database replacement into a framework migration
without a reason and its own contract. Baseline tests come first; use independent
experiment branches from the same frozen baseline for platform comparisons.

## Coverage as supporting evidence

Use a pinned Java 8-compatible JaCoCo agent on the Liberty application JVM, driven
by the characterization suite. Save execution data, XML/HTML reports, exact class
artifacts, inclusion/exclusion rules, and line/branch counts for EJB, web, and REST
modules. Explain unexercised paths and which scenarios exercise core transactions.
Add focused unit tests where they expose useful behavior; prioritize assertions
on trading state over increasing a percentage.

Measure instrumented runs separately from performance runs. If a migration changes
frameworks or architecture, coverage denominators change; compare scenario coverage
and business invariants, and report percentages with their scope rather than treating
equal percentages as equal assurance. Set coverage criteria after the first report.

## Repeatable performance measurements

The subject includes [JMeter material](../subjects/upstream/sample.daytrader3/jmeter_files/README.txt)
and `daytrader3.jmx`. Inspection found login, trading, portfolio, account/profile,
registration, REST, and JSF requests. Its five response assertions check generic
page/submission text; these cannot verify balances, rollback, or order completion.
Review workload validity before collecting comparison numbers.

The README says 50 default threads, but the XML specifies **10**. XML defaults are
180 seconds, zero ramp-up, a 100 ms constant delay, users 0–14999, and stock IDs
0–9999. These user/stock ranges do not match the smoke fixture. Set every load,
fixture, endpoint, and timing parameter explicitly. Original script SHA-256:
`767552e11900bd70c24fc8220742a72f8fa43e442eaead8c12ec9643e49c2145`.
The script uses random choices and registration mutates the dataset. Record any
adapted workload, randomness/replay policy, and state evolution; reset between runs.

Pin JMeter and its JVM independently of the application's Java 8 environment.
Run non-interactively with a saved JTL and reports. Define warm-up and measured
windows, workload mix, arrival/concurrency model, think time, and fixture scale.
Use repeated runs at low load and a representative higher load; a saturation sweep
can follow once the first protocol is reproducible. Keep correctness assertions
active and report errors separately from latency for successful operations.

Record per-operation p50/p95/p99 latency and sample counts, successful request and
completed-business-operation throughput, HTTP/assertion/business failures, server
CPU/RSS or equivalent process memory, heap/GC pauses and frequency, and startup to
readiness. For asynchronous orders also measure enqueue-to-completion latency,
pending work, and drain time. Capture logs, timeouts, and lock/contention evidence
when relevant. Preserve raw measurements and per-run summaries, including variability.

Record hardware, OS, JVM/vendor/flags, heap, server/database config, database size,
warm/cold-cache conditions, background load, and load-generator location. A dedicated
generator is preferable; a laptop running both client and server yields explicitly
local comparative results. Compare runs under equivalent resource limits. Establish
regression tolerances from observed variability and project requirements before
looking at migrated results. Do not infer a universal speedup from one average.

## Completion and next action

Before migration, retain a baseline bundle: frozen application/harness/workload
revisions, artifact checksums, environment/configuration, controlled fixture/reset,
test results and coverage, repeated performance/resource measurements, known defects,
and accepted scope/tolerances. A fresh baseline run must reproduce the checks;
unmeasured dimensions stay explicitly unknown.

**Next action (recommendation updated 2026-10-11):** rerun the ordinary build on
the currently pinned test-formatting revision `1c43422`. The suite and server
coverage already recorded at `fd8c371` satisfy the prerequisite for a separate
Gradle/Liberty-plugin upgrade. Verify the same assertions and unchanged Java EE 6
runtime after that tooling change. Then add a bounded same-account concurrency
scenario, checking cash against execution values and fees, completed orders and
holdings, including persisted state. Finish controlled performance measurements
and the migration contract before application transformation. Exact tooling
versions remain to be selected and validated; this is not an accepted upgrade
decision. This advances milestone 3 without making exhaustive coverage a
prerequisite for progress.
