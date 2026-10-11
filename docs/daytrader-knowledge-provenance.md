# DayTrader knowledge and evidence provenance

Recorded 2026-10-11 during collaboration reflection, at root `935a656` and subject
`6e6cfa787553e918e5c90edfd1e8882ce2c84d54`. This retrospective inventory links
recorded source categories to concrete choices and observations. It is based on
existing public project records, not a reconstruction of unrecorded model reasoning
or a fresh application run. [ADR 0002](decisions/0002-knowledge-and-evidence-provenance.md)
captures the established attribution rules; the [agenda](reflection-agenda.md)
tracks reflection topics.

## Sources and their contribution

| Source category | Inspectable record | Concrete contribution and limit |
|---|---|---|
| Author decisions and project instructions | [Project history](project-history.md#decision-log), [AGENTS](../AGENTS.md), [contract](daytrader-jakarta-contract.md) | The author chose the Jakarta EE 11 direction, required preserving tests and IDEA formatting, and authorized repair before migration. The contract bounds EAR/interface/schema preservation and allowed platform changes. These are requirements and authorization, not evidence that an implementation meets them. |
| Subject code and frozen evaluation | [Input manifest](../experiments/daytrader3-jakarta-migration/2026-10-11/input-manifest.json), [target source manifest](../experiments/daytrader3-jakarta-migration/2026-10-11/target-source-manifest.json) | Pin input `d25398b`, result `6e6cfa7`, test/source identities and workload changes. Source/interface inspection supported changing the provider-dependent ArrayList cast to Collection. Manifests identify artifacts; hashes alone do not establish behavior. |
| Earlier experiments | [Baseline](../experiments/daytrader3-baseline/2026-10-10/README.md), [concurrency](../experiments/daytrader3-concurrency/2026-10-11/README.md), [repair](../experiments/daytrader3-account-repair/2026-10-11/README.md) | The restart harness correction prevented carrying a mistaken defect diagnosis forward. The lost-debit result and repair establish a deliberately changed migration input. Earlier passing results are scoped observations, not universal equivalence. |
| Official platform/build documentation | [Target choices and linked official pages](daytrader-jakarta-contract.md#authorized-target-and-initial-compatibility-evidence), [saved plugin compatibility snapshot](../experiments/daytrader3-gradle-upgrade/2026-10-11/compatibility-source.txt) | Versioned Liberty EE 11/Persistence/messaging pages and Gradle support guidance informed target compatibility and provider expectations. The contract records consultation on 2026-10-11. Documentation support was followed by probes and deployment; it was not treated as reproduced runtime behavior. |
| Tools, schemas and skills | [IDEA mechanisms and recorded commands](idea-agent-workflow.md#tools-skills-and-gui-actions), [debugger skill record](idea-agent-workflow.md#debugging-observe-state-rather-than-infer-it-from-source) | Tool schemas described callable operations; IDEA executed patching, formatting, builds and debugger requests. The `ij-debugger` skill supplied hypothesis/probe/event/cleanup guidance. Tools and the skill did not independently choose or prove the migration. Full historical schema versions and installation provenance are not pinned. |
| Executed diagnostics and checks | [Migration debugger observation](../experiments/daytrader3-jakarta-migration/2026-10-11/attempts/debugger-observation.txt), [migration attempts and acceptance](../experiments/daytrader3-jakarta-migration/2026-10-11/README.md) | Observed persisted financial state and stale inverse collections supported disabling shared caching, followed by unchanged-suite validation. Two 52-case shell result summaries and matching workload records support bounded acceptance. Debugger rendering can initialize lazy state; diagnostic fixtures were excluded from acceptance/performance results. |
| General model knowledge | Agent identity/limits in the [migration record](../experiments/daytrader3-jakarta-migration/2026-10-11/README.md) and [IDEA account](idea-agent-workflow.md#knowledge-used-and-next-practice) | JVM/Jakarta/persistence knowledge helped formulate hypotheses and select probes. Individual pretrained sources and the contribution of each to an output cannot be traced. Do not turn a plausible explanation into a claim that a specific publication was consulted. |

## Decisions and their attribution

These entries summarize existing decisions. They do not newly authorize engineering
or promote every implementation choice to a separate author decision.

| Decision or correction | Origin and support | Status |
|---|---|---|
| Use Java 21 / Jakarta EE 11 with the proposed Liberty/provider stack; retain enterprise architecture | Author selected the direction and authorized the proposed migration. The agent specified compatibility choices in the [contract](daytrader-jakarta-contract.md). | Authorized scope; bounded functional acceptance is recorded. Performance remains unresolved. |
| Correct lost debits before migration and retain the failing original result | Author superseded the suggestion to carry the defect forward; debugger events and unchanged-suite checks support the [account repair](../experiments/daytrader3-account-repair/2026-10-11/README.md). | Intentional input correction at `f43c5f2`, not a target-platform improvement. |
| Freeze evaluation before transformation and retain observed HTTP 415 behavior | Author preferred unchanged tests; the agent added characterization before input `d25398b`. A speculative XML success expectation failed and was corrected against the baseline before freezing. See [enrichment](../experiments/daytrader3-jakarta-migration/2026-10-11/README.md#baseline-enrichment-checkpoint). | Original assertions retained; the later REST guard is a compatibility implementation choice within the contract. |
| Use the declared Collection interface and explicit no-shared-cache policy | Agent implementation/diagnosis during authorized migration, supported by source, failed runs, debugger state and subsequent tests in [the deployment checkpoint](../experiments/daytrader3-jakarta-migration/2026-10-11/README.md#transformation-and-deployment-checkpoint). | Validated within the named suite; not a separately recorded author architecture choice or a general provider recommendation. |
| Report correctness separately from performance | Recorded in the [migration assessment rule](../experiments/daytrader3-jakarta-migration/2026-10-11/README.md) before target measurements: investigate below 80% throughput or above 120% p95. | Local investigation thresholds; neither production SLAs nor permission to disregard regressions. |
| Apply IDEA formatting before agent-code commits and group root/subject milestones | Author working agreement, recorded in [AGENTS](../AGENTS.md#formatting-and-coordinated-commits) and [the workflow](subject-branches.md#coordinated-milestone-commits-and-publication). | Standing project requirement; formatting and successful tool calls do not establish preserved behavior. |

## Migration context versus later reflection

The migration records state that private Theseus material and reference target
implementations were not consulted. Public README descriptions of Theseus were in
workspace context. This is a recorded boundary of the collaborative case study,
not an independently audited access restriction; no independent-agent boundary
was established.

The [AI-assisted code migration and Amazon JavaMigration inspections](planning-and-checkpoints.md#comparison-with-two-reference-approaches)
were performed later for planning reflection and committed in `f69cae4`. They
inform checkpoint recommendations, not the recorded DayTrader transformation.
Neither reference approach was executed in that inspection.

The [IDEA enablement follow-up](idea-agent-workflow.md#enablement-recommendations-after-reflection)
records later use of the `openai-docs` skill and OpenAI MCP/skills documentation.
Those sources explain general enablement mechanisms; they do not establish which
JetBrains plugin supplied this installation or that those pages guided migration.

## IDEA installation and skill provenance still to capture

The skill record identifies the observed cache path and SHA-256
`ac51005bc26fa4a60bdef86673739bbb97b43c1c66f60c758293cd0c331b59f6`.
This is a hash recorded in the earlier reflection, not a new verification of the
current skill file. No local skill content is copied into this repository.

| Setup fact | Current evidence/status |
|---|---|
| IDE version | IntelliJ IDEA 2026.2 in the setup/migration records. Exact build was not established by this reflection. |
| Plugin or integration name/version | Unknown; awaiting the author's setup account. Tool names alone do not establish plugin ownership. |
| Installation/enabling and connection steps | Unknown; distinguish author recollection from any later inspection or reproduction. |
| Supplier and discovery of `ij-debugger` | Local path and hash recorded; author, packaging source and installation step remain unverified. A cache path does not prove origin. |
| Portable reconstruction | Shared run configurations and guides exist; fresh-clone setup and full installation reconstruction remain unverified. |

The author has been asked for plugin name/version, connection steps and how the
skill arrived. Retain unknown fields if the details cannot be recovered. No
credentials or private configuration contents are needed for this account.

## Limits and future recording

Exact served model, token/cost totals and total human/agent effort remain unknown;
the historical records identify Codex/GPT-6 according to session identity. Broad
claims that official specifications/provider documentation were used do not supply
an exhaustive URL list. In particular, exact page/excerpt attribution for every
Faces, Pages, XML Binding or provider fix is incomplete. Do not add a newly found
page and label it a historical consultation.

For future consequential choices, record the source path/revision or URL/version
and consultation date, what it informed, who decided, the executed check that
assessed it and remaining uncertainty. Experiment-local choices stay with their
experiment; the reusable attribution convention is in ADR 0002. Keep recording
proportional; no complete prompt/tool-call archive or planning automation is required.

This inventory was prepared through public Markdown, manifest/result-summary and
Git inspection using Codex/GPT-6. No application tests were rerun, private material
read, reference revisions advanced or agents delegated. Its stopping condition is
a reviewable source/decision inventory with traceability limits; unknown installation
details do not prevent recording the supported findings.

Documentation review passed: 134 local links, 17 section anchors and 15 table
blocks across the affected documents were checked, along with authored whitespace.
Inspection of the two saved shell result summaries confirms 52 cases each with
zero failures/errors/skips; that is a check of recorded results, not a new test run.
Those link/anchor checks verify destinations and identifiers, not click navigation
in IDEA preview. A later [navigation investigation](idea-markdown-navigation.md)
found a matching reported bug. After a temporary plain-file workaround, the author
chose to restore the contract's heading link and retain standard cross-file anchors.
