"""Tests for backoff and retry logic."""

import pytest

from cli.aoc_client import AoCClient


def test_backoff_increases_exponentially():
    """Test that backoff time increases exponentially."""
    client = AoCClient(None, dry_run=True)
    
    backoff_0 = client._backoff_with_jitter(0)
    backoff_1 = client._backoff_with_jitter(1)
    backoff_2 = client._backoff_with_jitter(2)
    
    # Each should be roughly double (within jitter tolerance)
    assert backoff_0 < backoff_1 < backoff_2
    assert backoff_0 >= client.BASE_BACKOFF * 0.9  # Account for jitter
    assert backoff_2 <= client.MAX_BACKOFF


def test_backoff_has_jitter():
    """Test that jitter adds randomness to backoff."""
    client = AoCClient(None, dry_run=True)
    
    # Run multiple times and check they're not all identical
    backoffs = [client._backoff_with_jitter(3) for _ in range(10)]
    
    # Should have some variation due to jitter
    assert len(set(backoffs)) > 1


def test_dry_run_mode():
    """Test that dry run mode prevents network calls."""
    client = AoCClient("fake_token", dry_run=True)
    
    success, message = client.download_input(2025, 1)
    
    assert not success
    assert "DRY RUN" in message
    assert "Manual download" in message
