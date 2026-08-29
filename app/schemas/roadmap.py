from typing import Any

from pydantic import BaseModel, Field


class RoadmapRequest(BaseModel):
    company: str = Field(min_length=1, max_length=200)
    role: str = Field(min_length=1, max_length=200)

    match_percentage: float = Field(ge=0, le=100)

    matched_skills: list[str] = Field(default_factory=list)

    missing_skills: list[str] = Field(default_factory=list)


class RoadmapResponse(BaseModel):
    company: str
    role: str
    roadmap_id: str

    match_percentage: float

    matched_skills: list[str]

    missing_skills: list[str]

    estimated_days: int

    total_xp: int

    current_level: dict[str, Any]

    roadmap: list[dict[str, Any]]
