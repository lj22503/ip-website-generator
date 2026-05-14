"""
SaaS Platform — FastAPI Entry Point
Web platform for Personal IP Website Generator.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI(
    title="IP Website Generator",
    description="Generate personal brand websites with 54 design systems",
    version="0.1.0",
)

# Import and register routes
from saas.api.routes import router as api_router
app.include_router(api_router)


@app.get("/")
async def root():
    return {
        "message": "IP Website Generator API",
        "version": "0.1.0",
        "docs": "/docs",
        "health": "/api/v1/health"
    }


@app.get("/api/v1/health")
async def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
