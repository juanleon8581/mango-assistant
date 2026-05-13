## Context

La TUI de mango tiene tres paneles: `category-list`, `macro-list` y `shortcut-input`. La navegación entre ellos hoy se hace con `Tab`/`Shift+Tab` y con `Enter` desde el `category-list`. Las teclas `←`/`→` no están ligadas a ningún comportamiento, aunque el instinto del usuario es usarlas para moverse lateralmente entre paneles.

El widget `ListView` de Textual captura `↑`/`↓` y `Enter`, pero **no** captura `←`/`→`. Esas teclas burbujean hasta el `Screen`.

## Goals / Non-Goals

**Goals:**
- `→` en `category-list` mueve el foco a `macro-list`
- `←` en `macro-list` mueve el foco a `category-list`
- Las teclas `←`/`→` dentro de `Input` no se interceptan

**Non-Goals:**
- Cambiar el comportamiento de `Tab`/`Shift+Tab`
- Agregar animaciones o indicadores visuales de navegación lateral
- Soporte de `←`/`→` en el `shortcut-input`

## Decisions

### Decisión: usar `on_key` en `MainScreen` en lugar de `BINDINGS`

`BINDINGS` de Textual es declarativo y adecuado para acciones globales. Sin embargo, la navegación lateral requiere **contexto**: la misma tecla (`→`) debe ignorarse si el foco está en `macro-list` o en un `Input`. Ese chequeo condicional es más claro en `on_key`, que ya se usa en el mismo archivo para `q`.

**Alternativa descartada — BINDINGS con `action_panel_right`/`action_panel_left`**: Requeriría duplicar la lógica de chequeo de foco dentro de los action methods o usar `check_action`. La ganancia declarativa no compensa la complejidad extra para un caso tan puntual.

### Decisión: no disparar `ListView.Selected` al presionar `→`

`→` solo mueve el foco. El `macro-list` ya está populado por el evento `ListView.Highlighted` que se dispara al navegar con `↑`/`↓` en `category-list`. No es necesario re-seleccionar para tener el contenido correcto.

## Risks / Trade-offs

- **[Riesgo] Textual cambia el comportamiento de `←`/`→` en `ListView` en versiones futuras** → Si `ListView` empieza a capturar esas teclas, dejarían de burbujear y `on_key` no las vería. Mitigación: el comportamiento es fácil de verificar manualmente; pin de versión de Textual en `pyproject.toml` ya existe.
- **[Trade-off] `on_key` acumula responsabilidades** → Ya maneja `q`; agregar `←`/`→` lo hace crecer. Aceptable dado el tamaño pequeño del módulo.
