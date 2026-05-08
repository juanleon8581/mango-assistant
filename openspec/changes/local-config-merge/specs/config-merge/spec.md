## ADDED Requirements

### Requirement: Lazy merge via hash sidecar
The system SHALL maintain a `.merge-state.json` sidecar file in the mango config directory, storing the SHA-256 hashes of `config.default.yaml` and `config.local.yaml` (or `null` if the local file is absent) recorded at the time of the last merge.

#### Scenario: Merge is skipped when hashes match
- **WHEN** the SHA-256 hashes of both source files match the values stored in `.merge-state.json`
- **THEN** the merge SHALL be skipped and `commands.yaml` SHALL be left unchanged

#### Scenario: Merge runs when default hash changes
- **WHEN** the hash of `config.default.yaml` differs from the stored `default_hash`
- **THEN** the merge SHALL run and `.merge-state.json` SHALL be updated with the new hashes

#### Scenario: Merge runs when local hash changes
- **WHEN** the hash of `config.local.yaml` differs from the stored `local_hash`
- **THEN** the merge SHALL run and `.merge-state.json` SHALL be updated with the new hashes

#### Scenario: Merge runs when sidecar is absent
- **WHEN** `.merge-state.json` does not exist in the config directory
- **THEN** the merge SHALL run unconditionally

### Requirement: Category merge rules
During merge, a local category SHALL be included in `commands.yaml` only if it is an exact match (same key AND same shortcut as a default category, triggering macro-level merge) or a new category (key not present in default AND shortcut not used by any default category). Any other combination SHALL be treated as a conflict and the local category SHALL be omitted entirely.

#### Scenario: Exact match category — macros are merged
- **WHEN** a local category has the same key and same shortcut as a default category
- **THEN** its valid local macros SHALL be added to that category in the merged output

#### Scenario: New category — included entirely
- **WHEN** a local category has a key not present in default AND a shortcut not used by any default category
- **THEN** the entire local category SHALL be included in `commands.yaml`

#### Scenario: Same key, different shortcut — conflict
- **WHEN** a local category has the same key as a default category but a different shortcut
- **THEN** the local category SHALL be omitted and a conflict warning SHALL be emitted to stderr

#### Scenario: Different key, same shortcut — conflict
- **WHEN** a local category has a different key but the same shortcut as a default category
- **THEN** the local category SHALL be omitted and a conflict warning SHALL be emitted to stderr

### Requirement: Macro merge rules within shared categories
Within a category that exists in both default and local, a local macro SHALL be included only if its key does not already exist in the default macros for that category AND its shortcut does not already exist among the default macro shortcuts for that category.

#### Scenario: New key and new shortcut — macro included
- **WHEN** a local macro has a key and shortcut not present among the default macros of its category
- **THEN** the local macro SHALL be added to the merged category

#### Scenario: Duplicate macro key — macro omitted with warning
- **WHEN** a local macro has the same key as a default macro in the same category
- **THEN** the local macro SHALL be omitted and a conflict warning SHALL be emitted to stderr

#### Scenario: Duplicate macro shortcut — macro omitted with warning
- **WHEN** a local macro has the same shortcut as a default macro in the same category
- **THEN** the local macro SHALL be omitted and a conflict warning SHALL be emitted to stderr

#### Scenario: Macro shortcut scope is per-category
- **WHEN** the same shortcut string exists in two different categories (one from default, one from local)
- **THEN** it SHALL NOT be treated as a conflict

### Requirement: Merge output is commands.yaml
The merge result SHALL be written to `commands.yaml` in the mango config directory, which is the file `load_config()` reads at runtime.

#### Scenario: commands.yaml is written after merge
- **WHEN** the merge runs
- **THEN** `commands.yaml` SHALL be created or overwritten with the merged config in valid YAML format

### Requirement: Conflict warnings reported to stderr before TUI opens
All conflict warnings from the merge SHALL be printed to stderr before the Textual TUI opens, using the prefix `[mango] config conflict:`.

#### Scenario: Category conflict warning format
- **WHEN** a local category is omitted due to a conflict
- **THEN** a line SHALL be printed to stderr in the format: `[mango] config conflict: category '<key>' — <reason> (skipped)`

#### Scenario: Macro conflict warning format
- **WHEN** a local macro is omitted due to a conflict
- **THEN** a line SHALL be printed to stderr in the format: `[mango] config conflict: macro '<category>><key>' — <reason> (skipped)`

#### Scenario: TUI opens normally after warnings
- **WHEN** one or more conflict warnings are emitted
- **THEN** the TUI SHALL open normally after all warnings are printed
