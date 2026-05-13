import sys
from pathlib import Path

from .config import ensure_config, get_config_path, load_config
from .merger import merge_configs
from .updater import check_for_update


def main() -> None:
    check_for_update()
    config_path = get_config_path()
    config_dir = config_path.parent
    try:
        ensure_config(config_dir)
        merge_configs(config_dir)
        config = load_config(config_path)
    except Exception as exc:
        print(f"mango: config error — {exc}", file=sys.stderr)
        sys.exit(1)

    from .tui.app import MangoApp

    cwd = str(Path.cwd())
    app = MangoApp(config=config, cwd=cwd)
    app.run()
