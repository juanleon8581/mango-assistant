## Context

Categories and macros are stored as `dict[str, ...]` in `config.py`, preserving YAML insertion order. After `merger.py` merges default + local configs into `commands.yaml`, `load_config()` parses the result into a `Config` object. Currently no ordering is applied — display order is whatever the YAML had.

The sort must happen after the merge so custom local macros participate in the same ordering as default macros.

## Goals / Non-Goals

**Goals:**
- Deterministic, predictable display order for categories and macros
- Short shortcuts surface first (faster visual scan for keyboard-driven users)
- Custom local macros sorted together with default ones, not appended at the end

**Non-Goals:**
- User-configurable sort order (not needed — one sensible default is enough)
- Sorting within `merger.py` or `app.py`
- Any changes to config schema or shortcut resolution logic

## Decisions

### Sort location: `config.py` at parse time, not `app.py` at render time

`load_config()` reads the already-merged `commands.yaml`. Applying sort here means the `Config` object always carries ordered data — consistent for any future consumer (CLI, tests, etc.). Sorting in `app.py` would scatter the logic into the presentation layer and require two sort sites (`on_mount` and `_populate_macros`).

**Alternative considered**: Sort in `app.py`
- Pro: keeps the data model neutral
- Con: two call sites, presentation concern leaks sorting logic, doesn't benefit future non-TUI consumers

### Sort key: `(len(shortcut), description_or_name)`

Primary key `len(shortcut)` groups by typing effort — single-char shortcuts first, then 2-char, etc. Secondary key alpha-sorts within each length group.

- Categories: `(len(cat.shortcut), cat.name)` — `name` is the YAML key (e.g., `git`, `docker`)
- Macros: `(len(macro.shortcut), macro.description)` — description is user-facing and often prefixed (`"branch | create"`, `"branch | delete"`), which clusters related macros naturally

**Alternative considered**: Sort macros by YAML key instead of description
- YAML keys are internal identifiers (`create-branch-push`), not what users read in the TUI
- Description sort produces a better visual grouping in the panel

## Risks / Trade-offs

- **User workflow order lost** → Users who organized their YAML by workflow (not alpha) will see a reordered list. Mitigation: the sort is deterministic and predictable — users adapt once.
- **Description-based sort depends on naming convention** → Only groups macros nicely if descriptions use a `"prefix | action"` pattern. Macros with unstructured descriptions will still be sorted correctly, just without semantic grouping.

## Migration Plan

No migration needed. Sort is applied transparently at parse time. Existing configs require no changes.
