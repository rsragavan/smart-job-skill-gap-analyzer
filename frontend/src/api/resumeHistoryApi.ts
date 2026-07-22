import api from "./api";

export const getResumeHistory = async () => {
    const response = await api.get("/resume/history");
    return response.data;
};

export const deleteResumeHistory = async (id: number) => {
    const response = await api.delete(`/resume/history/${id}`);
    return response.data;
};

