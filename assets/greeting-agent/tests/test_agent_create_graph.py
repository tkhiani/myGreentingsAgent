"""Additional agent coverage tests — _create_graph and _invoke_with_fallback paths."""
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

from agent import SampleAgent


def _make_agent(fallback_model: str = "") -> SampleAgent:
    agent = SampleAgent.__new__(SampleAgent)
    agent._primary_model = "test-model"
    agent._fallback_model = fallback_model
    agent._temperature = 0.0
    agent.llm = MagicMock()
    agent._fallback_llm = None
    agent._checkpointer = None
    agent._summarization_middleware = None
    return agent


@pytest.mark.asyncio
async def test_invoke_with_fallback_primary_success():
    """_invoke_with_fallback should return primary model result on success."""
    mock_response = MagicMock()
    mock_response.content = "Good Morning!"
    mock_result = {"messages": [mock_response]}

    mock_graph = MagicMock()
    mock_graph.ainvoke = AsyncMock(return_value=mock_result)

    agent = _make_agent()
    with patch.object(agent, "_create_graph", return_value=mock_graph):
        with patch("mcp_providers.agw.get_user_sub", return_value="test-user"):
            result = await agent._invoke_with_fallback([], "prompt", "Hello", "ctx-x")

    assert result == mock_result


@pytest.mark.asyncio
async def test_invoke_with_fallback_no_fallback_raises():
    """_invoke_with_fallback should re-raise when no fallback model configured."""
    from litellm.exceptions import APIConnectionError

    mock_graph = MagicMock()
    mock_graph.ainvoke = AsyncMock(side_effect=APIConnectionError("fail", None, None))

    agent = _make_agent(fallback_model="")
    with patch.object(agent, "_create_graph", return_value=mock_graph):
        with patch("mcp_providers.agw.get_user_sub", return_value="test-user"):
            with pytest.raises(APIConnectionError):
                await agent._invoke_with_fallback([], "prompt", "Hello", "ctx-y")


@pytest.mark.asyncio
async def test_stream_no_tools_injects_notice():
    """stream() with empty tools should still complete successfully."""
    mock_response = MagicMock()
    mock_response.content = "Good Afternoon!"
    mock_result = {"messages": [mock_response]}

    agent = _make_agent()
    with patch.object(agent, "_invoke_with_fallback", new=AsyncMock(return_value=mock_result)):
        chunks = []
        async for chunk in agent.stream("Hi", "ctx-z", tools=[]):
            chunks.append(chunk)

    completed = [c for c in chunks if c["is_task_complete"]]
    assert len(completed) == 1
    assert "Good Afternoon!" in completed[0]["content"]
