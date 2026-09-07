"""Tests for mcp_providers.agw module — mock mode and token utilities."""
import json
import os
import sys
import types
from pathlib import Path
from unittest.mock import patch

import pytest

# Ensure IBD_TESTING is set before importing agw
os.environ["IBD_TESTING"] = "1"


def test_get_mcp_tools_returns_empty_when_no_mock_file():
    """When mcp-mock.json is absent, _build_mock_tools returns empty list."""
    from mcp_providers.agw import _build_mock_tools
    with patch("mcp_providers.agw._MOCK_FILE", Path("/nonexistent/mcp-mock.json")):
        result = _build_mock_tools()
    assert result == []


def test_get_mcp_tools_handles_invalid_json():
    """When mcp-mock.json contains invalid JSON, returns empty list gracefully."""
    from mcp_providers.agw import _build_mock_tools
    import tempfile
    with tempfile.NamedTemporaryFile(suffix=".json", mode="w", delete=False) as f:
        f.write("NOT VALID JSON {{{{")
        tmp_path = Path(f.name)
    try:
        with patch("mcp_providers.agw._MOCK_FILE", tmp_path):
            result = _build_mock_tools()
        assert result == []
    finally:
        tmp_path.unlink(missing_ok=True)


@pytest.mark.asyncio
async def test_get_mcp_tools_returns_list_in_test_mode():
    """In IBD_TESTING mode with no mock file, get_mcp_tools returns empty list."""
    from mcp_providers.agw import get_mcp_tools
    with patch("mcp_providers.agw._MOCK_FILE", Path("/nonexistent/mcp-mock.json")):
        result = await get_mcp_tools()
    assert isinstance(result, list)


def test_set_and_get_user_token():
    """set_user_token and get_user_token should round-trip correctly."""
    from mcp_providers.agw import set_user_token, get_user_token, reset_user_token
    token = set_user_token("my-test-token")
    assert get_user_token() == "my-test-token"
    reset_user_token(token)


def test_get_user_sub_returns_unknown_in_test_mode_without_token():
    """get_user_sub should return 'unknown' in IBD_TESTING when no token is set."""
    from mcp_providers.agw import set_user_token, reset_user_token, get_user_sub
    token = set_user_token(None)
    try:
        result = get_user_sub()
        assert result == "unknown"
    finally:
        reset_user_token(token)


def test_get_user_sub_decodes_valid_jwt():
    """get_user_sub should extract sub from a valid JWT payload."""
    import base64
    payload = base64.urlsafe_b64encode(
        json.dumps({"sub": "user-123", "iss": "test"}).encode()
    ).rstrip(b"=").decode()
    fake_token = f"header.{payload}.signature"

    from mcp_providers.agw import set_user_token, reset_user_token, get_user_sub
    ctx_token = set_user_token(fake_token)
    try:
        result = get_user_sub()
        assert result == "user-123"
    finally:
        reset_user_token(ctx_token)


def test_reset_user_token_restores_previous_value():
    """reset_user_token should restore the previous context value."""
    from mcp_providers.agw import set_user_token, get_user_token, reset_user_token
    original = get_user_token()
    ctx_token = set_user_token("temp-token")
    assert get_user_token() == "temp-token"
    reset_user_token(ctx_token)
    assert get_user_token() == original
