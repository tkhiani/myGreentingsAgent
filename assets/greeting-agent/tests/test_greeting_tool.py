"""Unit tests for get_greeting tool — covers all four time ranges."""
from unittest.mock import patch
from datetime import datetime

import pytest


def _greeting_at_hour(hour: int) -> str:
    """Helper: return the greeting the tool would produce at the given hour."""
    fake_dt = datetime(2024, 1, 1, hour, 0, 0)
    with patch("tools.datetime") as mock_dt:
        mock_dt.now.return_value = fake_dt
        from tools import get_greeting
        return get_greeting.invoke({})


def test_good_morning():
    """Hours 05-11 should yield 'Good Morning'."""
    for hour in [5, 8, 11]:
        assert _greeting_at_hour(hour) == "Good Morning", f"Failed at hour {hour}"


def test_good_afternoon():
    """Hours 12-17 should yield 'Good Afternoon'."""
    for hour in [12, 14, 17]:
        assert _greeting_at_hour(hour) == "Good Afternoon", f"Failed at hour {hour}"


def test_good_evening():
    """Hours 18-20 should yield 'Good Evening'."""
    for hour in [18, 19, 20]:
        assert _greeting_at_hour(hour) == "Good Evening", f"Failed at hour {hour}"


def test_good_night():
    """Hours 21-04 should yield 'Good Night'."""
    for hour in [21, 23, 0, 3, 4]:
        assert _greeting_at_hour(hour) == "Good Night", f"Failed at hour {hour}"


def test_fallback_on_exception():
    """If datetime raises, the tool should fall back to 'Hello'."""
    with patch("tools.datetime") as mock_dt:
        mock_dt.now.side_effect = Exception("time error")
        from tools import get_greeting
        result = get_greeting.invoke({})
    assert result == "Hello"
