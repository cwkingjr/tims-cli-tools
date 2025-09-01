clean-coverage:
  - uv run coverage erase
  - rm -rf htmlcov/ # Remove the generated HTML report directory

lint:
  - uv run -m ruff check --fix .
  - uv run -m ruff format .
test:
  - uv run coverage run -m pytest
  - uv run coverage report
  - uv run coverage html
typing:
  - uv run python3 -m mypy src
all: lint typing clean-coverage test
