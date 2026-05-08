## 1. Project Setup

- [ ] 1.1 Inicializar proyecto Python con `pyproject.toml`: dependencias `textual` y `pyyaml`, entry point `mango`
- [ ] 1.2 Crear estructura de directorios del proyecto (`src/mango/`, `__init__.py`, `main.py`)
- [ ] 1.3 Verificar que `mango` corre desde la terminal tras `pip install -e .`

## 2. Macro Catalog — Config Loading

- [ ] 2.1 Implementar función que resuelve la ruta `~/.config/mango/commands.yaml` (respetando XDG)
- [ ] 2.2 Implementar creación del archivo de config de ejemplo si no existe
- [ ] 2.3 Implementar carga y parseo del YAML a dataclasses/TypedDicts internos
- [ ] 2.4 Implementar validación de schema: campos requeridos, shortcuts únicos por scope
- [ ] 2.5 Implementar interpolación de parámetros en steps (`{param_name}` → valor)

## 3. Command Runner — Execution Engine

- [ ] 3.1 Implementar función `run_step(command: str, cwd: str)` que ejecuta un comando como subproceso no interactivo
- [ ] 3.2 Implementar streaming de output línea a línea desde stdout/stderr del subproceso
- [ ] 3.3 Implementar `run_macro(macro, params, cwd, on_output)` que ejecuta pasos en secuencia y detiene en error
- [ ] 3.4 Verificar que el cwd usado es siempre el del proceso padre (donde se lanzó `mango`)

## 4. TUI — Layout Base

- [ ] 4.1 Crear `MangoApp(App)` con `MainScreen(Screen)` usando Textual
- [ ] 4.2 Implementar layout de dos paneles: `CategoryList` (izquierda) y `MacroList` (derecha) con `ListView`
- [ ] 4.3 Implementar `ShortcutBar` en el footer como widget de input siempre visible
- [ ] 4.4 Poblar `CategoryList` con las categorías cargadas desde config
- [ ] 4.5 Implementar actualización de `MacroList` al seleccionar una categoría

## 5. TUI — Navegación y Keyboard

- [ ] 5.1 Implementar navegación entre paneles con `Tab`
- [ ] 5.2 Implementar selección de categoría/macro con teclas de flecha y `Enter`
- [ ] 5.3 Implementar cierre de la app con `q` y `Escape`
- [ ] 5.4 Implementar resolución y dispatch de shortcut desde el `ShortcutBar` (`g>su` → macro)
- [ ] 5.5 Implementar mensaje de error en footer para shortcuts inválidos

## 6. TUI — Parameter Input Dialog

- [ ] 6.1 Implementar diálogo de input secuencial para parámetros de una macro
- [ ] 6.2 Implementar cancelación del diálogo con `Escape`

## 7. TUI — Output Panel

- [ ] 7.1 Crear `OutputLog` (panel de log) que se muestra durante la ejecución
- [ ] 7.2 Conectar el streaming del runner con el `OutputLog` via worker thread y `call_from_thread`
- [ ] 7.3 Mostrar mensaje de éxito al completar todos los pasos
- [ ] 7.4 Mostrar mensaje de error con el step fallido y su exit code

## 8. Integration & Polish

- [ ] 8.1 Probar el flujo completo: navegar → seleccionar macro con params → ejecutar → ver output
- [ ] 8.2 Probar dispatch por shortcut: `g>su main` → ejecutar con param `branch=main`
- [ ] 8.3 Verificar comportamiento con YAML inválido (schema incorrecto, shortcuts duplicados)
- [ ] 8.4 Agregar config de ejemplo con al menos 2 categorías y 3 macros representativas del flujo de trabajo
