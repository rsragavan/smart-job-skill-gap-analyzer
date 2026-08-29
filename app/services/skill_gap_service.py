"""Single, explainable skill-gap calculation used by targets and matching."""

from collections import Counter

from app.services.technical_skills_engine import skills_engine


class SkillGapService:
    @staticmethod
    def _key(skill: str) -> str:
        return skills_engine.normalize(skill or "")

    @staticmethod
    def _canonical(skill: str) -> str:
        return skills_engine.canonicalize(skill or "")

    def normalize_skills(self, skills: list[str] | None) -> list[str]:
        result: dict[str, str] = {}
        for skill in skills or []:
            canonical = self._canonical(skill)
            key = self._key(canonical)
            if key and key not in result:
                result[key] = canonical
        return sorted(result.values(), key=str.casefold)

    def extract_target_skills(self, role: str | None, description: str | None, db=None) -> list[str]:
        text = " ".join(item for item in (role or "", description or "") if item)
        return self.normalize_skills(skills_engine.extract(text, db=db, source="job" if db else None))

    def analyze(
        self,
        resume_skills: list[str] | None,
        target_skills: list[str] | None,
        *,
        role: str | None = None,
        job_description: str | None = None,
        market_counts: Counter | dict[str, int] | None = None,
    ) -> dict:
        resume = self.normalize_skills(resume_skills)
        target = self.normalize_skills(target_skills)
        resume_keys = {self._key(skill) for skill in resume}
        matched = [skill for skill in target if self._key(skill) in resume_keys]
        missing = [skill for skill in target if self._key(skill) not in resume_keys]
        description = (job_description or "").casefold()
        role_text = (role or "").casefold()
        details = []
        for skill in missing:
            key = self._key(skill)
            frequency = description.count(key)
            role_relevant = any(part in role_text for part in key.split() if len(part) > 2)
            priority = "HIGH" if frequency >= 2 or role_relevant else "MEDIUM" if frequency >= 1 else "LOW"
            market_value = (market_counts or {}).get(key)
            details.append({
                "skill": skill,
                "priority": priority,
                "reason": f"{skill} appears in the target requirements but was not detected in the resume.",
                "job_market": {"jobs": market_value, "status": "AVAILABLE" if market_value is not None else "INSUFFICIENT_DATA"},
            })
        details.sort(key=lambda item: ({"HIGH": 0, "MEDIUM": 1, "LOW": 2}[item["priority"]], item["skill"].casefold()))
        total = len(target)
        return {
            "match_percentage": round(len(matched) / total * 100, 2) if total else 0,
            "matched_skills": matched,
            "missing_skills": missing,
            "missing_skill_details": details,
            "explanations": {
                "matched": "Matched because the skill appears in both the resume and target requirements.",
                "missing": "Missing because the skill appears in the target requirements but was not detected in the resume.",
            },
        }

    def find_missing_skills(self, resume_skills: list[str], job_skills: list[str]) -> list[str]:
        return self.analyze(resume_skills, job_skills)["missing_skills"]


skill_gap_service = SkillGapService()
