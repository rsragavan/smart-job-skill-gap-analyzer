export interface RoadmapItem {
    skill: string;
    difficulty: string;
    estimated_days: number;
    priority: number;
    topics: string[];
    learning_resource: string;
}

export interface LearningResponse {
    job_title: string;
    company: string;
    resume_skills: string[];
    job_skills: string[];
    matched_skills: string[];
    missing_skills: string[];
    match_percentage: number;
    total_missing_skills: number;
    estimated_completion_days: number;
    learning_roadmap: RoadmapItem[];
}

