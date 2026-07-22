from fastapi import APIRouter, Depends, HTTPException
from app.core.security import require_roles
from app.models.user import Role, User

from app.services.learning_service import LearningService

router = APIRouter(
    prefix="/learning",
    tags=["Learning"]
)

@router.post("/job/{job_id}")
def generate_learning_roadmap(job_id: int, user: User = Depends(require_roles(Role.USER))):
    """
    Generate a learning roadmap for a selected job.
    """

    result = LearningService().generate_learning_plan(job_id, user_id=user.id)

    if "error" in result:
        raise HTTPException(
            status_code=404,
            detail=result["error"]
        )

    return result
