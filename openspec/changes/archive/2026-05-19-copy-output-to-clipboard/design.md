## Context

`RichLog` (el widget actual del output panel) no expone su contenido como texto plano — renderiza Rich markup y ANSI codes visualmente pero no ofrece un `.text` property. Para copiar el output hay que capturarlo aparte.

Textual 0.60+ incluye `App.copy_to_clipboard(text: str)` que usa la secuencia de escape OSC 52, un protocolo estándar de terminal que permite a aplicaciones TUI escribir al clipboard del sistema sin dependencias externas.

El runner emite dos tipos de contenido vía `on_output()`:
- Rich markup propio de mango: `[bold cyan][step 1/2][/] $ git fetch`
- Output crudo del subprocess: puede incluir ANSI color codes de git, npm, etc.

Ambos llegan a `RichLog.write()`. El buffer paralelo debe recibir el mismo texto pero limpio.

## Goals / Non-Goals

**Goals:**
- Copiar el contenido completo del output panel al clipboard con `ctrl+c`
- Sin dependencias nuevas
- Feedback visual inmediato (notificación)
- Funcionar en terminales que soportan OSC 52 (mayoría de terminales modernos)

**Non-Goals:**
- Selección granular de texto (subconjunto del output)
- Soporte garantizado en terminales que no implementan OSC 52 (ej. macOS Terminal.app)
- Persistencia del output entre sesiones

## Decisions

### D1: `app.copy_to_clipboard()` en lugar de subprocess con xclip/wl-copy

`copy_to_clipboard()` usa OSC 52, que funciona en la mayoría de emuladores modernos (Kitty, Alacritty, WezTerm, iTerm2, GNOME Terminal, xterm). Evita detectar el entorno (Wayland vs X11 vs macOS) y no añade dependencias.

Alternativa descartada: `subprocess` con fallback entre `wl-copy`, `xclip`, `xsel`, `pbcopy`. Más frágil, requiere detección del entorno, falla silenciosamente si ninguna herramienta está instalada.

### D2: Buffer paralelo `_output_lines: list[str]` en lugar de leer RichLog

`RichLog` no expone su contenido. Mantener una lista de strings en paralelo es simple y controlado. El buffer se limpia en cada nueva ejecución.

### D3: Stripping con regex en lugar de `rich.markup.strip()`

Dos pasos de limpieza sobre cada línea del buffer:
1. ANSI codes: `re.sub(r'\x1b\[[0-9;]*[mA-Za-z]', '', line)`
2. Rich markup tags: `re.sub(r'\[/?[^\]]+\]', '', line)`

`rich.markup.strip()` está disponible vía Textual pero importar Rich directamente en `app.py` añade un acoplamiento innecesario. Regex cubre ambos casos con `re`, que ya está en la stdlib.

### D4: Interceptar en `on_key()` en lugar de añadir a `BINDINGS`

`ctrl+c` en Textual 8.x es un binding de sistema (`system=True`) mapeado a `action_help_quit`. Los bindings de sistema tienen prioridad sobre los de Screen/App. Interceptar en `on_key()` con `event.stop()` antes de que el evento llegue al sistema es el camino correcto.

La intercepción solo ocurre cuando `output_log.display is True` (el panel tiene contenido visible). Si no hay output, `ctrl+c` llega a `help_quit` normalmente.

## Risks / Trade-offs

**OSC 52 no soportado en el terminal del usuario** → El texto no se copia pero la notificación aparece igual. El usuario verá "Copied to clipboard" sin resultado. Mitigación: es el comportamiento estándar de `copy_to_clipboard()` en Textual; documentar en README que requiere terminal con soporte OSC 52.

**Output muy largo** → OSC 52 tiene un límite práctico de ~100KB en la mayoría de terminales. Macros que generen outputs masivos pueden fallar silenciosamente. Mitigación: fuera de scope para v0.2.6; casos típicos de mango son outputs pequeños.

**Markup regex demasiado agresivo** → El pattern `\[/?[^\]]+\]` podría hacer match con texto legítimo en corchetes del output del subprocess (ej. `[WARNING]`). Mitigación: el stripping es solo para el buffer de clipboard; el RichLog sigue mostrando el texto original sin modificar.
