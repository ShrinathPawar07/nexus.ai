# nexus_ai/utils/context_detector.py

def detect_context(query: str) -> str:
    query = query.lower()
    
    if any(term in query for term in ["revenue", "finance", "risk"]):
        return "fintech"
    elif any(term in query for term in ["student", "course", "learn"]):
        return "edtech"
    elif any(term in query for term in ["symptom", "report", "vital", "diagnose"]):
        return "healthcare"
    elif any(term in query for term in ["sensor", "vehicle", "automotive", "diagnostic"]):
        return "automotive"
    
    return "unknown"
