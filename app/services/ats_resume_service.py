"""Evidence-based ATS analysis for already parsed resume text.

This service deliberately uses explainable heuristics. It does not invent
experience, projects, contacts, scores, or recommendations unsupported by the
resume and selected target.
"""

import re
from typing import Any

from app.jobs.job_skill_extractor import JobSkillExtractor


SECTION_ALIASES = {
    "summary": ("summary", "profile", "objective", "about me"),
    "experience": ("experience", "work experience", "employment", "work history"),
    "education": ("education", "academic background"),
    "projects": ("projects", "personal projects", "academic projects"),
    "certifications": ("certifications", "certificates"),
    "languages": ("languages", "language proficiency"),
    "skills": ("skills", "technical skills", "technologies", "competencies"),
}
ACTION_VERBS = {"built", "developed", "designed", "implemented", "improved", "created", "automated", "led", "optimized", "delivered", "deployed", "reduced", "increased"}


class ATSResumeService:
    def __init__(self) -> None:
        self.extractor = JobSkillExtractor()

    def analyze(self, text: str, resume_skills: list[str], *, target_role: str | None = None, target_company: str | None = None, job_description: str | None = None, target_missing_skills: list[str] | None = None) -> dict[str, Any]:
        normalized_text = text.casefold()
        sections = self._sections(text)
        contacts = self._contacts(text)
        target_keywords = self._keywords(target_role, target_company, job_description, target_missing_skills or [])
        matched = sorted({keyword for keyword in target_keywords if self._contains(normalized_text, keyword)})
        missing = sorted(set(target_keywords) - set(matched))
        components = {
            "skills_match": self._score(len(matched), len(target_keywords), 0 if target_keywords else min(100, len(resume_skills) * 5)),
            "resume_structure": self._section_score(sections),
            "keywords": self._score(len(matched), len(target_keywords), 70 if not target_keywords else 0),
            "experience": self._experience_score(sections.get("experience", "")),
            "education": self._presence_score(sections, "education"),
            "projects": self._project_score(sections.get("projects", "")),
            "formatting": self._formatting_score(text),
            "contact_information": self._contact_score(contacts),
        }
        overall = round(sum(components.values()) / len(components))
        return {
            "overall_score": overall,
            "components": {key: {"score": value, "explanation": self._explanation(key, value)} for key, value in components.items()},
            "contact_information": contacts,
            "sections": {key: bool(value.strip()) for key, value in sections.items()},
            "missing_sections": [key.title() for key, value in sections.items() if not value.strip()],
            "skills": sorted(set(resume_skills), key=str.casefold),
            "experience": self._section_summary(sections.get("experience", "")),
            "education": self._section_summary(sections.get("education", "")),
            "projects": self._project_analysis(sections.get("projects", ""), resume_skills),
            "certifications": self._lines(sections.get("certifications", "")),
            "languages": self._lines(sections.get("languages", "")),
            "summary": sections.get("summary", "").strip(),
            "keywords": {"matched": matched, "missing": missing, "recommended": missing[:12], "match_percentage": self._score(len(matched), len(target_keywords), 0 if target_keywords else 0), "target_role": target_role, "target_company": target_company},
            "skill_gap": {"current": sorted(set(resume_skills), key=str.casefold), "missing": target_missing_skills or missing, "strong": matched, "weak": missing[:], "priority": missing[:8], "estimated_learning_days": 7 * min(12, len(target_missing_skills or missing))},
            "improvements": self._improvements(components, sections, missing),
            "analysis_basis": "Resume text, extracted skills, and the selected target/job description only.",
        }

    @staticmethod
    def _sections(text: str) -> dict[str, str]:
        lines = text.splitlines()
        found: dict[str, list[str]] = {key: [] for key in SECTION_ALIASES}
        current: str | None = None
        aliases = {alias.casefold(): key for key, values in SECTION_ALIASES.items() for alias in values}
        for line in lines:
            heading = re.sub(r"[^a-z ]", "", line.casefold()).strip()
            if heading in aliases and len(line.strip()) <= 50:
                current = aliases[heading]
                continue
            if current:
                found[current].append(line)
        return {key: "\n".join(value).strip() for key, value in found.items()}

    @staticmethod
    def _contacts(text: str) -> dict[str, str | None]:
        links = re.findall(r"https?://[^\s)]+", text, re.IGNORECASE)
        lower = text.casefold()
        return {"name": next((line.strip() for line in text.splitlines() if line.strip() and len(line.strip()) < 80 and not re.search(r"@|https?://|\d", line)), None), "email": next(iter(re.findall(r"[\w.+-]+@[\w-]+\.[\w.-]+", text)), None), "phone": next(iter(re.findall(r"(?:\+?\d[\d ()-]{8,}\d)", text)), None), "linkedin": next((link for link in links if "linkedin.com" in link.casefold()), None), "github": next((link for link in links if "github.com" in link.casefold()), None), "portfolio": next((link for link in links if "linkedin.com" not in link.casefold() and "github.com" not in link.casefold()), None), "email_present": "@" in lower}

    def _keywords(self, role: str | None, company: str | None, description: str | None, missing: list[str]) -> set[str]:
        values = set(missing)
        if description:
            values.update(self.extractor.extract_skills(description))
        if role:
            values.update(word for word in re.findall(r"[a-zA-Z][a-zA-Z+#.]{2,}", role) if word.casefold() not in {"engineer", "developer", "senior", "junior"})
        return {value.strip().casefold() for value in values if value and value.strip()}

    @staticmethod
    def _contains(text: str, keyword: str) -> bool:
        return keyword in text

    @staticmethod
    def _score(numerator: int, denominator: int, fallback: int) -> int:
        return round(numerator / denominator * 100) if denominator else fallback

    @staticmethod
    def _presence_score(sections: dict[str, str], key: str) -> int:
        return 100 if sections.get(key, "").strip() else 0

    @staticmethod
    def _section_score(sections: dict[str, str]) -> int:
        return round(sum(bool(value.strip()) for value in sections.values()) / len(sections) * 100)

    @staticmethod
    def _experience_score(value: str) -> int:
        if not value.strip(): return 0
        return min(100, 45 + len(re.findall(r"\d+%|\$?\d+", value)) * 10 + len(set(re.findall(r"\b[a-z]+ed\b", value.casefold()))) * 3)

    @staticmethod
    def _project_score(value: str) -> int:
        if not value.strip(): return 0
        return min(100, 40 + len(value.splitlines()) * 5)

    @staticmethod
    def _formatting_score(text: str) -> int:
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        if not lines: return 0
        long_lines = sum(len(line) > 180 for line in lines)
        bullet_lines = sum(line.startswith(("-", "•", "*")) for line in lines)
        return max(0, min(100, 100 - long_lines * 8 + min(10, bullet_lines)))

    @staticmethod
    def _contact_score(contacts: dict[str, str | None]) -> int:
        return round(sum(bool(contacts.get(key)) for key in ("name", "email", "phone")) / 3 * 100)

    @staticmethod
    def _lines(value: str) -> list[str]:
        return [line.strip(" -•*") for line in value.splitlines() if line.strip()]

    def _section_summary(self, value: str) -> dict[str, Any]:
        lines = self._lines(value)
        return {"present": bool(lines), "items": lines[:20], "count": len(lines)}

    def _project_analysis(self, value: str, skills: list[str]) -> list[dict[str, Any]]:
        lines = self._lines(value)
        if not lines: return []
        return [{"title": line[:120], "complexity": "Evidence unavailable" if len(line) < 80 else "Detailed", "technology_match": [skill for skill in skills if skill.casefold() in line.casefold()], "relevance": "Based on project description evidence", "improvement": "Add measurable impact, scale, or outcome." if not re.search(r"\d+%|\d+ users|\d+ms", line, re.IGNORECASE) else "Keep the measurable outcome."} for line in lines[:10]]

    @staticmethod
    def _improvements(components: dict[str, int], sections: dict[str, str], missing: list[str]) -> dict[str, list[str]]:
        improvements: dict[str, list[str]] = {"summary": [], "projects": [], "action_verbs": [], "technical_keywords": missing[:12], "achievement_statements": [], "formatting": [], "section_order": []}
        if not sections.get("summary", "").strip(): improvements["summary"].append("Add a concise summary aligned to the selected role.")
        if not sections.get("projects", "").strip(): improvements["projects"].append("Add relevant projects with technology, contribution, and outcome.")
        if components["experience"] < 70: improvements["achievement_statements"].append("Quantify outcomes with percentages, scale, latency, revenue, or users where supported by your experience.")
        improvements["action_verbs"] = sorted(ACTION_VERBS)
        if components["formatting"] < 80: improvements["formatting"].append("Use consistent bullets and shorter lines for parser compatibility.")
        improvements["section_order"].append("Recommended order: contact, summary, skills, experience, projects, education, certifications.")
        return improvements

    @staticmethod
    def _explanation(key: str, score: int) -> str:
        return f"{key.replace('_', ' ').title()} evidence score: {score}/100 based on parsed resume content."


ats_resume_service = ATSResumeService()
