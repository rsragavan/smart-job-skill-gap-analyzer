import api from "./api";
import type { ResumeResponse } from "../types/resume";

export async function uploadResume(
    file: File
): Promise<ResumeResponse> {

    const formData = new FormData();

    formData.append("file", file);

    const response = await api.post<ResumeResponse>(
        "/resume/upload",
        formData,
        {
            headers: {
                "Content-Type": "multipart/form-data",
            },
        }
    );

    return response.data;
}