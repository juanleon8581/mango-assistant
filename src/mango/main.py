import sys
from pathlib import Path

from .config import ensure_config, get_config_path, load_config


def main() -> None:
    config_path = get_config_path()
    try:
        ensure_config(config_path)
        config = load_config(config_path)
    except Exception as exc:
        print(f"mango: config error — {exc}", file=sys.stderr)
        sys.exit(1)

    from .tui.app import MangoApp

    cwd = str(Path.cwd())
    app = MangoApp(config=config, cwd=cwd)
    app.run()
