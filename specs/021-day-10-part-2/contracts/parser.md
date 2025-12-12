# Contract: Input Parser

**Phase**: Phase 1 (Design & Contracts)  
**Component**: Input parsing  
**Spec Reference**: [spec.md](../spec.md)  
**Data Model Reference**: [data-model.md](../data-model.md)

---

## Function Signature

```python
def parse_input(text: str) -> PuzzleInput:
    """
    Parse problem input text into PuzzleInput data structure.
    
    Args:
        text (str): Raw input text from Advent of Code puzzle
        
    Returns:
        PuzzleInput: Fully validated puzzle with machines, buttons, and counters
        
    Raises:
        ValueError: If input format is invalid
        IndexError: If line structure doesn't match expected format
    """
```

---

## Input Format Specification

### Format Grammar

```
INPUT := LINE+ EOF
LINE := LIGHTS SPACES BUTTONS+ SPACES TARGETS
LIGHTS := '[' ([.#]+) ']'
BUTTONS := '(' (DIGIT (',' DIGIT)*)? ')'
TARGETS := '{' (DIGIT (',' DIGIT)*) '}'
DIGIT := [0-9]+
SPACES := (' ')+
```

### Example Input Lines

```
[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
```

### Parsing Rules

1. **Indicator Lights `[...]`** (IGNORED in Part 2)
   - Format: Square brackets containing `.` and `#` characters
   - Purpose: Defines machine structure (ignored; only counters matter)
   - Extraction: Skip entirely; not used

2. **Buttons `(...)` (REQUIRED)**
   - Format: Parentheses containing comma-separated integers
   - Meaning: Each button definition lists counter indices it affects
   - Example: `(1,3)` = button affects counters 1 and 3
   - Rules:
     - Can have 0 to N indices (where N = number of counters)
     - Indices must be non-negative integers
     - Order within button: must be sorted ascending
     - Duplicates within button: not allowed (but spec examples may have them - sanitize)
   - Extraction: Create Button objects with sequential IDs (0, 1, 2, ...)

3. **Targets `{...}` (REQUIRED)**
   - Format: Curly braces containing comma-separated integers
   - Meaning: Target values for each counter (in order)
   - Example: `{3,5,4,7}` = counter 0→3, counter 1→5, counter 2→4, counter 3→7
   - Rules:
     - Must have at least one target
     - All targets must be non-negative integers
     - Number of targets = number of counters in machine
   - Extraction: Create Counter objects with targets

### Detailed Parsing Steps

```python
def parse_line(line: str, machine_id: int) -> Machine:
    """Parse single machine definition line."""
    
    # Step 1: Extract sections using regex or string splitting
    import re
    
    # Pattern: LIGHTS BUTTONS+ TARGETS
    pattern = r'\[([.#]+)\]\s+((?:\([^)]*\)\s*)+)\s*\{([^}]+)\}'
    match = re.match(pattern, line.strip())
    
    if not match:
        raise ValueError(f"Invalid line format: {line}")
    
    lights_str, buttons_str, targets_str = match.groups()
    
    # Step 2: Parse indicator lights (IGNORED but extract for validation)
    lights = list(lights_str)  # ['.',  '#', '#', '.']
    num_lights = len(lights)
    
    # Step 3: Parse buttons
    button_patterns = re.findall(r'\(([^)]*)\)', buttons_str)
    buttons = []
    
    for button_id, button_str in enumerate(button_patterns):
        if button_str.strip() == '':
            # Empty parentheses: button affects no counters (SKIP or validate)
            affected = []
        else:
            # Parse comma-separated indices
            affected = []
            for idx_str in button_str.split(','):
                idx = int(idx_str.strip())
                affected.append(idx)
        
        # Validation: Remove duplicates and sort
        affected = sorted(set(affected))
        
        # Only create button if it affects at least one counter
        if affected:
            button = Button(button_id, affected)
            buttons.append(button)
    
    # Step 4: Parse targets
    target_strs = targets_str.split(',')
    counters = []
    
    for counter_id, target_str in enumerate(target_strs):
        target = int(target_str.strip())
        counter = Counter(counter_id, target)
        counters.append(counter)
    
    # Step 5: Validate button counter indices are within range
    num_counters = len(counters)
    for button in buttons:
        for idx in button.affected_counter_indices:
            if idx >= num_counters:
                raise ValueError(
                    f"Button {button.button_id} references counter {idx}, "
                    f"but machine only has {num_counters} counters"
                )
    
    # Step 6: Create Machine
    machine = Machine(machine_id, buttons, counters)
    return machine
```

---

## Error Handling

### Invalid Input Errors

| Error | Example | Handling |
|-------|---------|----------|
| **Missing section** | `[.##.] (0) (1)` (no targets) | Raise `ValueError` with clear message |
| **Invalid format** | `[.##.] 0 1 2 {3,4,5}` (no parens) | Raise `ValueError: Expected parentheses` |
| **Malformed parens** | `[.##.] (0 (1) {3,4}` (mismatched) | Raise `ValueError: Malformed button definition` |
| **Non-integer** | `[.##.] (a,b) {3,4}` (letters) | Raise `ValueError: Invalid counter index` |
| **Out of range** | `[.##.] (5) {3,4}` (5 ≥ 2 counters) | Raise `ValueError: Counter index out of range` |
| **Empty targets** | `[.##.] (0,1) {}` (no targets) | Raise `ValueError: Machine must have at least one counter` |
| **Empty buttons** | `[.##.] {3,4,5}` (no buttons) | Raise `ValueError: Machine must have at least one button` |

---

## Test Vectors

### Test 1: Parse First Example

**Input**:
```
[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
```

**Expected Output**:
```python
Machine(
    machine_id=0,
    buttons=[
        Button(0, [3]),
        Button(1, [1, 3]),
        Button(2, [2]),
        Button(3, [2, 3]),  # Might be [2, 3] or [3, 2] depending on input
        Button(4, [0, 2]),
        Button(5, [0, 1])
    ],
    counters=[
        Counter(0, 3),
        Counter(1, 5),
        Counter(2, 4),
        Counter(3, 7)
    ]
)
```

**Verification**: Machine has 6 buttons, 4 counters, all counter indices valid

### Test 2: Parse Second Example

**Input**:
```
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
```

**Expected Output**:
```python
Machine(
    machine_id=1,
    buttons=[
        Button(0, [0, 2, 3, 4]),
        Button(1, [2, 3]),
        Button(2, [0, 4]),
        Button(3, [0, 1, 2]),
        Button(4, [1, 2, 3, 4])
    ],
    counters=[
        Counter(0, 7),
        Counter(1, 5),
        Counter(2, 12),
        Counter(3, 7),
        Counter(4, 2)
    ]
)
```

**Verification**: Machine has 5 buttons, 5 counters

### Test 3: Parse Multi-Machine Input

**Input**:
```
[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
```

**Expected Output**:
```python
PuzzleInput(
    machines=[
        Machine(0, ...),  # First machine
        Machine(1, ...),  # Second machine
        Machine(2, ...),  # Third machine
    ]
)
```

**Verification**: `puzzle.num_machines == 3`

---

## Edge Cases

### Edge Case 1: Button with No Affected Counters

**Input**: `[.#] () {5}`

**Behavior**: 
- Option A: Skip this button (create Machine without it)
- Option B: Raise error (button must affect something)
- **Choice**: Option A - skip silently (may make machine unsolvable, but OK)

### Edge Case 2: Counter with Target Zero

**Input**: `[.#] (0) {0}`

**Behavior**: Create Counter with target=0; no presses needed for this counter

**Expected**: Should work fine (already at target)

### Edge Case 3: Duplicate Button Definitions

**Input**: `[.##] (0) (0) {3,4}`

**Behavior**: Create two separate buttons, both affecting counter 0
- Button 0 affects [0]
- Button 1 affects [0]
- Either can be pressed to increment counter 0

**Expected**: Machine is valid; solver can choose either button

### Edge Case 4: Very Large Target

**Input**: `[.#] (0) {999999}`

**Behavior**: Create Counter with target=999999; solver must handle large numbers

**Expected**: Should work (depends on algorithm performance)

---

## Implementation Notes

### Regex Pattern

Suggested robust regex:
```python
# Matches: [lights] buttons... {targets}
pattern = r'\[([.#]+)\]\s+((?:\([^)]*\)\s*)+)\{([^}]+)\}'

# Extract individual buttons from buttons section
button_pattern = r'\(([^)]*)\)'

# Extract targets
# Already have targets_str from main pattern
```

### Sanitization

```python
def sanitize_indices(indices: list[int]) -> list[int]:
    """Remove duplicates, sort, validate."""
    indices = [int(x) for x in indices]
    indices = sorted(set(indices))
    for idx in indices:
        if idx < 0:
            raise ValueError(f"Negative index not allowed: {idx}")
    return indices
```

### Full Implementation Template

```python
import re
from typing import List

def parse_input(text: str) -> PuzzleInput:
    """Parse full input (multiple lines)."""
    machines = []
    for line_num, line in enumerate(text.strip().split('\n')):
        if line.strip():  # Skip empty lines
            machine = parse_line(line, line_num)
            machines.append(machine)
    
    return PuzzleInput(machines, metadata={'source': 'aoc_2025_day_10'})

def parse_line(line: str, machine_id: int) -> Machine:
    """Parse single line into Machine."""
    pattern = r'\[([.#]+)\]\s+((?:\([^)]*\)\s*)+)\s*\{([^}]+)\}'
    match = re.match(pattern, line.strip())
    
    if not match:
        raise ValueError(f"Invalid line format (line {machine_id}): {line}")
    
    lights_str, buttons_str, targets_str = match.groups()
    
    # Parse buttons
    button_strs = re.findall(r'\(([^)]*)\)', buttons_str)
    buttons = []
    
    for btn_id, btn_str in enumerate(button_strs):
        if btn_str.strip():
            indices = [int(x.strip()) for x in btn_str.split(',')]
            indices = sorted(set(indices))  # Deduplicate and sort
            if indices:  # Only add if affects at least one counter
                buttons.append(Button(btn_id, indices))
    
    if not buttons:
        raise ValueError(f"Machine must have at least one button (line {machine_id})")
    
    # Parse targets
    targets = [int(x.strip()) for x in targets_str.split(',')]
    
    if not targets:
        raise ValueError(f"Machine must have at least one target (line {machine_id})")
    
    counters = [Counter(i, targets[i]) for i in range(len(targets))]
    
    # Validate button indices
    for button in buttons:
        for idx in button.affected_counter_indices:
            if idx >= len(counters):
                raise ValueError(
                    f"Button {button.button_id} references counter {idx}, "
                    f"but machine only has {len(counters)} counters (line {machine_id})"
                )
    
    return Machine(machine_id, buttons, counters)
```

---

## Next Steps (Phase 2)

1. **Solver Contract**: Define `solve_machine()` and `solve_all()` interfaces
2. **Implementation**: Code parser against these specs
3. **Tests**: Write unit tests for each edge case above
4. **Integration**: Connect parser to solver and output
