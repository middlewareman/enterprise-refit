# Repair concurrent account updates before migration

## Step 1 — accepted scope and diagnosis

Author decision (2026-10-11): fix discovered defects and prepare for upgrade/migration,
using bounded documented steps and updating the plan after each step. This supersedes
the agent recommendation to carry the known lost debit into the first migration.

Input: `7a4b337a0a1e291f4815888f313ba345d9538a89`, on the author's fork.
Work branch: `repair/concurrent-account-updates`. Preserve the
[original failing experiment](../../daytrader3-concurrency/2026-10-11/README.md).

Repair contract: successful overlapping Full EJB purchases for the same account
must retain both debits exactly once, both completed orders and both holdings.
The same state must survive a fresh session, Liberty restart and independent SQL
inspection. Keep prices, fees, interfaces, schema, runtime and dependencies unchanged.
Serialize account mutations in the existing container transaction; handle the
corresponding sell and login/logout mutation paths consistently if source/runtime
evidence shows they share the same account row. Do not introduce retries, schema
version columns or a JVM-only lock. Failures must roll back rather than leave
partial financial effects. JDBC and asynchronous contention guarantees are outside
this bounded repair; their existing regression scenarios remain required.

Acceptance: unchanged 49-case suite passes from a freshly reset fixture, with
multiple fresh runs of the concurrent purchase scenario, correct cash `29597.10`,
orders/holdings and automatic shutdown. Add targeted integration assertions only
where needed to exercise the repair's account mutation/rollback boundary. Passing
repetitions are bounded evidence, not proof against every possible schedule.

Diagnosis questions: do both purchase transactions read `30000.00` before either
commits? Does locking an already-loaded account also require refreshing its state?
Can another account mutation overwrite a financial update? Use non-suspending IDEA
logpoints where feasible; distinguish observed values from source hypotheses.

Stopping condition: a focused repair with passing regression/durability evidence,
then a readiness review and concrete migration preparation. Avoid an open-ended
legacy defect hunt or unrelated dependency upgrades.

## Evidence and subsequent steps

Step 1 completed: non-suspending IDEA logpoints confirmed two distinct executor
threads both read `30000.00` before assigning `29835.05` and `29762.05`.
[Transcribed debugger events](debugger-observation.txt) distinguish the observed
stale read/write from the unobserved database commit order. The unchanged
[diagnostic test](diagnostic-test.log) failed its cash assertion. A temporary init
script first failed because it called `project()` on Gradle rather than
`gradle.rootProject`; [failure](diagnostic-init-failure.log) retained. No test ran
in that failed launch. Diagnostic shutdown was deliberately disabled to retain
IDEA events; native stop then succeeded. Agent logpoints and the temporary remote
configuration were removed; user breakpoints were untouched.

Step 2 implementation: `EntityManager.refresh(account, PESSIMISTIC_WRITE)` before
buy/sell/login/logout mutations. Refresh matters because the profile relationship
can already have loaded stale state; a lock on that stale object alone would not
express the required reread. The database lock lasts through the existing REQUIRED
container transaction. Optimistic versioning would require a schema change and
handling/retrying conflicts; JVM synchronization would not protect multiple server
processes. Neither was chosen. Account serialization may reduce same-account
throughput; performance remains to be measured. IDEA reformatted the changed bean
using project settings; unrelated formatting within that file is retained and
semantic diff reviewed. No test source changed for this first validation.

Agent: Codex/GPT-6 per session instructions; exact served model, usage, cost and
effort are unknown. No reference target implementation or private material consulted.

## Step 2 — verified repair outcome

Result subject commit: `f43c5f2ec403285a5d50fe9c2eaa2327618e8b3a`. No pushes performed in this task.

| Run | Executed result | Evidence |
|---|---|---|
| Clean shell build | 49/49 pass, zero failures/errors/skips; units fresh | [Log/results](build-1/) |
| Second reset shell build, `cleanTest build` | 49/49 pass, units fresh | [Log/results](build-2/) |
| IDEA **DayTrader Build** | 41 integration cases fresh, 8 units up-to-date from run 2; success | [Log/results](idea-build/) |

All three independent reset fixtures verify expected cash `29597.10`, two orders,
two holdings, client interval overlap, fresh-session state, restart and stopped-DB
SQL. The unchanged unknown-quote rollback check passes after acquiring the new
account lock. Every run executes both automatic shutdown tasks. Source-line
coverage is 1719/4790 (35.9%), branches 342/1085; denominators reflect the repair
and IDEA formatting. Coverage is supporting evidence, not completeness.

Commands run from the subject with the [recorded environment](environment.txt):

```bash
./gradlew --offline --no-daemon --console=plain \
  :daytrader3-ee6-ejb:clean :daytrader3-ee6-web:clean \
  :daytrader3-ee6-rest:clean :daytrader3-verification:clean build
./gradlew --offline --no-daemon --console=plain :daytrader3-ee6-ejb:cleanTest build
```

IDEA run configuration invokes `:daytrader3-ee6:build --console=plain` and its
existing local Gradle settings. It verifies IDE execution, not explicit reimport
or interactive startup. [Formatting](formatting.txt), [source hash](validated-source-sha256.txt).
A documentation update initially ran from the subject directory using root-relative
paths and failed before making changes; it was rerun from the root. A Markdown
IDE patch hunk also failed without changes and was replaced with an exact edit.
Neither failure altered the validated application or test assertions.

Remaining limits: no forced transaction schedule or lock-timeout/deadlock injection;
concurrent sells/login/logout and mixed JDBC/EJB contention are not independently
characterized. Sequential sell, session, JDBC and async regressions pass. The
original broader JMS reliability, JSF/browser and REST gaps remain. Native debugger
shutdown was used only for diagnosis; ordinary build cleanup remains automatic.

Next: collect a bounded uninstrumented local workload with business-state checks,
then write the first migration contract and explicitly distinguish readiness from
unexecuted migration/performance claims.
