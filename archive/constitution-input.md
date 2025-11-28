# Purpose

​To solve Advent of Code challenges in Python, focusing on clean, readable, and efficient code.

# Code Structure

There is a meta runner script at the root level (which downloads task description, input.txt (if not present) and a prompt template to parse current day's task into test_input.txt, possibly with multiple test input files for different parts). It also runs the solution and validates against AoC website. Assume the cookies/session token is stored in a .env file.

​Each day’s challenge should be in its own folder: day-XX/ (e.g., day-01/).
​Each folder contains:
​solution.py — main solution script.
​input.txt — puzzle input.
​test_input.txt — sample input for testing.
test_input_N.txt — (optional) additional sample inputs for different parts. N signifies a numeric ID.
​README.md — (optional) notes or explanations.

# Coding Standards

​Use Python 3.10+ features where appropriate.
​Follow PEP8 style guide.
​Write functions for each part (e.g., solve_part1(input_data)).
​Include docstrings for all functions and modules.
Use ruff.

# Testing

​Include at least one test per part, using pytest or simple assert statements.
​Test files should be named test_solution.py and placed in the same folder as the solution.

# Collaboration

​Use Git for version control.
We will push straight to main
Commit messages should be clear and descriptive. Follow conventional commit style.

# Documentation

​Update the main README.md with:
​Progress tracker (which days are solved).
​Any special notes or learnings.

# Dependencies

​We use uv.
