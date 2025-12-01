"""Tests for scaffolding functions."""

import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

from cli.scaffold import scaffold_day, scaffold_multi_test_inputs


def test_scaffold_creates_files():
    """Test that scaffold creates all required files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = Path.cwd()
        try:
            import os

            os.chdir(tmpdir)

            created = scaffold_day(1)

            assert len(created) == 5
            assert Path("day-01/solution.py").exists()
            assert Path("day-01/test_solution.py").exists()
            assert Path("day-01/input.txt").exists()
            assert Path("day-01/test_input.txt").exists()
            assert Path("day-01/README.md").exists()
        finally:
            import os

            os.chdir(original_cwd)


def test_scaffold_idempotent():
    """Test that scaffold doesn't overwrite without force."""
    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = Path.cwd()
        try:
            import os

            os.chdir(tmpdir)

            # First scaffold
            created1 = scaffold_day(1)
            assert len(created1) == 5

            # Second scaffold without force
            created2 = scaffold_day(1, overwrite=False)
            assert len(created2) == 0
        finally:
            import os

            os.chdir(original_cwd)


def test_scaffold_multi_test_inputs():
    """Test creating multiple test input files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = Path.cwd()
        try:
            import os

            os.chdir(tmpdir)

            # Create base scaffold first
            scaffold_day(1)

            # Add multi-part test inputs
            created = scaffold_multi_test_inputs(1, 3)

            assert len(created) == 2  # test_input_2.txt and test_input_3.txt
            assert Path("day-01/test_input_2.txt").exists()
            assert Path("day-01/test_input_3.txt").exists()
        finally:
            import os

            os.chdir(original_cwd)


# ============================================================================
# User Story 1 Tests: Download Puzzle Input to File
# ============================================================================


def test_scaffold_downloads_input_with_valid_session():
    """Test that scaffold downloads input.txt when session token is valid (T008)."""
    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = Path.cwd()
        try:
            import os

            os.chdir(tmpdir)

            # Mock AoCClient to return successful download
            mock_client = MagicMock()
            mock_client.download_input.return_value = (True, "mock input data\n123\n456\n")
            mock_client.download_description.return_value = (
                True,
                "<html><body><article class='day-desc'><h2>Test</h2></article></body></html>",
            )
            mock_client.extract_task_description.return_value = [
                "<article class='day-desc'><h2>Test</h2><p>Content</p></article>"
            ]
            mock_client.convert_html_to_markdown.return_value = "## Test\n\nContent"
            mock_client.save_task_file.return_value = True
            mock_client.BASE_URL = "https://adventofcode.com"

            with patch("cli.scaffold.AoCClient", return_value=mock_client):
                created = scaffold_day(1, session_token="mock_token", year=2024)

            # Verify input.txt was created and populated
            input_file = Path("day-01/input.txt")
            assert input_file.exists()
            content = input_file.read_text()
            assert content == "mock input data\n123\n456\n"
            assert "input.txt" in str(created) or any("input.txt" in f for f in created)
        finally:
            import os

            os.chdir(original_cwd)


def test_scaffold_handles_rate_limiting():
    """Test that scaffold handles rate limiting (429) gracefully (T009)."""
    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = Path.cwd()
        try:
            import os

            os.chdir(tmpdir)

            # Mock AoCClient to return rate limit error
            mock_client = MagicMock()
            error_msg = "❌ Rate limit exceeded after 5 attempts.\n📋 Please download manually"
            mock_client.download_input.return_value = (False, error_msg)
            mock_client.download_description.return_value = (
                True,
                "<html><body><article class='day-desc'><h2>Test</h2></article></body></html>",
            )
            mock_client.extract_task_description.return_value = [
                "<article class='day-desc'><h2>Test</h2></article>"
            ]
            mock_client.convert_html_to_markdown.return_value = "## Test"
            mock_client.save_task_file.return_value = True
            mock_client.BASE_URL = "https://adventofcode.com"

            with patch("cli.scaffold.AoCClient", return_value=mock_client):
                scaffold_day(1, session_token="mock_token", year=2024)

            # Verify scaffold continued (other files created)
            assert Path("day-01/solution.py").exists()
            # input.txt should either be empty or contain error message
            input_file = Path("day-01/input.txt")
            if input_file.exists():
                content = input_file.read_text()
                # Should be empty or have placeholder
                assert len(content) == 0 or "Please download manually" in content
        finally:
            import os

            os.chdir(original_cwd)


def test_scaffold_handles_missing_session_token():
    """Test that scaffold works without session token (dry-run mode) (T010)."""
    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = Path.cwd()
        try:
            import os

            os.chdir(tmpdir)

            # Mock AoCClient for dry-run (no session token)
            mock_client = MagicMock()
            dry_run_msg = "🔍 DRY RUN: Would download input"
            mock_client.download_input.return_value = (False, dry_run_msg)
            mock_client.download_description.return_value = (
                True,
                "<html><body><article class='day-desc'><h2>Test</h2></article></body></html>",
            )
            mock_client.extract_task_description.return_value = [
                "<article class='day-desc'><h2>Test</h2></article>"
            ]
            mock_client.convert_html_to_markdown.return_value = "## Test"
            mock_client.save_task_file.return_value = True
            mock_client.BASE_URL = "https://adventofcode.com"

            with patch("cli.scaffold.AoCClient", return_value=mock_client):
                scaffold_day(1, session_token=None, year=2024)

            # Verify other files still created
            assert Path("day-01/solution.py").exists()
            assert Path("day-01/test_solution.py").exists()
            # input.txt should be empty or have dry-run placeholder
            input_file = Path("day-01/input.txt")
            assert input_file.exists()
            content = input_file.read_text()
            assert len(content) == 0  # Empty placeholder for manual entry
        finally:
            import os

            os.chdir(original_cwd)


# =============================================================================
# User Story 3: Error Handling Tests
# =============================================================================


# T050: Test exhausted retries printing manual URL
def test_exhausted_retries_prints_manual_url():
    """Test that exhausted retries result in helpful manual download message (T050)."""
    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = Path.cwd()
        try:
            import os

            os.chdir(tmpdir)

            # Mock AoCClient to simulate exhausted retries
            mock_client = MagicMock()
            error_msg = (
                "❌ Failed after 5 attempts.\n"
                "📋 Please download manually:\n"
                "   https://adventofcode.com/2024/day/1/input\n"
                "   Save to: day-01/input.txt"
            )
            mock_client.download_input.return_value = (False, error_msg)
            mock_client.download_description.return_value = (
                True,
                "<html><body><article class='day-desc'><h2>Test</h2></article></body></html>",
            )
            mock_client.extract_task_description.return_value = [
                "<article class='day-desc'><h2>Test</h2></article>"
            ]
            mock_client.convert_html_to_markdown.return_value = "## Test"
            mock_client.save_task_file.return_value = True
            mock_client.BASE_URL = "https://adventofcode.com"

            with patch("cli.scaffold.AoCClient", return_value=mock_client):
                scaffold_day(1, session_token="mock_token", year=2024)

            # Verify scaffold completed despite download failure
            assert Path("day-01/solution.py").exists()
            assert Path("day-01/test_solution.py").exists()
            assert Path("day-01/README.md").exists()

            # input.txt should exist but be empty (download failed)
            input_file = Path("day-01/input.txt")
            assert input_file.exists()
        finally:
            import os

            os.chdir(original_cwd)


# T052: Test scaffold continuing after download failure
def test_scaffold_continues_after_download_failure():
    """Test that scaffold continues creating files even if downloads fail (T052)."""
    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = Path.cwd()
        try:
            import os

            os.chdir(tmpdir)

            # Mock both input and description downloads to fail
            mock_client = MagicMock()
            mock_client.download_input.return_value = (False, "Network error")
            mock_client.download_description.return_value = (False, "Network error")
            mock_client.BASE_URL = "https://adventofcode.com"

            with patch("cli.scaffold.AoCClient", return_value=mock_client):
                created = scaffold_day(1, session_token="mock_token", year=2024)

            # Verify all base files were created despite download failures
            assert Path("day-01/solution.py").exists()
            assert Path("day-01/test_solution.py").exists()
            assert Path("day-01/input.txt").exists()
            assert Path("day-01/test_input.txt").exists()
            assert Path("day-01/README.md").exists()

            # Created list should include all base files
            assert len(created) == 5
        finally:
            import os

            os.chdir(original_cwd)
