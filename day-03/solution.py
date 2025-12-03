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


def main() -> None:
    """
    Entry point for running solution with input.txt.

    Reads the input file, computes the total output joltage,
    and prints the result for Part 1.
    """
    input_file: Path = Path(__file__).parent / "input.txt"
    input_text: str = input_file.read_text()
    result: int = solve_part1(input_text)
    print(f"Part 1: {result}")


if __name__ == "__main__":
    main()
