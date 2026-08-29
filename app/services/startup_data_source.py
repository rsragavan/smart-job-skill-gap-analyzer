"""Source adapters for startup ingestion.

The first adapter reuses the project's existing curated, source-backed catalog.
New providers can implement the same small interface without changing the API.
"""

from typing import Any, Protocol


class StartupDataSource(Protocol):
    source_name: str

    def fetch_startups(self) -> list[dict[str, Any]]:
        ...


class CuratedStartupDataSource:
    source_name = "curated_local_dataset"

    def fetch_startups(self) -> list[dict[str, Any]]:
        # Import lazily so the existing catalog remains the single source of
        # curated facts and can continue to be used by the legacy importer.
        from app.services.verified_import_service import COMPANY_CATALOG, STARTUP_NAMES

        records = []
        for item in COMPANY_CATALOG:
            if item["name"] not in STARTUP_NAMES:
                continue
            records.append({
                "name": item["name"],
                "industry": item["industry"],
                "location": item["headquarters"],
                "state": "Tamil Nadu" if item["headquarters"] in {"Chennai", "Coimbatore"} else None,
                "country": item.get("country", "India"),
                "description": item["description"],
                "founded_year": item.get("founded_year"),
                "website_url": item.get("website_url"),
                "careers_url": item.get("career_url"),
                "public_email": item.get("public_email"),
                "source_url": item.get("source"),
                "source_name": self.source_name,
                "verification_status": "verified",
            })
        return records
