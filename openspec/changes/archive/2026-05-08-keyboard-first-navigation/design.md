## Context

La TUI está construida con Textual. El `MainScreen` tiene tres widgets focusables en orden DOM:
1. `#category-list` (ListView)
2. `#macro-list` (ListView)
3. `#shortcut-input` (Input)

Textual tiene un mecanismo nativo `focus_next` / `focus_previous` que cicla en orden DOM, y el Screen ya declara `tab` como binding a `focus_next`. El problema: cuando un `ListView` tiene el foco, puede interceptar Tab internamente antes de que llegue al Screen, rompiendo el ciclo.

El display bug ocurre porque `Label` en Textual usa Rich markup por defecto, y `[su]` es interpretado como un tag de estilo (inválido → silenciado).

## Goals / Non-Goals

**Goals:**
- Tab cicla de forma confiable: `category-list → macro-list → shortcut-input → category-list`
- Enter en `category-list` mueve el foco a `macro-list`
- `[shortcut]` se muestra correctamente como texto literal en los labels
- Parámetros se muestran como `<param_name>` inline en la descripción

**Non-Goals:**
- Navegación con flechas izquierda/derecha entre paneles
- Cambios en lógica de ejecución de macros
- Modificaciones a config, runner, o cualquier otro módulo

## Decisions

### D1 — Ciclo Tab: override explícito de `action_focus_next`

**Decisión**: Sobrescribir `action_focus_next` (y `action_focus_previous`) en `MainScreen` con un ciclo hardcodeado de los tres widgets en vez de depender de `focus_next` nativo de Textual.

**Alternativa descartada**: Confiar en el `focus_next` nativo de Textual. El problema es que ListView puede capturar Tab internamente y el comportamiento puede variar entre versiones de Textual. Un ciclo explícito es predecible y fácil de entender.

**Implementación**:
```python
_FOCUS_CYCLE = ["#category-list", "#macro-list", "#shortcut-input"]

def action_focus_next(self) -> None:
    focused = self.focused
    ids = [w.id for w in self.query("ListView, Input")]
    # encontrar posición actual y avanzar al siguiente
    ...
```

Más simple aún: lista estática de IDs en orden, buscar el actual, avanzar con módulo.

### D2 — Enter en category-list: handler `ListView.Selected`

**Decisión**: Agregar `@on(ListView.Selected, "#category-list")` que llame `self.query_one("#macro-list").focus()`.

`ListView.Selected` se dispara con Enter sobre el item resaltado. Ya existe el handler `@on(ListView.Highlighted, "#category-list")` que actualiza el contenido del macro-list — `Selected` complementa con el cambio de foco.

### D3 — Fix markup: escapar corchetes con `\[`

**Decisión**: En Rich/Textual markup, `\[` se renderiza como `[` literal. Cambiar el f-string de:
```python
f"[{shortcut}] {description}"
```
a:
```python
f"\\[{shortcut}] {description}"
```

**Alternativa descartada**: `Label(..., markup=False)`. Funciona pero bloquea el uso futuro de estilos Rich en los labels (colores para item seleccionado, etc.). Escapar el corchete es más preciso.

### D4 — Formato de parámetros: `<param>` inline

**Decisión**: Cambiar `params_hint` de:
```python
f"  ({', '.join(p.name for p in macro.params)})"
```
a:
```python
" ".join(f"<{p.name}>" for p in macro.params)
```
y concatenarlo directamente después de la descripción con un espacio.

Resultado: `\[su] Switch branch, fetch and pull <branch>`

## Risks / Trade-offs

- **[Risk] Textual actualiza ListView y cambia cómo maneja Tab** → El override explícito de `action_focus_next` nos aísla de ese cambio; es más resiliente que depender del nativo.
- **[Trade-off] Ciclo hardcodeado**: Si en el futuro se agrega un cuarto widget focusable, hay que actualizar la lista manualmente. Aceptable dado el alcance acotado del proyecto.

## Open Questions

Ninguna. El diseño está completo y acotado a `app.py`.
