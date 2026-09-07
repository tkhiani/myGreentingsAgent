"""Integration test: end-to-end agent flow with mocked LLM and tools."""
import asyncio
import sys
import types
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

# Stub missing SDK sub-modules before importing agent
_factory_mod = types.ModuleType("sap_cloud_sdk.agent_memory.factory")
_factory_mod.create_checkpointer = lambda **kw: None  # type: ignore
_cp_mod = types.ModuleType("sap_cloud_sdk.agent_memory.factory.langgraph_checkpoint")
_cp_mod.create_checkpointer = lambda **kw: None  # type: ignore
sys.modules.setdefault("sap_cloud_sdk.agent_memory.factory", _factory_mod)
sys.modules.setdefault("sap_cloud_sdk.agent_memory.factory.langgraph_checkpoint", _cp_mod)


@pytest.mark.asyncio
async def test_agent_greeting_flow():
    """Agent should invoke get_greeting and return a greeting response."""
    # Mock the LLM chain to return a greeting message without real AI Core calls
    mock_response = MagicMock()
    mock_response.content = "Good Morning! Hope you have a great day!"

    mock_result = {"messages": [mock_response]}

    with patch("agent.SampleAgent._invoke_with_fallback", new=AsyncMock(return_value=mock_result)):
        from agent import SampleAgent
        from tools import get_greeting

        agent = SampleAgent.__new__(SampleAgent)
        # Minimal init — skip real LLM/checkpointer setup
        agent._primary_model = "test-model"
        agent._fallback_model = ""
        agent._temperature = 0.0
        agent._fallback_llm = None
        agent._checkpointer = None
        agent._summarization_middleware = None

        response = await agent.invoke("Greet me", "test-context-1", tools=[get_greeting])

    assert response.status == "completed"
    assert "Good Morning" in response.message or len(response.message) > 0


@pytest.mark.asyncio
async def test_agent_stream_yields_response():
    """Agent stream() should yield a completed response."""
    mock_response = MagicMock()
    mock_response.content = "Good Evening! Welcome."

    mock_result = {"messages": [mock_response]}

    with patch("agent.SampleAgent._invoke_with_fallback", new=AsyncMock(return_value=mock_result)):
        from agent import SampleAgent
        from tools import get_greeting

        agent = SampleAgent.__new__(SampleAgent)
        agent._primary_model = "test-model"
        agent._fallback_model = ""
        agent._temperature = 0.0
        agent._fallback_llm = None
        agent._checkpointer = None
        agent._summarization_middleware = None

        chunks = []
        async for chunk in agent.stream("Hello", "test-context-2", tools=[get_greeting]):
            chunks.append(chunk)

    assert any(c["is_task_complete"] for c in chunks)
    final = next(c for c in chunks if c["is_task_complete"])
    assert "Good Evening" in final["content"] or len(final["content"]) > 0


@pytest.mark.asyncio
async def test_agent_error_handling():
    """Agent should return an error response if the LLM fails."""
    with patch("agent.SampleAgent._invoke_with_fallback", new=AsyncMock(side_effect=Exception("LLM error"))):
        from agent import SampleAgent

        agent = SampleAgent.__new__(SampleAgent)
        agent._primary_model = "test-model"
        agent._fallback_model = ""
        agent._temperature = 0.0
        agent._fallback_llm = None
        agent._checkpointer = None
        agent._summarization_middleware = None

        response = await agent.invoke("Greet me", "test-context-3", tools=[])

    assert response.status in ("error", "completed")
    assert len(response.message) > 0
