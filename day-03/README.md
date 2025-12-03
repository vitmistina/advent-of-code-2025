# Day 03

## Puzzle Description

Battery Bank Joltage Calculator - Advent of Code 2025 Day 3

## Notes

- **Part 1**: Select 2 batteries to maximize joltage using greedy algorithm

  - Greedy approach: max digit in bank[:-1], then max digit after that position
  - O(n) time complexity per bank

- **Part 2**: Select 12 batteries to maximize joltage using monotonic stack
  - Monotonic stack algorithm for optimal k-digit selection
  - O(n) time complexity per bank
  - Test cases:
    - `987654321111111` → `987654321111`
    - `811111111111119` → `811111111119`
    - `234234234234278` → `434234234278`
    - `818181911112111` → `888911112111`
  - Example total: 3121910778619

## Algorithm: Monotonic Stack (Part 2)

The monotonic stack algorithm selects exactly k digits from a string to form the largest possible k-digit number while preserving order:

1. Initialize empty stack
2. For each digit in the input:
   - Pop smaller digits from stack if we have enough remaining digits to refill
   - Push digit if stack has < k elements
3. Result: Stack contains the largest k digits in order

**Time Complexity**: O(n) - each digit is pushed/popped at most once
**Space Complexity**: O(k) - stack holds exactly k digits

## Usage

```powershell
# Run tests (RED phase)
uv run pytest day-03/test_solution.py -v

# Run solution (GREEN phase)
uv run python day-03/solution.py
```
