# Quickstart: Day 3 Part 2

## How to Solve

1. For each bank (line of digits):
   - Use monotonic stack algorithm to select 12 digits for the largest possible number
   - Convert selected digits to integer
2. Sum across all banks

## Example

Input:

```
987654321111111
811111111111119
234234234234278
818181911112111
```

Output: 3121910778619

## Implementation Sketch

```python
def select_max_k_digits(bank: str, k: int = 12) -> str:
    stack = []
    n = len(bank)
    for i, digit in enumerate(bank):
        while stack and digit > stack[-1] and len(stack) + (n - i) > k:
            stack.pop()
        if len(stack) < k:
            stack.append(digit)
    return ''.join(stack)

def solve_part2(input_text: str) -> int:
    banks = [line.strip() for line in input_text.strip().splitlines() if line.strip()]
    return sum(int(select_max_k_digits(bank)) for bank in banks)
```
