from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.core.security import require_roles
from app.db.database import get_db
from app.models.user import Role, User
from app.schemas.roadmap import RoadmapResponse
from app.schemas.target import CompanyRoleTargetRequest, CustomTargetRequest, TargetResponse
from app.services.target_service import TargetService
from app.services.company_intelligence_service import company_intelligence_service

router = APIRouter(prefix="/targets", tags=["Targets"])


@router.get("/active", response_model=TargetResponse | None)
def get_active_target(
    user: User = Depends(require_roles(Role.USER)),
    db: Session = Depends(get_db),
):
    return TargetService(db).get_active(user.id)


@router.get("/active/skill-gap")
def active_skill_gap(user: User = Depends(require_roles(Role.USER)), db: Session = Depends(get_db)):
    return TargetService(db).skill_gap(user.id)


@router.get("/active/intelligence")
def get_active_target_intelligence(user: User = Depends(require_roles(Role.USER)), db: Session = Depends(get_db)):
    target = TargetService(db).get_active(user.id)
    if target is None:
        return {"company": None, "role": None, "selection_process": [], "preparation": [], "skills": [], "questions": [], "resources": []}
    return company_intelligence_service.target_intelligence(db, target.company_id, target.company_role_id, target.company, target.role_title)


@router.get("/active/preparation")
def get_active_target_preparation(user: User = Depends(require_roles(Role.USER)), db: Session = Depends(get_db)):
    return company_intelligence_service.preparation_for_active_target(db, user.id) or {"company": None, "role": None, "rounds": [], "questions": []}


@router.post("/from-job/{job_id}", response_model=TargetResponse)
def set_target_from_job(
    job_id: int,
    user: User = Depends(require_roles(Role.USER)),
    db: Session = Depends(get_db),
):
    return TargetService(db).set_from_job(user.id, job_id)


@router.post("/custom", response_model=TargetResponse)
def set_custom_target(
    payload: CustomTargetRequest,
    user: User = Depends(require_roles(Role.USER)),
    db: Session = Depends(get_db),
):
    return TargetService(db).set_custom(user.id, payload)


@router.post("/company-role", response_model=TargetResponse)
def set_company_role_target(payload: CompanyRoleTargetRequest, user: User = Depends(require_roles(Role.USER)), db: Session = Depends(get_db)):
    return TargetService(db).set_company_role(user.id, payload.company_id, payload.role_id)


@router.post("/active/generate-roadmap", response_model=RoadmapResponse)
def generate_active_target_roadmap(
    user: User = Depends(require_roles(Role.USER)),
    db: Session = Depends(get_db),
):
    return TargetService(db).generate_roadmap(user.id)


@router.delete("/active", status_code=status.HTTP_204_NO_CONTENT)
def clear_active_target(
    user: User = Depends(require_roles(Role.USER)),
    db: Session = Depends(get_db),
):
    TargetService(db).clear_active(user.id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
