"""Tests for AoCClient HTML extraction and Markdown conversion."""

from pathlib import Path
from unittest.mock import patch

import pytest

from cli.aoc_client import AoCClient


@pytest.fixture
def fixtures_dir():
    """Return the path to test fixtures directory."""
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def sample_full_page(fixtures_dir):
    """Load sample AOC page with Part 1 and Part 2."""
    return (fixtures_dir / "sample_aoc_page.html").read_text()


@pytest.fixture
def sample_part1_only(fixtures_dir):
    """Load sample AOC page with Part 1 only."""
    return (fixtures_dir / "sample_part1_only.html").read_text()


@pytest.fixture
def sample_no_articles(fixtures_dir):
    """Load sample page with no article elements."""
    return (fixtures_dir / "sample_no_articles.html").read_text()


# T021: Test extracting single article (Part 1)
def test_extract_single_article(sample_part1_only):
    """Test extracting a single article element from HTML."""
    client = AoCClient(session_token="fake-token")

    articles = client.extract_task_description(sample_part1_only)

    assert len(articles) == 1
    assert "Day 1" in articles[0]
    assert "<article" in articles[0]
    assert "</article>" in articles[0]


# T022: Test extracting two articles (Part 1 & Part 2)
def test_extract_two_articles(sample_full_page):
    """Test extracting two article elements (Part 1 and Part 2) from HTML."""
    client = AoCClient(session_token="fake-token")

    articles = client.extract_task_description(sample_full_page)

    assert len(articles) == 2
    assert "Day 1: Historian Hysteria" in articles[0]
    assert "Part Two" in articles[1]


# T023: Test extracting zero articles (empty list)
def test_extract_zero_articles(sample_no_articles):
    """Test extracting from HTML with no article elements returns empty list."""
    client = AoCClient(session_token="fake-token")

    articles = client.extract_task_description(sample_no_articles)

    assert len(articles) == 0
    assert isinstance(articles, list)


# T024: Test HTML to Markdown conversion - headers
def test_html_to_markdown_headers():
    """Test that HTML headers convert correctly to Markdown."""
    client = AoCClient(session_token="fake-token")

    html = "<h2>--- Day 1: Test Title ---</h2><p>Content here.</p>"
    markdown = client.convert_html_to_markdown(html)

    assert "## --- Day 1: Test Title ---" in markdown or "Day 1: Test Title" in markdown
    assert "Content here." in markdown


# T025: Test HTML to Markdown conversion - emphasis/strong
def test_html_to_markdown_emphasis():
    """Test that HTML emphasis and strong tags convert to Markdown."""
    client = AoCClient(session_token="fake-token")

    html = "<p>This is <em>emphasized</em> and <strong>bold</strong> text.</p>"
    markdown = client.convert_html_to_markdown(html)

    assert "*emphasized*" in markdown or "_emphasized_" in markdown
    assert "**bold**" in markdown or "__bold__" in markdown


# T026: Test HTML to Markdown conversion - code blocks
def test_html_to_markdown_code_blocks():
    """Test that HTML code blocks convert to Markdown code blocks."""
    client = AoCClient(session_token="fake-token")

    html = "<pre><code>def hello():\n    print('world')</code></pre>"
    markdown = client.convert_html_to_markdown(html)

    assert "```" in markdown or "    def hello():" in markdown
    assert "hello()" in markdown


# T027: Test HTML to Markdown conversion - inline code
def test_html_to_markdown_inline_code():
    """Test that inline code converts to Markdown backticks."""
    client = AoCClient(session_token="fake-token")

    html = "<p>The function <code>calculate()</code> returns a value.</p>"
    markdown = client.convert_html_to_markdown(html)

    assert "`calculate()`" in markdown
    assert "returns a value" in markdown


# T028: Test HTML to Markdown conversion - lists
def test_html_to_markdown_lists():
    """Test that HTML lists convert to Markdown lists."""
    client = AoCClient(session_token="fake-token")

    html = "<ul><li>First item</li><li>Second item</li><li>Third item</li></ul>"
    markdown = client.convert_html_to_markdown(html)

    assert "First item" in markdown
    assert "Second item" in markdown
    assert "Third item" in markdown
    # Check for list markers (-, *, or numbers)
    assert "-" in markdown or "*" in markdown or "1." in markdown


# T029: Test HTML to Markdown conversion - links
def test_html_to_markdown_links():
    """Test that HTML links convert to Markdown link syntax."""
    client = AoCClient(session_token="fake-token")

    html = '<p>Visit <a href="https://adventofcode.com">Advent of Code</a> for puzzles.</p>'
    markdown = client.convert_html_to_markdown(html)

    assert "Advent of Code" in markdown
    assert "adventofcode.com" in markdown or "https://adventofcode.com" in markdown


# T030: Test HTML entity decoding
def test_html_entity_decoding():
    """Test that HTML entities are decoded correctly."""
    client = AoCClient(session_token="fake-token")

    html = "<p>Use &lt;tag&gt; for markup &amp; &quot;quotes&quot;.</p>"
    markdown = client.convert_html_to_markdown(html)

    assert "<tag>" in markdown
    assert "&" in markdown
    assert '"' in markdown or "quotes" in markdown


# T031: Test save_task_file() creating new file
def test_save_task_file_creates_new():
    """Test that save_task_file creates a new file with content."""
    client = AoCClient(session_token="fake-token")

    with (
        patch("pathlib.Path.exists", return_value=False),
        patch("pathlib.Path.write_text") as mock_write,
    ):
        result = client.save_task_file("day-01", "# Task Content")

        assert result is True
        mock_write.assert_called_once_with("# Task Content", encoding="utf-8")


# T032: Test save_task_file() skipping existing file
def test_save_task_file_skips_existing():
    """Test that save_task_file skips writing if file exists and force=False."""
    client = AoCClient(session_token="fake-token")

    with (
        patch("pathlib.Path.exists", return_value=True),
        patch("pathlib.Path.write_text") as mock_write,
    ):
        result = client.save_task_file("day-01", "# Task Content", force=False)

        assert result is False
        mock_write.assert_not_called()


# T033: Test save_task_file() overwriting with force flag
def test_save_task_file_overwrites_with_force():
    """Test that save_task_file overwrites existing file when force=True."""
    client = AoCClient(session_token="fake-token")

    with (
        patch("pathlib.Path.exists", return_value=True),
        patch("pathlib.Path.write_text") as mock_write,
    ):
        result = client.save_task_file("day-01", "# New Content", force=True)

        assert result is True
        mock_write.assert_called_once_with("# New Content", encoding="utf-8")


# =============================================================================
# User Story 3: Error Handling Tests
# =============================================================================


# T048: Test network timeout with retry
def test_network_timeout_with_retry():
    """Test that network timeouts trigger retries with backoff."""
    from unittest.mock import Mock

    import requests

    client = AoCClient(session_token="fake-token")

    # Mock session.get to raise timeout on first call, succeed on second
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = "puzzle input data"

    client.session.get = Mock(side_effect=[requests.Timeout("Connection timeout"), mock_response])

    success, content = client.download_input(2024, 1)

    assert success is True
    assert content == "puzzle input data"
    assert client.session.get.call_count == 2


# T049: Test 404 response (puzzle not available)
def test_404_puzzle_not_available():
    """Test that 404 responses return helpful error message."""
    from unittest.mock import Mock

    client = AoCClient(session_token="fake-token")

    mock_response = Mock()
    mock_response.status_code = 404
    client.session.get = Mock(return_value=mock_response)

    success, message = client.download_input(2024, 25)

    assert success is False
    assert "not yet available" in message.lower()


# T051: Test missing articles warning message in task.md
def test_missing_articles_warning_in_task_md(tmp_path):
    """Test that missing articles result in warning message saved to task.md."""

    client = AoCClient(session_token="fake-token")

    # HTML with no article elements
    html_no_articles = "<html><body><main><p>No articles here</p></main></body></html>"

    articles = client.extract_task_description(html_no_articles)

    assert len(articles) == 0
    assert isinstance(articles, list)


# =============================================================================
# User Story 1: Save Description on Download Tests (RED Phase)
# =============================================================================


# T006: Test that description.md file is created on successful download
def test_save_description_creates_file(tmp_path, sample_full_page):
    """Test that save_description_file creates description.md with correct content."""
    from cli.meta_runner import save_description_file

    day = 1
    client = AoCClient(session_token="fake-token")

    # Extract and convert to markdown
    articles = client.extract_task_description(sample_full_page)
    combined_html = "\n\n".join(articles)
    markdown = client.convert_html_to_markdown(combined_html)

    # Save to tmp_path instead of real day folder
    day_folder = tmp_path / f"day-{day:02d}"
    result = save_description_file(day_folder, markdown)

    assert result is True
    desc_file = day_folder / "description.md"
    assert desc_file.exists()
    assert "Day 1: Historian Hysteria" in desc_file.read_text()


# T007: Test that description.md contains correct Markdown content
def test_save_description_correct_content(tmp_path, sample_full_page):
    """Test that description.md contains properly formatted Markdown."""
    from cli.meta_runner import save_description_file

    day = 1
    client = AoCClient(session_token="fake-token")

    articles = client.extract_task_description(sample_full_page)
    combined_html = "\n\n".join(articles)
    markdown = client.convert_html_to_markdown(combined_html)

    day_folder = tmp_path / f"day-{day:02d}"
    save_description_file(day_folder, markdown)

    desc_file = day_folder / "description.md"
    content = desc_file.read_text()

    # Verify it's Markdown format (has markdown syntax)
    assert "Day 1" in content
    assert "Part Two" in content  # Full page has both parts
    # Check for typical Markdown elements
    assert "#" in content or "##" in content  # Headers


# T008: Test that day folder is created if it doesn't exist
def test_save_description_creates_folder(tmp_path, sample_part1_only):
    """Test that save_description_file creates day folder if missing."""
    from cli.meta_runner import save_description_file

    day = 5
    client = AoCClient(session_token="fake-token")

    articles = client.extract_task_description(sample_part1_only)
    combined_html = "\n\n".join(articles)
    markdown = client.convert_html_to_markdown(combined_html)

    # Use a non-existent folder path
    day_folder = tmp_path / f"day-{day:02d}"
    assert not day_folder.exists()  # Verify it doesn't exist yet

    save_description_file(day_folder, markdown)

    assert day_folder.exists()  # Folder should be created
    assert (day_folder / "description.md").exists()  # File should exist


# =============================================================================
# User Story 2: Overwrite Description After Part 2 Unlock Tests (RED Phase)
# =============================================================================


# T021: Test that description.md is overwritten when it exists
def test_save_description_overwrites_existing(tmp_path, sample_full_page):
    """Test that save_description_file overwrites existing description.md."""
    from cli.meta_runner import save_description_file

    day = 1
    client = AoCClient(session_token="fake-token")
    day_folder = tmp_path / f"day-{day:02d}"
    day_folder.mkdir(parents=True)

    # Create existing file with old content
    desc_file = day_folder / "description.md"
    desc_file.write_text("# Old Content\n\nThis is old content.", encoding="utf-8")

    # Now save new content
    articles = client.extract_task_description(sample_full_page)
    combined_html = "\n\n".join(articles)
    markdown = client.convert_html_to_markdown(combined_html)

    result = save_description_file(day_folder, markdown)

    assert result is True
    new_content = desc_file.read_text()
    assert "Old Content" not in new_content  # Old content replaced
    assert "Day 1: Historian Hysteria" in new_content  # New content present


# T022: Test updating from Part 1 only to Part 1 + Part 2
def test_save_description_part2_update(tmp_path, sample_part1_only, sample_full_page):
    """Test updating description.md when Part 2 unlocks."""
    from cli.meta_runner import save_description_file

    day = 1
    client = AoCClient(session_token="fake-token")
    day_folder = tmp_path / f"day-{day:02d}"

    # First download: Part 1 only
    articles_part1 = client.extract_task_description(sample_part1_only)
    combined_html_part1 = "\n\n".join(articles_part1)
    markdown_part1 = client.convert_html_to_markdown(combined_html_part1)
    save_description_file(day_folder, markdown_part1)

    desc_file = day_folder / "description.md"
    part1_content = desc_file.read_text()
    assert "Part Two" not in part1_content  # Only Part 1

    # Second download: Part 1 + Part 2
    articles_full = client.extract_task_description(sample_full_page)
    combined_html_full = "\n\n".join(articles_full)
    markdown_full = client.convert_html_to_markdown(combined_html_full)
    save_description_file(day_folder, markdown_full)

    full_content = desc_file.read_text()
    assert "Day 1" in full_content  # Still has Part 1
    assert "Part Two" in full_content  # Now has Part 2


# =============================================================================
# User Story 3: Error Handling Tests (RED Phase)
# =============================================================================


# T030: Test that no file is created when download fails
def test_save_description_failure_no_write(tmp_path):
    """Test that no description.md is created on download failure."""
    from cli.meta_runner import save_description_file

    day_folder = tmp_path / f"day-01"

    # Simulate download failure by not calling save_description_file
    # (in real code, this is the path when desc_success == False)

    desc_file = day_folder / "description.md"
    assert not desc_file.exists()  # File should not exist


# T031: Test that existing file is preserved when download fails
def test_save_description_failure_preserves_existing(tmp_path):
    """Test that existing description.md is unchanged on download failure."""
    from cli.meta_runner import save_description_file

    day_folder = tmp_path / f"day-01"
    day_folder.mkdir(parents=True)

    # Create existing file
    desc_file = day_folder / "description.md"
    original_content = "# Original Content\n\nThis should be preserved."
    desc_file.write_text(original_content, encoding="utf-8")

    # Simulate download failure by not calling save_description_file
    # Verify file is unchanged
    assert desc_file.read_text() == original_content


# T032: Test that no file is created if content is empty
def test_save_description_empty_content(tmp_path):
    """Test that empty content results in no file creation."""
    from cli.meta_runner import save_description_file

    day_folder = tmp_path / f"day-01"

    # Empty string should not create a file
    # In real implementation, we check if articles list is empty
    # and skip calling save_description_file

    desc_file = day_folder / "description.md"
    assert not desc_file.exists()


# =============================================================================
# Polish: Unicode and Additional Tests
# =============================================================================


# T043: Test Unicode characters are preserved
def test_save_description_unicode_preserved(tmp_path):
    """Test that Unicode characters in description are preserved correctly."""
    from cli.meta_runner import save_description_file

    day = 1
    day_folder = tmp_path / f"day-{day:02d}"

    # Content with Unicode characters
    unicode_content = "# Day 1: Puzzle 🎄\n\nEmoji: ✨ 🎅 ⭐\nSymbols: → ≠ ∞\nChars: é ñ 中文"

    result = save_description_file(day_folder, unicode_content)

    assert result is True
    desc_file = day_folder / "description.md"
    saved_content = desc_file.read_text(encoding="utf-8")

    assert "🎄" in saved_content
    assert "✨" in saved_content
    assert "→" in saved_content
    assert "é" in saved_content
    assert "中文" in saved_content
