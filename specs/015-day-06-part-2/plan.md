# Implementation Plan: Day 6 Part 2 - Cephalopod Math (Right-to-Left Columns)

## Overview

Implement a worksheet solver that parses columns right-to-left, reconstructs numbers from columns, and applies the correct operator per problem. Reuse and adapt the streaming pipeline and data model from Part 1.

## Steps

1. **Parsing Logic**: Implement columnar parsing (right-to-left), reconstruct numbers from columns (top-to-bottom digits).
2. **Grouping Logic**: Group columns into problems, separated by columns of only spaces.
3. **Problem Extraction**: For each problem, extract operands and operator (bottom of column).
4. **Evaluation**: Apply operator to operands, compute result.
5. **Aggregation**: Sum all problem results for grand total.
6. **Testing**: Validate with all examples and edge cases from spec.
7. **Error Handling**: Raise clear errors for malformed input.

## Reuse

- `Problem` dataclass and evaluation logic from Part 1
- Streaming pipeline structure

## Deliverables

- Updated agent context
- Data model, contracts, quickstart, research
- Implementation in `solution_part2.py` (to be created)
- Tests for all acceptance criteria
