import re
from typing import Any

from sqlalchemy.orm import Session

from app.models.learning_progress import LearningProgress
from app.roadmap.reward_system import XP_RULES
from app.services.gamification_service import GamificationService


MISSION_TEMPLATES = (
    ("watch-course", "Watch Course", XP_RULES["watch_resource"]),
    ("read-documentation", "Read Documentation", XP_RULES["watch_resource"]),
    ("solve-problems", "Solve Problems", XP_RULES["watch_resource"]),
    ("complete-quiz", "Complete Quiz", XP_RULES["watch_resource"]),
    ("build-mini-project", "Build Mini Project", XP_RULES["watch_resource"]),
)
XP_BY_TYPE = {"topic": XP_RULES["complete_topic"], "project": XP_RULES["complete_project"], "mission": XP_RULES["watch_resource"]}
VALID_TYPES = set(XP_BY_TYPE)
VALID_STATUSES = {"not_started", "in_progress", "completed"}


def _slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.casefold()).strip("-")


def _topic_value(topic: Any, index: int) -> tuple[str, str]:
    if isinstance(topic, str):
        return f"topic-{index + 1}-{_slug(topic)}", topic
    title = str(topic.get("title") or topic.get("name") or f"Topic {index + 1}")
    return f"topic-{index + 1}-{_slug(title)}", title


def _project_value(project: Any, index: int) -> tuple[str, str]:
    if isinstance(project, str):
        return f"project-{index + 1}-{_slug(project)}", project
    title = str(project.get("title") or project.get("name") or f"Project {index + 1}")
    return f"project-{index + 1}-{_slug(title)}", title


class LearningProgressService:
    def __init__(self, db: Session):
        self.db = db

    def sync(self, user_id: int, roadmap_id: str, roadmap: list[dict[str, Any]]) -> dict[str, Any]:
        existing = {
            (item.skill_key, item.item_type, item.item_key)
            for item in self.db.query(LearningProgress).filter_by(user_id=user_id, roadmap_id=roadmap_id).all()
        }
        for skill in roadmap:
            skill_key = str(skill.get("skill_key") or _slug(str(skill.get("skill") or "skill")))[:120]
            for index, topic in enumerate(skill.get("topics") or []):
                item_key, _ = _topic_value(topic, index)
                self._ensure_item(user_id, roadmap_id, skill_key, "topic", item_key, existing)
            for index, project in enumerate(skill.get("projects") or []):
                item_key, _ = _project_value(project, index)
                self._ensure_item(user_id, roadmap_id, skill_key, "project", item_key, existing)
            for item_key, _, _ in MISSION_TEMPLATES:
                self._ensure_item(user_id, roadmap_id, skill_key, "mission", item_key, existing)
        GamificationService(self.db).get_or_create_state(user_id)
        self.db.commit()
        return self.get_progress(user_id, roadmap_id)

    def update(self, user_id: int, roadmap_id: str, skill_key: str, item_type: str, item_key: str, status: str) -> dict[str, Any]:
        if item_type not in VALID_TYPES:
            raise ValueError("Unsupported learning item type")
        if status not in VALID_STATUSES:
            raise ValueError("Unsupported learning status")
        item = (
            self.db.query(LearningProgress)
            .filter_by(
                user_id=user_id,
                roadmap_id=roadmap_id,
                skill_key=skill_key,
                item_type=item_type,
                item_key=item_key,
            )
            .first()
        )
        if item is None:
            raise LookupError("Learning item not found")
        if item_type == "project":
            parts = item_key.split("-", 2)
            if len(parts) > 1 and parts[1].isdigit() and int(parts[1]) > 1:
                previous_key = f"project-{int(parts[1]) - 1}-"
                previous = (
                    self.db.query(LearningProgress)
                    .filter(
                        LearningProgress.user_id == user_id,
                        LearningProgress.roadmap_id == roadmap_id,
                        LearningProgress.skill_key == skill_key,
                        LearningProgress.item_type == "project",
                        LearningProgress.item_key.like(f"{previous_key}%"),
                    )
                    .first()
                )
                if previous is not None and previous.status != "completed":
                    raise PermissionError("Complete the previous project first")
        became_completed = item.status != "completed" and status == "completed"
        item.status = status
        item.xp_earned = XP_BY_TYPE[item_type] if status == "completed" else 0
        self.db.commit()
        GamificationService(self.db).process_completion(user_id, roadmap_id, skill_key, became_completed)
        self.db.commit()
        return self.get_progress(user_id, roadmap_id)

    def get_progress(self, user_id: int, roadmap_id: str) -> dict[str, Any]:
        items = self.db.query(LearningProgress).filter_by(user_id=user_id, roadmap_id=roadmap_id).all()
        gamification = GamificationService(self.db)
        dashboard = gamification.dashboard(user_id)
        self.db.commit()
        return {
            "roadmap_id": roadmap_id,
            "items": [
                {
                    "skill_key": item.skill_key,
                    "item_type": item.item_type,
                    "item_key": item.item_key,
                    "status": item.status,
                    "xp_earned": item.xp_earned,
                }
                for item in items
            ],
            "total_xp": dashboard["total_xp"],
            "current_level": dashboard["current_level"],
            "next_level": dashboard["next_level"],
            "gamification": dashboard,
        }

    def _ensure_item(self, user_id: int, roadmap_id: str, skill_key: str, item_type: str, item_key: str, existing: set[tuple[str, str, str]]) -> None:
        item_identity = (skill_key, item_type, item_key)
        if item_identity not in existing:
            self.db.add(LearningProgress(
                user_id=user_id,
                roadmap_id=roadmap_id,
                skill_key=skill_key,
                item_type=item_type,
                item_key=item_key,
            ))
            existing.add(item_identity)
