export type TargetSourceType = "scraped" | "custom";

export interface ActiveTarget {
    id: number;
    source_type: TargetSourceType;
    job_id: number | null;
    company_id: number | null;
    company_role_id: number | null;
    company: string;
    role_title: string;
    location: string | null;
    job_description: string | null;
    match_percentage: number;
    matched_skills: string[];
    missing_skills: string[];
    roadmap_id: string | null;
    is_active: boolean;
    created_at: string;
    updated_at: string;
}

export interface CustomTargetPayload {
    company: string;
    role: string;
    job_description: string;
    location?: string;
}
