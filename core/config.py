# nexus_ai/core/config.py

class Config:
    VERSION = "0.1.0"
    LOG_LEVEL = "INFO"
    ENABLE_LOGGING = True
    ENABLE_API_MOCK = True  # Toggle for dummy API enrichment
    SUPPORTED_CONTEXTS = ["fintech", "edtech"]
    TIMEOUT = 5  # Seconds for API calls
