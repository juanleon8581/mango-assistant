# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this project is

**mango** is a keyboard-driven terminal UI (TUI) for running multi-step shell command sequences ("macros") defined in YAML. Users navigate categories and macros via a Textual UI or by typing `cat>macro` shortcuts. It is a Python CLI tool installed via `pip install -e .`.

## Setup and running

```bash
# Create and activate venv
python3 -m venv .venv
source .venv/bin/activate

# Install in editable mode
pip install -e .

# Run
mango
```

The config file is auto-created at first run: `~/.config/mango/commands.yaml` (or `$XDG_CONFIG_HOME/mango/commands.yaml`).

**To test with a custom config during development:**

```bash
XDG_CONFIG_HOME=.test-config mango
```

## Architecture

```
src/mango/
├── config.py     # YAML parsing → Config/Category/Macro/Param dataclasses; interpolate()
├── runner.py     # run_macro() / run_step() — subprocess execution with streaming output
├── main.py       # CLI entry point: resolves config path, calls MangoApp.run()
└── tui/
    └── app.py    # Textual UI: MangoApp → MainScreen + ParamDialog modal
```

**Data flow:** `main.py` loads config → passes `Config` and `cwd` to `MangoApp` → `MainScreen` renders category/macro lists → on macro selection, `ParamDialog` collects params → `_run_worker` (thread worker) calls `runner.run_macro()` → output streams to `RichLog`.

**Key design constraints:**
- `runner.py` runs each step via `shell=True` subprocess, merging stdout+stderr. Steps run sequentially; first non-zero exit code aborts the sequence.
- Step templates use Python `str.format_map` for `{param}` interpolation — validated before execution.
- Shortcut format is `cat_shortcut>macro_shortcut` (e.g. `g>su`). Shortcuts must be unique within their scope (validated at parse time).
- The TUI output panel (`#output-log`) is hidden until a macro runs and revealed dynamically.

## Config schema

```yaml
categories:
  <key>:
    shortcut: "g"          # unique single char or string
    macros:
      <key>:
        shortcut: "su"     # unique within category
        description: "..."
        params:            # optional
          - name: branch
            prompt: "Branch name"
        steps:
          - git checkout {branch}
          - git fetch
```

## No test suite

There are currently no automated tests. Manual testing uses `.test-config/mango/commands.yaml` as shown above.
