## Why

El `default_config.yaml` actualmente se copia al directorio del usuario una sola vez y nunca se actualiza — los macros nuevos o mejorados en el paquete nunca llegan a instalaciones existentes. Se necesita un mecanismo donde el default siempre esté vigente y el usuario pueda mantener sus propios macros de forma persistente entre actualizaciones.

## What Changes

- `default_config.yaml` (package resource) se renombra a `config.default.yaml`.
- En cada startup, el package resource `config.default.yaml` se copia a `~/.config/mango/config.default.yaml`, actualizando el archivo si el contenido difiere.
- Se introduce `~/.config/mango/config.local.yaml` como archivo opcional del usuario para macros personales, persiste entre actualizaciones.
- Ambos archivos se mergean para producir `~/.config/mango/commands.yaml` con prioridad del default sobre el local.
- El merge es lazy: solo se ejecuta si los hashes de `config.default.yaml` o `config.local.yaml` cambiaron respecto al último merge, usando un sidecar `~/.config/mango/.merge-state.json`.
- Conflictos (key o shortcut duplicado) se omiten del local y se reportan por stderr antes de que el TUI abra.
- `commands.yaml` existente de instalaciones previas es ignorado sin migración.

## Capabilities

### New Capabilities

- `local-user-config`: Archivo `config.local.yaml` en `~/.config/mango/` — estructura, ubicación y ciclo de vida (opcional, persiste entre actualizaciones del paquete).
- `config-merge`: Algoritmo de merge entre default y local con reglas de prioridad, detección de conflictos, y merge lazy via hash sidecar (`.merge-state.json`).

### Modified Capabilities

- `default-config-resource`: El package resource se renombra de `default_config.yaml` a `config.default.yaml`. El comportamiento de `ensure_config()` cambia — en lugar de copiar el default al directorio del usuario una sola vez, ahora lo propaga en cada startup si el contenido difiere.

## Impact

- `src/mango/config.default.yaml`: renombrado desde `default_config.yaml`.
- `src/mango/config.py`: `ensure_config()` actualizada para propagar `config.default.yaml`; nueva función `check_and_merge()` que coordina detección de cambios via hash y ejecuta merge si es necesario; nueva función `merge_configs(default, local) → (Config, list[str])`.
- `src/mango/main.py`: imprime warnings del merge a stderr antes de lanzar el TUI.
- `pyproject.toml`: actualizar referencia de package data de `default_config.yaml` a `config.default.yaml`.
- No hay cambios en `runner.py`, `tui/app.py`, ni en el schema del YAML de configuración.
- Usuarios existentes con `commands.yaml` personalizado deben migrar manualmente a `config.local.yaml`.
