# Contributing

1. Fork the repository and clone it.
2. Create a virtual environment and install the project for development:
   ```bash
   python -m venv .venv && source .venv/bin/activate
   pip install -e ".[dev]"
   ```
3. Create a branch: `git checkout -b feature/my-feature`.
4. Make your changes and add tests.
5. Check the code:
   ```bash
   ruff check .
   pytest
   ```
6. Open a Pull Request.

## Adding a unit
- Add the factor (relative to the base unit) to the right table in `src/unitconv/units.py`.
- The unit name must be unique across all categories and written in lowercase.
- Add aliases to `ALIASES` (Russian, English) if useful.
- Add a test to `tests/test_core.py`.
