from fastapi import APIRouter, Depends
from app.core.security import require_roles
from app.models.user import Role, User

from app.db.database import SessionLocal
from app.services.dashboard_service import DashboardService

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get("/")
def dashboard(_: User = Depends(require_roles(Role.USER))):

    db = SessionLocal()

    try:

        service = DashboardService(db)

        return service.get_dashboard()

    finally:
        db.close()
