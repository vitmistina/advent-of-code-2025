"""Tests for Advent of Code 2025 - Day 11."""

from pathlib import Path

import pytest

from .solution import (
    build_graph,
    display_paths,
    find_all_paths,
    find_single_path,
    parse_device_config,
    solve_part1,
)

# ============================================================================
# FIXTURES (Phase 2: Foundational)
# ============================================================================


@pytest.fixture
def test_input():
    """Load test input from file (T002)."""
    test_file = Path(__file__).parent / "test_input.txt"
    return test_file.read_text()


@pytest.fixture
def load_config_from_string():
    """Helper to load device configuration from string (T003)."""

    def _load(config_str: str):
        return parse_device_config(config_str)

    return _load


@pytest.fixture
def assert_path_valid():
    """Helper to validate paths (T004)."""

    def _validate(graph, path, start="you", end="out"):
        """Assert that a path is valid in the graph."""
        assert path is not None, "Path should not be None"
        assert isinstance(path, list), "Path should be a list"
        assert len(path) >= 2, "Path should have at least start and end"
        assert path[0] == start, f"Path should start with '{start}'"
        assert path[-1] == end, f"Path should end with '{end}'"

        # Verify each step has a valid connection
        for i in range(len(path) - 1):
            current = path[i]
            next_device = path[i + 1]
            assert next_device in graph.get(current, []), (
                f"No connection from {current} to {next_device}"
            )

        return True

    return _validate


# ============================================================================
# PHASE 3: USER STORY 1 - Parse Device Configuration (T005-T012)
# ============================================================================


class TestParseDeviceConfig:
    """Tests for parse_device_config function."""

    def test_parse_single_connection(self, load_config_from_string):
        """Test parsing single connection: you: bbb (T005)."""
        config = "you: bbb"
        result = load_config_from_string(config)

        assert "you" in result
        assert "bbb" in result
        assert result["you"] == ["bbb"]
        assert result["bbb"] == []

    def test_parse_multiple_connections(self, load_config_from_string):
        """Test parsing multiple connections: bbb: ddd eee (T006)."""
        config = "bbb: ddd eee"
        result = load_config_from_string(config)

        assert "bbb" in result
        assert set(result["bbb"]) == {"ddd", "eee"}
        assert "ddd" in result
        assert "eee" in result

    def test_parse_example_config(self, load_config_from_string):
        """Test parsing complete example configuration (T007)."""
        config = """aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out"""
        result = load_config_from_string(config)

        # Verify all devices are present
        expected_devices = {
            "aaa",
            "you",
            "bbb",
            "ccc",
            "ddd",
            "eee",
            "fff",
            "ggg",
            "hhh",
            "iii",
            "out",
        }
        assert set(result.keys()) == expected_devices

        # Verify specific connections
        assert result["you"] == ["bbb", "ccc"]
        assert set(result["ccc"]) == {"ddd", "eee", "fff"}

    def test_parse_implicit_devices(self, load_config_from_string):
        """Test parsing devices appearing only as destinations (T008)."""
        config = """you: bbb
bbb: out"""
        result = load_config_from_string(config)

        # Verify "out" exists even though it has no outputs specified
        assert "out" in result
        assert result["out"] == []

    def test_parse_duplicate_devices(self, load_config_from_string):
        """Test duplicate device handling in configuration (T009)."""
        config = """you: bbb
bbb: out
you: ccc"""
        # Only test that parsing completes (later rule: last definition wins
        # or we handle it gracefully)
        result = load_config_from_string(config)
        assert "you" in result
        assert "bbb" in result
        assert "out" in result


# ============================================================================
# PHASE 4: USER STORY 2 - Build Complete Device Network Graph (T013-T020)
# ============================================================================


class TestBuildGraph:
    """Tests for build_graph function."""

    def test_graph_all_devices(self, load_config_from_string):
        """Test graph contains all unique devices (T013)."""
        config = "you: bbb\nbbb: out"
        connections = load_config_from_string(config)
        graph = build_graph(connections)

        expected = {"you", "bbb", "out"}
        assert set(graph.keys()) == expected

    def test_graph_connections(self, load_config_from_string):
        """Test graph correctly identifies device outputs (T014)."""
        config = "you: bbb\nbbb: ddd eee\nddd: out"
        connections = load_config_from_string(config)
        graph = build_graph(connections)

        assert graph["you"] == ["bbb"]
        assert set(graph["bbb"]) == {"ddd", "eee"}

    def test_graph_terminal_devices(self, load_config_from_string):
        """Test graph handles devices with no outputs (T015)."""
        config = "you: bbb\nbbb: out"
        connections = load_config_from_string(config)
        graph = build_graph(connections)

        assert "out" in graph
        assert graph["out"] == []

    def test_graph_single_output(self, load_config_from_string):
        """Test graph handles single output devices (T016)."""
        config = "you: bbb\nbbb: out"
        connections = load_config_from_string(config)
        graph = build_graph(connections)

        assert len(graph["you"]) == 1
        assert graph["you"][0] == "bbb"

    def test_graph_multiple_outputs(self, load_config_from_string):
        """Test graph handles multiple output devices (T017)."""
        config = "you: bbb ccc ddd"
        connections = load_config_from_string(config)
        graph = build_graph(connections)

        assert len(graph["you"]) == 3
        assert set(graph["you"]) == {"bbb", "ccc", "ddd"}


# ============================================================================
# PHASE 5: USER STORY 3 - Find Single Path from Source to Target (T021-T027)
# ============================================================================


class TestFindSinglePath:
    """Tests for find_single_path function."""

    def test_find_path_linear(self, load_config_from_string, assert_path_valid):
        """Test finds simple linear path (you → out) (T021)."""
        config = "you: out"
        connections = load_config_from_string(config)
        graph = build_graph(connections)

        path = find_single_path(graph, "you", "out")
        assert_path_valid(graph, path)

    def test_find_path_intermediate(self, load_config_from_string, assert_path_valid):
        """Test finds path through intermediate devices (T022)."""
        config = """you: bbb
bbb: ccc
ccc: out"""
        connections = load_config_from_string(config)
        graph = build_graph(connections)

        path = find_single_path(graph, "you", "out")
        assert_path_valid(graph, path)
        assert len(path) == 4  # you, bbb, ccc, out

    def test_find_path_example(self, load_config_from_string, assert_path_valid):
        """Test finds path from example configuration (T023)."""
        config = """aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out"""
        connections = load_config_from_string(config)
        graph = build_graph(connections)

        path = find_single_path(graph, "you", "out")
        assert_path_valid(graph, path)

    def test_find_path_no_solution(self, load_config_from_string):
        """Test returns None when no path exists (T024)."""
        config = """you: bbb
other: out"""
        connections = load_config_from_string(config)
        graph = build_graph(connections)

        path = find_single_path(graph, "you", "out")
        assert path is None


# ============================================================================
# PHASE 6: USER STORY 4 - Enumerate All Paths with Backtracking (T028-T039)
# ============================================================================


class TestEnumerateAllPaths:
    """Tests for find_all_paths function."""

    def test_enumerate_single_path(self, load_config_from_string):
        """Test enumerates single path when only one exists (T028)."""
        config = "you: out"
        connections = load_config_from_string(config)
        graph = build_graph(connections)

        paths = find_all_paths(graph, "you", "out")
        assert len(paths) == 1
        assert paths[0] == ["you", "out"]

    def test_enumerate_two_paths(self, load_config_from_string):
        """Test enumerates simple two-path branching (T029)."""
        config = """you: bbb ccc
bbb: out
ccc: out"""
        connections = load_config_from_string(config)
        graph = build_graph(connections)

        paths = find_all_paths(graph, "you", "out")
        assert len(paths) == 2

    def test_enumerate_example_paths(self, load_config_from_string):
        """Test enumerates example configuration correctly (5 paths) (T030)."""
        config = """aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out"""
        connections = load_config_from_string(config)
        graph = build_graph(connections)

        paths = find_all_paths(graph, "you", "out")
        assert len(paths) == 5

    def test_enumerate_paths_start_correct(self, load_config_from_string):
        """Test all enumerated paths start with 'you' (T031)."""
        config = """you: bbb ccc
bbb: out
ccc: out"""
        connections = load_config_from_string(config)
        graph = build_graph(connections)

        paths = find_all_paths(graph, "you", "out")
        for path in paths:
            assert path[0] == "you"

    def test_enumerate_paths_end_correct(self, load_config_from_string):
        """Test all enumerated paths end with 'out' (T032)."""
        config = """you: bbb ccc
bbb: out
ccc: out"""
        connections = load_config_from_string(config)
        graph = build_graph(connections)

        paths = find_all_paths(graph, "you", "out")
        for path in paths:
            assert path[-1] == "out"

    def test_enumerate_paths_valid_connections(self, load_config_from_string):
        """Test all enumerated paths follow valid connections (T033)."""
        config = """you: bbb ccc
bbb: ddd
ccc: ddd
ddd: out"""
        connections = load_config_from_string(config)
        graph = build_graph(connections)

        paths = find_all_paths(graph, "you", "out")
        for path in paths:
            for i in range(len(path) - 1):
                assert path[i + 1] in graph[path[i]]

    def test_enumerate_paths_no_duplicates(self, load_config_from_string):
        """Test no duplicate paths in enumeration (T034)."""
        config = """you: bbb ccc
bbb: ddd
ccc: ddd
ddd: out"""
        connections = load_config_from_string(config)
        graph = build_graph(connections)

        paths = find_all_paths(graph, "you", "out")
        paths_as_tuples = [tuple(path) for path in paths]
        assert len(paths_as_tuples) == len(set(paths_as_tuples))

    def test_enumerate_complex_branching(self, load_config_from_string):
        """Test enumerate handles multiple branching and reconvergence (T035)."""
        config = """aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out"""
        connections = load_config_from_string(config)
        graph = build_graph(connections)

        paths = find_all_paths(graph, "you", "out")
        # Should find exactly 5 paths
        assert len(paths) == 5


# ============================================================================
# PHASE 7: USER STORY 5 - Count Total Distinct Paths (T040-T047)
# ============================================================================


class TestCountPaths:
    """Tests for path counting functionality."""

    def test_count_single_path(self, load_config_from_string):
        """Test counts single path correctly (T040)."""
        config = "you: out"
        count = solve_part1(config)
        assert count == 1

    def test_count_multiple_paths(self, load_config_from_string):
        """Test counts multiple paths correctly (T041)."""
        config = """you: bbb ccc
bbb: out
ccc: out"""
        count = solve_part1(config)
        assert count == 2

    def test_count_example_paths(self, load_config_from_string):
        """Test counts example configuration as 5 (T042)."""
        config = """aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out"""
        count = solve_part1(config)
        assert count == 5

    def test_count_no_solution(self, load_config_from_string):
        """Test counts 0 when no path exists (T043)."""
        config = """you: bbb
other: out"""
        count = solve_part1(config)
        assert count == 0

    def test_count_matches_enumeration(self, load_config_from_string):
        """Test count matches enumeration length (T044)."""
        config = """you: bbb ccc
bbb: ddd
ccc: ddd
ddd: eee fff
eee: out
fff: out"""
        connections = load_config_from_string(config)
        graph = build_graph(connections)
        paths = find_all_paths(graph, "you", "out")
        count = solve_part1(config)
        assert count == len(paths)


# ============================================================================
# PHASE 8: USER STORY 6 - Display Enumerated Paths for Verification (T048-T053)
# ============================================================================


class TestDisplayPaths:
    """Tests for display_paths function."""

    def test_display_path_format(self, load_config_from_string):
        """Test path display format is correct (T048)."""
        config = "you: out"
        connections = load_config_from_string(config)
        graph = build_graph(connections)
        paths = find_all_paths(graph, "you", "out")
        displayed = display_paths(paths)

        assert len(displayed) == 1
        assert displayed[0] == "you → out"

    def test_display_all_example_paths(self, load_config_from_string):
        """Test all paths displayed for example configuration (T049)."""
        config = """aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out"""
        connections = load_config_from_string(config)
        graph = build_graph(connections)
        paths = find_all_paths(graph, "you", "out")
        displayed = display_paths(paths)

        assert len(displayed) == 5
        for path_str in displayed:
            assert " → " in path_str
            assert path_str.startswith("you")
            assert path_str.endswith("out")

    def test_display_valid_paths(self, load_config_from_string):
        """Test displayed paths contain only valid connections (T050)."""
        config = """you: bbb ccc
bbb: out
ccc: out"""
        connections = load_config_from_string(config)
        graph = build_graph(connections)
        paths = find_all_paths(graph, "you", "out")
        displayed = display_paths(paths)

        # Each displayed path should have valid connections
        for path_str in displayed:
            devices = path_str.split(" → ")
            for i in range(len(devices) - 1):
                assert devices[i + 1] in graph[devices[i]]


# ============================================================================
# PHASE 9: USER STORY 7 - Handle Device Network with No Solution (T054-T061)
# ============================================================================


class TestNoSolution:
    """Tests for handling no-solution edge cases."""

    def test_no_solution_you_no_outputs(self):
        """Test no solution when 'you' has no outputs (T054)."""
        config = """you: 
out: """
        count = solve_part1(config)
        assert count == 0

    def test_no_solution_dead_end(self):
        """Test no solution when path leads to dead-end (T055)."""
        config = """you: bbb
bbb: ccc
ccc: 
out: """
        count = solve_part1(config)
        assert count == 0

    def test_no_solution_unreachable_out(self):
        """Test no solution when 'out' unreachable (T056)."""
        config = """you: bbb
bbb: ccc
ccc: bbb
ddd: out"""
        count = solve_part1(config)
        assert count == 0

    def test_no_solution_disconnected(self):
        """Test graceful handling of disconnected components (T057)."""
        config = """you: aaa
aaa: bbb
bbb: ccc
out: xxx
xxx: yyy"""
        count = solve_part1(config)
        assert count == 0


# ============================================================================
# PHASE 10: POLISH & INTEGRATION TESTS (T062-T068)
# ============================================================================


class TestIntegration:
    """Integration tests with real input."""

    def test_real_input_integration(self, test_input):
        """Integration test with actual puzzle input (T062)."""
        count = solve_part1(test_input)
        # Expected: 5 paths from example input
        assert count == 5

    def test_performance(self, test_input):
        """Performance validation: verify solution runs quickly (T063)."""
        import time

        start = time.time()
        count = solve_part1(test_input)
        elapsed = time.time() - start

        # Should complete in under 1 second
        assert elapsed < 1.0
        assert count == 5

    def test_example_returns_five_paths(self, test_input):
        """Final manual verification: Example input returns exactly 5 paths (T067)."""
        count = solve_part1(test_input)
        assert count == 5
