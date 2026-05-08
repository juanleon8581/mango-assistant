## MODIFIED Requirements

### Requirement: Default config exists as a package resource file
The system SHALL provide the default configuration template as a YAML file (`config.default.yaml`) located inside the `mango` package directory and declared as package data so it is included in all distribution formats.

#### Scenario: File is accessible after pip install
- **WHEN** the `mango` package is installed via `pip install`
- **THEN** `importlib.resources.files("mango").joinpath("config.default.yaml")` SHALL resolve to a readable file

#### Scenario: File contains valid YAML
- **WHEN** `config.default.yaml` is read
- **THEN** its content SHALL be parseable by `yaml.safe_load` without errors

### Requirement: ensure_config propagates default config on every startup
`ensure_config()` SHALL propagate the `config.default.yaml` package resource to `~/.config/mango/config.default.yaml` on every startup, writing the file only when its content differs from the package resource (SHA-256 hash comparison).

#### Scenario: First run creates config.default.yaml in user config dir
- **WHEN** `config.default.yaml` does not exist in the user config directory
- **THEN** `ensure_config()` SHALL create it with the content of the package resource

#### Scenario: Startup after package upgrade overwrites config.default.yaml
- **WHEN** the package resource `config.default.yaml` has different content than the user's copy
- **THEN** `ensure_config()` SHALL overwrite the user's file with the new package resource content

#### Scenario: Unchanged resource — no write performed
- **WHEN** the package resource and the user's `config.default.yaml` have identical content
- **THEN** `ensure_config()` SHALL NOT write to the file
