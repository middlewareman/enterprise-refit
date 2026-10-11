# How the agent used IntelliJ IDEA in DayTrader

Recorded 2026-10-11 during the author's reflection pause, following migration
subject `6e6cfa7` and root evidence `0da7a65`. This describes observed use in this
workspace, with alternatives and recommendations labeled separately. It is not
a claim that every available IDEA feature was used or that IDEA performed the
migration decisions itself.

IDEA contributed existing engineering capabilities: project formatting,
editor-aware patching, Gradle run configurations and JVM debugging. The agent
selected operations and interpreted results; IDEA executed them. Most of this
interaction used structured tools rather than mouse/keyboard automation.

## Tools, skills and GUI actions

The integration exposed tools named `mcp__idea__...` with argument schemas and
descriptions. MCP (Model Context Protocol) supplies an interface through which
the agent can request operations from IDEA and receive structured results or
text. A request can name a file or run configuration without locating it visually.
The tool definitions describe available operations; success still needs checking
against resulting files, logs or debugger events.

Three mechanisms need distinguishing:

| Mechanism | What it supplies | Use in this work |
|---|---|---|
| IDEA tool | An executable operation with parameters and results | Apply a patch, reformat named files, execute a run configuration, inspect debugger state |
| Skill | Written instructions the agent reads and follows | `ij-debugger` specifies a debugger workflow, tool routing and evidence/cleanup rules |
| GUI automation | Screenshots and mouse/keyboard actions on the visible application | Attempt to register the temporary Java 21 JDK and select the Gradle JVM |

A skill does not execute the debugger or install a capability. It guides tool
choice and use. The tools must already be available. The migration's patching and
formatting operations used tool descriptions and project instructions; the
recorded specialized IDEA skill was `ij-debugger`.

For debugger and run-configuration operations, that skill directs calls through
the universal `mcp__idea__execute_tool` router. For example, the recorded migration
build used this command:

```text
execute_run_configuration --configurationName 'DayTrader Build' --timeout 1000 --waitForExit false
```

The router invokes the IDEA operation and returns its result, including the log
location in this case. It does not turn the command into an ordinary shell
command. The shell remained a separate tool for Gradle runs, Git, fixture/workload
orchestration and artifact analysis.

## Formatting: delegate the existing formatter

The agent called `mcp__idea__reformat_file` with a list of project-relative files.
The following illustrates the request shape, using a file formatted during the
migration; it is not a new formatting action performed for this document:

```json
{
  "files": [
    "subjects/upstream/sample.daytrader3/daytrader3-ee6-ejb/src/main/java/com/ibm/websphere/samples/daytrader/ejb3/TradeSLSBBean.java"
  ]
}
```

IDEA applies the formatter and the effective project settings. The root repository
tracks [Project.xml](../.idea/codeStyles/Project.xml) and
[codeStyleConfig.xml](../.idea/codeStyles/codeStyleConfig.xml); the latter enables
per-project settings. The recorded style includes Java/Groovy right margin 160,
Java brace spacing and Groovy parameter alignment. Unspecified choices still
depend on IDEA's formatter/defaults, so the style files do not fully pin every
formatting behavior across IDE versions.

This is easier and more reliable than having the model generate approximate
spacing and line breaks. The formatter understands the supported language's
syntax and applies the project's conventions consistently. No model generation
is needed for each indentation decision. The agent still reviews the diff:
formatting a changed file can also reflow comments and untouched portions of
that file, increasing review size. Formatting is not behavioral validation.

The [tooling upgrade formatting record](../experiments/daytrader3-gradle-upgrade/2026-10-11/formatting.txt)
confirms the six changed Gradle scripts were formatted with the root style.
The [account repair](../experiments/daytrader3-account-repair/2026-10-11/README.md)
records formatting the changed bean. The [migration record](../experiments/daytrader3-jakarta-migration/2026-10-11/README.md)
records formatting changed source/build/JSP files and the workload adapter before
code commits. The author's requirement made this an explicit acceptance step.

Without the live integration, an alternative would be IDEA's command-line
formatter where available, or having the author invoke Reformat Code. A different
formatter would require an explicit style choice; it would not establish IDEA
formatting. Manual approximation would not satisfy the agreement. Generated
Gradle wrapper files remained official task output rather than hand-formatted code.

## Editing: keep IDEA's document state involved

The agent supplied explicit patches to `mcp__idea__apply_patch`. This applies the
requested text changes through the IDE integration. It is a patch tool, not a
semantic Java migration or rename operation: the agent remained responsible for
selective enterprise namespace changes and preserving Java SE `javax` packages.

There was a concrete reason to use it. During the Gradle upgrade, external edits
to open EJB/web/REST build files were replaced by stale editor documents when
IDEA formatted them. Applying corrections through IDEA's patch API and then
reformatting resolved the problem. [Failure record](../experiments/daytrader3-gradle-upgrade/2026-10-11/README.md#failures-and-limitations).
A shell-only workflow would need to reconcile or reload editor buffers before
formatting/saving, or use a separate checkout.

IDE integration did not eliminate editing failures. A combined unified patch
was rejected during migration, and a build was launched before verifying that
the source transformation had landed. Explicit per-file patches then succeeded.
That failed launch remains excluded from target acceptance. The resulting lesson
is to inspect the tool result and actual source before launching dependent work.

## Debugging: observe state rather than infer it from source

The integration supplied a local `ij-debugger/SKILL.md`. The agent read it and
followed its instructions: begin with a small hypothesis-driven probe, prefer
non-suspending logpoints, drain debugger events, inspect stack/values if necessary,
preserve user breakpoints and remove agent probes afterwards. The skill is
instructional material rather than another model to which diagnosis was delegated.

Its observed installation was under
`~/Library/Caches/JetBrains/IntelliJIdea2026.2/aia/agents/views/codex/.agents/skills/ij-debugger/SKILL.md`.
The file inspected during reflection has SHA-256
`ac51005bc26fa4a60bdef86673739bbb97b43c1c66f60c758293cd0c331b59f6`.
This identifies the local instruction source; its cache location alone does not
establish who authored it or which plugin installation step supplied it. The skill
is not copied into this repository.

Two diagnoses show what the debugger gained:

| Failure | Runtime observation | Consequence |
|---|---|---|
| Lost debit on the legacy stack | Two distinct threads read cash 30000.00 and assigned different single-purchase balances | Supported refreshing and locking mutable accounts within the existing transaction; preserved the original failing result separately |
| Missing order history after the Jakarta provider change | Order-creation logpoints observed both orders; paused account state showed cash 29597.10, two holdings and an inverse orders collection of size zero | Supported an explicit no-shared-cache policy, followed by unchanged-suite validation |

The first observation is in the
[repair debugger record](../experiments/daytrader3-account-repair/2026-10-11/debugger-observation.txt).
The second is in the
[migration debugger record](../experiments/daytrader3-jakarta-migration/2026-10-11/attempts/debugger-observation.txt).
An earlier restart diagnosis also used runtime evidence to correct a premature
application-defect claim: JVM-local long-run configuration was missing after
restart. [Baseline diagnosis](../experiments/daytrader3-baseline/2026-10-10/README.md#restart-failure-diagnosed-harness-error).

Non-suspending logpoints evaluate expressions and report events without stopping
threads. They still add work and can disturb timing. During migration, two
provider-type logpoint expressions failed because IDEA could not resolve their
metadata. The agent then paused one request and inspected the object graph and
call path. Collection rendering may initialize lazy state; that limitation is
recorded. User breakpoints were untouched, agent probes/configuration were
removed and the diagnostic server was stopped. Diagnostic fixtures were excluded
from ordinary acceptance and performance results.

Without IDEA integration, alternatives include another JVM debugger, temporary
application logging and database observations. Temporary logging requires source
changes, rebuilding and later cleanup; SQL establishes persisted state but cannot
alone show what an in-flight entity or branch actually contained. None of those
alternatives was run as a controlled effort comparison, so there is no measured
time-saving claim.

## Running builds and using the visible GUI

The agent used IDEA's existing Gradle run configurations, including
**DayTrader Build**, through the tool router. This exercised the author's IDE
execution path and captured logs. Gradle still compiled and tested the application;
IDEA was the launcher. Most acceptance builds and all repeated workload
orchestration used native shell commands, which made environment/version selection
and saved commands explicit.

The final [IDEA run context](../experiments/daytrader3-jakarta-migration/2026-10-11/target-idea-build/context.txt)
records 44 fresh HTTP/restart/SQL cases and eight unit results up to date from a
passing shell build. This was incremental compilation, not another clean build.
The isolated target server ran Java 21 and stopped after verification.

The visible GUI attempt was narrower: register the pinned Java 21 JDK and select
it as IDEA's Gradle JVM. It did not change the setting. The successful fallback
used `-Porg.gradle.java.installations.paths` in the run configuration. IDEA's
Gradle JVM remained Zulu 8, while Gradle toolchains selected Java 21 for the
application/unit/server and Java 8 for independent verification. SDK registration,
reimport and interactive target startup were not thereby verified.

The author noticed the screen interaction and asked about it. GUI interaction
stopped; later build verification used the tool interface and explicit toolchain
path. Formatting and debugger inspection did not require finding buttons on the
screen. The recorded GUI attempt had no demonstrated setup benefit; direct tools
were the more useful route for the operations they exposed.

## What the author enabled, and what remains unknown

The session ran with an IDEA integration exposing the tool definitions and the
debugger skill. The project was open and its DayTrader Gradle modules were linked.
Earlier restoration work configured SDK/Gradle execution and local run
configurations. Those setup changes were performed as part of the collaboration,
not all manual actions by the author. [Restoration evidence](../experiments/daytrader3-restoration/2026-10-10/README.md).

The author's documented contributions include requesting IDEA/SDK setup before
runtime work, establishing project code style (root commits `a905c68` and
`86623bf`), formatting earlier code, and requiring actual IDEA formatting before
subsequent code commits. These choices made the formatter's output meaningful
and repeatable within the project.

The exact plugin name/version, installation steps, MCP connection settings and
how the skill was installed have not been verified. An open project and style
files alone would not give an agent these tool permissions or expose a debugger
skill. The agent has asked the author for those setup details rather than
inventing them. The earlier run configurations and Gradle JVM settings are local
ignored files; code-style files are tracked. The later reusable debug follow-up
adds three portable configurations under `.run/`. A public clone does not
recreate the whole live IDE integration automatically.

## Knowledge used and next practice

Project README/PLAN/AGENTS, the migration contract, subject code, frozen tests and
previous experiment records supplied local context. Tool schemas supplied the
operation interfaces. The debugger skill supplied procedural guidance. Official
platform documentation and general JVM/Jakarta knowledge informed hypotheses;
runtime observations and tests assessed them. Private Theseus material and
reference target implementations were not consulted for this migration; public
project descriptions of Theseus were present in context.

The supported practice is to delegate an existing operation when its behavior
fits the task: use IDEA formatting for the project's IDEA style, editor-aware
patching when live documents matter, the debugger for runtime questions and
Gradle for compilation/tests. Use the shell for reproducible orchestration and
artifact analysis. Confirm results rather than treating a successful tool call
as completion. Semantic rename, call hierarchy and inspection tools are also
available in the current interface, but their availability is not evidence that
they were used in the recorded migration. Their value can be assessed in a later
concrete task rather than replacing working methods solely to increase IDE use.

## Enablement recommendations after reflection

The author asked whether further setup would make IDEA or other tools more useful.
The current interface already exposes formatting, patching, debugger controls,
semantic symbol/call lookup, inspections, refactoring and source/decompiled-class
reading. Better selection of these existing tools is an agent responsibility;
their presence does not establish that every capability has been exercised.

The initial recommendations and their current follow-up status are:

| Priority | Change | Expected gain and responsibility |
|---|---|---|
| First | Provision/register the pinned Java 21 JDK in a stable location; keep Java 8 available and verify Gradle sync/toolchain selection | Author completed installation/registration; agent verified discovery and removed the temporary path override. Gradle reimport remains unverified. See the follow-up below. |
| Next | Prepare a reusable isolated test/debug server launch and attach configuration | Author requested this follow-up; Start/Attach/Stop now work with separate debug data and ports, named launch settings and verified cleanup. [Usage](daytrader-debugging.md), [evidence](../experiments/daytrader3-debug-setup/2026-10-11/README.md). |
| Next | Share portable selected run configurations, with workstation-specific paths kept local | The debug follow-up supplies three shared `.run/` configurations using project-root macros. Existing build/interactive configurations remain local. Fresh-clone reconstruction remains unverified. |
| Documentation | Record the plugin/integration name, version and enabling steps | This missing author input would make the tooling/skill provenance reproducible and help diagnose changes after upgrades. An open project alone does not expose the agent tools. |
| Conditional | Add a small repository skill for a proven repeated diagnostic workflow | Useful once fixture/start/attach/probe/cleanup steps stabilize. Keep it short and test discovery in each integration; avoid duplicating the existing debugger skill or turning every task into another skill. |

Gradle synchronization and resolvable project dependencies help semantic tools
operate on the intended code model. They do not guarantee that every runtime
provider type can be resolved in a debugger expression; the earlier EclipseLink
expression failures remain evidence of a limitation, not a proven setup fix.

No additional connector installation is currently justified by a demonstrated
missing capability for DayTrader. Git, Gradle, artifact analysis and workloads
already work through the shell. Prefer adding a connector when a concrete task
reveals a gap rather than expanding the tool catalog speculatively.

For this follow-up, the agent read official OpenAI documentation using the
`openai-docs` skill. The [MCP guide](https://developers.openai.com/codex/mcp/)
describes configuration and tool selection; the
[skills guide](https://developers.openai.com/codex/skills/) describes repository
skill discovery under `.agents/skills`. These establish general Codex mechanisms,
not the exact configuration of this JetBrains integration. No JDK, plugin,
run configuration or skill was installed or changed during that recommendation review.

### Author completed the stable JDK setup

The author subsequently installed `temurin@21` and registered `temurin-21` in
IDEA. Native inspection confirms Temurin **21.0.12.1+1**, matching the pinned
migration version, at `/Library/Java/JavaVirtualMachines/temurin-21.jdk/Contents/Home`.
The IDEA SDK registry names the same home. This is a verified author contribution;
it does not establish the new installation's original archive checksum.

Gradle's `javaToolchains` task succeeds without an explicit installation-path
property under both Java 8 and Java 21 daemon setups. Under the existing Java 8
IDEA Gradle-JVM equivalent, Java 21 is detected through macOS `java_home`.
The agent consequently removed the temporary toolchain-path override from the
local **DayTrader Build** configuration through IDEA's patch tool and formatted
that XML through IDEA. This configuration no longer depends on the temporary JDK
directory. No application build/test/server launch was run during this check.

[Setup follow-up evidence](../experiments/daytrader3-jakarta-migration/2026-10-11/target-idea-build/jdk-registration-followup.txt)
records the commands, version, SDK entry and remaining limits. The original
build's context is preserved unchanged. Gradle JVM is still Zulu 8 and root
project SDK is still Temurin 25; SDK registration is now verified, while Gradle
reimport and interactive target startup remain unverified.

### Reusable isolated debug setup completed

The author next requested recommendation 2. The agent used IDEA patching and
formatting to create a root Gradle init script and three shared configurations:
**DayTrader Debug Start**, **DayTrader Debug Attach** and **DayTrader Debug Stop**.
The script reuses the subject's fixture loader and target runtime while keeping
debug data, ports and output separate. Ordinary builds do not load it.

IDEA launched the server, attached its JVM debugger and reported a non-suspending
quote logpoint during a real HTTP request. A second Start was refused before any
task ran, with unchanged debug database hashes. Explicit Stop and deliberate
failed-start cleanup passed. Interactive/acceptance fixtures and frozen tests are
unchanged; the subject needs no new commit or pointer. All three configurations
report `supportsDynamicLaunchOverrides=false`; named values worked without
overrides. No visible GUI interaction was needed.

The initial reset-guard verification had an ordering mistake: cleanup began
before the competing start finished, invalidating that result. The agent
acknowledged it and reran sequentially, then moved the guard ahead of provisioning
dependencies. The [setup record](../experiments/daytrader3-debug-setup/2026-10-11/README.md)
preserves the failure, correction, final implementation hashes and validation
limits. The [guide](daytrader-debugging.md) explains Run Start → Debug Attach →
detach and Run Stop. This is a setup smoke check; the full acceptance suite and
performance investigation were not resumed.
