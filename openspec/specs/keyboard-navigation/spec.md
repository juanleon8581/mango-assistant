# Spec: Keyboard Navigation

## Purpose

Define how keyboard focus moves between the three main panels of the TUI (`category-list`, `macro-list`, `shortcut-input`), enabling full keyboard-first interaction without mouse input.

## Requirements

### Requirement: Tab cicla entre los tres paneles en orden fijo
El sistema SHALL navegar el foco cíclicamente entre `category-list`, `macro-list` y `shortcut-input` al presionar Tab, siguiendo ese orden exacto. Al llegar al último elemento, el siguiente Tab vuelve al primero.

#### Scenario: Tab desde category-list va a macro-list
- **WHEN** el foco está en `category-list` y el usuario presiona Tab
- **THEN** el foco se mueve a `macro-list`

#### Scenario: Tab desde macro-list va a shortcut-input
- **WHEN** el foco está en `macro-list` y el usuario presiona Tab
- **THEN** el foco se mueve a `shortcut-input`

#### Scenario: Tab desde shortcut-input vuelve a category-list
- **WHEN** el foco está en `shortcut-input` y el usuario presiona Tab
- **THEN** el foco se mueve a `category-list`

#### Scenario: Shift+Tab cicla en sentido inverso
- **WHEN** el usuario presiona Shift+Tab desde cualquier panel
- **THEN** el foco se mueve al panel anterior en el ciclo

### Requirement: Enter en category-list mueve el foco a macro-list
El sistema SHALL mover el foco al `macro-list` cuando el usuario presiona Enter sobre un item en el `category-list`. El contenido del macro-list SHALL reflejar las macros de la categoría seleccionada.

#### Scenario: Enter en category-list con categoría seleccionada
- **WHEN** el foco está en `category-list`, hay un item resaltado y el usuario presiona Enter
- **THEN** el foco se mueve a `macro-list` mostrando las macros de esa categoría

### Requirement: Flecha derecha mueve el foco de category-list a macro-list
El sistema SHALL mover el foco al `macro-list` cuando el usuario presiona `→` estando en `category-list`, sin disparar selección de categoría.

#### Scenario: → desde category-list mueve el foco a macro-list
- **WHEN** el foco está en `category-list` y el usuario presiona `→`
- **THEN** el foco se mueve a `macro-list` y el contenido del macro-list no cambia

#### Scenario: → desde macro-list no hace nada
- **WHEN** el foco está en `macro-list` y el usuario presiona `→`
- **THEN** el foco permanece en `macro-list` sin ningún efecto

### Requirement: Flecha izquierda mueve el foco de macro-list a category-list
El sistema SHALL mover el foco al `category-list` cuando el usuario presiona `←` estando en `macro-list`.

#### Scenario: ← desde macro-list mueve el foco a category-list
- **WHEN** el foco está en `macro-list` y el usuario presiona `←`
- **THEN** el foco se mueve a `category-list`

#### Scenario: ← desde category-list no hace nada
- **WHEN** el foco está en `category-list` y el usuario presiona `←`
- **THEN** el foco permanece en `category-list` sin ningún efecto

### Requirement: Las flechas laterales no se interceptan en Input
El sistema SHALL ignorar `←` y `→` para navegación entre paneles cuando el foco está en cualquier widget `Input`.

#### Scenario: ← y → en shortcut-input no cambian el foco
- **WHEN** el foco está en `shortcut-input` y el usuario presiona `←` o `→`
- **THEN** el cursor del input se mueve normalmente y el foco no cambia de panel
