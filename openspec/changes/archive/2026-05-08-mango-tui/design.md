## Context

`mango` es una herramienta personal de terminal sin base de código previa. Se construye desde cero en Python con Textual como framework TUI. El único estado persistente es el archivo de configuración YAML del usuario. No hay backend, base de datos ni API — es un proceso local que vive mientras el usuario lo tiene abierto.

## Goals / Non-Goals

**Goals:**
- TUI navegable con dos paneles (categorías / macros) operativo con teclado
- Prompt de shortcut escrito para dispatch rápido sin navegar menús
- Motor de ejecución secuencial de comandos shell con interpolación de parámetros
- Config YAML legible y editable a mano
- Instalable como comando global (`mango`)

**Non-Goals:**
- Edición de macros desde dentro del TUI (v1 — config manual)
- Ejecución paralela de pasos dentro de una macro
- Sincronización de config entre máquinas
- Historial de ejecuciones

## Decisions

### 1. Framework TUI: Textual

Textual ofrece el mejor balance entre madurez, documentación y productividad para Python. Alternativas consideradas:
- `curses` / `blessed`: bajo nivel, mucho boilerplate para navegación básica
- `prompt_toolkit`: orientado a prompts, no a layouts multipanel
- `urwid`: maduro pero API anticuada

**Decisión**: Textual.

### 2. Formato de config: YAML vía PyYAML

YAML es más legible que JSON para config anidada y más familiar que TOML para un usuario JS/TS. PyYAML es la librería estándar de facto.

Schema de referencia:
```yaml
categories:
  git:
    shortcut: "g"
    macros:
      switch-and-pull:
        shortcut: "su"
        description: "Cambia de rama, fetch y pull"
        params:
          - name: branch
            prompt: "Nombre de la rama"
        steps:
          - git checkout {branch}
          - git fetch
          - git pull
```

### 3. Ubicación del archivo de config

`~/.config/mango/commands.yaml` (respetando XDG Base Directory). Si el archivo no existe al iniciar, mango crea uno de ejemplo.

### 4. Resolución de shortcuts

El formato `g>su` se parsea como `<category_shortcut>><macro_shortcut>`. El separador `>` es fijo. La resolución es:
1. Buscar categoría cuyo `shortcut` == `g`
2. Dentro de esa categoría, buscar macro cuyo `shortcut` == `su`
3. Si no hay match → mostrar error en el footer

### 5. Interpolación de parámetros

Los parámetros se referencian por nombre en los steps: `{branch}`. Al ejecutar una macro con parámetros, el TUI muestra un diálogo de input secuencial (uno por parámetro) antes de lanzar los pasos.

### 6. Ejecución de pasos

Cada paso se ejecuta como subproceso (`subprocess.run`) en el `cwd` desde donde se lanzó `mango`. Los pasos son secuenciales y se detienen si un paso retorna exit code != 0. El output se muestra en tiempo real en un panel de log dentro del TUI.

### 7. Arquitectura Textual (App → Screens → Widgets)

```
MangoApp (App)
└── MainScreen (Screen)
    ├── CategoryList (ListView)   ← panel izquierdo
    ├── MacroList (ListView)      ← panel derecho
    ├── OutputLog (RichLog)       ← panel de output (visible al ejecutar)
    └── ShortcutBar (Input)       ← footer siempre visible
```

## Risks / Trade-offs

- **Output streaming con Textual** → Textual corre en el hilo principal; los subprocesos deben ejecutarse en un worker thread y postear mensajes al hilo UI. Mitigación: usar `app.call_from_thread()` o `workers`.
- **YAML malformado** → Si el usuario rompe el YAML, mango no arranca. Mitigación: validar el schema al cargar y mostrar un error descriptivo antes de renderizar el TUI.
- **Shortcuts colisionantes** → Si dos categorías tienen el mismo shortcut, el comportamiento es ambiguo. Mitigación: validar unicidad al cargar config y reportar el conflicto.
