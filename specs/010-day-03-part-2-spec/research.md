# Research: Day 3 Part 2 - Maximize Joltage with 12 Batteries

**Feature**: [spec.md](spec.md)
**Date**: December 3, 2025
**Purpose**: Research technical decisions and algorithms for maximum 12-digit joltage calculation

## Research Questions

### 1. How to select the largest possible 12-digit number from a string of up to 100 digits, preserving order?

**Decision**: Use monotonic stack (optimal subsequence selection) algorithm, O(n) per bank

**Rationale**:

- Need to select exactly 12 digits, preserving order, to maximize the resulting number
- Brute-force (O(n^12)) is infeasible for n=100
- Monotonic stack is proven optimal for "maximum number by selecting k digits in order" problems

**Algorithm**:

- Initialize an empty stack
- For each digit in the bank (left to right):
  - While stack is not empty, digit > stack[-1], and enough digits remain to fill stack to k, pop stack
  - Push digit if stack has < k digits
- Result: Stack contains the largest possible k digits in order

**Complexity**: O(n) per bank

**Alternatives considered**:

- Brute-force: O(n^k), rejected
- Dynamic programming: O(nk), feasible but more complex
- Greedy with lookahead: O(nk), but monotonic stack is simpler and optimal

**Test cases**:

- Input: "987654321111111" → Output: "987654321111"
- Input: "811111111111119" → Output: "811111111119"
- Input: "234234234234278" → Output: "434234234278"
- Input: "818181911112111" → Output: "888911112111"

### 2. How to parse input and handle multiple battery banks?

**Decision**: Split by newlines, process each line independently

**Rationale**: Each line is a bank; process each with the monotonic stack algorithm

### 3. How to calculate total output joltage?

**Decision**: Sum the integer values of the selected 12-digit numbers from each bank

### 4. Edge cases to handle

- Bank with <12 digits: Error or skip
- All identical digits: Stack will select first k digits
- Multiple selections yielding same max: Any valid selection is acceptable

### 5. Testing strategy

- Use pytest or assert statements
- Test all provided examples and edge cases

## Technology Stack Decisions

- Python 3.10+
- Stdlib only
- PEP8, docstrings, ruff

## Risk Assessment

- Low risk: Algorithm is optimal and proven
- No brute-force
- Handles large banks efficiently
