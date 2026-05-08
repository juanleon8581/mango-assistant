## ADDED Requirements

### Requirement: Default config exists as a package resource file
The system SHALL provide the default configuration template as a YAML file (`default_config.yaml`) located inside the `mango` package directory and declared as package data so it is included in all distribution formats.

#### Scenario: File is accessible after pip install
- **WHEN** the `mango` package is installed via `pip install`
- **THEN** `importlib.resources.files("mango").joinpath("default_config.yaml")` SHALL resolve to a readable file

#### Scenario: File contains valid YAML
- **WHEN** `default_config.yaml` is read
- **THEN** its content SHALL be parseable by `yaml.safe_load` without errors

### Requirement: ensure_config reads default template from package resource
`ensure_config()` SHALL read the default config content from the `default_config.yaml` package resource using `importlib.resources`, and write it to the user config path when the file does not yet exist.

#### Scenario: First run creates config from resource
- **WHEN** the user config file does not exist
- **THEN** `ensure_config()` SHALL create it with the content of `default_config.yaml`

#### Scenario: Existing config is not overwritten
- **WHEN** the user config file already exists
- **THEN** `ensure_config()` SHALL leave it unchanged

### Requirement: EXAMPLE_CONFIG constant is removed from config.py
The `EXAMPLE_CONFIG` string constant SHALL be removed from `config.py`. No other module SHALL define an inline YAML string as a substitute.

#### Scenario: config.py has no inline YAML string
- **WHEN** `config.py` is read
- **THEN** it SHALL contain no multi-line string literal with YAML category/macro structure
