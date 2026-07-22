export interface Job {
    id: number;
    title: string;
    company: string;
    location: string;
    department: string;
    employment_type: string;
    url: string;
    description?: string;
    status: "ACTIVE" | "INACTIVE";
    posted_date: string;
    match_percentage: number;
    matched_skills: string[];
    missing_skills: string[];
}

export interface JobsResponse {
    count: number;
    total_count: number;
    page: number;
    page_size: number;
    total_pages: number;
    has_next: boolean;
    has_previous: boolean;
    jobs: Job[];
}
