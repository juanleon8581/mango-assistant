## Context

Actualmente `config.py` tiene una función `ensure_config()` que copia el package resource `default_config.yaml` al directorio del usuario una única vez. Si el paquete se actualiza con nuevos macros, el usuario no recibe esos cambios. Tampoco existe un mecanismo oficial para que el usuario agregue macros propios sin riesgo de que sean sobreescritos.

El cambio introduce tres archivos en `~/.config/mango/`:

- `config.default.yaml` — propagado desde el package resource en cada startup
- `config.local.yaml` — macros del usuario (opcional)
- `commands.yaml` — resultado del merge, leído por la app en runtime

## Goals / Non-Goals

**Goals:**

- Los macros default siempre reflejan la versión instalada del paquete
- El usuario puede definir macros propios que persisten entre actualizaciones
- El merge se ejecuta solo cuando es necesario (lazy)
- Los conflictos son visibles para el usuario antes de entrar al TUI

**Non-Goals:**

- Migración automática de `commands.yaml` existente
- Edición de `config.local.yaml` desde dentro del TUI
- Soporte para múltiples archivos local o perfiles

## Decisions

### 1. Tres archivos en lugar de uno

**Decisión:** `config.default.yaml` + `config.local.yaml` → `commands.yaml` (merge output)

El archivo leído por la app en runtime siempre es `commands.yaml`. Esto desacopla el sistema de merge del sistema de carga — `load_config()` no cambia, sigue leyendo un único YAML.

Alternativa descartada: leer y mergear en memoria en cada startup. Requiere cambiar la firma de `load_config()` y complica la lógica de carga sin beneficio real para un tool personal.

### 2. Lazy merge via hash sidecar

**Decisión:** `.merge-state.json` almacena los hashes SHA-256 de las fuentes al momento del último merge.

```json
{
  "default_hash": "<sha256 de config.default.yaml>",
  "local_hash": "<sha256 de config.local.yaml | null si no existe>"
}
```

On startup: si los hashes actuales coinciden con los almacenados → skip merge. Cualquier diferencia → re-merge + actualizar sidecar.

Alternativa descartada: comparación por mtime. Menos confiable (editors, cp, rsync pueden alterar mtime sin cambiar contenido).

### 3. Propagación del package resource

**Decisión:** en cada startup, el package resource `config.default.yaml` se propaga a `~/.config/mango/config.default.yaml` solo si el contenido difiere (comparación de hashes antes de escribir).

Esto garantiza que el usuario siempre tenga el default actualizado tras un `pip install --upgrade`, sin escrituras innecesarias en cada run.

### 4. Reglas de merge — categorías

Una categoría local es válida en uno de dos casos:

```
Exacta match  (key == default_key AND shortcut == default_shortcut) → merge de macros
Nueva         (key no existe en default AND shortcut no existe en default) → agregar completa
```

Cualquier match parcial es CONFLICTO → categoría local omitida + warning:

- Mismo key, distinto shortcut: `git (gi)` cuando default tiene `git (g)`
- Distinto key, mismo shortcut: `tools (g)` cuando default tiene `git (g)`

### 5. Reglas de merge — macros

Dentro de categorías compartidas, un macro local es válido solo si:

- Su **key** no existe en los macros default de esa categoría
- Su **shortcut** no existe en los shortcuts de macros default de esa categoría

Los shortcuts de macros tienen scope por categoría: `g>st` y `d>st` son independientes.

### 6. Reporte de conflictos

**Decisión:** stderr antes de que el TUI abra.

```
[mango] config conflict: category 'tools' — shortcut 'g' already used by 'git' (skipped)
[mango] config conflict: macro 'git>status' — key already defined in default (skipped)
```

El TUI abre normalmente después. El usuario puede editar `config.local.yaml` y relanzar.

## Risks / Trade-offs

- **`.merge-state.json` desincronizado**: Si el usuario edita manualmente `commands.yaml`, el sidecar queda stale y el merge no se reejecutará. Mitigación: documentar que `commands.yaml` es generado — no editar manualmente.
- **Rename del package resource**: cualquier código que referencie `default_config.yaml` por nombre hardcodeado romperá. Mitigación: grep completo antes de implementar.
- **`commands.yaml` previo ignorado**: usuarios con personalizaciones en `commands.yaml` las perderán silenciosamente. Aceptable para un proyecto personal en etapa temprana.

## Migration Plan

1. Renombrar `src/mango/default_config.yaml` → `src/mango/config.default.yaml`
2. Actualizar `pyproject.toml` y cualquier referencia en `config.py`
3. Reemplazar `ensure_config()` con la nueva lógica de propagación + merge lazy
4. El archivo `commands.yaml` existente en el sistema del usuario será sobreescrito en el próximo startup si los hashes no coinciden (que será siempre, ya que el sidecar no existirá)
