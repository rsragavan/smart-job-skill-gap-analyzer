from fastapi import APIRouter

from app.schemas.roadmap import (
    RoadmapRequest,
    RoadmapResponse,
)

from app.services.roadmap_service import roadmap_service

router = APIRouter(
    prefix="/roadmap",
    tags=["Roadmap"],
)


@router.post(
    "/generate",
    response_model=RoadmapResponse,
)
def generate_roadmap(request: RoadmapRequest):

    return roadmap_service.generate(
        company=request.company,
        role=request.role,
        match_percentage=request.match_percentage,
        matched_skills=request.matched_skills,
        missing_skills=request.missing_skills,
    )