"""Analyze Day 11 input complexity"""

from collections import defaultdict
import sys

devices = defaultdict(list)
edges_total = 0

with open("day-11/input.txt", "r") as f:
    lines = f.readlines()
    for line in lines:
        parts = line.strip().split(": ")
        source = parts[0]
        destinations = parts[1].split()
        devices[source] = destinations
        edges_total += len(destinations)

        for dest in destinations:
            if dest not in devices:
                devices[dest] = []

# Calculate statistics
out_degrees = [len(devices[d]) for d in devices]
max_degree = max(out_degrees)
avg_degree = sum(out_degrees) / len(out_degrees)
multi_output = sum(1 for d in out_degrees if d > 1)
terminals = sum(1 for d in out_degrees if d == 0)
degree_distribution = defaultdict(int)
for d in out_degrees:
    degree_distribution[d] += 1

# Find "you" and "out"
you_outputs = len(devices.get("you", []))
out_inputs = sum(1 for d in devices if "out" in devices[d])

print("=" * 60)
print("DAY 11 INPUT COMPLEXITY ANALYSIS")
print("=" * 60)
print(f"\nGraph Structure:")
print(f"  Input lines:              {len(lines)}")
print(f"  Unique devices:           {len(devices)}")
print(f"  Total edges:              {edges_total}")
print(f"\nNode Degree Statistics:")
print(f"  Max out-degree:           {max_degree}")
print(f"  Avg out-degree:           {avg_degree:.2f}")
print(f"  Devices with 1+ outputs:  {multi_output}")
print(f"  Terminal devices (0):     {terminals}")
print(f"\nDegree Distribution:")
for degree in sorted(degree_distribution.keys()):
    print(f"  Degree {degree}: {degree_distribution[degree]} devices")
print(f"\nKey Nodes:")
print(f"  'you' outputs to:         {you_outputs} device(s): {devices.get('you', [])}")
print(f"  Devices that output to 'out': {out_inputs}")

# Estimate complexity
print(f"\nComplexity Estimation:")
print(f"  Branching factor (avg):   {avg_degree:.1f}")
print(f"  Graph diameter estimate:  ~5-15 hops")
print(f"  Worst-case paths:         ~{int(avg_degree**10)} (b^d for 10-hop)")
print(f"  Expected paths:           Unknown (could be 10-10000+)")
print(f"\nAlgorithm Considerations:")
print(f"  DFS with backtracking:    VIABLE")
print(f"  Visit set for cycles:     REQUIRED (DAG assumption may not hold)")
print(f"  Memoization potential:    LOW (path enumeration is the goal)")
print(f"  Expected runtime:         <1s likely, depends on path count")
