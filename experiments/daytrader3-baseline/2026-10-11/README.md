# DayTrader baseline refresh before the tooling upgrade

Executed: 2026-10-11. Question: does the currently pinned, author-formatted
harness still pass under the existing Gradle/Liberty build setup? Stopping
condition: execute the ordinary build, retain named results and coverage, and
confirm the isolated server has stopped. No application or tooling upgrade is
part of this run.

Subject: `1c4342211ef627c433cfe3463f9905ded0833c9c` on
`tooling/baseline-tests`; superproject starting revision:
`40e1cc6ea5bab0449db162eb3f2e69749604168f`. Both working trees were clean
before execution. The subject remains unchanged afterward. The author formatted
the new harness code after the [previous passing baseline](../2026-10-10/README.md).
[Harness hashes](harness-sha256.txt) and [packaged artifact hashes](artifact-sha256.txt)
identify this snapshot.

## Environment and commands

[Environment](environment.txt): macOS/arm64, Gradle 4.10.3, Liberty plugin 2.4,
IBM Liberty 24.0.0.9 with the original Java EE 6 features, Derby 10.10.1.1,
JUnit Jupiter 5.10.3, Jsoup 1.17.2 and JaCoCo 0.8.12.

The installed Zulu Java 8 is now `1.8.0_504`, whereas the previous record reports
`1.8.0_282`. This is an observed environment change, not a JDK upgrade performed
by this run. [Runtime evidence](runtime-environment.txt) confirms Liberty used
`8u504`. This result therefore covers the formatted revision in the current
environment; it does not isolate formatting from the JDK patch-version change.

```bash
export JAVA_HOME=/Library/Java/JavaVirtualMachines/zulu-8.jdk/Contents/Home
export GRADLE_USER_HOME=/private/tmp/daytrader-gradle-inspection/user-home
./gradlew --offline --no-daemon --console=plain build
```

The initial restricted-sandbox attempt failed before project tasks ran
([log](sandbox-startup-failure.log)). A separate `help --stacktrace` diagnostic
identified `java.net.BindException: Operation not permitted` in Gradle's
cache-lock communicator ([diagnostic](startup-diagnostic.log)). Running the
same offline build with approved execution outside the sandbox passed; no
build-script changes were needed.

## Results

The [ordinary build](build.log) passed: 27 actionable tasks, 13 executed and
14 up-to-date. Fixture reset, HTTP, restart, stopped-database SQL verification
and coverage ran through the normal lifecycle. Compilation and packaging were
up-to-date: this was an incremental build, not a clean rebuild.

The eight unit cases were also up-to-date in that build. To obtain fresh unit
results on the current JDK, the following separate command passed
([unit log](unit-tests.log)):

```bash
./gradlew --offline --no-daemon --console=plain \
  :daytrader3-ee6-ejb:cleanTest :daytrader3-ee6-ejb:test
```

| Suite | Fresh passing cases |
|---|---:|
| Financial unit, separate refresh | 8 |
| Session HTTP | 8 |
| Trading HTTP | 7 |
| Restart HTTP | 12 |
| Stopped-database SQL | 9 |
| Total across both commands | 44 |

All failures, errors and skips are zero.
[Named JUnit XML](results/) and [machine-readable totals](test-summary.json)
retain the results. [Expected financial state](expected-state.properties)
comes from the existing independent scenario calculations.

[Coverage summary](coverage-summary.json) and [JaCoCo XML](coverage.xml):
1713/4784 source lines (35.8%) and 341/1085 source branches. The ordinary build
merged fresh server coverage with existing unit coverage before the separate
unit refresh. The previous report covered 342 branches. The single changed
branch is `TradeConfig.java:405`, the random sign choice for quote price changes;
this run exercised one outcome rather than both. No coverage mismatch warning
appeared. These are scoped coverage results, not an equivalence guarantee.

Both server lifetimes stopped successfully in the build log. A separate Liberty
`server status daytrader3_Baseline` check confirmed that the isolated server was
not running ([status](server-status.log)). No deliberate failure-cleanup probe
was repeated; earlier probes remain in the previous record.

## Outcome and limits

The existing suite passes at the current pin, providing a starting result for
the separate tooling upgrade. No source, assertions, wrapper, Liberty plugin,
runtime version or gitlink changed. No commit or push was performed. Concurrency,
broader messaging failures, performance, clean compilation on the current JDK,
IDEA execution of the suite and Jakarta EE 11 compatibility remain unverified
by this run.

Agent: Codex, GPT-6 per session instructions; exact served version, usage,
cost and human/agent elapsed effort are unknown. Tools: shell/Gradle, Python
artifact collection, file editing. Context: root working agreements and plan,
subject testing instructions and existing baseline evidence. Human contributions:
author formatting and instruction to execute the next plan action. No reference
target implementation or private material was consulted.

**Next action:** select and verify an exact Gradle/Liberty-plugin/build-JDK tuple
on a separate tooling branch from `1c43422`. Preserve explicit compiler, test
and server JVM choices, IBM Liberty and application behavior, then compare clean
packaging, named test results, coverage collection and cleanup against this record.
