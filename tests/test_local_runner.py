import shutil

import pytest
from fastapi.testclient import TestClient

import runner.app as runner_app


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setattr(runner_app, "RUNNER_TOKEN", "test-runner-token")
    return TestClient(runner_app.app)


def execute(client, language, code, tests):
    return client.post(
        "/execute",
        headers={"Authorization": "Bearer test-runner-token"},
        json={"language": language, "code": code, "tests": tests},
    )


def test_runner_health_and_authentication(client):
    assert client.get("/health", headers={"Authorization": "Bearer test-runner-token"}).status_code == 200
    assert client.get("/health").status_code == 401


def test_python_javascript_and_java_execution(client):
    assert execute(client, "python", 'print("HELLO_RUNNER")', [{"expected": "HELLO_RUNNER"}]).json()["status"] == "ACCEPTED"
    assert execute(client, "javascript", 'console.log("HELLO_RUNNER")', [{"expected": "HELLO_RUNNER"}]).json()["status"] == "ACCEPTED"
    java = 'public class Main { public static void main(String[] args) { System.out.println("HELLO_RUNNER"); } }'
    result = execute(client, "java", java, [{"expected": "HELLO_RUNNER"}])
    if result.json()["status"] == "RUNNER_UNAVAILABLE":
        pytest.skip("Java runtime/compiler is not installed")
    assert result.json()["status"] == "ACCEPTED"


def test_cpp_execution_is_conditional_on_compiler(client):
    if not (shutil.which("g++") or shutil.which("clang++") or shutil.which("cl")):
        pytest.skip("C++ compiler is not installed")
    code = '#include <iostream>\nint main(){std::cout << "HELLO_RUNNER";}'
    assert execute(client, "cpp", code, [{"expected": "HELLO_RUNNER"}]).json()["status"] == "ACCEPTED"


def test_runner_error_statuses(client):
    assert execute(client, "python", 'print("WRONG")', [{"expected": "RIGHT"}]).json()["status"] == "WRONG_ANSWER"
    assert execute(client, "python", 'raise RuntimeError("boom")', [{"expected": ""}]).json()["status"] == "RUNTIME_ERROR"
    assert execute(client, "python", "while True: pass", [{"expected": ""}]).json()["status"] == "TIME_LIMIT_EXCEEDED"
    assert execute(client, "ruby", "puts 1", [{"expected": "1"}]).json()["status"] == "INVALID_REQUEST"


def test_custom_input_is_forwarded_to_the_runtime(client):
    response = client.post(
        "/execute",
        headers={"Authorization": "Bearer test-runner-token"},
        json={"language": "python", "code": "print(input())", "custom_input": "CUSTOM_INPUT"},
    )
    assert response.json()["status"] == "ACCEPTED"
    assert "CUSTOM_INPUT" in response.json()["output"]
