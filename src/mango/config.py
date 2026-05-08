from dataclasses import dataclass, field
from pathlib import Path
import os
import yaml


@dataclass
class Param:
    name: str
    prompt: str


@dataclass
class Macro:
    shortcut: str
    description: str
    steps: list[str]
    params: list[Param] = field(default_factory=list)


@dataclass
class Category:
    name: str
    shortcut: str
    macros: dict[str, Macro]


@dataclass
class Config:
    categories: dict[str, Category]


EXAMPLE_CONFIG = """\
categories:
  git:
    shortcut: "g"
    macros:
      switch-and-pull:
        shortcut: "su"
        description: "Switch branch, fetch and pull"
        params:
          - name: branch
            prompt: "Branch name"
        steps:
          - git checkout {branch}
          - git fetch
          - git pull
      status:
        shortcut: "st"
        description: "Show git status"
        steps:
          - git status
      log:
        shortcut: "lo"
        description: "Show recent commits"
        steps:
          - git log --oneline -10
  docker:
    shortcut: "d"
    macros:
      up:
        shortcut: "up"
        description: "Start containers"
        steps:
          - docker compose up -d
      down:
        shortcut: "dn"
        description: "Stop containers"
        steps:
          - docker compose down
      logs:
        shortcut: "lg"
        description: "Follow logs for a service"
        params:
          - name: service
            prompt: "Service name"
        steps:
          - docker compose logs -f {service}
"""


def get_config_path() -> Path:
    xdg_config = os.environ.get("XDG_CONFIG_HOME", "")
    base = Path(xdg_config) if xdg_config else Path.home() / ".config"
    return base / "mango" / "commands.yaml"


def ensure_config(path: Path) -> None:
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(EXAMPLE_CONFIG)


def _parse_param(data: object, macro_name: str, idx: int) -> Param:
    if not isinstance(data, dict):
        raise ValueError(f"Macro '{macro_name}': param[{idx}] must be a mapping")
    name = data.get("name")
    prompt = data.get("prompt")
    if not name:
        raise ValueError(f"Macro '{macro_name}': param[{idx}] missing 'name'")
    if not prompt:
        raise ValueError(f"Macro '{macro_name}': param[{idx}] missing 'prompt'")
    return Param(name=str(name), prompt=str(prompt))


def _parse_macro(data: object, macro_key: str, cat_name: str) -> Macro:
    if not isinstance(data, dict):
        raise ValueError(f"Category '{cat_name}': macro '{macro_key}' must be a mapping")
    shortcut = data.get("shortcut")
    description = data.get("description")
    steps = data.get("steps")
    if not shortcut:
        raise ValueError(f"'{cat_name}.{macro_key}': missing 'shortcut'")
    if not description:
        raise ValueError(f"'{cat_name}.{macro_key}': missing 'description'")
    if not steps or not isinstance(steps, list):
        raise ValueError(f"'{cat_name}.{macro_key}': missing or empty 'steps'")
    params = [_parse_param(p, macro_key, i) for i, p in enumerate(data.get("params") or [])]
    return Macro(
        shortcut=str(shortcut),
        description=str(description),
        steps=[str(s) for s in steps],
        params=params,
    )


def _parse_category(data: object, cat_key: str) -> Category:
    if not isinstance(data, dict):
        raise ValueError(f"Category '{cat_key}' must be a mapping")
    shortcut = data.get("shortcut")
    macros_raw = data.get("macros") or {}
    if not shortcut:
        raise ValueError(f"Category '{cat_key}': missing 'shortcut'")
    if not isinstance(macros_raw, dict):
        raise ValueError(f"Category '{cat_key}': 'macros' must be a mapping")
    macros: dict[str, Macro] = {}
    seen_shortcuts: set[str] = set()
    for mk, mv in macros_raw.items():
        macro = _parse_macro(mv, mk, cat_key)
        if macro.shortcut in seen_shortcuts:
            raise ValueError(f"Category '{cat_key}': duplicate macro shortcut '{macro.shortcut}'")
        seen_shortcuts.add(macro.shortcut)
        macros[mk] = macro
    return Category(name=cat_key, shortcut=str(shortcut), macros=macros)


def load_config(path: Path) -> Config:
    raw = yaml.safe_load(path.read_text())
    if not isinstance(raw, dict) or "categories" not in raw:
        raise ValueError("Config must have a top-level 'categories' key")
    cats_raw = raw["categories"]
    if not isinstance(cats_raw, dict):
        raise ValueError("'categories' must be a mapping")
    categories: dict[str, Category] = {}
    seen_shortcuts: set[str] = set()
    for ck, cv in cats_raw.items():
        cat = _parse_category(cv, ck)
        if cat.shortcut in seen_shortcuts:
            raise ValueError(f"Duplicate category shortcut '{cat.shortcut}'")
        seen_shortcuts.add(cat.shortcut)
        categories[ck] = cat
    return Config(categories=categories)


def interpolate(template: str, params: dict[str, str]) -> str:
    return template.format_map(params)
