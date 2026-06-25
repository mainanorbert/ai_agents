from agents import Agent, Runner, SQLiteSession, OpenAIChatCompletionsModel
from agents.mcp import MCPServerStdio 
from dotenv import load_dotenv
import asyncio
import os
from IPython.display import display, Markdown
from pathlib import Path
from qdrant_client import QdrantClient
from agents.extensions.models.litellm_model import LitellmModel
import gradio as gr
load_dotenv(override=True)
from openai import OpenAI, AsyncOpenAI
from styles import CSS, JS



openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
openrouter_model = os.getenv("OPENROUTER_MODEL")


llm_client = AsyncOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=openrouter_api_key,
)
model = OpenAIChatCompletionsModel(
    model=openrouter_model,
    openai_client=llm_client,
)

agent = Agent("Test Agent",
    model=model,
)

knowledge_dir = Path.cwd() / "knowledge2"
knowledge_dir.mkdir(exist_ok=True)
vectordb_path = knowledge_dir / "vectordb"

fetch_params = {
    "command": "uvx",
    "args": ["mcp-server-fetch"],
}

vectorstore_params = {
    "command": "uvx",
    "args": ["mcp-server-qdrant"],
    "env": {
        "QDRANT_LOCAL_PATH": str(vectordb_path),
        "COLLECTION_NAME": "knowledge",
    },
}

CONTEXT = """
You are an Agent with expert knowledge about Norbert Osiemo with particular focus on his Career, Education, Skills, Projects, and Achievements.
"""

INSTRUCTIONS = CONTEXT + """
You are populating your memories with information retrieved from a given website.
Use your MCP tools to retrieve the website. Extract key knowledge. Check what's already in your memories to avoid duplicates.
After you are done, reply with a brief status update and the number of memories you added.
Aim to add at least 10 unique memories, unless your existing memories are already comprehensive.
"""
urls = ['https://nober-portfolio-mvh2214as-norberts-projects-6a0c5fda.vercel.app']*2 + ['https://digi-twin-3x3j.vercel.app/']*2


async def main():
    for url in urls:
        async with MCPServerStdio(
            params=fetch_params, client_session_timeout_seconds=120
        ) as fetch_mcp:
            async with MCPServerStdio(
                params=vectorstore_params, client_session_timeout_seconds=120
            ) as vectorstore_mcp:
                agent = Agent(name="Ingester", model=model, instructions=INSTRUCTIONS, mcp_servers=[fetch_mcp, vectorstore_mcp])
                task = f"Add unique memories with information from this website: {url} and reply with a one sentence status update including how many memories were added."
                response = await Runner.run(agent, task, max_turns=20)
                print(f"Response from {url}: {response.final_output}")


if __name__ == "__main__":
    asyncio.run(main())



# client = QdrantClient(path=str(vectordb_path))
# collection_name = "knowledge"

# info = client.get_collection(collection_name)
# print(f"Memories in '{collection_name}': {info.points_count}\n")

# points, _ = client.scroll(collection_name=collection_name, limit=200, with_payload=True, with_vectors=False)
# for i, p in enumerate(points, 1):
#     doc = (p.payload or {}).get("document", "")
#     preview = doc.replace("\n", " ")[:160]
#     print(f"{i:>3}. {preview}{'...' if len(doc) > 160 else ''}")

# client.close()



## Agentic RAG + OpenAI Agents SDK + MCP in a 4 line function!

async def agentic_rag(message, history) -> str:
    EXPERT_INSTRUCTIONS = """
    You are an expert about Norbert and his career. You are answering questions about him and his career to visitors on his website.
    Use your memories to help answer the question. If you don't know the answer, say so.
    """

    convo = SQLiteSession("test_conversation")
    async with MCPServerStdio(
        params=vectorstore_params, client_session_timeout_seconds=120
    ) as vectorstore_mcp:
        agent = Agent(name="RAG Agent", model=model, instructions=EXPERT_INSTRUCTIONS, mcp_servers=[vectorstore_mcp])
        response = await Runner.run(agent, message, session=convo)
        return response.final_output


EXAMPLES = ["Which are your top 3 skills"]
gr.ChatInterface(agentic_rag, examples=EXAMPLES, chatbot=gr.Chatbot(show_label=False, height=700)).launch(css=CSS, js=JS, theme=gr.themes.Base(), inbrowser=True)