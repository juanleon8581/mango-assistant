## Context

`config.py` actualmente contiene `EXAMPLE_CONFIG`, una string literal de ~47 líneas con el contenido YAML del config inicial del usuario. Esta string vive en el mismo módulo que el parser, los modelos de datos y la lógica de rutas. Es contenido de datos, no lógica — su lugar no es un archivo `.py`.

Python ofrece `importlib.resources` como mecanismo estándar para acceder a archivos que se distribuyen junto con un paquete instalado.

## Goals / Non-Goals

**Goals:**
- Mover `EXAMPLE_CONFIG` a `src/mango/default_config.yaml`
- Leer ese archivo en runtime usando `importlib.resources.files()`
- Asegurar que el archivo quede incluido en instalaciones via `pip` (package-data)
- Mantener el comportamiento externo de `ensure_config()` sin cambios

**Non-Goals:**
- Cambiar el contenido del config por defecto
- Modificar `load_config()`, `get_config_path()` o `interpolate()`
- Agregar validación del archivo de recursos

## Decisions

### 1. `importlib.resources.files()` sobre `Path(__file__).parent`

`Path(__file__).parent / "default_config.yaml"` funciona en desarrollo (`pip install -e .`) pero no está garantizado en todos los modos de distribución (e.g., zipimport, namespace packages). `importlib.resources.files()` es la API estándar de Python 3.9+ para recursos de paquete y funciona correctamente en todos los contextos de instalación.

```python
from importlib.resources import files
content = files("mango").joinpath("default_config.yaml").read_text(encoding="utf-8")
```

El proyecto requiere Python ≥ 3.10, por lo que esta API está disponible sin condiciones.

**Alternativa descartada:** `pkg_resources` (setuptools) — API legacy, añade dependencia innecesaria.

### 2. Archivo `.yaml` en `src/mango/` (no en subdirectorio)

El archivo vive al mismo nivel que `config.py`. No hay razón para introducir un subdirectorio `resources/` para un solo archivo. Si en el futuro hubiera más recursos, se puede reorganizar entonces.

### 3. `package-data` explícito en `pyproject.toml`

setuptools no incluye archivos no-Python automáticamente. Hay que declararlo:

```toml
[tool.setuptools.package-data]
mango = ["*.yaml"]
```

Esto garantiza que `default_config.yaml` se copie al directorio del paquete instalado.

## Risks / Trade-offs

- **[Riesgo] El archivo `.yaml` no se incluye en la distribución** → Mitigación: la entrada `package-data` en `pyproject.toml` lo resuelve; si falta, `importlib.resources` lanza `FileNotFoundError` inmediatamente al primer uso.
- **[Trade-off] Un import más en `config.py`** → Aceptable; `importlib.resources` es stdlib.
