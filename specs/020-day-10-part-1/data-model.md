# Data Model — AoC Day 10 Part 1

## Entities

- Machine

  - lights_count: int
  - target: list[bool]
  - buttons: list[Button]

- Button
  - toggles: list[int] # indices of lights toggled

## Derived Structures

- ToggleMatrix (GF(2))

  - shape: (buttons_count, lights_count)
  - rows: one per button, 1 where button toggles that light

- TargetVector (GF(2))
  - length: lights_count
  - entries: 1 for `#`, 0 for `.`
