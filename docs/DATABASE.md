# Database Design

PostgreSQL via SQLAlchemy. Development creates missing tables with `create_schema()` / `create_tables.py`.

## Tables

| Table | Purpose |
| --- | --- |
| `users` | Accounts (name, email, password hash, role, active) |
| `refresh_tokens` | Refresh token persistence |
| `password_reset_tokens` | Password reset flow |
| `companies` | Greenhouse company sync config |
| `jobs` | Scraped job postings |
| `job_applications` | User applications for scraped jobs |
| `resume_history` | Uploaded resumes and extracted skills |
| `user_targets` | Active career target (scraped or custom JD) |
| `learning_progress` | Topic/project/mission status per roadmap |
| `user_gamification` | XP, streaks, daily/weekly goals |
| `user_badges` | Unlocked badges |
| `achievements` | Achievement records |
| `gamification_events` | XP/event audit trail |
| `career_progress` | Cached Career GPS scores |
| `career_goals` | Key/value career goals |
| `unknown_skills` | Admin taxonomy review queue |

## Key relationships

```text
users 1──* resume_history
users 1──* user_targets          (one is_active at a time, enforced in service)
users 1──* learning_progress     (keyed by roadmap_id hash)
users 1──1 user_gamification
users 1──* job_applications ──* jobs
jobs *──1 companies (by company name / sync config)
```

## `user_targets` (universal target)

| Column | Notes |
| --- | --- |
| `source_type` | `scraped` \| `custom` |
| `job_id` | Nullable FK for scraped jobs |
| `company`, `role_title` | Display + GPS + roadmap inputs |
| `job_description` | Custom JD text (and snapshot for scraped) |
| `match_percentage`, `matched_skills`, `missing_skills` | Skill-gap snapshot |
| `roadmap_id` | Hash from RoadmapEngine |
| `is_active` | Current target flag |

## Design notes

- Learning progress is keyed by **roadmap_id**, not job_id, so custom targets work identically.
- Applications remain tied to scraped `jobs` only.
- Unknown skills never block roadmap generation; defaults are generated and may be queued for admin approval when discovered through extraction.
