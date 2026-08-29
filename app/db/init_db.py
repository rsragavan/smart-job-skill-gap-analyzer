import logging

from sqlalchemy import inspect, text
from sqlalchemy.exc import SQLAlchemyError

from app.db.database import Base, engine

logger = logging.getLogger(__name__)


def create_schema() -> None:
    """Register every model before creating development tables from shared metadata."""
    from app.models.auth import PasswordResetToken, RefreshToken
    from app.models.company import Company
    from app.models.company_intelligence import CompanyInsight, CompanyInterviewQuestion, CompanyLocation, CompanyPreparation, CompanyResource, CompanyRole, CompanySelectionProcess, CompanySkill, StartupFunding, StartupInformation, StartupRole
    from app.models.mock_interview import AssessmentAttempt, CodingAssessment, CodingAttempt, MockInterview, MockInterviewQuestion
    from app.models.job import Job
    from app.models.learning_progress import LearningProgress
    from app.models.content import CodingQuestion, InterviewQuestion, LearningResource
    from app.models.content_seed import seed_content
    from app.models.gamification import Achievement, GamificationEvent, UserBadge, UserGamification
    from app.models.career_gps import CareerGoal, CareerProgress
    from app.models.resume_history import ResumeHistory
    from app.models.unknown_skill import UnknownSkill
    from app.models.user import User
    from app.models.user_target import UserTarget
    from app.models.admin import AdminActivityLog, SystemSetting

    from app.models.job_application import ApplicationStageHistory, ApplicationTimeline, JobApplication
    _ = (Company, CompanyLocation, CompanyRole, CompanySelectionProcess, CompanyPreparation, CompanySkill, CompanyInterviewQuestion, CompanyResource, CompanyInsight, StartupInformation, StartupFunding, StartupRole, MockInterview, MockInterviewQuestion, CodingAssessment, AssessmentAttempt, CodingAttempt, CodingQuestion, InterviewQuestion, LearningResource, Job, JobApplication, ApplicationTimeline, ApplicationStageHistory, LearningProgress, Achievement, GamificationEvent, UserBadge, UserGamification, CareerGoal, CareerProgress, PasswordResetToken, RefreshToken, ResumeHistory, UnknownSkill, User, UserTarget, AdminActivityLog, SystemSetting)
    Base.metadata.create_all(bind=engine)
    _ensure_interview_question_columns()
    _ensure_mock_interview_question_columns()
    _ensure_coding_question_columns()
    from sqlalchemy.orm import Session
    with Session(engine) as session:
        seed_content(session)
    _ensure_resume_history_columns()
    _ensure_job_status_columns()
    _ensure_company_intelligence_columns()
    _ensure_application_tracking_columns()
    _ensure_target_company_role_columns()
    _ensure_selection_process_columns()
    _ensure_startup_information_columns()
    _ensure_startup_ingestion_columns()
    _ensure_assessment_attempt_columns()
    _ensure_performance_indexes()


def _ensure_performance_indexes() -> None:
    """Create additive indexes for the high-volume list and analytics queries."""
    statements = (
        "CREATE INDEX IF NOT EXISTS ix_jobs_company ON jobs (company)",
        "CREATE INDEX IF NOT EXISTS ix_jobs_title ON jobs (title)",
        "CREATE INDEX IF NOT EXISTS ix_jobs_created_at ON jobs (created_at)",
        "CREATE INDEX IF NOT EXISTS ix_job_applications_status ON job_applications (status)",
        "CREATE INDEX IF NOT EXISTS ix_job_applications_applied_at ON job_applications (applied_at)",
    )
    with engine.begin() as connection:
        existing_tables = set(inspect(engine).get_table_names())
        for statement in statements:
            table = statement.split(" ON ", 1)[1].split(" ", 1)[0]
            if table in existing_tables:
                connection.execute(text(statement))


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
    if "ats_analysis" not in columns:
        statements.append("ALTER TABLE resume_history ADD COLUMN ats_analysis JSONB")
    if "storage_path" not in columns:
        statements.append("ALTER TABLE resume_history ADD COLUMN storage_path VARCHAR(500)")

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


def _ensure_company_intelligence_columns() -> None:
    """Add optional profile fields without disrupting the existing company feed."""
    columns = {column["name"] for column in inspect(engine).get_columns("companies")}
    additions = {
        "logo_url": "VARCHAR(500)", "industry": "VARCHAR(150)", "headquarters": "VARCHAR(150)",
        "founded_year": "INTEGER", "country": "VARCHAR(120)", "company_size": "VARCHAR(100)", "website_url": "VARCHAR(500)",
        "public_email": "VARCHAR(255)", "linkedin_url": "VARCHAR(500)", "description": "TEXT",
        "tech_stack": "TEXT", "hiring_status": "VARCHAR(80)", "internship_available": "BOOLEAN DEFAULT FALSE",
        "freshers_hiring": "BOOLEAN DEFAULT FALSE", "office_locations": "TEXT", "products": "TEXT", "business_domains": "TEXT", "remote_policy": "VARCHAR(150)", "culture_summary": "TEXT", "data_source_url": "VARCHAR(500)", "last_verified_at": "TIMESTAMP WITH TIME ZONE", "verification_status": "VARCHAR(30) NOT NULL DEFAULT 'Unverified'",
    }
    with engine.begin() as connection:
        for name, definition in additions.items():
            if name not in columns:
                connection.execute(text(f"ALTER TABLE companies ADD COLUMN {name} {definition}"))


def _ensure_application_tracking_columns() -> None:
    """Safely extend the legacy scraped-only application table."""
    columns = {column["name"] for column in inspect(engine).get_columns("job_applications")}
    additions = {"source_type": "VARCHAR(20) NOT NULL DEFAULT 'scraped'", "company_id": "INTEGER REFERENCES companies(id) ON DELETE SET NULL", "company_role_id": "INTEGER REFERENCES company_roles(id) ON DELETE SET NULL", "current_selection_round": "VARCHAR(150)", "current_round_number": "INTEGER", "interview_date": "TIMESTAMP WITH TIME ZONE", "custom_company_name": "VARCHAR(255)", "custom_job_title": "VARCHAR(255)", "custom_location": "VARCHAR(255)", "custom_job_url": "VARCHAR(500)"}
    with engine.begin() as connection:
        for name, definition in additions.items():
            if name not in columns:
                connection.execute(text(f"ALTER TABLE job_applications ADD COLUMN {name} {definition}"))
        connection.execute(text("ALTER TABLE job_applications ALTER COLUMN job_id DROP NOT NULL"))
        connection.execute(text("CREATE INDEX IF NOT EXISTS ix_job_applications_source_type ON job_applications (source_type)"))


def _ensure_target_company_role_columns() -> None:
    columns = {column["name"] for column in inspect(engine).get_columns("user_targets")}
    with engine.begin() as connection:
        if "company_id" not in columns:
            connection.execute(text("ALTER TABLE user_targets ADD COLUMN company_id INTEGER REFERENCES companies(id) ON DELETE SET NULL"))
            connection.execute(text("CREATE INDEX IF NOT EXISTS ix_user_targets_company_id ON user_targets (company_id)"))
        if "company_role_id" not in columns:
            connection.execute(text("ALTER TABLE user_targets ADD COLUMN company_role_id INTEGER REFERENCES company_roles(id) ON DELETE SET NULL"))
            connection.execute(text("CREATE INDEX IF NOT EXISTS ix_user_targets_company_role_id ON user_targets (company_role_id)"))


def _ensure_selection_process_columns() -> None:
    """Keep role-specific process metadata additive for existing installations."""
    role_columns = {column["name"] for column in inspect(engine).get_columns("company_roles")}
    round_columns = {column["name"] for column in inspect(engine).get_columns("company_selection_process")}
    with engine.begin() as connection:
        if "required_skills" not in role_columns:
            connection.execute(text("ALTER TABLE company_roles ADD COLUMN required_skills TEXT"))
        for name, definition in {"purpose": "TEXT", "preparation_topics": "TEXT", "source_url": "VARCHAR(500)", "last_verified_at": "TIMESTAMP WITH TIME ZONE", "verification_status": "VARCHAR(30) NOT NULL DEFAULT 'Unverified'"}.items():
            if name not in round_columns:
                connection.execute(text(f"ALTER TABLE company_selection_process ADD COLUMN {name} {definition}"))


def _ensure_startup_information_columns() -> None:
    """Upgrade early startup tables with later verification and location fields."""
    columns = {column["name"] for column in inspect(engine).get_columns("startup_information")}
    additions = {
        "state": "VARCHAR(100)",
        "country": "VARCHAR(120)",
        "founders": "TEXT",
        "products": "TEXT",
        "growth_stage": "VARCHAR(80)",
        "culture_summary": "TEXT",
        "preparation_tips": "TEXT",
        "hiring_status": "VARCHAR(80)",
        "source_url": "VARCHAR(500)",
        "last_verified_at": "TIMESTAMP WITH TIME ZONE",
    }
    with engine.begin() as connection:
        for name, definition in additions.items():
            if name not in columns:
                connection.execute(text(f"ALTER TABLE startup_information ADD COLUMN {name} {definition}"))
                logger.info("Added startup_information.%s", name)


def _ensure_assessment_attempt_columns() -> None:
    """Add assessment result fields introduced after the original schema."""
    columns = {column["name"] for column in inspect(engine).get_columns("assessment_attempts")}
    if "percentage" not in columns:
        with engine.begin() as connection:
            connection.execute(text("ALTER TABLE assessment_attempts ADD COLUMN percentage INTEGER"))
        logger.info("Updated assessment_attempts schema with percentage result field.")


def _ensure_coding_question_columns() -> None:
    """Add every model column missing from a pre-existing coding_questions table."""
    inspector = inspect(engine)
    if "coding_questions" not in inspector.get_table_names():
        return
    columns = {column["name"] for column in inspector.get_columns("coding_questions")}
    from app.models.content import CodingQuestion
    additions = {
        column.name: column.type.compile(dialect=engine.dialect)
        for column in CodingQuestion.__table__.columns
        if column.name not in columns
    }
    statements = [f"ALTER TABLE coding_questions ADD COLUMN IF NOT EXISTS {name} {definition}" for name, definition in additions.items()]
    if not statements:
        return
    with engine.begin() as connection:
        for statement in statements:
            connection.execute(text(statement))
    logger.info("Updated coding_questions schema with IDE metadata.")


def _ensure_interview_question_columns() -> None:
    """Add additive metadata columns for skill-aware interview selection."""
    inspector = inspect(engine)
    if "interview_questions" not in inspector.get_table_names():
        return
    columns = {column["name"] for column in inspector.get_columns("interview_questions")}
    from app.models.content import InterviewQuestion
    additions = {
        column.name: column.type.compile(dialect=engine.dialect)
        for column in InterviewQuestion.__table__.columns
        if column.name not in columns
    }
    if not additions:
        return
    with engine.begin() as connection:
        for name, definition in additions.items():
            connection.execute(text(f"ALTER TABLE interview_questions ADD COLUMN IF NOT EXISTS {name} {definition}"))
    logger.info("Updated interview_questions schema with skill metadata.")


def _ensure_mock_interview_question_columns() -> None:
    """Keep started-interview snapshots compatible with newer question metadata."""
    inspector = inspect(engine)
    if "mock_interview_questions" not in inspector.get_table_names():
        return
    columns = {column["name"] for column in inspector.get_columns("mock_interview_questions")}
    from app.models.mock_interview import MockInterviewQuestion
    additions = {
        column.name: column.type.compile(dialect=engine.dialect)
        for column in MockInterviewQuestion.__table__.columns
        if column.name not in columns
    }
    if not additions:
        return
    with engine.begin() as connection:
        for name, definition in additions.items():
            connection.execute(text(f"ALTER TABLE mock_interview_questions ADD COLUMN IF NOT EXISTS {name} {definition}"))
    logger.info("Updated mock_interview_questions schema with skill snapshots.")


def _ensure_startup_ingestion_columns() -> None:
    """Add nullable ingestion metadata without rewriting existing startup data."""
    columns = {column["name"] for column in inspect(engine).get_columns("startup_information")}
    additions = {
        "slug": "VARCHAR(180)",
        "source_name": "VARCHAR(120)",
        "verification_status": "VARCHAR(20)",
    }
    with engine.begin() as connection:
        for name, definition in additions.items():
            if name not in columns:
                connection.execute(text(f"ALTER TABLE startup_information ADD COLUMN {name} {definition}"))
        connection.execute(text("ALTER TABLE startup_information ALTER COLUMN open_positions DROP NOT NULL"))
        connection.execute(text("CREATE INDEX IF NOT EXISTS ix_startup_information_verification_status ON startup_information (verification_status)"))
