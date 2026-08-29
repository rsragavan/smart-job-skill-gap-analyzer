import api from "./api";

export const getTopSkills = async () => {

    const response = await api.get(
        "/analytics/top-skills"
    );

    return response.data;
};

export const getOverview = async () => {
    const response = await api.get("/analytics/overview");
    return response.data;
};

export type AnalyticsDashboard = {
    filters: { company: string | null; role: string | null; skill: string | null; date_from: string | null; date_to: string | null };
    resume_statistics: { uploads: number; latest_upload: string | null; skills: number };
    job_statistics: { jobs: number; companies: number; applications: number };
    skill_statistics: { top: { name: string; count: number }[]; match_percentage: number; matched: string[]; missing: string[] };
    learning_statistics: { total_items: number; completed_items: number; progress: number; missions_completed: number };
    roadmap_statistics: { roadmaps: number; skills: number; completed_skills: number; projects_completed: number };
    career_statistics: { readiness: number; role_readiness: number; path: string };
    xp_statistics: { total: number; level: number; growth: { date: string; xp: number }[] };
    badge_statistics: { unlocked: number; achievements: number };
    mission_statistics: { total: number; completed: number; completion_percentage: number };
    charts: { skill_match: { name: string; value: number }[]; learning_progress: { name: string; value: number }[]; completed_skills: { name: string; value: number }[]; missing_skills: { name: string; value: number }[]; projects_completed: { name: string; value: number }[]; daily_activity: { date: string; activity: number }[]; weekly_activity: { period: string; activity: number }[]; monthly_activity: { period: string; activity: number }[] };
};

export type PlacementAnalytics = {
    readiness: { overall: number; company: number; interview: number; coding: number; resume: number; communication: number; learning: number; trend: { label: string; value: number }[] };
    applications: { submitted: number; accepted: number; rejected: number; shortlisted: number; interview_scheduled: number; offers: number; offer_rate: number; response_rate: number; company_wise: Record<string, number>; role_wise: Record<string, number>; monthly_timeline: { month: string; applications: number }[] };
    companies: { top_hiring: [string, number][]; most_applied: [string, number][]; highest_match: { company: string; jobs: number; match_percentage: number }[]; missing_skills: { company: string; jobs: number; match_percentage: number }[]; remote_friendly: string[] };
    skills: { most_requested: [string, number][]; strong: string[]; missing: string[]; rare: string[]; trending: [string, number][]; learning_progress: number };
    interviews: { mock_interviews: number; completed: number; average_score: number; best_company: string | null; weak_areas: string[]; technical_progress: number; hr_progress: number; coding_progress: number };
    timeline: { date: string; type: string; title: string }[];
    recommendations: { companies: { company: string; jobs: number; match_percentage: number }[]; startups: { id: number; name: string; industry: string }[]; skills: { skill: string; reason: string }[]; mock_interviews: { type: string; reason: string }[]; coding_practice: { topic: string; reason: string }[] };
};

export type AnalyticsNotification = { type: string; title: string; detail: string; severity: "info" | "warning" };

export const getAnalyticsDashboard = async (filters: { company?: string; role?: string; skill?: string; date_from?: string; date_to?: string } = {}) => {
    const response = await api.get<AnalyticsDashboard>("/analytics/dashboard", { params: filters });
    return response.data;
};

export const getPlacementAnalytics = async () => (await api.get<PlacementAnalytics>("/analytics/placement")).data;
export const getAnalyticsNotifications = async () => (await api.get<AnalyticsNotification[]>("/analytics/notifications")).data;

export const downloadPlacementReport = async (reportType: string) => {
    const response = await api.get<Blob>("/analytics/placement/report", { params: { report_type: reportType }, responseType: "blob" });
    const url = window.URL.createObjectURL(response.data);
    const link = document.createElement("a");
    link.href = url;
    link.download = `${reportType}-report.pdf`;
    link.click();
    window.URL.revokeObjectURL(url);
};
