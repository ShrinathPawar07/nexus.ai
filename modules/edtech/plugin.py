from nexus_ai.modules.edtech.edtech_module import EdtechModule

class EdtechPlugin:
    def run(self, query):
        engine = EdtechModule()
        return engine.process(query)

    def get_metadata(self):
        return {
            "name": "edtech",
            "vertical": "edtech",  # 👈 required for CLI filtering
            "validated": True,     # 👈 required for --validated-only
            "description": "Handles EdTech workflows including personalized learning, curriculum mapping, and student analytics.",
            "module": "EdtechModule",
            "author": "Shrinath",
            "version": "1.0.0",
            "tags": ["education", "learning", "curriculum", "analytics"]
        }