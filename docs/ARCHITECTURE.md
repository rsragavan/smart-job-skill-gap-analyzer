# System Architecture

## Overview

Smart Job Skill Gap Analyzer is a layered full-stack application. The frontend is a React SPA. The backend is a FastAPI service with SQLAlchemy models over PostgreSQL. Business logic lives in services; routers stay thin.

```text
┌─────────────────────────────────────────────────────────────┐
│  React 19 + MUI (Vite)                                      │
│  AuthContext · WorkflowContext (active target + roadmap)    │
└───────────────────────────┬─────────────────────────────────┘
                            │ REST + JWT
┌───────────────────────────▼─────────────────────────────────┐
│  FastAPI routers                                            │
│  auth · resume · jobs · targets · roadmap · learning · GPS  │
└───────────────────────────┬─────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────┐
│  Services                                                   │
│  Match · Target · RoadmapEngine · Progress · Gamification   │
│  Career GPS · Analytics · Job Sync                          │
└───────────────────────────┬─────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────┐
│  PostgreSQL                                                 │
│  users · jobs · user_targets · learning_progress · …        │
└─────────────────────────────────────────────────────────────┘
```

## Core design principle: Universal Target

Every learning experience starts from one **active target** per user:

| Mode | Input | Pipeline |
| --- | --- | --- |
| Scraped | Existing `jobs` row | Match resume vs job description |
| Custom | Company + role + pasted JD | Extract skills from text, then same match |

Both modes produce the same snapshot (company, role, match %, matched/missing skills) and feed the same roadmap → learning → Career GPS path.

## Backend layers

| Folder | Responsibility |
| --- | --- |
| `app/api/` | HTTP routers and auth dependencies |
| `app/services/` | Business logic orchestration |
| `app/roadmap/` | Roadmap libraries and engine |
| `app/models/` | SQLAlchemy ORM |
| `app/schemas/` | Pydantic request/response models |
| `app/repositories/` | Data-access helpers where used |
| `app/resume/` | Resume parse + skill extract |
| `app/jobs/` | Job skill extraction |
| `app/core/` | Config and security |
| `app/db/` | Engine, sessions, schema bootstrap |
| `app/scheduler/` | Request-time Greenhouse sync worker |

## Frontend layers

| Folder | Responsibility |
| --- | --- |
| `src/pages/` | Route-level screens |
| `src/components/` | Reusable UI pieces |
| `src/contexts/` | Auth + workflow state |
| `src/api/` | Axios client with refresh, feature APIs |
| `src/services/` | Thin wrappers (dashboard, applications, roadmap) |
| `src/types/` | Shared TypeScript types |
| `src/theme/` | MUI theme (light/dark) |
| `src/routes/` | React Router map |

## Authentication flow

1. Register / login returns access + refresh tokens.
2. Access token is sent as `Authorization: Bearer …`.
3. On 401, the Axios interceptor refreshes via `/auth/refresh`.
4. Password reset uses SMTP + time-limited tokens.

## Roadmap generation flow

```text
Active target missing skills
        │
        ▼
RoadmapEngine.hash(company, role, skill keys)
        │
        ▼
Skill / project / resource / milestone libraries
        │
        ▼
RoadmapResponse (same shape for scraped and custom)
        │
        ▼
learning_progress rows keyed by roadmap_id
```

Unknown skills use safe defaults from `roadmap_defaults.py` (never crash).

## Folder structure (summary)

```text
app/
  api/ services/ models/ schemas/ roadmap/ resume/ jobs/ core/ db/
frontend/
  src/pages/ components/ contexts/ api/ services/ types/ theme/ routes/
docs/
tests/
```
