# Production Readiness

## Runtime checks

- Backend health: `GET /health`
- OpenAPI documentation: `/docs` and `/redoc`
- Frontend build: `npm ci && npm run build`
- Backend compile: `python -m compileall -q app`
- Backend tests: `python -m pytest -q`
- Frontend quality: `npm run lint`

## Security checklist

- Use a unique `JWT_SECRET_KEY` with at least 32 characters.
- Keep access tokens short-lived and validate refresh-token digest, expiry, type, and revocation.
- Set `CORS_ORIGINS` to explicit HTTPS frontend origins; wildcards are rejected by configuration validation.
- Keep `ENVIRONMENT=production` and never commit `.env` files or uploaded resumes.
- Confirm `/admin/*` returns 403 for authenticated non-admin users.
- Confirm resume uploads are restricted to bounded PDF content and stored outside source control.

## Operational checklist

- Run `python create_tables.py` before the first deployment.
- Use PostgreSQL with SSL and monitor connection health.
- Use external object storage for production resume files.
- Run job synchronization through an external scheduler or a worker when the web service can sleep.
- Monitor structured application, authentication, synchronization, and admin audit logs.
- Back up PostgreSQL before schema changes; the project currently uses additive startup schema creation rather than Alembic migrations.

## Request flows

Authentication is JWT access-token based with refresh-token rotation. Protected FastAPI dependencies enforce authenticated user or admin roles. React restores the session, retries one expired access token through refresh, and clears the session when refresh fails. Resume processing validates the upload before parsing, persists ATS and skill-gap results, and feeds dashboard, roadmap, learning, and analytics services.
