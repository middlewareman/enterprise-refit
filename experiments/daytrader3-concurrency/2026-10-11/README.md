# Concurrent purchases expose a durable lost debit

Executed 2026-10-11 as the second author-assigned iteration. Input:
`a73e1ef8e6857677ae75c6fca03970abb9e76b2b`, the
[validated tooling upgrade](../../daytrader3-gradle-upgrade/2026-10-11/README.md).
Result: local subject commit `7a4b337a0a1e291f4815888f313ba345d9538a89`
on `tooling/concurrency-baseline`. The root milestone groups the pointer, evidence
and plan. No push was requested or performed. Application Java sources,
dependencies, IBM Liberty and server configuration remain unchanged.

**Outcome: the strict suite is red.** Two reset-fixture runs completed both
purchases and retained their orders/holdings, but persisted only one account
debit. SQL verified both runs; restart verified the first. The previous 44 cases
still pass across the HTTP, diagnostic restart/SQL and refreshed unit results.
The five added cases reveal this defect; assertions are retained, with no known
failure exclusion or application repair bundled into the harness change.

## Question and contract

Can Full EJB/synchronous trading preserve both financial effects when two
independent sessions buy different quotes for the same account? Use one bounded
scenario and reproduce a discovered mismatch on a second reset fixture; inspect
durability before classifying it. Stop after the result and cleanup are supported
by evidence. This is neither a load test nor a migration experiment.

Account 20 starts with 30000.00 and no orders/holdings. Two worker threads wait
at a common dispatch latch. Each owns a separate HTTP client/cookie manager and
authenticated session. Configuration is set once before dispatch. Each sends
one purchase, with bounded readiness, HTTP, result and executor-shutdown waits.
The recorded client request intervals must overlap. This does not force a
particular application transaction interleaving.

| Purchase | Shares | Fixture price | Value | Fee | Debit |
|---|---:|---:|---:|---:|---:|
| `s:20` | 2 | 70.00 | 140.00 | 24.95 | 164.95 |
| `s:21` | 3 | 71.00 | 213.00 | 24.95 | 237.95 |

Expected cash is **29597.10**, calculated before either operation. The test
requires successful responses, two unique completed buy orders and holdings,
correct symbols/quantities/execution prices/fees, and fresh-session cash/state.
Restart and stopped-DB checks use the same independent expected cash. SQL also
checks order-to-holding identities, ownership and completion dates.

Original SQL cardinality checks still require nine orders and one retained
holding; their queries exclude only the newly allocated account 20, which has
separate strict checks. Original expected values and assertion predicates are
retained. The suite now has 49 named cases: 8 unit, 16 HTTP, 14 restart and 11 SQL.
[Environment](environment.txt) is unchanged from the tooling iteration.
[IDEA formatting](formatting.txt) was applied to all four changed code files.
[Validated harness hashes](validated-harness-sha256.txt).

## Executed results

For all commands, set the same `JAVA_HOME` and `GRADLE_USER_HOME` as in the
environment record; use `--offline --no-daemon --console=plain`.

| Run/check | Result | Evidence |
|---|---|---|
| First corrected ordinary `build` | HTTP 15/16 pass; concurrent cash assertion fails. Unit cases up-to-date; restart/SQL do not run after failure. | [Build](build-2.log), [JUnit](run-1-results/), [expectations](run-1-expected-state.properties) |
| Stopped-DB diagnostic, same fixture | 10/11 pass; only account 20 cash fails. Both concurrent orders/holdings and their details pass. | [SQL command](run-1-sql-diagnostic.log), [JUnit](run-1-results/daytrader3-verification/persistedTest/) |
| Restart diagnostic, same fixture | 13/14 pass; only account 20 cash fails. Order history survives. Shutdown runs despite the assertion failure. | [Restart command](run-1-restart-diagnostic.log), [JUnit](run-1-results/daytrader3-verification/restartTest/) |
| Second reset `:daytrader3-ee6-ejb:cleanTest build` | All 8 unit cases execute/pass; HTTP 15/16 pass. Concurrent cash fails with the opposite debit missing. Later phases do not run. | [Build](build-3.log), [JUnit](run-2-results/), [expectations](run-2-expected-state.properties) |
| Stopped-DB diagnostic, second fixture | 10/11 pass; only account 20 cash fails. Concurrent order/holding details pass again. | [SQL command](run-2-sql-diagnostic.log), [JUnit](run-2-results/daytrader3-verification/persistedTest/) |

[Machine-readable suite results](test-summary.json) distinguish each run and
phase. The diagnostic commands were:

```bash
./gradlew --offline --no-daemon --console=plain \
  :daytrader3-verification:persistedTest -x restartTest
./gradlew --offline --no-daemon --console=plain \
  :daytrader3-verification:restartTest -x test
./gradlew --offline --no-daemon --console=plain \
  :daytrader3-verification:coverageSummary -x persistedTest -x restartTest -x test
```

Exclusions preserve the failed fixture for diagnosis; none of these commands
establishes a successful ordinary build. Only the coverage calculation passes
([log](run-1-coverage-diagnostic.log)). [Coverage](coverage-summary.json) and
[raw XML](coverage.xml) remain 1713/4784 source lines and 342/1085 branches,
merging the first corrected HTTP run, its restart and existing unit data.
The financial failure adds assurance value without adding covered source lines.

## Financial finding and attribution

[Observed balances and client intervals](financial-observations.json):

| Fixture | Actual persisted cash | Missing debit |
|---|---:|---:|
| First | 29835.05 | 237.95 (`s:21` value and fee) |
| Second | 29762.05 | 164.95 (`s:20` value and fee) |

Both observations match one purchase debit surviving while the other is lost.
This is a persisted financial mismatch, not merely stale HTML or a restart
configuration omission. Client intervals overlapped by approximately 19.8 ms and
17.5 ms. Those timings demonstrate client overlap, not performance or exact
database interleaving.

Source inspection supports a read/modify/write race hypothesis:
`TradeSLSBBean.buy` obtains the account, reads its balance and assigns a debit
using `account.setBalance(balance.subtract(total))`; the account's `@Version`
field is commented out. No explicit balance lock appears in that method. The
exact provider transaction interleaving was not traced, so this mechanism remains
a hypothesis rather than a debugger-proven root cause. The financial defect
itself is supported independently by HTTP, SQL, restart and the second fixture.
Concurrent JDBC and asynchronous profiles remain untested.

## Harness failures and corrections

The [initial build](build-1.log) failed because `awaitOrder` used the default,
unauthenticated observer. It could not see an otherwise completed order.
The fix assigns the authenticated first client to that helper. No financial
expectation was changed. [Initial results](initial-failure-results/),
[expected state](initial-failure-expected-state.properties) and
[formatted failed source](initial-failure-TradingContractTest.java.txt) retain
that failed attempt and its [hash](initial-failure-harness-sha256.txt).

The same failure exposed a lifecycle gap: a targeted test-selection probe passed
cleanup in the tooling iteration, but a failure in the full build skipped the
shared shutdown task and left the server running. An explicit native stop was
required ([transcribed observation](initial-cleanup-observation.txt)). Removing
shutdown from restart/SQL prerequisite edges and using `mustRunAfter` retains it
as a finalizer. Both corrected full-build failures and the restart failure then
ran shutdown. The final [status check](server-status.log) confirms no isolated
server remains running. Forced process termination still requires explicit stop.
Saved console logs normalize trailing whitespace, retaining values/diagnostics.

## Direction and next action

The two assigned iterations are committed independently; this second iteration
completes a bounded characterization experiment with a failing result, not a
green correctness baseline. Keep its strict regression scenario. Recommend a
separate baseline repair contract for the concurrent cash update, explicitly
recording the intended behavior correction, then verify the unchanged 49-case
suite and repeated concurrency scenarios. Author acceptance of an application
behavior change has not been inferred from the test result. Performance and
Jakarta transformation should follow that decision and repair evidence.

Agent: Codex/GPT-6 per session instructions; exact served model version, usage,
cost and human/agent effort are unknown. Tools: shell/Gradle, Python artifact
collection, IDEA patch/formatting MCP. Context: root working agreements/plan,
tooling and baseline evidence, subject tests and original trading source.
Human contributions: assignment of two iterations with commits and prior
formatting preference. No private material or reference target implementation
was consulted; no additional human intervention occurred during this iteration.
