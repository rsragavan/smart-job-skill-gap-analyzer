from datetime import UTC, date, datetime, timedelta
from typing import Any

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.gamification import Achievement, GamificationEvent, UserBadge, UserGamification
from app.models.learning_progress import LearningProgress
from app.roadmap.reward_system import BADGES, XP_RULES, get_level, next_level


class GamificationService:
    def __init__(self, db: Session):
        self.db = db

    def get_or_create_state(self, user_id: int) -> UserGamification:
        state = self.db.query(UserGamification).filter_by(user_id=user_id).first()
        if state is None:
            state = UserGamification(user_id=user_id)
            self.db.add(state)
            self.db.flush()
        return state

    def process_completion(self, user_id: int, roadmap_id: str, skill_key: str, became_completed: bool) -> None:
        state = self.get_or_create_state(user_id)
        items = self._learning_items(user_id)
        if became_completed:
            self._record_activity(state)
            self._update_goals(state, user_id)
        self._recalculate_xp(user_id, state, items)
        self._sync_badges_and_achievements(user_id, state, items)

    def dashboard(self, user_id: int) -> dict[str, Any]:
        state = self.get_or_create_state(user_id)
        items = self._learning_items(user_id)
        self._recalculate_xp(user_id, state, items)
        self._sync_badges_and_achievements(user_id, state, items)
        current = get_level(state.total_xp)
        upcoming = next_level(state.total_xp)
        level_span = (upcoming["xp"] - current["xp"]) if upcoming else 1
        level_progress = min(100, max(0, ((state.total_xp - current["xp"]) / level_span) * 100))
        return {
            "total_xp": state.total_xp,
            "current_level": current,
            "next_level": upcoming,
            "level_progress": round(level_progress, 1),
            "current_streak": state.current_streak,
            "longest_streak": state.longest_streak,
            "daily_goal": {"target": state.daily_goal_target, "progress": state.daily_goal_progress, "completed": state.daily_goal_progress >= state.daily_goal_target},
            "weekly_goal": {"target": state.weekly_goal_target, "progress": state.weekly_goal_progress, "completed": state.weekly_goal_progress >= state.weekly_goal_target},
            "badges": [self._badge_dict(badge) for badge in self.db.query(UserBadge).filter_by(user_id=user_id).order_by(UserBadge.unlocked_at.desc()).all()],
            "achievements": [self._achievement_dict(item) for item in self.db.query(Achievement).filter_by(user_id=user_id).order_by(Achievement.unlocked_at.desc()).all()],
        }

    def _record_activity(self, state: UserGamification) -> None:
        today = datetime.now(UTC).date()
        if state.last_activity_date == today:
            return
        if state.last_activity_date == today - timedelta(days=1):
            state.current_streak += 1
        else:
            state.current_streak = 1
        state.longest_streak = max(state.longest_streak, state.current_streak)
        state.last_activity_date = today

    def _update_goals(self, state: UserGamification, user_id: int) -> None:
        today = datetime.now(UTC).date()
        monday = today - timedelta(days=today.weekday())
        if state.daily_goal_date != today:
            state.daily_goal_date = today
            state.daily_goal_progress = 0
        if state.weekly_goal_week_start != monday:
            state.weekly_goal_week_start = monday
            state.weekly_goal_progress = 0
        state.daily_goal_progress += 1
        state.weekly_goal_progress += 1
        if state.daily_goal_progress == state.daily_goal_target:
            self._add_event(user_id, f"daily-goal:{today.isoformat()}", "daily_goal", XP_RULES["daily_goal"])
        if state.weekly_goal_progress == state.weekly_goal_target:
            self._add_event(user_id, f"weekly-goal:{monday.isoformat()}", "weekly_goal", XP_RULES["weekly_goal"])

    def _add_event(self, user_id: int, event_key: str, event_type: str, xp: int) -> None:
        if self.db.query(GamificationEvent).filter_by(user_id=user_id, event_key=event_key).first() is None:
            self.db.add(GamificationEvent(user_id=user_id, event_key=event_key, event_type=event_type, xp=xp))

    def _recalculate_xp(self, user_id: int, state: UserGamification, items: list[LearningProgress]) -> None:
        item_xp = sum(item.xp_earned for item in items)
        topic_groups: dict[tuple[str, str], list[LearningProgress]] = {}
        for item in items:
            if item.item_type == "topic":
                topic_groups.setdefault((item.roadmap_id, item.skill_key), []).append(item)
        completed_skills = sum(bool(rows) and all(item.status == "completed" for item in rows) for rows in topic_groups.values())
        goal_xp = self.db.query(func.coalesce(func.sum(GamificationEvent.xp), 0)).filter(
            GamificationEvent.user_id == user_id,
            GamificationEvent.event_type.in_(("daily_goal", "weekly_goal")),
        ).scalar() or 0
        state.total_xp = item_xp + completed_skills * XP_RULES["complete_skill"] + int(goal_xp)
        state.level = get_level(state.total_xp)["level"]

    def _sync_badges_and_achievements(self, user_id: int, state: UserGamification, items: list[LearningProgress]) -> None:
        skills = self._completed_skill_count(items)
        projects = sum(item.item_type == "project" and item.status == "completed" for item in items)
        roadmap_complete = bool(items) and all(item.status == "completed" for item in items)
        conditions = {
            "first-skill": skills >= 1,
            "first-project": projects >= 1,
            "ten-skills": skills >= 10,
            "seven-day-streak": state.current_streak >= 7,
            "thirty-day-streak": state.current_streak >= 30,
            "roadmap-complete": bool(roadmap_complete),
            "company-ready": bool(roadmap_complete and projects >= 1),
        }
        definitions = {item["key"]: item for item in BADGES}
        badge_keys = {item.badge_key for item in self.db.query(UserBadge).filter_by(user_id=user_id).all()}
        achievement_keys = {item.achievement_key for item in self.db.query(Achievement).filter_by(user_id=user_id).all()}
        for key, unlocked in conditions.items():
            if not unlocked:
                continue
            definition = definitions[key]
            if key not in badge_keys:
                self.db.add(UserBadge(user_id=user_id, badge_key=key, name=definition["name"], description=definition["description"]))
            if key not in achievement_keys:
                self.db.add(Achievement(user_id=user_id, achievement_key=key, name=definition["name"], description=definition["description"]))

    @staticmethod
    def _completed_skill_count(items: list[LearningProgress]) -> int:
        groups: dict[tuple[str, str], list[LearningProgress]] = {}
        for item in items:
            if item.item_type == "topic":
                groups.setdefault((item.roadmap_id, item.skill_key), []).append(item)
        return sum(bool(rows) and all(item.status == "completed" for item in rows) for rows in groups.values())

    def _learning_items(self, user_id: int) -> list[LearningProgress]:
        return self.db.query(LearningProgress).filter_by(user_id=user_id).all()

    @staticmethod
    def _badge_dict(item: UserBadge) -> dict[str, Any]:
        return {"key": item.badge_key, "name": item.name, "description": item.description, "unlocked_at": item.unlocked_at.isoformat()}

    @staticmethod
    def _achievement_dict(item: Achievement) -> dict[str, Any]:
        return {"key": item.achievement_key, "name": item.name, "description": item.description, "unlocked_at": item.unlocked_at.isoformat()}
