# DayTrader baseline tests — 2026-10-10

## Scope and revisions

The author requested meaningful tests during the Gradle build, with minimal
test-source changes during a later migration. This run implements the first
correctness and coverage slice of milestone 3; it is not a completed performance
baseline or migration contract.

Original source: `a2d61af8c75c771fe4c9ad3f101bbdef08046c1a`.
Restoration: `37a8facf9729f271160aabc02dcf312fff7e0fc9`.
Published Gradle-only base: `0894dc9998d42fe8563169aabca479a63372d675`.
Superproject base: `a1ec802`. Harness commit:
`fd8c371a1bd5dbb26c28b7bbd5216de50a181660`, based on `0894dc9`. On 2026-10-11 the
author requested committing/pushing DayTrader, then committing Enterprise Refit
with its pointer. The harness was pushed to `tooling/baseline-tests`;
`git ls-remote origin refs/heads/tooling/baseline-tests` returned the exact commit
above before the superproject gitlink was staged. This milestone pins it.
Enterprise Refit is committed locally; its push was not requested.
[Harness hashes](harness-sha256.txt) identify the source/build-script snapshot
used for the final passing results. The earlier failing snapshot is retained
in [pre-fix harness hashes](pre-fix-harness-sha256.txt). Application Java sources and original server XML
remain unchanged. No target/reference implementation was used to write these tests.

Environment: Zulu Java 8 `1.8.0_282` on macOS/aarch64, Gradle 4.10.3,
Liberty Gradle plugin 2.4, IBM Liberty 24.0.0.9 with original Java EE 6 features,
Derby 10.10.1.1, JUnit Jupiter 5.10.3, Jsoup 1.17.2, JaCoCo 0.8.12.
Dependencies were resolved before the final offline runs. Hardware/resource
limits were not controlled for performance measurement. This is local execution;
remote CI and the new suite through IDEA have not been checked.

## Implementation and fixture

The independent `daytrader3-verification` module has no application-class or
enterprise-API dependency. A legacy HTML/HTTP adapter drives scenarios with
test-owned values and independent decimal financial calculations. Separate unit
tests cover financial calculations. Gradle `build`/`check` and EAR `fvt` reach
the suite. Normal builds use an isolated server rather than deploying to the
interactive server. [Subject instructions](../../../subjects/upstream/sample.daytrader3/docs/Testing.md).

The test server uses HTTP 19083, HTTPS 19443, JMS 17276, JMS SSL 17286.
The fixture creates 40 accounts (`test:n`, password `xxx`), 40 quotes (`s:n`),
zero orders/holdings, cash `10000 + 1000*n`, prices `50+n`, timestamps
2020-01-01, and key seed 10000, using the original Derby DDL. State is reset
under the verification module's ignored `build/`. Trading accounts are isolated
per scenario, and the test forks run sequentially because configuration is global.

The application randomizes prices after a trade. Tests assert the fixed initial
buy price, observe the execution quote before selling, and calculate the cash
effect independently, with a 24.95 fee per trade. Thus post-trade values vary
between runs; this is a controlled starting fixture, not deterministic quote
evolution. [Final expected outcomes](expected-state.properties) include those
pre-operation calculations and identities learned from successful HTTP responses.

## Executed results

```bash
export JAVA_HOME=/Library/Java/JavaVirtualMachines/zulu-8.jdk/Contents/Home
export GRADLE_USER_HOME=/private/tmp/daytrader-gradle-inspection/user-home
./gradlew --offline --no-daemon --console=plain build
```

The [first fixed build](fixed-build-1.log) **passes**, including all strict
restart assertions and the ordinary SQL/coverage pipeline. HTTP tasks reran
from a reset fixture. Unit tests were up-to-date; their eight cases executed successfully earlier
([first functional build](first-functional-build.log)).

An immediate [second ordinary build](final-build.log) also passed, with 12
executed and 15 up-to-date tasks. Fixture preparation/loading, HTTP tests,
restart tests, SQL checks and coverage all reran; mutable tests were not reused
from cache. Across the 44 recorded cases, failures/errors/skips are all zero.
[First passing results](fixed-run-1-results/) and [final results](final-results/)
retain both outcomes. Coverage line/branch counts match between these two runs;
post-trade prices differ as expected from the application's randomization.

| Suite | Cases | Passed | Failed | Scope |
|---|---:|---:|---:|---|
| Financial unit | 8 | 8 | 0 | Gains/losses, zero balances, holding value and fractional shares |
| Session HTTP | 8 | 8 | 0 | Authentication, logout, isolation, profile update/rejection, registration |
| Trading HTTP | 7 | 7 | 0 | Fixed quote, buy, four buy/sell profiles, unknown-quote rollback |
| Restart HTTP | 12 | 12 | 0 | Cash/holdings and order history survive restart for six accounts |
| Stopped-DB SQL | 9 | 9 | 0 | Cash/counts for six accounts, nine order details, retained holding, profile/registration |

The trading profiles are separately named: Full EJB synchronous, Direct JDBC
synchronous, Session EJB to JDBC synchronous, and Full EJB asynchronous
two-phase. Async completion is bounded at 15 seconds. These results do not test
redelivery, retries, or contention. Unknown-quote purchase and wrong-password
login return legacy HTTP 500; their characterizations retain that behavior.
[Final JUnit XML](final-results/) retains named cases and assertions.

Before the fix, the [strict build](pre-fix-final-build.log) failed five
order-history checks. SQL/coverage were then run diagnostically against the
same stopped database:

```bash
./gradlew --offline --no-daemon --console=plain \
  :daytrader3-verification:coverageSummary -x restartTest -x stopAfterRestart
```

This [diagnostic command](pre-fix-final-sql-coverage.log) passed. It was not
evidence of a passing ordinary build. The fixed build subsequently executes
all these tasks through the normal lifecycle, without exclusions.

## Restart failure: diagnosed harness error

Before the fix, Full EJB account pages for accounts 4, 10, 11, 12, and 13
showed zero orders after restart, while SQL found all nine orders with expected
financial details. Cash and holdings survived. The initial
[failure](restart-history-failure.log), [SQL diagnosis](restart-sql-check.log),
[synthetic account page](restart-account.html), and
[final pre-fix JUnit XML](pre-fix-results/) are preserved.

The agent initially described this as a legacy defect and proposed asking for
review before characterizing the zero-order UI result. That diagnosis was
premature. The author asked whether to commit or fix first, then explicitly
requested diagnosis and a fix. No characterization change was approved or made;
there is no remaining assertion-review blocker.

Runtime evidence proved a harness configuration mismatch:

1. `TradeConfig.java:105` defaults the JVM-local `longRun` flag to `true`.
2. The HTTP setup posts `/config` without the `EnableLongRun` checkbox.
   `TradeConfigServlet.java:306-312` therefore disables the flag.
3. `TradeServletAction.java:80` deliberately supplies an empty order list when
   long-run mode is enabled, bypassing `getOrders` for benchmark efficiency.
4. The initial restart tests reapplied neither this flag nor their runtime
   profile. A new JVM restored the application's defaults, while the database
   correctly retained the orders.

Using the **ij-debugger** skill, two non-suspending IDEA logpoints on lines 80
and 82 recorded `longRun=true, user=test:4` and `orderCount=0` before any
configuration change ([events](debug-before-events.json),
[response](debug-account-before.html)). Posting the existing functional profile
on the same running server and database produced `longRun=false` and
`orderCount=1` ([events](debug-after-events.json),
[response](debug-account-after.html)). Both event drains reported no breakpoint
errors. Trailing whitespace in saved debug HTML is normalized for Git review;
page values and markup are retained. No debugger expression changed application state; the controlled change
used the application's existing configuration endpoint.

Fix: `RestartPersistenceTest` reapplies Full EJB synchronous configuration in
`@BeforeAll`, after the restart and before assertions. A comment in the legacy
client explains how an omitted checkbox disables long-run mode. No fixture is
reloaded, no expected value or assertion is changed, and no application Java
source or original server configuration is changed. The existing strict tests
are the regression checks for the corrected setup.

The diagnostic run used the existing synthetic DB, an ignored temporary Remote
JVM Debug configuration, and local-only JDWP port 17777. The first launch attempt
used an incorrect generated-options path and started without debugging; it was
corrected. The server was then run in a managed foreground session and IDEA
attached. The temporary config and both agent logpoints were removed, all six
pre-existing user breakpoints were retained, and the server/session stopped.
The ordinary build regenerates JVM options without JDWP.

## Coverage

[Source coverage summary](coverage-summary.json), [raw JaCoCo XML](coverage.xml),
and [matching class/exec inputs](coverage-inputs.tar.gz) are preserved. HTML can
be regenerated through the coverage task and is available locally under the
verification module's `build/reports/coverage/`. The agent includes application
packages only and appends both Liberty JVM lifetimes. Unit coverage is merged.

OpenJPA runtime enhancement initially caused class-mismatch warnings. The harness
now retains all original compiled classes (including uncovered code) and replaces
enhanced classes with agent-dumped runtime bytecode. Ambiguous variants fail the
report. The final report has no mismatch warning. Raw JaCoCo includes generated
persistence methods; the summary counts source lines and branches with line
metadata. Coverage is supporting evidence, not a pass threshold.

| Module/class | Lines | Line coverage | Source branches |
|---|---:|---:|---:|
| EJB module | 1384/2953 | 46.9% | 258/732 |
| Web module | 307/1732 | 17.7% | 84/343 |
| REST module | 22/99 | 22.2% | 0/10 |
| All application modules | 1713/4784 | 35.8% | 342/1085 |
| TradeSLSBBean | 225/357 | 63.0% | 53/122 |
| TradeDirect | 469/1147 | 40.9% | 81/238 |
| TradeAppServlet | 73/87 | 83.9% | 29/40 |
| TradeServletAction | 123/205 | 60.0% | 20/34 |
| FinancialUtils | 35/43 | 81.4% | 10/12 |
| DTBroker3MDB | 29/62 | 46.8% | 9/24 |

REST startup coverage does not imply a REST behavioral assertion. Many primitives,
error paths, and messaging branches remain unexercised. Source attachment excludes
generated methods without line information; it is not a general decompilation
filter. Changed architectures/providers can change coverage denominators.

## Harness failures, cleanup, and limitations

- An initial Groovy quoting failure was corrected
  ([log](initial-build-script-failure.log)).
- The first functional run passed, but its coverage had enhancement mismatch
  warnings ([log](first-functional-build.log)); it is superseded by the final
  passing report. [Bytecode diagnosis](coverage-bytecode-check.log).
- Coverage summary package matching initially mistook `/websphere` for `/web`.
  It now uses `/daytrader/web` and `/daytrader/rest`; final totals above use
  the corrected grouping.
- A rapid rerun's port probe rejected recently closed connections in TIME_WAIT
  ([failure](rapid-rerun-port-failure.log)). Enabling address reuse corrected
  the probe; the final preparation and deployment passed. The server lock is
  checked before test state is removed. A controlled active-listener probe
  confirmed preparation still fails before fixture reset; the expected-state
  file's SHA-256 remained unchanged ([log](active-port-probe.log)).
- The actual restart failure ran its shutdown finalizer. Deliberately selecting
  a nonexistent test also failed and stopped the test server
  ([cleanup probe](cleanup-selection-failure.log)). Finalizers cannot guarantee
  cleanup after forcibly terminating Gradle itself; explicit stop instructions
  are in the subject guide. The final test server was stopped.

Tests cover a useful trading slice, not exhaustive equivalence. Remaining work:
concurrency, broader rollback and failure injection, JMS redelivery/duplicate
handling, browser/JSF behavior, REST/address-book assertions, performance/resource
measurements, agreed tolerances, and a target migration contract. This harness
has not yet been ported to Jakarta EE 11. Gradle/runtime versions remain pinned.

Agent: Codex, model GPT-6 per session instructions; exact served model version,
usage, cost, elapsed effort, and human effort are unknown. Context included root
README/PLAN/AGENTS, the baseline plan, existing application sources and restoration
records, plus a previous-agent handoff summary. Tools: native shell/Gradle,
Python for artifact collection, file editing, and asynchronous assertion-review
question and IDEA debugger router/logpoints. Human input established the test
request, Gradle preference, primary Jakarta target, working agreements, and
request to diagnose/fix before committing. No assertion meaning was changed.

**Next action:** use coverage to select one bounded concurrency or
messaging-failure scenario with explicit financial invariants. Performance and
the migration contract remain open. The published harness and this evidence
preserve the failure and correction for later comparisons.
