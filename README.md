[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
# ptree

  A colorful, icon-rich directory tree printer for your terminal. It walks a path, shows folders/files with Nerd Font icons, colors directories blue and
  files green, and can hide dotfiles by default.

  ## Requirements
  - Python 3.6+
  - A Nerd Font (icons come from `ptree/icons-sample.yaml`)
  - Dependencies: `colorama`, `pyyaml` (install via `pip install -r requirement.txt` or `pip install -e .`)

  ## Installation
  ```bash
  git clone pip install git+https://github.com/Nii-Antiaye/ptree.git
  cd ptree
  python -m venv .venv && .\.venv\Scripts\activate
  pip install -r requirement.txt
  ```
  Alternatively, install in editable mode to get the console script:
  ```bash
  pip install -e .
  ```

  ## Usage
  From the repo without installing:
  ```bash
  python ptree/main.py .
  ```
  After installing with the console entry point:
  ```bash
  ptree .
  ```

  Flags:
  - `--all` — include hidden files/folders.
  - `-d`, `--directory` — show directories only.

  Example:
  ```
  ptree . --all
  ```
  Sample output (icons depend on your font):
  ```
  <dir_icon> .
  ├── <dir_icon> src
  │   ├── <file_icon> main.py
  │   └── <file_icon> utils.py
  └── <file_icon> README.md

  <dir_icon> 3 directories, <file_icon> 5 files
  ```

  ## Customizing icons
  - Edit `ptree/icons-sample.yaml` or copy it to another YAML file.
  - Three sections are supported: `filetype` (general defaults), `name` (exact file/dir names), and `extension` (by file extension).
  - Icons use Nerd Font glyphs; restart the command after edits.

  ## Notes
  - Hidden items (names starting with `.`) are skipped unless `--all` is set.
  - The tree order lists directories before files.
  - Color output uses `colorama`; Windows terminals are supported out of the box.