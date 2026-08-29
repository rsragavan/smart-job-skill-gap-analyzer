"""
Roadmap Priorities

Defines the learning order for every skill.

Lower number = Higher priority.
"""

ROADMAP_PRIORITIES = {

    # -----------------------------
    # Programming Languages
    # -----------------------------

    "c": 1,
    "python": 1,
    "java": 1,
    "javascript": 1,

    # -----------------------------
    # Core Programming
    # -----------------------------

    "oop": 2,
    "dsa": 2,
    "problem solving": 2,

    # -----------------------------
    # Version Control
    # -----------------------------

    "git": 3,
    "github": 3,

    # -----------------------------
    # Web Fundamentals
    # -----------------------------

    "html": 4,
    "css": 4,

    # -----------------------------
    # Databases
    # -----------------------------

    "sql": 5,
    "mysql": 5,
    "postgresql": 5,

    # -----------------------------
    # Backend
    # -----------------------------

    "rest api": 6,
    "fastapi": 6,
    "flask": 6,
    "django": 6,
    "spring": 6,
    "spring boot": 6,
    "jwt": 6,

    # -----------------------------
    # Frontend
    # -----------------------------

    "react": 7,

    # -----------------------------
    # DevOps
    # -----------------------------

    "docker": 8,
    "linux": 8,

    # -----------------------------
    # Cloud
    # -----------------------------

    "aws": 9,
    "azure": 9,
    "gcp": 9,

    # -----------------------------
    # Containers
    # -----------------------------

    "kubernetes": 10,

}

# Lightweight prerequisites used to order learning without requiring a graph
# database. Dependencies may already be present in a user's resume; they are
# still exposed so the learner understands why a skill comes later.
ROADMAP_DEPENDENCIES = {
    "spring": ["java"],
    "spring_boot": ["java", "spring"],
    "fastapi": ["python"],
    "django": ["python"],
    "react": ["javascript"],
    "typescript": ["javascript"],
    "docker": ["linux"],
    "kubernetes": ["docker"],
    "aws": ["linux"],
    "rest_api": ["http"],
    "postgresql": ["sql"],
}
