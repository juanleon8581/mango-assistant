# Spec: Label Formatting

## Purpose

Define how category and macro labels are rendered in list items, including shortcut visibility and parameter display format.

## Requirements

### Requirement: Shortcut visible como texto literal en items de lista
El sistema SHALL mostrar el shortcut de cada categoría y macro encerrado en corchetes como texto literal (ej: `[g]`, `[su]`). Los corchetes NO SHALL ser interpretados como markup de estilo por el framework de renderizado.

#### Scenario: CategoryItem muestra shortcut visible
- **WHEN** se renderiza un item de categoría en el `category-list`
- **THEN** el label muestra `[<shortcut>]  <nombre>` con los corchetes visibles

#### Scenario: MacroItem muestra shortcut visible
- **WHEN** se renderiza un item de macro en el `macro-list`
- **THEN** el label muestra `[<shortcut>] <descripción>` con los corchetes visibles

### Requirement: Parámetros de macro se muestran en formato inline con ángulos
El sistema SHALL mostrar los parámetros de una macro como `<nombre_param>` concatenados inline después de la descripción, separados por espacios. Las macros sin parámetros SHALL mostrar solo la descripción.

#### Scenario: Macro con un parámetro
- **WHEN** se renderiza una macro con un parámetro de nombre `branch`
- **THEN** el label muestra `[su] Switch branch, fetch and pull <branch>`

#### Scenario: Macro con múltiples parámetros
- **WHEN** se renderiza una macro con parámetros `service` y `tag`
- **THEN** el label muestra `[xx] Descripción <service> <tag>`

#### Scenario: Macro sin parámetros
- **WHEN** se renderiza una macro sin parámetros
- **THEN** el label muestra solo `[xx] Descripción` sin sufijo adicional
