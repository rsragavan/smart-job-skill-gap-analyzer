"""
Roadmap Service

Business logic between API and Roadmap Engine.
"""

from app.roadmap.roadmap_engine import roadmap_engine


class RoadmapService:

    def generate(
        self,
        company: str,
        role: str,
        match_percentage: float,
        matched_skills: list[str],
        missing_skills: list[str],
    ):

        return roadmap_engine.generate_company_roadmap(
            company=company,
            role=role,
            match_percentage=match_percentage,
            matched_skills=matched_skills,
            missing_skills=missing_skills,
        )


roadmap_service = RoadmapService()