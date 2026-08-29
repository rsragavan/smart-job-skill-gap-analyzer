from datetime import UTC, datetime

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class CompanyRole(Base):
    __tablename__ = "company_roles"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id", ondelete="CASCADE"), index=True)
    title: Mapped[str] = mapped_column(String(150), index=True)
    description: Mapped[str | None] = mapped_column(Text)
    is_open: Mapped[bool] = mapped_column(Boolean, default=False)
    required_skills: Mapped[str | None] = mapped_column(Text)


class CompanyLocation(Base):
    __tablename__ = "company_locations"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id", ondelete="CASCADE"), index=True)
    city: Mapped[str] = mapped_column(String(120), index=True)
    state: Mapped[str | None] = mapped_column(String(120), index=True)
    country: Mapped[str] = mapped_column(String(120), default="India")
    is_tamil_nadu: Mapped[bool] = mapped_column(Boolean, default=False)


class CompanyPreparation(Base):
    __tablename__ = "company_preparation"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    company_role_id: Mapped[int | None] = mapped_column(ForeignKey("company_roles.id", ondelete="CASCADE"), nullable=True, index=True)
    topic: Mapped[str] = mapped_column(String(200))
    category: Mapped[str] = mapped_column(String(80))
    learning_order: Mapped[int] = mapped_column(Integer, default=1)
    resource_url: Mapped[str | None] = mapped_column(String(500))
    source_url: Mapped[str | None] = mapped_column(String(500))


class CompanySelectionProcess(Base):
    __tablename__ = "company_selection_process"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    company_role_id: Mapped[int] = mapped_column(ForeignKey("company_roles.id", ondelete="CASCADE"), index=True)
    round_number: Mapped[int] = mapped_column(Integer)
    title: Mapped[str] = mapped_column(String(150))
    description: Mapped[str | None] = mapped_column(Text)
    expected_duration: Mapped[str | None] = mapped_column(String(100))
    difficulty: Mapped[str | None] = mapped_column(String(30))
    interview_mode: Mapped[str | None] = mapped_column(String(30))
    freshers_eligible: Mapped[bool] = mapped_column(Boolean, default=True)
    purpose: Mapped[str | None] = mapped_column(Text)
    preparation_topics: Mapped[str | None] = mapped_column(Text)
    source_url: Mapped[str | None] = mapped_column(String(500))
    last_verified_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    verification_status: Mapped[str] = mapped_column(String(30), default="Unverified")


class CompanySkill(Base):
    __tablename__ = "company_skills"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id", ondelete="CASCADE"), index=True)
    skill: Mapped[str] = mapped_column(String(120), index=True)
    importance: Mapped[str] = mapped_column(String(30), default="Preferred")


class CompanyInterviewQuestion(Base):
    __tablename__ = "company_interview_questions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    company_role_id: Mapped[int] = mapped_column(ForeignKey("company_roles.id", ondelete="CASCADE"), index=True)
    category: Mapped[str] = mapped_column(String(50))
    question: Mapped[str] = mapped_column(Text)
    difficulty: Mapped[str | None] = mapped_column(String(30))
    preparation_tip: Mapped[str | None] = mapped_column(Text)


class CompanyResource(Base):
    __tablename__ = "company_resources"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    company_role_id: Mapped[int] = mapped_column(ForeignKey("company_roles.id", ondelete="CASCADE"), index=True)
    title: Mapped[str] = mapped_column(String(200))
    url: Mapped[str] = mapped_column(String(500))
    resource_type: Mapped[str] = mapped_column(String(50), default="Article")


class CompanyInsight(Base):
    __tablename__ = "company_insights"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id", ondelete="CASCADE"), unique=True)
    average_hiring_time: Mapped[str | None] = mapped_column(String(100))
    interview_difficulty: Mapped[str | None] = mapped_column(String(30))
    hiring_frequency: Mapped[str | None] = mapped_column(String(100))
    remote_jobs: Mapped[bool] = mapped_column(Boolean, default=False)
    hybrid_jobs: Mapped[bool] = mapped_column(Boolean, default=False)
    office_jobs: Mapped[bool] = mapped_column(Boolean, default=True)
    graduate_hiring: Mapped[bool] = mapped_column(Boolean, default=False)
    internship_available: Mapped[bool] = mapped_column(Boolean, default=False)
    last_updated: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))


class StartupInformation(Base):
    __tablename__ = "startup_information"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(150), unique=True, index=True)
    industry: Mapped[str] = mapped_column(String(150), index=True)
    location: Mapped[str] = mapped_column(String(150), index=True)
    funding_stage: Mapped[str | None] = mapped_column(String(50))
    latest_funding_amount: Mapped[str | None] = mapped_column(String(100))
    funding_date: Mapped[Date | None] = mapped_column(Date)
    investors: Mapped[str | None] = mapped_column(Text)
    founded_year: Mapped[int | None] = mapped_column(Integer)
    employees: Mapped[str | None] = mapped_column(String(100))
    website_url: Mapped[str | None] = mapped_column(String(500))
    careers_url: Mapped[str | None] = mapped_column(String(500))
    public_email: Mapped[str | None] = mapped_column(String(255))
    open_positions: Mapped[int | None] = mapped_column(Integer, nullable=True)
    tech_stack: Mapped[str | None] = mapped_column(Text)
    description: Mapped[str | None] = mapped_column(Text)
    founders: Mapped[str | None] = mapped_column(Text)
    products: Mapped[str | None] = mapped_column(Text)
    growth_stage: Mapped[str | None] = mapped_column(String(80))
    culture_summary: Mapped[str | None] = mapped_column(Text)
    preparation_tips: Mapped[str | None] = mapped_column(Text)
    last_updated: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    state: Mapped[str | None] = mapped_column(String(100), index=True)
    country: Mapped[str | None] = mapped_column(String(120), index=True)
    hiring_status: Mapped[str | None] = mapped_column(String(80))
    source_url: Mapped[str | None] = mapped_column(String(500))
    last_verified_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    slug: Mapped[str | None] = mapped_column(String(180), index=True)
    source_name: Mapped[str | None] = mapped_column(String(120))
    verification_status: Mapped[str | None] = mapped_column(String(20), index=True)


class StartupFunding(Base):
    __tablename__ = "startup_funding"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    startup_id: Mapped[int] = mapped_column(ForeignKey("startup_information.id", ondelete="CASCADE"), index=True)
    round_name: Mapped[str] = mapped_column(String(80))
    amount: Mapped[str | None] = mapped_column(String(100))
    investors: Mapped[str | None] = mapped_column(Text)
    announced_at: Mapped[Date | None] = mapped_column(Date)
    source_url: Mapped[str] = mapped_column(String(500))


class StartupRole(Base):
    __tablename__ = "startup_roles"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    startup_id: Mapped[int] = mapped_column(ForeignKey("startup_information.id", ondelete="CASCADE"), index=True)
    title: Mapped[str] = mapped_column(String(200), index=True)
    is_open: Mapped[bool] = mapped_column(Boolean, default=False)
