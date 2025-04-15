from typing import Literal

from langchain_core.runnables import RunnableConfig
from langchain_openai import AzureChatOpenAI
from langgraph.graph import MessagesState, StateGraph
from langgraph.graph.state import CompiledStateGraph
from langgraph.types import Command, interrupt

from agent_states.agents.appointment_planner import (
    create as create_appointment_planner,
)
from agent_states.hosting import container
from agent_states.protocols.i_azure_openai_service import IAzureOpenAIService

llm_client = container[IAzureOpenAIService].get_model()


def human_node(state: MessagesState, config: RunnableConfig):
    """A node for collecting user input."""
    val = ""
    user_input = interrupt(value=val)
    return Command(resume=user_input)


def create_graph(llm: AzureChatOpenAI) -> CompiledStateGraph:
    def call_appointment_planner(
        state: MessagesState,
    ) -> Command[Literal["human"]]:
        response = create_appointment_planner(llm).invoke(state)
        return Command(update=response, goto="human")

    builder = StateGraph(MessagesState)
    builder.set_entry_point("appointment_planner")
    builder.add_node("appointment_planner", call_appointment_planner)
    builder.add_node("human", human_node)
    return builder.compile()


def main():
    llm = container[IAzureOpenAIService].get_model()
    graph = create_graph(llm)

    def stream(user_input: str) -> None:
        stream_input = (
            {"messages": [{"role": "user", "content": user_input}]}
            if user_input
            else None
        )
        for output in graph.stream(input=stream_input):
            if isinstance(output, dict):
                node_id = list(output.keys())[0]
                # print(output)
                if node_id != "__interrupt__":
                    vals = list(output.values())[0]

                    if vals and type(vals["messages"][-1]) is not dict:  # noqa: E721
                        vals["messages"][-1].pretty_print()

    print("Start a chat. Type 'quit' or 'exit' or 'q' to exit.\n")
    print("Can you please provide your medical condition?\n")
    prompt_msg = "User (enter q/quit/exit to quit): "
    user_input: str = input(prompt_msg).strip()

    while user_input.lower() not in ["q", "quit", "exit"]:
        stream(user_input)
        user_input = input(prompt_msg).strip()


if __name__ == "__main__":
    main()
