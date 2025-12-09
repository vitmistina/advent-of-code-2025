# Research: Day 6 Part 2 - Cephalopod Math (Right-to-Left Columns)

## Decision: Parsing and Solving Logic

- **Chosen Approach:** Adapt the streaming pipeline from Part 1, but change the parsing logic to process columns right-to-left, reconstructing numbers from columns (top-to-bottom digits), and grouping columns into problems separated by space columns.
- **Rationale:** The Part 1 solution is modular and robust, with clear separation of parsing, grouping, and evaluation. Reusing the pipeline structure allows for minimal code duplication and easier maintenance. Only the parsing/grouping logic needs to be replaced for Part 2.
- **Alternatives Considered:**
  - Rewriting the entire solution from scratch (less maintainable, more error-prone)
  - Adapting only the evaluation logic (insufficient, as grouping and extraction are fundamentally different)

## Decision: Data Model

- **Chosen Approach:** Reuse the `Problem` dataclass and evaluation logic from Part 1. Only the extraction of operands and operators changes.
- **Rationale:** The data model is generic and fits both vertical and columnar math problems. This allows for shared testing and easier extension.
- **Alternatives Considered:**
  - Creating a new data model for Part 2 (unnecessary complexity)

## Decision: Grouping Columns into Problems

- **Chosen Approach:** Identify columns of only spaces as separators, then group adjacent non-space columns into problems, reading right-to-left.
- **Rationale:** This matches the problem description and is robust to variable spacing and alignment.
- **Alternatives Considered:**
  - Using fixed-width grouping (not robust to input variations)

## Decision: Number Extraction

- **Chosen Approach:** For each problem, reconstruct each number by reading the digits in a column from top to bottom (most significant at top).
- **Rationale:** This matches the cephalopod math rules for Part 2.
- **Alternatives Considered:**
  - Reading numbers left-to-right (incorrect for Part 2)

## Decision: Operator Extraction

- **Chosen Approach:** The operator is the symbol at the bottom of each problem column.
- **Rationale:** Consistent with both Part 1 and Part 2 rules.
- **Alternatives Considered:**
  - Placing operator elsewhere (not supported by input format)

## Decision: Error Handling

- **Chosen Approach:** Raise clear errors for missing numbers, operators, or malformed columns. Handle edge cases as specified.
- **Rationale:** Ensures robustness and clear feedback for invalid inputs.
- **Alternatives Considered:**
  - Silent failure or skipping invalid problems (less user-friendly)

## Summary

- The solution will adapt the Part 1 pipeline, replacing only the parsing and grouping logic for right-to-left column reading.
- The data model and evaluation logic are reused.
- All acceptance criteria and edge cases are covered by design.
