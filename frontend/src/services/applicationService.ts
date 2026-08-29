import api from "../api/api";

const applicationService = {
  async getApplications() {
    const response = await api.get("/applications");
    return response.data;
  },

  async applyForJob(jobId: number, notes?: string) {
    const response = await api.post("/applications", {
      job_id: jobId,
      notes,
    });

    return response.data;
  },

  async updateApplication(
    id: number,
    status?: string,
    notes?: string
  ) {
    const response = await api.patch(`/applications/${id}`, {
      status,
      notes,
    });

    return response.data;
  },

  async deleteApplication(id: number) {
    const response = await api.delete(`/applications/${id}`);
    return response.data;
  },

  async createCustomApplication(data: { company_name: string; job_title: string; location?: string; job_url?: string; notes?: string; status?: string }) {
    return (await api.post("/applications/custom", data)).data;
  },

  async getDashboardStats() {
    const response = await api.get("/applications/dashboard");
    return response.data;
  },
};

export default applicationService;
