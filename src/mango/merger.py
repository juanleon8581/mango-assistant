from pathlib import Path

import yaml


def merge_configs(config_dir: Path) -> list[str]:
    default_path = config_dir / "config.default.yaml"
    local_path = config_dir / "config.local.yaml"

    warnings: list[str] = []

    default_raw = yaml.safe_load(default_path.read_text())
    default_cats: dict = (default_raw or {}).get("categories", {})

    merged_cats: dict = {}
    for key, data in default_cats.items():
        merged_cats[key] = {"shortcut": data["shortcut"], "macros": dict(data.get("macros") or {})}

    if not local_path.exists():
        return warnings

    local_raw = yaml.safe_load(local_path.read_text())
    local_cats: dict = (local_raw or {}).get("categories", {})

    default_shortcuts: set[str] = {str(v["shortcut"]) for v in default_cats.values()}

    for local_key, local_data in local_cats.items():
        local_shortcut = str(local_data.get("shortcut", ""))

        if local_key in default_cats:
            default_shortcut = str(default_cats[local_key].get("shortcut", ""))
            if local_shortcut == default_shortcut:
                # Exact match — macro merge (task 3.2)
                pass
            else:
                warnings.append(
                    f"[mango] config conflict: category '{local_key}' — "
                    f"shortcut '{local_shortcut}' conflicts with default shortcut '{default_shortcut}' (skipped)"
                )
        elif local_shortcut in default_shortcuts:
            conflicting_key = next(k for k, v in default_cats.items() if str(v["shortcut"]) == local_shortcut)
            warnings.append(
                f"[mango] config conflict: category '{local_key}' — "
                f"shortcut '{local_shortcut}' already used by '{conflicting_key}' (skipped)"
            )
        else:
            merged_cats[local_key] = local_data

    return warnings
