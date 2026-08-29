# Project Report — Smart Job Skill Gap Analyzer

## 1. Problem Statement

Final-year students and early-career software engineers struggle to prepare for specific companies. Job portals list openings, but they rarely:

- Compare a candidate’s resume skills against a concrete job description  
- Produce a structured learning plan for the missing skills  
- Track progress with measurable readiness signals  

Existing approaches either scrape a fixed set of companies or give generic courses. Candidates targeting companies outside a scraper catalog (Zoho, TCS, startups) are left without the same pipeline.

## 2. Objectives

1. Parse resumes and extract technical skills.  
2. Match candidates against scraped job listings.  
3. Support **any company** via pasted job descriptions (universal target).  
4. Generate a learning roadmap from missing skills.  
5. Track learning progress with XP, levels, badges, and goals.  
6. Present Career GPS readiness and analytics.  
7. Provide secure JWT authentication and an admin skill-review console.  

## 3. System Architecture

Layered architecture: React SPA → FastAPI routers → services → SQLAlchemy → PostgreSQL.

The **active target** (`user_targets`) is the shared object consumed by Job Match, Roadmap, Learning, Career GPS, and Analytics. See [ARCHITECTURE.md](ARCHITECTURE.md).

## 4. Technology Stack

- **Frontend:** React 19, TypeScript, Vite, Material UI  
- **Backend:** Python 3.12, FastAPI, SQLAlchemy  
- **Database:** PostgreSQL  
- **Auth:** JWT (access + refresh), bcrypt  
- **Integrations:** Greenhouse job API, SMTP password reset  

## 5. Modules

| Module | Description |
| --- | --- |
| Authentication | Register, login, refresh, logout, password reset |
| Resume | Upload, parse, extract skills, history |
| Jobs | Greenhouse sync, search, match % |
| Universal Target | Scraped or custom JD as default workflow |
| Roadmap | Skill libraries → topics/projects/resources/milestones |
| Learning | Progress sync, missions, project gating |
| Gamification | XP, levels, badges, daily/weekly goals |
| Career GPS | Readiness scores aligned to active target |
| Analytics | Cross-module dashboards and charts |
| Applications | Track scraped-job applications |
| Admin | Users, jobs, resumes, skill taxonomy approval |

## 6. Workflow

```text
Register → Upload Resume → Choose Target (scraped | custom)
    → Skill Gap → Roadmap → Learning (XP) → Career GPS → Analytics
```

## 7. Database Design

Fifteen tables covering users, jobs, targets, learning, gamification, career goals, and admin skill queue. Primary design choice: progress keyed by `roadmap_id` so custom targets work without a scraped `job_id`. Details in [DATABASE.md](DATABASE.md).

## 8. Screenshots Required (for report / demo)

Capture these screens for the submission PDF:

1. Login / Register  
2. Resume upload result with recommended jobs  
3. Target — scraped company list  
4. Target — custom company form  
5. Roadmap skill cards  
6. Learning dashboard with XP and badges  
7. Career GPS scores  
8. Analytics charts  
9. Dashboard with active target banner  
10. Admin skill pending queue  

## 9. Testing Summary

| Area | Result |
| --- | --- |
| Backend import / OpenAPI routes | Pass |
| Custom JD match + roadmap engine smoke | Pass |
| Frontend production build (`tsc -b && vite build`) | Pass |
| Auth, resume, scraped jobs, learning APIs | Covered by existing flows / unit tests |
| Manual UI checklist | Auth, upload, target modes, roadmap, learning, GPS, analytics, profile, admin |

## 10. Future Enhancements

- Multi-target history and comparison  
- Applications for custom (non-scraped) roles  
- Alembic versioned migrations  
- Durable object storage for resumes  
- External cron for Greenhouse sync on free hosts  
- Optional LLM-assisted JD parsing (kept deterministic today)

## 11. Limitations

- Resume file storage is local/ephemeral on free PaaS.  
- Skill extraction is rule/taxonomy based, not full NLP.  
- Salary / market estimates in Career GPS are heuristic.  
- Applications require scraped jobs.  
- Free hosting may sleep; cold starts delay first request.  

## 12. Conclusion

The project evolves a job-scraper demo into a **career preparation platform**: if a company is scraped, use stored jobs; otherwise paste a JD and reuse the identical analysis pipeline. That design keeps one maintainable architecture while supporting any software company for a final-year demonstration.
