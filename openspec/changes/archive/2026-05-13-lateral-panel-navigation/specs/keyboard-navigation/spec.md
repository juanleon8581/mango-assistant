## ADDED Requirements

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
