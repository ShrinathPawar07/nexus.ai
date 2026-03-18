from nexus_ai.modules.automotive.automotive_module import AutomotiveModule

class AutomotivePlugin:
    def run(self, query):
        engine = AutomotiveModule()
        return engine.process(query)

    def get_metadata(self):
        return {
            "name": "automotive",
            "vertical": "automotive",  # 👈 required for CLI filtering
            "validated": True,         # 👈 required for --validated-only
            "description": "Manages Automotive workflows such as vehicle telemetry, diagnostics, and predictive maintenance.",
            "module": "AutomotiveModule",
            "author": "Shrinath",
            "version": "1.0.0",
            "tags": ["automotive", "telemetry", "diagnostics", "predictive"]
        }