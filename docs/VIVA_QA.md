# Viva Preparation — 50 Questions & Answers

Use these during college viva. Answers are aligned with this codebase.

---

### 1. What is the problem your project solves?
Students need company-specific preparation. Generic courses ignore a real job description. This app compares a resume to a target job and builds a learning plan for the gaps.

### 2. What is the main innovation?
**Universal Target** — scraped jobs and pasted JDs share one pipeline and one response format.

### 3. Why FastAPI?
Async-friendly, automatic OpenAPI docs, Pydantic validation, and clean router/dependency injection for JWT.

### 4. Why React + TypeScript?
Component UI with Material UI; TypeScript catches contract mistakes between API and pages.

### 5. Why PostgreSQL?
Relational integrity for users, jobs, targets, progress, and applications; production-ready (e.g., Neon).

### 6. Explain the layered architecture.
Routers → services → models/repositories → database. UI never embeds matching or roadmap business rules.

### 7. What is WorkflowContext?
Frontend state for active target, learning plan, and progress; hydrates from `/targets/active`.

### 8. How does JWT authentication work?
Login returns short-lived access + longer refresh tokens. Access goes in `Authorization`. Refresh rotates tokens; logout invalidates refresh rows.

### 9. Why access and refresh tokens?
Limits exposure of long-lived credentials while keeping sessions usable without re-login every few minutes.

### 10. How are passwords stored?
bcrypt hashes in `users.password_hash`; plain passwords are never stored.

### 11. How does resume parsing work?
Upload → extract text → skill extractor against approved taxonomy → store in `resume_history`.

### 12. How is job matching calculated?
Extract skills from JD → set difference vs resume → match % = matched / total job skills × 100.

### 13. Where is matching implemented?
`JobMatchService.match_job` (DB job) and `match_text` (raw description) — same logic.

### 14. What is a scraped target?
User selects a Greenhouse-synced `jobs` row; server stores `user_targets` with `source_type=scraped`.

### 15. What is a custom target?
Company + role + pasted JD; `source_type=custom`; no requirement that the company exist in `companies`.

### 16. What if the company is unknown?
No error — save custom target and run extraction/match/roadmap normally.

### 17. What if a skill is unknown?
Roadmap defaults generate difficulty, days, topics, projects, resources, XP; engine does not crash.

### 18. How is roadmap_id generated?
SHA-256 hash of company, role, and ordered skill keys (truncated) so the same plan maps to stable progress.

### 19. Why key learning progress by roadmap_id?
Custom targets have no job_id; roadmap_id works for both modes.

### 20. What does the Roadmap Engine output?
Company, role, match %, skills list with topics, resources, projects, milestones, total XP, estimated days.

### 21. Difference between `/roadmap/generate` and `/learning/job/{id}`?
UI uses roadmap/target path. `/learning/job/{id}` is a preserved alternate API that builds a plan from a scraped job.

### 22. How do XP and levels work?
Completing topics/projects/missions awards XP; level titles come from reward thresholds; stored in gamification tables.

### 23. What are daily and weekly goals?
Targets for completions in a day/week; progress and completion flags live on `user_gamification`.

### 24. How are badges unlocked?
Gamification service evaluates events (streaks, completions) and inserts `user_badges` / achievements.

### 25. What is Career GPS?
Dashboard of readiness scores, gaps, paths, trends, timeline — prefers active target company/role/match.

### 26. How does Career GPS differ from Analytics?
GPS is career-readiness oriented for the user/target; Analytics aggregates broader module statistics and charts.

### 27. How are Greenhouse jobs synced?
Admin `/jobs/sync` fetches company boards and upserts `jobs`.

### 28. Why keep applications scraped-only?
`job_applications.job_id` FK requires a real job row; custom JD targets are learning-focused in this phase.

### 29. How is dark mode implemented?
MUI theme mode via `useTheme` / theme provider; CssBaseline applies palette.

### 30. How is the SPA secured?
`ProtectedRoute` checks auth; admin routes require admin role; API enforces roles with dependencies.

### 31. What is CORS and why configure it?
Browsers block cross-origin API calls; `CORS_ORIGINS` must list the frontend URL.

### 32. Explain SQLAlchemy’s role.
ORM maps Python models to tables; sessions manage transactions; `create_all` bootstraps schema in this project.

### 33. What is Pydantic used for?
Request/response schemas (e.g., `CustomTargetRequest`, `RoadmapResponse`) with validation.

### 34. How do you prevent duplicate active targets?
Service deactivates prior `is_active` rows before inserting the new active target.

### 35. What happens if no resume exists when setting a target?
API returns 400 asking the user to upload a resume first.

### 36. How does the frontend refresh tokens?
Axios interceptor on 401 calls `/auth/refresh`, retries the request, or clears auth on failure.

### 37. What is Material UI’s benefit here?
Consistent accessible components, responsive Grid/Stack, built-in dark mode support.

### 38. How is mobile responsiveness handled?
MUI breakpoints (`xs`/`sm`/`md`), permanent sidebar on desktop, navbar menu on mobile.

### 39. Name three security measures.
JWT secrets, password hashing, CORS restriction, security headers middleware, role checks.

### 40. What is the technical_skills_engine?
Loads approved skills (including admin-approved unknowns) used during extraction/matching.

### 41. How would you scale job sync?
Move scheduler off the web process to cron/worker; use queues for large company sets.

### 42. Limitation of free hosting?
Cold starts, ephemeral disk for uploads, sleeping services break in-process schedulers.

### 43. Why not scrape every company?
Impossible to cover the market; custom JD path covers the long tail with one architecture.

### 44. How are API errors handled?
HTTPException for expected cases; global handlers return generic 500 messages without leaking internals.

### 45. What tests exist?
Unit tests for services such as learning recommendation and resume analysis; smoke tests for match/roadmap.

### 46. How would you add Alembic?
Generate migrations from model diffs; replace ad-hoc `create_all` for production schema changes.

### 47. React Router’s role?
Declares routes; lazy-loads pages; protects authenticated sections.

### 48. What is idempotent about roadmap generation?
Same company/role/skills → same roadmap_id → progress continues for that plan.

### 49. How does Analytics use the active target?
Frontend seeds company/role filters from the active target for contextual charts.

### 50. One sentence pitch for evaluators?
A JWT-secured career platform that turns any job description—scraped or pasted—into a skill gap, roadmap, and measurable readiness score without duplicating engines.
