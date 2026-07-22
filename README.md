# Smart Job Skill Gap Analyzer

React and FastAPI application that parses resumes, compares technical skills with Greenhouse job descriptions, and recommends learning paths.

## Stack

- Frontend: React 19, TypeScript, Vite, Material UI
- Backend: FastAPI, SQLAlchemy, Python 3.12
- Data: PostgreSQL (Neon in cloud)
- Authentication: JWT access/refresh tokens and bcrypt

## Local development

1. Copy `.env.example` to `.env` and fill in local PostgreSQL and Gmail SMTP values.
2. Create the virtual environment, install `requirements.txt`, and run:

   ```powershell
   .\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
   ```

3. Copy `frontend/.env.example` to `frontend/.env` and set `VITE_API_URL=http://127.0.0.1:8000`.
4. In `frontend`, install packages and run `npm run dev -- --port 5174`.

## Environment variables

| Variable | Service | Purpose |
| --- | --- | --- |
| `DATABASE_URL` | Backend | Neon PostgreSQL SQLAlchemy URL, including `sslmode=require` |
| `ENVIRONMENT` | Backend | Set to `production` on Render |
| `JWT_SECRET_KEY` | Backend | Random 32+ character signing secret |
| `JWT_ACCESS_TOKEN_MINUTES` / `JWT_REFRESH_TOKEN_DAYS` | Backend | JWT lifetimes |
| `FRONTEND_URL` / `BACKEND_URL` | Backend | Public Vercel and Render URLs |
| `CORS_ORIGINS` | Backend | Comma-separated allowed frontend origins |
| `SMTP_HOST`, `SMTP_PORT`, `SMTP_USERNAME`, `SMTP_PASSWORD`, `SMTP_FROM_EMAIL` | Backend | Gmail App Password SMTP configuration |
| `VITE_API_URL` | Frontend | Public Render API URL, set at Vercel build time |

The application uses `JWT_SECRET_KEY`; names such as `SECRET_KEY` or `JWT_SECRET` are not read by the current backend.

## Free cloud deployment

1. Push this repository to GitHub. Do not commit `.env`, Gmail App Passwords, database URLs, or JWT secrets.
2. Create a Neon PostgreSQL project and copy its pooled or direct SQLAlchemy connection string. Add `sslmode=require` if it is not already included.
3. In Render, create a Blueprint from this repository. It reads `render.yaml`. Enter the `sync: false` backend variables in the dashboard and deploy. Copy the resulting `https://...onrender.com` URL.
4. In Vercel, import the same GitHub repository and set the project root directory to `frontend`. Set `VITE_API_URL` to the Render URL, then deploy.
5. Set Render `FRONTEND_URL` and `CORS_ORIGINS` to the final Vercel URL, redeploy Render, then test login, resume upload, reset password, and job search.

## Hosting limitations

Render Free services spin down after inactivity and have an ephemeral filesystem. Consequently, the current local `uploads/` directory is not durable after a restart or deploy, and an in-process daily scheduler cannot run while the service is asleep. For durable resume files and guaranteed scheduled synchronization, use object storage and an external scheduler or a paid always-on worker. The existing manual admin job-sync endpoint remains available.

## Key API routes

- `POST /auth/register`, `POST /auth/login`, `POST /auth/refresh`, `POST /auth/logout`
- `POST /auth/forgot-password`, `POST /auth/reset-password`
- `POST /resume/upload`, `GET /resume/history`
- `GET /jobs/`
- `POST /jobs/sync` (admin)
- `GET /admin/skills/pending`, `POST /admin/skills/{id}/approve` (admin)

## Project structure

```text
app/          FastAPI routers, services, models, scheduler, and database code
frontend/     React/Vite application
render.yaml   Render Blueprint configuration
.env.example  Backend environment-variable template
```
