"""Integration with Specify commands for spec and task generation."""

import subprocess
from pathlib import Path


def generate_spec_and_tasks(day: int, description: str) -> tuple[Path, Path]:
    """
    Generate spec.md and tasks.md for a day using Specify.
    
    Args:
        day: Day number
        description: Puzzle description text
        
    Returns:
        Tuple of (spec_path, tasks_path)
    """
    spec_folder = Path("specs") / f"day-{day:02d}"
    spec_folder.mkdir(parents=True, exist_ok=True)
    
    spec_path = spec_folder / "spec.md"
    tasks_path = spec_folder / "tasks.md"
    
    # Write initial spec from description
    with open(spec_path, "w", encoding="utf-8") as f:
        f.write(f"# Day {day:02d} Specification\n\n")
        f.write(description)
    
    print(f"📝 Spec created at: {spec_path}")
    
    # Call Specify tasks command (skip plan phase per Constitution VIII)
    try:
        result = subprocess.run(
            ["specify", "tasks", str(spec_folder)],
            capture_output=True,
            text=True,
            check=False,
        )
        
        if result.returncode == 0:
            print(f"✅ Tasks generated at: {tasks_path}")
        else:
            print(f"⚠️  Tasks generation had issues: {result.stderr}")
            # Create placeholder tasks file
            with open(tasks_path, "w", encoding="utf-8") as f:
                f.write(f"# Tasks: Day {day:02d}\n\n")
                f.write("## Phase 1: RED (Tests)\n\n")
                f.write("- [ ] Write test for Part 1\n")
                f.write("- [ ] Write test for Part 2\n\n")
                f.write("## Phase 2: GREEN (Implementation)\n\n")
                f.write("- [ ] Implement Part 1 solution\n")
                f.write("- [ ] Implement Part 2 solution\n\n")
                f.write("## Phase 3: REFACTOR\n\n")
                f.write("- [ ] Optimize and clean up code\n")
            print(f"📝 Placeholder tasks created at: {tasks_path}")
            
    except FileNotFoundError:
        print("⚠️  'specify' command not found. Creating placeholder tasks.")
        with open(tasks_path, "w", encoding="utf-8") as f:
            f.write(f"# Tasks: Day {day:02d}\n\n")
            f.write("## Phase 1: RED (Tests)\n\n")
            f.write("- [ ] Write test for Part 1\n")
            f.write("- [ ] Write test for Part 2\n\n")
            f.write("## Phase 2: GREEN (Implementation)\n\n")
            f.write("- [ ] Implement Part 1 solution\n")
            f.write("- [ ] Implement Part 2 solution\n\n")
            f.write("## Phase 3: REFACTOR\n\n")
            f.write("- [ ] Optimize and clean up code\n")
        print(f"📝 Placeholder tasks created at: {tasks_path}")
    
    return spec_path, tasks_path
