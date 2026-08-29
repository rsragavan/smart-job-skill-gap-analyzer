from typing import Any, Literal

from pydantic import BaseModel, Field


ProgressStatus = Literal["not_started", "in_progress", "completed"]


class LearningProgressSyncRequest(BaseModel):
    roadmap_id: str = Field(min_length=8, max_length=64)
    roadmap: list[dict[str, Any]] = Field(default_factory=list)


class LearningProgressUpdateRequest(BaseModel):
    skill_key: str = Field(min_length=1, max_length=120)
    item_type: Literal["topic", "project", "mission"]
    item_key: str = Field(min_length=1, max_length=180)
    status: ProgressStatus
