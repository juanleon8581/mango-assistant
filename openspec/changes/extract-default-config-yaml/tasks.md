## 1. Crear el archivo de recurso

- [ ] 1.1 Crear `src/mango/default_config.yaml` con el contenido actualmente en `EXAMPLE_CONFIG`

## 2. Actualizar configuración del paquete

- [ ] 2.1 Agregar `[tool.setuptools.package-data]` en `pyproject.toml` para incluir `*.yaml`

## 3. Actualizar config.py

- [ ] 3.1 Eliminar la constante `EXAMPLE_CONFIG` de `config.py`
- [ ] 3.2 Modificar `ensure_config()` para leer el contenido desde `importlib.resources`

## 4. Verificación

- [ ] 4.1 Ejecutar `mango` con `XDG_CONFIG_HOME=.test-config` y verificar que crea el archivo de config correctamente desde el recurso
