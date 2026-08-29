from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.security import require_roles
from app.db.database import get_db
from app.models.user import Role, User
from app.services.career_gps_service import CareerGPSService

router = APIRouter(prefix="/career-gps", tags=["Career GPS"])


@router.get("")
def get_career_gps(user: User = Depends(require_roles(Role.USER)), db: Session = Depends(get_db)):
    return CareerGPSService(db).get_dashboard(user.id)


@router.get("/coach")
def get_ai_career_coach(user: User = Depends(require_roles(Role.USER)), db: Session = Depends(get_db)):
    return CareerGPSService(db).get_dashboard(user.id)


@router.patch("/goals")
def update_career_goals(payload: dict[str, str | None], user: User = Depends(require_roles(Role.USER)), db: Session = Depends(get_db)):
    return CareerGPSService(db).update_goals(user.id, payload)
