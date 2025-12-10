"""Debug script to trace connection process."""

from pathlib import Path
from solution import *

inp = Path(__file__).parent.joinpath("test_input.txt").read_text()
pts = parse_input(inp)
dists = compute_all_distances(pts)

print("=== INTERPRETATION 1: Count only actual connections ===")
circuits = {}
next_id = 0
connections = 0

for i, (dist, a, b) in enumerate(dists):
    ca = find_circuit(a, circuits)
    cb = find_circuit(b, circuits)

    action = ""
    if ca is None and cb is None:
        circuits[f"c{next_id}"] = {a, b}
        next_id += 1
        connections += 1
        action = f"CREATE c{next_id - 1}"
    elif ca is not None and cb is None:
        circuits[ca].add(b)
        connections += 1
        action = f"ADD to {ca}"
    elif ca is None and cb is not None:
        circuits[cb].add(a)
        connections += 1
        action = f"ADD to {cb}"
    elif ca != cb:
        circuits[ca].update(circuits[cb])
        del circuits[cb]
        connections += 1
        action = f"MERGE"
    else:
        action = f"SKIP"

    if connections <= 12 or i < 15:
        print(f"{i}: ({a},{b}) -> {action} | Connections: {connections}")

    if connections == 10:
        for pid in range(len(pts)):
            if find_circuit(pid, circuits) is None:
                circuits[f"c{next_id}"] = {pid}
                next_id += 1

        sizes = sorted([len(m) for m in circuits.values()], reverse=True)
        print(f"\nAfter 10 CONNECTIONS: {sizes}")
        print(f"Product: {sizes[0] * sizes[1] * sizes[2]}")
        break

print("\n=== INTERPRETATION 2: Count all attempts (including skips) ===")
circuits2 = {}
next_id2 = 0
attempts = 0

for i, (dist, a, b) in enumerate(dists):
    ca = find_circuit(a, circuits2)
    cb = find_circuit(b, circuits2)

    action = ""
    if ca is None and cb is None:
        circuits2[f"c{next_id2}"] = {a, b}
        next_id2 += 1
        action = "CREATE"
    elif ca is not None and cb is None:
        circuits2[ca].add(b)
        action = "ADD"
    elif ca is None and cb is not None:
        circuits2[cb].add(a)
        action = "ADD"
    elif ca != cb:
        circuits2[ca].update(circuits2[cb])
        del circuits2[cb]
        action = "MERGE"
    else:
        action = "SKIP"

    attempts += 1

    if attempts <= 12:
        print(f"{i}: ({a},{b}) -> {action} | Attempts: {attempts}")

    if attempts == 10:
        for pid in range(len(pts)):
            if find_circuit(pid, circuits2) is None:
                circuits2[f"c{next_id2}"] = {pid}
                next_id2 += 1

        sizes2 = sorted([len(m) for m in circuits2.values()], reverse=True)
        print(f"\nAfter 10 ATTEMPTS: {sizes2}")
        print(f"Product: {sizes2[0] * sizes2[1] * sizes2[2]}")
        break
