from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from io import BytesIO
import json
import fitz
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


@router.get("/dashboard")
def analytics_dashboard(
    company: str | None = Query(default=None),
    role: str | None = Query(default=None),
    skill: str | None = Query(default=None),
    date_from: str | None = Query(default=None),
    date_to: str | None = Query(default=None),
    user: User = Depends(require_roles(Role.USER)),
):
    db = SessionLocal()
    try:
        return AnalyticsService(db).get_dashboard(user.id, company, role, skill, date_from, date_to)
    finally:
        db.close()


@router.get("/placement")
def placement_analytics(user: User = Depends(require_roles(Role.USER))):
    db = SessionLocal()
    try:
        return AnalyticsService(db).get_placement_analytics(user.id)
    finally:
        db.close()


@router.get("/notifications")
def analytics_notifications(user: User = Depends(require_roles(Role.USER))):
    db = SessionLocal()
    try:
        return AnalyticsService(db).get_notifications(user.id)
    finally:
        db.close()


@router.get("/placement/report")
def placement_report(report_type: str = Query(default="placement"), user: User = Depends(require_roles(Role.USER))):
    db = SessionLocal()
    try:
        report = AnalyticsService(db).get_placement_analytics(user.id)
    finally:
        db.close()
    body = report.get({"skill": "skills", "application": "applications", "interview": "interviews", "learning": "readiness", "dashboard": "readiness"}.get(report_type, "readiness"), report)
    document = fitz.open(); page = document.new_page(); page.insert_text((45, 55), f"Placement Analytics Report\n\n{json.dumps(body, indent=2, default=str)[:9000]}", fontsize=9); payload = document.tobytes(); document.close()
    return StreamingResponse(BytesIO(payload), media_type="application/pdf", headers={"Content-Disposition": f"attachment; filename={report_type}-report.pdf"})
