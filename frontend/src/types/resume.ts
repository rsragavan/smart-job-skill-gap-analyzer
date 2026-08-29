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
    resume_id?: number;
    filename: string;
    resume_skills: string[];
    recommended_jobs: RecommendedJob[];
    ats_report?: ATSReport;
}

export interface ATSReport {
    overall_score: number;
    components: Record<string, { score: number; explanation: string }>;
    contact_information: Record<string, string | null | boolean>;
    sections: Record<string, boolean>;
    missing_sections: string[];
    skills: string[];
    summary: string;
    keywords: { matched: string[]; missing: string[]; recommended: string[]; match_percentage: number; target_role?: string | null; target_company?: string | null };
    skill_gap: { current: string[]; missing: string[]; strong: string[]; weak: string[]; priority: string[]; estimated_learning_days: number };
    projects: Array<{ title: string; complexity: string; technology_match: string[]; relevance: string; improvement: string }>;
    improvements: Record<string, string[]>;
}
