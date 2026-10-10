# DayTrader baseline before migration

The author requested correctness, test-coverage, and performance baselines before
refitting DayTrader. This is the proposed measurement contract and implementation
sequence. No new tests, coverage collection, or load runs were executed during
this inventory. Numerical performance limits and the final migration scope are
still to be agreed after observing baseline variability.

## Frozen application and current evidence

Use restoration commit `37a8facf9729f271160aabc02dcf312fff7e0fc9`, preserving original
source `a2d61af8c75c771fe4c9ad3f101bbdef08046c1a`. The fork's `restore/runtime`
branch is fetchable, and superproject commit `c6c9c88` records its gitlink. Keep
application changes separate from baseline harness, fixture, and instrumentation
changes; record their own revisions and configuration.

The established environment is Gradle 4.10.3, Liberty plugin 2.4, Zulu Java
1.8.0_282/aarch64, IBM Liberty 24.0.0.9 with the original Java EE 6 features,
and embedded Derby 10.10.1.1. [Executed restoration evidence](../experiments/daytrader3-restoration/2026-10-10/README.md).

| Baseline dimension | Verified so far | Evidence still needed |
|---|---|---|
| Build/deployment | IDEA compilation, EAR packaging, full EAR-module build, server readiness | Repeatable setup and dependency/artifact identities for later comparisons |
| Test success | One external smoke script passes Full EJB3/synchronous login, quote, buy/sell, and holding persistence | Named test cases with pass/fail/skipped counts and response, money, database, and side-effect assertions |
| Test coverage | No measurement; no files under `src/test` found, inherited `test`/`fvt` were `NO-SOURCE` | Runtime line/branch coverage by application module and a scenario-to-behavior map |
| Performance/resources | No measured result | Latency distribution, successful throughput, errors, CPU, memory, GC, startup, and asynchronous completion where applicable |

The absence of tests is not a measured 0% coverage result. `TestServlet.java` is
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

**Next action:** implement a deterministic fixture and named Full EJB3/synchronous
characterization tests for login → quote → buy → sell, including fees, cash, order
state, and persisted holdings. Then collect coverage to find gaps before extending
transaction profiles and measuring the validated workload. This advances milestone 3;
application modernization remains subsequent work.
