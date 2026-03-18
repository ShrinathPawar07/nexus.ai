from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from nexus_ai.api.plugin_router import router as plugin_router

# Initialize FastAPI app
app = FastAPI(
    title="Nexus.AI Plugin API",
    version="1.0.0",
    description="Real-time plugin router for modular verticals in Nexus.AI",
    docs_url="/docs",  # Swagger UI
    redoc_url="/redoc"  # ReDoc UI
)

# Allow cross-origin access (adjust allow_origins in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount plugin router
app.include_router(plugin_router)

# Healthcheck endpoint
@app.get("/health", tags=["Health"])
async def healthcheck():
    return {"status": "ok", "message": "Nexus.AI API is alive"}
