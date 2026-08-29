import api from "./api";

export type LearningProgressItem = {
    skill_key: string;
    item_type: "topic" | "project" | "mission";
    item_key: string;
    status: "not_started" | "in_progress" | "completed";
    xp_earned: number;
};

export type LearningProgress = {
    roadmap_id: string;
    items: LearningProgressItem[];
    total_xp: number;
    current_level: { level: number; title: string; xp: number };
    next_level: { level: number; title: string; xp: number } | null;
    gamification: GamificationDashboard;
};

export type GamificationDashboard = {
    total_xp: number;
    current_level: { level: number; title: string; xp: number };
    next_level: { level: number; title: string; xp: number } | null;
    level_progress: number;
    current_streak: number;
    longest_streak: number;
    daily_goal: { target: number; progress: number; completed: boolean };
    weekly_goal: { target: number; progress: number; completed: boolean };
    badges: { key: string; name: string; description: string; unlocked_at: string }[];
    achievements: { key: string; name: string; description: string; unlocked_at: string }[];
};

export const syncLearningProgress = async (roadmap_id: string, roadmap: unknown[]) => {
    const response = await api.post<LearningProgress>("/learning/progress/sync", { roadmap_id, roadmap });
    return response.data;
};

export const getLearningProgress = async (roadmap_id: string) => {
    const response = await api.get<LearningProgress>(`/learning/progress/${roadmap_id}`);
    return response.data;
};

export const updateLearningProgress = async (
    roadmap_id: string,
    item: Omit<LearningProgressItem, "xp_earned">,
) => {
    const response = await api.patch<LearningProgress>(`/learning/progress/${roadmap_id}`, item);
    return response.data;
};

export type LearningResource = { id: number; title: string; description: string; category: string; topic: string; skill: string; resource_type: string; url: string; source: string };
export const getLearningResources = async (skill?: string) => (await api.get<LearningResource[]>("/learning/resources", { params: skill ? { skill } : undefined })).data;
