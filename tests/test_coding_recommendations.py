from datetime import UTC, datetime
from types import SimpleNamespace

from app.services.coding_practice_service import CodingPracticeService


class _Query:
    def __init__(self, rows):
        self.rows = rows

    def filter_by(self, **_: object):
        return self

    def filter(self, *_: object):
        return self

    def order_by(self, *_: object):
        return self

    def all(self):
        return self.rows

    def first(self):
        return self.rows[0] if self.rows else None


class _DB:
    def __init__(self, target, questions, attempts=None):
        self.rows = {"target": [target] if target else [], "questions": questions, "attempts": attempts or []}

    def query(self, model):
        name = model.__name__
        return _Query(self.rows["target"] if name == "UserTarget" else self.rows["questions"] if name == "CodingQuestion" else self.rows["attempts"])


def _question(question_id, title, skill, topic="Arrays", difficulty="easy"):
    return SimpleNamespace(id=question_id, title=title, skill=skill, skills=[skill], topic=topic, category=topic, difficulty=difficulty)


def test_missing_skill_is_ranked_above_unrelated_question():
    target = SimpleNamespace(company="Example", role_title="Backend Developer", job_description="Python SQL PostgreSQL", missing_skills=["Hashing"], matched_skills=[])
    db = _DB(target, [_question(1, "Two Sum", "Hashing"), _question(2, "Tree Traversal", "Trees", "Trees", "medium")])
    result = CodingPracticeService().recommend(db, 7, limit=2)
    assert result["questions"][0]["question"].title == "Two Sum"
    assert "missing" in result["questions"][0]["recommendation_reason"]


def test_successfully_passed_question_is_deprioritized_and_stats_returned():
    target = SimpleNamespace(company="Example", role_title="Backend Developer", job_description="", missing_skills=[], matched_skills=[])
    passed = SimpleNamespace(question_id=1, status="ACCEPTED", passed_tests=3, total_tests=3, submitted_at=datetime.now(UTC))
    db = _DB(target, [_question(1, "Solved", "Arrays"), _question(2, "New", "Strings")], [passed])
    result = CodingPracticeService().recommend(db, 7, limit=2)
    assert result["questions"][0]["question"].title == "New"
    assert result["questions"][1]["practice"]["best_result"] == 100


def test_recommendations_fall_back_without_active_target():
    db = _DB(None, [_question(1, "Array Basics", "Arrays"), _question(2, "SQL Basics", "SQL", "SQL")])
    result = CodingPracticeService().recommend(db, 7, limit=2)
    assert result["target"] is None
    assert len(result["questions"]) == 2
