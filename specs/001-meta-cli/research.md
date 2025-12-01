# Research: Meta Runner & CLI (AoC 2025)

## Unknowns Resolved

- Decision: Use `requests` with custom exponential backoff (jitter)

  - Rationale: Lightweight, no extra dependency; control over AoC rate limits
  - Alternatives considered: `tenacity` (nice API, extra dep), `urllib3` retry

- Decision: UV for dependency management

  - Rationale: Constitution mandates UV; align with tooling
  - Alternatives considered: pip + venv (non-compliant), poetry (heavier)

- Decision: CLI framework: `argparse` + rich-style prints (no external lib)

  - Rationale: Keep dependencies minimal; fast startup; Windows-friendly
  - Alternatives considered: `typer`/`click` (ergonomic, but adds deps)

- Decision: Specify integration via shell commands

  - Rationale: Constitution uses Specify; call `specify` and `tasks` directly
  - Alternatives considered: Python API (not required), manual templating

- Decision: Year handling via `.env` `AOC_YEAR` with `--year` override

  - Rationale: Matches spec clarifications; default to latest published year
  - Alternatives considered: infer from date (may be before Dec)

- Decision: Interactive masked entry for `AOC_SESSION`
  - Rationale: Security and UX per spec; fallback to dry-run when non-interactive
  - Alternatives considered: prompt unmasked (rejected), error out (unfriendly)

## Best Practices

- Rate limiting: exponential backoff with cap, handle 429/5xx; include jitter
- Security: never print `AOC_SESSION`; store only in `.env`
- Filesystem: idempotent scaffold, safe overwrites with confirmations
- TDD: enforce RED→GREEN→REFACTOR messaging and flow
- Compliance: manual submission guidance; no auto-posting

## Decisions Summary

- Decision: Single Python CLI project with helper modules
  - Rationale: Simple scope; per Constitution II
  - Alternatives: Multi-package layout (overkill)
