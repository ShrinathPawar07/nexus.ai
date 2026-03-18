from nexus_ai.modules.healthcare.healthcare_module import HealthcareModule

class HealthcarePlugin:
    def run(self, query):
        engine = HealthcareModule()
        return engine.process(query)

    def get_metadata(self):
        return {
            "name": "healthcare",
            "vertical": "healthcare",  # 👈 required for CLI filtering
            "validated": True,         # 👈 required for --validated-only
            "description": "Supports Healthcare workflows such as patient monitoring, diagnostics, and clinical decision support.",
            "module": "HealthcareModule",
            "author": "Shrinath",
            "version": "1.0.0",
            "tags": ["healthcare", "patient-data", "diagnostics", "clinical-support"]
        }