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

## Transformation and deployment checkpoint

Selective enterprise namespace changes, Java 21 application toolchains, provided
Jakarta EE/JAXB APIs, Jakarta descriptors, CDI request-scoped Faces beans and
Jakarta Tags/Faces URIs compile/package. Java SE naming, SQL and XML stay unchanged.
Financial assertion source remains frozen. Target deployment attempts exposed:

- Combined IDE unified patch rejection; an accidental legacy-source/target-runtime
  launch followed before verification. Corrected using explicit per-file IDEA
  patch operations (74 succeeded), then inspected source and applied formatting.
- Jakarta EE 11 aggregate API excludes JAXB; explicit provided API4.0.2 added.
- Full EE11 ORB needs a basic registry; local sample registry added.
- Pages4 removes `isThreadSafe`; removed15 redundant true directives.
- Jakarta REST ignores the legacy GET consumes restriction with no request body;
  explicit415 guard preserves characterized GET-without-Content-Type behavior.
- Liberty plugin `libertyRoot` conflicts with plugin internal state; the supplied
  path was not used. Subsequent default install overlaid the ignored IBM runtime,
  yielding mixed metadata. Those attempts are invalid target evidence. Use
  `daytraderLibertyHome` for an existing runtime and a separate `jakarta-runtime`
  installation base for portable builds. Interactive user directory/data untouched.
- Clean pinned target deploys and passes JSF/REST/JDBC cases. Full EJB first failed
  on an `ArrayList` cast; `Collection` matches the declared service/JSP interface.
- After that correction, three unchanged EJB history cases failed.
  [Debugger observation](attempts/debugger-observation.txt) confirms two created
  orders but cached inverse collection size0, two holdings and cash29597.10.
  Configure portable shared-cache-mode NONE because JPA and JDBC both write
  the same schema. Both subsequent acceptance runs pass without changing tests.

[Failed attempts](attempts/) are preserved, including the offline artifact-cache
miss. Deprecation warnings remain; no optional Java syntax cleanup is included.

## Target acceptance checkpoint

Result subject commit: `6e6cfa7` on `experiment/001/jakarta-ee11`.
The [source manifest](target-source-manifest.json) pins its full revision,
reviewed changed-file hashes and workload-adapter hash. Acceptance runs and
workloads preceded this commit with those application changes pending; workload
environment records preserve that fact and the exact EAR hash. The adapter adds
runtime selection and artifact provenance; client workload and test assertions
retain their frozen source. Java token review confirms the only changes beyond
namespace substitution are the documented REST guard, collection handling and
Faces CDI conversions; formatting also changes whitespace/Javadoc layout.

Two shell builds pass all 52 frozen cases with zero failures/errors/skips:
[first target run](target-tests-1/) uses the clean probe installation;
[second target run](target-tests-2/) cleans EJB, web, REST and verification
modules and uses the default portable runtime installation. It executes 30 of
31 tasks. Each run includes a fresh unit execution and independent concurrent
purchase schedule, HTTP/session checks, restart and stopped-database SQL checks.
Expected concurrent cash remains 29597.10; both purchases/orders/holdings persist.
Failed target runs also exercised shutdown finalizers; successful runs stop both
server lifetimes. The legacy configuration module was not cleaned, protecting
the interactive database.

Shell environment: `JAVA_HOME=/private/tmp/daytrader-target-probe/java21/jdk-21.0.12.1+1/Contents/Home`,
`GRADLE_USER_HOME=/private/tmp/daytrader-gradle-inspection/user-home`.
The second build command is:

```bash
./gradlew --offline --no-daemon --console=plain \
  :daytrader3-ee6-ejb:clean :daytrader3-ee6-web:clean \
  :daytrader3-ee6-rest:clean :daytrader3-verification:clean build
```

[Artifact inspection](target-artifact-inspection.json) records all 77 application
classes at Java 21 major version 65, preserved EAR modules and no bundled nested
API/library jars. Target metadata contains only `openliberty.properties`.
The EAR SHA-256 is `bfe0e04d4e4f14e7b2bdd4c273e95413dcc9b9eb99e6fca8869f302198fb2166`.
All seven frozen test-source hashes match the input manifest; no assertion was
ported or weakened. Source coverage is 1741/4795 lines (36.3%) and 341/1087
branches (31.4%). Provider enhancement and changed source layout affect coverage
details; these percentages do not establish whole-application equivalence.

Actual IDEA formatting was applied to changed source/build/JSP files and the
workload adapter. The [IDEA build](target-idea-build/) executes 13 of 26 tasks;
44 HTTP/restart/SQL cases run freshly, while the eight unit cases remain up to
date from the passing shell build. It installs the target runtime, uses Java 21
for the application/server and stops the isolated server. Its Gradle JVM remains
Zulu 8: an explicit `-Porg.gradle.java.installations.paths` run-configuration
argument supplies the temporary Java 21 toolchain. GUI attempts to register/select
Java 21 did not change that setting; global SDK registration, reimport and
interactive target startup are unverified. GUI use stopped after the author
asked what it was doing. IDEA edits/formatting/debugging used MCP tools.

## Matching target workload and threshold investigation

All six target fixtures pass HTTP and SQL financial invariants. The client/fixture
tools remain on Java 8; the server uses pinned Java 21. The workload, counts,
think time, heap and instrumentation settings match the baseline.
[Raw target records](target-workload-2/) and [comparison/diagnostic values](workload-comparison.json)
preserve each run, rather than pooling request percentiles across fixtures.

| Workers | Baseline / target purchases/s | Target throughput ratio | Baseline / target median run p95 | Target p95 ratio |
|---|---|---|---|---|
| 1 | 29.12 / 27.66 | 95.0% | 8.99 / 11.05 ms | 122.9% |
| 4 | 129.12 / 120.73 | 93.5% | 5.92 / 9.57 ms | 161.6% |

Throughput remains above the predefined 80% threshold. Both p95 ratios exceed
120%, so performance acceptance is unresolved. The bounded investigation found:

- Second-half request p95 improves in every baseline and target run. Target
  values vary from 6.91 to 18.46 ms across complete runs; warmup/stabilization
  and workstation noise remain plausible contributors, not proven causes.
- Whole-server-lifetime GC pauses total 197–252 ms on target versus 382–462 ms
  on baseline; maximum pauses are 24–47 ms versus 96–107 ms. Defaults changed
  from Parallel GC to G1. These totals include startup/warmup/shutdown and clocks
  are not aligned to individual requests: they neither explain nor exclude GC
  contributions to measured tails.
- Median sampled peak RSS is 572944/577584 KiB at one worker
  (target/baseline), and 613824/588704 KiB at four.
  Samples cover startup and workload; CPU/RSS are process observations, not
  machine-wide utilization or a resource budget test.

The target measurement windows remain only 16–20 seconds. Shared caching is
disabled to preserve behavior and could add reads; JVM, server and provider
changed together. No isolated evidence attributes the latency gap to one change.
Do not tune away required correctness or relax thresholds. The recommended next
step is longer, alternating baseline/target measurements with stabilization and
aligned diagnostics before choosing an optimization. That is a separate bounded
performance iteration; functional migration evidence is ready to commit.

The first workload launch failed before server startup because `-D` was used for
Gradle toolchain discovery. The successful invocation uses the project property:

```bash
python3 harness/daytrader/run-workload.py \
  --subject subjects/upstream/sample.daytrader3 \
  --output experiments/daytrader3-jakarta-migration/2026-10-11/target-workload-2 \
  --java-home /Library/Java/JavaVirtualMachines/zulu-8.jdk/Contents/Home \
  --gradle-home /private/tmp/daytrader-gradle-inspection/user-home \
  --server-java-home /private/tmp/daytrader-target-probe/java21/jdk-21.0.12.1+1/Contents/Home \
  --runtime "$PWD/subjects/upstream/sample.daytrader3/daytrader3-ee6/build/jakarta-runtime/wlp" \
  --gradle-argument=-Porg.gradle.java.installations.paths=/private/tmp/daytrader-target-probe/java21/jdk-21.0.12.1+1/Contents/Home
```

[Failed launch records](target-workload/) retain text evidence; generated class
files were removed. The ignored old `build/wlp` installation has mixed product
metadata from an invalid attempt and must be replaced before any future legacy
baseline reuse. Accepted target runs use separate clean installations. Interactive
user/data directories were not reset.

Known gaps: broad JMS redelivery/failure behavior, concurrent sells and mixed
JDBC/EJB contention, complete JSF/browser/REST coverage, real-data compatibility,
interactive startup, CI's two-JDK setup and steady-state performance. No reference
implementation was consulted; no independent benchmark or production readiness
claim is made. The author selected the target and formatting/commit practice and
queried GUI use; the agent performed transformation, debugger diagnosis and checks.
Exact served model, token/cost totals and effort remain unavailable.

## Coordinated publication checkpoint

The later [knowledge/provenance reflection](../../../docs/daytrader-knowledge-provenance.md)
links recorded inputs, official guidance, skill/tool use, decisions and observations.
It distinguishes migration context from subsequent reference inspections and
enablement research; this retrospective documentation adds no executed acceptance
claim and leaves unavailable source/installation details explicit.

The author pushed the subject branch. Remote verification with
`git ls-remote origin refs/heads/experiment/001/jakarta-ee11` returns
`6e6cfa787553e918e5c90edfd1e8882ce2c84d54`, matching the local result and
source manifest. The root milestone records this fetchable gitlink together with
the migration evidence, documentation and workload adapter. Root publication
has not been requested. No new application tests were necessary for this
documentation/gitlink completion; staged document links, JSON and frozen hashes
were reviewed. Raw logs retain their original whitespace.
