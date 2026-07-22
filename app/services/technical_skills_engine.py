"""Cached, lightweight recognition of technical skills."""
import json
import re
from datetime import UTC, datetime
from pathlib import Path

from sqlalchemy.orm import Session

from app.models.unknown_skill import UnknownSkill


class TechnicalSkillsEngine:
    def __init__(self) -> None:
        self._aliases: dict[str, str] = {}
        self._pattern: re.Pattern[str] | None = None
        path = Path(__file__).resolve().parents[1] / "data" / "technical_skills.json"
        with path.open(encoding="utf-8") as file:
            for canonical, aliases in json.load(file).items():
                self.add_skill(canonical, aliases, rebuild=False)
        self._rebuild()

    @staticmethod
    def normalize(value: str) -> str:
        return re.sub(r"\s+", " ", value.strip().casefold())

    def _rebuild(self) -> None:
        alternatives = "|".join(re.escape(value) for value in sorted(self._aliases, key=len, reverse=True))
        self._pattern = re.compile(rf"(?<![\w+#.])(?:{alternatives})(?![\w+#.])", re.IGNORECASE) if alternatives else None

    def add_skill(self, canonical: str, aliases: list[str] | None = None, rebuild: bool = True) -> None:
        canonical = canonical.strip()
        self._aliases[self.normalize(canonical)] = canonical
        for alias in aliases or []:
            self._aliases[self.normalize(alias)] = canonical
        if rebuild:
            self._rebuild()

    def load_approved_skills(self, db: Session) -> None:
        for skill in db.query(UnknownSkill).filter(UnknownSkill.status == "approved"):
            self.add_skill(skill.skill_name)

    def extract(self, text: str, db: Session | None = None, source: str | None = None) -> list[str]:
        clean = re.sub(r"<[^>]+>", " ", text or "")
        result = {self._aliases[self.normalize(match.group())] for match in self._pattern.finditer(clean)} if self._pattern else set()
        if db is not None and source in {"resume", "job"}:
            self._record_unknowns(clean, source, db)
        return sorted(result, key=str.casefold)

    def _record_unknowns(self, text: str, source: str, db: Session) -> None:
        candidates: dict[str, str] = {}
        for match in re.finditer(r"(?:technical\s+)?(?:skills?|technologies|tools|frameworks?|languages?)\s*[:\-]\s*([^\n]{1,300})", text, re.IGNORECASE):
            for item in re.split(r"[,;|/â€¢]", match.group(1)):
                name = re.sub(r"\s+", " ", item).strip(" .:-()[]")
                key = self.normalize(name)
                if 2 <= len(name) <= 80 and key not in self._aliases and re.fullmatch(r"[A-Za-z0-9+#. -]+", name):
                    candidates[key] = name
        if not candidates:
            return

        now = datetime.now(UTC)
        existing = {
            item.normalized_name: item
            for item in db.query(UnknownSkill).filter(UnknownSkill.normalized_name.in_(candidates)).all()
        }
        existing.update({
            item.normalized_name: item
            for item in db.new
            if isinstance(item, UnknownSkill) and item.normalized_name in candidates
        })
        for key, name in candidates.items():
            skill = existing.get(key)
            if skill:
                skill.frequency += 1
                skill.last_seen = now
                if source not in skill.source.split(","):
                    skill.source = f"{skill.source},{source}"
            else:
                skill = UnknownSkill(skill_name=name, normalized_name=key, source=source, first_seen=now, last_seen=now)
                db.add(skill)
                existing[key] = skill


skills_engine = TechnicalSkillsEngine()
