import pytest
from solution import FreshRange, merge_ranges


def test_parse_ranges_first_lines():
    # T008: Parsing ranges on first lines
    lines = ["3-5", "10-14", "16-20", "12-18"]
    ranges = [FreshRange(*(map(int, l.split("-")))) for l in lines]
    assert ranges[0] == FreshRange(3, 5)
    assert ranges[1] == FreshRange(10, 14)
    assert ranges[2] == FreshRange(16, 20)
    assert ranges[3] == FreshRange(12, 18)


def test_inclusive_range_interpretation():
    # T009: Inclusive range interpretation
    r = FreshRange(10, 14)
    assert r.start == 10 and r.end == 14
    assert list(range(r.start, r.end + 1)) == [10, 11, 12, 13, 14]


def test_overlapping_ranges_merge():
    # T010: Handling overlapping ranges
    ranges = [FreshRange(10, 14), FreshRange(12, 18)]
    merged = merge_ranges(ranges)
    assert merged == [(10, 18)]


def test_parse_available_ids_after_blank_line():
    # T011: Parsing available IDs after blank line
    data = "3-5\n10-14\n16-20\n12-18\n\n1\n5\n8\n11\n17\n32\n"
    from solution import parse_database, FreshRange

    ranges, ids = parse_database(data)
    assert ranges == [FreshRange(3, 5), FreshRange(10, 14), FreshRange(16, 20), FreshRange(12, 18)]
    assert ids == [1, 5, 8, 11, 17, 32]


def test_is_fresh_id_5():
    # T018: Ingredient ID 5 is fresh
    from solution import is_fresh, merge_ranges, FreshRange

    ranges = [FreshRange(3, 5), FreshRange(10, 14), FreshRange(16, 20), FreshRange(12, 18)]
    merged = merge_ranges(ranges)
    assert is_fresh(5, merged) is True


def test_is_fresh_id_1():
    # T019: Ingredient ID 1 is spoiled
    from solution import is_fresh, merge_ranges, FreshRange

    ranges = [FreshRange(3, 5), FreshRange(10, 14), FreshRange(16, 20), FreshRange(12, 18)]
    merged = merge_ranges(ranges)
    assert is_fresh(1, merged) is False


def test_is_fresh_id_17():
    # T020: Ingredient ID 17 is fresh (overlapping ranges)
    from solution import is_fresh, merge_ranges, FreshRange

    ranges = [FreshRange(3, 5), FreshRange(10, 14), FreshRange(16, 20), FreshRange(12, 18)]
    merged = merge_ranges(ranges)
    assert is_fresh(17, merged) is True


def test_is_fresh_id_32():
    # T021: Ingredient ID 32 is spoiled
    from solution import is_fresh, merge_ranges, FreshRange

    ranges = [FreshRange(3, 5), FreshRange(10, 14), FreshRange(16, 20), FreshRange(12, 18)]
    merged = merge_ranges(ranges)
    assert is_fresh(32, merged) is False


def test_is_fresh_id_11():
    # T022: Ingredient ID 11 is fresh
    from solution import is_fresh, merge_ranges, FreshRange

    ranges = [FreshRange(3, 5), FreshRange(10, 14), FreshRange(16, 20), FreshRange(12, 18)]
    merged = merge_ranges(ranges)
    assert is_fresh(11, merged) is True


def test_is_fresh_id_8():
    # T023: Ingredient ID 8 is spoiled
    from solution import is_fresh, merge_ranges, FreshRange

    ranges = [FreshRange(3, 5), FreshRange(10, 14), FreshRange(16, 20), FreshRange(12, 18)]
    merged = merge_ranges(ranges)
    assert is_fresh(8, merged) is False


def test_example_database_count_fresh():
    # T028: Example database counts 3 fresh ingredients (5, 11, 17)
    from solution import solve_part1

    data = "3-5\n10-14\n16-20\n12-18\n\n1\n5\n8\n11\n17\n32\n"
    assert solve_part1(data) == 3


def test_empty_available_ingredients():
    # T029: Empty available ingredients list returns count 0
    from solution import solve_part1

    data = "3-5\n10-14\n\n"
    assert solve_part1(data) == 0


def test_all_ids_fresh():
    # T030: All IDs fresh scenario
    from solution import solve_part1

    data = "1-100\n\n5\n10\n50\n99\n"
    assert solve_part1(data) == 4


def test_no_ids_fresh():
    # T031: No IDs fresh scenario
    from solution import solve_part1

    data = "10-20\n\n1\n5\n25\n30\n"
    assert solve_part1(data) == 0
