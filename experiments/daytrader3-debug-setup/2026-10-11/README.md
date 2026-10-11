# Reusable isolated DayTrader debug setup

## Question and result

Can the author and agent reuse named IDEA configurations to debug migrated
DayTrader without resetting interactive or acceptance data, changing frozen tests
or recreating temporary attach settings?

**Yes, within the checked scope.** Shared Start/Attach/Stop configurations and an
opt-in root Gradle adapter were created and formatted through IDEA. The final
adapter passes real IDEA startup/attachment, login/quote logpoint observation,
active-server refusal before any task execution, explicit Stop and automatic
failed-start cleanup. The stopping condition was these setup checks; further
migration/performance work remains paused.

[Usage guide](../../../docs/daytrader-debugging.md),
[init script](../../../harness/daytrader/debug.gradle) and
[shared configurations](../../../.run/).

## Inputs, environment and provenance

- Root starting revision: `9fe49e6a08116b54a8d33f22783f0976cc09b751`.
- Subject: `experiment/001/jakarta-ee11`,
  `6e6cfa787553e918e5c90edfd1e8882ce2c84d54`; unchanged and clean after checks.
- Gradle 8.14.3, Liberty plugin 3.10.0, Open Liberty 26.0.0.9;
  macOS, IntelliJ IDEA 2026.2.
- Server/application: stable Temurin 21.0.12.1+1 at
  `/Library/Java/JavaVirtualMachines/temurin-21.jdk/Contents/Home`.
  Native Gradle/fixture loader: Zulu 8u504 at
  `/Library/Java/JavaVirtualMachines/zulu-8.jdk/Contents/Home`.
  The author installed/registered Java 21 before this task.
- Agent: Codex/GPT-6 per session identity; exact served model, token/cost totals
  and effort unavailable. No delegated agents or GUI automation used.
- Tools: IDEA MCP patching, formatting, run configurations and JVM debugger via
  `mcp__idea__execute_tool`; native shell/Gradle, Python urllib/hashlib and Git
  inspection. The supplied local `ij-debugger` skill guided logpoints and cleanup;
  its provenance is recorded in [the IDEA account](../../../docs/idea-agent-workflow.md).
  Project instructions, build/fixture code and earlier experiment records supplied
  context. No private Theseus content or reference target implementations consulted.

The author authorized recommendation 2 from the IDEA account. Root-only tooling
keeps debug setup separate from subject acceptance logic. Existing uncommitted
reflection/JDK documentation and the already-staged IDEA document were preserved.
The author subsequently requested documentation and a local commit. This setup,
the IDEA account and stable-JDK follow-up form one root enablement milestone.
No subject commit, pointer update or push is required; root publication was not requested.
[Validation summary](validation-summary.json) pins the final implementation hashes.

## Executed evidence

| Check | Observed result | Artifact |
|---|---|---|
| Initial opt-in task discovery | Four public debug tasks listed; script compiled | Command below; initial console result was inspected, not separately saved |
| Final IDEA Start | Fresh 40-account/40-quote debug fixture, readiness/profile applied; build succeeds and server remains running | [Final Start log](idea-start-final.log) |
| Remote attach and HTTP exercise | Session running; login and quote HTTP 200 with expected text; non-suspending logpoint logs `debug-setup quote=s:0`, line 427, no breakpoint errors | [HTTP result](http-smoke.json), [drained event](debugger-event.json) |
| Active-server refusal | Exit 1 before any task runs; occupied HTTP 19084 identified; all 100 debug database file hashes unchanged | [Preflight log](preflight-refusal.log), [before](preflight-fixture-before.json), [after](preflight-fixture-after.json) |
| Explicit IDEA Stop | Build succeeds; `daytrader3_Debug stopped` | [Final Stop log](idea-stop-final.log) |
| Final failed-start cleanup | Deliberate exception after readiness gives expected exit 1; cleanup finalizer stops the debug server | [Probe script](failed-start-probe.gradle), [final probe log](failed-start-cleanup-final.log) |
| Ordinary Gradle invocation | No Debugging-group tasks without the init script; task listing succeeds | [Ordinary task log](ordinary-tasks.log) |
| Existing fixture preservation | Interactive 98 files and acceptance 100 files retain identical hashes across all checks | [Before](preserved-fixtures-before.json), [after](preserved-fixtures-after.json), [summary](validation-summary.json) |
| Source/test preservation | Subject working tree clean; all seven frozen test-source hashes match migration input | [Summary](validation-summary.json) |
| Final cleanup | Server status says not running (Liberty status exit 1); no debugger sessions or agent breakpoints; six user breakpoints remain, three enabled | [Server status](final-server-status.txt), [debugger cleanup](debugger-cleanup.json) |

The final server [messages](final-messages.log) identify the runtime and separate
debug user/output locations. The attach console log is empty; the drained debugger
event, not a console file, establishes probe execution. No full 52-case suite,
coverage or workload comparison was rerun for this task.
Raw logs are retained verbatim, including tool-emitted trailing spaces. Commit
review checks authored code/configuration/document whitespace separately from logs;
implementation hashes match the executed checks, XML parses and 84 local document
links resolve. IDEA formatting was applied before staging.

## Commands and tool calls

Native checks ran from the subject checkout with:

```bash
export JAVA_HOME=/Library/Java/JavaVirtualMachines/zulu-8.jdk/Contents/Home
export GRADLE_USER_HOME=/private/tmp/daytrader-gradle-inspection/user-home
workspace_root=/Users/middlewareman/Work/Migration
./gradlew --offline --no-daemon --console=plain \
  --init-script "$workspace_root/harness/daytrader/debug.gradle" \
  :daytrader3-verification:tasks --group Debugging
./gradlew --offline --no-daemon --console=plain \
  --init-script "$workspace_root/harness/daytrader/debug.gradle" \
  :daytrader3-verification:startDebugServer
./gradlew --offline --no-daemon --console=plain \
  --init-script "$workspace_root/harness/daytrader/debug.gradle" \
  --init-script /private/tmp/daytrader-debug-failed-start-probe.gradle \
  :daytrader3-verification:startDebugServer
./gradlew --offline --no-daemon --console=plain \
  :daytrader3-verification:tasks --group Debugging
```

The second command is the active-server refusal check; cleanup began only after
its completed failure was inspected. The probe adds an intentional failing
`doLast` action after the normal Start readiness/profile action.

IDEA router commands included:

```text
execute_run_configuration --configurationName 'DayTrader Debug Start' --timeout 1000 --waitForExit false
xdebug_set_breakpoint --filePath subjects/upstream/sample.daytrader3/daytrader3-ee6-ejb/src/main/java/com/ibm/websphere/samples/daytrader/ejb3/TradeSLSBBean.java --line 427 --logExpression '"debug-setup quote=" + symbol' --suspendPolicy NONE
xdebug_start_debugger_session --configurationName 'DayTrader Debug Attach' --timeout 1000 --graceWaitMs 1000
xdebug_control_session --action DRAIN_EVENTS --sessionId 'DayTrader Debug Attach'
xdebug_remove_breakpoint --owner agent
xdebug_control_session --action STOP --sessionId 'DayTrader Debug Attach'
execute_run_configuration --configurationName 'DayTrader Debug Stop' --timeout 1000 --waitForExit false
```

The HTTP probe used a Python urllib cookie client: POST `/daytrader/app` with
`action=login&uid=test:0&passwd=xxx`, then `action=quotes&symbols=s:0`.
Final Liberty status used the Java 21 home above and explicit `WLP_USER_DIR` /
`WLP_OUTPUT_DIR` pointing to the debug directories, with
`daytrader3-ee6/build/jakarta-runtime/wlp/bin/server status daytrader3_Debug`.

## Corrections and limits

The first active-reset check was invalid: the agent began cleanup while the
competing Gradle command was still running. That command subsequently succeeded
after the original server stopped, resetting the debug fixture.
[Excluded log](excluded-reset-check.log). The agent acknowledged the ordering
mistake and reran the check sequentially. The corrected original guard refused
reset and preserved database hashes: [log](active-reset-refusal.log).

Review then found that the reset guard ran after provisioning dependencies.
Switching between IDEA and native Gradle cache contexts had caused Liberty
installation work to rerun. The final adapter checks at task-graph readiness
before task dependencies and repeats the check before deletion; the final refusal
log demonstrates that no task executed. Initial
[Start](idea-start.log), [cleanup probe](failed-start-cleanup.log) and
[runtime log](cleanup-messages.log) remain earlier evidence, superseded by final
checks for the revised adapter.

Two router help attempts failed because the skill's help example did not work
with the exposed router. No session launched from them; provided tool schemas
supplied the argument definitions. All three shared configurations were recognized
and report `supportsDynamicLaunchOverrides=false`; named launch values worked
without overrides.

Isolation covers database, server identity, ports and output. The target runtime,
EAR and fixture classes are shared build products. Only the active-server refusal
path was exercised; separate forced lock-only and each occupied-port scenario were
not run. Failure cleanup was tested after readiness, not every possible startup
failure or forced termination. Fresh-clone setup, other operating systems and
Gradle configuration-cache behavior remain unverified. Existing Gradle deprecation
warnings are preserved in logs. Setup smoke checks establish a working debug
workflow, not broader functional equivalence or a performance explanation.
