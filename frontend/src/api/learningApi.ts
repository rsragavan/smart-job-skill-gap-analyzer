import api from "./api";

export const generateRoadmap = async (jobId: number) => {

    const response = await api.post(
        `/learning/job/${jobId}`
    );

    return response.data;
};