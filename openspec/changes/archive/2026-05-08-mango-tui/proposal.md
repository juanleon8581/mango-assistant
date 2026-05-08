## Why

El ciclo de trabajo diario implica repetir secuencias de comandos que, aunque predecibles, consumen atención y tiempo (git flows, scripts de desarrollo, operaciones de Docker, etc.). No existe una herramienta personal que centralice estas macros con una interfaz de terminal rápida y navegable.

## What Changes

- Nuevo CLI `mango` que convierte la terminal en un entorno de ejecución de macros personales
- TUI de dos paneles: categorías a la izquierda, macros disponibles a la derecha
- Prompt interno para ejecutar macros por shortcut escrito (e.g., `g>su`)
- Motor de ejecución que corre secuencias de comandos shell en orden
- Configuración declarativa en YAML: categorías, macros, pasos y shortcuts

## Capabilities

### New Capabilities

- `macro-catalog`: Definición y persistencia de macros en YAML. Incluye schema de categorías, lista de pasos por macro, shortcuts y soporte de parámetros posicionales.
- `tui-interface`: Interfaz TUI con Textual. Layout de dos paneles (categorías + macros), navegación por teclado, y prompt de shortcut en el footer.
- `command-runner`: Motor de ejecución de macros. Corre los pasos de una macro como subprocesos shell secuenciales, interpola parámetros, y muestra el output en tiempo real dentro del TUI.

### Modified Capabilities

## Impact

- Nuevo proyecto Python standalone
- Dependencias: `textual`, `pyyaml`
- Config file: `~/.config/mango/commands.yaml`
- Instalable vía `pip install -e .` o `pipx`
- Sin efecto sobre el `cwd` del proceso padre — mango opera siempre desde el path donde fue invocado
