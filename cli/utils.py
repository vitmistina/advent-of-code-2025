"""Utility functions for CLI and environment handling."""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv


def load_env() -> None:
    """Load environment variables from .env file."""
    load_dotenv()


def get_session_token(interactive: bool = True) -> str | None:
    """
    Get AOC session token from environment or interactive prompt.
    
    Args:
        interactive: If True, prompt user when token is missing
        
    Returns:
        Session token or None if unavailable
    """
    token = os.getenv("AOC_SESSION")
    
    if token:
        return token
    
    if not interactive or not sys.stdin.isatty():
        print("⚠️  AOC_SESSION not found in .env")
        print("📋 Running in dry-run mode. For full functionality:")
        print("   1. Get your session token from adventofcode.com cookies")
        print("   2. Add it to .env file: AOC_SESSION=your_token_here")
        print("   3. Never commit the .env file!")
        return None
    
    # Interactive masked input
    import getpass
    print("\n🔐 AOC_SESSION not found in .env")
    print("You can enter it now (input will be masked) or press Enter to skip.")
    token = getpass.getpass("Paste your session token: ").strip()
    
    if token:
        return token
    
    print("\n⚠️  No token provided. Running in dry-run mode.")
    print("📋 To enable downloads, add AOC_SESSION to your .env file.")
    return None


def get_year() -> int:
    """
    Get AOC year from environment or default to 2025.
    
    Returns:
        Year as integer
    """
    year_str = os.getenv("AOC_YEAR", "2025")
    try:
        return int(year_str)
    except ValueError:
        print(f"⚠️  Invalid AOC_YEAR value: {year_str}, defaulting to 2025")
        return 2025


def validate_day(day: int) -> bool:
    """
    Validate that day is in range 1-25.
    
    Args:
        day: Day number
        
    Returns:
        True if valid, False otherwise
    """
    if 1 <= day <= 25:
        return True
    print(f"❌ Invalid day: {day}. Must be between 1 and 25.")
    return False


def get_day_folder(day: int) -> Path:
    """
    Get the folder path for a given day.
    
    Args:
        day: Day number
        
    Returns:
        Path object for day folder
    """
    return Path(f"day-{day:02d}")


def get_spec_folder(day: int) -> Path:
    """
    Get the spec folder path for a given day.
    
    Args:
        day: Day number
        
    Returns:
        Path object for spec folder
    """
    return Path("specs") / f"day-{day:02d}"


def print_tdd_reminder() -> None:
    """Print friendly TDD workflow reminder."""
    print("\n✅ Scaffolding complete! Follow the TDD flow:")
    print("   🔴 RED:     Run tests (they should fail initially)")
    print("   🟢 GREEN:   Implement minimal solution to pass tests")
    print("   🔵 REFACTOR: Clean up code while keeping tests green")
    print()


def print_submission_guidance(part: int, answer: str) -> None:
    """
    Print manual submission guidance.
    
    Args:
        part: Part number (1 or 2)
        answer: The computed answer
    """
    print(f"\n🎯 Part {part} Answer: {answer}")
    print("\n📋 Manual Submission Required:")
    print("   AoC rules prohibit automated submissions.")
    print("   Please submit manually at: https://adventofcode.com/")
    print()


def never_log_secret(text: str) -> str:
    """
    Scan text for potential AOC_SESSION leaks and mask them.
    
    Args:
        text: Text to scan
        
    Returns:
        Sanitized text with secrets masked
    """
    token = os.getenv("AOC_SESSION")
    if token and token in text:
        return text.replace(token, "***REDACTED***")
    return text


def print_progress_reminder() -> None:
    """Remind user to update progress tracker."""
    print("\n📝 Don't forget to update your progress in README.md!")
    print()
