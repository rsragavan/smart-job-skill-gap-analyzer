import api from "./api";

export type AdminStats = { users: number; active_users: number; resumes: number; jobs: number; active_jobs: number; inactive_jobs: number; companies: number; startups: number; applications: number; target_companies: number; mock_interviews: number; learning_progress: number; last_synchronization: string | null; most_applied_companies: { name: string; count: number }[]; most_popular_roles: { name: string; count: number }[]; recent_registrations: AdminUser[]; recent_applications: { id: number; company: string | null; role: string | null; status: string; applied_at: string }[] };
export type AdminUser = { id: number; full_name: string; email: string; role: string; is_active: boolean; created_at: string };
export type AdminResume = { id: number; filename: string; uploaded_at: string; user_id: number | null; user_email: string };
export type AdminJob = { id: number; title: string; company: string; location: string; url: string; status: string; inactive_at: string | null };
export const getAdminStats = () => api.get<AdminStats>("/admin/stats").then(({ data }) => data);
export const getAdminUsers = () => api.get<AdminUser[]>("/admin/users").then(({ data }) => data);
export const getAdminResumes = () => api.get<AdminResume[]>("/admin/resumes").then(({ data }) => data);
export const getAdminJobs = (status: "ACTIVE" | "INACTIVE" = "ACTIVE") => api.get<AdminJob[]>("/admin/jobs", { params: { status } }).then(({ data }) => data);
export const syncAdminJobs = () => api.post<{ message?: string; new_jobs?: number }>("/jobs/sync").then(({ data }) => data);
export const updateAdminUser = (id: number, payload: { role?: "admin" | "user"; is_active?: boolean }) => api.patch<AdminUser>(`/admin/users/${id}`, payload).then(({ data }) => data);
export const deleteAdminUser = (id: number) => api.delete(`/admin/users/${id}`);
export const updateAdminJob = (id: number, payload: { status: "ACTIVE" | "INACTIVE" }) => api.patch(`/admin/jobs/${id}`, payload);
export const getAdminCompanies = (search = "") => api.get<{ items: { id: number; name: string; industry: string | null; hiring_status: string | null; is_active: boolean }[]; total: number }>("/admin/companies", { params: { search } }).then(({ data }) => data);
export const getAdminAudit = () => api.get<{ items: { id: number; action: string; resource: string; detail: string | null; created_at: string }[]; total: number }>("/admin/audit").then(({ data }) => data);
export const exportAdminResource = (resource: string, format: "json" | "csv") => api.get(`/admin/export/${resource}`, { params: { format }, responseType: format === "csv" ? "blob" : "json" }).then(({ data }) => data);
