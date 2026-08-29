from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CompanySummary(BaseModel):
    id: int
    name: str
    logo_url: str | None = None
    industry: str | None = None
    headquarters: str | None = None
    country: str | None = None
    hiring_status: str | None = None
    internship_available: bool = False
    freshers_hiring: bool = False
    description: str | None = None
    tech_stack: str | None = None
    products: str | None = None
    career_url: str | None = None
    open_roles: int | None = None
    verification_status: str
    verified: bool
    data_source_url: str | None = None
    last_verified_at: datetime | None = None
    model_config = ConfigDict(from_attributes=True)


class CompanyDetail(CompanySummary):
    founded_year: int | None = None
    company_size: str | None = None
    website_url: str | None = None
    public_email: str | None = None
    linkedin_url: str | None = None
    description: str | None = None
    tech_stack: str | None = None
    office_locations: str | None = None
    skills: list[dict]
    roles: list[dict]
    locations: list[dict] = Field(default_factory=list)
    remote_policy: str | None = None
    insights: dict | None = None


class StartupSummary(BaseModel):
    id: int
    name: str
    industry: str
    location: str
    funding_stage: str | None = None
    latest_funding_amount: str | None = None
    founded_year: int | None = None
    employees: str | None = None
    website_url: str | None = None
    careers_url: str | None = None
    open_positions: int | None = None
    open_roles: int | None = None
    tech_stack: str | None = None
    description: str | None = None
    state: str | None = None
    country: str | None = None
    public_email: str | None = None
    hiring_status: str | None = None
    source_url: str | None = None
    source_name: str | None = None
    founders: str | None = None
    investors: str | None = None
    products: str | None = None
    culture_summary: str | None = None
    verification_status: str
    verified: bool
    last_verified_at: datetime | None = None
    last_updated: datetime
    model_config = ConfigDict(from_attributes=True)


class StartupRoleResponse(BaseModel):
    id: int
    startup_id: int
    title: str
    is_open: bool


class StartupDetail(StartupSummary):
    preparation_tips: str | None = None
    roles: list[StartupRoleResponse] = Field(default_factory=list)


class StartupUpsert(BaseModel):
    name: str
    industry: str
    location: str
    state: str | None = None
    country: str | None = None
    description: str | None = None
    funding_stage: str | None = None
    latest_funding_amount: str | None = None
    website_url: str | None = None
    careers_url: str | None = None
    public_email: str | None = None
    tech_stack: str | None = None
    hiring_status: str | None = None
    open_positions: int | None = None
    source_url: str


class TargetCompanyRequest(BaseModel):
    company: str = Field(min_length=1, max_length=150)
    role: str = Field(min_length=1, max_length=150)
    experience_level: str = Field(default="fresher", min_length=2, max_length=30)
    job_description: str | None = Field(default=None, max_length=50000)
