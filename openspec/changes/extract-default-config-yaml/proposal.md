## Why

`config.py` mezcla responsabilidades: parseo de YAML, modelos de datos, y el template del config por defecto embebido como string de Python. El template de configuración es contenido YAML, no lógica — separarlos permite editarlo, leerlo y validarlo como lo que es.

## What Changes

- Se crea `src/mango/default_config.yaml` con el contenido actualmente en `EXAMPLE_CONFIG`
- Se elimina la constante `EXAMPLE_CONFIG` de `config.py`
- `ensure_config()` lee el archivo YAML usando `importlib.resources` en lugar de la constante
- Se agrega `package-data` en `pyproject.toml` para incluir `*.yaml` en la distribución

## Capabilities

### New Capabilities

- `default-config-resource`: El config por defecto existe como archivo YAML independiente, empaquetado como recurso del paquete y leído en tiempo de ejecución vía `importlib.resources`.

### Modified Capabilities

<!-- No hay cambios en requisitos de specs existentes -->

## Impact

- `src/mango/config.py`: se elimina `EXAMPLE_CONFIG`, se modifica `ensure_config()`
- `src/mango/default_config.yaml`: archivo nuevo
- `pyproject.toml`: se agrega `[tool.setuptools.package-data]`
- Sin cambios en la interfaz pública de `config.py` — `load_config()`, `get_config_path()`, `interpolate()` no cambian
