# DayTrader restoration and IDEA setup — 2026-10-10

## Question and acceptance evidence

Can the pinned legacy DayTrader source be built in the author's running IDEA and
started with its original Java EE 6 feature configuration? The author accepted
the runtime-restoration recommendation and requested IDEA setup first.

Build acceptance: IDEA recognizes the Gradle modules, uses Java 8 and the checked-in
Gradle 4.10.3 wrapper, and completes compilation and EAR packaging. Runtime
acceptance: Liberty starts the EAR, Derby tables/data are initialized, and login,
quotes, synchronous purchase/sale, and portfolio persistence are checked. A passing
smoke check is a first runtime baseline, not equivalence across all application modes.

## Revisions and environment

- Original source:
  `a2d61af8c75c771fe4c9ad3f101bbdef08046c1a`.
- Restoration commit: `37a8facf9729f271160aabc02dcf312fff7e0fc9` on `restore/runtime`, created from that source.
  The fork's `master` is unchanged. The prior superproject setup/feasibility
  commit is `892d2bc`.
- Publication/gitlink status: the restoration commit is local. Automatic approval
  review rejected its push because the commit request did not explicitly authorize
  remote publication. Push approval is pending; the superproject gitlink retains
  the original source revision until the fork commit is fetchable.
- macOS / Apple Silicon; Zulu Java `1.8.0_282`, aarch64, installed before this work.
- Gradle 4.10.3; Liberty Gradle plugin 2.4 retained.
- IDEA 2026.2.3; IDEA's own runtime remains independent of the Gradle/project SDK.
- Candidate runtime: IBM Liberty `24.0.0.9`, artifact
  `com.ibm.websphere.appserver.runtime:wlp-javaee7:24.0.0.9@zip`.
  The distribution README states Java 8, 11, or 17. Its Java EE 7 packaging does
  not change the server's requested Java EE 6 feature versions.
- Agent: Codex (GPT-6 family); exact model identifier, token usage, and total effort
  unavailable. Tools: shell, IDEA MCP connector, and unified computer use. Project
  instructions and README/PLAN were loaded explicitly; no migration/reference
  implementation or held-out tests were consulted.

## Executed build evidence

The wrapper was generated with Gradle 4.10.3. Its distribution checksum is
`8626cbf206b4e201ade7b87779090690447054bc93f052954c78480fa6ed186e`.

From the subject root, with `JAVA_HOME` set to the installed Java 8 JDK and
`GRADLE_USER_HOME=/private/tmp/daytrader-gradle-inspection/user-home`:

```bash
./gradlew --no-daemon --console=plain :daytrader3-ee6:ear :daytrader3-ee6:copyDerbyLib
```

Exit 0, ten executed tasks, including EJB/web/REST compilation and EAR packaging.
The EJB Java 7 bootstrap-classpath warning and deprecated Gradle API warning remain.

IDEA's initial import failed because it selected a Java 27 Gradle JVM, incompatible
with Gradle 4.10.3. Registered the installed Zulu Java 8 SDK, selected it for the
project and linked Gradle build, selected the wrapper/delegated build, and removed
the stale link to the former checkout path. These settings are ignored local IDEA
configuration; backups are in temporary storage. No machine SDK path is committed.

Automatic approval review initially rejected **Reload All from Disk** because
unsaved editor changes had not been ruled out. Executed **Save All** before
retrying the reload. SDK registration through the UI was unsuccessful; updating
IDEA's SDK table with a backup and then reloading succeeded. Some UI calls failed
because focus/state changed; fresh observations and connector checks resolved this.

The IDEA log then explicitly selected the Zulu Java 8 home. The connector returned
the root DayTrader module, all five submodules, and source-set Java modules. Delegated
IDEA compilation (`web:classes`, `rest:classes`, and EJB dependency) passed.
The local **DayTrader Package** run configuration executed the two packaging tasks
above, exited 0, and reported ten up-to-date tasks. [IDEA packaging output](idea-package.log).
IDEA warns that support for this Gradle version is deprecated and scheduled for
removal; a newer build-tool experiment remains separate.

## Runtime selection and restoration

Open Liberty `24.0.0.9` was downloaded and inspected. Its archive lacks the requested
`ejbLite-3.1`, `jsf-2.0`, `jaxrs-1.1`, `jpa-2.0`, `jmsMdb-3.1`, and
`wasJmsClient-1.1` manifests. It was not used to run DayTrader. SHA-256:
`a598ac580cbbdddaa7f77f7d6bfd1d78614555bcc4839db3d3f1aed9c8265db5`.

IBM Liberty's Java EE 7 archive also needs these older features installed separately.
The pinned artifact's SHA-256 is
`7a40ec35db2eb3fb7c2bc24263ac572013e380b47508360f1c540e1e56a25bbc`;
its SHA-1 matched Maven Central's header
`3042158336a94bf89fd0921263d42cb446127098`.
Downloaded artifacts came from Maven Central over HTTPS.

In a temporary runtime, the following command completed with exit 0. Feature
signatures and the resulting product were validated by the utility:

```bash
JAVA_HOME=<Java 8 JDK> wlp/bin/featureUtility installFeature \
  ejbLite-3.1 jsf-2.0 jaxrs-1.1 jpa-2.0 jmsMdb-3.1 wasJmsClient-1.1
```

No license-acceptance flag or interactive acceptance was supplied. The utility
installed a broader dependency set, including other enterprise feature versions;
only server.xml's original requested features will be enabled. First installation
was substantially slower than compilation. This is not a platform upgrade result.

The Gradle runtime dependency is pinned. A new `installDayTraderFeatures` task uses
the runtime's feature utility with all seven original requested features, replacing
the obsolete sample-asset installation hook. `libertyStart` depends on that task,
EAR installation, and Derby library copying. It skips feature installation when
all seven manifests already exist. An external `libertyRoot` requires a compatible
installation with `featureUtility`. Generated deployment/server/data files are ignored.

`./gradlew :daytrader3-ee6:installLiberty` returned exit 0 and installed the pinned
runtime into `daytrader3-ee6/build/wlp`. `./gradlew :daytrader3-ee6:libertyStart` returned exit 0 after feature and product
validation, deployed the EAR, and reported server readiness. [Startup output](gradle-runtime-start.log), with ANSI formatting and trailing whitespace normalized.
The shell-started background server was no longer running after the command session
ended; the first HTTP attempt failed with connection refused ([failure](initial-http-failure.log)).
The precise process-termination cause was not established. Running **DayTrader Start**
through IDEA then returned exit 0 and left a reachable server running. [IDEA start](idea-start.log).
The feature task's installed-manifest check skipped repeat feature resolution.

## Executed runtime and full build checks

The local database was initially new. Commands below are relative to the
superproject root; each HTTP command returned exit 0 except the recorded initial
login-assertion failure. Stop/start operations used the corresponding IDEA Gradle
run configurations and returned exit 0.

```bash
python3 experiments/daytrader3-restoration/2026-10-10/runtime-smoke.py --create-tables
# IDEA: DayTrader Stop, then DayTrader Start
python3 experiments/daytrader3-restoration/2026-10-10/runtime-smoke.py --populate
# IDEA: DayTrader Build, then DayTrader Start
python3 experiments/daytrader3-restoration/2026-10-10/runtime-smoke.py
```

[Table creation](create-tables.log) detected Apache Derby and confirmed success.
[Population](populate.log) reported 100 quotes and ten users. The application
randomizes their contents and initial holdings; the fixture is bounded but not
seed-deterministic. The account used was the synthetic sample `uid:0` / `xxx`.

**DayTrader Build** ran `:daytrader3-ee6:build` inside IDEA and exited 0; fourteen
tracked tasks, three executed and eleven up-to-date. `test` and `fvt` were explicitly
`NO-SOURCE`. The inherited `fvt` finalizer stopped the running server, so it was
started again before the smoke check. [Full IDEA build](idea-build.log).

The first smoke attempt successfully logged in but failed a harness assertion:
the servlet sets "Ready to Trade", while the JSP renders "Welcome uid:0," and
the cash balance. Corrected the assertion to check the rendered authenticated
account identity and summary; no application code or evaluation expectation was
changed. [Initial assertion](initial-smoke-assertion.log).

The subsequent [smoke check](smoke.log) returned exit 0 in Full EJB3/synchronous mode:
login, quote `s:0`, purchase of two shares, one new holding (`1000`), persistence
across logout/login, sale of that holding, and the original holding set after
another logout/login. Holdings changed **5 → 6 → 5**. Buy order `1000` and sell
order `1001` both had status `closed`. These are rendered application observations;
no independent SQL/account-balance assertion was executed.

[Server readiness](server-readiness.log) confirms the EAR started, the original
Java EE 6 feature set was active, and both MDB endpoints were activated. Activation
alone is not an asynchronous transaction check. No error/warning entries were
found in the inspected final-start `messages.log`. The server is left running
at `http://localhost:9083/daytrader` from IDEA.

Reusable subject instructions: [IDEA setup](../../../subjects/upstream/sample.daytrader3/docs/Using-IDEA.md)
and [runtime/database setup](../../../subjects/upstream/sample.daytrader3/docs/Restored-runtime.md).

## Final output/state correction

Final Git review found that upstream tracks generated `derby.log`, messaging-store,
and transaction-log files; the initial start changed them. Stopped the server,
backed up that runtime state in temporary storage, and restored only those tracked
files. Configured `liberty.outputDir` under ignored `daytrader3-ee6/build/liberty-output`.
The Derby database remains at the original shared-resource path. The application
started with the new output directory, and [the repeated smoke check](final-smoke.log)
passed again: holdings 5 → 6 → 5, new holding/buy order `2000`, sell order `2001`,
both orders `closed`. This repeat was justified by the output/state relocation.
[The final full IDEA build](final-idea-build.log) and [restart](final-idea-start.log)
also returned exit 0. Final HTTP readiness was 200; no error/warning entries were
found in that final-start log. Git review confirms generated tracked state is restored;
only intentional wrapper/build/docs/ignore changes remain in the subject.

## Gaps

No migration or Gradle/plugin upgrade. Application sources and server feature
versions remain unchanged. No discovered unit/functional tests; the inherited
`fvt` lifecycle does not establish behavioral coverage. The executed assertions are in [runtime-smoke.py](runtime-smoke.py); their scope
is limited to the recorded Full EJB3/synchronous workflow.
Asynchronous processing, rollback, concurrent access, REST, JSF, monetary-state
assertions, and performance remain outside this first check.
