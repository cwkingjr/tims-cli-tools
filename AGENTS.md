# AGENTS.md

## Project Overview

Python CLI tools package (`tims-cli-tools`) with two executables:
- `tims_invoice` - transforms invoice export spreadsheets into submission format
- `tims_payroll` - generates consolidated payroll spreadsheets from input data

## Dev Commands

```bash
just --list              # Show all available commands
just lint                # ruff check --fix && ruff format
just test                # pytest with coverage report + HTML
just typing              # mypy src && ty check src
just all                 # lint -> typing -> clean-coverage -> test
```

**Command order matters:** `lint` before `typing` before `test`.

## Python Version

Requires Python 3.14+. Dev environment uses `uv`:
```bash
uv run <command>         # Run commands in uv-managed environment
```

## Project Structure

```
src/tims_cli_tools/      # Source package (pythonpath root for tests)
tests/                   # Tests (pythonpath = "./src")
```

Entry points in `pyproject.toml`:
```
tims_invoice = "tims_cli_tools.tims_invoice:main"
tims_payroll = "tims_cli_tools.tims_payroll:main"
```

## Configuration

`tims_payroll` requires config at: `~/.config/tims_tools/tims_payroll.toml`

## Dependencies

- Uses `duckdb` for payroll data processing
- Uses `pandas`, `openpyxl`/`xlsxwriter` for spreadsheet handling
- Ruff target version: `py314`

## Code Quality

- Ruff excludes: `src/before.py`
- Test file ignores: `S101` (assert), `PLR0133` (constant comparison)
- `ty` configured with `error-on-warning = true`
