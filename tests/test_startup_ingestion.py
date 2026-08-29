from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.models.company_intelligence import StartupInformation
from app.services.startup_ingestion_service import StartupIngestionService, normalize_url, normalize_text


class FakeSource:
    source_name = "test_source"

    def __init__(self, records):
        self.records = records

    def fetch_startups(self):
        return self.records


def session_for_startups():
    engine = create_engine("sqlite:///:memory:")
    StartupInformation.__table__.create(engine)
    return engine, Session(engine)


def base_record(**overrides):
    record = {
        "name": "  Example AI  ",
        "industry": " AI software ",
        "location": " Chennai ",
        "website_url": "HTTPS://Example.com/",
        "source_url": "https://example.com/about",
        "verification_status": "verified",
    }
    record.update(overrides)
    return record


def test_normalization_and_url_validation():
    service = StartupIngestionService(FakeSource([]))
    result = service.normalize_and_validate(base_record())
    assert result["name"] == "Example AI"
    assert result["industry"] == "AI software"
    assert result["website_url"] == "https://example.com"
    assert normalize_text("  a   b ") == "a b"
    assert normalize_url("https://Example.com/path/") == "https://example.com/path"

    try:
        service.normalize_and_validate(base_record(website_url="not-a-url"))
    except ValueError as error:
        assert "Invalid URL" in str(error)
    else:
        raise AssertionError("malformed URLs must be rejected")


def test_ingestion_insert_update_preserves_verified_values_and_is_idempotent():
    engine, db = session_for_startups()
    source = FakeSource([base_record(description="Verified description")])
    service = StartupIngestionService(source)
    first = service.ingest(db)
    second = service.ingest(db)
    assert first["inserted"] == 1
    assert second["inserted"] == 0
    assert second["updated"] == 0
    assert db.query(StartupInformation).count() == 1

    source.records = [base_record(description=None, verification_status="pending")]
    downgrade = service.ingest(db)
    row = db.query(StartupInformation).one()
    assert downgrade["updated"] == 0
    assert row.description == "Verified description"
    assert row.verification_status == "verified"
    db.close()
    engine.dispose()


def test_duplicate_pending_and_rejected_records_are_reported():
    engine, db = session_for_startups()
    source = FakeSource([
        base_record(),
        base_record(name="Example AI duplicate"),
        base_record(name="Pending Startup", website_url=None, source_url=None, verification_status="pending"),
        base_record(name="Rejected Startup", website_url=None, source_url=None, verification_status="rejected"),
    ])
    result = StartupIngestionService(source).ingest(db)
    assert result["inserted"] == 3
    assert result["duplicates"] == 1
    assert db.query(StartupInformation).count() == 3
    assert {row.verification_status for row in db.query(StartupInformation).all()} == {"verified", "pending", "rejected"}
    db.close()
    engine.dispose()
