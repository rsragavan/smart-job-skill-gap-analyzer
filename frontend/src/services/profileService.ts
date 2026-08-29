import api from "../api/api";
import type { Profile } from "../types/profile";

const profileService = {
    async getProfile(): Promise<Profile> {
        const response = await api.get("/users/me/profile");
        return response.data;
    },
};

export default profileService;
