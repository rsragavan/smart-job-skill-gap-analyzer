# Admin Guide

Admin accounts use `role = admin`. After login, admins land on **/admin**.

## Capabilities

### Dashboard stats

View high-level counts (users, resumes, jobs, pending skills).

### Users

List users and deactivate accounts when needed.

### Resumes & jobs

Inspect uploaded resume history and scraped job inventory.

### Skill taxonomy queue

Unknown skills discovered during extraction appear under pending skills:

1. Review the skill name and frequency.
2. **Approve** — adds to the approved technical skills engine for future matching.
3. **Reject** — dismisses the pending entry.

### Job synchronization

Trigger Greenhouse sync via `POST /jobs/sync` (admin). For production free hosts that sleep, prefer an external cron hitting this endpoint.

## Creating an admin

Admins are typically promoted in the database (`users.role = 'admin'`) or seeded during setup. Regular registration creates `user` role accounts.

## Security checklist

- Use a strong `JWT_SECRET_KEY` (32+ characters in production).  
- Restrict `CORS_ORIGINS` to the real frontend origin.  
- Never commit `.env` secrets.  
- Keep SMTP credentials as App Passwords, not account passwords.  
- Rotate refresh tokens on logout.

## Operational notes

- Render free tiers: ephemeral disk — resume files in `uploads/` are not durable across restarts.  
- Schema bootstrap uses SQLAlchemy `create_all` / lightweight column checks; introduce Alembic before destructive schema changes in long-lived production.
