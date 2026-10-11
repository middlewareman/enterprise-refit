# Theseus: Initial Reasoning and Questions to Test

Drafted: 2026-10-09

Status: a provisional account requiring disclosure review, based on reviewed documentation. Supporting chronology is private. The questions and author answers are private for now; concrete outcomes and review of this account remain incomplete.

## Source basis

The [project guide](project-guide.md#theseus-an-independent-starting-point) describes Theseus as an approach developed iteratively by the author while working through migration problems, before stepping back to survey existing approaches. That is the project's retrospective account. It does not establish that the author had no prior exposure to related ideas or that the techniques are novel.

The author answer and its agent-written summary are retained privately. Their detailed narrative is withheld from this account.

For this draft, agents reviewed selected method documentation and scripts from a private checkout. Supporting chronology and source references are retained privately. Current documentation was inspected separately to avoid attributing later practices to the initial approach.

Source revisions and review references are retained in ignored local notes. Omitting names and raw excerpts does not establish disclosure suitability. Readers cannot independently inspect the private evidence from this repository; subsequent public demonstrations will provide their own inspectable artifacts.

## Strategy found in the early documents

The reviewed material describes migrating an existing enterprise Java application to a newer Java and Jakarta EE stack, including changes to enterprise APIs, dependencies, and modular organization. Continuing development of the original application is recorded as a constraint. The strategy therefore accommodates an evolving original alongside work to adapt individual components to the new platform.

The documented strategy was to begin from snapshots of existing modules and tackle them one at a time. This records a migration arrangement and working procedure, not proof of who originated it. Merely copying a module or including it in a build did not establish that it worked on the target platform. The migration needed a way to distinguish components that had been adapted from those still awaiting work.

The reviewed guidance calls for minimizing changes to the migrated code to reduce difficulty transferring ongoing changes from the original. This is a stated intention. It is not a measured reduction in conflicts or proof that all subsequent work followed that scope.

## Early choices and intended benefits

| Choice supported by the early documents | Recorded aim or present interpretation | What remains to establish |
|---|---|---|
| Work on one module at a time, starting from a source snapshot. | Present interpretation: limit the immediate migration surface and make progress visible. | Whether module boundaries were sufficient to isolate changes and validation. |
| Keep adaptations small while the original continues evolving. | The reviewed guidance explicitly connects similarity to fewer transfer difficulties. | Actual conflict rates, adaptation effort, and behavioral preservation. |
| Preserve decisions, standards, and observations in shared Markdown. | The routines explicitly aim to retain knowledge and guide subsequent module migrations. | Whether later humans and agents used that guidance correctly, and how much rediscovery it avoided. |
| Explain the reason for a change in its commit record. | Present interpretation: keep intent available for later review and continuation. | Whether the recorded intent was sufficient to understand and replay changes. |

The present interpretations describe why a choice may help; they are not reconstructed author beliefs. The available documents do not establish every assumption the author held or what caused each choice.

## Current documented method

The current reviewed materials describe the following practices:

- Working routines call for keeping migration guidance and status consistent, and preserving decisions from discussions and reviews as reusable instructions.
- Current guidance calls for breaking large transformations into steps, with compilation checks, diff review, and commit checkpoints. Such checks provide evidence about the step being performed; compilation alone cannot establish preserved business behavior.
- The documents distinguish ongoing functional changes from platform adaptations. Revision pairs and intermediate source-shaped histories support decisions about which changes to transfer, adapt, reject, or defer.
- Scripts encode selected mechanical operations, including code cleanup and history replay. The inspected replay tool has an empty platform-transformation extension point; it should be understood as change-transfer machinery, rather than evidence of an implemented automated platform migration.

These observations concern the current documentation and code. Their relationship to every original author assumption remains unknown. No reviewed script was executed in this task, and prior-run claims in the private material were not reproduced.

There is also a scope tension to investigate: current guidance includes style changes and structural cleanup alongside compatibility changes. Those can increase the distance from the original code, despite the earlier preference for minimal adaptations. A public experiment should state which changes belong to its contract and evaluate that tradeoff explicitly.

## Present hypotheses for public experiments

The following are questions derived for this investigation, not assertions about the author's original beliefs:

| Hypothesis | Evidence that could support or challenge it |
|---|---|
| Shared documentation improves continuity between sessions and tools. | A later session can resume from recorded context, recover the rationale, and execute the next validated step; record missing or misleading context and human corrections. |
| Bounded scripts reduce repetitive work without displacing judgment. | Review script diffs and failures on public inputs, validate behavior independently, and compare the effort with a manual alternative where feasible. |
| Small migration steps and explicit change-transfer decisions make ongoing development easier to manage. | Use public revision pairs to inspect accepted, adapted, rejected, and deferred changes; check the resulting behavior and record intervention effort. |
| Methods learned on one application transfer to another. | Apply reviewed generic guidance to a public subject and record which instructions work, require adaptation, or fail. |

## Remaining evidence and review

Further historical context and author input are retained privately. Review of this provisional account and its outcome evidence remains open; the chronology, questions, and answers are private for now. Public subject feasibility work can proceed independently. Any later successful public migration will be reported as a new demonstration with its own source revisions, contract, checks, and limitations.
