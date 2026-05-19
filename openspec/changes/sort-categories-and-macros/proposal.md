## Why

Categories and macros currently render in YAML insertion order, which is arbitrary and inconsistent — especially after merging default + local configs. Users scanning the TUI or shortcut bar have no predictable layout to rely on.

## What Changes

- Categories sorted by `(len(shortcut), name)` — single-char shortcuts first, then alphabetically within each length group
- Macros within each category sorted by `(len(shortcut), description)` — same rule applied to macros
- Sort applied once at parse time, after the default+local merge, so custom user macros are included in the global ordering

## Capabilities

### New Capabilities
- `config-sort`: Deterministic ordering of categories and macros by shortcut length then alphabetically by description

### Modified Capabilities
- `macro-catalog`: Display order of categories and macros now follows a defined sort rule, not YAML insertion order

## Impact

- `src/mango/config.py`: `load_config` and `_parse_category` — add `sorted()` calls when building the `categories` and `macros` dicts
- No changes to `merger.py`, `app.py`, or any other file
- No breaking changes to config schema or shortcut resolution
