# Bounded local trading measurement before migration

Input subject: `f43c5f2`, the separately verified account repair. Author requested
repair and preparation for migration in bounded documented steps. This measurement
answers whether a small reproducible uninstrumented workload can retain financial
invariants and provide local comparison data. Stop after three fresh runs each at
one and four independent-account workers; no saturation search or capacity claim.

Protocol: Full EJB synchronous purchases; one quote/account per worker (accounts
30–33); five warmup purchases and 20 measured purchases per worker, 20 ms think
time; all workers finish warmup before the measured window. One share per purchase;
quote read before each purchase supplies the expected execution price, and fees
remain 24.95. Warmup mutations stay in the fixture. Fresh sessions and stopped-DB
SQL check balances, order/holding counts, completion and links. No assertions are
removed. Timing samples cover buy HTTP responses including parsing; throughput
includes quote requests and think time. Auxiliary requests are not counted as
purchases. JIT/GC steady state is not guaranteed by this short warmup.

Java 8 runner/server; IBM Liberty 24.0.0.9, Derby 10.10.1.1; 256–512 MiB heap.
No JaCoCo/debugger. Reset only the verification fixture; ordinary tests and the
interactive server must not run concurrently. Runner has bounded request/worker/
subprocess/readiness timeouts and stops the server in a finally block. CPU/RSS
samples (100 ms), GC logs, HTTP readiness time, raw requests and SQL outcomes are
retained. Same laptop generates load and serves requests: results are local,
short-window observations, not production sizing or a benchmark speedup claim.

Implementation: [driver](../../../harness/daytrader/TradingWorkload.java) reuses the
pinned subject HTTP adapter without application imports; [orchestrator](../../../harness/daytrader/run-workload.py).
Both use IDEA project formatting. Runs are explicit and outside ordinary builds.

Command from the root:

```bash
python3 harness/daytrader/run-workload.py \
  --subject subjects/upstream/sample.daytrader3 \
  --output experiments/daytrader3-workload/2026-10-11/results \
  --java-home /Library/Java/JavaVirtualMachines/zulu-8.jdk/Contents/Home \
  --gradle-home /private/tmp/daytrader-gradle-inspection/user-home
```

## Executed outcome

Six reset runs pass HTTP/fresh-session and stopped-DB SQL business invariants.
375 total purchases (75 warmup, 300 measured) retain correct cash, completed
orders, holdings, quantities, fees and links. All six servers stop in finally; a final [native status check](final-server-status.log) confirms the isolated server is not running.
[Raw evidence and per-run summaries](results/), [console](console.log),
[GC summaries](gc-summary.json), [hardware](hardware.txt),
[input checksums](input-sha256.txt), [formatting](formatting.txt).

| Workers | Measured samples per run | Purchases/s across three runs | Buy response p95 across runs |
|---|---:|---:|---:|
| 1 | 20 | 23.75–24.10 | 14.22–14.64 ms |
| 4 | 80 | 91.61–93.93 | 19.79–22.54 ms |

Measured windows are only 0.83–0.87 seconds. These are **workload smoke measurements**,
not an established steady-state performance baseline or acceptance tolerance.
The fixed think time limits throughput; higher worker throughput does not imply
improved efficiency or capacity. Startup-to-HTTP-ready varies 5.41–11.79 seconds,
illustrating local variability. Sampled peak RSS is 520–569 MiB (includes native
JVM memory); ps CPU percentage can exceed 100% on multiple cores. CPU/RSS samples
span warmup, measured requests and final HTTP validation; ps CPU is a process
lifetime estimate, not instantaneous measured-window utilization. GC summaries
also cover the whole server lifetime. Short sample counts make p99 particularly
weak; no performance regression threshold is inferred.

No same-account contention, sells, async workload, representative workload mix,
saturation or sustained memory growth was measured. The earlier strict suite
separately checks same-account concurrent purchases. Quote prices randomize as in
the application, so request timing is repeatable by protocol, not identical data
or SQL across runs. A longer warmup/measurement protocol is required before
claiming a performance comparison; performance remains an open milestone item.
Hardware inspection was initially denied in the filesystem sandbox, then rerun
successfully with approved execution access. This did not affect workload execution.

Next: finalize/check the target-platform preparation contract and then undertake
bounded compatibility migration, reporting correctness separately from incomplete
performance comparison. Whether sustained performance is a hard migration gate
remains a project decision; this step does not silently declare it completed.

Agent: Codex/GPT-6 per session; exact served version, usage, cost and effort unknown.
No reference target implementation or private material consulted.
