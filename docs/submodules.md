# Public Submodule Inventory

Recorded: 2026-10-09

The eight public repositories listed in the README are registered in [.gitmodules](../.gitmodules). The initial selection rule was to capture each repository's default-branch HEAD when added, retaining its full Git history. These are starting snapshots for inspection; no build, runtime behavior, or migration result has been validated. Experiment revisions may be selected differently after feasibility work and must be recorded explicitly.

## Initial revisions and license observations

| Checkout | Role | Initial branch | Pinned commit | License evidence |
|---|---|---|---|---|
| [subjects/upstream/deftERP](../subjects/upstream/deftERP) | Prospective subject | `master` | `ba859d461cbfeb1d0c2f871a8c89f82fd7e25c07` | Apache-2.0: [LICENSE](../subjects/upstream/deftERP/LICENSE). |
| [subjects/upstream/sample.daytrader3](../subjects/upstream/sample.daytrader3) | Prospective subject | `master` | `a2d61af8c75c771fe4c9ad3f101bbdef08046c1a` | Apache-2.0: [LICENSE](../subjects/upstream/sample.daytrader3/LICENSE); component notices also exist. |
| [references/kai](../references/kai) | Migration tooling | `main` | `34dc136c735a2fcc0c1e6fa549747fd449a07927` | Apache-2.0: [LICENSE](../references/kai/LICENSE). |
| [references/java-migration](../references/java-migration) | Research agent implementation | `main` | `35b1dce3a5698cde62916ef0312a43f9b0895de9` | Apache-2.0: [LICENSE](../references/java-migration/LICENSE) and [NOTICE](../references/java-migration/NOTICE). |
| [references/ai-assisted-code-migration](../references/ai-assisted-code-migration) | Case-study code | `main` | `62e3394379a69a153aef8508c0229070148d98d0` | Apache-2.0: [LICENSE](../references/ai-assisted-code-migration/LICENSE); included code has additional license files. |
| [references/spring-boot-example](../references/spring-boot-example) | Case-study code | `master` | `6f7ed5ae6ad896810ac892d211672983b18d5421` | No license file identified in this checkout; reuse terms remain unresolved. |
| [evaluation/scarfbench](../evaluation/scarfbench) | Evaluation and reference implementations | `main` | `7c83756671f5297cf3576c813c52aa9fb956867f` | The root README links to a root LICENSE file that is absent at this revision. Included applications carry individual licenses; repository-wide terms remain unresolved. |
| [evaluation/migrationbench](../evaluation/migrationbench) | Dataset and evaluation framework | `main` | `92bf074e28b1e86f66bd99acfa01e5bcbafe5b72` | Apache-2.0: [LICENSE](../evaluation/migrationbench/LICENSE) and [NOTICE](../evaluation/migrationbench/NOTICE). |

These observations identify license files, not a complete audit of every included component or dataset. Preserve applicable notices and check the terms of material selected for reuse. The superproject's license does not replace upstream licenses.

## Checkout and verification

For an existing clone, initialize the recorded repositories with:

```bash
git submodule update --init --recursive
git submodule status --recursive
```

For a fresh clone:

```bash
git clone --recurse-submodules https://github.com/middlewareman/enterprise-refit.git
```

The fresh-clone command will reproduce these additions after `.gitmodules` and the Git links have been committed and published. Each recorded revision must remain fetchable from its configured repository URL.

Verification during setup checked that all eight repositories were initialized, their HEADs matched the Git links staged in the superproject, and their worktrees were clean. None contained a nested `.gitmodules` file at the recorded revision. Recursive status showed eight initialized entries with no uninitialized or revision-mismatch markers. A fresh clone of the published superproject has not been tested in this task.

The initial `git submodule add` checkouts are on their upstream default branches; the superproject pins commit IDs, not moving branch tips. Later initialization normally produces detached HEADs. Original upstream subjects and reference checkouts remain untouched. Author-controlled subject forks may use explicitly assigned work branches at the existing subject path; [the proposed branch convention](subject-branches.md) separates restoration, tooling, and experiments. Record deliberate source or reference revision updates separately.

## DayTrader fork configuration

On 2026-10-10, the author selected [middlewareman/sample.daytrader3](https://github.com/middlewareman/sample.daytrader3) as the configured DayTrader submodule repository. Its provenance remains [WASdev/sample.daytrader3](https://github.com/WASdev/sample.daytrader3). The initial revision table above is unchanged.

`git ls-remote` verified that the fork's HEAD and `master` were both `a2d61af8c75c771fe4c9ad3f101bbdef08046c1a`, matching the existing pin. `git submodule set-url` updated [.gitmodules](../.gitmodules) and synchronized local configuration; the local DayTrader `origin` now points to the fork, and an `upstream` remote records the original repository. That additional remote must be configured separately in a new clone.

No application source, branch, gitlink, or build output was changed during this configuration. No build or runtime check was performed, and a fresh clone using the revised URL has not been tested.

Theseus is absent from the public manifest. The shared workspace currently contains reference target implementations; isolate the permitted context before measuring independent agent performance.

## DayTrader restoration milestone

Restoration commit `37a8facf9729f271160aabc02dcf312fff7e0fc9` on `restore/runtime`
adds the Gradle 4.10.3 wrapper, pinned Liberty runtime, generated-state isolation,
and build/run instructions. The original source remains the initial revision above,
and the fork default branch remains an upstream mirror. [Build and runtime evidence](../experiments/daytrader3-restoration/2026-10-10/README.md).

The restoration commit is now published on the fork's `restore/runtime` branch;
`git ls-remote` verified its tip. Superproject commit `c6c9c88` records this
restoration gitlink. All other submodule revisions are unchanged.

## DayTrader Gradle-only tooling milestone

The current DayTrader pin is `0894dc9998d42fe8563169aabca479a63372d675` on
`tooling/gradle-only`, derived from restoration commit `37a8fac`. It removes Maven
build support before introducing the Gradle verification suite. The branch is
published on the configured fork, and `git ls-remote` verified its exact tip
before this gitlink update. Application sources and runtime/dependency versions
are retained; the other seven submodule pins are unchanged.
[Change and validation evidence](../experiments/daytrader3-gradle-only/2026-10-10/README.md).
