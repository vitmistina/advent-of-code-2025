"""Advent of Code 2025 - Day 10 Solution."""

from pathlib import Path
import re
from typing import List, Tuple, Dict, Optional
from collections import Counter


Machine = Dict[str, object]
VERBOSE = False  # Set to True to enable verbose output


def parse_line(line: str) -> Machine:
    """Parse a single machine configuration line into structured components.

    Returns a dict with keys:
    - lights: List[int] target state (0 for '.', 1 for '#')
    - buttons: List[List[int]] list of button toggle indices
    - jolts: List[int] joltage values (ignored for Part 1)
    """
    # Extract the bracketed lights, parenthesized buttons, and curly jolts
    lights_match = re.search(r"\[([.#]+)\]", line)
    if not lights_match:
        raise ValueError("Invalid line: missing lights diagram")
    lights_str = lights_match.group(1)
    lights = [1 if ch == "#" else 0 for ch in lights_str]

    # Find all button groups
    buttons: List[List[int]] = []
    for btn in re.findall(r"\(([^)]*)\)", line):
        btn = btn.strip()
        if not btn:
            buttons.append([])
            continue
        indices = [int(x.strip()) for x in btn.split(",") if x.strip() != ""]
        buttons.append(indices)

    # Extract joltage values inside the last {...} if present
    jolts: List[int] = []
    jolts_match = re.search(r"\{([^}]*)\}", line)
    if jolts_match:
        jolts = [int(x.strip()) for x in jolts_match.group(1).split(",") if x.strip()]

    return {"lights": lights, "buttons": buttons, "jolts": jolts}


def parse_input(input_text: str) -> List[Machine]:
    """Parse the puzzle input into a list of machines."""
    lines = [ln for ln in input_text.splitlines() if ln.strip()]
    machines = [parse_line(ln) for ln in lines]
    # Validate indices within bounds
    for m in machines:
        n = len(m["lights"])  # type: ignore[index]
        for b in m["buttons"]:  # type: ignore[index]
            for idx in b:
                if idx < 0 or idx >= n:
                    raise ValueError(f"Button index {idx} out of range for {n} lights")
    return machines


def solve_part1(data) -> int:
    """Solve Part 1 of the puzzle.

    Expects parsed machines (from parse_input). Placeholder returns 0 until solver implemented.
    """
    # Sum minimal presses across machines
    total = 0
    k_values = []  # Store k = m - rank for each machine
    for idx, m in enumerate(data):
        lights = m["lights"]  # type: ignore[index]
        buttons = m["buttons"]  # type: ignore[index]
        presses, k = _min_presses(buttons, lights)
        if VERBOSE:
            print(f"Machine {idx}: {presses} presses")
        total += presses
        if k is not None:
            k_values.append(k)

    if VERBOSE and k_values:
        _print_k_histogram(k_values)

    return total


def _min_presses(buttons: List[List[int]], target: List[int]) -> Tuple[int, Optional[int]]:
    """Compute minimal button presses to reach target from all-off via GF(2).

    Build matrix B (n_lights x m_buttons) where B[i][j] = 1 if button j toggles light i.
    Solve B x = target over GF(2). When k > 0 (free variables exist), enumerate all
    2^k possibilities to find the true minimum.
    Returns (Hamming weight of solution vector x, k value where k = m - rank).
    """
    n = len(target)
    m = len(buttons)
    if n == 0 or m == 0:
        # If no buttons, only solvable when target all-off
        return (0, None) if sum(target) == 0 else (0, None)

    # Build augmented matrix [B | target]
    # Represent rows as lists of ints (0/1)
    rows: List[List[int]] = []
    for i in range(n):
        row = [0] * m
        for j, btn in enumerate(buttons):
            if i in btn:
                row[j] ^= 1
        row.append(target[i])
        rows.append(row)

    # Gaussian elimination over GF(2)
    col = 0
    pivot_rows: List[int] = [-1] * m
    current_row = 0
    for col in range(m):
        if current_row >= n:
            break
        # Find pivot row with 1 in column col
        pivot = None
        for rr in range(current_row, n):
            if rows[rr][col] == 1:
                pivot = rr
                break
        if pivot is None:
            # No pivot in this column, it's a free column
            continue
        # Swap current row with pivot
        if pivot != current_row:
            rows[current_row], rows[pivot] = rows[pivot], rows[current_row]
        # Eliminate below
        for rr in range(current_row + 1, n):
            if rows[rr][col] == 1:
                for c in range(col, m + 1):
                    rows[rr][c] ^= rows[current_row][c]
        pivot_rows[col] = current_row
        current_row += 1

    # Compute rank (number of pivot rows)
    rank = sum(1 for pr in pivot_rows if pr != -1)

    # Collect pivot and free columns
    pivot_cols = [c for c in range(m) if pivot_rows[c] != -1]
    free_cols = [c for c in range(m) if pivot_rows[c] == -1]

    k = m - rank

    if VERBOSE:
        print(f"\nMachine with n={n}, m={m}")
        print(f"  Rank: {rank}")
        print(f"  Pivot columns: {pivot_cols}")
        print(f"  Free columns: {free_cols}")
        print(f"  k (m - rank): {k}")

    # Check for inconsistent system
    for r in range(n):
        if all(rows[r][c] == 0 for c in range(m)) and rows[r][m] == 1:
            # No solution
            return (0, k)

    # If k > 0, enumerate all 2^k possibilities for free variables
    if k > 0:
        min_presses = float("inf")

        # Try all 2^k combinations of free variable values
        for mask in range(1 << k):
            x = [0] * m

            # Set free variables according to mask
            for i, free_col in enumerate(free_cols):
                x[free_col] = (mask >> i) & 1

            # Back substitution for pivot variables
            for c in range(m - 1, -1, -1):
                r = pivot_rows[c]
                if r == -1:
                    # Already set above
                    continue
                # Compute rhs minus known contributions
                s = rows[r][m]
                for c2 in range(c + 1, m):
                    if rows[r][c2] == 1:
                        s ^= x[c2]
                x[c] = s

            # Count presses for this solution
            presses = sum(x)
            min_presses = min(min_presses, presses)

        return (int(min_presses), k)

    # k == 0: unique solution, use back substitution
    x = [0] * m
    for c in range(m - 1, -1, -1):
        r = pivot_rows[c]
        if r == -1:
            continue
        s = rows[r][m]
        for c2 in range(c + 1, m):
            if rows[r][c2] == 1:
                s ^= x[c2]
        x[c] = s

    return (sum(x), k)


def _print_k_histogram(k_values: List[int]) -> None:
    """Print ASCII histogram of k values (k = m - rank) across machines."""
    if not k_values:
        return

    counter = Counter(k_values)
    max_k = max(k_values)
    max_count = max(counter.values())

    print("\n" + "=" * 50)
    print("K-VALUE HISTOGRAM (k = m - rank)")
    print("=" * 50)
    print(f"Total machines: {len(k_values)}")
    print(f"Maximum k: {max_k}")
    print()

    # Determine bar width (scale to fit in terminal)
    max_bar_width = 40
    scale = max_bar_width / max_count if max_count > 0 else 1

    # Print histogram
    for k in sorted(counter.keys()):
        count = counter[k]
        bar_length = int(count * scale)
        bar = "#" * bar_length
        print(f"k={k:3d}: {bar} ({count})")

    print("=" * 50 + "\n")


def apply_button(state: List[int], indices: List[int]) -> List[int]:
    """Toggle lights at given indices and return new state."""
    new = state[:]
    for i in indices:
        new[i] ^= 1
    return new


def apply_sequence(state: List[int], buttons: List[List[int]], counts: List[int]) -> List[int]:
    """Apply each button count times (mod 2) and return final state."""
    cur = state[:]
    for btn, cnt in zip(buttons, counts):
        if cnt % 2 == 1:
            cur = apply_button(cur, btn)
    return cur


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
