"""Tests for Day 10 Part 2: Joltage Configuration."""

import pytest
import sys
from pathlib import Path

# Add day-10 to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from solution import parse_input, parse_line


# Phase 3: US4 - Parsing Tests (T006-T010)


def test_parse_first_example_line():
    """T007: Verify parse_line extracts buttons and targets for first example."""
    line = "[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}"

    machine = parse_line(line)

    assert machine["buttons"] == [[3], [1, 3], [2], [2, 3], [0, 2], [0, 1]]
    assert machine["jolts"] == [3, 5, 4, 7]


def test_parse_second_example_line():
    """T008: Verify parse_line extracts buttons and targets for second example."""
    line = "[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}"

    machine = parse_line(line)

    assert machine["buttons"] == [[0, 2, 3, 4], [2, 3], [0, 4], [0, 1, 2], [1, 2, 3, 4]]
    assert machine["jolts"] == [7, 5, 12, 7, 2]


def test_parse_third_example_line():
    """T009: Verify parse_line extracts 4 buttons and 6 targets for third example."""
    line = "[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}"

    machine = parse_line(line)

    assert len(machine["buttons"]) == 4
    assert machine["buttons"] == [[0, 1, 2, 3, 4], [0, 3, 4], [0, 1, 2, 4, 5], [1, 2]]
    assert len(machine["jolts"]) == 6
    assert machine["jolts"] == [10, 11, 11, 5, 10, 5]


# Phase 4: US3 - Core Algorithm Tests (RED: T011-T014)


def test_build_button_matrix_structure():
    """T011: Verify button matrix construction is correct."""
    import numpy as np
    from solution_part2 import build_button_matrix

    buttons = [[3], [1, 3], [2], [2, 3], [0, 2], [0, 1]]
    num_counters = 4

    B = build_button_matrix(buttons, num_counters)

    # Expected matrix:
    #      B0  B1  B2  B3  B4  B5
    # C0: [ 0   0   0   0   1   1 ]
    # C1: [ 0   1   0   0   0   1 ]
    # C2: [ 0   0   1   1   1   0 ]
    # C3: [ 1   1   0   1   0   0 ]

    expected = np.array(
        [[0, 0, 0, 0, 1, 1], [0, 1, 0, 0, 0, 1], [0, 0, 1, 1, 1, 0], [1, 1, 0, 1, 0, 0]]
    )

    assert np.array_equal(B, expected), f"Matrix mismatch:\n{B}\nvs expected:\n{expected}"


def test_verify_solution_accepts_valid():
    """T012: Test that verify_solution accepts a valid solution."""
    import numpy as np
    from solution_part2 import verify_solution

    B = np.array([[1, 2], [1, 1]])
    t = np.array([5, 3])
    x = np.array([1, 2])  # 1×1 + 2×2 = 5, 1×1 + 1×2 = 3

    assert verify_solution(B, t, x), "Valid solution rejected"


def test_verify_solution_rejects_invalid():
    """T013: Test that verify_solution rejects invalid solutions."""
    import numpy as np
    from solution_part2 import verify_solution

    B = np.array([[1, 2], [1, 1]])
    t = np.array([5, 3])
    x = np.array([0, 2])  # 0×1 + 2×2 = 4 ≠ 5

    assert not verify_solution(B, t, x), "Invalid solution accepted"


# Phase 5: US1 - Example Machine Tests (RED: T024-T028)


def test_example_1_machine():
    """T024: Test first example machine: expected minimum presses = 10."""
    import numpy as np
    from solution_part2 import build_button_matrix, solve_integer_linear_system, verify_solution

    # Machine: [.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
    buttons = [[3], [1, 3], [2], [2, 3], [0, 2], [0, 1]]
    targets = [3, 5, 4, 7]

    B = build_button_matrix(buttons, len(targets))
    t = np.array(targets)

    x = solve_integer_linear_system(B, t)

    assert x is not None, "System should be feasible"
    assert verify_solution(B, t, x), "Solution must satisfy B·x = t"
    assert np.all(x >= 0), "All button presses must be non-negative"
    assert np.sum(x) == 10, f"Expected 10 presses, got {np.sum(x)}"


def test_example_2_machine():
    """T025: Test second example machine: expected minimum presses = 12."""
    import numpy as np
    from solution_part2 import build_button_matrix, solve_integer_linear_system, verify_solution

    buttons = [[0, 2, 3, 4], [2, 3], [0, 4], [0, 1, 2], [1, 2, 3, 4]]
    targets = [7, 5, 12, 7, 2]

    B = build_button_matrix(buttons, len(targets))
    t = np.array(targets)

    x = solve_integer_linear_system(B, t)

    assert x is not None, "System should be feasible"
    assert verify_solution(B, t, x), "Solution must satisfy B·x = t"
    assert np.sum(x) == 12, f"Expected 12 presses, got {np.sum(x)}"


def test_example_3_machine():
    """T026: Test third example machine: expected minimum presses = 11."""
    import numpy as np
    from solution_part2 import build_button_matrix, solve_integer_linear_system, verify_solution

    buttons = [[0, 1, 2, 3, 4], [0, 3, 4], [0, 1, 2, 4, 5], [1, 2]]
    targets = [10, 11, 11, 5, 10, 5]

    B = build_button_matrix(buttons, len(targets))
    t = np.array(targets)

    x = solve_integer_linear_system(B, t)

    assert x is not None, "System should be feasible"
    assert verify_solution(B, t, x), "Solution must satisfy B·x = t"
    assert np.sum(x) == 11, f"Expected 11 presses, got {np.sum(x)}"


def test_zero_target_case():
    """T027: Test edge case where all targets are zero (optimal: 0 presses)."""
    import numpy as np
    from solution_part2 import build_button_matrix, solve_integer_linear_system

    buttons = [[0], [1], [0, 1]]
    targets = [0, 0]

    B = build_button_matrix(buttons, len(targets))
    t = np.array(targets)

    x = solve_integer_linear_system(B, t)

    assert x is not None, "Zero target should be feasible"
    assert np.sum(x) == 0, "Zero target requires 0 presses"


# Phase 6: US2 - Aggregation Tests (T033-T040)


def test_all_examples_aggregate():
    """T033: Test aggregation across all three example machines: total = 33."""
    from solution_part2 import solve_part2

    test_input = Path(__file__).parent / "test_input.txt"
    machines = parse_input(test_input.read_text())

    total = solve_part2(machines)

    assert total == 33, f"Expected total 33 presses, got {total}"
