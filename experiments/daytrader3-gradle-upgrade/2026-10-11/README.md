# Gradle/Liberty tooling upgrade

Executed 2026-10-11 as the first of two author-assigned iterations. Contract:
upgrade build tooling while preserving application source, dependencies, IBM
Liberty 24.0.0.9/Java EE 6, Java 8 execution, application bytecode and all existing
assertions. Stop after clean compilation, packaging comparison, the unchanged
suite, coverage and a failure-cleanup probe pass. Application modernization and
performance are outside this iteration.

Input: `1c4342211ef627c433cfe3463f9905ded0833c9c`. Result:
`a73e1ef8e6857677ae75c6fca03970abb9e76b2b` on `tooling/gradle-8.14.3`.
The subject commit and root milestone are local; publication was not requested.
The root commit groups this evidence, plan and pointer instead of mirroring
intermediate edits. Saved console logs normalize trailing whitespace; output
values and diagnostics are retained. [Validated snapshot hashes](validated-snapshot-sha256.txt).

## Selection and implementation

Gradle 8.14.3 / Liberty plugin 3.10.0 is compatible with the installed Java 8
according to the fetched [compatibility snapshot](compatibility-source.txt).
[Maven version metadata](liberty-plugin-versions.xml) confirms the plugin release;
the wrapper pins the [official distribution checksum](distribution-sha256.txt).
This deliberately avoids introducing a newer daemon JVM in the same iteration.
[Environment](environment.txt): Zulu 8u504, macOS/arm64. JVM patch level is the
same in the before and after runs.

Updated dependency configurations, archive and JaCoCo report APIs, modern
`deploy` task/configuration, Liberty user/output directory placement and the
generated wrapper. Derby copying now resolves only a dedicated driver
configuration. IBM runtime coordinates remain explicit, avoiding the plugin's
Open Liberty default. The compiler/test/isolated-server toolchain is Java 8.
EJB application output remains Java 7; web/REST output remains Java 8.
JUnit 5 dependencies and assertions are unchanged. The Platform launcher 1.10.3
is now explicit, and EJB test compilation/dependency attributes target Java 8.

IDEA formatting was applied to all six changed build scripts, using the root
project's style. [Formatting record](formatting.txt). Generated wrapper scripts
and JAR are official Gradle task output. Subject guides now describe the current
wrapper and safe recompilation commands.

## Executed validation

Before and after, set:

```bash
export JAVA_HOME=/Library/Java/JavaVirtualMachines/zulu-8.jdk/Contents/Home
export GRADLE_USER_HOME=/private/tmp/daytrader-gradle-inspection/user-home
./gradlew --no-daemon --console=plain \
  :daytrader3-ee6-ejb:clean :daytrader3-ee6-web:clean \
  :daytrader3-ee6-rest:clean :daytrader3-verification:clean build
```

The before command also used `--offline`; the after command used
`--warning-mode all` and could resolve new tooling dependencies. Cleaning excludes
the installed runtime and the interactive configuration module/database.

- [Before clean build](before-build.log): 44 cases pass, 29 tasks executed.
- [Final after clean build](after-build-fixed.log): 44 cases pass, 29 tasks
  executed. [Before XML](before-results/), [after XML](after-results/), and
  [after totals](after-test-summary.json) retain named results. No failures,
  errors or skips; no assertion or application Java source changed.
- [Packaging comparison](packaging-comparison.json): all 452 expanded EAR,
  nested JAR/WAR, class and resource entries have identical SHA-256 content;
  no additions, removals or changes. This compares entry bytes, not whole ZIP
  timestamps/compression. [Before](before-bytecode.json) and
  [after](after-bytecode.json) retain 28 EJB classes at major 51 and 49 web/REST
  classes at major 52. The comparison used the freshly recompiled old build.
- [Coverage](coverage-summary.json), [raw XML](coverage.xml): 1713/4784 source
  lines and 342/1085 branches, matching the clean before run.
- An intentionally unmatched `--tests baseline.NonexistentCleanupProbe` selection
  failed, and Gradle ran shutdown ([probe](cleanup-failure-probe.log)). A separate
  [status check](server-status.log) confirmed the test server was stopped.
- `:daytrader3-ee6:libertyStart --dry-run` resolves the renamed deployment graph
  successfully ([log](interactive-start-dry-run.log)). The interactive startup
  path was not executed; the ordinary suite exercised runtime installation and
  direct isolated-server startup twice. IDEA reimport/execution remains untested.

## Failures and limitations

Two wrapper-generation attempts failed on removed archive APIs
([first](wrapper-upgrade.log), [second](wrapper-upgrade-fixed.log)). External
edits were replaced by stale open documents when IDEA formatted EJB/web/REST
build files. Applying the corrections through IDEA's patch API and reformatting
resolved that integration issue; [wrapper generation](wrapper-upgrade-final.log)
then passed. This is a workflow failure, not an application defect.

The [first upgraded build](after-build.log) failed before tests because Gradle's
variant checks rejected Java 8 JUnit on a Java 7 test classpath. Explicit Java 8
test compilation/attributes fixed it without changing application targets or
test source. Test bytecode is intentionally raised from Java 7 to Java 8.

Warnings remain for a Java 8 Gradle daemon (Gradle 9 needs Java 17+), plugin
project-dependency access, and execution-time project access in plugin/harness
tasks. Configuration-cache compatibility and Gradle 9 are not established.
These do not prevent the selected Gradle 8.14.3 build. No performance, concurrency
or new messaging-failure guarantee is claimed by this iteration.

Agent: Codex/GPT-6 per session instructions; exact served version, usage, cost
and human/agent effort are unknown. Tools: shell/Gradle, public compatibility
downloads, Python comparisons/artifact collection, IDEA patch/formatting MCP.
Context: root working agreements, plan, baseline evidence, subject guides and
build scripts. Human contribution: assigned two independent iterations with
commits and required IDEA formatting. No private material or reference target
implementation was consulted; no additional human intervention was required.

**Next action:** bounded same-account concurrent purchases through two independent
sessions, checking both debits/fees, order/holding identities and durable state.
