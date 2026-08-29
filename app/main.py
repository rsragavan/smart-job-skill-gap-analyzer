import logging

from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

from app.api.admin_api import router as admin_router, sync_router
from app.api.analytics_api import router as analytics_router
from app.api.auth_api import router as auth_router
from app.api.dashboard_api import router as dashboard_router
from app.api.job_api import router as job_router
from app.api.job_application_api import router as job_application_router
from app.api.learning_api import router as learning_router
from app.api.career_gps_api import router as career_gps_router
from app.api.company_intelligence_api import company_target_router, public_router as companies_router, router as company_intelligence_router, startup_router
from app.api.resume_api import router as resume_router
from app.api.user_api import router as user_router

from app.api.roadmap_api import router as roadmap_router
from app.api.target_api import router as target_router
from app.api.mock_interview_api import assessment_router, router as mock_interview_router
from app.api.content_api import router as content_router
from app.api.coding_practice_api import router as coding_practice_router

from app.core.config import settings
from app.core.security import get_current_user, require_roles
from app.models.user import Role

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO),
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)


app = FastAPI(
    title="Smart Job Skill Gap Analyzer API",
    version="1.0.0",
)

# ======================================================
# Protected Routes
# ======================================================

protected = [Depends(require_roles(Role.USER))]

app.include_router(
    resume_router,
    dependencies=protected,
)

app.include_router(
    roadmap_router,
    dependencies=protected,
)
app.include_router(
    target_router,
    dependencies=protected,
)
app.include_router(
    career_gps_router,
    dependencies=protected,
)

app.include_router(
    job_router,
    dependencies=[Depends(get_current_user)],
)

app.include_router(
    job_application_router,
    dependencies=[Depends(get_current_user)],
)
app.include_router(company_intelligence_router, dependencies=[Depends(get_current_user)])
app.include_router(companies_router, dependencies=[Depends(get_current_user)])
app.include_router(startup_router, dependencies=[Depends(get_current_user)])
app.include_router(company_target_router, dependencies=[Depends(get_current_user)])

app.include_router(
    dashboard_router,
    dependencies=protected,
)

app.include_router(
    analytics_router,
    dependencies=protected,
)

app.include_router(
    learning_router,
    dependencies=protected,
)
app.include_router(mock_interview_router, dependencies=protected)
app.include_router(assessment_router, dependencies=protected)
app.include_router(content_router)
app.include_router(coding_practice_router)

app.include_router(admin_router)
app.include_router(sync_router)

# ======================================================
# Public Routes
# ======================================================

app.include_router(auth_router)
app.include_router(user_router)


@app.middleware("http")
async def security_headers(request: Request, call_next):
    response = await call_next(request)

    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = (
        "camera=(), microphone=(), geolocation=()"
    )

    if settings.ENVIRONMENT.lower() == "production":
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self'; "
            "style-src 'self'; "
            "img-src 'self' data:; "
            "connect-src 'self'; "
            "font-src 'self'; "
            "frame-ancestors 'none'; "
            "base-uri 'self'; "
            "form-action 'self';"
        )

    return response


@app.exception_handler(SQLAlchemyError)
async def database_exception_handler(
    _: Request,
    exc: SQLAlchemyError,
):
    logger.exception(
        "Unhandled database error",
        exc_info=exc,
    )

    return JSONResponse(
        status_code=500,
        content={
            "detail": "A database error occurred"
        },
    )


@app.exception_handler(Exception)
async def unexpected_exception_handler(
    _: Request,
    exc: Exception,
):
    logger.exception(
        "Unhandled application error",
        exc_info=exc,
    )

    return JSONResponse(
        status_code=500,
        content={
            "detail": "An unexpected server error occurred"
        },
    )


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        origin.strip()
        for origin in settings.CORS_ORIGINS.split(",")
    ],
    allow_credentials=True,
    allow_methods=[
        "GET",
        "POST",
        "PUT",
        "PATCH",
        "DELETE",
        "OPTIONS",
    ],
    allow_headers=[
        "Authorization",
        "Content-Type",
    ],
)


@app.get("/")
def root():
    return {
        "message": "Smart Job Skill Gap Analyzer API",
        "version": "1.0.0",
        "environment": settings.ENVIRONMENT,
    }


@app.get("/health", tags=["System"])
def health():
    return {"status": "ok"}
