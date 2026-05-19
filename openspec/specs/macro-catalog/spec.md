# Spec: macro-catalog

## Purpose

Define how mango loads, validates, and exposes the macro catalog — the YAML-based configuration that declares categories, macros, parameters, and command steps.

## Requirements

### Requirement: Config file location
El sistema SHALL buscar el archivo de configuración en `~/.config/mango/commands.yaml`. Si el archivo no existe al iniciar, el sistema SHALL crearlo con un ejemplo funcional.

#### Scenario: Config file exists
- **WHEN** el usuario ejecuta `mango` y el archivo `~/.config/mango/commands.yaml` existe
- **THEN** el sistema carga la configuración desde ese archivo

#### Scenario: Config file does not exist
- **WHEN** el usuario ejecuta `mango` por primera vez y no existe el archivo de config
- **THEN** el sistema crea `~/.config/mango/commands.yaml` con contenido de ejemplo y lo carga

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

### Requirement: Config schema — macros
Cada macro SHALL tener: `shortcut` (string único dentro de su categoría), `description` (string), `steps` (lista de strings con comandos shell). Opcionalmente puede tener `params` (lista de objetos con `name` y `prompt`).

#### Scenario: Macro with no params
- **WHEN** una macro no define `params`
- **THEN** el sistema ejecuta sus pasos directamente sin solicitar input al usuario

#### Scenario: Macro with params
- **WHEN** una macro define uno o más `params`
- **THEN** el sistema solicita al usuario el valor de cada parámetro antes de ejecutar los pasos

### Requirement: Parameter interpolation in steps
Los steps de una macro SHALL soportar interpolación de parámetros con la sintaxis `{param_name}`. El sistema SHALL reemplazar cada `{param_name}` con el valor provisto por el usuario antes de ejecutar el paso.

#### Scenario: Step with parameter reference
- **WHEN** un step contiene `{branch}` y el usuario proveyó `main` como valor para `branch`
- **THEN** el sistema ejecuta el comando con `{branch}` reemplazado por `main`

### Requirement: Config validation on load
El sistema SHALL validar el schema del YAML al cargarlo. Si la estructura es inválida o falta algún campo requerido, el sistema SHALL mostrar un mensaje de error claro con el campo problemático y no iniciar el TUI.

#### Scenario: Missing required field in macro
- **WHEN** una macro no tiene el campo `steps`
- **THEN** el sistema muestra un error indicando la macro y el campo faltante, y termina sin abrir el TUI
