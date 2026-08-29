# Smart Job Skill Gap Analyzer

Final-year career preparation platform that turns a resume and a **target job** (scraped company listing or pasted job description) into skill-gap analysis, a learning roadmap, XP progress, and Career GPS readiness insights.

## Highlights

- **Universal Target workflow** — scraped Greenhouse jobs or any custom company JD
- Resume parsing and technical skill extraction
- Job match percentage with matched / missing skills
- Company-aware learning roadmap (topics, projects, resources, milestones)
- Learning progress, XP, levels, badges, daily/weekly goals
- Career GPS readiness dashboard
- Analytics and application tracking
- JWT authentication and admin skill taxonomy review

## Technology stack

| Layer | Technologies |
| --- | --- |
| Frontend | React 19, TypeScript, Vite, Material UI |
| Backend | FastAPI, Python 3.12, SQLAlchemy |
| Database | PostgreSQL |
| Auth | JWT access + refresh tokens, bcrypt |
| Jobs | Greenhouse API sync (manual admin API) |

## Quick start (local)

### Prerequisites

- Python 3.12+
- Node.js 20+
- PostgreSQL database

### Backend

```powershell
cd C:\Users\rsrag\PycharmProjects\smart-job-skill-gap-analyzer
copy .env.example .env
# Edit .env with DATABASE_URL, JWT_SECRET_KEY, FRONTEND_URL, BACKEND_URL, CORS_ORIGINS
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python create_tables.py
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000
```

API docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### Frontend

```powershell
cd frontend
copy .env.example .env
# Set VITE_API_URL=http://127.0.0.1:8000
npm install
npm run dev -- --port 5174
```

App: [http://127.0.0.1:5174](http://127.0.0.1:5174)

## Default user workflow

1. Register / login  
2. Upload resume  
3. **Choose Target** — scraped company job **or** paste custom JD  
4. Review skill gap and roadmap  
5. Learn on the Learning Dashboard (XP, badges, goals)  
6. Track readiness on Career GPS  
7. Review Analytics and job applications  

## Documentation

| Document | Description |
| --- | --- |
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | System architecture and folder structure |
| [docs/API.md](docs/API.md) | API reference summary |
| [docs/DATABASE.md](docs/DATABASE.md) | Database tables |
| [docs/USER_GUIDE.md](docs/USER_GUIDE.md) | End-user guide |
| [docs/ADMIN_GUIDE.md](docs/ADMIN_GUIDE.md) | Admin guide |
| [docs/PROJECT_REPORT.md](docs/PROJECT_REPORT.md) | College project report |
| [docs/DEMO_PREPARATION.md](docs/DEMO_PREPARATION.md) | 5/10-min demo scripts & faculty Q&A |
| [docs/VIVA_QA.md](docs/VIVA_QA.md) | 50 viva Q&A |
| [DEPLOYMENT.md](DEPLOYMENT.md) | Cloud deployment guide |

## Environment variables

See [`.env.example`](.env.example). Important keys:

| Variable | Purpose |
| --- | --- |
| `DATABASE_URL` | PostgreSQL SQLAlchemy URL |
| `JWT_SECRET_KEY` | Signing secret (32+ chars in production) |
| `FRONTEND_URL` / `BACKEND_URL` | Public URLs |
| `CORS_ORIGINS` | Allowed frontend origins |
| `SMTP_*` | Password-reset email (Gmail App Password) |
| `VITE_API_URL` | Frontend API base URL |
| `EXECUTION_SERVICE_URL` | URL of the separate isolated coding runner |
| `EXECUTION_SERVICE_TOKEN` | Optional shared runner authentication token |

## Project structure

```text
app/                 FastAPI application (API, services, models, roadmap engine)
frontend/            React + TypeScript UI
docs/                Architecture, guides, report, viva Q&A
tests/               Backend unit tests
create_tables.py     Create SQLAlchemy tables
runner/              Separate localhost coding runner service
render.yaml          Render Blueprint
DEPLOYMENT.md        Production deployment notes
```

## Local coding runner

FastAPI never executes learner source. To enable the Coding Practice Run
button, start the separate local runner service:

```powershell
pip install -r runner/requirements.txt
$env:EXECUTION_SERVICE_TOKEN='local-runner-token'
.venv\Scripts\python.exe -m uvicorn runner.app:app --host 127.0.0.1 --port 8090
```

Set `EXECUTION_SERVICE_URL=http://127.0.0.1:8090` and
`EXECUTION_SERVICE_TOKEN=local-runner-token` in FastAPI's environment. Use the
same token when starting the runner and restart FastAPI after changing `.env`.
The runner uses detected local `python`, `javac/java`,
`node`, and `g++`/`clang++` executables with fixed argument lists, temporary
workspaces, output capture, timeout enforcement, and cleanup. Docker is not
required. This runner is for trusted local development only and must remain
bound to `127.0.0.1`; it is not production-grade isolation.

For local development, use three terminals: start this runner on port 8090,
start FastAPI on port 8000, and start the frontend on its Vite port. Restart
FastAPI after changing `.env`; the frontend never receives the runner token.

## License / academic use

Built as a final-year academic project. Do not commit `.env`, database credentials, or SMTP secrets.
