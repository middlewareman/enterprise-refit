# Subject Forks and Branches

Prepared: 2026-10-10

The author requested using the DayTrader fork and separating build restoration, focused tooling upgrades, and migration work. The names below are an agent-proposed convention. `restore/runtime` now records the first DayTrader restoration milestone; no baseline tag has been created.

## Repository and checkout roles

For DayTrader, `origin` is [middlewareman/sample.daytrader3](https://github.com/middlewareman/sample.daytrader3); `upstream` identifies [WASdev/sample.daytrader3](https://github.com/WASdev/sample.daytrader3). The submodule remains at `subjects/upstream/sample.daytrader3/`. In this fork-backed checkout, the path identifies the subject's source location; an explicitly assigned work branch can contain changes. It does not make every revision under that path an untouched baseline.

The unchanged source revision remains `a2d61af8c75c771fe4c9ad3f101bbdef08046c1a`. The fork's `master` and HEAD matched that revision when checked on 2026-10-10. Keep `master` as an upstream mirror, with deliberate upstream updates recorded separately. Do not merge restoration, tooling, or migration work into it.

Other subjects still using their original repositories, plus reference and evaluation checkouts, remain untouched. Apply this editable workflow to another subject only after selecting an author-controlled fork or implementation checkout for it.

## Recommended names and scope

| Branch | Purpose | Starting point and scope |
|---|---|---|
| `master` | Preserve upstream source history. | Mirror upstream through recorded updates; no experiment changes. |
| `restore/<purpose>` | Make the original application build or run. Example: `restore/build`. | Start at the pinned source. Limit changes to necessary repairs, and record any unavoidable version changes. Preserve the intended platform and behavior. |
| `tooling/<tool>-<target>` | Evaluate a focused tooling upgrade. Example: `tooling/gradle-<version>`. | Start at an explicitly recorded source or restored baseline. Include required build-script/plugin changes, and verify compilation target, packaging, tasks, and tests. Do not silently bundle an enterprise-platform migration. |
| `experiment/<id>/<approach>` | Execute a migration contract. Example: `experiment/001/manual`, `experiment/001/agent`. | Comparable approaches start at the same recorded baseline commit, with the same contract and evaluation inputs. Separate approaches use separate branches. |

Use lowercase names and hyphens. Choose actual target versions and experiment IDs when their scope is defined; placeholders above are not literal branch names to create.

A repair branch and a tooling branch need not form a mandatory sequence. Try the recorded original build environment first where feasible. An optional Gradle upgrade can branch from a working restored baseline; if it is required to restore buildability, record that dependency and the expanded restoration scope explicitly. A later migration may use a tooling result as a prerequisite, but its exact input revision must identify that choice.

## Revision and validation rules

- Branch names identify purpose; commit IDs identify evidence. Record the untouched source, restoration result, any tooling prerequisite, and each experiment's starting and final revisions separately.
- Treat a restored baseline as validated only after its stated checks pass. A branch called `restore/build` does not establish buildability or preserved behavior. An optional `baseline/<id>` tag can mark a checked baseline; retain its commit ID and validation record, and never move the tag to replace an earlier result.
- Keep shared repairs in separate commits. Incorporating one into an experiment changes the run's inputs and requires recording the new revision and affected validation. Do not merge one comparator's migration into another.
- A submodule's gitlink is the selected workspace revision. Switching a local work branch can make it differ from that pin; do not stage that difference as routine cleanup. Update the pin only for an intentional recorded milestone. Local root commits may reference local subject commits; publication requires the referenced commits to be available from the configured fork.
- Before changing branches or restoring a pinned checkout, inspect and preserve outstanding work. Normal submodule initialization produces a detached HEAD; create an explicit work branch before editing. For concurrent experiments, separate worktrees or implementation checkouts avoid sharing one checked-out branch.
- Changing branch or checkout layout does not establish an agent access boundary. Independent migration evaluation still requires excluding reference solutions and held-out tests from the migration agent's accessible workspace.

For example, after assigning a build-restoration task, this command creates its branch from the unchanged DayTrader source:

```bash
git -C subjects/upstream/sample.daytrader3 switch -c restore/build a2d61af8c75c771fe4c9ad3f101bbdef08046c1a
```

The command is an example and was not executed during fork configuration. No branch tip is selected through `.gitmodules`; the superproject continues to pin exact commits.

## Coordinated milestone commits and publication

Author preference, recorded 2026-10-11: apply IDEA project formatting before
committing agent-written code, or leave it for the author to format. Group related
work rather than creating root commits solely to synchronize intermediate pins.

Work steps, validation checkpoints and commits can have different boundaries.
Use targeted checks while diagnosing and required acceptance checks on the final
milestone state. A subject may contain several focused commits within one root
milestone; label failing or incomplete recovery checkpoints with observed evidence
and distinguish them from accepted working results. Preserve intentional repairs
separately from migration. See [ADR 0001](decisions/0001-documentation-and-checkpoints.md)
for the accepted documentation and checkpoint arrangement.

1. Complete the subject change, apply IDEA formatting, inspect the diff and run
   appropriate validation on the final code. Prepare the related root evidence
   and documentation alongside it.
2. Commit the subject change locally. Use its exact commit ID in the root evidence,
   then commit the related root documentation and gitlink together as one milestone.
   A milestone may contain several purposeful subject commits without a root
   pointer update for each. Git cannot make one atomic commit across repositories.
   Staging or committing a pointer before the subject is fetchable is authorized.
   Clearly report its exact revision and branch still needing publication so the
   author can push it afterwards; no separate approval is needed for local preparation.
3. When publication is authorized, push affected subject branches first. Verify
   that every referenced subject commit is fetchable from its configured remote;
   when it is the branch tip, compare the full commit ID with `git ls-remote`.
4. Push the root branch only after subject publication and verification succeed.
   Use `git push --recurse-submodules=check` as an additional guard. If a subject
   push fails, retain the local root commit and resolve that failure before
   publishing it; do not create another root commit just to repeat the same pin.

The publication order is required for reproducible checkout; the local root
commit does not require an earlier subject push. These steps describe the agreed
workflow, not commands executed during this documentation update.

## Local remote setup

The fork URL is shared through [.gitmodules](../.gitmodules). An existing clone can synchronize it with:

```bash
git submodule sync -- subjects/upstream/sample.daytrader3
```

The additional `upstream` remote is local configuration. In a new initialized checkout, add it if absent:

```bash
git -C subjects/upstream/sample.daytrader3 remote add upstream https://github.com/WASdev/sample.daytrader3.git
```

## Implication for the next task

The pinned DayTrader root `build.gradle` only applies the Eclipse plugin; module build files contain the application build and Liberty configuration. The EAR module uses Liberty Gradle plugin 2.4 and legacy Gradle APIs. The repository also has Maven builds, and no tracked Gradle wrapper was found in the inspected source inventory. These observations do not establish which build currently works.

The [feasibility assessment](daytrader-feasibility.md) now verifies unchanged-source compilation and packaging with Gradle 4.10.3 and Java 8 in temporary storage. The [restoration record](../experiments/daytrader3-restoration/2026-10-10/README.md) now records successful IDEA build, pinned Liberty startup, and synchronous trading smoke checks on `restore/runtime`. Keep restoration and tooling upgrades visible as separate changes when evaluating migration results.
