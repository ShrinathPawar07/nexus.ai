# compliance_checker.py

VERTICAL_REQUIREMENTS = {
    "fintech": ["detect_fraud", "score_risk"],
    "edtech": ["transform", "analyze"],
    "healthcare": ["predict", "sanitize"]
}

def check_compliance(plugin):
     if plugin["vertical"] == "fintech":

      required = VERTICAL_REQUIREMENTS.get(plugin["vertical"], [])
      return all(cap in plugin["capabilities"] for cap in required)