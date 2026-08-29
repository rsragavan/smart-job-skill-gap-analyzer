from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.job_application import (
    ApplicationTimelineEntry,
    CustomApplicationCreate,
    JobApplicationCreate,
    JobApplicationUpdate,
)
from app.services.job_application_service import (
    job_application_service,
)

router = APIRouter(
    prefix="/applications",
    tags=["Job Applications"],
)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
)
def apply_for_job(
    data: JobApplicationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return job_application_service.apply_for_job(
        db=db,
        user_id=current_user.id,
        job_id=data.job_id,
        notes=data.notes,
    )


@router.get("")
def get_my_applications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return job_application_service.get_my_applications(
        db=db,
        user_id=current_user.id,
    )


@router.post("/custom", status_code=status.HTTP_201_CREATED)
def add_custom_application(data: CustomApplicationCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return job_application_service.create_custom_application(db, current_user.id, data)


@router.get("/dashboard")
def application_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return job_application_service.get_dashboard_stats(
        db=db,
        user_id=current_user.id,
    )


@router.patch("/{application_id}")
def update_application(
    application_id: int,
    data: JobApplicationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return job_application_service.update_application(
        db=db,
        application_id=application_id,
        user_id=current_user.id,
        status=data.status,
        notes=data.notes,
        current_selection_round=data.current_selection_round,
        current_round_number=data.current_round_number,
        interview_date=data.interview_date,
    )


@router.delete("/{application_id}")
def delete_application(
    application_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return job_application_service.delete_application(
        db=db,
        application_id=application_id,
        user_id=current_user.id,
    )


@router.get("/{application_id}/timeline", response_model=list[ApplicationTimelineEntry])
def application_timeline(
    application_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return job_application_service.get_timeline(db, application_id, current_user.id)


@router.get("/{application_id}/history")
def application_history(application_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return job_application_service.get_history(db, application_id, current_user.id)
