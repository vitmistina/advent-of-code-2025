# Implementation Plan: Day 7 Part 1 - Tachyon Beam Split Counter

**Feature Branch**: `001-day-07-part-1`
**Spec**: [spec.md](../spec.md)
**Created**: 2025-12-09

## Overview

This plan describes the steps to implement a solution for Day 7 Part 1, which simulates tachyon beam splitting in a manifold as described in the Advent of Code puzzle. The solution must:

- Parse a 2D grid from an input file
- Simulate beam movement and splitting according to the rules
- Count the number of splits
- Support both integration testing (test_input.txt) and main puzzle input (input.txt)

## Complexity Analysis

- **Beam simulation**: The main complexity is in simulating multiple beams, especially as they split and overlap. Overlapping beams must be carefully managed to prevent double-counting splits and to ensure that merged beams are handled correctly for further splits.
- **Critical behavior**: If two splits result in three beams (with the middle beam duplicated), this still counts as **two splits**, and the middle beams merge into one for subsequent processing. The merged beam can then trigger further splits down the line.
- **Beam merging**: Beams that occupy the same position and move in the same direction should be merged to prevent duplicate processing and double-counting of splits.
- **Testability**: The plan must ensure that the solution is easily testable with both the provided example and arbitrary inputs.

## Phases

### Phase 0: Research & Clarification

- Review puzzle rules and clarify split and merge behavior for overlapping beams
- Research efficient algorithms for simulating multiple beams in a grid (BFS/queue-based, state deduplication)
- Investigate approaches to track and merge duplicate beams (same position + direction)
- Review prior AoC solutions for similar grid/beam problems for best practices

### Phase 1: Data Model & Contracts

- Define data structures:
  - Grid (2D list of chars)
  - Beam (position, direction, active state)
  - Split tracking (set of split locations, split count)
- Define input/output contracts:
  - Input: test_input.txt or input.txt (grid as text)
  - Output: single integer (split count)
- Specify module interface for splitter logic

### Phase 2: Implementation

- Implement parser for input files
- Implement beam simulation engine:
  - Start from 'S', move downward
  - On splitter ('^'), stop current beam, emit left/right beams (increment split count by 1)
  - Track all active beams by (position, direction), merging duplicates to prevent double-processing
  - Count splits: each splitter encounter = 1 split, regardless of beam merging
  - If two splits result in three beams (middle beam duplicated), count 2 splits and merge middle beams into one
  - Merged beams continue simulation and can trigger further splits
- Implement CLI or script entry point for both test and main input
- No error handling needed for missing 'S' or invalid characters

### Phase 3: Testing & Validation

- Write unit tests for splitter logic and beam simulation
- Write unit tests specifically for beam merging scenarios
- Write integration test using test_input.txt (expect 21 splits)
- Validate solution on input.txt (AoC main input)
- Test edge cases (no splitters, overlapping beams, merged beams triggering further splits)

### Phase 4: Documentation & Review

- Document code and usage
- Update README and quickstart as needed
- Review against spec and checklist

## Deliverables

- `solution.py` (main logic)
- `splitter.py` or module for splitter logic
- Tests (unit and integration)
- Updated README/quickstart
- All code reviewed for clarity and correctness
