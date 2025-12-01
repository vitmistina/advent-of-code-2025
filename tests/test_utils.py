"""Tests for utility functions."""

import os

import pytest

from cli.utils import get_year, never_log_secret, validate_day


def test_validate_day_valid():
    """Test day validation for valid days."""
    assert validate_day(1) is True
    assert validate_day(25) is True
    assert validate_day(15) is True


def test_validate_day_invalid():
    """Test day validation for invalid days."""
    assert validate_day(0) is False
    assert validate_day(26) is False
    assert validate_day(-1) is False


def test_get_year_from_env(monkeypatch):
    """Test getting year from environment."""
    monkeypatch.setenv("AOC_YEAR", "2024")
    assert get_year() == 2024


def test_get_year_default(monkeypatch):
    """Test default year when not in environment."""
    monkeypatch.delenv("AOC_YEAR", raising=False)
    assert get_year() == 2025


def test_never_log_secret_masks_token(monkeypatch):
    """Test that secrets are masked in output."""
    monkeypatch.setenv("AOC_SESSION", "secret123")
    
    text = "Error: Using token secret123 failed"
    sanitized = never_log_secret(text)
    
    assert "secret123" not in sanitized
    assert "***REDACTED***" in sanitized


def test_never_log_secret_no_leak(monkeypatch):
    """Test that text without secrets passes through."""
    monkeypatch.setenv("AOC_SESSION", "secret123")
    
    text = "This is a normal message"
    sanitized = never_log_secret(text)
    
    assert sanitized == text
