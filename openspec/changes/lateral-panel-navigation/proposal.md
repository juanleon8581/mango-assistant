## Why

Al usar mango, el instinto natural es presionar `→` para pasar del panel de categorías al de macros, y `←` para regresar — el mismo modelo mental de TUIs como `ranger`, `lazygit` o `mc`. Hoy ese gesto no hace nada, rompiendo la expectativa del usuario.

## What Changes

- `→` desde `category-list` mueve el foco a `macro-list` (sin disparar selección)
- `←` desde `macro-list` mueve el foco de vuelta a `category-list`
- `←` desde `category-list` y `→` desde `macro-list` no hacen nada (no hay panel en esa dirección)
- Las teclas `←`/`→` dentro de un `Input` nunca se interceptan (son movimiento de cursor)

## Capabilities

### New Capabilities

_(ninguna — no se introduce una capacidad nueva, se extiende una existente)_

### Modified Capabilities

- `keyboard-navigation`: agregar navegación lateral entre paneles con `←`/`→`

## Impact

- `src/mango/tui/app.py` — método `on_key` en `MainScreen`
- Sin cambios en config, runner, ni dependencias externas
