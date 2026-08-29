import api from "../api/api";

export interface Topic {
  title?: string;
  name?: string;
  description?: string;
}

export type RoadmapTopic = Topic | string;

export interface Resource {
  title: string;
  url: string;
  type: string;
}

export interface Project {
  title?: string;
  name?: string;
  description?: string;
  url?: string;
}

export interface Milestone {
  title: string;
  description: string;
}

export interface Level {
  level?: number;
  title: string;
  xp?: number;
}

export interface RoadmapSkill {
  skill: string;
  skill_key: string;
  category: string;
  description: string;
  difficulty: string;
  priority: number;
  estimated_days: number;
  xp: number;
  topics: RoadmapTopic[];
  dependencies: string[];
  resources: Resource[];
  projects: Project[];
  milestones: Milestone[];
}

export interface RoadmapResponse {
  company: string;
  role: string;
  roadmap_id: string;
  match_percentage: number;
  matched_skills: string[];
  missing_skills: string[];
  total_xp: number;
  current_level: Level;
  estimated_days: number;
  roadmap: RoadmapSkill[];
}

const roadmapService = {
  async generate(data: unknown): Promise<RoadmapResponse> {
    const response = await api.post<RoadmapResponse>("/roadmap/generate", data);
    return response.data;
  },
};

export default roadmapService;
