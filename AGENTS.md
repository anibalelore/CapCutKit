# Local Windows adaptation

Read the Windows section of README.md. Use `uv run capcut-bridge.py doctor`
and `ls` to locate drafts. Use `state --draft <name>` to read saved timelines.
The JSON backend handles normal shutdown, backup, and native cache invalidation.
Never bypass it to edit a running CapCut project. Backups are under the draft
root's `.bridge-backups` and preserve metadata and Timelines, excluding media.

Use the installed computer-use skill and its supported sky APIs for Windows UI
actions. The original macOS accessibility commands and export offsets do not
apply here. Do not publish or share media as part of export.

Text templates are absent until extracted from a local styled text segment.
Replay is experimental until the new draft is opened and verified in CapCut.
Validate changes with test_windows.py using temporary draft roots.
