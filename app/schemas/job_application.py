from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class JobApplicationCreate(BaseModel):
    job_id: int = Field(gt=0)
    notes: str | None = Field(default=None, max_length=1000)


class JobApplicationUpdate(BaseModel):
    status: str | None = Field(default=None, max_length=30)
    notes: str | None = Field(default=None, max_length=1000)
    current_selection_round: str | None = Field(default=None, max_length=150)
    current_round_number: int | None = Field(default=None, ge=1)
    interview_date: datetime | None = None


class CustomApplicationCreate(BaseModel):
    company_name: str = Field(min_length=1, max_length=255)
    job_title: str = Field(min_length=1, max_length=255)
    location: str | None = Field(default=None, max_length=255)
    job_url: str | None = Field(default=None, max_length=500)
    applied_at: datetime | None = None
    status: str = Field(default="Applied", max_length=30)
    notes: str | None = Field(default=None, max_length=1000)
    interview_date: datetime | None = None


class JobApplicationResponse(BaseModel):
    id: int
    job_id: int
    user_id: int

    job_title: str
    company: str
    location: str
    job_url: str

    status: str
    notes: str | None

    applied_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ApplicationTimelineEntry(BaseModel):
    id: int
    status: str
    notes: str | None
    progress_percentage: int
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
