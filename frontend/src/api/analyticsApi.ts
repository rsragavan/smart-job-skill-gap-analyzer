import api from "./api";

export const getTopSkills = async () => {

    const response = await api.get(
        "/analytics/top-skills"
    );

    return response.data;
};

export const getOverview = async () => {
    const response = await api.get("/analytics/overview");
    return response.data;
};
