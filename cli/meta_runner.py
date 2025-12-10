"""Main CLI entry point for AoC Meta Runner."""

import argparse
import sys
from pathlib import Path

from .aoc_client import AoCClient
from .scaffold import scaffold_day
from .specify_integration import generate_spec_and_tasks
from .utils import (
    get_session_token,
    get_year,
    load_env,
    never_log_secret,
    print_progress_reminder,
    print_tdd_reminder,
    validate_day,
)


def save_description_file(day_folder: Path, markdown_content: str) -> bool:
    """
    Save puzzle description to description.md file.

    Args:
        day_folder: Path to day folder (e.g., Path("day-01"))
        markdown_content: Markdown content to save

    Returns:
        True if file was written successfully, False otherwise
    """
    try:
        # Create folder if it doesn't exist
        day_folder.mkdir(parents=True, exist_ok=True)

        # Write description.md file
        desc_file = day_folder / "description.md"
        desc_file.write_text(markdown_content, encoding="utf-8")

        return True
    except OSError as e:
        print(f"❌ Failed to save description: {e}")
        return False


def cmd_setup(args):
    """Handle setup command (scaffold + download)."""
    day = args.day
    year = args.year or get_year()

    if not validate_day(day):
        return 1

    print(f"\n🚀 Setting up Day {day:02d}...")

    # Scaffold
    created_files = scaffold_day(day, overwrite=args.force)
    if created_files:
        print(f"\n✅ Scaffolded {len(created_files)} files:")
        for filepath in created_files:
            print(f"   - {filepath}")
    else:
        print("\n⚠️  All files already exist. Use --force to overwrite.")

    # Download
    print(f"\n📥 Downloading inputs for {year} Day {day:02d}...")
    token = get_session_token(interactive=not args.dry_run)
    client = AoCClient(token, dry_run=args.dry_run)

    # Download description
    print("\n📄 Downloading puzzle description...")
    desc_success, desc_content = client.download_description(year, day)
    if desc_success:
        articles = client.extract_task_description(desc_content)
        if articles:
            combined_html = "\n\n".join(articles)
            markdown = client.convert_html_to_markdown(combined_html)
            day_folder = Path(f"day-{day:02d}")
            if save_description_file(day_folder, markdown):
                print(f"✅ Description saved to {day_folder / 'description.md'}")
            else:
                print("⚠️  Description download succeeded but file save failed")
        else:
            print("⚠️  Description downloaded but no articles found")
    else:
        print(f"⚠️  Description download failed: {never_log_secret(desc_content)}")

    # Download input
    print("\n📥 Downloading puzzle input...")
    input_success, input_content = client.download_input(year, day)
    if input_success:
        day_folder = Path(f"day-{day:02d}")
        day_folder.mkdir(parents=True, exist_ok=True)
        input_file = day_folder / "input.txt"
        with open(input_file, "w", encoding="utf-8") as f:
            f.write(input_content)
        print(f"✅ Input saved to {input_file}")
    else:
        print(f"⚠️  Input download failed: {never_log_secret(input_content)}")

    print_tdd_reminder()
    print_progress_reminder()
    return 0 if (desc_success or input_success or created_files) else 1


def cmd_download(args):
    """Handle download command."""
    day = args.day
    year = args.year or get_year()

    if not validate_day(day):
        return 1

    print(f"\n📥 Downloading inputs for {year} Day {day:02d}...")

    # Get session token
    token = get_session_token(interactive=not args.dry_run)

    # Create client
    client = AoCClient(token, dry_run=args.dry_run)

    # Download description
    print("\n📄 Downloading puzzle description...")
    desc_success, desc_content = client.download_description(year, day)

    if desc_success:
        # Extract articles from HTML
        articles = client.extract_task_description(desc_content)

        if articles:
            # Join articles and convert to Markdown
            combined_html = "\n\n".join(articles)
            markdown = client.convert_html_to_markdown(combined_html)

            # Save to description.md
            day_folder = Path(f"day-{day:02d}")
            if save_description_file(day_folder, markdown):
                print(f"✅ Description saved to {day_folder / 'description.md'}")
            else:
                print("⚠️  Description download succeeded but file save failed")
        else:
            print("⚠️  Description downloaded but no articles found")
    else:
        print(f"⚠️  Description download failed: {never_log_secret(desc_content)}")

    # Download input
    print("\n📥 Downloading puzzle input...")
    input_success, input_content = client.download_input(year, day)

    if input_success:
        day_folder = Path(f"day-{day:02d}")
        day_folder.mkdir(parents=True, exist_ok=True)
        input_file = day_folder / "input.txt"

        with open(input_file, "w", encoding="utf-8") as f:
            f.write(input_content)

        print(f"✅ Input saved to {input_file}")
    else:
        print(f"⚠️  Input download failed: {never_log_secret(input_content)}")

    return 0 if (desc_success or input_success) else 1


def cmd_specify(args):
    """Handle specify command (generate spec & tasks)."""
    day = args.day

    if not validate_day(day):
        return 1

    print(f"\n📝 Generating spec and tasks for Day {day:02d}...")

    # Read description or create placeholder
    day_folder = Path(f"day-{day:02d}")
    desc_file = day_folder / "description.txt"

    if desc_file.exists():
        description = desc_file.read_text()
    else:
        description = f"# Day {day:02d}\n\nTODO: Add puzzle description"

    spec_path, tasks_path = generate_spec_and_tasks(day, description)

    print("\n✅ Generated:")
    print(f"   - {spec_path}")
    print(f"   - {tasks_path}")
    print("\n📋 Next: Review the spec and tasks, then start TDD!")

    return 0


def cmd_all(args):
    """Handle all-in-one command (scaffold + download + specify)."""
    day = args.day
    # year is accessed via args in cmd_download

    if not validate_day(day):
        return 1

    print(f"\n🎯 Setting up Day {day:02d} (all-in-one)...")

    # Setup (scaffold + download)
    print("\n" + "=" * 50)
    print("STEP 1: Setup (Scaffold + Download)")
    print("=" * 50)
    args.force = False
    result = cmd_setup(args)
    if result != 0:
        return result

    # Download
    print("\n" + "=" * 50)
    print("STEP 2: Downloading")
    print("=" * 50)
    result = cmd_download(args)
    # Continue even if download fails (might be dry-run or rate-limited)

    # Specify
    print("\n" + "=" * 50)
    print("STEP 3: Generating Spec & Tasks")
    print("=" * 50)
    result = cmd_specify(args)

    print("\n" + "=" * 50)
    print("🎉 Day setup complete!")
    print("=" * 50)
    print_tdd_reminder()
    print_progress_reminder()

    return 0


def main():
    """Main CLI entry point."""
    # Load environment
    load_env()

    # Create parser
    parser = argparse.ArgumentParser(
        description="Advent of Code 2025 Meta Runner & CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Scaffold a new day
  uv run -m cli.meta_runner scaffold --day 1

  # Download inputs (with optional year override)
  uv run -m cli.meta_runner download --day 1 --year 2025
  uv run -m cli.meta_runner download --day 1 --dry-run

  # Generate spec and tasks
  uv run -m cli.meta_runner specify --day 1

  # All-in-one: scaffold + download + specify
  uv run -m cli.meta_runner all --day 1

For more info: https://github.com/vitmistina/advent-of-code-2025
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Setup command (merged scaffold + download)
    setup_parser = subparsers.add_parser(
        "setup",
        help="Scaffold day folder and download puzzle input/description",
    )
    setup_parser.add_argument(
        "--day",
        type=int,
        required=True,
        help="Day number (1-25)",
    )
    setup_parser.add_argument(
        "--year",
        type=int,
        help="Year (defaults to AOC_YEAR from .env or 2025)",
    )
    setup_parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing files",
    )
    setup_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be downloaded without making requests",
    )

    # Specify command
    specify_parser = subparsers.add_parser(
        "specify",
        help="Generate spec.md and tasks.md via Specify",
    )
    specify_parser.add_argument(
        "--day",
        type=int,
        required=True,
        help="Day number (1-25)",
    )

    # All command
    all_parser = subparsers.add_parser(
        "all",
        help="Run scaffold + download + specify in sequence",
    )
    all_parser.add_argument(
        "--day",
        type=int,
        required=True,
        help="Day number (1-25)",
    )
    all_parser.add_argument(
        "--year",
        type=int,
        help="Year (defaults to AOC_YEAR from .env or 2025)",
    )
    all_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be downloaded without making requests",
    )

    # Parse arguments
    args = parser.parse_args()

    # Show help if no command
    if not args.command:
        parser.print_help()
        return 0

    # Dispatch command

    commands = {
        "setup": cmd_setup,
        "specify": cmd_specify,
        "all": cmd_all,
    }

    try:
        return commands[args.command](args)
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        return 130
    except Exception as e:
        print(f"\n❌ Error: {never_log_secret(str(e))}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
