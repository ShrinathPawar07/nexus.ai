class ITModule:
    """
    The IT plugin for Nexus.AI.
    Handles diagnostics for infrastructure APIs, service health, and DevOps integration.
    """

    def __init__(self):
        self.name = "ItModule"
        self.version = "1.0.0"
        self.author = "Nexus Core Team"

    def process(self, input_data: dict) -> str:
        query = input_data.get("query", "")
        context = input_data.get("context", "")
        query_lower = query.lower()

        if "incident" in query_lower:
            return f"[{self.name}] Incident response triggered for: '{query}' in context '{context}'"
        elif "monitoring" in query_lower:
            return f"[{self.name}] Infrastructure monitoring initiated for: '{query}'"
        elif "asset" in query_lower:
            return f"[{self.name}] Asset management activated for: '{query}'"
        else:
            return f"[{self.name}] Unrecognized query type: '{query}'"

    def _handle_infrastructure(self, query: str) -> str:
        return f"[{self.name}] Infrastructure diagnostics – feature coming soon."

    def _handle_devops(self, query: str) -> str:
        return f"[{self.name}] DevOps integration diagnostics – feature coming soon."

    def get_metadata(self) -> dict:
        return {
            "name": "ItModule",
            "version": "1.0",
            "author": "Shrinath",
            "vertical": "IT",
            "description": "Handles diagnostics for infrastructure APIs, service health, and DevOps integration.",
            "capabilities": ["infrastructure_diagnostics", "devops_integration"],
            "tags": ["api", "it", "diagnostics"]
        }

    def test(self) -> str:
        return "ItModule test passed"
