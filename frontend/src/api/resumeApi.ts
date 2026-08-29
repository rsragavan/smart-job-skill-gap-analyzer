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

export async function downloadATSReport(historyId: number, reportType = "ats") {
    const response = await api.get(`/resume/ats-report/${historyId}/export`, { params: { report_type: reportType }, responseType: "blob" });
    const url = URL.createObjectURL(response.data);
    const anchor = document.createElement("a"); anchor.href = url; anchor.download = `${reportType}-${historyId}.pdf`; anchor.click(); URL.revokeObjectURL(url);
}
