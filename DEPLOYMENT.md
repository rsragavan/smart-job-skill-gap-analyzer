# Production Deployment

This project deploys as two Render services:

- `smart-job-skill-gap-api`: FastAPI web service
- `smart-job-skill-gap-frontend`: React/Vite static site

The root `render.yaml` contains both service definitions.

## Backend environment variables

Configure these in the Render API service:

| Variable | Required value |
| --- | --- |
| `ENVIRONMENT` | `production` |
| `DATABASE_URL` | PostgreSQL SQLAlchemy URL, for example `postgresql+psycopg2://...?...` |
| `JWT_SECRET_KEY` | Random secret of at least 32 characters |
| `JWT_ACCESS_TOKEN_MINUTES` | `15` or another short lifetime |
| `JWT_REFRESH_TOKEN_DAYS` | `7` or the selected refresh lifetime |
| `FRONTEND_URL` | Public frontend URL |
| `BACKEND_URL` | Public API URL |
| `CORS_ORIGINS` | Comma-separated trusted frontend origins only |
| `MAX_RESUME_SIZE_BYTES` | `5242880` by default |
| `LOG_LEVEL` | `INFO` or `WARNING` |
| `SMTP_HOST` | SMTP provider host |
| `SMTP_PORT` | Usually `587` |
| `SMTP_USERNAME` | SMTP account |
| `SMTP_PASSWORD` | SMTP app password or provider secret |
| `SMTP_FROM_EMAIL` | Verified sender address |

Do not commit `.env` files, database URLs, SMTP passwords, or JWT secrets.

## Frontend environment variables

Configure this at the frontend build service:

```text
VITE_API_URL=https://your-api.onrender.com
```

Vite injects this value during the production build. It must be the public HTTPS API URL and must not use Render's private hostname.

## Render configuration

Backend:

```text
Build: pip install --no-cache-dir -r requirements.txt
Pre-deploy: python create_tables.py
Start: uvicorn app.main:app --host 0.0.0.0 --port $PORT
Health: /health
```

Frontend:

```text
Root directory: frontend
Build: npm ci && npm run build
Publish directory: frontend/dist
SPA fallback: /* → /index.html
```

The pre-deploy command creates missing tables through the existing SQLAlchemy metadata. This project does not currently contain versioned Alembic migrations; production schema changes should be introduced through a migration system before future destructive or column-changing releases.

## Production checklist

- Create or select a PostgreSQL database and use its SSL connection string.
- Set a unique production `JWT_SECRET_KEY`.
- Set `CORS_ORIGINS` to the exact frontend origin(s).
- Confirm `FRONTEND_URL` and `BACKEND_URL` use HTTPS.
- Deploy the API and confirm `/health` and `/docs` respond.
- Deploy the frontend with `VITE_API_URL` set before the build.
- Verify registration, login, refresh, logout, resume upload, job matching, roadmap, learning progress, XP, badges, Career GPS, analytics, and admin access.
- Configure external object storage for resume files before relying on uploaded files in production.
- Use an external scheduler or worker for guaranteed job synchronization; free web services can sleep.
- Review SMTP delivery and password-reset behavior.
- Monitor logs and database connection health after the first deployment.
