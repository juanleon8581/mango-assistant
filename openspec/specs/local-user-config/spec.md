# Capability: Local User Config

## Purpose

TBD — Support an optional user-managed `config.local.yaml` file where users can define personal macros that are merged with the default config at startup.

## Requirements

### Requirement: config.local.yaml is an optional user config file
The system SHALL support an optional `config.local.yaml` file in the mango config directory (`~/.config/mango/` or `$XDG_CONFIG_HOME/mango/`) where users can define personal macros.

#### Scenario: App starts normally when config.local.yaml is absent
- **WHEN** `config.local.yaml` does not exist in the config directory
- **THEN** mango SHALL start normally using only the default config

#### Scenario: App reads local config when present
- **WHEN** `config.local.yaml` exists in the config directory
- **THEN** mango SHALL incorporate its categories and macros into the merged `commands.yaml` output

### Requirement: config.local.yaml follows the same YAML schema
The `config.local.yaml` file SHALL use the same `categories` YAML schema as `config.default.yaml`.

#### Scenario: Valid local config is parsed without errors
- **WHEN** `config.local.yaml` contains a valid `categories` structure
- **THEN** it SHALL be parsed by the existing config loading logic without errors

### Requirement: config.local.yaml is never written or deleted by mango
Mango SHALL never create, overwrite, or delete `config.local.yaml`. It is exclusively managed by the user.

#### Scenario: First run does not create config.local.yaml
- **WHEN** the user runs mango for the first time
- **THEN** `config.local.yaml` SHALL NOT be created in the config directory

#### Scenario: Package upgrade does not affect config.local.yaml
- **WHEN** the mango package is upgraded and the next startup runs
- **THEN** `config.local.yaml` SHALL remain unchanged on disk
