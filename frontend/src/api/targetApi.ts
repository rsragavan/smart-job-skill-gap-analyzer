import api from "./api";
import type { RoadmapResponse } from "../services/roadmapService";
import type { ActiveTarget, CustomTargetPayload } from "../types/target";

function errorMessage(error: unknown, fallback: string) {
    if (typeof error === "object" && error !== null && "response" in error) {
        const detail = (error as { response?: { data?: { detail?: string } } }).response?.data?.detail;
        if (typeof detail === "string" && detail.trim()) return detail;
    }
    return error instanceof Error ? error.message : fallback;
}

export async function getActiveTarget(): Promise<ActiveTarget | null> {
    const { data } = await api.get<ActiveTarget | null>("/targets/active");
    return data;
}

export type SkillGapAnalysis = {
    target: { company: string; role: string; source_type: string };
    resume_skills: string[];
    match_percentage: number;
    matched_skills: string[];
    missing_skills: string[];
    missing_skill_details: { skill: string; priority: string; reason: string; job_market: { jobs: number | null; status: string } }[];
    learning_recommendations: { title: string; skill: string; reason: string }[];
    coding_recommendations: { id: number; title: string; topic: string; difficulty: string; reason: string }[];
    interview_recommendations: { id: number; question: string; category: string; topic: string; source: string; reason: string }[];
};

export async function getActiveSkillGap(): Promise<SkillGapAnalysis> {
    const { data } = await api.get<SkillGapAnalysis>("/targets/active/skill-gap");
    return data;
}

export async function setTargetFromJob(jobId: number): Promise<ActiveTarget> {
    try {
        const { data } = await api.post<ActiveTarget>(`/targets/from-job/${jobId}`);
        return data;
    } catch (error) {
        throw new Error(errorMessage(error, "Unable to set target from job."), { cause: error });
    }
}

export async function setCustomTarget(payload: CustomTargetPayload): Promise<ActiveTarget> {
    try {
        const { data } = await api.post<ActiveTarget>("/targets/custom", payload);
        return data;
    } catch (error) {
        throw new Error(errorMessage(error, "Unable to create custom target."), { cause: error });
    }
}

export async function generateActiveTargetRoadmap(): Promise<RoadmapResponse> {
    try {
        const { data } = await api.post<RoadmapResponse>("/targets/active/generate-roadmap");
        return data;
    } catch (error) {
        throw new Error(errorMessage(error, "Unable to generate roadmap for active target."), { cause: error });
    }
}

export async function clearActiveTarget(): Promise<void> {
    await api.delete("/targets/active");
}
