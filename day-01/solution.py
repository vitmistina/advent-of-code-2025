"""Advent of Code 2025 - Day 01 Solution."""

from pathlib import Path


def parse_input(input_text: str):
    """Parse the puzzle input."""
    lines = input_text.strip().split("\n")
    # TODO: Parse input according to puzzle requirements
    return lines


def solve_part1(data) -> int:
    """Solve Part 1 of the puzzle."""
    # TODO: Implement Part 1 solution
    return 0


def solve_part2(data) -> int:
    """Solve Part 2 of the puzzle."""
    # TODO: Implement Part 2 solution
    return 0


def main():
    """Main entry point."""
    input_file = Path(__file__).parent / "input.txt"
    input_text = input_file.read_text()
    
    data = parse_input(input_text)
    
    part1_answer = solve_part1(data)
    print(f"Part 1: {part1_answer}")
    
    part2_answer = solve_part2(data)
    print(f"Part 2: {part2_answer}")


if __name__ == "__main__":
    main()
