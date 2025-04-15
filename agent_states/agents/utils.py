from typing import Annotated

from langchain_core.tools import tool
from langchain_core.tools.base import InjectedToolCallId
from langgraph.prebuilt import InjectedState
from langgraph.types import Command


def build_handoff_tool(agent_name: str):
    """Create a tool that can return handoff via a Command

    :param agent_name: The name of the agent to transfer to.
    :return: A function that can be used as a tool to transfer to the agent.
    """
    tool_name = f"transfer_to_{agent_name}"

    @tool(tool_name)
    def handoff_to_agent(
        state: Annotated[dict, InjectedState],
        tool_call_id: Annotated[str, InjectedToolCallId],
    ) -> Command:
        """Ask another agent for help.

        @param state: The current state of the conversation.
        @param tool_call_id: The ID of the tool call.
        @return: A Command to transfer to the specified agent.
        """
        tool_message = {
            "role": "tool",
            "content": f"Successfully transferred to {agent_name}",
            "name": tool_name,
            "tool_call_id": tool_call_id,
        }
        return Command(
            # navigate to another agent node in the PARENT graph
            goto=agent_name,
            graph=Command.PARENT,
            update={"messages": state["messages"] + [tool_message]},
        )

    return handoff_to_agent
