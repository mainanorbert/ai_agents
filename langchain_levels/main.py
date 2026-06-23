# The four levels of LangChain abstraction

"""LangChain and LangGraph are best understood as a stack of four layers, where each layer is built on the one below. As you climb the stack, you hand more decisions to the framework in exchange for writing less code.

| Layer | Package | What it gives you | What you control |
|---|---|---|---|
| 1. Building blocks | `langchain-core` + `langchain-openai` | chat models, the `@tool` decorator, messages | everything, including the tool loop by hand |
| 2. Orchestration | `langgraph` | a graph of steps, with state and routing | the control flow (you design the graph) |
| 3. Agent | `langchain` (`create_agent`) | the standard agent loop, prebuilt | just model, tools and a prompt |
| 4. Harness | `deepagents` (`create_deep_agent`) | planning, a filesystem and sub-agents | your intent |

In this notebook we take one small idea, a share price lookup, and rebuild it at each layer so you can feel the abstraction rising. The whole walk takes a few minutes."""


# pip install -qU langchain langchain-openai langgraph deepagents openai python-dotenv

import os
from openai import OpenAI, AsyncOpenAI
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import requests
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage
from langgraph.graph import StateGraph, START, END
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from IPython.display import Image, Markdown, display
from langgraph.prebuilt import ToolNode, tools_condition
from langchain.agents import create_agent
from deepagents import create_deep_agent

load_dotenv(override=True)

openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
if not openrouter_api_key:
    raise ValueError("Please set the OPENROUTER_API_KEY environment variable.")

openrouter_base_url = "https://openrouter.ai/api/v1"
model_name = os.getenv("OPENROUTER_MODEL", "openai/gpt-5.4-mini")
prompt = "Hey good evening what is BODMAS."


# Layer 1: the building blocks
llm = ChatOpenAI(
    model=model_name,
    api_key=openrouter_api_key,
    base_url=openrouter_base_url,
)




def fetch_live_price(symbol: str) -> float:
    response = requests.get("https://www.alphavantage.co/query", timeout=10, params={
        "function": "GLOBAL_QUOTE", "symbol": symbol, "apikey": os.getenv("ALPHAVANTAGE_API_KEY")})
    return float(response.json()["Global Quote"]["05. price"])

@tool
def get_share_price(symbol: str) -> float:
    """Return the current share price for a given ticker symbol."""
    if os.environ.get("ALPHAVANTAGE_API_KEY"):
        try:
            return fetch_live_price(symbol)
        except Exception:
            pass
    fake_prices = {"AAPL": 241.5, "GOOG": 168.2, "GOOGL": 168.2, "AMZN": 198.0}
    return fake_prices.get(symbol.upper(), 0.0)

llm_with_tools = llm.bind_tools([get_share_price])

conversation = [HumanMessage('What is the share price of Boeing?')]

ai_message = llm_with_tools.invoke(conversation)
conversation.append(ai_message)

for call in ai_message.tool_calls:
    result = get_share_price.invoke(call["args"])
    print(f"Result: {result}")
    conversation.append(ToolMessage(content=str(result), tool_call_id=call["id"]))
print(llm_with_tools.invoke(conversation).content)


# Layer 2: LangGraph orchestration
## Doing the same as above with Langgraph
class State(TypedDict):
    messages: Annotated[list, add_messages]

def chatbot(state: State) -> dict:
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

builder = StateGraph(State)
builder.add_node("chatbot", chatbot)
builder.add_node("tools", ToolNode([get_share_price]))
builder.add_edge(START, "chatbot")
builder.add_conditional_edges("chatbot", tools_condition)
builder.add_edge("tools", "chatbot")
graph = builder.compile()

# display(Image(graph.get_graph().draw_mermaid_png()))
result = graph.invoke({"messages": [{"role": "user", "content": "Which is more expensive, Apple share or Google share?"}]})
print(result["messages"][-1].content)


# Layer 3: the agent
# Creating an Agent
agent = create_agent(
    model=llm,
    tools=[get_share_price],
    system_prompt="You are a helpful financial assistant. Use your tools.",
)

result = agent.invoke({"messages": [{"role": "user", "content": "What are the stock prices of Apple, Google and Amazon?"}]})
print(result["messages"][-1].content)


# Layer 4: the harness: Deep Agents
# Has a planning tool, todo list, filesystem, and subagent for delegating

deep_agent = create_deep_agent(
    model=llm,
    tools=[get_share_price],
    system_prompt="You are an analyst. Plan your work with your todo tool, use your tools, and write your answer to a file when asked as a bulleted list.",
)
result = deep_agent.invoke({"messages": [{"role": "user", "content":
    "Look up the share prices of AAPL, GOOG and AMZN, then write a short markdown note ranking them to prices.md"}]})

tools_used = [tc["name"] for m in result["messages"] for tc in (getattr(m, "tool_calls", []) or [])]
print("Tools the agent called, in order:")
print(tools_used)

display(Markdown(result["files"]["/prices.md"]["content"].replace('$','')))