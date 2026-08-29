from datetime import UTC, datetime
import random
import re

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.company_intelligence import CompanyRole, CompanySelectionProcess
from app.models.content import CodingQuestion, InterviewQuestion
from app.models.company_intelligence import CompanyInterviewQuestion
from app.models.mock_interview import AssessmentAttempt, CodingAssessment, MockInterview, MockInterviewQuestion
from app.models.resume_history import ResumeHistory
from app.models.user_target import UserTarget


INTERVIEW_TYPES = {"technical", "hr", "behavioral", "situational", "communication", "system-design", "frontend", "backend", "database", "cloud"}
TYPE_CATEGORIES = {
    "technical": {"technical", "programming", "dsa", "coding"}, "hr": {"hr"}, "behavioral": {"behavioral", "culture"}, "situational": {"situational"}, "communication": {"communication"},
    "system-design": {"system design", "system_design"}, "frontend": {"frontend", "react", "javascript", "typescript", "html", "css"},
    "backend": {"backend", "technical", "programming"}, "database": {"sql", "database"}, "cloud": {"cloud", "devops"},
}
EXPERIENCE_DIFFICULTIES = {
    "fresher": {"easy", "medium"},
    "entry": {"easy", "medium"},
    "intermediate": {"medium", "hard"},
    "mid": {"medium", "hard"},
    "advanced": {"medium", "hard"},
    "senior": {"medium", "hard"},
}


class MockInterviewService:
    def start(self, db: Session, user_id: int, payload) -> dict:
        target = db.query(UserTarget).filter_by(user_id=user_id, is_active=True).first()
        if not target:
            raise HTTPException(status_code=400, detail="Please select an active target job before starting a mock interview.")

        interview_type = payload.interview_type.casefold()
        if interview_type not in INTERVIEW_TYPES:
            raise HTTPException(status_code=422, detail="Invalid interview type selected.")

        experience_level = payload.experience_level.casefold()
        if experience_level not in EXPERIENCE_DIFFICULTIES:
            raise HTTPException(status_code=422, detail="Invalid experience level selected.")

        company_id = payload.company_id or (target.company_id if target else None)
        role_id = payload.company_role_id or (target.company_role_id if target else None)
        role = db.query(CompanyRole).filter_by(id=role_id).first() if role_id else None
        category_names = TYPE_CATEGORIES.get(interview_type, set())
        all_rows = db.query(InterviewQuestion).filter(InterviewQuestion.active.is_(True), InterviewQuestion.verified.is_(True)).order_by(InterviewQuestion.id).all()
        if not all_rows:
            raise HTTPException(status_code=422, detail="No verified interview questions are available for the selected target.")

        rows = self._eligible_by_type(all_rows, category_names)
        if not rows:
            raise HTTPException(status_code=422, detail="No verified interview questions are available for the selected interview type.")

        company_rows = []
        if role_id:
            company_rows = db.query(CompanyInterviewQuestion).filter_by(company_role_id=role_id).order_by(CompanyInterviewQuestion.id).all()
            company_rows = [row for row in company_rows if self._eligible_company_question(row, category_names)]
        resume_skills = self._latest_resume_skills(db, user_id)
        performance = self._performance_by_topic(db, user_id)
        selected = self._recommend_questions(rows, company_rows, target, interview_type, experience_level, resume_skills, performance, limit=10)
        if not selected:
            raise HTTPException(status_code=422, detail="No verified interview questions are available for the selected interview type.")

        interview = MockInterview(user_id=user_id, company_id=company_id, company_role_id=role_id, company_name=target.company, role_title=role.title if role else target.role_title, interview_type=interview_type, experience_level=experience_level)
        db.add(interview); db.flush()
        for sequence, item in enumerate(selected, start=1):
            row = item["row"]
            is_company = item["source"] == "COMPANY-SPECIFIC"
            db.add(MockInterviewQuestion(interview_id=interview.id, sequence=sequence, category=item["category"].casefold(), topic=item["topic"], difficulty=item["difficulty"], skill=item["skill"], question=item["question"], source_question_id=row.id if is_company else None, source_type=item["source"], recommendation_reason=item["reason"]))
        db.commit()
        return self.get_interview(db, user_id, interview.id)

    def get_interview(self, db: Session, user_id: int, interview_id: int) -> dict:
        interview = self._owned_interview(db, user_id, interview_id)
        rounds = db.query(CompanySelectionProcess).filter_by(company_role_id=interview.company_role_id).order_by(CompanySelectionProcess.round_number).all() if interview.company_role_id else []
        questions = db.query(MockInterviewQuestion).filter_by(interview_id=interview.id).order_by(MockInterviewQuestion.sequence).all()
        return {"id": interview.id, "company_name": interview.company_name, "role_title": interview.role_title, "interview_type": interview.interview_type, "experience_level": interview.experience_level, "status": interview.status, "started_at": interview.started_at, "completed_at": interview.completed_at, "questions": [{"id": row.id, "sequence": row.sequence, "category": row.category, "topic": row.topic, "difficulty": row.difficulty, "skill": row.skill, "question": row.question, "answer": row.answer, "score": row.score, "feedback": row.feedback, "source": row.source_type, "source_type": row.source_type, "recommendation_reason": row.recommendation_reason} for row in questions], "company_rounds": [{"round_number": row.round_number, "title": row.title} for row in rounds], "feedback": self._feedback(interview)}

    def answer(self, db: Session, user_id: int, interview_id: int, question_id: int, answer: str) -> dict:
        self._owned_interview(db, user_id, interview_id)
        question = db.query(MockInterviewQuestion).filter_by(id=question_id, interview_id=interview_id).first()
        if not question: raise HTTPException(status_code=404, detail="Interview question not found.")
        question.answer = answer.strip()
        question.score = self._answer_score(answer, question.question)
        question.feedback = self._answer_feedback(question.score, question.question)
        db.commit()
        return self.get_interview(db, user_id, interview_id)

    def complete(self, db: Session, user_id: int, interview_id: int) -> dict:
        interview = self._owned_interview(db, user_id, interview_id)
        questions = db.query(MockInterviewQuestion).filter_by(interview_id=interview.id).all()
        answered = [row for row in questions if row.answer]
        if not answered: raise HTTPException(status_code=422, detail="Answer at least one question before completing the interview.")
        average = round(sum(row.score if row.score is not None else self._answer_score(row.answer or "", row.question) for row in answered) / len(answered))
        communication = min(100, round(sum(len(row.answer or "") for row in answered) / len(answered) / 4))
        technical = round(sum(row.score or 0 for row in answered) / len(answered))
        interview.status = "completed"; interview.completed_at = datetime.now(UTC); interview.overall_score = average; interview.technical_score = technical; interview.communication_score = communication; interview.problem_solving_score = technical; interview.confidence_score = communication; interview.hr_score = communication
        strong_skills = sorted({row.skill for row in answered if row.skill and (row.score if row.score is not None else self._answer_score(row.answer or "", row.question)) >= 70})
        weak_skills = sorted({row.skill for row in answered if row.skill and (row.score if row.score is not None else self._answer_score(row.answer or "", row.question)) < 70})
        interview.strengths = strong_skills or (["Completed responses were provided."] if average >= 60 else [])
        interview.weaknesses = weak_skills or (["Expand answers with evidence and trade-offs."] if average < 80 else [])
        interview.recommended_skills = weak_skills
        interview.next_steps = [f"Review the Learning module resources for {skill}." for skill in weak_skills[:3]] or (["Review missed questions and repeat the interview."] if average < 70 else ["Practice timed company-specific rounds."])
        interview.feedback = "Score is based on answer completeness, structure, and evidence using deterministic evaluation."; db.commit()
        return self.get_interview(db, user_id, interview_id)

    def history(self, db: Session, user_id: int) -> list[dict]:
        rows = db.query(MockInterview).filter_by(user_id=user_id).order_by(MockInterview.started_at.desc()).limit(50).all()
        return [{"id": row.id, "company_name": row.company_name, "role_title": row.role_title, "interview_type": row.interview_type, "status": row.status, "overall_score": row.overall_score, "started_at": row.started_at, "completed_at": row.completed_at} for row in rows]

    def assessments(self, db: Session, user_id: int | None = None) -> list[dict]:
        self._ensure_assessments(db)
        target = db.query(UserTarget).filter_by(user_id=user_id, is_active=True).first() if user_id else None
        result = []
        for item in db.query(CodingAssessment).order_by(CodingAssessment.id).all():
            available = sum(1 for row in db.query(CodingQuestion).filter(CodingQuestion.difficulty == item.difficulty, CodingQuestion.active.is_(True), CodingQuestion.verified.is_(True)).all() if row.description and row.input_format and row.output_format and row.constraints and row.examples and row.starter_code and row.function_signature)
            result.append({"id": item.id, "title": item.title, "difficulty": item.difficulty, "time_limit_minutes": item.time_limit_minutes, "question_count": min(item.question_count, available), "available_questions": available, "pass_percentage": item.pass_percentage, "topics": item.topics, "target": {"company": target.company, "role": target.role_title, "experience_level": "fresher"} if target else None, "selection_mode": "TARGET_RECOMMENDATION" if target else "GENERAL_RECOMMENDATION"})
        return result

    def start_assessment(self, db: Session, user_id: int, assessment_id: int) -> dict:
        self._ensure_assessments(db); assessment = db.get(CodingAssessment, assessment_id)
        if not assessment: raise HTTPException(status_code=404, detail="Assessment not found.")
        available = [row for row in db.query(CodingQuestion).filter(CodingQuestion.difficulty == assessment.difficulty, CodingQuestion.active.is_(True), CodingQuestion.verified.is_(True)).order_by(CodingQuestion.id).all() if row.description and row.input_format and row.output_format and row.constraints and row.examples and row.starter_code and row.function_signature][:assessment.question_count]
        if not available: raise HTTPException(status_code=422, detail="No verified coding questions are available.")
        target = db.query(UserTarget).filter_by(user_id=user_id, is_active=True).first()
        attempt = AssessmentAttempt(user_id=user_id, assessment_id=assessment.id, company_id=target.company_id if target else None, company_role_id=target.company_role_id if target else None, answers={})
        db.add(attempt); db.commit(); db.refresh(attempt)
        return {"id": attempt.id, "assessment": {"id": assessment.id, "title": assessment.title, "difficulty": assessment.difficulty, "time_limit_minutes": assessment.time_limit_minutes, "pass_percentage": assessment.pass_percentage, "topics": assessment.topics}, "target": {"company": target.company if target else None, "role": target.role_title if target else None, "experience_level": "fresher"}, "questions": [{"id": row.id, "title": row.title, "description": row.description, "category": row.category, "topic": row.topic, "input_format": row.input_format, "output_format": row.output_format, "constraints": row.constraints, "examples": row.examples, "explanation": row.explanation, "expected_complexity": row.expected_complexity, "expected_space_complexity": row.expected_space_complexity, "tags": row.tags, "starter_code": row.starter_code, "function_signature": row.function_signature, "execution_mode": row.execution_mode, "test_cases": row.test_cases, "hints": row.hints, "source_type": row.source_type if row.source_type in {"COMPANY_SOURCED", "CURATED", "GENERATED_RECOMMENDATION"} else ("CURATED" if row.source == "Curated educational content" else "GENERATED_RECOMMENDATION")} for row in available]}

    def submit_assessment(self, db: Session, user_id: int, attempt_id: int, answers: dict[str, str]) -> dict:
        attempt = db.query(AssessmentAttempt).filter_by(id=attempt_id, user_id=user_id).first()
        if not attempt: raise HTTPException(status_code=404, detail="Assessment attempt not found.")
        assessment = db.get(CodingAssessment, attempt.assessment_id)
        questions = db.query(CodingQuestion).filter(CodingQuestion.id.in_([int(key) for key in answers if str(key).isdigit()])).all()
        correct = sum(1 for question in questions if any(keyword in answers.get(str(question.id), "").casefold() for keyword in (question.expected_answer_keywords or [])))
        total = len(questions); attempt.answers = answers; attempt.score = correct; attempt.percentage = round(correct / total * 100) if total else 0; attempt.passed = attempt.percentage >= assessment.pass_percentage; attempt.status = "completed"; attempt.completed_at = datetime.now(UTC); db.commit()
        return {"attempt_id": attempt.id, "total_questions": total, "correct_answers": correct, "incorrect_answers": total - correct, "score": f"{correct} / {total}", "percentage": attempt.percentage, "passed": attempt.passed, "pass_percentage": assessment.pass_percentage, "topics": sorted({question.topic for question in questions}), "execution_mode": "safe-rubric", "passed_tests": correct, "failed_tests": total - correct}

    def assessment_history(self, db: Session, user_id: int) -> list[dict]:
        rows = db.query(AssessmentAttempt).filter_by(user_id=user_id).order_by(AssessmentAttempt.started_at.desc()).limit(50).all()
        return [{"id": row.id, "assessment_id": row.assessment_id, "status": row.status, "score": row.score, "percentage": row.percentage, "passed": row.passed, "started_at": row.started_at, "completed_at": row.completed_at} for row in rows]

    @classmethod
    def _answer_score(cls, answer: str, question: str = "") -> int:
        """Return a deterministic score based on question concepts and answer evidence."""
        normalized = re.findall(r"[a-z][a-z0-9+#.-]*", (answer or "").casefold())
        non_answers = {"no", "yes", "ok", "okay", "idk", "nothing", "maybe", "unknown", "none"}
        answer_phrase = " ".join(normalized)
        if not normalized or answer_phrase in {"i do not know", "i don t know", "i dont know"} or (len(normalized) <= 4 and answer_phrase in non_answers):
            return 0 if not normalized else 5

        concepts = cls._answer_concepts(question)
        answer_tokens = set(normalized)
        matched = {concept for concept in concepts if concept in answer_tokens}
        word_count = len(normalized)
        if len(matched) <= 1 and word_count <= 3:
            return min(15, 5 + len(matched) * 5)
        if not matched:
            return min(20, round(max(0.0, (word_count - 3) / 25) * 20))

        coverage = len(matched) / len(concepts) if concepts else 0
        completeness = min(1.0, max(0.0, (word_count - 3) / 25))
        explanation = min(1.0, max(0.0, (word_count - 1) / 10))
        score = round(coverage * 55 + completeness * 25 + explanation * 20)
        return max(0, min(100, score))

    @staticmethod
    def _answer_concepts(question: str) -> set[str]:
        words = set(re.findall(r"[a-z][a-z0-9+#.-]*", (question or "").casefold()))
        stop_words = {"what", "how", "why", "when", "where", "which", "who", "is", "are", "the", "a", "an", "to", "from", "in", "of", "for", "and", "or", "on", "with", "your", "you", "can", "do", "does", "different", "typical", "work", "use", "used"}
        concepts = {word for word in words if word not in stop_words and len(word) > 2}
        if {"java", "javascript"} <= concepts:
            concepts.update({"backend", "frontend", "jvm", "browser", "node.js", "runtime"})
        return concepts or {"explain"}

    @classmethod
    def _answer_feedback(cls, score: int, question: str) -> str:
        if score <= 10:
            concepts = sorted(cls._answer_concepts(question))[:3]
            return f"Your answer does not address the question. Explain the main concepts: {', '.join(concepts)}."
        if score < 50:
            return "Your answer is partially relevant. Add the missing concepts, reasoning, and an example."
        if score < 70:
            return "Your answer addresses part of the question. Explain the key concepts and trade-offs more completely."
        if score < 86:
            return "Good answer. Add more detail, reasoning, or examples to make it stronger."
        return "Strong answer with clear coverage of the important concepts and supporting explanation."

    @staticmethod
    def _feedback(interview: MockInterview) -> dict:
        return {"overall_score": interview.overall_score, "technical_score": interview.technical_score, "communication_score": interview.communication_score, "problem_solving": interview.problem_solving_score, "confidence": interview.confidence_score, "hr_score": interview.hr_score, "strengths": interview.strengths or [], "weaknesses": interview.weaknesses or [], "recommended_skills": interview.recommended_skills or [], "next_steps": interview.next_steps or [], "feedback": interview.feedback}

    @staticmethod
    def _eligible_by_type(rows: list[InterviewQuestion], category_names: set[str]) -> list[InterviewQuestion]:
        if not category_names:
            return rows
        return [
            row for row in rows
            if row.category.casefold() in category_names
            or row.topic.casefold() in category_names
            or (row.skill and row.skill.casefold() in category_names)
        ]

    @staticmethod
    def _select_questions(rows: list[InterviewQuestion], target: UserTarget, interview_type: str, experience_level: str, limit: int = 10, rng: random.Random | None = None) -> list[InterviewQuestion]:
        """Compatibility helper retained for callers/tests using the old selector."""
        return [item["row"] for item in MockInterviewService._recommend_questions(rows, [], target, interview_type, experience_level, set(), {}, limit)]

    @classmethod
    def _recommend_questions(cls, rows, company_rows, target, interview_type, experience_level, resume_skills, performance, limit=10):
        missing = cls._normalized_set(target.missing_skills)
        matched = cls._normalized_set(target.matched_skills) | resume_skills
        role_terms = cls._role_terms(target.role_title)
        description_terms = cls._description_terms(target.job_description)
        preferred = {"fresher": ("easy", "medium"), "entry": ("medium", "easy"), "mid": ("medium", "hard"), "senior": ("hard", "medium")}.get(experience_level, ("medium", "easy"))
        suitable_rows = [row for row in rows if (row.difficulty or "").casefold() in EXPERIENCE_DIFFICULTIES.get(experience_level, set())] or rows
        candidates = []
        for row in suitable_rows:
            candidates.append((row, "CURATED", row.category, row.topic, row.skill, row.question, row.difficulty))
        for row in company_rows:
            candidates.append((row, "COMPANY-SPECIFIC", row.category, getattr(row, "category", None), None, row.question, row.difficulty or "medium"))

        ranked = []
        for row, source, category, topic, skill, question, difficulty in candidates:
            values = cls._normalized_set([category, topic, skill, question])
            text = f"{category} {topic or ''} {skill or ''} {question}".casefold()
            score = 0
            reasons = []
            missing_match = missing & values
            role_match = any(term in text for term in role_terms)
            jd_match = bool(description_terms & values)
            if missing_match:
                score += 35; reasons.append(f"matches missing skill {', '.join(sorted(missing_match))}")
            if role_match:
                score += 25; reasons.append("matches your target role")
            if jd_match:
                score += 15; reasons.append("matches the target job description")
            if cls._type_relevant(category, topic, interview_type):
                score += 10; reasons.append(f"fits the {interview_type} interview type")
            if difficulty.casefold() == preferred[0]:
                score += 10
            elif difficulty.casefold() == preferred[1]:
                score += 7
            topic_key = cls._normalized(topic or skill or category)
            perf = performance.get(topic_key, {})
            if perf.get("answered"):
                score -= 5
                if perf.get("average", 100) < 70:
                    score += 10; reasons.append("targets a previously weak topic")
                elif perf.get("average", 0) >= 80:
                    score -= 5; reasons.append("reduces repetition of a strong topic")
            else:
                score += 5; reasons.append("new or unanswered practice")
            if source == "COMPANY-SPECIFIC":
                reasons.append("company-specific question available for this role")
            ranked.append((min(100, max(0, score)), row.id, topic_key, {"row": row, "source": source, "category": category, "topic": topic, "difficulty": difficulty, "skill": skill, "question": question, "reason": "; ".join(reasons) or "curated interview practice"}))
        ranked.sort(key=lambda item: (-item[0], item[1]))
        selected = []
        seen_topics = set()
        for item in ranked:
            if len(selected) >= limit: break
            if item[2] not in seen_topics or len(ranked) - len(selected) <= limit:
                selected.append(item[3]); seen_topics.add(item[2])
        return selected

    @staticmethod
    def _type_relevant(category, topic, interview_type):
        names = TYPE_CATEGORIES.get(interview_type, set())
        return not names or (category or "").casefold() in names or (topic or "").casefold() in names

    @classmethod
    def _normalized_set(cls, values):
        return {cls._normalized(value) for value in (values or []) if cls._normalized(value)}

    @staticmethod
    def _eligible_company_question(row, category_names):
        return not category_names or (row.category or "").casefold() in category_names

    @staticmethod
    def _latest_resume_skills(db, user_id):
        row = db.query(ResumeHistory).filter_by(user_id=user_id).order_by(ResumeHistory.uploaded_at.desc()).first()
        if not row:
            return set()
        return {item.strip().casefold() for item in (row.extracted_skills or "").replace(";", ",").split(",") if item.strip()}

    @staticmethod
    def _performance_by_topic(db, user_id):
        rows = db.query(MockInterviewQuestion).join(MockInterview, MockInterview.id == MockInterviewQuestion.interview_id).filter(MockInterview.user_id == user_id).all()
        grouped = {}
        for row in rows:
            key = (row.topic or row.skill or row.category or "").casefold()
            if not key: continue
            item = grouped.setdefault(key, {"answered": 0, "scores": []})
            if row.answer:
                item["answered"] += 1; item["scores"].append(row.score or 0)
        return {key: {"answered": value["answered"], "average": sum(value["scores"]) / len(value["scores"]) if value["scores"] else 0} for key, value in grouped.items()}

    @staticmethod
    def _normalized(value: str | None) -> str:
        return (value or "").strip().casefold()

    @staticmethod
    def _role_terms(role_title: str | None) -> set[str]:
        role = (role_title or "").casefold()
        terms: set[str] = set()
        if "front" in role or "react" in role:
            terms.update({"frontend", "react", "javascript", "typescript", "html", "css"})
        if "back" in role or "api" in role:
            terms.update({"backend", "python", "fastapi", "sql", "postgresql", "rest"})
        if "data" in role:
            terms.update({"sql", "postgresql", "database"})
        if "cloud" in role or "devops" in role:
            terms.update({"cloud", "aws", "docker", "kubernetes", "linux", "ci/cd"})
        return terms

    @staticmethod
    def _description_terms(description: str | None) -> set[str]:
        known = {"python", "fastapi", "postgresql", "sql", "docker", "react", "javascript", "typescript", "java", "spring", "aws", "kubernetes", "linux", "git", "rest", "api", "testing", "communication", "leadership"}
        return {word for word in (description or "").casefold().replace("/", " ").replace(",", " ").split() if word in known}

    @staticmethod
    def _owned_interview(db: Session, user_id: int, interview_id: int) -> MockInterview:
        row = db.query(MockInterview).filter_by(id=interview_id, user_id=user_id).first()
        if not row: raise HTTPException(status_code=404, detail="Mock interview not found.")
        return row

    @staticmethod
    def _ensure_assessments(db: Session) -> None:
        if db.query(CodingAssessment).count(): return
        db.add_all([CodingAssessment(title="Coding Fundamentals", difficulty="easy", time_limit_minutes=30, question_count=5, topics=["Arrays", "Strings", "Searching"]), CodingAssessment(title="Technical Coding", difficulty="medium", time_limit_minutes=45, question_count=8, topics=["Linked List", "Trees", "Graphs", "SQL"]), CodingAssessment(title="Advanced Problem Solving", difficulty="hard", time_limit_minutes=60, question_count=10, topics=["Dynamic Programming", "Graphs", "Sorting"])])
        db.commit()


mock_interview_service = MockInterviewService()
