# Agent Working Agreements

## Purpose and language

This project investigates and compares approaches to modernizing legacy enterprise Java. Read [README.md](README.md) for the purpose, vocabulary, experiment workflow, and evidence requirements. Read [PLAN.md](PLAN.md) for the current focus, decisions, and next action.

Write project documentation, plans, experiment reports, and reusable instructions in English, even when the conversation uses another language.

The author intends to use the project as a portfolio showing how AI supports engineering and personal work management. Preserve concrete decisions, corrections, failures, and validation. Describe contributions and limitations accurately; the portfolio purpose is a reason for transparency.

## Continuity across sessions

- At the start of a new session or after losing context, read README.md and PLAN.md before substantive work. Read applicable instructions in the directories involved.
- Check the plan against the actual workspace. Resolve stale status using inspectable evidence and distinguish facts, hypotheses, recommendations, and accepted decisions.
- Briefly state the active milestone, intended outcome, and connection between the requested task and the project goal. Keep this proportional to the task.
- Treat repository documents as durable context. Do not assume access to earlier chats or that another agent or integration automatically discovers these instructions. When checking a new integration, verify which instructions it loaded.
- Before ending substantive work, update PLAN.md with verified progress, material decisions, unresolved issues, and one concrete next action. Update the detailed experiment record when relevant. Avoid logging routine conversation turns or duplicating evidence.

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

- Keep upstream subjects, reference repositories, and evaluation resource checkouts untouched. Make application changes in the assigned experiment implementation checkout or branch. Record baseline restoration separately from migration.
- Keep Theseus and other private material outside the public submodule manifest. Add `/local-private/` to the superproject's ignore rules before using it. Public setup must work without private credentials.
- Do not copy private or customer-specific content into public artifacts. Use reviewed, non-customer-specific methods and public demonstrations with accurate provenance.
- Keep client-history chronologies internal and private, including anonymized dates, work sequences, and tool-use details. Removing names and verifying source fidelity do not establish permission to disclose. The Theseus questions, original author answer, agent-written summary, and their contents are private for now by author decision. Keep all versions in ignored private storage and out of public staging, commits, and publication unless the author explicitly changes that decision. Review related account material for disclosure suitability before committing changes to it.
- Use **Theseus** as the public alias for the private effort. Keep former customer-facing project names and application identifiers in ignored private notes. Preserve original author responses privately before preparing anonymized public summaries, and label agent paraphrases and retrospective recollections explicitly.
- Pin relevant revisions and environments. Keep reference updates separate from experiment runs; do not silently advance upstream revisions.
- When evaluating independent migration performance, use an access boundary to exclude reference target implementations and held-out tests from the migration agent. Instructions alone do not provide that boundary. Label runs that consult reference solutions as reference-assisted.

## Evidence and completion

- Define the migration contract and acceptance evidence before transformation. Record permitted behavior differences explicitly.
- Run checks appropriate to the change. A successful build alone does not establish preserved application behavior; documentation-only tasks need document review rather than application tests.
- Preserve evaluation expectations. If test porting is required, document it; weakening an assertion or changing its meaning requires explicit review and a recorded reason.
- Record commands, relevant revisions, outcomes, known gaps, failures, and human interventions in the experiment record described by the README. Record model/tool identifiers and usage or effort where available; mark unavailable data as unknown.
- Describe exactly what was validated. Do not present planned checks as executed, reference claims as reproduced results, or passing tests as universal equivalence.
- Report the outcome, validation, and material limitations concisely, with links to artifacts a reader can inspect.
