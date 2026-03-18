from nexus_ai.modules.it.it_module import ITModule

class ITPlugin:
    def run(self, query):
        engine = ITModule()
        return engine.process(query)

    def get_metadata(self):
        return {
            "name": "it",
            "vertical": "it",  # 👈 required for CLI filtering
            "validated": True, # 👈 required for --validated-only
            "description": "Manages IT workflows such as infrastructure monitoring, incident response, and asset management.",
            "module": "ITModule",
            "author": "Shrinath",
            "version": "1.0.0",
            "tags": ["it", "infrastructure", "monitoring", "incident", "assets"]
        }