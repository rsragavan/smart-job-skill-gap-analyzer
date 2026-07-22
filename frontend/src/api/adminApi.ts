import api from "./api";

export type AdminStats = { users: number; active_users: number; resumes: number; jobs: number; active_jobs: number; inactive_jobs: number; last_synchronization: string | null };
export type AdminUser = { id: number; full_name: string; email: string; role: string; is_active: boolean; created_at: string };
export type AdminResume = { id: number; filename: string; uploaded_at: string; user_id: number | null; user_email: string };
export type AdminJob = { id: number; title: string; company: string; location: string; url: string; status: string; inactive_at: string | null };
export const getAdminStats = () => api.get<AdminStats>("/admin/stats").then(({ data }) => data);
export const getAdminUsers = () => api.get<AdminUser[]>("/admin/users").then(({ data }) => data);
export const getAdminResumes = () => api.get<AdminResume[]>("/admin/resumes").then(({ data }) => data);
export const getAdminJobs = (status: "ACTIVE" | "INACTIVE" = "ACTIVE") => api.get<AdminJob[]>("/admin/jobs", { params: { status } }).then(({ data }) => data);
export const syncAdminJobs = () => api.post<{ message?: string; new_jobs?: number }>("/jobs/sync").then(({ data }) => data);
