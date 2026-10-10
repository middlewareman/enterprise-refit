# DayTrader: Gradle as the sole build — 2026-10-10

## Question, scope, and revision

The author requested removing Maven support before adding tests, so the new
verification suite only needs Gradle integration. Acceptance: no Maven project
build/CI/documentation path remains, and Gradle still produces the same application
contents and can deploy/start/stop the original runtime.

Work branch: `tooling/gradle-only`, created from restoration commit
`37a8facf9729f271160aabc02dcf312fff7e0fc9`. Tooling commit:
`0894dc9998d42fe8563169aabca479a63372d675`, published on the fork branch;
`git ls-remote` verified its tip. This milestone records its superproject gitlink. Original source
remains `a2d61af8c75c771fe4c9ad3f101bbdef08046c1a`. Application Java sources,
server configuration, dependency versions, Gradle 4.10.3, Liberty plugin 2.4,
Zulu Java 8 `1.8.0_282`, Derby 10.10.1.1, and IBM Liberty 24.0.0.9 are retained.

## Changes

- Remove the root and five module POMs, plus two stale Maven metadata files
  originally committed under the configured server's apps directory.
- Remove the unused Gradle `maven-publish` plugin and commented publication block.
- Change the inherited Travis configuration to one wrapper-based Gradle build
  with Java 8; do not claim a remote CI run.
- Make README, command-line, server, Eclipse/WDT, and download guidance use Gradle.
  Eclipse/WDT guidance remains historical and has not been revalidated.

Maven Central and Gradle's Maven repository declarations remain dependency-resolution
configuration. Existing LICENSE/NOTICE/DEPENDENCIES attribution remains intact,
including references to historical Maven coordinates. No new tests were added.

## Executed validation

Used disposable copies under `/private/tmp/daytrader-gradle-only-nujyx8h8`.
The before-copy came from `git archive` of restoration commit `37a8fac`; the
after-copy contained the edited tracked files, omitting deleted POMs/metadata.
Both used the installed Java 8 JDK and the existing dependency cache:

```bash
export JAVA_HOME=/Library/Java/JavaVirtualMachines/zulu-8.jdk/Contents/Home
export GRADLE_USER_HOME=/private/tmp/daytrader-gradle-inspection/user-home
# Before-copy:
./gradlew --offline --no-daemon --console=plain :daytrader3-ee6:ear :daytrader3-ee6:copyDerbyLib
# After-copy, with a copy of the installed pinned runtime at daytrader3-ee6/build/wlp:
./gradlew --offline --no-daemon --console=plain build
```

Saved logs have trailing whitespace normalized.

Before packaging passed ([output](before-package.log)). After compilation and
packaging passed during the first full-build attempt. Recursive archive-content
comparison found identical entry names and SHA-256 content hashes for the EAR,
EJB JAR, web WAR, and REST WAR ([comparison](artifact-comparison.json)). Archive
file hashes differ because ZIP metadata/timestamps differ. This is a content
comparison, not a claim of reproducible archive bytes.

The final full Gradle build passed with 14 actionable tasks, three executed and
11 up-to-date ([build output](after-build.log)). The isolated runtime used HTTP
19083, HTTPS 19443, JMS 17276, and JMS SSL 17286 in its temporary configuration;
no corresponding change was made to the subject's server.xml. The [server log](final-server.log)
confirms application deployment, HTTP/JMS binding, readiness, and shutdown. No
error/warning entries were found in this final log. All `test`/`fvt` tasks remained
`NO-SOURCE`; no trading, transaction, coverage, or performance assertions ran.

Review confirmed no remaining POM files or stale Maven properties, no changed
Java/server.xml sources, retained attribution, and no changes to the interactive
database. Documentation links and whitespace were checked.

## Failures and corrections

- The first sandboxed before-build failed to initialize Gradle services. Repeating
  with reviewed execution succeeded; no application change was needed.
- The external `libertyRoot` validation attempt failed in offline mode because
  plugin 2.4 attempted to obtain an uncached `index.yml`
  ([failure](external-runtime-offline-failure.log)). Used the existing pinned
  runtime copied into the default build path instead. Fresh runtime download and
  external-runtime behavior were not validated by this task.
- The first default-runtime build passed but logged a JMS bind error: isolating
  only HTTP/HTTPS left default JMS port 7276 in use by the interactive server
  ([build](first-build-jms-port-collision.log), [server](first-server-jms-port-collision.log)).
  Inspected the installed runtime's `wasJmsEndpoint` metatype, assigned separate
  JMS ports in the temporary configuration, and repeated the full build. The
  final run passed with clean startup/shutdown logs.

Agent/tool provenance: Codex; exact model identifier/token usage/total effort
unknown. Shell, Gradle, Python archive comparison, and installed runtime metatype
inspection; no subagents, reference migration implementations, or Theseus content.

## Next action

Implement deterministic fixtures and framework-independent trading tests
through Gradle `check`/`build`, as described in the [baseline plan](../../../docs/daytrader-baseline.md).
