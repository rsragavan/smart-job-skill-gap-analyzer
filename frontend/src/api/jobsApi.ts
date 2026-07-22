import api from "./api";
import type { JobsResponse } from "../types/job";

export interface JobsSearchParams {
    keyword?: string;
    title?: string;
    company?: string;
    location?: string;
    department?: string;
    employment_type?: string;
    required_skills?: string;
    page?: number;
    page_size?: number;
    status?: "ACTIVE" | "INACTIVE" | "ALL";
    sort?: "newest" | "match" | "company" | "title";
}

export const getJobs = async (params: JobsSearchParams = {}): Promise<JobsResponse> => {
    const response = await api.get<JobsResponse>("/jobs/", {
        params: {
            keyword: params.keyword ?? "",
            title: params.title ?? "",
            company: params.company ?? "",
            location: params.location ?? "",
            department: params.department ?? "",
            employment_type: params.employment_type ?? "",
            required_skills: params.required_skills ?? "",
            page: params.page ?? 1,
            page_size: params.page_size ?? 12,
            status: params.status ?? "ACTIVE",
            sort: params.sort ?? "newest",
        },
    });

    return response.data;
};
