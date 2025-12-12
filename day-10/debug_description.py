"""Debug the example from the description."""

from solution import parse_line, _min_presses, apply_sequence

# Parse the DESCRIPTION example machine 1
line = "[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}"
machine = parse_line(line)

target = machine["lights"]
buttons = machine["buttons"]

print("DESCRIPTION EXAMPLE - Machine 1")
print("Target:", target)
print("Buttons:")
for i, btn in enumerate(buttons):
    print(f"  Button {i}: {btn}")

# Call the solver
presses, k = _min_presses(buttons, target)
print(f"\nMinimum presses: {presses}")
print(f"Expected: 2")
print(f"Match: {'✓' if presses == 2 else '✗'}")

# Try the solution mentioned: press (0,2) and (0,1)
# These are buttons 4 and 5 in 0-indexed
state = [0, 0, 0, 0]
result = apply_sequence(state, buttons, [0, 0, 0, 0, 1, 1])
print(f"\nPress buttons 4:(0,2) and 5:(0,1): {result}")
print(f"Target: {target}")
print(f"Match: {'✓' if result == target else '✗'}")
