## 1. Sort macros within each category

- [ ] 1.1 In `_parse_category` (`config.py`), after building the `macros` dict, sort it by `(len(macro.shortcut), macro.description)` before returning the `Category`

## 2. Sort categories in config

- [ ] 2.1 In `load_config` (`config.py`), after building the `categories` dict, sort it by `(len(cat.shortcut), cat.name)` before returning the `Config`

## 3. Manual verification

- [ ] 3.1 Run `mango` with default config and verify categories appear as: `docker`, `git`, `mango`, `node`, `ssh`, `help`
- [ ] 3.2 Select the `git` category and verify macros are grouped alphabetically by description prefix (`branch | ...` before `clean | ...` before `git | ...`)
