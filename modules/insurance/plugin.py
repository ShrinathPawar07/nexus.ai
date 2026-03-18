class InsurancePlugin:
    """Insurance plugin for Nexus_AI."""

    def get_metadata(self):
        """Returns structured metadata for plugin registration, validation, and CLI introspection."""
        return {
            "name": "insurance",
            "vertical": "insurance",
            "validated": False,
            "description": "Describe what this plugin does.",
            "module": "insurance_module",
            "author": "Shrinath",
            "version": "0.1",
            "tags": []
        }

    def run(self, input_data: dict):
        """Executes plugin logic based on input query."""
        query = input_data.get("query", "")
        return f"[InsurancePlugin] Received query: '{query}'"