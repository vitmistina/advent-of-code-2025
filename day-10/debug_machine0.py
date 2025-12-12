"""Debug machine 0 to understand the minimum presses."""

from solution import parse_line, _min_presses, apply_sequence

# Parse machine 0
line = "[#.#.] (2) (1,3) (0,2) (0,1,2) (0) (1,2,3) {27,9,26,9}"
machine = parse_line(line)

target = machine["lights"]
buttons = machine["buttons"]

print("Target:", target)
print("Buttons:")
for i, btn in enumerate(buttons):
    print(f"  Button {i}: {btn}")

# Call the solver
presses, k = _min_presses(buttons, target)
print(f"\nMinimum presses: {presses}")
print(f"k value: {k}")

# Now let's manually try different button combinations
print("\n" + "=" * 60)
print("Manual verification of all possible solutions:")
print("=" * 60)

# Since we have k=2, let's check what the free variables are doing
# Let's try all single button presses and see which ones work
for i, btn in enumerate(buttons):
    state = [0, 0, 0, 0]
    result = apply_sequence(state, [btn], [1])
    print(f"Press button {i} alone: {result} {'✓' if result == target else ''}")

# Try pairs
print("\nTrying pairs:")
for i in range(len(buttons)):
    for j in range(i + 1, len(buttons)):
        state = [0, 0, 0, 0]
        result = apply_sequence(
            state, buttons, [1 if idx in [i, j] else 0 for idx in range(len(buttons))]
        )
        if result == target:
            print(f"Press buttons {i} and {j}: {result} ✓")

# Try triples
print("\nTrying triples:")
for i in range(len(buttons)):
    for j in range(i + 1, len(buttons)):
        for k_idx in range(j + 1, len(buttons)):
            state = [0, 0, 0, 0]
            result = apply_sequence(
                state, buttons, [1 if idx in [i, j, k_idx] else 0 for idx in range(len(buttons))]
            )
            if result == target:
                print(f"Press buttons {i}, {j}, and {k_idx}: {result} ✓")
