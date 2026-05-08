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

On first run, a sample config is created at `~/.config/mango/commands.yaml` (respects `$XDG_CONFIG_HOME`).

Navigate with arrow keys or `j`/`k`. Press `Enter` to run a macro. If the macro has params, a dialog prompts for them before execution. Output streams to a panel at the bottom. Press `q` to quit.

**Shortcut mode:** type `<category_shortcut>><macro_shortcut>` (e.g. `g>su`) to jump directly to a macro from anywhere in the TUI.

## Config

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
  docker:
    shortcut: "d"
    macros:
      up:
        shortcut: "up"
        description: "Start containers"
        steps:
          - docker compose up -d
      logs:
        shortcut: "lg"
        description: "Follow logs for a service"
        params:
          - name: service
            prompt: "Service name"
        steps:
          - docker compose logs -f {service}
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
