"""Readable, deterministic coding recommendations for the active target."""

from collections import defaultdict

from sqlalchemy.orm import Session

from app.models.content import CodingQuestion
from app.models.mock_interview import CodingAttempt
from app.models.user_target import UserTarget

SUPPORTED_LANGUAGES = {"python", "java", "javascript", "cpp"}
DIFFICULTIES = {
    "fresher": ("easy", "medium", "hard"),
    "entry": ("easy", "medium", "hard"),
    "intermediate": ("medium", "hard", "easy"),
    "mid": ("medium", "hard", "easy"),
    "senior": ("medium", "hard", "easy"),
    "advanced": ("medium", "hard", "easy"),
}
KNOWN_SKILLS = {"python", "java", "javascript", "typescript", "react", "fastapi", "sql", "postgresql", "docker", "git", "aws", "kubernetes", "linux", "rest", "api", "arrays", "strings", "hashing", "searching", "sorting", "trees", "graphs", "algorithms", "database", "testing"}


class CodingPracticeService:
    def recommend(self, db: Session, user_id: int, *, limit: int = 20, topic: str | None = None, skill: str | None = None, difficulty: str | None = None, experience_level: str = "fresher", language: str | None = None) -> dict:
        target = db.query(UserTarget).filter_by(user_id=user_id, is_active=True).first()
        rows = db.query(CodingQuestion).filter(CodingQuestion.active.is_(True), CodingQuestion.verified.is_(True)).order_by(CodingQuestion.id).all()
        if difficulty:
            rows = [row for row in rows if row.difficulty.casefold() == difficulty.casefold()]
        if topic:
            rows = [row for row in rows if topic.casefold() in f"{row.category} {row.topic}".casefold()]
        if skill:
            rows = [row for row in rows if skill.casefold() in self._values([row.category, row.topic, *(row.skills or [])])]
        if language and language.casefold() not in SUPPORTED_LANGUAGES:
            return {"selection_mode": "TARGET_SKILL_GAP", "target": self._target(target), "experience_level": experience_level, "language": language, "questions": []}

        attempts = db.query(CodingAttempt).filter_by(user_id=user_id).all()
        history: dict[int, dict] = defaultdict(lambda: {"attempts": 0, "passed": 0, "failed": 0, "last_attempted": None, "best_result": 0})
        for attempt in attempts:
            item = history[attempt.question_id]
            item["attempts"] += 1
            item["last_attempted"] = max(filter(None, [item["last_attempted"], attempt.submitted_at]), default=attempt.submitted_at)
            item["best_result"] = max(item["best_result"], round((attempt.passed_tests / attempt.total_tests) * 100) if attempt.total_tests else 0)
            if attempt.status in {"PASSED", "ACCEPTED"}:
                item["passed"] += 1
            else:
                item["failed"] += 1

        missing = self._values(target.missing_skills if target else [])
        matched = self._values(target.matched_skills if target else [])
        required = self._job_skills(target.job_description if target else "")
        role_terms = self._role_terms(target.role_title if target else None)
        difficulty_order = DIFFICULTIES.get(experience_level.casefold(), DIFFICULTIES["fresher"])
        ranked = []
        for row in rows:
            values = self._values([row.category, row.topic, *(row.skills or []), row.title])
            text = f"{row.title} {row.category} {row.topic} {' '.join(row.skills or [])}".casefold()
            score = 0
            reasons = []
            missing_match = sorted(values & missing)
            if missing_match:
                score += 40
                reasons.append(f"matches your missing {', '.join(missing_match)} skill")
            required_match = values & required
            if required_match:
                score += 35
                reasons.append("matches skills from the target job")
            if values & matched:
                score += 20
                reasons.append("reinforces a resume skill")
            if any(term in text for term in role_terms):
                score += 15
                reasons.append("is relevant to the target role")
            if row.difficulty.casefold() == difficulty_order[0]:
                score += 10
            elif row.difficulty.casefold() == difficulty_order[1]:
                score += 7
            if row.category.casefold() in {"technical", "sql", "basic sql", "algorithms", "database"} or row.topic.casefold() in {"sql", "algorithms", "database"}:
                score += 10
                reasons.append("is interview-relevant technical practice")
            record = history.get(row.id)
            if record and record["passed"]:
                score -= 30
                reasons.append("already passed, so it is lower priority")
            elif record:
                score += 5
                reasons.append("has been attempted and is worth revisiting")
            else:
                score += 5
            ranked.append((score, row.id, row, reasons, record or {"attempts": 0, "passed": 0, "failed": 0, "last_attempted": None, "best_result": 0}))

        ranked.sort(key=lambda item: (-item[0], item[1]))
        selected = []
        topics = set()
        for item in ranked:
            if len(selected) >= limit:
                break
            topic_key = item[2].topic.casefold()
            if topic_key not in topics or len(ranked) - len(selected) <= limit:
                selected.append(item)
                topics.add(topic_key)
        return {"selection_mode": "TARGET_SKILL_GAP", "target": self._target(target), "experience_level": experience_level, "language": language, "questions": [{"question": row, "score": score, "recommendation_reason": "; ".join(reasons) or "curated coding practice", "practice": record} for score, _, row, reasons, record in selected]}

    @staticmethod
    def _target(target: UserTarget | None) -> dict | None:
        return {"company": target.company, "role": target.role_title, "job_description_available": bool(target.job_description), "missing_skills": target.missing_skills or [], "matched_skills": target.matched_skills or []} if target else None

    @staticmethod
    def _values(values) -> set[str]:
        return {str(value).strip().casefold() for value in values if str(value).strip()}

    @classmethod
    def _job_skills(cls, description: str) -> set[str]:
        text = (description or "").casefold().replace("/", " ").replace("-", " ")
        return {skill for skill in KNOWN_SKILLS if skill in text}

    @staticmethod
    def _role_terms(role: str | None) -> set[str]:
        value = (role or "").casefold()
        terms = set()
        if "back" in value or "api" in value:
            terms.update({"backend", "sql", "database", "fastapi", "python", "rest"})
        if "front" in value or "react" in value:
            terms.update({"frontend", "react", "javascript", "typescript"})
        if "data" in value:
            terms.update({"sql", "database", "arrays", "algorithms"})
        return terms


coding_practice_service = CodingPracticeService()
