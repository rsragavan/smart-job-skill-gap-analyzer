import logging

from sqlalchemy import inspect, text
from sqlalchemy.exc import SQLAlchemyError

from app.db.database import Base, engine

logger = logging.getLogger(__name__)


def create_schema() -> None:
    """Register every model before creating development tables from shared metadata."""
    from app.models.auth import PasswordResetToken, RefreshToken
    from app.models.company import Company
    from app.models.job import Job
    from app.models.resume_history import ResumeHistory
    from app.models.unknown_skill import UnknownSkill
    from app.models.user import User

    _ = (Company, Job, PasswordResetToken, RefreshToken, ResumeHistory, UnknownSkill, User)
    Base.metadata.create_all(bind=engine)
    _ensure_resume_history_columns()
    _ensure_job_status_columns()


def _remove_obsolete_auth_schema() -> None:
    """Remove authentication structures that belonged to the previous flow.

    This project creates its schema automatically in development.  Keeping this
    migration here lets an existing college-project database move to the
    simplified model without manual SQL.  It intentionally runs only for
    PostgreSQL, the application's configured database.
    """
    if engine.dialect.name != "postgresql":
        return

    inspector = inspect(engine)
    tables = set(inspector.get_table_names())
    user_columns = {column["name"] for column in inspector.get_columns("users")} if "users" in tables else set()
    obsolete_tables = ("email_verification_tokens", "audit_logs")
    obsolete_columns = {
        "provider",
        "provider_id",
        "avatar_url",
        "email_verified",
        "is_verified",
        "failed_login_attempts",
        "locked_until",
    }
    try:
        with engine.begin() as connection:
            # Do not prevent the development server from starting if another
            # local process is still connected to an old table.
            connection.execute(text("SET LOCAL lock_timeout = '2s'"))
            for table in obsolete_tables:
                if table in tables:
                    connection.execute(text(f"DROP TABLE {table}"))

            if user_columns:
                for column in obsolete_columns & user_columns:
                    connection.execute(text(f"ALTER TABLE users DROP COLUMN {column}"))
    except SQLAlchemyError:
        logger.warning("Could not yet remove obsolete authentication schema because it is locked. It will retry on the next development startup.")
    else:
        logger.info("Removed obsolete authentication tables and columns.")


def _ensure_resume_history_columns() -> None:
    """Bring the pre-existing resume table in line with its SQLAlchemy model."""
    columns = {column["name"] for column in inspect(engine).get_columns("resume_history")}
    statements: list[str] = []
    if "user_id" not in columns:
        statements.append("ALTER TABLE resume_history ADD COLUMN user_id INTEGER REFERENCES users(id) ON DELETE CASCADE")
    if "content_hash" not in columns:
        statements.append("ALTER TABLE resume_history ADD COLUMN content_hash VARCHAR(64)")

    if not statements:
        return

    with engine.begin() as connection:
        for statement in statements:
            connection.execute(text(statement))
        connection.execute(text("CREATE INDEX IF NOT EXISTS ix_resume_history_user_id ON resume_history (user_id)"))
        connection.execute(text("CREATE INDEX IF NOT EXISTS ix_resume_history_content_hash ON resume_history (content_hash)"))
    logger.info("Updated resume_history schema for user-owned resume records.")


def _ensure_job_status_columns() -> None:
    """Add job lifecycle fields to databases created before status tracking."""
    columns = {column["name"] for column in inspect(engine).get_columns("jobs")}
    statements: list[str] = []
    if "status" not in columns:
        statements.append("ALTER TABLE jobs ADD COLUMN status VARCHAR(8) NOT NULL DEFAULT 'ACTIVE'")
    if "inactive_at" not in columns:
        statements.append("ALTER TABLE jobs ADD COLUMN inactive_at TIMESTAMP WITH TIME ZONE")

    if not statements:
        return

    with engine.begin() as connection:
        for statement in statements:
            connection.execute(text(statement))
        connection.execute(text("CREATE INDEX IF NOT EXISTS ix_jobs_status ON jobs (status)"))
    logger.info("Updated jobs schema with active/inactive status tracking.")
