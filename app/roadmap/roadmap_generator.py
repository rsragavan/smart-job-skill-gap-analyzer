"""
app/roadmap/roadmap_generator.py

Creates complete personalized learning roadmaps by combining metadata
from all four synchronized roadmap libraries with robust fallback support.
"""

from typing import Any, Dict, List

from app.roadmap.skill_library import get_normalized_skill_key, get_skill_metadata
from app.roadmap.resource_library import get_resources
from app.roadmap.project_library import get_projects
from app.roadmap.milestone_library import get_milestones
from app.roadmap.roadmap_priorities import ROADMAP_DEPENDENCIES, ROADMAP_PRIORITIES


class RoadmapGenerator:
    """Generates structured, step-by-step skill gap roadmaps."""

    def generate(self, skills: List[str]) -> List[Dict[str, Any]]:
        """
        Generates a list of ordered roadmap items for provided skills.

        Args:
            skills: List of skill names (e.g. ["Python", "FastAPI", "Docker"]).

        Returns:
            List of roadmap item dictionaries containing priority, metadata,
            resources, projects, and milestones.
        """
        candidates: list[tuple[int, str, str]] = []
        seen: set[str] = set()
        for index, raw_skill in enumerate(skills):
            if not raw_skill or not raw_skill.strip():
                continue
            skill_key = get_normalized_skill_key(raw_skill)
            if skill_key in seen:
                continue
            seen.add(skill_key)
            candidates.append((index, raw_skill.strip(), skill_key))

        candidates.sort(key=lambda item: (ROADMAP_PRIORITIES.get(item[2], 999), item[0]))
        roadmap: List[Dict[str, Any]] = []

        for priority, (_, raw_skill, skill_key) in enumerate(candidates, start=1):

            skill_info = get_skill_metadata(skill_key)
            resources = get_resources(skill_key)
            projects = get_projects(skill_key)
            milestones = get_milestones(skill_key)

            roadmap.append(
                {
                    "priority": priority,
                    "skill_key": skill_key,
                    "skill": skill_info.get("name", raw_skill.strip().title()),
                    "category": skill_info.get("category", "General Software Engineering"),
                    "difficulty": skill_info.get("difficulty", "Intermediate"),
                    "estimated_days": skill_info.get("estimated_days", 10),
                    "xp": skill_info.get("xp", 200),
                    "description": skill_info.get("description", ""),
                    "topics": skill_info.get("topics", []),
                    "dependencies": ROADMAP_DEPENDENCIES.get(skill_key, []),
                    "resources": resources,
                    "projects": projects,
                    "milestones": milestones,
                }
            )

        return roadmap
