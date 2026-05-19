## MODIFIED Requirements

### Requirement: Config schema — categories
El archivo de config SHALL definir categorías como claves bajo `categories`. Cada categoría SHALL tener un campo `shortcut` (string de 1+ caracteres, único entre todas las categorías) y un campo `macros` (mapa de macros). El sistema SHALL ordenar las categorías por `(len(shortcut), name)` al cargar la configuración — el orden de inserción en el YAML no determina el orden de display.

#### Scenario: Valid category definition
- **WHEN** el YAML contiene una categoría con `shortcut` y al menos una macro
- **THEN** el sistema carga la categoría correctamente y la muestra en el panel izquierdo

#### Scenario: Duplicate category shortcut
- **WHEN** dos categorías tienen el mismo valor de `shortcut`
- **THEN** el sistema muestra un error descriptivo al iniciar y no renderiza el TUI

#### Scenario: Category display order
- **WHEN** el sistema carga el config mergeado
- **THEN** las categorías se muestran ordenadas por longitud de shortcut (ascendente), luego alfabéticamente por nombre — no en orden de aparición en el YAML
