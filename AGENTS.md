# Agent Working Agreements

## Purpose and language

This project investigates and compares approaches to modernizing legacy enterprise Java. Read [README.md](README.md) for the purpose, vocabulary, experiment workflow, and evidence requirements. Read [PLAN.md](PLAN.md) for the current verified state, active milestone, unresolved issues, and next action. Historical decisions and handoffs are in [project history](docs/project-history.md); consult them and linked experiment records when relevant, rather than treating historical next actions as current instructions.

Write project documentation, plans, experiment reports, and reusable instructions in English, even when the conversation uses another language.

The author intends to use the project as a portfolio showing how AI supports engineering and personal work management. Preserve concrete decisions, corrections, failures, and validation. Describe contributions and limitations accurately; the portfolio purpose is a reason for transparency.

## Continuity across sessions

- At the start of a new session or after losing context, read README.md and PLAN.md before substantive work. Read applicable instructions in the directories involved.
- Check the plan against the actual workspace. Resolve stale status using inspectable evidence and distinguish facts, hypotheses, recommendations, and accepted decisions.
- Briefly state the active milestone, intended outcome, and connection between the requested task and the project goal. Keep this proportional to the task.
- Treat repository documents as durable context. Do not assume access to earlier chats or that another agent or integration automatically discovers these instructions. When checking a new integration, verify which instructions it loaded.
- Before ending substantive work, replace PLAN.md's current status with verified progress, accepted revision/evidence links, unresolved issues, and one concrete next action. Keep one active milestone and a short parked list. Do not append session handoffs, decision-log rows, superseded next actions or detailed execution history to PLAN.md.
- Keep commands, validation checkpoints, failures and human interventions in the relevant experiment record. Preserve earlier project decisions and handoffs in project history; do not erase corrections or private/public boundaries when shortening current documentation.
- Keep experiment-local decisions with their experiment. Use a short Architecture Decision Record (ADR) under `docs/decisions/` only for consequential choices governing multiple experiments: context, alternatives, decision/status and consequences. Attribute recommendations and author acceptance separately. See [ADR 0001](docs/decisions/0001-documentation-and-checkpoints.md) for the accepted documentation arrangement.

## Help maintain direction

The author welcomes help recognizing when detailed work displaces the larger objective. Agents share responsibility for noticing drift in their own work.

- Keep one main milestone active. Explain how a proposed task advances it, resolves a prerequisite, or answers an investigation question.
- Answer detailed questions while retaining the current objective. Treat them as steering within ongoing work unless the author clearly changes the objective.
- At natural checkpoints, especially after repeated blockers, growing scope, or changed assumptions, summarize what was learned and recommend continuing, changing course, or parking the tangent.
- Make the recommendation concrete: identify the current goal, the detour, its value, and the next useful action. Be candid and respectful; support the author's agency.
- For exploratory work, define the question, expected result, and stopping condition. Use agreed limits when available. Do not invent budgets or elapsed-effort estimates.
- Park useful ideas in PLAN.md with a reason and a condition for revisiting them. Do not silently discard them or turn every idea into active scope.
- Continue routine work within the authorized task without repeated confirmation. Surface consequential tradeoffs when a decision is needed. An agent recommendation does not become an author decision merely because it appears in the plan.
- Keep planning lightweight. Prefer delivering and checking a useful result over expanding the planning system.

## Workspace and experiment boundaries

- Keep original upstream subject repositories, reference repositories, and evaluation resource checkouts untouched. An author-controlled subject fork may remain under `subjects/upstream/` and be edited on an explicitly assigned work branch; preserve the recorded original source revision and keep its default branch as an upstream mirror. Otherwise make application changes in the assigned implementation checkout. Follow the purpose separation in [the proposed subject branch convention](docs/subject-branches.md), and record baseline restoration, tooling upgrades, and migration results separately. Update a gitlink only for an intentional milestone. Staging and local root commits may reference subject commits that are not yet fetchable; clearly tell the author the exact revision and branch still needing publication. Before publishing the root commit, publish and verify the referenced subject commits in their configured forks.
- Keep Theseus and other private material outside the public submodule manifest. Add `/local-private/` to the superproject's ignore rules before using it. Public setup must work without private credentials.
- Do not copy private or customer-specific content into public artifacts. Use reviewed, non-customer-specific methods and public demonstrations with accurate provenance.
- Keep client-history chronologies internal and private, including anonymized dates, work sequences, and tool-use details. Removing names and verifying source fidelity do not establish permission to disclose. The Theseus questions, original author answer, agent-written summary, and their contents are private for now by author decision. Keep all versions in ignored private storage and out of public staging, commits, and publication unless the author explicitly changes that decision. Review related account material for disclosure suitability before committing changes to it.
- Use **Theseus** as the public alias for the private effort. Keep former customer-facing project names and application identifiers in ignored private notes. Preserve original author responses privately before preparing anonymized public summaries, and label agent paraphrases and retrospective recollections explicitly.
- Pin relevant revisions and environments. Keep reference updates separate from experiment runs; do not silently advance upstream revisions.
- When evaluating independent migration performance, use an access boundary to exclude reference target implementations and held-out tests from the migration agent. Instructions alone do not provide that boundary. Label runs that consult reference solutions as reference-assisted.

## Formatting and coordinated commits

- Before committing code written or changed by an agent, apply IntelliJ IDEA formatting using the project's code style in `.idea/codeStyles/`. Limit formatting to the changed code/files and inspect the resulting diff. If IDEA formatting cannot be applied, leave the code uncommitted for the author to format; do not claim manual approximation is IDEA formatting. Continue independent work while that handoff is pending.
- Group related code, formatting, validation evidence, documentation and gitlink updates into meaningful milestones. Do not create root commits solely to mirror every intermediate subject commit. Separate repositories necessarily have separate commits, but the root milestone commit should include its related documentation and the selected subject revision together.
- Distinguish work steps, validation checkpoints and commits. Use targeted checks during diagnosis and the required acceptance checks on the final milestone state; do not commit every attempt or rerun broad checks without a relevant change or unresolved concern. Group commits by reviewable purpose, keeping intentional repairs separate from migration and coupled compatibility changes together where necessary. A labeled failing or incomplete recovery checkpoint may be committed with its observed evidence; it is not an accepted working migration. Formatting may be separately reviewable within the same milestone, but final validation must describe the final code.
- An unpublished subject pointer does not require permission to stage or commit locally. Explicitly report which subject branch/revision needs pushing so the author can do it afterwards. Distinguish staged, locally committed and remotely verified status; do not imply that local preparation establishes public checkout reproducibility.
- When publication is authorized, handle push ordering: push affected subject branches, verify the referenced commits are fetchable from their configured remotes, then push the root branch. Stop root publication if a subject push or verification fails. `git push --recurse-submodules=check` is an additional guard, not a substitute for deliberate branch publication and verification. See [the coordinated workflow](docs/subject-branches.md#coordinated-milestone-commits-and-publication).

## Evidence and completion

- Define the migration contract and acceptance evidence before transformation. Record permitted behavior differences explicitly.
- Run checks appropriate to the change. A successful build alone does not establish preserved application behavior; documentation-only tasks need document review rather than application tests.
- Preserve evaluation expectations. If test porting is required, document it; weakening an assertion or changing its meaning requires explicit review and a recorded reason.
- Record commands, relevant revisions, outcomes, known gaps, failures, and human interventions in the experiment record described by the README. Record model/tool identifiers and usage or effort where available; mark unavailable data as unknown.
- Describe exactly what was validated. Do not present planned checks as executed, reference claims as reproduced results, or passing tests as universal equivalence.
- Report the outcome, validation, and material limitations concisely, with links to artifacts a reader can inspect.
