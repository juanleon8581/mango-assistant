import re
import subprocess
from typing import Callable

from .config import Macro, interpolate


def _validate_steps(macro: Macro, params: dict[str, str]) -> None:
    param_names = set(params.keys())
    for step in macro.steps:
        for match in re.finditer(r"\{(\w+)\}", step):
            name = match.group(1)
            if name not in param_names:
                raise ValueError(
                    f"Step '{step}' references undefined param '{name}'"
                )


def run_step(command: str, cwd: str, on_output: Callable[[str], None]) -> int:
    proc = subprocess.Popen(
        command,
        shell=True,
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        stdin=subprocess.DEVNULL,
        text=True,
        bufsize=1,
    )
    assert proc.stdout is not None
    for line in proc.stdout:
        on_output(line.rstrip())
    proc.wait()
    return proc.returncode


def run_macro(
    macro: Macro,
    params: dict[str, str],
    cwd: str,
    on_output: Callable[[str], None],
) -> tuple[bool, int | None, str | None]:
    _validate_steps(macro, params)
    total = len(macro.steps)
    for i, step_template in enumerate(macro.steps, 1):
        cmd = interpolate(step_template, params)
        on_output(f"[bold cyan][step {i}/{total}][/] $ {cmd}")
        rc = run_step(cmd, cwd, on_output)
        if rc != 0:
            return False, rc, cmd
    return True, None, None
