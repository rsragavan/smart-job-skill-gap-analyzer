# Phase 14 — Project Demo Preparation

**Project:** Smart Job Skill Gap Analyzer  
**Audience:** Final-year college evaluation / viva demo  
**Goal:** Show a complete, error-free walkthrough that proves the Universal Target career-preparation platform.

---

## Pre-demo checklist (do this before faculty arrives)

Complete these steps once so the live demo never fails:

1. Start backend (`uvicorn`) and frontend (`npm run dev`). Confirm `/health` returns OK.
2. Have two accounts ready:
   - **User account** — with a resume already uploaded (or a clean PDF ready)
   - **Admin account** — for the last segment only
3. Confirm scraped jobs exist (run admin job sync if the Jobs list is empty).
4. Keep a **short custom JD text** ready (Zoho / any company) for the Universal Target moment.
5. Clear browser cache only if auth looks stuck; otherwise keep an already-logged-in user tab ready as backup.
6. Use Chrome/Edge; zoom 90–100% so sidebars and charts fit on a projector.

### Demo-safe rules

| Do | Don’t |
| --- | --- |
| Upload resume **before** Target | Select Target with no resume (400 error) |
| Wait for loading spinners to finish | Double-click generate buttons |
| Show **one** scraped job OR one custom JD | Change targets mid-sentence |
| Complete **one** learning item for XP | Rush through every skill |
| Open Admin last, then logout | Switch accounts without logging out first |

---

## 1. Five-minute demo script

**Pitch (20 sec):**  
“This is a career preparation platform. Students upload a resume, pick any company job—scraped or pasted—and get a skill gap, learning roadmap, XP progress, and Career GPS readiness. One pipeline supports every software company.”

| Time | Action | What to say |
| --- | --- | --- |
| 0:00–0:40 | **Login** | “JWT-secured login with access and refresh tokens.” |
| 0:40–1:20 | **Upload Resume** | “We parse the file and extract technical skills.” Show extracted skills. |
| 1:20–2:10 | **Target → Scraped job** | “Select a Greenhouse job. Match % shows overlapped vs missing skills.” |
| 2:10–2:50 | **Roadmap** | “Missing skills become topics, projects, resources, and milestones.” |
| 2:50–3:40 | **Learning + XP** | Mark one topic complete. “XP, levels, and daily goals update.” |
| 3:40–4:20 | **Career GPS** | “Readiness scores follow the active target—company, role, remaining skills.” |
| 4:20–4:50 | **Analytics** (quick) | “Cross-module stats and charts.” |
| 4:50–5:00 | Close | “Same pipeline works for any pasted JD. Thank you.” |

**Skip in 5-min mode:** Custom JD form detail, Admin dashboard, full badge explanation.

---

## 2. Ten-minute demo script

**Opening (30 sec):**  
“Final-year project: Smart Job Skill Gap Analyzer. Problem—students prepare generically. Solution—universal target: scraped company or any pasted job description, same analysis pipeline.”

| Time | Step | Talk track |
| --- | --- | --- |
| 0:00–0:45 | Login | Auth, roles (user vs admin). |
| 0:45–1:45 | Upload + parsing | File upload → extract skills → recommended jobs. |
| 1:45–3:00 | Job matching / Target (scraped) | Filters, match %, matched (green) / missing (red) chips, set target. |
| 3:00–3:45 | **Custom Company tab** | Paste Zoho-style JD. “Company need not exist in our DB.” |
| 3:45–4:45 | Roadmap | Source badge, XP estimate, skill cards, resources. |
| 4:45–6:15 | Learning Dashboard | Topics, missions, project locking, complete one item → XP/badge/goal. |
| 6:15–7:15 | Career GPS | Match %, readiness rings, remaining skills, market demand. |
| 7:15–8:00 | Analytics | Filters seeded from active target; charts. |
| 8:00–9:00 | Admin (switch account) | Pending skills approve/reject, stats. |
| 9:00–9:30 | Logout | Session end / token invalidation. |
| 9:30–10:00 | Closing | Architecture one-liner + Q&A invitation. |

---

## 3. Complete feature walkthrough

### Authentication
- Register / Login / Forgot password / Refresh / Logout  
- Demo: login as user → later admin → logout  

### Resume Upload & Parsing
- PDF/DOCX upload, size limit, skill extraction, history  
- Demo: show skills list + recommended jobs  

### Job Matching
- Scraped jobs with per-user match percentage  
- Demo: sort by match, open a high-match card  

### Universal Target
- Scraped selection **or** custom company + pasted JD  
- Demo: emphasize “any company in the world”  

### Roadmap Generation
- Missing skills → library/defaults → roadmap_id  
- Demo: topics, resources, projects, milestones, estimated days  

### Learning Module
- Progress sync, missions, ordered projects  
- Demo: start topic → complete → see status  

### XP, Levels, Badges, Daily Goals
- Gamification service updates on completions  
- Demo: XP chip, streak/goals cards, badge if unlocked  

### Career GPS
- Target-aware readiness, gaps, paths, timeline  
- Demo: “Current Match” and remaining skills for active target  

### Analytics
- Resume, jobs, learning, roadmap, career, XP stats + charts  
- Demo: company/role filters from target  

### Profile
- Account info, logout  

### Admin Dashboard
- Stats, users, resumes, jobs, skill taxonomy queue, sync  

---

## 4. Step-by-step demo sequence (error-free)

Follow this exact order during the live demo.

### Step 1 — Login
1. Open the app URL.  
2. Sign in with the prepared **user** account.  
3. Confirm Dashboard loads (active-target banner may be empty—that is OK).

**If error:** Wrong password → use backup account. Never reset password live unless SMTP is confirmed.

### Step 2 — Upload Resume
1. Go to **Upload Resume**.  
2. Choose a resume that contains clear tech skills (Python, React, SQL, etc.).  
3. Wait until success UI shows extracted skills.

**If error:** File too large / wrong type → use the prepared smaller PDF.

### Step 3 — Resume Parsing (show results)
1. Point to extracted skills.  
2. Scroll recommended jobs if present.  
3. Optionally: “Set Target & Learn” on one recommendation **or** continue to Target page.

### Step 4 — Job Matching
1. Open **Target** (nav label; route `/jobs`).  
2. Stay on **Scraped Company**.  
3. Search a known company (e.g. GitLab / Cloudflare).  
4. Show match % and skill chips on a card.  
5. Select the job → wait for roadmap generation.

**If error:** “Upload a resume first” → return to Step 2. Empty list → admin sync earlier, or switch to Custom tab.

### Step 5 — Roadmap Generation
1. On **Roadmap**, show company, role, source chip, match bar.  
2. Open one skill card: topics → resources → projects → milestones.  
3. Mention estimated days and total XP.

### Step 6 — Learning Dashboard
1. Open **Learning**.  
2. Confirm company/role header matches the target.  
3. Start one topic, then mark it **completed**.

### Step 7 — XP & Badges
1. Point to XP / level card.  
2. Show daily/weekly goal progress bars.  
3. If a badge unlocked, highlight it; if not, explain unlock conditions without forcing many clicks.

### Step 8 — Career GPS
1. Open **Career GPS**.  
2. Show active-target alert (company, role, source, match %).  
3. Point to readiness scores and remaining skills.  
4. Briefly mention market demand from scraped jobs.

### Step 9 — Analytics
1. Open **Analytics**.  
2. Note filters defaulted from active target.  
3. Show one chart panel (skill match / learning / XP).

### Step 10 — Admin Dashboard
1. **Logout** from user (Profile → Logout or login page).  
2. Login as **admin**.  
3. Open **Admin**: stats → pending skills (approve one if available).  
4. Mention job sync for Greenhouse data.

### Step 11 — Logout
1. Logout admin.  
2. Confirm redirect to Login.  
3. End: “Questions welcome.”

### Optional “wow” insert (after Step 4 or instead of second scraped job)
1. Target → **Custom Company**.  
2. Paste prepared JD (company Zoho, role Software Developer).  
3. Generate → show identical roadmap experience.  
4. Say: “We did not scrape Zoho; the same engines ran.”

---

## 5. Expected faculty questions & best answers

### Q1. What is the novelty of your project?
**A:** Universal Target. Scraped jobs and pasted JDs share one match → roadmap → learning → GPS pipeline, so any company is supported without scraping the world.

### Q2. Why not only scrape jobs?
**A:** Scraping cannot cover every employer. Custom JD input covers the long tail while keeping one maintainable architecture.

### Q3. How is match percentage calculated?
**A:** Extract skills from the job description, compare with resume skills, then matched ÷ total job skills × 100.

### Q4. Which technologies did you use?
**A:** React 19 + TypeScript + MUI frontend; FastAPI + SQLAlchemy + PostgreSQL backend; JWT auth; Greenhouse for scraped jobs.

### Q5. How do you secure the API?
**A:** bcrypt password hashes, short-lived JWT access tokens, refresh tokens in DB, role checks, CORS allowlist, security headers.

### Q6. Explain roadmap_id.
**A:** A hash of company, role, and skill keys. Learning progress attaches to that id so custom targets (no job_id) still track correctly.

### Q7. What if an unknown skill appears?
**A:** Defaults generate a learning path (difficulty, days, topics, projects, XP). Admins can later approve skills into the taxonomy.

### Q8. Is Career GPS using AI/LLM?
**A:** No generative LLM in the core path. Scores are rule/heuristic based on resume, target skills, learning progress, and XP—deterministic and demo-stable.

### Q9. How is the database designed?
**A:** Users, jobs, `user_targets`, learning_progress, gamification tables, career_goals/progress, applications, unknown_skills. One active target per user enforced in the service layer.

### Q10. What are the limitations?
**A:** Taxonomy-based extraction (not full NLP), applications only for scraped jobs, free hosting cold starts/ephemeral uploads, salary estimates are heuristic.

### Q11. How would you improve it next?
**A:** Alembic migrations, object storage for resumes, multi-target history, custom-target applications, optional LLM-assisted parsing, external job-sync worker.

### Q12. Difference between Learning and Roadmap pages?
**A:** Roadmap is the plan view. Learning is interactive progress (checkboxes, missions, XP) synced to the backend for that roadmap_id.

---

## 6. Project flow explanation

```text
Register / Login
      ↓
Upload Resume → Extract Skills → (optional recommendations)
      ↓
Choose Target
   ├─ Scraped Job  → match vs Job.description
   └─ Custom JD    → match vs pasted text
      ↓
Persist user_targets (active) + sync Career GPS goals
      ↓
Generate Roadmap (missing skills → libraries/defaults)
      ↓
Learning progress + XP / badges / goals
      ↓
Career GPS readiness + Analytics
```

**One sentence for faculty:**  
“Everything after target selection consumes the same target object—company, role, source, skills, and match percentage.”

---

## 7. Architecture explanation (demo wording)

“We use a layered architecture. The React SPA talks to FastAPI over REST with JWT. Routers stay thin; services hold business logic—match, target orchestration, roadmap engine, learning progress, gamification, Career GPS. SQLAlchemy models map to PostgreSQL. The frontend WorkflowContext keeps the active target and learning plan so Roadmap, Learning, GPS, and Analytics stay consistent.”

Diagram (say aloud):

```text
UI (React) → API (FastAPI) → Services → PostgreSQL
                 ↑
         JWT + role guards
```

---

## 8. Database explanation (demo wording)

“Core tables: `users` for accounts; `jobs` for scraped postings; `user_targets` for the active scraped or custom goal; `resume_history` for skills; `learning_progress` keyed by roadmap_id; gamification tables for XP and badges; `career_progress` / `career_goals` for GPS; `unknown_skills` for admin review.”

Emphasize: **progress is not forced to job_id**, which is why custom companies work.

---

## 9. API explanation (demo wording)

“Important endpoints: `/auth/*` for login; `/resume/upload` for parsing; `/jobs/` for listings; `/targets/from-job/{id}` and `/targets/custom` for the universal target; `/targets/active/generate-roadmap` or `/roadmap/generate` for plans; `/learning/progress/*` for XP tracking; `/career-gps` and `/analytics/dashboard` for insights; `/admin/*` for taxonomy.”

Point to live Swagger at `/docs` if time allows (10-min demo only).

---

## 10. Future enhancements

1. Versioned Alembic migrations for production schema changes  
2. Cloud object storage for durable resume files  
3. Multi-target history and side-by-side comparison  
4. Job applications for custom (non-scraped) targets  
5. External cron/worker for Greenhouse sync on free hosts  
6. Optional LLM-assisted JD skill extraction (keep current path as fallback)  
7. Deeper interview-prep module tied to remaining skills  
8. Export roadmap as PDF for placement files  

---

## Closing lines (memorize one)

**5-minute close:**  
“We turned a job scraper into a career preparation platform—any company, one pipeline.”

**10-minute close:**  
“Scraped data when we have it; pasted JD when we don’t—same match, roadmap, learning, and Career GPS. That is the project contribution.”

---

## Quick reference — screens and routes

| Demo step | Nav / route |
| --- | --- |
| Login | `/login` |
| Upload | `/upload` |
| Target / matching | `/jobs` |
| Roadmap | `/roadmap` |
| Learning / XP | `/learning` |
| Career GPS | `/career-gps` |
| Analytics | `/analytics` |
| Profile / logout | `/profile` |
| Admin | `/admin` |

Related docs: [USER_GUIDE.md](USER_GUIDE.md) · [ARCHITECTURE.md](ARCHITECTURE.md) · [VIVA_QA.md](VIVA_QA.md) · [PROJECT_REPORT.md](PROJECT_REPORT.md)
