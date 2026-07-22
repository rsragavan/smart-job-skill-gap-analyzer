from fastapi import APIRouter, Depends
from app.core.security import require_roles
from app.models.user import Role, User

from app.db.database import SessionLocal
from app.services.analytics_service import AnalyticsService

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)


@router.get("/top-skills")
def top_skills(_: User = Depends(require_roles(Role.USER))):

    db = SessionLocal()

    try:

        service = AnalyticsService(db)

        return service.get_top_skills()

    finally:
        db.close()


@router.get("/overview")
def analytics_overview(_: User = Depends(require_roles(Role.USER))):

    db = SessionLocal()

    try:

        service = AnalyticsService(db)

        return service.get_overview()

    finally:

        db.close()
