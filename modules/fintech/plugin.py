from nexus_ai.modules.fintech.fintech_module import FintechModule

class FintechPlugin:
    def run(self, input_data: dict):
        """Executes Fintech logic based on input query. Supports fraud detection, credit scoring, etc."""
        print(f"[FintechPlugin] Received input_data: {input_data}")
        
        amount = input_data.get("amount", 0)
        credit_score = input_data.get("credit_score", 0)

        # Example logic
        risk_score = round((1000 - credit_score) / 1000 + amount / 100000, 2)
        approval = credit_score >= 700 and amount <= 10000

        return {
            "risk_score": risk_score,
            "approval": approval
        }

        
    def get_metadata(self):
     """Returns structured metadata for plugin registration, validation, and CLI introspection."""

     return {
            "name": "fintech",
            "vertical": "fintech",  # 👈 lowercase to match CLI filter
            "validated": True,      # 👈 required for --validated-only
            "description": "Handles Fintech workflows including fraud detection, credit scoring, and financial forecasting.",
            "module": "FintechModule",
            "author": "Shrinath",
            "version": "1.0.0",
            "tags": ["fintech", "fraud", "credit", "forecasting", "finance"]
        }
    