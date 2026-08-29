
import hashlib
import json

from app.roadmap.roadmap_generator import RoadmapGenerator
from app.roadmap.reward_system import get_level


class RoadmapEngine:

    def __init__(self):
        self.generator = RoadmapGenerator()

    def generate_company_roadmap(
        self,
        company: str,
        role: str,
        match_percentage: float,
        matched_skills: list[str],
        missing_skills: list[str],
    ):
        normalized_missing = list(dict.fromkeys(
            skill.strip() for skill in missing_skills if skill and skill.strip()
        ))
        roadmap = self.generator.generate(normalized_missing)
        roadmap_id = hashlib.sha256(
            json.dumps(
                {
                    "company": company.strip().casefold(),
                    "role": role.strip().casefold(),
                    "skills": [item["skill_key"] for item in roadmap],
                },
                sort_keys=True,
            ).encode("utf-8")
        ).hexdigest()[:32]

        total_days = sum(
            item.get("estimated_days", 15)
            for item in roadmap
        )

        # FIX: Sum the XP from the skill item directly,
        # using a safe .get() in case a skill is missing the key.
        total_xp = sum(
            item.get("xp", 200)
            for item in roadmap
        )

        level = get_level(total_xp)

        return {
            "company": company,
            "role": role,
            "roadmap_id": roadmap_id,
            "match_percentage": max(0, min(100, match_percentage)),
            "matched_skills": matched_skills,
            "missing_skills": normalized_missing,
            "estimated_days": total_days,
            "total_xp": total_xp,
            "current_level": level,
            "roadmap": roadmap,
        }


roadmap_engine = RoadmapEngine()
