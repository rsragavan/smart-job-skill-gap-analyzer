"""Consistent, useful defaults for skills outside the curated libraries."""

from urllib.parse import quote_plus


def display_skill_name(skill_name: str) -> str:
    cleaned = " ".join((skill_name or "Specialized Technology").replace("_", " ").split())
    return cleaned.title()


def _profile(skill_name: str) -> tuple[str, int, int]:
    normalized = skill_name.casefold()
    if any(term in normalized for term in ("architecture", "distributed", "kubernetes", "security", "mlops", "machine learning")):
        return "Advanced", 18, 320
    if any(term in normalized for term in ("html", "css", "basics", "fundamentals")):
        return "Beginner", 8, 140
    return "Intermediate", 12, 220


def get_unknown_skill_metadata(skill_name: str) -> dict:
    name = display_skill_name(skill_name)
    difficulty, estimated_days, xp = _profile(name)
    return {
        "name": name,
        "category": "Emerging Technologies",
        "difficulty": difficulty,
        "estimated_days": estimated_days,
        "xp": xp,
        "description": f"A practical learning path for applying {name} in production software projects.",
        "topics": [
            f"{name} fundamentals and terminology",
            f"{name} setup, workflow, and core patterns",
            f"Building a practical project with {name}",
            f"Testing, security, and production best practices for {name}",
        ],
    }


def get_unknown_resources(skill_name: str) -> list[dict[str, str]]:
    name = display_skill_name(skill_name)
    query = quote_plus(f"{name} official documentation tutorial")
    return [
        {"title": f"{name} official documentation", "url": f"https://www.google.com/search?q={query}", "type": "Documentation"},
        {"title": f"{name} fundamentals tutorial", "url": f"https://www.youtube.com/results?search_query={query}", "type": "Tutorial"},
    ]


def get_unknown_projects(skill_name: str) -> list[dict[str, str]]:
    name = display_skill_name(skill_name)
    return [
        {"title": f"{name} starter implementation", "description": f"Build a small application that demonstrates the core workflow and integration points of {name}."},
        {"title": f"Production-ready {name} service", "description": f"Extend the starter implementation with validation, tests, observability, and deployment documentation for {name}."},
    ]


def get_unknown_milestones(skill_name: str) -> list[dict[str, str]]:
    name = display_skill_name(skill_name)
    return [
        {"title": f"Understand {name} fundamentals", "description": f"Explain the core concepts, vocabulary, and common use cases of {name}."},
        {"title": f"Build with {name}", "description": f"Complete a working project using {name} and document the implementation decisions."},
        {"title": f"Apply {name} in production", "description": f"Add testing, security, performance checks, and deployment guidance for {name}."},
    ]
