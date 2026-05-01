from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api import routes, websockets

# Lifespan context manager for startup and shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("[SYSTEM] Booting Digital Twin Orchestrator...")
    # TODO: Initialize Vector DB connection here
    # TODO: Verify connection to Celery/Redis broker here
    yield
    print("[SYSTEM] Shutting down Orchestrator. Securing data...")
    # TODO: Close DB connections and clear temporary RAM

# Initialize the application
app = FastAPI(
    title="Digital Twin Matchmaker API",
    description="Asynchronous backend for LLM-driven dating simulations",
    version="1.0.0",
    lifespan=lifespan
)

# Include routing for standard REST endpoints (Data Ingestion, Dashboards, Match Drops)
app.include_router(routes.router, prefix="/api/v1")

# Include routing for Human-to-Human WebSockets
app.include_router(websockets.router, prefix="/ws/v1")

@app.get("/health")
async def health_check():
    return {"status": "online", "message": "Orchestrator is running."}

if __name__ == "__main__":
    import uvicorn
    # Running on standard local port, ready for async traffic
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)