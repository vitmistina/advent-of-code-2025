# advent-of-code-2025 Dev Directives

## Absolute Rules

- PowerShell only when sharing commands.
- Never emit Unix-only pipe idioms like `| tail`, `| head`, or `| sed`; always give native PowerShell equivalents such as `Get-Content -Tail`, `Select-Object -Last/-First`, or `Select-String`.
- `uv` is the one true runner: `uv run pytest`, `uv run python ...`, `uv tool run ruff`, etc. Never mention pip, python -m venv, or system python.
- Commits follow Conventional Commits: `type(scope): msg`.

## Spec Preparation Protocol

1. Strip the AoC description into executable acceptance criteria. These will be later expanded into pytest parametrizations, CLI golden files, and docstring examples until coverage mirrors the narrative perfectly.

## Implementation Protocol

1. Begin every task by skimming `.specify/memory/constitution.md` and citing any clause that influences the solution before writing code.
2. Practice unwavering TDD: create a failing test (or acceptance spec) first, make it pass with the smallest change, then refactor. No production code without a red test.

## Testing Expectations

- Treat tests as living documentation: name them after the scenario described in the AoC text or specs.
- Prefer `uv run pytest path::TestClass::test_case` during red/green loops and keep watch runs via `uv run pytest -k keyword`.
- For CLI flows, include snapshot-style tests that assert full stdout derived from the AoC example inputs.

## Delivery Checklist

- Document how extracted examples map to tests inside commit messages or PR notes.
- Call out any AoC example lacking direct test coverage; add TODO tests rather than leaving gaps.
- Keep instructions PowerShell-friendly (no `tail`, `head`, or bashisms).
