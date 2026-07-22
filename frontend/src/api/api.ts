import axios from "axios";

const api = axios.create({
    // Keep local development working even before a frontend .env file exists.
    baseURL: import.meta.env.VITE_API_URL || "http://127.0.0.1:8000",
    withCredentials: true,
    headers: {
        "Content-Type": "application/json",
    },
});

let refreshing: Promise<string> | null = null;
api.interceptors.response.use((response) => response, async (error) => {
    const request = error.config as { _retry?: boolean; headers?: Record<string, string>; url?: string } | undefined;
    if (error.response?.status !== 401 || !request || request._retry || request.url?.includes("/auth/")) return Promise.reject(error);
    request._retry = true;
    try {
        if (!refreshing) {
            const raw = localStorage.getItem("auth");
            const refreshToken = raw ? (JSON.parse(raw) as { refresh_token: string }).refresh_token : "";
            refreshing = api.post<{ access_token: string; refresh_token: string; user: unknown }>("/auth/refresh", { refresh_token: refreshToken }).then(({ data }) => {
                localStorage.setItem("auth", JSON.stringify(data));
                api.defaults.headers.common.Authorization = `Bearer ${data.access_token}`;
                return data.access_token;
            }).finally(() => { refreshing = null; });
        }
        const accessToken = await refreshing;
        request.headers = { ...request.headers, Authorization: `Bearer ${accessToken}` };
        return api(request);
    } catch {
        localStorage.removeItem("auth");
        window.dispatchEvent(new Event("auth:expired"));
        return Promise.reject(error);
    }
});

export default api;
