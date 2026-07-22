import { createContext, useContext, useMemo, useState } from "react";
import type { ReactNode } from "react";

import type { LearningResponse } from "../types/learning";

const SELECTED_JOB_STORAGE_KEY = "selected_job";

export interface SelectedJob {
    id: number;
    title: string;
    company: string;
    location: string;
}

interface WorkflowContextValue {
    selectedJob: SelectedJob | null;
    learningPlan: LearningResponse | null;
    roadmapProgress: number;
    selectJob: (job: SelectedJob | null) => void;
    setLearningPlan: (plan: LearningResponse | null) => void;
    setRoadmapProgress: (progress: number) => void;
}

const WorkflowContext = createContext<WorkflowContextValue | undefined>(undefined);

function readSelectedJob(): SelectedJob | null {
    try {
        const storedJob = localStorage.getItem(SELECTED_JOB_STORAGE_KEY);
        if (!storedJob) {
            return null;
        }

        const job: unknown = JSON.parse(storedJob);
        if (
            typeof job === "object" &&
            job !== null &&
            "id" in job &&
            "title" in job &&
            "company" in job &&
            "location" in job &&
            typeof job.id === "number" &&
            typeof job.title === "string" &&
            typeof job.company === "string" &&
            typeof job.location === "string"
        ) {
            return job as SelectedJob;
        }
    } catch {
        localStorage.removeItem(SELECTED_JOB_STORAGE_KEY);
    }

    return null;
}

export function WorkflowProvider({ children }: { children: ReactNode }) {
    const [selectedJob, setSelectedJob] = useState<SelectedJob | null>(readSelectedJob);
    const [learningPlan, setLearningPlan] = useState<LearningResponse | null>(null);
    const [roadmapProgress, setRoadmapProgress] = useState(0);

    const selectJob = (job: SelectedJob | null) => {
        setSelectedJob(job);
        setLearningPlan(null);
        setRoadmapProgress(0);

        if (job) {
            localStorage.setItem(SELECTED_JOB_STORAGE_KEY, JSON.stringify(job));
        } else {
            localStorage.removeItem(SELECTED_JOB_STORAGE_KEY);
        }
    };

    const value = useMemo(
        () => ({ selectedJob, learningPlan, roadmapProgress, selectJob, setLearningPlan, setRoadmapProgress }),
        [learningPlan, roadmapProgress, selectedJob],
    );

    return <WorkflowContext.Provider value={value}>{children}</WorkflowContext.Provider>;
}

export function useWorkflow() {
    const context = useContext(WorkflowContext);

    if (!context) {
        throw new Error("useWorkflow must be used within a WorkflowProvider");
    }

    return context;
}
