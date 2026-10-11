# ADR 0002: Attribute knowledge sources and distinguish evidence types

- Date: 2026-10-11
- Status: Recorded standing project requirements
- Origin: The author asked to capture the remaining reflection topics into persistent
  documentation and decisions. This records the evidence/privacy requirements
  already established in README and AGENTS; it does not introduce new engineering scope.

## Context

The DayTrader account combines author requirements, source inspection, skills,
official documentation, model knowledge and executed checks. A portfolio reader
needs to distinguish their contributions and limits. The
[provenance inventory](../daytrader-knowledge-provenance.md) identifies concrete
examples but cannot reconstruct every consulted page or pretrained source.

## Alternatives

- An undifferentiated list of sources would obscure which informed choices and
  which supplied acceptance evidence.
- An exhaustive retrospective reconstruction would invite unsupported attribution
  where consultation records or model provenance are unavailable.
- A bounded, linked inventory preserves supported contributions and explicit unknowns.

## Decision

Use the bounded inventory. Keep requirements/author decisions, documented claims,
inspected source, executed observations and hypotheses/general knowledge distinct.
Link consequential choices to their source and validation when recorded; identify
retrospective recollection or interpretation and mark missing provenance unknown.
Report the exact behavior checked rather than implying universal equivalence.

Keep migration context separate from reference study and setup research performed
afterward. Preserve the distinction between tool capabilities, skill instructions
and their unverified installation origin. Retain the public/private boundaries;
do not copy private Theseus material or credentials into the source inventory.

Experiment-local decisions remain in experiment records. This ADR records the
cross-experiment attribution convention; it does not imply new author acceptance
of each historical agent implementation choice.

## Consequences and open questions

The inventory is useful while incomplete. Plugin name/version, connection steps,
skill supplier/discovery and fresh-clone reconstruction remain open. Exact served
model, usage/effort and pretrained sources cannot be invented. Future records
should capture important source/decision/check relationships when they occur;
no exhaustive new logging system is required. Documentation checks validate links,
table structure and consistency, not past tool installation or application behavior.
