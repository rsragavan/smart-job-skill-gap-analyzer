export interface RecentApplication {
    id: number;
    job_id: number;
    job_title: string;
    company: string;
    location: string;
    status: string;
    applied_at: string;
}

export interface DashboardData {
    // Job Statistics
    total_jobs: number;
    total_companies: number;

    // Application Statistics
    total_applications: number;
    applied: number;
    reviewing: number;
    shortlisted: number;
    interview: number;
    offer: number;
    rejected: number;

    // Skills Statistics
    python_jobs: number;
    java_jobs: number;
    docker_jobs: number;
    linux_jobs: number;
    remote_jobs: number;

    // Recent Applications
    recent: RecentApplication[];
    interviews_completed?: number;
    average_interview_score?: number;
    coding_score?: number;
    technical_score?: number;
    hr_score?: number;
    recommended_interviews?: { application_id: number; type: string; company?: string | null; role?: string | null }[];
}
