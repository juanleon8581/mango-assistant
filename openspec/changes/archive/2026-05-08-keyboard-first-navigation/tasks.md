## 1. Label Formatting

- [x] 1.1 Escapar corchetes en `CategoryItem` — cambiar `f"[{category.shortcut}]"` a `f"\\[{category.shortcut}]"` para que Rich muestre `[g]` como texto literal
- [x] 1.2 Escapar corchetes en `MacroItem` — misma corrección para el shortcut de macro
- [x] 1.3 Cambiar formato de params en `MacroItem` de `(param)` a `<param>` inline después de la descripción

## 2. Keyboard Navigation

- [x] 2.1 Sobrescribir `action_focus_next` en `MainScreen` con ciclo explícito `category-list → macro-list → shortcut-input → category-list`
- [x] 2.2 Sobrescribir `action_focus_previous` en `MainScreen` con el ciclo inverso
- [x] 2.3 Agregar handler `@on(ListView.Selected, "#category-list")` que mueva el foco a `macro-list`
