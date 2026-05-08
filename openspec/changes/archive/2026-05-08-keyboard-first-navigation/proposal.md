## Why

La TUI actual obliga a usar el mouse para cambiar entre paneles y para enfocar el campo de input, lo que rompe el flujo de trabajo en terminal. Adicionalmente, los shortcuts y parámetros de categorías y macros no se muestran correctamente porque los corchetes son interpretados como markup de Rich/Textual.

## What Changes

- **Tab cycle funcional**: Tab navega cíclicamente entre los tres focos: `category-list → macro-list → shortcut-input → category-list`.
- **Enter en category-list**: Al presionar Enter sobre una categoría, el foco se mueve al `macro-list` correspondiente.
- **Fix display de shortcuts**: Los corchetes `[shortcut]` se escapan correctamente para que Rich no los interprete como tags de markup.
- **Formato de parámetros**: Los params pasan de `(branch)` a `<branch>` inline en la descripción de la macro.

## Capabilities

### New Capabilities

- `keyboard-navigation`: Navegación completa por teclado — ciclo Tab entre los tres paneles y comportamiento de Enter en category-list.
- `label-formatting`: Visualización correcta de shortcuts y parámetros en los items de categoría y macro.

### Modified Capabilities

## Impact

- Único archivo afectado: `src/mango/tui/app.py`
- Clases modificadas: `CategoryItem`, `MacroItem`, `MainScreen`
- Sin cambios en config, runner, ni dependencias externas
