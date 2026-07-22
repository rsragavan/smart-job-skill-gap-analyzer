from contextlib import asynccontextmanager

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
from app.api.learning_api import router as learning_router
from app.api.resume_api import router as resume_router
from app.api.user_api import router as user_router

from app.core.config import settings
from app.core.security import get_current_user, require_roles
from app.models.user import Role
from app.db.init_db import create_schema
from app.db.database import SessionLocal
from app.scheduler.job_scheduler import DailyJobScheduler
from app.services.technical_skills_engine import skills_engine

logger = logging.getLogger(__name__)
logging.basicConfig(level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO), format="%(asctime)s %(levelname)s %(name)s %(message)s")


@asynccontextmanager
async def lifespan(_: FastAPI):
    if settings.ENVIRONMENT.lower() == "development":
        create_schema()
    with SessionLocal() as db:
        skills_engine.load_approved_skills(db)
    scheduler = None
    if settings.ENABLE_JOB_SCHEDULER:
        scheduler = DailyJobScheduler()
        app.state.job_scheduler = scheduler
        await scheduler.start()
    try:
        yield
    finally:
        if scheduler is not None:
            await scheduler.stop()

app = FastAPI(
    title="Smart Job Skill Gap Analyzer API",
    version="1.0.0",
    lifespan=lifespan,
)
# -----------------------------
# Protected Routes
# -----------------------------
protected = [Depends(require_roles(Role.USER))]

app.include_router(resume_router, dependencies=protected)
app.include_router(job_router, dependencies=[Depends(get_current_user)])
app.include_router(dashboard_router, dependencies=protected)
app.include_router(analytics_router, dependencies=protected)
app.include_router(learning_router, dependencies=protected)
app.include_router(admin_router)
app.include_router(sync_router)

# Public Routes
app.include_router(auth_router)
app.include_router(user_router)

@app.middleware("http")
async def security_headers(request: Request, call_next):
    response = await call_next(request)

    # -----------------------------
    # Security Headers
    # -----------------------------
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"

    # -----------------------------
    # CSP ONLY IN PRODUCTION
    # -----------------------------
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
async def database_exception_handler(_: Request, exc: SQLAlchemyError) -> JSONResponse:
    logger.exception("Unhandled database error", exc_info=exc)
    return JSONResponse(status_code=500, content={"detail": "A database error occurred"})


@app.exception_handler(Exception)
async def unexpected_exception_handler(_: Request, exc: Exception) -> JSONResponse:
    logger.exception("Unhandled application error", exc_info=exc)
    return JSONResponse(status_code=500, content={"detail": "An unexpected server error occurred"})


# Added after the security middleware so CORS is the outermost user middleware,
# including for JSON error responses and browser preflight requests.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in settings.CORS_ORIGINS.split(",")],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)


@app.get("/")
def root():
    return {
        "message": "Smart Job Skill Gap Analyzer API",
        "version": "1.0.0",
        "environment": settings.ENVIRONMENT,
    }
