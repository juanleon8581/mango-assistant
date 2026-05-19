## Why

When a macro runs, its output appears in the TUI's output panel but cannot be selected or copied — Textual captures the terminal in raw mode, disabling the terminal emulator's native text selection. Users frequently need to copy specific fragments (executed commands, error messages, paths) to paste elsewhere.

## What Changes

- Add `ctrl+c` keybinding that copies the full contents of the output panel to the system clipboard
- Maintain a plain-text buffer alongside the `RichLog` widget to capture output without Rich markup or ANSI codes
- Show a notification confirming the copy
- Binding is only active when the output panel has content (post-macro execution)

## Capabilities

### New Capabilities

- `output-clipboard`: Copy macro output to clipboard via `ctrl+c` when output panel is visible

### Modified Capabilities

- `tui-interface`: Output panel gains clipboard copy interaction (new keybinding and feedback notification)

## Impact

- `src/mango/tui/app.py` — only file modified
- No new dependencies (`app.copy_to_clipboard()` is built into Textual via OSC 52)
- No config schema changes
- No breaking changes
