"""Normalize, validate, verify, deduplicate, and upsert startup records."""

from datetime import UTC, datetime
import logging
import re
from typing import Any
from urllib.parse import urlsplit, urlunsplit

from sqlalchemy.orm import Session

from app.models.company_intelligence import StartupInformation
from app.services.startup_data_source import CuratedStartupDataSource, StartupDataSource
from app.services.company_intelligence_service import company_intelligence_service

logger = logging.getLogger(__name__)
VALID_STATUSES = {"verified", "pending", "rejected"}
STATUS_RANK = {"rejected": 0, "pending": 1, "verified": 2}
TEXT_FIELDS = ("name", "industry", "location", "state", "country", "description", "funding_stage", "latest_funding_amount", "investors", "employees", "website_url", "careers_url", "public_email", "tech_stack", "founders", "products", "growth_stage", "culture_summary", "preparation_tips", "source_url", "source_name", "slug")


def normalize_text(value: Any) -> str | None:
    if value is None:
        return None
    value = " ".join(str(value).strip().split())
    return value or None


def normalize_url(value: Any) -> str | None:
    value = normalize_text(value)
    if value is None:
        return None
    parsed = urlsplit(value)
    if parsed.scheme.lower() not in {"http", "https"} or not parsed.netloc:
        raise ValueError(f"Invalid URL: {value}")
    return urlunsplit((parsed.scheme.lower(), parsed.netloc.lower(), parsed.path.rstrip("/"), parsed.query, ""))


class StartupIngestionService:
    def __init__(self, source: StartupDataSource | None = None):
        self.source = source or CuratedStartupDataSource()

    def ingest(self, db: Session) -> dict[str, Any]:
        logger.info("Startup ingestion started source=%s", self.source.source_name)
        raw_records = self.source.fetch_startups()
        result = {"source": self.source.source_name, "fetched": len(raw_records), "inserted": 0, "updated": 0, "duplicates": 0, "rejected": 0, "verified": 0, "pending": 0}
        existing = db.query(StartupInformation).all()
        by_key = {self.record_key(row): row for row in existing}
        seen: set[tuple[str, str]] = set()
        for raw in raw_records:
            try:
                record = self.normalize_and_validate(raw)
            except (TypeError, ValueError) as exc:
                result["rejected"] += 1
                logger.warning("Rejected startup record source=%s reason=%s", self.source.source_name, exc)
                continue
            key = self.record_key(record)
            if key in seen:
                result["duplicates"] += 1
                continue
            seen.add(key)
            row = by_key.get(key)
            if row is None:
                row = StartupInformation(open_positions=None, verification_status=record["verification_status"])
                self._merge(row, record, incoming_status=record["verification_status"])
                db.add(row)
                db.flush()
                by_key[key] = row
                result["inserted"] += 1
            elif self._merge(row, record, incoming_status=record["verification_status"]):
                result["updated"] += 1
            status = self.effective_status(row)
            if status in {"verified", "pending"}:
                result[status] += 1
        db.commit()
        logger.info("Startup ingestion completed source=%s fetched=%s inserted=%s updated=%s duplicates=%s rejected=%s verified=%s pending=%s", self.source.source_name, result["fetched"], result["inserted"], result["updated"], result["duplicates"], result["rejected"], result["verified"], result["pending"])
        return result

    def normalize_and_validate(self, raw: dict[str, Any]) -> dict[str, Any]:
        if not isinstance(raw, dict):
            raise TypeError("startup record must be an object")
        record = {field: normalize_text(raw.get(field)) for field in TEXT_FIELDS}
        if not record["name"]:
            raise ValueError("startup name is required")
        record["website_url"] = normalize_url(raw.get("website_url"))
        record["careers_url"] = normalize_url(raw.get("careers_url"))
        record["source_url"] = normalize_url(raw.get("source_url"))
        status = normalize_text(raw.get("verification_status"))
        record["verification_status"] = (status or "pending").casefold()
        if record["verification_status"] not in VALID_STATUSES:
            raise ValueError("verification_status must be verified, pending, or rejected")
        record["source_name"] = record["source_name"] or self.source.source_name
        record["slug"] = self.slug(record["name"])
        for field in ("founded_year", "open_positions"):
            value = raw.get(field)
            if value is not None:
                try:
                    record[field] = int(value)
                except (TypeError, ValueError) as exc:
                    raise ValueError(f"{field} must be an integer") from exc
        if record["verification_status"] == "verified" and not record["source_url"]:
            raise ValueError("verified startup requires source_url")
        return record

    @staticmethod
    def slug(name: str) -> str:
        return re.sub(r"[^a-z0-9]+", "-", name.casefold()).strip("-")

    @staticmethod
    def record_key(record: StartupInformation | dict[str, Any]) -> tuple[str, str]:
        website = record.website_url if isinstance(record, StartupInformation) else record.get("website_url")
        name = record.name if isinstance(record, StartupInformation) else record.get("name")
        location = record.location if isinstance(record, StartupInformation) else record.get("location")
        if website:
            host = urlsplit(website).netloc.casefold().removeprefix("www.")
            return ("domain", host)
        return ("name-location", f"{company_intelligence_service._normalized(name or '')}|{company_intelligence_service._normalized(location or '')}")

    @staticmethod
    def effective_status(row: StartupInformation) -> str:
        status = (row.verification_status or "").casefold()
        if status in VALID_STATUSES:
            return status
        if row.source_url and row.last_verified_at:
            return "verified"
        return "pending"

    def _merge(self, row: StartupInformation, record: dict[str, Any], incoming_status: str) -> bool:
        current_status = self.effective_status(row)
        if STATUS_RANK[incoming_status] < STATUS_RANK[current_status]:
            return False
        changed = False
        for field in TEXT_FIELDS + ("founded_year", "open_positions"):
            value = record.get(field)
            if value is not None and getattr(row, field, None) != value:
                setattr(row, field, value)
                changed = True
        if row.verification_status != incoming_status:
            row.verification_status = incoming_status
            changed = True
        if incoming_status == "verified" and row.last_verified_at is None:
            row.last_verified_at = datetime.now(UTC)
            changed = True
        return changed


startup_ingestion_service = StartupIngestionService()
