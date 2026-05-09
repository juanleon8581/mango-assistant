## 1. Rename Package Resource

- [x] 1.1 Rename `src/mango/default_config.yaml` to `src/mango/config.default.yaml`
- [x] 1.2 Update `pyproject.toml` package data declaration and all code references (`config.py`, any other file) from `default_config.yaml` to `config.default.yaml`

## 2. Update ensure_config() — Default Propagation

- [x] 2.1 Add a `_file_sha256(path: Path) -> str` helper in `config.py` that returns the SHA-256 hex digest of a file's content
- [x] 2.2 Replace the current `ensure_config()` with new logic: propagate the `config.default.yaml` package resource to `~/.config/mango/config.default.yaml` on every startup, writing only when the file is absent or the hash differs from the resource

## 3. Implement Merge Engine

- [x] 3.1 Create `src/mango/merger.py` with a `merge_configs(config_dir: Path) -> list[str]` function that applies category merge rules (exact match → merge macros, new category → include entirely, partial match → omit + collect warning)
- [x] 3.2 Add macro merge logic inside the shared-category branch: include a local macro only if neither its key nor its shortcut collides with any default macro in that category; otherwise collect a warning
- [x] 3.3 Write the merged `categories` dict to `commands.yaml` using `yaml.dump` and print each collected warning to stderr with the `[mango] config conflict:` prefix

## 4. Implement Lazy Hash Sidecar

- [x] 4.1 Add `_load_merge_state(config_dir: Path) -> dict` and `_save_merge_state(config_dir: Path, default_hash: str, local_hash: str | None) -> None` helpers in `merger.py` that read/write `.merge-state.json`
- [x] 4.2 Add `should_merge(config_dir: Path) -> bool` to `merger.py`: returns `True` if `.merge-state.json` is absent or either source hash differs from the stored values; wire this check into `merge_configs()` so it skips the merge and returns `[]` when not needed, and updates the sidecar after a successful merge

## 5. Integration

- [ ] 5.1 Update `main.py` to call `ensure_config()` (propagate default) then `merge_configs(config_dir)` (lazy merge) before `MangoApp.run()`, so `commands.yaml` is always up-to-date when the TUI opens
- [ ] 5.2 Smoke-test the full flow using `XDG_CONFIG_HOME=.test-config mango`: verify `config.default.yaml` is created, `commands.yaml` is written, `.merge-state.json` is present, and a second run skips the merge
