# nexus_ai/agents/langchain_router_agent.py

from langchain_core.tools import Tool
from langchain.agents import initialize_agent, AgentType
from langchain_openai import ChatOpenAI
from nexus_ai.core.router import Router
import os

# Ensure OpenAI key is available
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") or "sk-xxxxx"  # Replace as needed

router = Router(debug=False)

def router_tool_fn(query: str, context: str) -> str:
    return router.route_query(query, context)

tools = [
    Tool(
        name="NexusRouter",
        func=lambda x: router_tool_fn(query=x["query"], context=x["context"]),
        description="Routes query to the appropriate vertical module based on context."
    )
]

llm = ChatOpenAI(
    temperature=0,
    model="gpt-4",
    openai_api_key=OPENAI_API_KEY
)

agent = initialize_agent(tools, llm, agent_type=AgentType.OPENAI_FUNCTIONS)

def run_agent(query: str, context: str):
    return agent.run({"query": query, "context": context})
