# Phase 0 Research — AoC Day 10 Part 1

## Unknowns Resolution

- Dependency choice for GF(2) solving: Prefer pure Python Gaussian elimination to avoid external deps (numpy). Rationale: Simplicity, portability, and AoC constraints.
- Button press model: Binary variables per button; pressing twice cancels effect → variables in {0,1} over GF(2).
- Target derivation: Start state is all zeros; target vector is 1 where `#` appears.

## Best Practices

- Parse robustly: Tolerate spaces, variable counts, and trailing joltage braces (ignore contents).
- Validate indices: Ensure wiring indices are within bounds of diagram length.
- Optimize solve: Use Gaussian elimination modulo 2 with pivoting; if multiple solutions, choose minimal L1 norm solution (press count). For AoC inputs, system typically has unique or minimal solution via elimination; if underdetermined, prefer minimal count using greedy back-substitution tie-breaks.

## Patterns

- Represent buttons as rows of a matrix A (m buttons × n lights); represent target as vector b (n × 1).
- Solve A^T x = b over GF(2) or equivalently build A with columns as buttons toggling vectors depending on implementation; ensure dimensions align.

## Decisions

- Decision: Implement pure-Python GF(2) elimination.
- Rationale: No external dependencies; fast enough for 160 lines.
- Alternatives: numpy bit operations; SAT/ILP solver; BFS over state space — rejected for complexity/performance.
