"""Trusted localhost coding runner.

This is deliberately a separate process from FastAPI. It uses fixed local
language executables and temporary directories. It is suitable for local
development only, not for untrusted public submissions or production hosting.
"""

import json
import os
import re
import shutil
import subprocess
import tempfile
import time
from pathlib import Path

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Smart Job Local Coding Runner", version="1.0.0")
SUPPORTED = {"python", "java", "javascript", "cpp"}
TIMEOUT_SECONDS = float(os.getenv("CODING_RUNNER_TIMEOUT_SECONDS", "5"))
RUNNER_TOKEN = os.getenv("EXECUTION_SERVICE_TOKEN", "")


class ExecuteRequest(BaseModel):
    language: str = Field(max_length=20)
    code: str = Field(min_length=1, max_length=100000)
    tests: list[dict] = Field(default_factory=list, max_length=100)
    hidden_tests: list[dict] = Field(default_factory=list, max_length=100)
    custom_input: str | None = Field(default=None, max_length=20000)
    function_signature: str | None = Field(default=None, max_length=250)


def _executables() -> dict[str, str | None]:
    return {"python": shutil.which("python") or shutil.which("python3"), "java": shutil.which("java"), "javac": shutil.which("javac"), "javascript": shutil.which("node"), "cpp": shutil.which("g++") or shutil.which("clang++")}


def _authorize(authorization: str | None) -> None:
    if RUNNER_TOKEN and authorization != f"Bearer {RUNNER_TOKEN}":
        raise HTTPException(status_code=401, detail="Runner authentication failed.")


def _run_process(command: list[str], *, cwd: str, stdin: str = "") -> dict:
    started = time.perf_counter()
    process = None
    try:
        process = subprocess.Popen(command, cwd=cwd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=False)
        stdout, stderr = process.communicate(stdin, timeout=TIMEOUT_SECONDS)
        return {"returncode": process.returncode, "stdout": stdout[-20000:], "stderr": stderr[-20000:], "runtime_ms": round((time.perf_counter() - started) * 1000)}
    except subprocess.TimeoutExpired:
        if process is not None:
            process.kill()
            process.communicate()
        return {"timeout": True, "returncode": None, "stdout": "", "stderr": "", "runtime_ms": round((time.perf_counter() - started) * 1000)}
    except OSError as exc:
        return {"runner_error": str(exc), "returncode": None, "stdout": "", "stderr": "", "runtime_ms": round((time.perf_counter() - started) * 1000)}


def _python_source(code: str, signature: str | None) -> str:
    if not signature:
        return code
    match = re.match(r"\s*([A-Za-z_]\w*)\s*\(([^)]*)\)", signature)
    if not match:
        return code
    name, parameters = match.groups()
    count = len([item for item in parameters.split(",") if item.strip()])
    invocation = f"result = {name}(payload)" if count <= 1 else f"result = {name}(*payload)"
    return code + f"\n\nimport json, sys\npayload = json.loads(sys.stdin.read())\n{invocation}\nprint(json.dumps(result))\n"


def _execute_one(request: ExecuteRequest, test: dict, runtimes: dict[str, str | None], workspace: str) -> dict:
    language = request.language
    input_value = request.custom_input if request.custom_input is not None else str(test.get("input", ""))
    expected = test.get("expected")
    if language == "python":
        source = Path(workspace) / "solution.py"
        source.write_text(_python_source(request.code, request.function_signature), encoding="utf-8")
        result = _run_process([runtimes["python"], str(source)], cwd=workspace, stdin=input_value)
    elif language == "javascript":
        source = Path(workspace) / "solution.js"
        source.write_text(request.code, encoding="utf-8")
        result = _run_process([runtimes["javascript"], str(source)], cwd=workspace, stdin=input_value)
    elif language == "java":
        source = Path(workspace) / "Main.java"
        source.write_text(request.code, encoding="utf-8")
        compiled = _run_process([runtimes["javac"], str(source)], cwd=workspace)
        if compiled.get("timeout"):
            return {"status": "TIME_LIMIT_EXCEEDED", "message": "Compilation exceeded the time limit.", **compiled}
        if compiled.get("returncode") != 0:
            return {"status": "COMPILATION_ERROR", "message": "Your Java code could not be compiled.", **compiled}
        result = _run_process([runtimes["java"], "-cp", workspace, "Main"], cwd=workspace, stdin=input_value)
    else:
        source = Path(workspace) / "solution.cpp"
        executable = Path(workspace) / ("program.exe" if os.name == "nt" else "program")
        source.write_text(request.code, encoding="utf-8")
        compiled = _run_process([runtimes["cpp"], str(source), "-o", str(executable)], cwd=workspace)
        if compiled.get("timeout"):
            return {"status": "TIME_LIMIT_EXCEEDED", "message": "Compilation exceeded the time limit.", **compiled}
        if compiled.get("returncode") != 0:
            return {"status": "COMPILATION_ERROR", "message": "Your C++ code could not be compiled.", **compiled}
        result = _run_process([str(executable)], cwd=workspace, stdin=input_value)

    if result.get("runner_error"):
        return {"status": "RUNNER_UNAVAILABLE", "message": "The configured local language runtime could not be started.", **result}
    if result.get("timeout"):
        return {"status": "TIME_LIMIT_EXCEEDED", "message": "Execution exceeded the time limit.", **result}
    if result.get("returncode") != 0:
        return {"status": "RUNTIME_ERROR", "message": "The program terminated with a runtime error.", **result}
    if expected is None:
        return {"status": "ACCEPTED", "message": "Custom execution completed.", **result}
    accepted = result["stdout"].strip() == str(expected).strip()
    return {"status": "ACCEPTED" if accepted else "WRONG_ANSWER", "message": "All tests passed." if accepted else "Some test cases failed.", **result}


@app.get("/health")
def health(authorization: str | None = Header(default=None)):
    _authorize(authorization)
    runtimes = _executables()
    available = {name: bool(path) for name, path in runtimes.items() if name != "javac"}
    available["java"] = bool(runtimes["java"] and runtimes["javac"])
    return {"status": "ok" if all(available.values()) else "degraded", "runner": "local-subprocess", "docker_required": False, "runtimes": available}


@app.post("/execute")
def execute(request: ExecuteRequest, authorization: str | None = Header(default=None)):
    _authorize(authorization)
    if request.language not in SUPPORTED:
        return {"status": "INVALID_REQUEST", "message": "Unsupported language."}
    runtimes = _executables()
    required = {"python": "python", "javascript": "javascript", "java": "java", "cpp": "cpp"}[request.language]
    if not runtimes.get(required) or (request.language == "java" and not runtimes.get("javac")):
        return {"status": "RUNNER_UNAVAILABLE", "message": f"The local {request.language} runtime is not installed."}
    tests = request.hidden_tests or request.tests
    if request.custom_input is not None:
        tests = [{"input": request.custom_input}]
    if not tests:
        return {"status": "INVALID_REQUEST", "message": "No test cases were provided."}
    results = []
    with tempfile.TemporaryDirectory(prefix="coding-run-") as workspace:
        for test in tests:
            result = _execute_one(request, test, runtimes, workspace)
            results.append(result)
            if result["status"] in {"COMPILATION_ERROR", "RUNTIME_ERROR", "TIME_LIMIT_EXCEEDED", "RUNNER_UNAVAILABLE"}:
                break
    passed = sum(item["status"] == "ACCEPTED" for item in results)
    failed = len(results) - passed
    first_failure = next((item for item in results if item["status"] != "ACCEPTED"), None)
    status = first_failure["status"] if first_failure else "ACCEPTED"
    return {"status": status, "message": first_failure["message"] if first_failure else "All tests passed.", "passed_tests": passed, "failed_tests": failed, "total_tests": len(tests), "output": "\n".join(item.get("stdout", "") for item in results), "stdout": "\n".join(item.get("stdout", "") for item in results), "stderr": "\n".join(item.get("stderr", "") for item in results), "error": first_failure.get("stderr", "") if first_failure else "", "runtime_ms": sum(item.get("runtime_ms") or 0 for item in results), "memory_mb": None}
