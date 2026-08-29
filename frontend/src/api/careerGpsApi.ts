import api from "./api";

export type CareerGPSData = {
    readiness_score: number;
    company_readiness: number;
    role_readiness: number;
    interview_readiness: number;
    job_readiness_score: number;
    estimated_salary_growth: { percentage: number; basis: string };
    career_path: string;
    resume_skills: string[];
    completed_skills: string[];
    skill_gaps: string[];
    learning_progress: number;
    completed_projects: number;
    xp: number;
    estimated_learning_days: number;
    technology_trends: { skill: string; demand: number }[];
    market_demand: { skill: string; jobs: number }[];
    recommendations: {
        skills: { name: string; reason: string }[];
        certifications: { name: string; skill: string }[];
        projects: { title: string; skill: string; estimated_days: number }[];
    };
    career_paths: { path: string; score: number; matched_skills: string[]; next_skills: string[] }[];
    career_timeline: { date: string; type: string; title: string; detail: string }[];
    goals: { career_path: string; goal_role: string | null; target_company: string | null };
    active_target: {
        id: number;
        company: string;
        role_title: string;
        source_type: "scraped" | "custom" | null;
        match_percentage: number;
        remaining_skills: string[];
        roadmap_id: string | null;
    } | null;
    current_match_percentage: number;
    remaining_skills: string[];
    source_type: "scraped" | "custom" | null;
    skill_analysis?: { current_skills: string[]; missing_skills: string[]; strong_skills: string[]; weak_skills: string[]; skill_match_percentage: number; priority_skills: string[]; learning_priority: { skill: string; importance: number; estimated_days: number }[]; categories: Record<string, { current: string[]; missing: string[] }> };
    application_insights?: { applications_sent: number; interviews: number; interview_rate: number; rejections: number; rejection_rate: number; offers: number; offer_rate: number; companies_applied: number; average_match_percentage: number; top_industries: string[] };
    learning_plan?: { days: Record<string, unknown[]>; daily_tasks: unknown[]; weekly_goals: string[]; projects: unknown[]; resources: string[]; difficulty: string[]; estimated_days: number; progress_percentage: number };
    interview_preparation?: { required_skills: string[]; topics: string[]; dsa_topics: string[]; system_design_topics: string[]; coding_questions: { question: string; difficulty?: string; tip?: string }[]; hr_questions: string[]; behavioral_questions: string[]; checklist: string[]; tips: string[]; resources: { title: string; url: string; type: string }[] };
    skill_progress?: { completed: string[]; in_progress: string[]; missing: string[]; learning_percentage: number; interview_readiness: number; company_readiness: number; overall_readiness: number };
    daily_goal?: { progress: number; target: number; completed: boolean };
    weekly_goal?: { progress: number; target: number; completed: boolean };
    target?: { company: string; role: string; experience_level: string; source_type: string | null } | null;
    readiness?: { score: number | null; status: string; components: Record<string, number | null>; weights: Record<string, number> };
    skills?: { matched: string[]; missing: string[]; high_priority: string[]; medium_priority: string[]; low_priority: string[]; details: { skill: string; priority: string; reason: string }[] };
    learning?: { status: string; completed: number; in_progress: number; remaining: number; progress_percentage: number | null; items: { skill: string; item: string; status: string }[] };
    coding?: { status: string; attempted: number; solved: number; success_rate: number | null; recommended_practice: string[] };
    interview?: { status: string; completed: number; average_score: number | null; last_interview: string | null; strong_areas: string[]; weak_areas: string[]; recommended_type: string | null };
    roadmap?: { status: string; roadmap_id: string | null; progress_percentage: number | null; completed_topics: number; remaining_topics: number; current_topic: string | null; next_topic: string | null };
    career_goals?: { status: string; active: { key: string; value: string; status: string }[]; completed: unknown[]; pending: { key: string; value: string; status: string }[]; completion_tracking_available: boolean };
    gamification?: { xp: number; current_streak: number; longest_streak: number; badges: { name: string; description: string; unlocked_at: string }[]; daily_goal?: { progress: number; target: number } | null; weekly_goal?: { progress: number; target: number } | null };
    next_action?: { title: string; reason: string };
};

export const getCareerGPS = async () => (await api.get<CareerGPSData>("/career-gps")).data;
export const getAICareerCoach = async () => (await api.get<CareerGPSData>("/career-gps/coach")).data;

export const updateCareerGoals = async (values: Partial<CareerGPSData["goals"]>) =>
    (await api.patch<CareerGPSData>("/career-gps/goals", values)).data;
