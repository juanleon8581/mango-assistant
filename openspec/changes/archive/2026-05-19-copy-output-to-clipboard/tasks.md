## 1. Plain-text output buffer

- [x] 1.1 Agregar `_output_lines: list[str]` a `MainScreen.__init__()` e inicializarlo como lista vacía
- [x] 1.2 Crear función helper `_strip_to_plain(line: str) -> str` que elimine Rich markup tags y ANSI codes con regex
- [x] 1.3 En `_execute_macro()`, limpiar `_output_lines` antes de cada nueva ejecución
- [x] 1.4 En `_run_worker` → `on_output()`, llamar `_output_lines.append(_strip_to_plain(line))` junto al `output_log.write(line)` existente

## 2. Keybinding y clipboard

- [x] 2.1 En `on_key()`, interceptar `ctrl+c` cuando `output_log.display is True`: llamar `event.stop()`, `self.app.copy_to_clipboard(...)` y `self.app.notify("Copied to clipboard")`
