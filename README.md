# mango

A keyboard-driven terminal UI for running multi-step shell command sequences defined in YAML.

## What it does

mango lets you define "macros" — named sequences of shell commands — grouped into categories. You run them by navigating the TUI or typing shortcut combos like `g>su` (category `g`, macro `su`). Macros can prompt for parameters before running.

## Requirements

- Python 3.10+

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Usage

```bash
mango
```

Navigate with arrow keys or `j`/`k`. Press `Enter` to run a macro. If the macro has params, a dialog prompts for them before execution. Output streams to a panel at the bottom. Press `q` to quit.

**Shortcut mode:** type `<category_shortcut>><macro_shortcut>` (e.g. `g>su`) to jump directly to a macro from anywhere in the TUI.

## Config

mango manages three files under `~/.config/mango/` (respects `$XDG_CONFIG_HOME`):

| File | Purpose |
|---|---|
| `config.default.yaml` | Macros bundled with the package — updated automatically on each startup |
| `config.local.yaml` | Your personal macros — optional, persists across package updates |
| `commands.yaml` | Merge output read by the app — **do not edit manually** |

On each startup mango propagates the built-in defaults and merges them with your local config into `commands.yaml`. The merge is lazy: it only runs when either source file changes.

### Adding your own macros

Create `~/.config/mango/config.local.yaml` with the same YAML schema:

```yaml
categories:
  git:
    shortcut: "g"          # must match the default exactly to add macros into it
    macros:
      my-cleanup:
        shortcut: "cl"
        description: "Delete merged branches"
        steps:
          - git branch --merged | grep -v main | xargs git branch -d
  my-tools:                # entirely new category — key and shortcut must not exist in defaults
    shortcut: "t"
    macros:
      hello:
        shortcut: "hi"
        description: "Say hello"
        steps:
          - echo "hello"
```

**Merge rules:**

- To add macros into an existing default category: the category `key` and `shortcut` must match the default exactly.
- To add a new category: both the `key` and `shortcut` must not exist in the defaults.
- Within a shared category, each local macro must have a `key` and `shortcut` not already used by the defaults.

Conflicts are skipped and reported to stderr before the TUI opens:

```
[mango] config conflict: category 'tools' — shortcut 'g' already used by 'git' (skipped)
[mango] config conflict: macro 'git>status' — key already defined in default (skipped)
```

### Schema reference

```yaml
categories:
  git:
    shortcut: "g"
    macros:
      switch-and-pull:
        shortcut: "su"
        description: "Switch branch, fetch and pull"
        params:
          - name: branch
            prompt: "Branch name"
        steps:
          - git checkout {branch}
          - git fetch
          - git pull
      status:
        shortcut: "st"
        description: "Show git status"
        steps:
          - git status
```

- `shortcut` — unique within its scope (category shortcuts must be globally unique; macro shortcuts must be unique within their category)
- `params` — optional list of `{name, prompt}` pairs; referenced in steps as `{name}`
- `steps` — shell commands run sequentially; first non-zero exit code aborts the sequence

## Development

```bash
# Test with a local config instead of ~/.config/mango/
XDG_CONFIG_HOME=.test-config mango
```

Dependencies: [`textual`](https://github.com/Textualize/textual), [`pyyaml`](https://pyyaml.org/)
