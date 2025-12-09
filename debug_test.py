#!/usr/bin/env python3
"""Debug the test input layout"""

input_text = "12 34\n56 78\n*  + \n"

print("Input as string:")
print(repr(input_text))
print()

lines = input_text.strip("\n").split("\n")
print("Lines:")
for i, line in enumerate(lines):
    print(f"Row {i}: {repr(line)}")
    print("       ", end="")
    for j, char in enumerate(line):
        if char == " ":
            print(f"{j:1d}", end="")
        else:
            print(f"{char}", end="")
    print()
    print("       ", "".join(f"{j % 10}" for j in range(len(line))))
