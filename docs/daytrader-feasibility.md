# DayTrader 3: Gradle build and runtime feasibility

Inspected and checked: 2026-10-10. This is a feasibility assessment, not a migration or a validated runtime baseline.

## Recommendation and scope

Use **Gradle 4.10.3 with Java 8 first** to establish the original application's runtime baseline. Compilation and EAR packaging succeeded with that combination on this machine, without changing source or build scripts. A Gradle upgrade is therefore optional for buildability and should be recorded separately after startup and representative behavior are checked. The author requested getting DayTrader running and prefers Gradle; this sequencing is an agent recommendation, not an accepted upgrade decision.

The question was whether obtaining an older Gradle or upgrading the existing Gradle project is necessary. The stopping condition for this assessment was enough evidence to recommend a build path and identify the remaining runtime prerequisites. It did not include installing or starting an application server.

## Source and environment

- Subject: author-controlled [middlewareman/sample.daytrader3](https://github.com/middlewareman/sample.daytrader3), originally WASdev/sample.daytrader3.
- Original revision: `a2d61af8c75c771fe4c9ad3f101bbdef08046c1a` (2019-11-18, `Update TradeDirect.java`). The subject worktree remains clean on `master` at this pin; no work branch or changed gitlink was created.
- Checks used a disposable `git archive` of that revision at `/private/tmp/daytrader-gradle-inspection/source`, not the subject checkout. It is temporary storage, not a durable implementation checkout.
- Host: macOS 27.0.1, arm64. Build JDK: installed Zulu 8.52.0.23, OpenJDK `1.8.0_282-b08`, `/Library/Java/JavaVirtualMachines/zulu-8.jdk/Contents/Home`.
- Gradle 4.10.3 was downloaded from `https://services.gradle.org/distributions/gradle-4.10.3-bin.zip` into temporary storage. Its SHA-256 matched the official published checksum; see [artifact inspection](../experiments/daytrader3-feasibility/2026-10-10/artifact-inspection.txt).
- Homebrew has Gradle 9.8.1. With a writable temporary `GRADLE_USER_HOME`, `gradle --version` succeeded and reported Homebrew Java 27. The first invocation using the default user home failed to initialize native services; changing the user home resolved this probe. It was not an application build failure.
- Java 8, 11, 15, 17, and 22 appear in `/usr/libexec/java_home -V`. `command -v mvn` found no Maven executable. No global tool installation or default JDK setting was changed.

## What the existing Gradle build does

The [upstream command-line guide](../subjects/upstream/sample.daytrader3/docs/Using-cmd-line.md) says `gradle build`. The root build only applies the Eclipse plugin; five included projects implement the build:

| Project | Purpose |
|---|---|
| `daytrader3-ee6-ejb` | Java/EJB library named `dt-ejb.jar`; explicitly sets Java source compatibility to 1.7. |
| `daytrader3-ee6-web` | Web application named `web.war`; depends on the EJB archive as provided. |
| `daytrader3-ee6-rest` | JAX-RS web application named `Rest.war`. |
| `daytrader3-ee6` | Java EE 6 EAR named `daytrader3-ee6.ear`; Liberty tasks and Derby driver copying. |
| `daytrader3-ee6-wlpcfg` | Existing server configuration and a cleanup task that removes deployment/runtime data. |

There is no tracked Gradle wrapper or pinned Gradle version. `.travis.yml` requests OpenJDK 8, with separate Gradle and Maven build commands. The Liberty dependency is `net.wasdev.wlp.gradle.plugins:liberty-gradle-plugin:2.4`; [that plugin release's own wrapper](https://github.com/WASdev/ci.gradle/blob/liberty-gradle-plugin-2.4/gradle/wrapper/gradle-wrapper.properties) uses Gradle 4.3.1. Our choice of 4.10.3 is a tested compatible version, not a claim about the subject's exact historical toolchain.

Legacy usages include `compile`, `configurations.runtime`, `baseName`, `archiveName`, `archivePath`, and test-report `destination` properties. Gradle 4.10.3 itself reports deprecations incompatible with Gradle 5.0. Modern Gradle cannot be substituted without script/plugin adaptation.

`assemble` also installs the EAR through Liberty and copies Derby. `check` invokes `fvt`, which depends on application installation, server startup, and (without `libertyRoot`) feature installation, then stops the server. **The documented `gradle build` therefore includes runtime work.** The targeted packaging command below avoids these lifecycle hooks. Do not use `clean` casually against an established baseline: the server-configuration project deletes applications and database data.

## Executed checks and evidence

From the superproject, source was copied with:

```bash
mkdir -p /private/tmp/daytrader-gradle-inspection/source
git -C subjects/upstream/sample.daytrader3 archive a2d61af8c75c771fe4c9ad3f101bbdef08046c1a \
  | tar -x -C /private/tmp/daytrader-gradle-inspection/source
```

After downloading and extracting the Gradle distribution, these commands ran in the copied source:

```bash
export JAVA_HOME=/Library/Java/JavaVirtualMachines/zulu-8.jdk/Contents/Home
export GRADLE_USER_HOME=/private/tmp/daytrader-gradle-inspection/user-home
/private/tmp/daytrader-gradle-inspection/gradle-4.10.3/bin/gradle --no-daemon --console=plain help
/private/tmp/daytrader-gradle-inspection/gradle-4.10.3/bin/gradle --no-daemon --console=plain \
  :daytrader3-ee6:ear :daytrader3-ee6:copyDerbyLib
```

Both returned exit code 0. Public plugin and compile dependencies resolved successfully. Logs: [configuration](../experiments/daytrader3-feasibility/2026-10-10/gradle-4.10.3-help.log), [compilation and packaging](../experiments/daytrader3-feasibility/2026-10-10/gradle-4.10.3-package.log).

The generated EAR contains `dt-ejb.jar`, `web.war`, and `Rest.war`. Its supplied `META-INF/application.xml` retains Java EE version 6 and context roots `/daytrader` and `rest`. Class-header inspection found EJB major version 51 (Java 7; 28 classes) and web/REST major version 52 (Java 8; 43 and 6 application classes). Only EJB explicitly sets source compatibility, so the existing build does **not** uniformly target Java 7. The compiler warned about the Java 7 bootstrap classpath and unchecked operations. Archive hashes identify this run's outputs, not reproducible-byte guarantees.

No `src/test` or other test-source tree was found. The `fvt` task declaration and JMeter workload material do not establish executed application assertions. No full `build`, tests, Liberty install, deployment, startup, database initialization, UI/trading check, or Maven build was performed. Compilation and packaging do not establish preserved behavior.

Initial sandbox HTTP probes failed DNS resolution; the public downloads succeeded using reviewed network access. The first historical plugin documentation URL used `2.4` and returned HTTP 404; the POM's actual tag, `liberty-gradle-plugin-2.4`, succeeded. These were tooling/access corrections, not subject defects.

Agent/tool provenance: Codex (GPT-6), shell tools, Gradle 4.10.3, Python ZIP/class-header inspection. No subagents or reference target implementations were used. Model token usage, cost, and total human/agent effort are unknown. Gradle's logs report 6 seconds for configuration and 7 seconds for the packaging invocation; these are not performance measurements.

## Remaining steps to run the original application

1. On an explicit `restore/*` work branch, add a Gradle 4.10.3 wrapper with distribution checksum and document Java 8 selection. Keep application sources, enterprise APIs, and dependencies unchanged initially.
2. Choose and pin a **compatible Liberty distribution/version** and the runtime JVM. The supplied server requests `ejbLite-3.1`, `jsf-2.0`, `jaxrs-1.1`, `jpa-2.0`, `jmsMdb-3.1`, `wasJmsServer-1.0`, and `wasJmsClient-1.1`, plus Derby 10.10.1.1. Verify that the chosen distribution supplies this exact feature combination. A current server/version is not yet selected or validated.
3. Point the existing plugin at that installation with `-PlibertyRoot=/absolute/path/to/wlp`, or explicitly configure a pinned runtime artifact/download. Plugin 2.4's [installation documentation](https://github.com/WASdev/ci.gradle/blob/liberty-gradle-plugin-2.4/docs/installLiberty.md) defaults to the latest stable `webProfile6` runtime; the subject pins neither the server nor that download. Also check the historical `features.name = ['daytrader3_Sample']` installation mechanism. The server XML is the authoritative feature inventory: the upstream download guide instead describes Java EE 7 requirements and does not match it.
4. Deploy the EAR to `daytrader3-ee6-wlpcfg/servers/daytrader3_Sample/apps` and retain Derby in `shared/resources/Daytrader3_SampleDerbyLibs`. The existing packaging command already copies Derby; use the plugin/server tasks or documented server commands for deployment/startup after runtime selection. Record any restoration needed separately.
5. Follow the upstream sequence: set `WLP_USER_DIR` to `daytrader3-ee6-wlpcfg`, install required features, start `daytrader3_Sample`, open `http://localhost:9083/daytrader`, create tables/indexes, populate the database through the configuration page, and restart. Check server logs and actual deployment before treating startup as successful.
6. Validate login, quote lookup, buy, sell, and resulting order/portfolio state. Record selected JDBC/EJB and synchronous/asynchronous modes; exercise JMS completion where enabled. These remain proposed acceptance checks.

## What upgrading Gradle would require

| Route | Toolchain and work | Assessment |
|---|---|---|
| Original build first | Gradle 4.10.3 / Java 8; add wrapper and pin Liberty. | Compilation and packaging already verified. Recommended prerequisite for behavior comparisons. |
| Gradle 8.x | Select a pinned release and compatible Liberty plugin 3.x; update scripts/tasks and preserve compilation/runtime JDK choices. | Possible intermediate tooling scope; not tried and not needed to compile the current subject. |
| Installed Gradle 9.8.1 | Build JVM Java 17+; Liberty plugin 4.x; Java 8 compilation toolchain/runtime considered separately. | Larger build upgrade; not tried. Requires explicit separation of build JVM and application JVM. |

The [current Liberty plugin compatibility guidance](https://github.com/OpenLiberty/ci.gradle#compatibility--support), read on 2026-10-10, specifies plugin 3.8.2+ in the 3.x line for Gradle 7.6/8.x, and plugin 4.0.0+ for Gradle 9.x. [Gradle's Java matrix](https://docs.gradle.org/current/userguide/compatibility.html) permits running Gradle on Java 8 through 8.14.x; Gradle 9 requires Java 17+. These moving references inform planning, not reproduced upgrade results.

An upgrade would replace `compile`/`runtime` appropriately with `implementation`/`runtimeClasspath`, convert archive/report properties to modern APIs, review project artifact dependencies and EAR packaging, and adapt Liberty configuration and renamed tasks such as `installApps` to the selected plugin. Move the Derby copy to a dedicated driver dependency configuration instead of relying on all runtime dependencies. Preserve the observed mixed bytecode targets explicitly or record an intentional target change. Add a checksum-pinned wrapper and verify outputs, deployment, task ordering, and behavior against the original baseline. A plugin upgrade must also explicitly preserve the selected server distribution: newer plugin defaults use Open Liberty, which is not an automatic baseline-equivalent choice.

**Next concrete action:** select and verify a pinned Liberty runtime against the existing server features on a restoration branch, then attempt deployment/startup using the proven Gradle 4.10.3 / Java 8 build path.

## Restoration follow-up

The author accepted runtime restoration and requested IDEA setup first. The
[restoration record](../experiments/daytrader3-restoration/2026-10-10/README.md)
now records a Gradle 4.10.3 wrapper, successful IDEA import/full build with Java 8,
pinned IBM Liberty 24.0.0.9 startup, Derby initialization, and passing Full
EJB3/synchronous login, quote, buy/sell, and portfolio-persistence smoke checks.
Broader transactional coverage remains open. This follow-up does not turn the
earlier packaging-only assessment into an earlier runtime result.
