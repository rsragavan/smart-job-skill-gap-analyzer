import { getJobs, type JobsSearchParams } from "../api/jobsApi";

export async function fetchJobs(params: JobsSearchParams = {}) {
    return await getJobs(params);
}