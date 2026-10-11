# Mission: Enterprise Refit

**AI-assisted modernization of legacy enterprise Java.**

*To boldly build what nobody has built in years.*

Enterprise Refit explores how engineering judgment, AI coding agents and repeatable
tools can modernize legacy applications while preserving their business behavior.
It is a practical portfolio of working software, tests, decisions, failed attempts
and human interventions. It also examines how planning and shared knowledge help
engineers and agents work together, and how this experience compares with existing
migration approaches.

## Why this project

My curiosity grew out of enterprise Java migration work where policy and regulatory
constraints prevented the use of AI. I wanted to explore what I could achieve with
AI assistance, starting from my existing knowledge and learning through experiments
on public applications.

I learn best by making an initial attempt, then refining it through several
iterations before surveying existing approaches. Hands-on experience gives me
concrete problems and questions: mental hooks for understanding what others have
learned. For me, studying solutions too early can let their framing define the
problem before I have explored it myself. The aim is to build enough understanding
to assess those solutions thoughtfully and revise my own ideas.

## The working strategy

1. **Get the old application running.** Restore its build and runtime with minimal
   changes, establishing a baseline whose behavior can be observed.
2. **Build reasonable test coverage.** Characterize important business flows,
   persisted state and relevant failure cases. Define what must survive the migration
   and how it will be checked.
3. **Make substantial changes in deliberate steps.** With that evidence in place,
   tackle coherent platform or dependency changes boldly. Build, run and test each
   completed step against the agreed behavioral contract.
4. **Review, learn and replan.** Between steps, examine the results, revisit the
   plan and strategy, and record what worked, what failed and what required human
   help. Turn that knowledge into better instructions, checks and tools for the
   next iteration.

## Demonstrated so far

The first public case study takes **DayTrader from a restored Java 8 / Java EE 6
baseline to Java 21 / Jakarta EE 11**. The migrated application passes all
**52 frozen test cases**, covering selected trading, session, persistence, restart
and concurrency behavior. Tests also exposed a lost-debit concurrency defect,
[repaired separately](experiments/daytrader3-account-repair/2026-10-11/README.md)
before migration.

The [migration record](experiments/daytrader3-jakarta-migration/2026-10-11/README.md)
links the contract, changes, checks and failures. These results reflect collaboration
between author and agent within a defined scope. Bounded workload checks preserve
financial invariants, but latency exceeds the predefined investigation threshold;
performance acceptance remains unresolved. Other migration approaches have been
inspected, with execution and broader comparisons still ahead.

## Explore further

- [Project guide](docs/project-guide.md): method, vocabulary, subjects, references
  and workspace setup.
- [Collaboration reflection](docs/reflection-agenda.md): engineering tools,
  planning, knowledge sources and human/AI contributions.
- [Current focus](PLAN.md): verified progress, open questions and the next action.
