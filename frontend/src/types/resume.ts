export interface RecommendedJob {
    job_id: number;
    job_title: string;
    company: string;
    location: string;
    url: string;
    match_percentage: number;
    matched_skills: string[];
    missing_skills: string[];
}

export interface ResumeResponse {
    filename: string;
    resume_skills: string[];
    recommended_jobs: RecommendedJob[];
}