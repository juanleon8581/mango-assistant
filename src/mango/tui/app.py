import re

from textual import on, work
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.screen import ModalScreen, Screen
from textual.widgets import Input, Label, ListItem, ListView, RichLog, Static

from ..config import Category, Config, Macro, Param


def _strip_to_plain(line: str) -> str:
    line = re.sub(r'\x1b\[[0-9;]*[mA-Za-z]', '', line)
    line = re.sub(r'\[/?[^\]]+\]', '', line)
    return line


# ── Custom ListItem subclasses ────────────────────────────────────────────────


class CategoryItem(ListItem):
    def __init__(self, category: Category) -> None:
        super().__init__(Label(f"\\[{category.shortcut}]  {category.name}"))
        self.category = category


class MacroItem(ListItem):
    def __init__(self, macro: Macro) -> None:
        params_hint = (
            " " + " ".join(f"<{p.name}>" for p in macro.params) if macro.params else ""
        )
        super().__init__(Label(f"\\[{macro.shortcut}]  {macro.description}{params_hint}"))
        self.macro = macro


# ── Parameter input dialog ────────────────────────────────────────────────────


class ParamDialog(ModalScreen[dict[str, str] | None]):
    DEFAULT_CSS = """
    ParamDialog {
        align: center middle;
    }
    #dialog {
        background: $surface;
        border: solid $primary;
        width: 60;
        height: auto;
        padding: 1 2;
    }
    #dialog-title {
        text-style: bold;
        padding-bottom: 1;
        color: $text;
    }
    #param-label {
        color: $text-muted;
        padding-bottom: 1;
    }
    """

    BINDINGS = [Binding("escape", "cancel", "Cancel")]

    def __init__(self, params: list[Param]) -> None:
        super().__init__()
        self._params = params
        self._values: dict[str, str] = {}
        self._idx = 0

    def compose(self) -> ComposeResult:
        with Vertical(id="dialog"):
            yield Label("Parameters", id="dialog-title")
            yield Label(self._params[0].prompt if self._params else "", id="param-label")
            yield Input(
                placeholder=self._params[0].prompt if self._params else "",
                id="param-input",
            )

    def on_mount(self) -> None:
        self.query_one("#param-input", Input).focus()

    @on(Input.Submitted, "#param-input")
    def _on_submitted(self, event: Input.Submitted) -> None:
        param = self._params[self._idx]
        self._values[param.name] = event.value
        self._idx += 1
        if self._idx >= len(self._params):
            self.dismiss(self._values)
            return
        next_param = self._params[self._idx]
        self.query_one("#param-label", Label).update(next_param.prompt)
        inp = self.query_one("#param-input", Input)
        inp.value = ""
        inp.focus()

    def action_cancel(self) -> None:
        self.dismiss(None)


# ── Main screen ───────────────────────────────────────────────────────────────


class MainScreen(Screen):
    DEFAULT_CSS = """
    MainScreen {
        layout: vertical;
    }
    #panels {
        layout: horizontal;
        height: 2fr;
    }
    #category-panel {
        width: 1fr;
        border: solid $primary;
    }
    #category-panel > Label {
        background: $primary;
        color: $text;
        text-align: center;
        height: 1;
        width: 1fr;
    }
    #macro-panel {
        width: 3fr;
        border: solid $accent;
    }
    #macro-panel > Label {
        background: $accent;
        color: $text;
        text-align: center;
        height: 1;
        width: 1fr;
    }
    #output-log {
        height: 1fr;
        border: solid $warning;
        display: none;
    }
    #footer {
        dock: bottom;
        height: 4;
        layout: vertical;
        border-top: solid $primary;
    }
    #shortcut-row {
        height: 3;
        layout: horizontal;
        align: left middle;
    }
    #shortcut-label {
        width: auto;
        padding: 0 1;
        color: $text-muted;
        content-align: center middle;
    }
    #shortcut-input {
        width: 1fr;
        border: none;
    }
    #status-bar {
        height: 1;
        padding: 0 1;
        color: $text-muted;
    }
    """

    BINDINGS = [
        Binding("q", "quit_app", "Quit", show=True),
        Binding("escape", "quit_app", "Quit", show=False),
        Binding("tab", "focus_next", "Next panel", show=True),
        Binding("shift+tab", "focus_previous", "Prev panel", show=False),
    ]

    def __init__(self, config: Config, cwd: str) -> None:
        super().__init__()
        self._config = config
        self._cwd = cwd
        self._categories = list(config.categories.values())
        self._selected_cat_idx = 0
        self._output_lines: list[str] = []

    def compose(self) -> ComposeResult:
        with Horizontal(id="panels"):
            with Vertical(id="category-panel"):
                yield Label(" Categories ")
                yield ListView(id="category-list")
            with Vertical(id="macro-panel"):
                yield Label(" Macros ")
                yield ListView(id="macro-list")
        yield RichLog(id="output-log", highlight=True, markup=True)
        with Vertical(id="footer"):
            with Horizontal(id="shortcut-row"):
                yield Static("shortcut> ", id="shortcut-label")
                yield Input(placeholder="g>su", id="shortcut-input")
            yield Label("", id="status-bar")

    def on_mount(self) -> None:
        cat_list = self.query_one("#category-list", ListView)
        for cat in self._categories:
            cat_list.append(CategoryItem(cat))
        if self._categories:
            self._populate_macros(self._categories[0])
        cat_list.focus()

    # ── Category navigation ───────────────────────────────────────────────────

    @on(ListView.Highlighted, "#category-list")
    def _on_category_highlighted(self, event: ListView.Highlighted) -> None:
        if isinstance(event.item, CategoryItem):
            self._populate_macros(event.item.category)

    @on(ListView.Selected, "#category-list")
    def _on_category_selected(self, event: ListView.Selected) -> None:
        self.query_one("#macro-list", ListView).focus()

    def _populate_macros(self, cat: Category) -> None:
        macro_list = self.query_one("#macro-list", ListView)
        macro_list.clear()
        for macro in cat.macros.values():
            macro_list.append(MacroItem(macro))

    # ── Macro execution via list selection ────────────────────────────────────

    @on(ListView.Selected, "#macro-list")
    def _on_macro_selected(self, event: ListView.Selected) -> None:
        if isinstance(event.item, MacroItem):
            self._trigger_macro(event.item.macro)

    # ── Shortcut bar ──────────────────────────────────────────────────────────

    @on(Input.Submitted, "#shortcut-input")
    def _on_shortcut_submitted(self, event: Input.Submitted) -> None:
        shortcut = event.value.strip()
        self.query_one("#shortcut-input", Input).value = ""
        if not shortcut:
            return
        self._dispatch_shortcut(shortcut)

    def _dispatch_shortcut(self, shortcut: str) -> None:
        parts = shortcut.split(">", 1)
        if len(parts) != 2:
            self._set_status(
                f"[red]Invalid format: '{shortcut}'. Use cat>mac (e.g. g>su)[/]"
            )
            return
        cat_sc, macro_sc = parts[0].strip(), parts[1].strip()
        cat = next((c for c in self._categories if c.shortcut == cat_sc), None)
        if cat is None:
            self._set_status(f"[red]Unknown category shortcut: '{cat_sc}'[/]")
            return
        macro = next((m for m in cat.macros.values() if m.shortcut == macro_sc), None)
        if macro is None:
            self._set_status(
                f"[red]Unknown macro shortcut: '{macro_sc}' in '{cat.name}'[/]"
            )
            return
        self._trigger_macro(macro)

    # ── Macro trigger + param dialog ─────────────────────────────────────────

    def _trigger_macro(self, macro: Macro) -> None:
        self._set_status(f"Selected: {macro.description}")
        if macro.params:
            self.app.push_screen(
                ParamDialog(macro.params),
                callback=lambda values: (
                    self._execute_macro(macro, values)
                    if values is not None
                    else self._set_status("Cancelled")
                ),
            )
        else:
            self._execute_macro(macro, {})

    # ── Execution ─────────────────────────────────────────────────────────────

    def _execute_macro(self, macro: Macro, params: dict[str, str]) -> None:
        output_log = self.query_one("#output-log", RichLog)
        output_log.clear()
        output_log.display = True
        self._output_lines.clear()
        self._set_status(f"Running: {macro.description}…")
        self._run_worker(macro, params, output_log)

    @work(thread=True)
    def _run_worker(
        self, macro: Macro, params: dict[str, str], output_log: RichLog
    ) -> None:
        from ..runner import run_macro

        def on_output(line: str) -> None:
            self._output_lines.append(_strip_to_plain(line))
            self.app.call_from_thread(output_log.write, line)

        try:
            success, exit_code, failed_step = run_macro(macro, params, self._cwd, on_output)
        except ValueError as exc:
            self.app.call_from_thread(self._on_config_error, str(exc))
            return

        if success:
            self.app.call_from_thread(self._on_success, macro, output_log)
        else:
            self.app.call_from_thread(
                self._on_failure, failed_step or "", exit_code or 1, output_log
            )

    def _on_success(self, macro: Macro, output_log: RichLog) -> None:
        output_log.write(f"\n[bold green]✓ '{macro.description}' completed[/]")
        self._set_status(f"[green]✓ Done: {macro.description}[/]")

    def _on_failure(self, step: str, exit_code: int, output_log: RichLog) -> None:
        output_log.write(
            f"\n[bold red]✗ Step failed (exit code {exit_code}):[/] {step}"
        )
        self._set_status(f"[red]✗ Failed (exit {exit_code}): {step}[/]")

    def _on_config_error(self, message: str) -> None:
        self._set_status(f"[red]Config error: {message}[/]")

    # ── Helpers ───────────────────────────────────────────────────────────────

    def _set_status(self, message: str) -> None:
        self.query_one("#status-bar", Label).update(message)

    _FOCUS_CYCLE = ["#category-list", "#macro-list", "#shortcut-input"]

    def action_focus_next(self) -> None:
        focused_id = self.focused.id if self.focused else None
        ids = self._FOCUS_CYCLE
        try:
            idx = ids.index(f"#{focused_id}")
        except ValueError:
            idx = -1
        self.query_one(ids[(idx + 1) % len(ids)]).focus()

    def action_focus_previous(self) -> None:
        focused_id = self.focused.id if self.focused else None
        ids = self._FOCUS_CYCLE
        try:
            idx = ids.index(f"#{focused_id}")
        except ValueError:
            idx = 0
        self.query_one(ids[(idx - 1) % len(ids)]).focus()

    def action_quit_app(self) -> None:
        if isinstance(self.focused, Input):
            return
        self.app.exit()

    def on_key(self, event) -> None:
        if isinstance(self.focused, Input):
            return
        if event.key == "ctrl+c":
            output_log = self.query_one("#output-log", RichLog)
            if output_log.display:
                event.stop()
                self.app.copy_to_clipboard("\n".join(self._output_lines))
                self.app.notify("Copied to clipboard")
        elif event.key == "q":
            event.stop()
            self.app.exit()
        elif event.key == "right" and self.focused and self.focused.id == "category-list":
            event.stop()
            self.query_one("#macro-list", ListView).focus()
        elif event.key == "left" and self.focused and self.focused.id == "macro-list":
            event.stop()
            self.query_one("#category-list", ListView).focus()


# ── App ───────────────────────────────────────────────────────────────────────


class MangoApp(App):
    TITLE = "mango"
    SUB_TITLE = "macro runner"

    def __init__(self, config: Config, cwd: str, update_info: tuple[str, str] | None = None) -> None:
        super().__init__()
        self._config = config
        self._cwd = cwd
        self._update_info = update_info

    def on_mount(self) -> None:
        self.push_screen(MainScreen(config=self._config, cwd=self._cwd))
        if self._update_info:
            current, latest = self._update_info
            self.notify(
                f"pip install --upgrade mango-tui",
                title=f"Update available: {current} → {latest}",
                severity="warning",
                timeout=10.0,
            )
