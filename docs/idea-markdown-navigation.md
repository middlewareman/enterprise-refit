# IDEA Markdown preview: cross-file heading navigation

Checked 2026-10-11 during collaboration reflection. Question: is the reported
failure of `file.md#heading` a known IDEA Markdown preview issue? Stop after
checking primary sources, matching the link form and recording the supported
conclusion and practical workaround. This is not a migration engineering task.

## Findings

JetBrains' [IDEA 2026.2 Markdown documentation](https://www.jetbrains.com/help/idea/markdown.html#links)
explicitly illustrates cross-file heading links and source-editor navigation.
The selected link was syntactically consistent with that documented form:
`daytrader-jakarta-contract.md#authorized-target-and-initial-compatibility-evidence`.
Its file exists and the target heading matches. This is not generally an
unsupported Markdown feature.

[PY-93086: Markdown Preview fails to navigate to headings in other Markdown files](https://youtrack.jetbrains.com/issue/PY-93086)
is a close symptom match. It reports preview failure for `test1.md#test` in IDEA
Ultimate 2026.2.3 on Windows 11, while source-editor navigation, plain file links
and same-file heading links work. Retrieved metadata says Submitted and lists
no included fix build. This is a user report, not confirmation that JetBrains has
reproduced it or that it explains our macOS installation.

JetBrains also [acknowledged anchor-navigation failures in a 2021 support reply](https://intellij-support.jetbrains.com/hc/en-us/community/posts/4413443463826-Markdown-preview-clickable-links-how-to-do),
linking IDEA-238096 and a separate HTML-anchor issue. That is historical context;
it does not establish their current status or the cause of this later failure.

The current Advanced Settings documentation includes
[Squash multiple dashes in header anchors](https://www.jetbrains.com/help/idea/advanced-settings.html).
That setting can explain some identifier differences, but the selected heading
has no repeated dashes. There is no evidence that changing it would fix this case.

## Workspace evidence and practical handling

- The author reported the selected link failing. Prior checks confirmed target
  files/heading identifiers, but did not exercise clicks in preview. Their passing
  outcome must not be described as demonstrated preview navigation.
- IDEA's `get_file_problems` inspection reports no errors for the provenance
  inventory. This checks inspections, not browser navigation.
- A source scan after restoration found 24 cross-file fragment links across README,
  PLAN, AGENTS and Markdown files under docs, including 11 in the provenance inventory.
  This counts links of the relevant form; it does not establish that each fails.
- The selected link temporarily used a plain relative file path with the target
  section named beside it. No other fragment links were removed during this investigation.
- The author reported upvoting PY-93086 and chose to restore the selected heading
  link and retain standard cross-file anchors. The link is restored; this decision
  preserves precise destinations and does not establish that the preview bug is fixed.

Use source-editor Go to Declaration/navigation on a link as the reported workaround,
or follow a plain file link and locate the named heading. Exact gestures depend
on the active keymap. These alternatives have not been clicked through locally
in this investigation. Keep valid cross-file fragments for renderers that support
them; do not rewrite the repository or add HTML anchors on speculation.

If local diagnosis becomes necessary, record the exact IDEA build, Markdown plugin
and JCEF versions, then compare one same-file heading link, a plain cross-file
link and a cross-file heading link in source versus preview. Preserve indexing
state and the observed result. Only then choose a broader workaround or report
our reproduction to JetBrains. The agent submitted no issue/comment; the upvote
is author-reported.

Research used JetBrains documentation, indexed YouTrack content and the JetBrains
support page through web search, plus a source scan and IDEA inspection. Direct
opening of PY-93086 failed in the research tool; its content/status were available
in indexed results, so live fix status was not independently verified. No complete
local preview reproduction, plugin setting change or application test was performed.
