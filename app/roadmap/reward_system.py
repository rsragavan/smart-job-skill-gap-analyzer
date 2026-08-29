"""Shared XP, level, and badge definitions for the learning experience."""

XP_RULES = {
    "watch_resource": 10,
    "complete_topic": 20,
    "complete_project": 100,
    "complete_skill": 250,
    "daily_goal": 50,
    "weekly_goal": 300,
}

LEVELS = [
    {"level": 1, "title": "Beginner", "xp": 0},
    {"level": 2, "title": "Intermediate", "xp": 250},
    {"level": 3, "title": "Advanced", "xp": 750},
    {"level": 4, "title": "Professional", "xp": 1500},
    {"level": 5, "title": "Expert", "xp": 3000},
    {"level": 6, "title": "Master", "xp": 6000},
]

BADGES = [
    {"key": "first-skill", "name": "First Skill", "description": "Complete your first skill."},
    {"key": "first-project", "name": "First Project", "description": "Complete your first project."},
    {"key": "ten-skills", "name": "10 Skills", "description": "Complete ten skills."},
    {"key": "seven-day-streak", "name": "7 Day Streak", "description": "Learn for seven consecutive days."},
    {"key": "thirty-day-streak", "name": "30 Day Streak", "description": "Learn for thirty consecutive days."},
    {"key": "roadmap-complete", "name": "Roadmap Complete", "description": "Complete every skill in a roadmap."},
    {"key": "company-ready", "name": "Company Ready", "description": "Complete a full roadmap and its projects."},
]


def get_level(total_xp: int) -> dict:
    current = LEVELS[0]
    for level in LEVELS:
        if total_xp >= level["xp"]:
            current = level
    return current


def next_level(total_xp: int) -> dict | None:
    return next((level for level in LEVELS if total_xp < level["xp"]), None)


def daily_reward(streak: int) -> int:
    return XP_RULES["daily_goal"]
