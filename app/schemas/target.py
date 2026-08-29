from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class CustomTargetRequest(BaseModel):
    company: str = Field(min_length=1, max_length=200)
    role: str = Field(min_length=1, max_length=200)
    job_description: str = Field(min_length=20, max_length=50000)
    location: str | None = Field(default=None, max_length=200)


class CompanyRoleTargetRequest(BaseModel):
    company_id: int = Field(gt=0)
    role_id: int = Field(gt=0)


class TargetResponse(BaseModel):
    id: int
    source_type: Literal["scraped", "custom"]
    job_id: int | None = None
    company_id: int | None = None
    company_role_id: int | None = None
    company: str
    role_title: str
    location: str | None = None
    job_description: str | None = None
    match_percentage: float
    matched_skills: list[str]
    missing_skills: list[str]
    missing_skill_details: list[dict] = Field(default_factory=list)
    skill_gap_explanations: dict[str, str] = Field(default_factory=dict)
    roadmap_id: str | None = None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
