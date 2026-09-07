"""Tests for agent decorator functions and system prompt."""
import sys
import types

# Stub missing SDK sub-modules
_factory_mod = types.ModuleType("sap_cloud_sdk.agent_memory.factory")
_factory_mod.create_checkpointer = lambda **kw: None  # type: ignore
_cp_mod = types.ModuleType("sap_cloud_sdk.agent_memory.factory.langgraph_checkpoint")
_cp_mod.create_checkpointer = lambda **kw: None  # type: ignore
sys.modules.setdefault("sap_cloud_sdk.agent_memory.factory", _factory_mod)
sys.modules.setdefault("sap_cloud_sdk.agent_memory.factory.langgraph_checkpoint", _cp_mod)

import pytest
from agent import (
    get_model_name,
    get_fallback_model_name,
    get_temperature,
    thread_ttl_seconds,
    summarization_trigger_tokens,
    get_summarization_model_name,
    get_system_prompt,
)


def test_get_model_name_returns_string():
    result = get_model_name()
    assert isinstance(result, str)
    assert len(result) > 0


def test_get_fallback_model_name_returns_string():
    result = get_fallback_model_name()
    assert isinstance(result, str)


def test_get_temperature_returns_float():
    result = get_temperature()
    assert isinstance(result, float)
    assert 0.0 <= result <= 1.0


def test_thread_ttl_seconds_returns_positive_int():
    result = thread_ttl_seconds()
    assert isinstance(result, int)
    assert result > 0


def test_summarization_trigger_tokens_returns_positive_int():
    result = summarization_trigger_tokens()
    assert isinstance(result, int)
    assert result > 0


def test_get_summarization_model_name_returns_string():
    result = get_summarization_model_name()
    assert isinstance(result, str)
    assert len(result) > 0


def test_get_system_prompt_contains_greeting():
    result = get_system_prompt()
    assert isinstance(result, str)
    assert "greet" in result.lower() or "greeting" in result.lower()
    assert len(result) > 10


def test_get_system_prompt_mentions_tool():
    result = get_system_prompt()
    assert "get_greeting" in result or "tool" in result.lower()
