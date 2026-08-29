from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.security import require_roles
from app.db.database import get_db
from app.models.user import Role, User
from app.schemas.company_intelligence import CompanyDetail, CompanySummary, StartupDetail, StartupRoleResponse, StartupSummary, TargetCompanyRequest
from app.services.company_intelligence_service import company_intelligence_service

router = APIRouter(prefix="/company-intelligence", tags=["Company Intelligence"])
public_router = APIRouter(prefix="/companies", tags=["Company Intelligence"])
startup_router = APIRouter(prefix="/startups", tags=["Startup Discovery"])
company_target_router = APIRouter(tags=["Target Company Interview Preparation"])


@router.get("/companies", response_model=list[CompanySummary])
def list_companies(search: str | None = None, location: str | None = None, industry: str | None = None, role: str | None = None, skill: str | None = None, freshers: bool | None = None, internships: bool | None = None, verified: str | None = None, page: int = Query(default=1, ge=1), page_size: int = Query(default=24, ge=1, le=100), db: Session = Depends(get_db)):
    parsed_verified = None if verified is None or not verified.strip() else verified.strip().casefold() == "true"
    return company_intelligence_service.list_companies(db, search, location, industry, freshers, internships, role, skill, parsed_verified, page, page_size)


@router.get("/target-intelligence")
def target_intelligence(company_id: int | None = None, role_id: int | None = None, company: str = "", role: str = "", db: Session = Depends(get_db)):
    return company_intelligence_service.target_intelligence(db, company_id, role_id, company, role)


@router.get("/target-companies")
def target_companies(search: str | None = None, db: Session = Depends(get_db)):
    return company_intelligence_service.list_target_companies(db, search)


@router.post("/target-company")
def select_target_company(payload: TargetCompanyRequest, user: User = Depends(require_roles(Role.USER)), db: Session = Depends(get_db)):
    return company_intelligence_service.generate_target_preparation(db, user.id, payload.company, payload.role, payload.experience_level, payload.job_description)


@company_target_router.get("/target-companies")
def target_companies_alias(search: str | None = None, db: Session = Depends(get_db)):
    return company_intelligence_service.list_target_companies(db, search)


@company_target_router.post("/target-company")
def select_target_company_alias(payload: TargetCompanyRequest, user: User = Depends(require_roles(Role.USER)), db: Session = Depends(get_db)):
    return company_intelligence_service.generate_target_preparation(db, user.id, payload.company, payload.role, payload.experience_level, payload.job_description)


@router.get("/companies/{company_id}", response_model=CompanyDetail)
def get_company(company_id: int, db: Session = Depends(get_db)):
    result = company_intelligence_service.get_company(db, company_id)
    if not result:
        raise HTTPException(status_code=404, detail="Company not found.")
    return result


@router.get("/companies/{company_id}/roles/{role_id}")
def get_role_process(company_id: int, role_id: int, db: Session = Depends(get_db)):
    result = company_intelligence_service.get_role(db, company_id, role_id)
    if not result:
        raise HTTPException(status_code=404, detail="Company role not found.")
    return result


@router.get("/startups", response_model=list[StartupSummary])
def list_startups(search: str | None = None, location: str | None = None, industry: str | None = None, funding_stage: str | None = Query(default=None, alias="fundingStage"), verification_status: str | None = None, page: int = Query(default=1, ge=1), page_size: int = Query(default=24, ge=1, le=100), db: Session = Depends(get_db)):
    return company_intelligence_service.list_startups(db, search, location, industry, funding_stage, None, page, page_size, verification_status)


@public_router.get("")
def companies_alias(search: str | None = None, verified: bool | None = None, db: Session = Depends(get_db)):
    return company_intelligence_service.list_companies(db, search, verified=verified)


@public_router.get("/{company_id}")
def company_alias(company_id: int, db: Session = Depends(get_db)):
    result = company_intelligence_service.get_company(db, company_id)
    if not result: raise HTTPException(status_code=404, detail="Company not found.")
    return result


@public_router.get("/{company_id}/roles")
def roles_alias(company_id: int, db: Session = Depends(get_db)):
    return company_intelligence_service.list_roles(db, company_id)


@public_router.get("/{company_id}/roles/{role_id}")
@public_router.get("/{company_id}/roles/{role_id}/selection-process")
@public_router.get("/{company_id}/roles/{role_id}/interview-process")
def role_alias(company_id: int, role_id: int, db: Session = Depends(get_db)):
    result = company_intelligence_service.get_role(db, company_id, role_id)
    if not result: raise HTTPException(status_code=404, detail="Company role not found.")
    return result


@public_router.get("/{company_id}/preparation")
def preparation_alias(company_id: int, role_id: int | None = None, db: Session = Depends(get_db)):
    result = company_intelligence_service.preparation(db, company_id, role_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Company role not found.")
    return result


@startup_router.get("")
def startups_alias(search: str | None = None, location: str | None = None, industry: str | None = None, funding_stage: str | None = None, founder: str | None = None, verification_status: str | None = None, page: int = Query(default=1, ge=1), page_size: int = Query(default=24, ge=1, le=100), db: Session = Depends(get_db)):
    return company_intelligence_service.list_startups(db, search, location, industry, funding_stage, founder, page, page_size, verification_status)


@startup_router.get("/search")
def startup_search(search: str | None = None, city: str | None = None, state: str | None = None, industry: str | None = None, funding_stage: str | None = None, db: Session = Depends(get_db)):
    return company_intelligence_service.list_startups(db, search, city or state, industry, funding_stage)


@startup_router.get("/{startup_id}/roles", response_model=list[StartupRoleResponse])
def startup_roles(startup_id: int, db: Session = Depends(get_db)):
    result = company_intelligence_service.list_startup_roles(db, startup_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Startup not found.")
    return result


@startup_router.get("/{startup_id}", response_model=StartupDetail)
def startup_detail(startup_id: int, db: Session = Depends(get_db)):
    result = company_intelligence_service.get_startup(db, startup_id)
    if not result:
        raise HTTPException(status_code=404, detail="Startup not found.")
    return result
