"""Validate that every curated skill has a complete roadmap definition."""

import sys

from app.roadmap.milestone_library import MILESTONE_LIBRARY
from app.roadmap.project_library import PROJECT_LIBRARY
from app.roadmap.resource_library import RESOURCE_LIBRARY
from app.roadmap.skill_library import SKILL_LIBRARY


def verify_roadmap_libraries() -> bool:
    libraries = {
        "skill_library": set(SKILL_LIBRARY),
        "resource_library": set(RESOURCE_LIBRARY),
        "project_library": set(PROJECT_LIBRARY),
        "milestone_library": set(MILESTONE_LIBRARY),
    }
    canonical = libraries["skill_library"]
    errors: list[str] = []

    for name, keys in libraries.items():
        missing = sorted(canonical - keys)
        extra = sorted(keys - canonical)
        if missing:
            errors.append(f"{name} missing: {missing}")
        if extra:
            errors.append(f"{name} extra: {extra}")

    for key, metadata in SKILL_LIBRARY.items():
        for field in ("name", "difficulty", "estimated_days", "xp", "topics"):
            if not metadata.get(field):
                errors.append(f"skill_library[{key}] missing {field}")
    for name, library in (
        ("resource_library", RESOURCE_LIBRARY),
        ("project_library", PROJECT_LIBRARY),
        ("milestone_library", MILESTONE_LIBRARY),
    ):
        for key, entries in library.items():
            if not entries:
                errors.append(f"{name}[{key}] has no entries")
            titles = [entry.get("title") for entry in entries]
            if len(titles) != len(set(titles)):
                errors.append(f"{name}[{key}] contains duplicate titles")

    print("Roadmap library verification")
    print(f"Skills: {len(canonical)}")
    print(f"Resources: {len(RESOURCE_LIBRARY)}")
    print(f"Projects: {len(PROJECT_LIBRARY)}")
    print(f"Milestones: {len(MILESTONE_LIBRARY)}")
    if errors:
        print("FAILED")
        print("\n".join(errors))
        return False
    print("PASSED: all curated skills are synchronized and populated")
    return True


if __name__ == "__main__":
    sys.exit(0 if verify_roadmap_libraries() else 1)
