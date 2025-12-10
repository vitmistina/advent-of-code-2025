from .solution import FreshRange, merge_ranges


def test_parse_ranges_first_lines():
    # T008: Parsing ranges on first lines
    lines = ["3-5", "10-14", "16-20", "12-18"]
    ranges = [FreshRange(*(map(int, line.split("-")))) for line in lines]
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
    from .solution import FreshRange, parse_database

    ranges, ids = parse_database(data)
    assert ranges == [FreshRange(3, 5), FreshRange(10, 14), FreshRange(16, 20), FreshRange(12, 18)]
    assert ids == [1, 5, 8, 11, 17, 32]


def test_is_fresh_id_5():
    # T018: Ingredient ID 5 is fresh
    from solution import FreshRange, is_fresh, merge_ranges

    ranges = [FreshRange(3, 5), FreshRange(10, 14), FreshRange(16, 20), FreshRange(12, 18)]
    merged = merge_ranges(ranges)
    assert is_fresh(5, merged) is True


def test_is_fresh_id_1():
    # T019: Ingredient ID 1 is spoiled
    from solution import FreshRange, is_fresh, merge_ranges

    ranges = [FreshRange(3, 5), FreshRange(10, 14), FreshRange(16, 20), FreshRange(12, 18)]
    merged = merge_ranges(ranges)
    assert is_fresh(1, merged) is False


def test_is_fresh_id_17():
    # T020: Ingredient ID 17 is fresh (overlapping ranges)
    from solution import FreshRange, is_fresh, merge_ranges

    ranges = [FreshRange(3, 5), FreshRange(10, 14), FreshRange(16, 20), FreshRange(12, 18)]
    merged = merge_ranges(ranges)
    assert is_fresh(17, merged) is True


def test_is_fresh_id_32():
    # T021: Ingredient ID 32 is spoiled
    from solution import FreshRange, is_fresh, merge_ranges

    ranges = [FreshRange(3, 5), FreshRange(10, 14), FreshRange(16, 20), FreshRange(12, 18)]
    merged = merge_ranges(ranges)
    assert is_fresh(32, merged) is False


def test_is_fresh_id_11():
    # T022: Ingredient ID 11 is fresh
    from solution import FreshRange, is_fresh, merge_ranges

    ranges = [FreshRange(3, 5), FreshRange(10, 14), FreshRange(16, 20), FreshRange(12, 18)]
    merged = merge_ranges(ranges)
    assert is_fresh(11, merged) is True


def test_is_fresh_id_8():
    # T023: Ingredient ID 8 is spoiled
    from solution import FreshRange, is_fresh, merge_ranges

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


# =============================================================================
# PHASE 3: USER STORY 1 - Calculate Total Fresh Ingredients from Ranges (P1)
# =============================================================================


def test_part2_scenario_1_complex_overlapping():
    """US1 Acceptance Scenario 1: [3-5, 10-14, 16-20, 12-18] -> 14 fresh IDs"""
    from solution import solve_part2

    data = "3-5\n10-14\n16-20\n12-18\n\n1\n5\n8\n11\n17\n32\n"
    result = solve_part2(data)
    assert result == 14, f"Expected 14 fresh IDs, got {result}"


def test_part2_scenario_2_single_range():
    """US1 Acceptance Scenario 2: [3-5] -> 3 fresh IDs"""
    from solution import solve_part2

    data = "3-5\n\n"
    result = solve_part2(data)
    assert result == 3, f"Expected 3 fresh IDs, got {result}"


def test_part2_scenario_3_overlapping_ranges():
    """US1 Acceptance Scenario 3: [10-14, 16-20, 12-18] -> 11 fresh IDs"""
    from solution import solve_part2

    data = "10-14\n16-20\n12-18\n\n"
    result = solve_part2(data)
    assert result == 11, f"Expected 11 fresh IDs, got {result}"


def test_part2_scenario_4_nonadjacent_ranges():
    """US1 Acceptance Scenario 4: [1-3, 5-7] -> 6 fresh IDs"""
    from solution import solve_part2

    data = "1-3\n5-7\n\n"
    result = solve_part2(data)
    assert result == 6, f"Expected 6 fresh IDs, got {result}"


def test_part2_scenario_5_single_id_range():
    """US1 Acceptance Scenario 5: [10-10] -> 1 fresh ID"""
    from solution import solve_part2

    data = "10-10\n\n"
    result = solve_part2(data)
    assert result == 1, f"Expected 1 fresh ID, got {result}"


def test_part2_scenario_6_multiple_single_id_ranges():
    """US1 Acceptance Scenario 6: [1-1, 2-2, 3-3] -> 3 fresh IDs"""
    from solution import solve_part2

    data = "1-1\n2-2\n3-3\n\n"
    result = solve_part2(data)
    assert result == 3, f"Expected 3 fresh IDs, got {result}"


def test_part2_scenario_7_significantly_overlapping():
    """US1 Acceptance Scenario 7: [1-5, 3-7] -> 7 fresh IDs"""
    from solution import solve_part2

    data = "1-5\n3-7\n\n"
    result = solve_part2(data)
    assert result == 7, f"Expected 7 fresh IDs, got {result}"


# =============================================================================
# PHASE 4: USER STORY 2 - Parse Fresh Ranges and Ignore Available IDs (P1)
# =============================================================================


def test_part2_us2_parse_ranges_ignore_ids_scenario_1():
    """US2 Acceptance Scenario 1: Parse ranges, ignore available IDs"""
    from solution import parse_ranges_part2, solve_part2

    data = "3-5\n10-14\n16-20\n12-18\n\n1\n5\n8\n11\n17\n32\n"
    ranges = parse_ranges_part2(data)
    assert len(ranges) == 4
    assert ranges[0] == FreshRange(3, 5)
    assert ranges[1] == FreshRange(10, 14)
    assert ranges[2] == FreshRange(16, 20)
    assert ranges[3] == FreshRange(12, 18)

    # Verify result ignores IDs (should be 14, not 3)
    result = solve_part2(data)
    assert result == 14


def test_part2_us2_parse_single_range_ignore_ids():
    """US2 Acceptance Scenario 2: Single range, ignore available IDs"""
    from solution import parse_ranges_part2

    data = "5-5\n\n1\n2\n3\n4\n5\n6\n7\n"
    ranges = parse_ranges_part2(data)
    assert len(ranges) == 1
    assert ranges[0] == FreshRange(5, 5)


def test_part2_us2_parse_ranges_large_ids_list():
    """US2 Acceptance Scenario 3: Process ranges only, not iterate through available IDs"""
    from solution import parse_ranges_part2

    # Large IDs list should be ignored
    data = "1-5\n10-15\n\n" + "\n".join(str(i) for i in range(1, 1001))
    ranges = parse_ranges_part2(data)
    assert len(ranges) == 2
    assert ranges[0] == FreshRange(1, 5)
    assert ranges[1] == FreshRange(10, 15)


# =============================================================================
# PHASE 5: USER STORY 3 - Handle Edge Cases in Range Coverage (P2)
# =============================================================================


def test_part2_us3_large_range():
    """US3 Acceptance Scenario 1: [1-100] -> 100 fresh IDs"""
    from solution import solve_part2

    data = "1-100\n\n"
    result = solve_part2(data)
    assert result == 100, f"Expected 100 fresh IDs, got {result}"


def test_part2_us3_adjacent_contiguous_ranges():
    """US3 Acceptance Scenario 2: [1-10, 11-20] -> 20 fresh IDs (merged)"""
    from solution import solve_part2

    data = "1-10\n11-20\n\n"
    result = solve_part2(data)
    assert result == 20, f"Expected 20 fresh IDs, got {result}"


def test_part2_us3_multiple_overlapping_patterns():
    """US3 Acceptance Scenario 3: [5-10, 3-7, 8-12] -> 10 fresh IDs (3-12)"""
    from solution import solve_part2

    data = "5-10\n3-7\n8-12\n\n"
    result = solve_part2(data)
    assert result == 10, f"Expected 10 fresh IDs, got {result}"


def test_part2_us3_identical_ranges():
    """US3 Acceptance Scenario 4: [3-5, 3-5] -> 3 fresh IDs (no double-counting)"""
    from solution import solve_part2

    data = "3-5\n3-5\n\n"
    result = solve_part2(data)
    assert result == 3, f"Expected 3 fresh IDs, got {result}"


# =============================================================================
# EDGE CASES
# =============================================================================


def test_edge_case_very_large_ids():
    """Edge case: Very large ID values (1000000-1000010)"""
    from solution import solve_part2

    data = "1000000-1000010\n\n"
    result = solve_part2(data)
    assert result == 11, f"Expected 11 fresh IDs, got {result}"


def test_edge_case_empty_ranges():
    """Edge case: Empty ranges list"""
    from solution import solve_part2

    data = "\n\n"
    result = solve_part2(data)
    assert result == 0, f"Expected 0 fresh IDs for empty ranges, got {result}"


def test_edge_case_single_large_range():
    """Edge case: Single large range covering many IDs"""
    from solution import solve_part2

    data = "1-10000\n\n"
    result = solve_part2(data)
    assert result == 10000, f"Expected 10000 fresh IDs, got {result}"


def test_edge_case_many_overlapping_ranges():
    """Edge case: Many overlapping ranges"""
    from solution import solve_part2

    # All ranges [1-5] overlapping
    ranges_str = "\n".join(["1-5"] * 100)
    data = ranges_str + "\n\n"
    result = solve_part2(data)
    assert result == 5, f"Expected 5 fresh IDs (no double-count), got {result}"
