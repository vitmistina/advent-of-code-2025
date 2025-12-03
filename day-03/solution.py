"""Day 3 Part 1: Battery Bank Joltage Calculator.

Solution for Advent of Code 2025 Day 3.
Calculates maximum joltage from battery banks.
"""

from pathlib import Path


def parse_input(input_text: str) -> list[str]:
    """
    Parse input text into a list of battery bank strings.

    Args:
        input_text (str): Multi-line string where each line is a battery bank.

    Returns:
        list[str]: List of battery bank strings (one per line, whitespace stripped).
    """
    return [line.strip() for line in input_text.strip().splitlines() if line.strip()]


def max_joltage(bank: str) -> int:
    """
    Find maximum joltage from a battery bank using greedy algorithm.

    The maximum joltage is the largest two-digit number that can be formed
    by selecting exactly two batteries (digits) from the bank while
    maintaining their left-to-right order.

    Greedy approach:
    1. First battery: max digit in bank[:-1] (need at least one after it)
    2. Second battery: max digit after first battery's position

    Args:
        bank (str): String of digit characters representing batteries.

    Returns:
        int: Maximum joltage value (0-99).
    """
    if len(bank) < 2:
        return 0
    max_first_digit: str = max(bank[:-1])
    first_pos: int = bank.index(max_first_digit)
    max_second_digit: str = max(bank[first_pos + 1 :])
    joltage: int = int(max_first_digit) * 10 + int(max_second_digit)
    return joltage


def solve_part1(input_text: str) -> int:
    """
    Solve Day 3 Part 1: Calculate total output joltage.

    Processes each battery bank to find its maximum joltage, then
    sums all maximum joltages to get the total output.

    Args:
        input_text (str): Multi-line string of battery banks.

    Returns:
        int: Total output joltage (sum of all maximum joltages).
    """
    banks: list[str] = parse_input(input_text)
    total: int = sum(max_joltage(bank) for bank in banks)
    return total


def select_max_k_digits(bank: str, k: int = 12) -> str:
    """
    Select exactly k digits from bank to form the largest possible number.

    Uses monotonic stack algorithm to select k digits in order that form
    the maximum possible k-digit number. Algorithm runs in O(n) time.

    The monotonic stack works by:
    1. For each digit, pop smaller digits if we have room to refill stack
    2. Push digit if stack has < k digits
    3. Result: Stack contains largest k digits in order

    Args:
        bank (str): String of digit characters representing batteries.
        k (int): Number of digits to select (default 12).

    Returns:
        str: String of k digits forming the maximum number.

    Raises:
        ValueError: If bank has fewer than k digits.
    """
    n = len(bank)
    if n < k:
        raise ValueError(f"Bank has {n} digits but need {k}")

    stack = []
    for i, digit in enumerate(bank):
        # Pop smaller digits if we have enough remaining to fill stack to k
        while stack and digit > stack[-1] and len(stack) + (n - i) > k:
            stack.pop()
        # Add digit if stack not full
        if len(stack) < k:
            stack.append(digit)

    return "".join(stack)


def solve_part2(input_text: str) -> int:
    """
    Solve Day 3 Part 2: Maximize joltage with 12 batteries per bank.

    For each battery bank, selects exactly 12 digits (batteries) to form
    the largest possible 12-digit number while preserving left-to-right order.
    Sums the resulting numbers across all banks.

    Uses monotonic stack algorithm for optimal O(n) performance per bank.

    Args:
        input_text (str): Multi-line string of battery banks.

    Returns:
        int: Total output joltage (sum of all maximum 12-digit numbers).
    """
    banks: list[str] = parse_input(input_text)
    total: int = sum(int(select_max_k_digits(bank)) for bank in banks)
    return total


def main() -> None:
    """
    Entry point for running solution with input.txt.

    Reads the input file, computes the total output joltage,
    and prints the result for Part 1 and Part 2.
    """
    input_file: Path = Path(__file__).parent / "input.txt"
    input_text: str = input_file.read_text()
    result1: int = solve_part1(input_text)
    result2: int = solve_part2(input_text)
    print(f"Part 1: {result1}")
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
