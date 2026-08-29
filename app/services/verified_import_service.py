"""Idempotent imports for public, source-backed company intelligence.

The catalog intentionally contains profile facts and links only.  Hiring rounds
are not generated here: a process is inserted only when a source-backed record
is supplied by a caller.
"""

from datetime import UTC, datetime
import re
from typing import Any

from sqlalchemy.orm import Session

from app.models.company import Company
from app.models.company_intelligence import CompanyRole, StartupInformation, StartupRole


ROLE_FAMILIES = (
    "Software Engineer", "Backend Engineer", "Frontend Engineer",
    "Full Stack Engineer", "DevOps Engineer", "QA Engineer", "Data Analyst",
    "Data Engineer", "ML Engineer", "Cloud Engineer", "Security Engineer",
)


def _token(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")[:90]


COMPANY_CATALOG: tuple[dict[str, Any], ...] = (
    {"name":"Zoho","industry":"Business software","description":"Business software company providing cloud applications and operating-system products.","founded_year":1996,"headquarters":"Chennai","website_url":"https://www.zoho.com/","career_url":"https://www.zoho.com/careers/","source":"https://www.zoho.com/aboutus.html"},
    {"name":"Freshworks","industry":"Business software","description":"AI-first service software company for customer and employee experiences.","founded_year":2010,"headquarters":"San Mateo","country":"United States","website_url":"https://www.freshworks.com/","career_url":"https://www.freshworks.com/company/careers/","source":"https://www.freshworks.com/company/about/"},
    {"name":"TCS","industry":"IT services and consulting","description":"Technology services and consulting company serving enterprises worldwide.","founded_year":1968,"headquarters":"Mumbai","website_url":"https://www.tcs.com/","career_url":"https://www.tcs.com/careers","source":"https://www.tcs.com/who-we-are"},
    {"name":"Infosys","industry":"IT services and consulting","description":"Digital services and consulting company helping organizations navigate digital transformation.","founded_year":1981,"headquarters":"Bengaluru","website_url":"https://www.infosys.com/","career_url":"https://www.infosys.com/careers/","source":"https://www.infosys.com/about.html"},
    {"name":"Wipro","industry":"IT services and consulting","description":"Information technology, consulting and business process services company.","founded_year":1945,"headquarters":"Bengaluru","website_url":"https://www.wipro.com/","career_url":"https://careers.wipro.com/","source":"https://www.wipro.com/about-us/"},
    {"name":"HCL","industry":"IT services and consulting","description":"Technology company providing engineering, infrastructure and digital services.","founded_year":1976,"headquarters":"Noida","website_url":"https://www.hcltech.com/","career_url":"https://www.hcltech.com/careers","source":"https://www.hcltech.com/about-us"},
    {"name":"Accenture","industry":"Professional services","description":"Technology and consulting services company helping organizations build and operate change.","founded_year":1989,"headquarters":"Dublin","country":"Ireland","website_url":"https://www.accenture.com/","career_url":"https://www.accenture.com/in-en/careers","source":"https://www.accenture.com/us-en/about"},
    {"name":"Capgemini","industry":"IT services and consulting","description":"Business and technology transformation company.","founded_year":1967,"headquarters":"Paris","country":"France","website_url":"https://www.capgemini.com/","career_url":"https://www.capgemini.com/careers/","source":"https://www.capgemini.com/about-us/"},
    {"name":"IBM","industry":"Technology","description":"Technology company providing hybrid cloud, AI and consulting solutions.","founded_year":1911,"headquarters":"Armonk","country":"United States","website_url":"https://www.ibm.com/","career_url":"https://www.ibm.com/careers","source":"https://www.ibm.com/about"},
    {"name":"Microsoft","industry":"Technology","description":"Technology company developing software, cloud services, devices and platforms.","founded_year":1975,"headquarters":"Redmond","country":"United States","website_url":"https://www.microsoft.com/","career_url":"https://careers.microsoft.com/","source":"https://www.microsoft.com/en-us/about"},
    {"name":"Google","industry":"Technology","description":"Technology company organized around information, computing, advertising and digital services.","founded_year":1998,"headquarters":"Mountain View","country":"United States","website_url":"https://about.google/","career_url":"https://careers.google.com/","source":"https://about.google/intl/en_us/"},
    {"name":"Amazon","industry":"Technology and ecommerce","description":"Technology company operating ecommerce, cloud computing and digital services businesses.","founded_year":1994,"headquarters":"Seattle","country":"United States","website_url":"https://www.amazon.com/","career_url":"https://www.amazon.jobs/","source":"https://www.aboutamazon.com/about-us"},
    {"name":"Canonical","industry":"Open source software","description":"Publisher of Ubuntu and provider of open-source enterprise technologies.","founded_year":2004,"headquarters":"London","country":"United Kingdom","website_url":"https://canonical.com/","career_url":"https://canonical.com/careers","source":"https://canonical.com/about"},
    {"name":"GitLab","industry":"DevOps software","description":"Provider of a single application for the DevSecOps lifecycle.","founded_year":2011,"headquarters":"San Francisco","country":"United States","website_url":"https://about.gitlab.com/","career_url":"https://about.gitlab.com/handbook/hiring/","source":"https://about.gitlab.com/company/"},
    {"name":"Cloudflare","industry":"Internet infrastructure","description":"Connectivity cloud company providing network, security and developer services.","founded_year":2009,"headquarters":"San Francisco","country":"United States","website_url":"https://www.cloudflare.com/","career_url":"https://www.cloudflare.com/careers/","source":"https://www.cloudflare.com/about-overview/"},
    {"name":"MongoDB","industry":"Database software","description":"Developer data platform company built around MongoDB database technologies.","founded_year":2007,"headquarters":"New York","country":"United States","website_url":"https://www.mongodb.com/","career_url":"https://www.mongodb.com/careers","source":"https://www.mongodb.com/company"},
    {"name":"HashiCorp","industry":"Cloud infrastructure software","description":"Provider of infrastructure lifecycle management tools for cloud environments.","founded_year":2012,"headquarters":"San Francisco","country":"United States","website_url":"https://www.hashicorp.com/","career_url":"https://www.hashicorp.com/careers","source":"https://www.hashicorp.com/about"},
    {"name":"Figma","industry":"Design software","description":"Collaborative design and product development platform.","founded_year":2012,"headquarters":"San Francisco","country":"United States","website_url":"https://www.figma.com/","career_url":"https://www.figma.com/careers/","source":"https://www.figma.com/about/"},
    {"name":"Dropbox","industry":"Cloud software","description":"Software company providing tools for file storage, sharing and collaboration.","founded_year":2007,"headquarters":"San Francisco","country":"United States","website_url":"https://www.dropbox.com/","career_url":"https://jobs.dropbox.com/","source":"https://www.dropbox.com/about"},
    {"name":"Postman","industry":"API software","description":"API platform for building, testing and operating APIs.","founded_year":2014,"headquarters":"San Francisco","country":"United States","website_url":"https://www.postman.com/","career_url":"https://www.postman.com/careers/","source":"https://www.postman.com/company/about-postman/"},
    {"name":"Chargebee","industry":"Billing software","description":"Revenue growth management and subscription billing platform.","founded_year":2011,"headquarters":"Chennai","website_url":"https://www.chargebee.com/","career_url":"https://www.chargebee.com/careers/join-us/","source":"https://www.chargebee.com/careers/"},
    {"name":"Kissflow","industry":"Workflow software","description":"Low-code and workflow platform for business process management.","headquarters":"Chennai","website_url":"https://kissflow.com/","career_url":"https://kissflow.com/careers/","source":"https://kissflow.com/about/"},
    {"name":"SuperOps","industry":"IT management software","description":"IT management platform for managed service providers and IT teams.","headquarters":"Chennai","website_url":"https://superops.com/","career_url":"https://superops.com/careers","source":"https://superops.com/about-us"},
    {"name":"Agnikul Cosmos","industry":"Space technology","description":"Space technology company developing launch vehicles and launch services.","headquarters":"Chennai","website_url":"https://agnikul.in/","career_url":"https://agnikul.in/careers/","public_email":"humancapital@agnikul.in","source":"https://agnikul.in/careers/"},
    {"name":"Rocketlane","industry":"Professional services software","description":"Customer onboarding and professional services project management platform.","headquarters":"Chennai","website_url":"https://rocketlane.com/","career_url":"https://rocketlane.com/careers","source":"https://rocketlane.com/about-us"},
    {"name":"SurveySparrow","industry":"Customer experience software","description":"Online survey and customer experience management platform.","headquarters":"Coimbatore","website_url":"https://surveysparrow.com/","career_url":"https://surveysparrow.com/careers/","source":"https://surveysparrow.com/about-us/"},
    {"name":"Detect Technologies","industry":"Industrial technology","description":"Industrial technology company providing AI-enabled operations and safety solutions.","headquarters":"Chennai","website_url":"https://detecttechnologies.com/","career_url":"https://detecttechnologies.com/careers/","source":"https://detecttechnologies.com/about-us/"},
    {"name":"HyperVerge","industry":"Identity technology","description":"Identity verification and fraud prevention technology company.","headquarters":"Bengaluru","website_url":"https://hyperverge.co/","career_url":"https://hyperverge.co/careers/","source":"https://hyperverge.co/about-us/"},
)


def _reference_companies() -> tuple[dict[str, Any], ...]:
    """Return selectable identity records without asserting hiring data.

    These records are deliberately inactive and are not included in the
    Greenhouse synchronization set.  They exist only so students can choose a
    target company when verified company-specific interview data is absent.
    """
    groups = {
        "Tamil Nadu technology": ("Chennai", "Tamil Nadu", "Zoho Freshworks Chargebee Kissflow Ramco Systems SuperOps Rocketlane SurveySparrow Zuper Facilio Uniphore Whatfix Detect Technologies Agnikul Cosmos Juspay GUVI WayCool Disprz Vuram FourKites CloudCherry Pando Everstage M2P Fintech Spendflo Kapture CX Data Patterns LatentView Analytics Prodapt Aspire Systems CavinKare Cavin InfoTech Contus Integra Software Services Photon Sify Technologies Impiger Technologies"),
        "Indian product and SaaS": ("Pan-India", "India", "BrowserStack Postman Razorpay Zerodha PhonePe Paytm CRED Groww Meesho Flipkart Swiggy Zomato Dream11 ShareChat Dailyhunt InMobi Udaan OfBusiness Delhivery Policybazaar Nykaa Myntra BigBasket Urban Company Ola Rapido Druva Hasura PostHog Gupshup MoEngage CleverTap LeadSquared Darwinbox HighRadius Yellow.ai Observe.AI GreyOrange Apna MobiKwik Pine Labs Cashfree Payments Open Financial Technologies Perfios Innovaccer Practo Porter Infra.Market"),
        "Indian IT services": ("Pan-India", "India", "Cognizant HCLTech Tech Mahindra LTIMindtree Mphasis Persistent Systems Coforge Hexaware Virtusa CGI DXC Technology NTT DATA Tata Consultancy Services L&T Technology Services Birlasoft Sonata Software Cyient KPIT Technologies Zensar Technologies Tata Elxsi Happiest Minds Mastek Newgen Software Oracle Financial Services Software Sasken Technologies Nucleus Software eClerx"),
        "Indian fintech": ("Pan-India", "India", "BharatPe Navi ACKO CredAvenue Yubi Fi Jupiter slice"),
        "Indian internet and commerce": ("Pan-India", "India", "Amazon India Zepto Blinkit Ajio Tata Digital Tata Neu"),
        "Global technology with India hiring": ("India", "India", "Apple Meta Adobe Salesforce Intel NVIDIA AMD HP Visa Mastercard JPMorgan Chase Goldman Sachs Morgan Stanley Deutsche Bank UBS"),
        "Global technology and engineering": ("India", "India", "Cisco Dell Technologies Hewlett Packard Enterprise VMware Broadcom ServiceNow SAP ADP Workday Comcast Verizon Ford Caterpillar Schneider Electric Siemens Honeywell Bosch Mercedes-Benz Research & Development Renault Nissan Technology & Business Centre Wells Fargo Citi Barclays Standard Chartered HSBC NatWest FIS Fiserv BNY American Express"),
    }
    result: list[dict[str, Any]] = []
    seen: set[str] = set()
    existing = {" ".join(item["name"].casefold().split()) for item in COMPANY_CATALOG}
    for industry, (location, country, names) in groups.items():
        for name in names.split():
            # Preserve multi-word names supplied as explicit entries below.
            if name in {"/", "&", "India", "Indian", "CavinKare", "Cavin", "InfoTech", "Data", "Patterns", "LatentView", "Analytics", "M2P", "Fintech", "Kapture", "CX", "Open", "Financial", "Technologies", "Tata", "Consultancy", "Services", "Software", "L&T", "Technology", "Mercedes-Benz", "Research", "Development", "Renault", "Nissan", "Centre", "American", "Express", "Oracle", "Newgen", "CredAvenue", "Yubi", "Hewlett", "Packard", "Enterprise", "Walmart", "Global", "Tech", "Cashfree", "Payments", "Infra.Market", "Digital", "Neu", "Amazon"}:
                continue
            normalized = " ".join(name.casefold().split())
            if normalized in existing or normalized in seen:
                continue
            seen.add(normalized)
            result.append({"name": name, "industry": industry, "headquarters": location, "country": country, "career_url": "", "platform": "target-reference", "is_active": False, "verified": False})
    # Multi-word names are kept as explicit records so autocomplete remains useful.
    explicit = {
        "CavinKare": "Tamil Nadu technology", "Cavin InfoTech": "Tamil Nadu technology", "Data Patterns": "Tamil Nadu technology", "LatentView Analytics": "Tamil Nadu technology", "M2P Fintech": "Tamil Nadu technology", "Kapture CX": "Tamil Nadu technology", "Open Financial Technologies": "Indian product and SaaS", "Tata Consultancy Services": "Indian IT services", "Oracle Financial Services Software": "Indian IT services", "Mercedes-Benz Research & Development": "Global technology and engineering", "Renault Nissan Technology & Business Centre": "Global technology and engineering", "Hewlett Packard Enterprise": "Global technology and engineering", "Amazon India": "Indian internet and commerce", "CredAvenue / Yubi": "Indian fintech", "VMware / Broadcom": "Global technology and engineering", "Walmart Global Tech": "Global technology and engineering", "L&T Technology Services": "Indian IT services", "Infra.Market": "Indian product and SaaS", "Cashfree Payments": "Indian product and SaaS", "MobiKwik": "Indian fintech", "Pine Labs": "Indian fintech", "Policybazaar": "Indian fintech", "Tata Digital": "Indian internet and commerce", "Tata Neu": "Indian internet and commerce", "CavinKare / Cavin InfoTech": "Tamil Nadu technology",
    }
    for name, industry in explicit.items():
        normalized = " ".join(name.casefold().split())
        if normalized in existing or normalized in seen:
            continue
        location = "Chennai" if industry == "Tamil Nadu technology" else "Pan-India" if industry.startswith("Indian") else "India"
        result.append({"name": name, "industry": industry, "headquarters": location, "country": "India", "career_url": "", "platform": "target-reference", "is_active": False, "verified": False})
        seen.add(normalized)
    return tuple(result)


COMPANY_CATALOG = COMPANY_CATALOG + _reference_companies()


STARTUP_NAMES = {"Chargebee", "Kissflow", "SuperOps", "Agnikul Cosmos", "Rocketlane", "SurveySparrow", "Detect Technologies", "HyperVerge"}


class CompanyImportService:
    def import_all(self, db: Session) -> dict[str, Any]:
        now = datetime.now(UTC)
        created = updated = 0
        for item in COMPANY_CATALOG:
            normalized_name = " ".join(item["name"].casefold().split())
            row = next((candidate for candidate in db.query(Company).all() if " ".join(candidate.name.casefold().split()) == normalized_name), None)
            verified = item.get("verified", True)
            values = {**item, "country": item.get("country", "India"), "data_source_url": item.get("source"), "last_verified_at": now if verified else None, "verification_status": "Verified" if verified else "Unverified", "platform": item.get("platform", "verified-import"), "greenhouse_token": _token(item["name"]), "is_active": item.get("is_active", True)}
            values.pop("source", None)
            values["career_url"] = item.get("career_url", "")
            values.pop("verified", None)
            if row is None:
                row = Company(**values)
                db.add(row)
                created += 1
            else:
                for key, value in values.items(): setattr(row, key, value)
                updated += 1
            db.flush()
            for title in ROLE_FAMILIES:
                if not db.query(CompanyRole).filter_by(company_id=row.id, title=title).first():
                    db.add(CompanyRole(company_id=row.id, title=title, is_open=False))
        db.commit()
        return {"created": created, "updated": updated, "total": len(COMPANY_CATALOG), "verified_at": now}


class StartupImportService:
    def import_all(self, db: Session) -> dict[str, Any]:
        now = datetime.now(UTC)
        companies = {item["name"]: item for item in COMPANY_CATALOG if item["name"] in STARTUP_NAMES}
        created = updated = 0
        for name, item in companies.items():
            row = db.query(StartupInformation).filter(StartupInformation.name == name).first()
            values = {"name": name, "industry": item["industry"], "location": item["headquarters"], "state": "Tamil Nadu" if item["headquarters"] in {"Chennai", "Coimbatore"} else None, "country": item.get("country", "India"), "description": item["description"], "founded_year": item.get("founded_year"), "website_url": item["website_url"], "careers_url": item["career_url"], "public_email": item.get("public_email"), "tech_stack": None, "hiring_status": "Open careers page", "source_url": item["source"], "last_verified_at": now}
            if row is None:
                row = StartupInformation(**values)
                db.add(row)
                db.flush()
                created += 1
            else:
                for key, value in values.items(): setattr(row, key, value)
                updated += 1
            db.flush()
            # Only Agnikul's public careers page names current crews/openings;
            # other startup roles are deliberately not inferred.
            if name == "Agnikul Cosmos":
                for title in ("Power electronics Engineer", "Mission Design Software Developer", "Launch Vehicle Operations Strategist", "ERPNext Developer"):
                    if not db.query(StartupRole).filter_by(startup_id=row.id, title=title).first():
                        db.add(StartupRole(startup_id=row.id, title=title, is_open=True))
        db.commit()
        return {"created": created, "updated": updated, "total": len(companies), "verified_at": now}


company_import_service = CompanyImportService()
startup_import_service = StartupImportService()
