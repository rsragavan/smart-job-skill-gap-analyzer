import api from "../api/api";

export type CompanyRole = { id: number; title: string; description?: string | null; is_open?: boolean; required_skills?: string | null };
export type SelectionRound = { id: number; round_number: number; title: string; description?: string | null; purpose?: string | null };
export type Company = { id: number; name: string; logo_url?: string | null; industry?: string | null; headquarters?: string | null; country?: string | null; hiring_status?: string | null; internship_available: boolean; freshers_hiring: boolean; description?: string | null; tech_stack?: string | null; products?: string | null; culture_summary?: string | null; website_url?: string | null; career_url?: string | null; open_roles?: number | null; verification_status: string; verified: boolean; data_source_url?: string | null; last_verified_at?: string | null };
export type CompanyDetail = Company & { founded_year?: number | null; company_size?: string | null; public_email?: string | null; linkedin_url?: string | null; office_locations?: string | null; remote_policy?: string | null; skills: Array<{ skill: string; importance: string }>; roles: CompanyRole[]; locations: Array<{ city: string; state?: string | null; country: string }>; insights?: Record<string, unknown> | null };
export type RoleProcess = CompanyRole & { selection_process: SelectionRound[]; questions: Array<{ category: string; question: string; difficulty?: string | null; preparation_tip?: string | null }>; resources: Array<{ title: string; url: string; resource_type: string }> };
export type TargetCompany = { id: number; name: string; roles: Array<{ id: number; title: string }> };
export type TargetPreparation = { company: string; company_info: { name: string; location?: string | null; industry?: string | null; company_type?: string | null; verified: boolean }; role: string; experience_level: string; target_id: number; job_description_source: string; resume_skills: string[]; required_skills: string[]; coding_topics: string[]; notice: string; data_status: string; readiness: { overall: number; provisional: boolean; matched_skills: string[]; missing_skills: string[]; components: Record<string, number> }; rounds: Array<{ round_number: number; round_name: string; purpose?: string | null; topics: string[]; preparation_tasks: string[]; source_type: string }>; questions: Array<{ question: string; category: string; difficulty: string; source_type: string }> };
export type StartupRole = { id: number; startup_id: number; title: string; is_open: boolean };
export type Startup = { id: number; name: string; industry: string; location: string; state?: string | null; country?: string | null; funding_stage?: string | null; latest_funding_amount?: string | null; founded_year?: number | null; employees?: string | null; website_url?: string | null; careers_url?: string | null; public_email?: string | null; hiring_status?: string | null; open_positions?: number | null; open_roles?: number | null; tech_stack?: string | null; description?: string | null; founders?: string | null; investors?: string | null; products?: string | null; culture_summary?: string | null; preparation_tips?: string | null; verification_status: string; verified: boolean; source_url?: string | null; source_name?: string | null; last_verified_at?: string | null; last_updated: string; roles?: StartupRole[] };

const companyIntelligenceService = {
  async companies(params: Record<string, string | boolean | undefined> = {}) { return (await api.get<Company[]>("/company-intelligence/companies", { params })).data; },
  async company(id: number) { return (await api.get<CompanyDetail>(`/company-intelligence/companies/${id}`)).data; },
  async role(companyId: number, roleId: number) { return (await api.get<RoleProcess>(`/company-intelligence/companies/${companyId}/roles/${roleId}`)).data; },
  async targetIntelligence(target: { company_id?: number | null; company_role_id?: number | null; company: string; role_title: string }) { return (await api.get("/company-intelligence/target-intelligence", { params: { company_id: target.company_id || undefined, role_id: target.company_role_id || undefined, company: target.company, role: target.role_title } })).data; },
  async activeTargetIntelligence() { return (await api.get("/targets/active/intelligence")).data; },
  async activeTargetPreparation() { return (await api.get<TargetPreparation>("/targets/active/preparation")).data; },
  async targetCompanies(search = "") { return (await api.get<TargetCompany[]>("/company-intelligence/target-companies", { params: search ? { search } : undefined })).data; },
  async analyzeTargetCompany(payload: { company: string; role: string; experience_level: string; job_description?: string }) { return (await api.post<TargetPreparation>("/company-intelligence/target-company", payload)).data; },
  async roles(companyId: number) { return (await api.get<CompanyRole[]>(`/companies/${companyId}/roles`)).data; },
  async startups(params: Record<string, string | undefined> = {}) { return (await api.get<Startup[]>("/company-intelligence/startups", { params })).data; },
  async startup(id: number) { return (await api.get<Startup>(`/startups/${id}`)).data; },
  async startupRoles(id: number) { return (await api.get<StartupRole[]>(`/startups/${id}/roles`)).data; },
};
export default companyIntelligenceService;
