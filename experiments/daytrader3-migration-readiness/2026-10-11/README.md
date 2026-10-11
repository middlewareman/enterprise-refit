# Jakarta EE 11 target preparation and compatibility probes

Executed 2026-10-11 as a bounded preparation step after the author-authorized
account repair and workload smoke measurements. Application input remains
`f43c5f2`; no migration transformation or target application deployment occurred.
The [migration contract](../../../docs/daytrader-jakarta-contract.md) records the
question, scope, invariant/test requirements and remaining decisions.

## Provisioned artifacts

[Artifact URLs, SHA-256 and sizes](artifact-manifest.json) identify Open Liberty
26.0.0.9 and Temurin 21.0.12.1+1 macOS/aarch64. Downloaded into
`/private/tmp/daytrader-target-probe`, outside the subject and public Git artifacts.
Each archive was compared against its publisher checksum before extraction.
Only manifests/configuration/logs are committed; temporary binaries may disappear
and must be reprovisioned from the manifest. [JDK version](java-version.log),
[Liberty version](product-version.log), [product validation](product-validation.log).

The Adoptium latest-assets API returned HTTP 403 even with approved network
execution. The public publisher GitHub release API supplied the exact archive
and checksum links instead. Maven Central supplied the runtime and checksum.
This fallback changed retrieval, not the selected Java major version.

## Executed checks and correction

- Native `productInfo version` and `productInfo validate` on the pinned Java 21
  JVM identify Open Liberty 26.0.0.9 and pass product validation.
- The unchanged Java 8-compiled `baseline.DerbyFixture` with Derby 10.10.1.1 runs
  under Java 21, creates the original schema and 40-account/quote dataset in a
  separate temporary database, then shuts it down. [Result](derby-fixture-java21.log).
  This tests direct driver/fixture compatibility, not target JPA or JTA integration.
- [Feature inventory](feature-inventory.txt) contains Jakarta EE 11, Persistence
  3.2, MDBs, embedded messaging, Faces, REST and XML Binding support.
- Initial isolated server replaces the old feature list with `jakartaee-11.0`,
  removes application deployment, uses independent ports 29083/29443/27276/27286,
  and updates the topic destination type to `jakarta.jms.Topic`. It retains the
  baseline datasource/embedded messaging resource structure and a copied fixture.
  [Initial configuration](initial-server.xml), [messages](initial-server-messages.log).
  It reports readiness **but also LTPA error CWWKS4118E**: full-platform security
  needs an explicit keystore/LTPA password. Readiness alone was insufficient.
- Corrected probe adds explicit **public disposable probe-only** keystore/LTPA
  credentials and `xmlBinding-4.0` for legacy REST JAXB usage. It activates the
  required features, starts embedded JMS and reports readiness with no logged
  warnings/errors. [Corrected configuration](corrected-server.xml),
  [messages](corrected-server-messages.log), [start](corrected-server-start.log),
  [automatic explicit stop](corrected-server-stop.log). These credentials are
  synthetic demonstration values and are not production configuration guidance.

Reproduction essentials (set target `JAVA_HOME` and isolated `WLP_USER_DIR` /
`WLP_OUTPUT_DIR`; paths identify the temporary preparation environment):

```bash
/private/tmp/daytrader-target-probe/liberty/wlp/bin/productInfo version
/private/tmp/daytrader-target-probe/liberty/wlp/bin/productInfo validate
java -Dderby.stream.error.file=/private/tmp/daytrader-target-probe/derby-java21.log \
  -cp '<subject>/daytrader3-verification/build/classes/java/main:<cached derby-10.10.1.1.jar>' \
  baseline.DerbyFixture /private/tmp/daytrader-target-probe/derby-java21 \
  '<subject>/daytrader3-ee6-web/src/main/webapp/dbscripts/derby/Table.ddl'
/private/tmp/daytrader-target-probe/liberty/wlp/bin/server start DayTrader_Target_Probe
/private/tmp/daytrader-target-probe/liberty/wlp/bin/server stop DayTrader_Target_Probe
```

The probe copies the committed configuration into an isolated user directory,
copies the stopped fixture and pinned driver into shared resources, applies a
256–512 MiB heap, waits at most 90 seconds for CWWKF0011I, inspects messages for
warnings/errors, and stops in a finally block. Product launchers extracted from
ZIP needed executable permissions restored. The initial failure/correction is
preserved rather than replaced by the successful log.

## Readiness and limits

We have a repaired passing source, unchanged external evaluation expectations,
an executable bounded workload, a checksum-verified Java 21/server pair and a
clean target feature/resource-configuration startup. This supports starting a
controlled compatibility transformation. It does **not** establish DayTrader
runtime behavior, JPA lock semantics, datasource transactions, application JNDI
lookups or async delivery on the target: no application was deployed here.

The JPA provider changes OpenJPA → EclipseLink, and aggregate EE 11 does not
implicitly activate XML Binding in this probe. Preserve the financial/restart/
SQL checks when adapting APIs, XML descriptors and resources. Longer performance
windows/tolerances, broader concurrency/JMS failures, JSF/browser and REST
behavior remain open. Existing interactive server/data were not changed. The final [status check](final-server-status.log) confirms the target probe is stopped; the baseline workload server is also stopped.

Next bounded step: lengthen baseline workload windows and establish comparison
criteria, preserving the author-selected baseline-before-migration sequence.
Then create a separate migration branch from `f43c5f2`, inventory source/descriptor
changes and compile/package on the pinned target without changing test assertions.
Target preparation is complete for those probes; full performance baseline and
application transformation are not claimed complete.

Agent: Codex/GPT-6 per session; exact model, usage, cost and effort unknown.
Tools: shell/Python, official web documentation and checksum downloads, native
Java/Liberty. No reference target implementation or private material consulted.
