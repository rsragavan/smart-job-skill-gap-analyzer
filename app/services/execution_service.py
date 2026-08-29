"""Client for the isolated code runner.

This module deliberately contains no code execution primitives. The runner
must be a separately deployed service with OS/container limits applied there.
"""

import ast
import json
import re
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from app.core.config import settings

SUPPORTED_LANGUAGES = {"python", "java", "javascript", "cpp"}


class ExecutionService:
    def health(self) -> dict:
        if not settings.EXECUTION_SERVICE_URL:
            return {"status": "RUNNER_UNAVAILABLE", "message": "The isolated execution service is not configured."}
        request = Request(settings.EXECUTION_SERVICE_URL.rstrip("/") + "/health", headers=self._headers(), method="GET")
        try:
            with urlopen(request, timeout=settings.EXECUTION_SERVICE_TIMEOUT_SECONDS) as response:
                result = json.loads(response.read().decode("utf-8"))
                if result.get("status") in {"ok", "degraded"}:
                    return result
                return {"status": "RUNNER_UNAVAILABLE", "message": result.get("message", "The isolated runner is unavailable.")}
        except (HTTPError, URLError, TimeoutError, ValueError):
            return {"status": "RUNNER_UNAVAILABLE", "message": "The isolated execution service could not be reached."}

    def execute(self, *, code: str, language: str, public_tests: list, hidden_tests: list, custom_input: str | None, include_hidden: bool, function_signature: str | None = None) -> dict:
        if language not in SUPPORTED_LANGUAGES:
            return self._failure("INVALID_REQUEST", "Select Python, Java, JavaScript, or C++.")
        if not code.strip():
            return self._failure("INVALID_REQUEST", "Add a solution before running tests.")
        contract_error = self.validate_function_contract(code, language, function_signature)
        if contract_error:
            return self._failure("INVALID_REQUEST", contract_error)
        if not settings.EXECUTION_SERVICE_URL:
            return self._failure("RUNNER_UNAVAILABLE", "The local execution runner is not configured.")

        payload = {"language": language, "code": code, "tests": public_tests, "custom_input": custom_input, "function_signature": function_signature}
        if include_hidden:
            payload["hidden_tests"] = hidden_tests
        headers = self._headers()
        request = Request(settings.EXECUTION_SERVICE_URL.rstrip("/") + "/execute", data=json.dumps(payload).encode(), headers=headers, method="POST")
        try:
            with urlopen(request, timeout=settings.EXECUTION_SERVICE_TIMEOUT_SECONDS) as response:
                result = json.loads(response.read().decode("utf-8"))
        except (HTTPError, URLError, TimeoutError, ValueError):
            return self._failure("RUNNER_UNAVAILABLE", "The local execution runner could not be reached.")
        return self._normalize(result)

    @staticmethod
    def validate_function_contract(code: str, language: str, function_signature: str | None) -> str | None:
        """Validate only the declared Python function name; never execute code."""
        if language != "python" or not function_signature:
            return None
        match = re.match(r"\s*([A-Za-z_]\w*)\s*\(", function_signature)
        if not match:
            return None
        expected_name = match.group(1)
        try:
            tree = ast.parse(code)
        except SyntaxError:
            return None
        declared_names = {node.name for node in tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))}
        if expected_name not in declared_names:
            return f"Define the required function `{expected_name}` from the starter template."
        return None

    @staticmethod
    def _headers() -> dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if settings.EXECUTION_SERVICE_TOKEN:
            headers["Authorization"] = f"Bearer {settings.EXECUTION_SERVICE_TOKEN}"
        return headers

    @staticmethod
    def _failure(status: str, message: str) -> dict:
        return {"status": status, "message": message, "runtime_ms": None, "passed_tests": 0, "failed_tests": 0, "total_tests": 0, "output": "", "error": message}

    @staticmethod
    def _normalize(result: dict) -> dict:
        allowed = {"status", "message", "runtime_ms", "memory_mb", "passed_tests", "failed_tests", "total_tests", "output", "stdout", "stderr", "error", "compilation_error"}
        clean = {key: result.get(key) for key in allowed if key in result}
        clean.setdefault("status", "RUNNER_ERROR")
        clean.setdefault("message", "Execution completed.")
        for key in ("passed_tests", "failed_tests", "total_tests"):
            clean[key] = max(0, int(clean.get(key) or 0))
        return clean


execution_service = ExecutionService()
