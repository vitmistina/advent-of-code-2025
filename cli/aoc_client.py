"""HTTP client for Advent of Code with rate limiting and backoff."""

import random
import time
from pathlib import Path

import html2text
import requests
from bs4 import BeautifulSoup


class AoCClient:
    """Client for downloading puzzle data from Advent of Code."""

    BASE_URL = "https://adventofcode.com"
    MAX_RETRIES = 5
    BASE_BACKOFF = 1.0  # seconds
    MAX_BACKOFF = 60.0  # seconds

    def __init__(self, session_token: str | None, dry_run: bool = False):
        """
        Initialize AoC client.

        Args:
            session_token: Session cookie value for authentication
            dry_run: If True, don't make actual requests
        """
        self.session_token = session_token
        self.dry_run = dry_run
        self.session = requests.Session()
        if session_token:
            self.session.cookies.set("session", session_token)

    def _backoff_with_jitter(self, attempt: int) -> float:
        """
        Calculate backoff time with exponential backoff and jitter.

        Args:
            attempt: Current attempt number (0-indexed)

        Returns:
            Sleep time in seconds
        """
        backoff = min(self.BASE_BACKOFF * (2**attempt), self.MAX_BACKOFF)
        jitter = random.uniform(0, backoff * 0.1)  # 10% jitter
        return backoff + jitter

    def download_input(self, year: int, day: int) -> tuple[bool, str]:
        """
        Download puzzle input for a given day.

        Args:
            year: Year of the puzzle
            day: Day number (1-25)

        Returns:
            Tuple of (success, content_or_error_message)
        """
        if self.dry_run or not self.session_token:
            msg = (
                f"🔍 DRY RUN: Would download input for {year} day {day}\n"
                f"📋 Manual download: {self.BASE_URL}/{year}/day/{day}/input\n"
                f"   1. Log in to adventofcode.com\n"
                f"   2. Navigate to the URL above\n"
                f"   3. Save the content to day-{day:02d}/input.txt"
            )
            print(msg)
            return False, msg

        url = f"{self.BASE_URL}/{year}/day/{day}/input"

        for attempt in range(self.MAX_RETRIES):
            try:
                response = self.session.get(url, timeout=10)

                if response.status_code == 200:
                    return True, response.text

                if response.status_code == 404:
                    return False, f"Puzzle not yet available for day {day}"

                if response.status_code == 429:
                    if attempt < self.MAX_RETRIES - 1:
                        sleep_time = self._backoff_with_jitter(attempt)
                        print(f"⏳ Rate limited (429). Retrying in {sleep_time:.1f}s...")
                        time.sleep(sleep_time)
                        continue
                    else:
                        msg = (
                            f"❌ Rate limit exceeded after {self.MAX_RETRIES} attempts.\n"
                            f"📋 Please download manually:\n"
                            f"   {url}\n"
                            f"   Save to: day-{day:02d}/input.txt"
                        )
                        return False, msg

                if response.status_code >= 500 and attempt < self.MAX_RETRIES - 1:
                    sleep_time = self._backoff_with_jitter(attempt)
                    print(
                        f"⚠️  Server error ({response.status_code}). "
                        f"Retrying in {sleep_time:.1f}s..."
                    )
                    time.sleep(sleep_time)
                    continue

                return False, f"HTTP {response.status_code}: {response.text[:200]}"

            except requests.RequestException as e:
                if attempt < self.MAX_RETRIES - 1:
                    sleep_time = self._backoff_with_jitter(attempt)
                    print(f"⚠️  Network error: {e}. Retrying in {sleep_time:.1f}s...")
                    time.sleep(sleep_time)
                    continue
                return False, f"Network error: {e}"

        msg = (
            f"❌ Failed after {self.MAX_RETRIES} attempts.\n"
            f"📋 Please download manually:\n"
            f"   {url}\n"
            f"   Save to: day-{day:02d}/input.txt"
        )
        return False, msg

    def download_description(self, year: int, day: int) -> tuple[bool, str]:
        """
        Download puzzle description (HTML) for a given day.

        Args:
            year: Year of the puzzle
            day: Day number (1-25)

        Returns:
            Tuple of (success, content_or_error_message)
        """
        if self.dry_run:
            msg = (
                f"🔍 DRY RUN: Would download description for {year} day {day}\n"
                f"📋 Manual access: {self.BASE_URL}/{year}/day/{day}"
            )
            print(msg)
            return False, msg

        url = f"{self.BASE_URL}/{year}/day/{day}"

        for attempt in range(self.MAX_RETRIES):
            try:
                response = self.session.get(url, timeout=10)

                if response.status_code == 200:
                    return True, response.text

                if response.status_code == 404:
                    return False, f"Puzzle not yet available for day {day}"

                if response.status_code == 429:
                    if attempt < self.MAX_RETRIES - 1:
                        sleep_time = self._backoff_with_jitter(attempt)
                        print(f"⏳ Rate limited (429). Retrying in {sleep_time:.1f}s...")
                        time.sleep(sleep_time)
                        continue
                    else:
                        msg = (
                            f"❌ Rate limit exceeded after {self.MAX_RETRIES} attempts.\n"
                            f"📋 Please access manually: {url}"
                        )
                        return False, msg

                if response.status_code >= 500 and attempt < self.MAX_RETRIES - 1:
                    sleep_time = self._backoff_with_jitter(attempt)
                    print(
                        f"⚠️  Server error ({response.status_code}). "
                        f"Retrying in {sleep_time:.1f}s..."
                    )
                    time.sleep(sleep_time)
                    continue

                return False, f"HTTP {response.status_code}"

            except requests.RequestException as e:
                if attempt < self.MAX_RETRIES - 1:
                    sleep_time = self._backoff_with_jitter(attempt)
                    print(f"⚠️  Network error: {e}. Retrying in {sleep_time:.1f}s...")
                    time.sleep(sleep_time)
                    continue
                return False, f"Network error: {e}"

        msg = f"❌ Failed after {self.MAX_RETRIES} attempts.\n📋 Please access manually: {url}"
        return False, msg

    def extract_task_description(self, html_content: str) -> list[str]:
        """
        Extract article elements with class "day-desc" from HTML.

        Args:
            html_content: HTML content from AOC page

        Returns:
            List of HTML strings, each containing one article element
        """
        soup = BeautifulSoup(html_content, "html.parser")
        articles = soup.find_all("article", class_="day-desc")
        return [str(article) for article in articles]

    def convert_html_to_markdown(self, html_content: str) -> str:
        """
        Convert HTML content to Markdown format.

        Args:
            html_content: HTML string to convert

        Returns:
            Markdown-formatted string
        """
        converter = html2text.HTML2Text()
        converter.body_width = 0  # No line wrapping
        converter.ignore_links = False  # Keep links
        converter.unicode_snob = True  # Use Unicode characters

        return converter.handle(html_content)

    def save_task_file(self, day_dir: str, content: str, force: bool = False) -> bool:
        """
        Save task description to task.md file.

        Args:
            day_dir: Directory name (e.g., "day-01")
            content: Markdown content to save
            force: If True, overwrite existing file

        Returns:
            True if file was written, False if skipped
        """
        task_file = Path(day_dir) / "task.md"

        if task_file.exists() and not force:
            return False

        task_file.write_text(content, encoding="utf-8")
        return True
