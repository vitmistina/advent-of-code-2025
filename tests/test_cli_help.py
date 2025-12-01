"""Tests for CLI help and ergonomics."""

import subprocess


def test_help_output():
    """Test that help output is available and readable."""
    result = subprocess.run(
        ["uv", "run", "-m", "cli.meta_runner", "--help"],
        capture_output=True,
        text=True,
    )
    
    assert result.returncode == 0
    assert "Advent of Code" in result.stdout
    assert "scaffold" in result.stdout
    assert "download" in result.stdout
    assert "specify" in result.stdout


def test_scaffold_help():
    """Test scaffold subcommand help."""
    result = subprocess.run(
        ["uv", "run", "-m", "cli.meta_runner", "scaffold", "--help"],
        capture_output=True,
        text=True,
    )
    
    assert result.returncode == 0
    assert "--day" in result.stdout
    assert "--force" in result.stdout


def test_download_help():
    """Test download subcommand help."""
    result = subprocess.run(
        ["uv", "run", "-m", "cli.meta_runner", "download", "--help"],
        capture_output=True,
        text=True,
    )
    
    assert result.returncode == 0
    assert "--day" in result.stdout
    assert "--year" in result.stdout
    assert "--dry-run" in result.stdout
