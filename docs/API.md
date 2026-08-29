# API Documentation

Interactive OpenAPI UI: `GET /docs` (Swagger) and `GET /redoc`.

All user routes require a JWT access token unless noted. Admin routes require `role=admin`.

## System

| Method | Path | Description |
| --- | --- | --- |
| GET | `/` | API metadata |
| GET | `/health` | Health check |

## Authentication

| Method | Path | Description |
| --- | --- | --- |
| POST | `/auth/register` | Create user |
| POST | `/auth/login` | Access + refresh tokens |
| POST | `/auth/refresh` | Rotate tokens |
| POST | `/auth/logout` | Invalidate refresh token |
| GET | `/auth/me` | Current user |
| POST | `/auth/forgot-password` | Email reset link |
| POST | `/auth/reset-password` | Set new password |

## Resume

| Method | Path | Description |
| --- | --- | --- |
| POST | `/resume/upload` | Parse resume, extract skills, recommend jobs |
| GET | `/resume/history` | Upload history |
| DELETE | `/resume/history/{history_id}` | Delete history row |

## Jobs

| Method | Path | Description |
| --- | --- | --- |
| GET | `/jobs/` | List scraped jobs with per-user match |
| POST | `/jobs/sync` | Admin Greenhouse sync |

## Universal Target

| Method | Path | Description |
| --- | --- | --- |
| GET | `/targets/active` | Active target or `null` |
| POST | `/targets/from-job/{job_id}` | Set scraped target |
| POST | `/targets/custom` | Set custom company + JD |
| POST | `/targets/active/generate-roadmap` | Generate roadmap for active target |
| DELETE | `/targets/active` | Clear active target |

**Custom target body**

```json
{
  "company": "Zoho",
  "role": "Software Developer",
  "job_description": "Paste full JD…",
  "location": "Chennai"
}
```

## Roadmap & Learning

| Method | Path | Description |
| --- | --- | --- |
| POST | `/roadmap/generate` | Generate roadmap from company/role/skills |
| POST | `/learning/job/{job_id}` | Alternate job-plan endpoint (API preserved) |
| POST | `/learning/progress/sync` | Sync roadmap items for progress tracking |
| GET | `/learning/progress/{roadmap_id}` | Get progress |
| PATCH | `/learning/progress/{roadmap_id}` | Update topic/project/mission status |
| GET | `/learning/gamification` | XP, streaks, badges, goals |

## Career GPS & Analytics

| Method | Path | Description |
| --- | --- | --- |
| GET | `/career-gps` | Readiness dashboard (prefers active target) |
| PATCH | `/career-gps/goals` | Update career path / role / company goals |
| GET | `/analytics/dashboard` | Combined analytics |
| GET | `/analytics/overview` | Overview metrics |
| GET | `/analytics/top-skills` | Top skills |

## Applications & Dashboard

| Method | Path | Description |
| --- | --- | --- |
| GET | `/dashboard` | User dashboard aggregates |
| POST | `/applications` | Track application for scraped job |
| GET | `/applications` | List applications |
| PATCH | `/applications/{id}` | Update status/notes |
| DELETE | `/applications/{id}` | Delete application |
| GET | `/applications/dashboard` | Application stats |

## Users & Admin

| Method | Path | Description |
| --- | --- | --- |
| GET/PATCH | `/users/me`, `/users/me/profile` | Profile |
| GET | `/users/` | Admin list users |
| POST | `/users/{id}/deactivate` | Admin deactivate |
| GET | `/admin/stats` | Admin overview |
| GET | `/admin/users`, `/admin/resumes`, `/admin/jobs` | Admin tables |
| GET | `/admin/skills/pending` | Unknown skill queue |
| POST | `/admin/skills/{id}/approve` | Approve skill |
| POST | `/admin/skills/{id}/reject` | Reject skill |

## Error conventions

- `400` — validation / missing resume before target selection  
- `401` — missing/invalid token  
- `403` — insufficient role  
- `404` — resource not found  
- `500` — unexpected server error (generic message to client)
