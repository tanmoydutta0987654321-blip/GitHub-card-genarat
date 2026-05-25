import os
import sys
from google.adk.agents.llm_agent import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset, StdioConnectionParams, StdioServerParameters

# Resolve absolute path to the local mcp_server.py file
base_dir = os.path.dirname(os.path.abspath(__file__))
mcp_server_path = os.path.join(base_dir, "mcp_server.py")

# Use current python executable to start the stdio server
python_executable = sys.executable or "python"

# Initialize connection parameters with StdioConnectionParams as recommended
server_params = StdioServerParameters(
    command=python_executable,
    args=[mcp_server_path]
)
connection_params = StdioConnectionParams(
    server_params=server_params
)

# Create McpToolset instance
mcp_toolset = McpToolset(connection_params=connection_params)

# System instruction for the agent
system_instruction = (
    "You are a GitHub profile analyst and dev card generator. When a user gives you a GitHub username, "
    "you ALWAYS follow this exact sequence: first call scrape_github, then analyze_profile with the result, "
    "then generate_card_html with all three inputs, then save_card. Never skip steps. "
    "Be enthusiastic about developers' work. If the profile is private or doesn't exist, say so clearly."
)

# Export the agent as github_card_agent using Gemini 2.5 Flash
github_card_agent = LlmAgent(
    name="github_card_agent",
    model="gemini-2.5-flash",
    instruction=system_instruction,
    tools=[mcp_toolset]
)

class GitHubCardAgent:
    """
    Orchestrates the GitHub Developer Card Generation pipeline
    using Google ADK and local MCP tools.
    """
    def __init__(self):
        self.agent = github_card_agent
        self.toolset = mcp_toolset

    async def initialize(self):
        # Tools are registered synchronously in recent ADK versions
        pass

    async def generate_card(self, username: str) -> str:
        prompt = f"Generate and save a developer card for the GitHub user: {username}"
        response = await self.agent.run(prompt)
        return response.text

    async def close(self):
        try:
            await self.toolset.close()
        except Exception as e:
            print(f"Error closing McpToolset: {e}", file=sys.stderr)
