from datetime import UTC, datetime

from sqlalchemy import Boolean, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class Company(Base):
    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    name: Mapped[str] = mapped_column(
        String(150),
        unique=True,
        nullable=False
    )

    greenhouse_token: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False
    )

    career_url: Mapped[str] = mapped_column(
        String(500),
        nullable=False
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    last_scraped_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC)
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC)
    )
    platform: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="greenhouse"
    )
    logo_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    industry: Mapped[str | None] = mapped_column(String(150), nullable=True, index=True)
    headquarters: Mapped[str | None] = mapped_column(String(150), nullable=True, index=True)
    country: Mapped[str | None] = mapped_column(String(120), nullable=True, index=True)
    founded_year: Mapped[int | None] = mapped_column(Integer, nullable=True)
    company_size: Mapped[str | None] = mapped_column(String(100), nullable=True)
    website_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    public_email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    linkedin_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    tech_stack: Mapped[str | None] = mapped_column(Text, nullable=True)
    hiring_status: Mapped[str | None] = mapped_column(String(80), nullable=True)
    internship_available: Mapped[bool] = mapped_column(Boolean, default=False)
    freshers_hiring: Mapped[bool] = mapped_column(Boolean, default=False)
    office_locations: Mapped[str | None] = mapped_column(Text, nullable=True)
    products: Mapped[str | None] = mapped_column(Text, nullable=True)
    business_domains: Mapped[str | None] = mapped_column(Text, nullable=True)
    remote_policy: Mapped[str | None] = mapped_column(String(150), nullable=True)
    culture_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    data_source_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    last_verified_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    verification_status: Mapped[str] = mapped_column(String(30), default="Unverified")
