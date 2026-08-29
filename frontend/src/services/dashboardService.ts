import api from "../api/api";
import type { DashboardData } from "../types/dashboard";

const dashboardService = {
    async getDashboard(): Promise<DashboardData> {
        const response = await api.get("/dashboard");
        return response.data;
    },
};

export default dashboardService;