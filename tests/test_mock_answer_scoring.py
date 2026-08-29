from app.services.mock_interview_service import MockInterviewService


QUESTION = "How is Java different from JavaScript in typical backend and frontend work?"


def score(answer: str) -> int:
    return MockInterviewService._answer_score(answer, QUESTION)


def test_empty_and_non_answers_are_low_and_safe():
    for answer in ("", "no", "yes", "I don't know", "idk", "nothing", "maybe"):
        assert 0 <= score(answer) <= 10


def test_irrelevant_answers_do_not_get_keyword_or_length_inflation():
    assert score("This answer discusses cooking recipes and weather forecasts only.") <= 20
    assert score("Java") <= 15
    assert MockInterviewService._answer_score("PostgreSQL no", "What is PostgreSQL?") <= 15


def test_partial_answer_scores_below_complete_answer():
    partial = score("Java is commonly used for backend work.")
    correct = score("Java is commonly used for backend applications and runs on the JVM, while JavaScript is commonly used in browsers for frontend development and can also run on the backend using Node.js.")
    assert 0 <= partial <= 100
    assert correct > partial
    assert partial < 70


def test_strong_answer_is_high_and_case_insensitive():
    answer = "JAVA differs from JAVASCRIPT in runtime and typing. Java runs on the JVM for backend systems, while JavaScript runs in the browser for frontend work and on the backend with Node.js."
    assert score(answer) >= 70
    assert score(answer.lower()) == score(answer)


def test_feedback_matches_score_band():
    low = score("no")
    strong = score("Java runs on the JVM and is commonly used for backend applications, while JavaScript runs in browsers and Node.js for frontend and backend work.")
    assert "does not address" in MockInterviewService._answer_feedback(low, QUESTION)
    assert "Good answer" in MockInterviewService._answer_feedback(strong, QUESTION)
