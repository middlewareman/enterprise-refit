# Isolated DayTrader debugging in IDEA

The shared configurations in [`.run/`](../.run/) start the migrated DayTrader on
its own disposable database, attach IDEA's JVM debugger and stop that server.
They use the existing deterministic fixture without changing the subject build
or acceptance tests. [Setup verification](../experiments/daytrader3-debug-setup/2026-10-11/README.md)
records the executed checks and limitations.

## Prerequisites

Open the **Migration root** in IDEA with the DayTrader Gradle project linked.
The subject must be initialized at the Jakarta migration revision (`6e6cfa7`
at verification). Keep Java 21 and Java 8 installed and discoverable by Gradle:
21 builds/runs the application, while 8 loads the inherited Derby fixture.
The verified installation uses Temurin 21.0.12.1+1 and Zulu 8u504. The existing
IDEA Gradle JVM can remain Java 8; the init script uses Gradle toolchains.
First use needs the normal Gradle dependencies and pinned Liberty archive,
either cached or downloadable.

IDEA should list **DayTrader Debug Start**, **DayTrader Debug Attach** and
**DayTrader Debug Stop** from the shared XML files. Their paths use
`$PROJECT_DIR$`; they do not contain workstation-specific JDK locations.

## Use it

1. **Run** `DayTrader Debug Start`. Wait for `Debug fixture ready` and a successful
   Gradle result. Start provisions the pinned target runtime if needed, builds the
   EAR and loads 40 accounts/quotes with zero holdings/orders. It applies the
   Full EJB/synchronous profile and leaves the server running.
2. Set a breakpoint or a non-suspending logpoint in the application source.
   For example, `TradeSLSBBean.getQuote` can log
   `"debug-setup quote=" + symbol` at its first statement.
3. **Debug** `DayTrader Debug Attach`. Open
   <http://127.0.0.1:19084/daytrader/>, log in as `test:0` with password `xxx`,
   and request quote `s:0` to exercise that method.
4. Detach/stop the debugger, then **Run** `DayTrader Debug Stop`.
   Disconnecting the remote debugger leaves Liberty running; Stop is explicit.
   Remove temporary probes when finished and preserve existing user breakpoints.

Every new Start resets only the debug fixture. Stop retains its database/logs
for inspection until the next Start. To run changed source, detach, Stop,
then repeat Start and Attach. Use a single debug server at a time.

## Isolation and lifecycle

| Resource | Debug configuration |
|---|---|
| Server | `daytrader3_Debug` |
| HTTP / HTTPS | `19084` / `19444` |
| JMS / JMS SSL | `17277` / `17287` |
| JDWP | `127.0.0.1:15005`, server mode, `suspend=n` |
| Heap | 256–512 MiB |
| User directory | `daytrader3-verification/build/debug-liberty-user` |
| Database | `debug-liberty-user/shared/resources/data/tradedb` |
| Output/logs | `daytrader3-verification/build/debug-liberty-output/daytrader3_Debug` |
| Fixture loader log | `daytrader3-verification/build/debug-derby-fixture.log` |

Paths in the table are relative to the subject checkout unless nested under the
user directory. The interactive database and acceptance fixture have separate
locations and are not reset by these tasks. The EAR, compiled fixture classes
and pinned target Liberty installation are reused; this is fixture isolation,
not a separate runtime installation. Avoid concurrent builds/provisioning of
that shared runtime while debugging.

Start checks the five ports and Liberty's server lock before executing task
dependencies, and checks again immediately before deleting debug storage.
An active server or occupied port aborts Start. A failure during the Start task,
including readiness/profile failure, runs a cleanup finalizer that stops only
the debug server. Forced process termination can bypass Gradle finalizers;
use Stop to clean up an interrupted launch. HTTP readiness waits at most
90 seconds; check `logs/messages.log` and `logs/console.log` under the debug
output directory when startup fails.

The server has JDWP enabled and no JaCoCo agent. Debugger probes can alter timing;
these runs do not count as performance or migration acceptance evidence.

## Shell equivalent and implementation

From the Migration root, with a supported Gradle JVM selected (Java 8 was used
for native verification):

```bash
workspace_root="$PWD"
cd subjects/upstream/sample.daytrader3
./gradlew --console=plain \
  --init-script "$workspace_root/harness/daytrader/debug.gradle" \
  :daytrader3-verification:startDebugServer
# Attach IDEA's named Remote JVM configuration, then stop it when finished.
./gradlew --console=plain \
  --init-script "$workspace_root/harness/daytrader/debug.gradle" \
  :daytrader3-verification:stopDebugServer
```

The opt-in [Gradle init script](../harness/daytrader/debug.gradle) registers the
debug tasks only when explicitly loaded. Ordinary subject builds have no debug
tasks. It reuses `baseline.DerbyFixture`, the existing server XML template,
EAR/features tasks and the `daytraderLibertyHome` runtime override.

Start/Stop are Gradle run configurations; Attach is a Remote JVM configuration.
They are deliberately separate named operations, so a debugger disconnect has
an explicit lifecycle meaning. All three report
`supportsDynamicLaunchOverrides=false` in the observed IDEA interface; launch
overrides are unnecessary. Changes to ports require updating both the init
script and Attach configuration. The script and XML were formatted by IDEA.
