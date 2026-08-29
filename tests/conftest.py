"""Keep legacy manual smoke scripts out of the automated pytest collection."""

# These files execute database/network/manual-demo code at import time and
# reference fixtures or modules removed during the architecture migration.
# Production regression coverage lives in regular assertion-based tests.
collect_ignore = [
    "test_company_db.py",
    "test_company_service.py",
    "test_greenhouse.py",
    "test_greenhouse_client.py",
    "test_job_fetch_service.py",
    "test_job_recommendation_service.py",
    "test_job_sync_service.py",
    "test_learning_recommendation_service.py",
    "test_pymupdf.py",
    "test_resume_analysis_service.py",
    "test_resume_parser.py",
    "test_job_match_service.py",
    "test_skill_gap_service.py",
    "test_skill_extractor.py",
    "test_job_skill_extractor.py",
]
