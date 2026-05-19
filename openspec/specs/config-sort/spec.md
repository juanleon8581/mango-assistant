# Spec: config-sort

## Purpose

Define how mango sorts categories and macros after loading the merged config, ensuring a consistent and predictable display order independent of YAML insertion order.

## Requirements

### Requirement: Categories sorted by shortcut length then name
After loading the merged config, the system SHALL sort categories by `(len(shortcut), name)` in ascending order. Categories with shorter shortcuts SHALL appear before those with longer shortcuts. Within the same shortcut length, categories SHALL be ordered alphabetically by their YAML key.

#### Scenario: Mixed shortcut lengths
- **WHEN** the config has categories with shortcuts of different lengths (e.g., `g`, `d`, `help`)
- **THEN** single-char shortcut categories appear first, sorted alphabetically (`d`, `g`), followed by longer-shortcut categories (`help`)

#### Scenario: All same length shortcuts
- **WHEN** all categories have shortcuts of the same length
- **THEN** categories are sorted alphabetically by name regardless of YAML file order

#### Scenario: Custom local category included in sort
- **WHEN** a user-defined category from `config.local.yaml` is merged into `commands.yaml`
- **THEN** it participates in the same sort order as default categories, not appended at the end

### Requirement: Macros sorted by shortcut length then description
Within each category, the system SHALL sort macros by `(len(shortcut), description)` in ascending order. Macros with shorter shortcuts SHALL appear first. Within the same shortcut length, macros SHALL be ordered alphabetically by their `description` field.

#### Scenario: Mixed shortcut lengths in macros
- **WHEN** a category contains macros with shortcuts of different lengths (e.g., `a`, `bc`)
- **THEN** the single-char shortcut macro appears before 2-char shortcut macros

#### Scenario: Same length shortcuts sorted by description
- **WHEN** multiple macros share the same shortcut length
- **THEN** they are ordered alphabetically by description — macros with `"branch | ..."` descriptions group together before `"git | ..."` descriptions

#### Scenario: Custom local macro included in sort
- **WHEN** a user-defined macro is merged into an existing category
- **THEN** it is sorted among the category's macros by the same `(len(shortcut), description)` rule
