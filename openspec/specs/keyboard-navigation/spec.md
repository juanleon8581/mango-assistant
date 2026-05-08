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
