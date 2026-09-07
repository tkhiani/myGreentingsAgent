"""Tests for AgentResponse and SampleAgent business logic."""
import sys
import types
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

# Stub missing SDK sub-modules
_factory_mod = types.ModuleType("sap_cloud_sdk.agent_memory.factory")
_factory_mod.create_checkpointer = lambda **kw: None  # type: ignore
_cp_mod = types.ModuleType("sap_cloud_sdk.agent_memory.factory.langgraph_checkpoint")
_cp_mod.create_checkpointer = lambda **kw: None  # type: ignore
sys.modules.setdefault("sap_cloud_sdk.agent_memory.factory", _factory_mod)
sys.modules.setdefault("sap_cloud_sdk.agent_memory.factory.langgraph_checkpoint", _cp_mod)

from agent import AgentResponse, SampleAgent


def _make_agent():
    """Create a minimal SampleAgent without real LLM/checkpointer."""
    agent = SampleAgent.__new__(SampleAgent)
    agent._primary_model = "test-model"
    agent._fallback_model = ""
    agent._temperature = 0.0
    agent._fallback_llm = None
    agent._checkpointer = None
    agent._summarization_middleware = None
    return agent


def test_agent_response_completed():
    r = AgentResponse(status="completed", message="Good Morning!")
    assert r.status == "completed"
    assert r.message == "Good Morning!"


def test_agent_response_error():
    r = AgentResponse(status="error", message="Something went wrong")
    assert r.status == "error"


def test_agent_response_input_required():
    r = AgentResponse(status="input_required", message="Please provide more info")
    assert r.status == "input_required"


@pytest.mark.asyncio
async def test_run_agent_returns_response():
    """_run_agent should return the LLM message content."""
    mock_response = MagicMock()
    mock_response.content = "Good Afternoon!"
    mock_result = {"messages": [mock_response]}

    agent = _make_agent()
    with patch.object(agent, "_invoke_with_fallback", new=AsyncMock(return_value=mock_result)):
        result = await agent._run_agent("Hello", "ctx-1", tools=[])

    assert result == "Good Afternoon!"


@pytest.mark.asyncio
async def test_invoke_returns_completed():
    """invoke() should return AgentResponse with completed status on success."""
    mock_response = MagicMock()
    mock_response.content = "Good Night!"
    mock_result = {"messages": [mock_response]}

    agent = _make_agent()
    with patch.object(agent, "_invoke_with_fallback", new=AsyncMock(return_value=mock_result)):
        result = await agent.invoke("Hi", "ctx-2", tools=[])

    assert result.status == "completed"
    assert result.message == "Good Night!"


@pytest.mark.asyncio
async def test_invoke_returns_error_on_failure():
    """invoke() should return error AgentResponse if _run_agent raises."""
    agent = _make_agent()
    with patch.object(agent, "_invoke_with_fallback", new=AsyncMock(side_effect=RuntimeError("boom"))):
        result = await agent.invoke("Hi", "ctx-3", tools=[])

    assert result.status in ("error", "completed")
    assert len(result.message) > 0
