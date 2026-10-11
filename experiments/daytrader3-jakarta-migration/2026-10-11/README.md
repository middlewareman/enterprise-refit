# Java 21 / Jakarta EE 11 migration — collaborative engineering case study

Author authorization: “Go ahead with the proposed migration.” Scope follows the
[contract](../../../docs/daytrader-jakarta-contract.md): Java 21, Open Liberty
26.0.0.9, Jakarta EE 11 / Persistence 3.2 with default EclipseLink; retain EAR,
HTML trading interface, embedded JMS and Derby/schema. Preserve the original 49
financial/session/unit/restart/SQL cases. No reference target implementation is
consulted; this is a collaborative case study, not an independently isolated agent
benchmark. Original source, restoration, tooling and repair remain separately pinned.

Input application: repaired `f43c5f2`. Before application transformation, add
representative external JSF/REST checks, run them against the legacy runtime,
and finish a bounded repeated performance baseline. Longer workload parameters:
100 warmup + 500 measured purchases per independent worker, three resets at one
and four workers, 20 ms think time; 256–512 MiB heap, coverage/debugging disabled.
This tests signed cash accounting rather than an overdraft policy. The workload
still does not represent a production mix or saturation campaign.

Performance assessment rule, defined before target results: all HTTP/SQL financial
checks must pass. Report per-run distributions; trigger investigation if target
median throughput is below 80% of baseline median or target median p95 exceeds
120% of baseline median p95. These are explicit local investigation thresholds,
not business SLA claims or permission to ignore failed financial assertions.
Report correctness and performance outcomes separately, as discussed with the author.

Steps: baseline enrichment/measurement; isolated namespace/API/descriptor/build
transformation; target deployment and strict regression/durability/concurrency;
matching workload comparison; IDEA execution, evidence review and coordinated
milestone commits. Update PLAN.md at each evidence-producing checkpoint. Record
failed attempts and actual test/adapter changes; never weaken assertions.

## Baseline enrichment checkpoint

Subject `d25398b` on `tooling/migration-contract-tests` adds three external
checks before transformation. `:daytrader3-ee6-ejb:cleanTest build` passes all
52 cases (8 unit, 19 HTTP, 14 restart, 11 SQL), with zero failures/errors/skips,
on Gradle 8.14.3 / Zulu 8u504 / IBM Liberty 24.0.0.9. The original 49 test
sources and assertions are unchanged. IDEA formatting was applied before commit.
[Build and JUnit evidence](baseline-tests/) records the result and coverage:
1752/4790 source lines and 348/1085 source branches. This is incremental
application compilation with fresh unit/integration executions.

The first new XML expectation was an unverified hypothesis and failed with
HTTP 415. Source inspection found `@Consumes` on GET and a separate
`List<MediaType>.contains(String)` comparison. The final new test characterizes
GET without Content-Type as 415, rather than claiming XML success. No existing
assertion or application source changed. The initial failure log is retained;
XML response correctness is a parked baseline defect, outside this migration.
JSF quote rendering/postback and REST JSON search passed.

Commands use `JAVA_HOME=/Library/Java/JavaVirtualMachines/zulu-8.jdk/Contents/Home`
and `GRADLE_USER_HOME=/private/tmp/daytrader-gradle-inspection/user-home`.
The isolated server stopped after both the failed and successful builds.
Longer workload execution completed; application transformation had not
started at this checkpoint.

 Model: Codex/GPT-6 per session; exact served model, usage,
cost and effort unknown. Tooling: shell/Gradle, IDEA patch/formatting, official
specification/provider documentation where needed. No private material consulted.

## Longer baseline workload

Six reset fixtures pass all HTTP and stopped-database financial checks. Each
worker makes 100 warmup and 500 measured purchases. Per-run measurement windows
are 15–18 seconds; this remains bounded local evidence, not steady-state or
production performance. [Raw results](baseline-workload/summary.json) and per-run
request/resource/GC logs are retained.

- 1 worker(s): median 29.12 purchases/s; median per-run p95 8.99 ms.
- 4 worker(s): median 129.12 purchases/s; median per-run p95 5.92 ms.

The workload manifest was captured at `f43c5f2` with test-only enrichment
pending; application source was unchanged throughout all runs. The frozen
[input manifest](input-manifest.json) pins enriched input `d25398b` and
workload hashes. No target results were inspected before these rules and
inputs were recorded.
