"""
SaaS API Routes
FastAPI routes for the web platform.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

router = APIRouter(prefix="/api/v1")


class GenerateRequest(BaseModel):
    product: str  # "portfolio" or "personal_site"
    design: str  # design system name e.g. "linear.app"
    content: Dict[str, Any]
    selected_modules: List[str]
    mbti: Optional[str] = None


class GenerateResponse(BaseModel):
    id: str
    status: str
    html_url: Optional[str] = None


@router.post("/generate", response_model=GenerateResponse)
async def generate_website(req: GenerateRequest):
    """Generate a personal IP website."""
    # TODO: Implement actual generation
    return GenerateResponse(
        id="demo-123",
        status="ready",
        html_url="/output/demo.html"
    )


@router.get("/designs")
async def list_designs():
    """List all available design systems."""
    from skill.design_systems.registry import DESIGN_SYSTEMS
    return {"designs": list(DESIGN_SYSTEMS.keys())}


@router.get("/designs/{design_name}")
async def get_design(design_name: str):
    """Get details for a specific design system."""
    from skill.design_systems.registry import DESIGN_SYSTEMS
    if design_name not in DESIGN_SYSTEMS:
        raise HTTPException(status_code=404, detail="Design not found")
    return DESIGN_SYSTEMS[design_name]


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok"}
