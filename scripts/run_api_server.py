# scripts/run_api_server.py

import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "nexus_ai.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        workers=1
    )
