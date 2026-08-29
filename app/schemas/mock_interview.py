from datetime import datetime

from pydantic import BaseModel, Field


class MockInterviewStart(BaseModel):
    interview_type: str = Field(min_length=2, max_length=40)
    experience_level: str = Field(default="mid", max_length=30)
    company_id: int | None = None
    company_role_id: int | None = None


class InterviewAnswer(BaseModel):
    answer: str = Field(min_length=1, max_length=10000)


class AssessmentStart(BaseModel):
    assessment_id: int


class AssessmentSubmit(BaseModel):
    answers: dict[str, str] = {}


class ContentFilter(BaseModel):
    category: str | None = None
    topic: str | None = None


class InterviewHistoryItem(BaseModel):
    id: int
    company_name: str | None
    role_title: str | None
    interview_type: str
    status: str
    overall_score: int | None
    started_at: datetime
    completed_at: datetime | None
