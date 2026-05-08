# Spec: tui-interface

## Purpose

Define the behavior and interaction model of the mango terminal UI — layout, keyboard navigation, shortcut prompt, parameter dialogs, and output display.

## Requirements

### Requirement: Two-panel layout
El TUI SHALL mostrar un layout de dos paneles: panel izquierdo con la lista de categorías y panel derecho con la lista de macros de la categoría seleccionada.

#### Scenario: Initial render
- **WHEN** el usuario ejecuta `mango`
- **THEN** el TUI muestra la lista de categorías en el panel izquierdo y las macros de la primera categoría en el panel derecho

#### Scenario: Category selection updates macro panel
- **WHEN** el usuario navega a una categoría diferente
- **THEN** el panel derecho se actualiza para mostrar las macros de esa categoría

### Requirement: Keyboard navigation
El usuario SHALL poder navegar entre categorías y macros usando las teclas de flecha. La tecla `Enter` SHALL ejecutar la macro seleccionada. La tecla `Tab` SHALL mover el foco entre el panel de categorías y el panel de macros. La tecla `Escape` o `q` SHALL cerrar la aplicación.

#### Scenario: Navigate categories with arrow keys
- **WHEN** el foco está en el panel de categorías y el usuario presiona flecha arriba/abajo
- **THEN** la selección se mueve a la categoría anterior/siguiente

#### Scenario: Execute macro with Enter
- **WHEN** el foco está en el panel de macros y el usuario presiona Enter sobre una macro
- **THEN** el sistema inicia el flujo de ejecución de esa macro

#### Scenario: Quit application
- **WHEN** el usuario presiona `q` o `Escape` sin ningún diálogo activo
- **THEN** la aplicación termina y el usuario regresa al prompt normal de la terminal

### Requirement: Shortcut prompt in footer
El TUI SHALL mostrar un campo de input en el footer siempre visible donde el usuario puede escribir un shortcut en formato `<category_shortcut>><macro_shortcut>`. Al presionar `Enter` en el prompt SHALL resolverse y ejecutarse la macro correspondiente.

#### Scenario: Valid shortcut entered
- **WHEN** el usuario escribe `g>su` en el prompt y presiona Enter
- **THEN** el sistema identifica la macro `switch-and-pull` de la categoría `git` y la ejecuta

#### Scenario: Invalid shortcut entered
- **WHEN** el usuario escribe un shortcut que no corresponde a ninguna categoría o macro
- **THEN** el sistema muestra un mensaje de error en el footer y limpia el input

### Requirement: Parameter input dialog
Cuando la macro a ejecutar tiene parámetros definidos, el TUI SHALL mostrar un diálogo de input secuencial, uno por parámetro, usando el campo `prompt` de cada parámetro como label.

#### Scenario: Macro with one parameter
- **WHEN** se dispara una macro con un parámetro `branch` (prompt: "Nombre de la rama")
- **THEN** el TUI muestra un input con el label "Nombre de la rama" antes de ejecutar los pasos

#### Scenario: User cancels parameter input
- **WHEN** el usuario presiona `Escape` durante el ingreso de parámetros
- **THEN** la ejecución se cancela y el TUI regresa al estado de navegación normal

### Requirement: Output panel
Durante la ejecución de una macro, el TUI SHALL mostrar un panel de output con el resultado en tiempo real de cada paso. Al finalizar todos los pasos, el panel SHALL mostrar un resumen de éxito o el error del paso fallido.

#### Scenario: Successful execution output
- **WHEN** todos los pasos de una macro completan con exit code 0
- **THEN** el panel de output muestra el stdout/stderr de cada paso y un mensaje de éxito al final

#### Scenario: Failed step output
- **WHEN** un paso retorna exit code != 0
- **THEN** el panel de output muestra la salida del paso fallido, un mensaje de error, y la ejecución se detiene
