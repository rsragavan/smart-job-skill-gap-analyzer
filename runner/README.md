# Local Coding Runner

The runner is a separate localhost service from FastAPI. It detects the local
Python, Java, Node.js, and C++ runtimes, executes with fixed argument lists,
uses a unique temporary workspace per request, applies a strict timeout, and
removes the workspace after execution.

Start it as a host process:

```powershell
pip install -r runner/requirements.txt
$env:EXECUTION_SERVICE_TOKEN='local-runner-token'
.venv\Scripts\python.exe -m uvicorn runner.app:app --host 127.0.0.1 --port 8090
```

Set `EXECUTION_SERVICE_URL=http://127.0.0.1:8090` and
`EXECUTION_SERVICE_TOKEN=local-runner-token` in FastAPI's environment. Use the
same token when starting the runner; never expose it to the frontend. Restart
FastAPI after changing `.env` because settings are loaded at process startup.

This is a trusted local-development runner, not a production sandbox. It does
not provide container-level isolation, so bind it to `127.0.0.1`, do not expose
it to the public internet, and do not accept untrusted submissions.
