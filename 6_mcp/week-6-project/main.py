from issues import IssueStore

from issues_server import add_issue, search_issues
from IPython.display import Markdown, display
import asyncio
from agents import Agent, Runner, trace

from agents.mcp import MCPServerStdio

from dotenv import load_dotenv
load_dotenv(override=True)
from mcp_agent import search_known_issues

def main():
    """Add sample issues and demonstrate searching."""
    store = IssueStore()

    issues_to_add = [
        {
            "issue": "Port 8000 already in use",
            "command": "lsof -i :8000 | grep LISTEN | awk '{print $2}' | xargs kill -9",
            "project_path": "/home/nober/andela2/ai_agents/6_mcp/week-6-project",
        }
    ]

    for entry in issues_to_add:
        issue_id = store.add_issue(
            issue=entry["issue"],
            command=entry["command"],
            project_path=entry["project_path"],
        )
        print(f"Added issue #{issue_id}: {entry['issue']}")


def search_issues():
    """Search for issues in the database."""
    store = IssueStore()
    results = store.search_issues("port 8000")
    for r in results:
        print(f"  [{r['id']}] {r['issue']}")
        print(f"       command: {r['command']}")
        print(f"       path:    {r['project_path']}")

def clear_log():
    """Clear the log file."""
    store = IssueStore()
    store.clear_log()
    print("Log file cleared.")




async def listing_mcp_tools():
    mcp_params = {"command": "uv", "args": ["run", "issues_server.py"]}
    async with MCPServerStdio(params=mcp_params, client_session_timeout_seconds=60) as server:
        mcp_tools = await server.list_tools()
    for tool in mcp_tools:
        print(f"  [{tool.name}] {tool.description}")





if __name__ == "__main__":
    # request = "What's the issue with my server not starting?"    
    # asyncio.run(search_known_issues(request))
    asyncio.run(listing_mcp_tools())