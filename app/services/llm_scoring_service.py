"""LLM-powered interview answer scoring using Google Gemini API.

Falls back to the existing heuristic scorer when:
- GEMINI_API_KEY is not configured
- The API call fails or times out
- The response cannot be parsed

This ensures zero regression — existing behaviour is preserved unless
the API key is explicitly set.
"""

from __future__ import annotations

import json
import logging
import re

logger = logging.getLogger(__name__)

_SCORE_PROMPT = """You are an expert technical interviewer. Score the following interview answer.

Question: {question}

Candidate's Answer: {answer}

Evaluate the answer and respond with ONLY a valid JSON object in this exact format:
{{
  "score": <integer 0-100>,
  "feedback": "<one or two sentence feedback explaining the score>"
}}

Scoring guide:
- 0-20: No relevant content or completely wrong
- 21-49: Partially relevant but missing key concepts
- 50-69: Addresses the question but lacks depth or examples
- 70-85: Good answer with clear explanation
- 86-100: Excellent answer with concepts, reasoning, and examples
"""


class LLMScoringService:
    def __init__(self) -> None:
        self._client = None
        self._available: bool | None = None

    def _load(self) -> bool:
        if self._available is not None:
            return self._available
        try:
            from app.core.config import settings
            api_key = getattr(settings, "GEMINI_API_KEY", "")
            if not api_key:
                self._available = False
                logger.info("LLM scoring disabled: GEMINI_API_KEY not set, using heuristic fallback.")
                return False
            import google.generativeai as genai  # type: ignore
            genai.configure(api_key=api_key)
            self._client = genai.GenerativeModel("gemini-1.5-flash")
            self._available = True
            logger.info("LLM scoring enabled via Gemini API.")
        except Exception as exc:
            self._available = False
            logger.warning("LLM scoring unavailable: %s", exc)
        return self._available  # type: ignore[return-value]

    def score_answer(self, question: str, answer: str) -> tuple[int, str]:
        """
        Returns (score 0-100, feedback string).
        Falls back to heuristic if LLM is unavailable.
        """
        if not answer or not answer.strip():
            return 0, "No answer was provided."

        if not self._load() or self._client is None:
            return self._heuristic_score(question, answer)

        try:
            prompt = _SCORE_PROMPT.format(question=question.strip(), answer=answer.strip())
            response = self._client.generate_content(prompt)
            text = response.text.strip()
            # Strip markdown code fences if present
            text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text, flags=re.MULTILINE).strip()
            data = json.loads(text)
            score = max(0, min(100, int(data["score"])))
            feedback = str(data.get("feedback", "")).strip() or self._feedback_for_score(score)
            return score, feedback
        except Exception as exc:
            logger.warning("LLM scoring failed, using heuristic fallback: %s", exc)
            return self._heuristic_score(question, answer)

    @staticmethod
    def _heuristic_score(question: str, answer: str) -> tuple[int, str]:
        """Original heuristic scorer preserved as fallback."""
        normalized = re.findall(r"[a-z][a-z0-9+#.-]*", (answer or "").casefold())
        non_answers = {"no", "yes", "ok", "okay", "idk", "nothing", "maybe", "unknown", "none"}
        answer_phrase = " ".join(normalized)
        if not normalized or answer_phrase in {"i do not know", "i don t know", "i dont know"} or (len(normalized) <= 4 and answer_phrase in non_answers):
            score = 0 if not normalized else 5
            return score, LLMScoringService._feedback_for_score(score)

        concepts = LLMScoringService._answer_concepts(question)
        answer_tokens = set(normalized)
        matched = {concept for concept in concepts if concept in answer_tokens}
        word_count = len(normalized)

        if len(matched) <= 1 and word_count <= 3:
            score = min(15, 5 + len(matched) * 5)
            return score, LLMScoringService._feedback_for_score(score)
        if not matched:
            score = min(20, round(max(0.0, (word_count - 3) / 25) * 20))
            return score, LLMScoringService._feedback_for_score(score)

        coverage = len(matched) / len(concepts) if concepts else 0
        completeness = min(1.0, max(0.0, (word_count - 3) / 25))
        explanation = min(1.0, max(0.0, (word_count - 1) / 10))
        score = max(0, min(100, round(coverage * 55 + completeness * 25 + explanation * 20)))
        return score, LLMScoringService._feedback_for_score(score, question)

    @staticmethod
    def _answer_concepts(question: str) -> set[str]:
        words = set(re.findall(r"[a-z][a-z0-9+#.-]*", (question or "").casefold()))
        stop_words = {"what", "how", "why", "when", "where", "which", "who", "is", "are", "the", "a", "an", "to", "from", "in", "of", "for", "and", "or", "on", "with", "your", "you", "can", "do", "does", "different", "typical", "work", "use", "used"}
        concepts = {word for word in words if word not in stop_words and len(word) > 2}
        if {"java", "javascript"} <= concepts:
            concepts.update({"backend", "frontend", "jvm", "browser", "node.js", "runtime"})
        return concepts or {"explain"}

    @staticmethod
    def _feedback_for_score(score: int, question: str = "") -> str:
        if score <= 10:
            concepts = sorted(LLMScoringService._answer_concepts(question))[:3]
            hint = f" Explain the main concepts: {', '.join(concepts)}." if concepts else ""
            return f"Your answer does not address the question.{hint}"
        if score < 50:
            return "Your answer is partially relevant. Add the missing concepts, reasoning, and an example."
        if score < 70:
            return "Your answer addresses part of the question. Explain the key concepts and trade-offs more completely."
        if score < 86:
            return "Good answer. Add more detail, reasoning, or examples to make it stronger."
        return "Strong answer with clear coverage of the important concepts and supporting explanation."

    @property
    def available(self) -> bool:
        return self._load()


llm_scoring_service = LLMScoringService()
