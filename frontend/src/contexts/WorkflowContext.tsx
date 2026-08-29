import { createContext, useCallback, useContext, useEffect, useMemo, useState } from "react";
import type { ReactNode } from "react";

import {
    clearActiveTarget as clearActiveTargetApi,
    generateActiveTargetRoadmap,
    getActiveTarget,
    setCustomTarget as setCustomTargetApi,
    setTargetFromJob as setTargetFromJobApi,
} from "../api/targetApi";
import { useAuth } from "./AuthContext";
import type { RoadmapResponse } from "../services/roadmapService";
import type { ActiveTarget, CustomTargetPayload } from "../types/target";
import companyIntelligenceService from "../services/companyIntelligenceService";

/** @deprecated Prefer ActiveTarget — kept for gradual migration of SelectedJob usages */
export interface SelectedJob {
    id: number;
    title: string;
    company: string;
    location: string;
}

const LEARNING_PLAN_STORAGE_KEY = "learning_plan";
const SELECTED_JOB_STORAGE_KEY = "selected_job";

interface WorkflowContextValue {
    activeTarget: ActiveTarget | null;
    selectedJob: SelectedJob | null;
    learningPlan: RoadmapResponse | null;
    roadmapProgress: number;
    targetReady: boolean;
    selectJob: (job: SelectedJob | null) => void;
    setActiveTarget: (target: ActiveTarget | null) => void;
    setLearningPlan: (plan: RoadmapResponse | null) => void;
    setRoadmapProgress: (progress: number) => void;
    selectScrapedTarget: (jobId: number) => Promise<{ target: ActiveTarget; roadmap: RoadmapResponse }>;
    selectCustomTarget: (payload: CustomTargetPayload) => Promise<{ target: ActiveTarget; roadmap: RoadmapResponse }>;
    clearTarget: () => Promise<void>;
    refreshTarget: () => Promise<void>;
    targetIntelligence: any | null;
}

const WorkflowContext = createContext<WorkflowContextValue | undefined>(undefined);

function readLearningPlan(): RoadmapResponse | null {
    try {
        const stored = localStorage.getItem(LEARNING_PLAN_STORAGE_KEY);
        const plan = stored ? JSON.parse(stored) as RoadmapResponse : null;
        if (plan && !plan.roadmap_id) {
            localStorage.removeItem(LEARNING_PLAN_STORAGE_KEY);
            return null;
        }
        return plan;
    } catch {
        localStorage.removeItem(LEARNING_PLAN_STORAGE_KEY);
        return null;
    }
}

function toSelectedJob(target: ActiveTarget | null): SelectedJob | null {
    if (!target || target.job_id == null) return null;
    return {
        id: target.job_id,
        title: target.role_title,
        company: target.company,
        location: target.location || "",
    };
}

export function WorkflowProvider({ children }: { children: ReactNode }) {
    const { user, ready } = useAuth();
    const [activeTarget, setActiveTargetState] = useState<ActiveTarget | null>(null);
    const [learningPlan, setLearningPlanState] = useState<RoadmapResponse | null>(readLearningPlan);
    const [roadmapProgress, setRoadmapProgress] = useState(0);
    const [targetReady, setTargetReady] = useState(false);
    const [targetIntelligence, setTargetIntelligence] = useState<any | null>(null);

    const setLearningPlan = useCallback((plan: RoadmapResponse | null) => {
        setLearningPlanState(plan);
        if (plan) {
            localStorage.setItem(LEARNING_PLAN_STORAGE_KEY, JSON.stringify(plan));
        } else {
            localStorage.removeItem(LEARNING_PLAN_STORAGE_KEY);
        }
    }, []);

    const setActiveTarget = useCallback((target: ActiveTarget | null) => {
        setActiveTargetState(target);
        if (target?.job_id != null) {
            localStorage.setItem(
                SELECTED_JOB_STORAGE_KEY,
                JSON.stringify(toSelectedJob(target)),
            );
        } else {
            localStorage.removeItem(SELECTED_JOB_STORAGE_KEY);
        }
    }, []);

    const refreshTarget = useCallback(async () => {
        if (!user) {
            setActiveTarget(null);
            setTargetReady(true);
            return;
        }
        try {
            const target = await getActiveTarget();
            setActiveTarget(target);
            if (target?.roadmap_id && learningPlan && learningPlan.roadmap_id !== target.roadmap_id) {
                setLearningPlan(null);
                setRoadmapProgress(0);
            }
        } catch {
            setActiveTarget(null);
        } finally {
            setTargetReady(true);
        }
    }, [user, setActiveTarget, setLearningPlan, learningPlan]);

    useEffect(() => {
        if (!ready) return;
        setTargetReady(false);
        void refreshTarget();
    }, [ready, user?.id, refreshTarget]);

    useEffect(() => {
        if (!activeTarget) { setTargetIntelligence(null); return; }
        void companyIntelligenceService.activeTargetIntelligence()
            .then(setTargetIntelligence)
            .catch(() => setTargetIntelligence(null));
    }, [activeTarget?.id]);

    const selectScrapedTarget = useCallback(async (jobId: number) => {
        const target = await setTargetFromJobApi(jobId);
        const roadmap = await generateActiveTargetRoadmap();
        setActiveTarget({ ...target, roadmap_id: roadmap.roadmap_id });
        setLearningPlan(roadmap);
        setRoadmapProgress(0);
        return { target, roadmap };
    }, [setActiveTarget, setLearningPlan]);

    const selectCustomTarget = useCallback(async (payload: CustomTargetPayload) => {
        const target = await setCustomTargetApi(payload);
        const roadmap = await generateActiveTargetRoadmap();
        setActiveTarget({ ...target, roadmap_id: roadmap.roadmap_id });
        setLearningPlan(roadmap);
        setRoadmapProgress(0);
        return { target, roadmap };
    }, [setActiveTarget, setLearningPlan]);

    const clearTarget = useCallback(async () => {
        await clearActiveTargetApi();
        setActiveTarget(null);
        setTargetIntelligence(null);
        setLearningPlan(null);
        setRoadmapProgress(0);
    }, [setActiveTarget, setLearningPlan]);

    const selectJob = useCallback((job: SelectedJob | null) => {
        if (!job) {
            setActiveTarget(null);
            setLearningPlan(null);
            setRoadmapProgress(0);
            localStorage.removeItem(SELECTED_JOB_STORAGE_KEY);
            return;
        }
        localStorage.setItem(SELECTED_JOB_STORAGE_KEY, JSON.stringify(job));
        setLearningPlan(null);
        setRoadmapProgress(0);
    }, [setActiveTarget, setLearningPlan]);

    const value = useMemo(
        () => ({
            activeTarget,
            selectedJob: toSelectedJob(activeTarget),
            learningPlan,
            roadmapProgress,
            targetReady,
            selectJob,
            setActiveTarget,
            setLearningPlan,
            setRoadmapProgress,
            selectScrapedTarget,
            selectCustomTarget,
            clearTarget,
            refreshTarget,
            targetIntelligence,
        }),
        [
            activeTarget,
            learningPlan,
            roadmapProgress,
            targetReady,
            selectJob,
            setActiveTarget,
            setLearningPlan,
            selectScrapedTarget,
            selectCustomTarget,
            clearTarget,
            refreshTarget,
            targetIntelligence,
        ],
    );

    return (
        <WorkflowContext.Provider value={value}>
            {children}
        </WorkflowContext.Provider>
    );
}

export function useWorkflow() {
    const context = useContext(WorkflowContext);
    if (!context) {
        throw new Error("useWorkflow must be used within WorkflowProvider");
    }
    return context;
}
