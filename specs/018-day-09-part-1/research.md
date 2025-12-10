# Phase 0 Research: AoC Day 9 Part 1 - Largest Red Tile Rectangle

## Decision Log

### 1. Input Parsing Robustness

- **Decision**: Use try/except with validation for each line; raise ValueError on malformed input.
- **Rationale**: Ensures immediate halt on bad input, clear error message, matches AoC expectations.
- **Alternatives considered**: Ignore bad lines (not robust), skip errors (not allowed by spec).

### 2. Data Structure Choice

- **Decision**: Use tuple `(x, y)` for each coordinate; store in a list.
- **Rationale**: Tuples are lightweight, fast, and idiomatic for AoC; list allows easy iteration and combinations.
- **Alternatives considered**: namedtuple, dataclass (overkill for simple coordinates).

### 3. Performance for Large Inputs

- **Decision**: Use itertools.combinations for pair generation; list for storage.
- **Rationale**: Efficient for n <= 1000; combinations avoids duplicate/permutation issues.
- **Alternatives considered**: Set, numpy arrays (not needed for this scale).

### 4. Error Handling Pattern

- **Decision**: Raise Exception (ValueError) and exit on error.
- **Rationale**: Matches AoC script style, clear for debugging, halts execution as required.
- **Alternatives considered**: sys.exit (less informative), custom error class (unnecessary).

### 5. Testing Approach

- **Decision**: Use pytest for test_solution.py; inline asserts for quick checks in solution.py.
- **Rationale**: pytest is standard for AoC repo, inline asserts are fast for development.
- **Alternatives considered**: Only inline asserts (less maintainable), only pytest (slower dev loop).

### 6. Handling Multiple Max Rectangles

- **Decision**: Return any one pair with max area (not all).
- **Rationale**: Spec allows either, but AoC expects a single answer; returning all adds complexity.
- **Alternatives considered**: Return all pairs (not needed).

## Best Practices

- Use Python 3.10+ features (type hints, match/case if needed).
- Follow PEP8 and ruff for style/linting.
- Use pytest for test files, inline asserts for solution quick checks.
- Use standard library only for file I/O and combinations.
- Organize code in day-09/ folder: solution.py, test_solution.py, input.txt, test_input.txt.
- Use clear, conventional commit messages.
- Update README progress tracker after completion.

## All clarifications resolved. Ready for Phase 1 design.
