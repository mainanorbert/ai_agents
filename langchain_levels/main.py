# pip install -qU langchain langchain-openai langgraph deepagents

import os
import requests
from typing import Annotated
from typing_extensions import TypedDict
from IPython.display import Image, Markdown, display
from openai import PermissionDeniedError, RateLimitError
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain.agents import create_agent
from deepagents import create_deep_agent
from dotenv import load_dotenv

load_dotenv()


openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("Please set the OPENAI_API_KEY environment variable.")

os.environ["OPENAI_API_KEY"] = openai_api_key

alphavantage_api_key = os.getenv("ALPHAVANTAGE_API_KEY")
if alphavantage_api_key:
    os.environ["ALPHAVANTAGE_API_KEY"] = alphavantage_api_key


default_models = [
    "gpt-4o-mini",
    "gpt-4o",
    "gpt-4.1",
    "gpt-4.1-mini",
    "gpt-3.5-turbo",
]

configured_model = os.getenv("OPENAI_MODEL")
candidate_models = [configured_model] if configured_model else default_models
prompt = "In one sentence, what does it mean to say that an AI Agent is 'autonomous'?"

last_error = None
for model_name in candidate_models:
    try:
        llm = ChatOpenAI(model=model_name)
        reply = llm.invoke(prompt)
        print(f"Using model: {model_name}")
        print(reply.content)
        break
    except PermissionDeniedError as exc:
        last_error = exc
        continue
    except RateLimitError as exc:
        raise RuntimeError(
            f"Model '{model_name}' is accessible, but your OpenAI project is out of quota. "
            "Check billing/usage or switch to a project with available credits."
        ) from exc
else:
    tried_models = ", ".join(candidate_models)
    raise RuntimeError(
        f"No accessible OpenAI model found. Tried: {tried_models}. "
        "Set OPENAI_MODEL to a model your OpenAI project can access."
    ) from last_error
