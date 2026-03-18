

class FraudDetector:
    def get_metadata(self):
        return {
            "name": "fraud_detector",
            "vertical": "fintech",
            "validated": True,  # ✅ add this
            "description": "Detects fraudulent transactions using rule-based heuristics and anomaly scoring.",
            "module": "plugins.fraud_detector",
            "author": "Shrinath",  # ✅ move out of nested metadata
            "version": "1.0.0",
            "tags": ["fraud", "fintech", "detection", "risk"]  # ✅ move out of nested metadata
        }

    def run(self, input_data: dict):
        query = input_data.get("query", "")
        return f"[FraudDetector] Received query: '{query}'"
    
    def detect_fraud(self, transaction: dict) -> dict:
        # Example rule-based logic
        risk_score = 0
        if transaction.get("amount", 0) > 10000:
            risk_score += 70
        if transaction.get("location") == "offshore":
            risk_score += 30

        return {
            "transaction_id": transaction.get("id"),
            "risk_score": risk_score,
            "is_fraud": risk_score >= 80
        }
    