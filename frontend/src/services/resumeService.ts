import { uploadResume } from "../api/resumeApi";

export async function uploadResumeService(file: File) {
    return await uploadResume(file);
}