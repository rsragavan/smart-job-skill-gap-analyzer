from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import require_roles
from app.db.database import get_db
from app.models.user import Role, User
from app.schemas.learning import LearningProgressSyncRequest, LearningProgressUpdateRequest
from app.services.learning_service import LearningService
from app.services.learning_progress_service import LearningProgressService
from app.services.gamification_service import GamificationService

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


@router.post("/progress/sync")
def sync_learning_progress(
    request: LearningProgressSyncRequest,
    user: User = Depends(require_roles(Role.USER)),
    db: Session = Depends(get_db),
):
    return LearningProgressService(db).sync(user.id, request.roadmap_id, request.roadmap)


@router.get("/progress/{roadmap_id}")
def get_learning_progress(
    roadmap_id: str,
    user: User = Depends(require_roles(Role.USER)),
    db: Session = Depends(get_db),
):
    return LearningProgressService(db).get_progress(user.id, roadmap_id)


@router.get("/gamification")
def get_gamification(
    user: User = Depends(require_roles(Role.USER)),
    db: Session = Depends(get_db),
):
    result = GamificationService(db).dashboard(user.id)
    db.commit()
    return result


@router.patch("/progress/{roadmap_id}")
def update_learning_progress(
    roadmap_id: str,
    request: LearningProgressUpdateRequest,
    user: User = Depends(require_roles(Role.USER)),
    db: Session = Depends(get_db),
):
    try:
        return LearningProgressService(db).update(
            user.id,
            roadmap_id,
            request.skill_key,
            request.item_type,
            request.item_key,
            request.status,
        )
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except PermissionError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
