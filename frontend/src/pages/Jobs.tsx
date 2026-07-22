import { useCallback, useEffect, useMemo, useState } from "react";
import {
    Alert, Box, FormControl, Grid, InputLabel, MenuItem, Pagination,
    Select, Skeleton, Stack, TextField, Typography, Button,
} from "@mui/material";
import { generateRoadmap } from "../api/learningApi";
import JobCard from "../components/JobCard";
import { useAuth } from "../contexts/AuthContext";
import { useWorkflow } from "../contexts/WorkflowContext";
import { fetchJobs } from "../services/jobService";
import type { Job, JobsResponse } from "../types/job";

type Filters = {
    keyword: string; company: string; location: string;
    employment_type: string; required_skills: string;
    status: "ACTIVE" | "INACTIVE" | "ALL"; sort: "newest" | "match" | "company" | "title";
};

export default function Jobs() {
    const { user } = useAuth();
    const { selectedJob, selectJob, setLearningPlan } = useWorkflow();
    const [filters, setFilters] = useState<Filters>({ keyword: "", company: "", location: "", employment_type: "", required_skills: "", status: "ACTIVE", sort: "newest" });
    const [response, setResponse] = useState<JobsResponse | null>(null);
    const [matchRange, setMatchRange] = useState("all");
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [page, setPage] = useState(1);

    const loadJobs = useCallback(async () => {
        setLoading(true); setError(null);
        try { setResponse(await fetchJobs({ ...filters, page })); }
        catch (err: unknown) { setError(err instanceof Error ? err.message : "Failed to load jobs"); setResponse(null); }
        finally { setLoading(false); }
    }, [filters, page]);

    useEffect(() => { const timer = window.setTimeout(() => void loadJobs(), 250); return () => window.clearTimeout(timer); }, [loadJobs]);
    useEffect(() => { setPage(1); }, [filters]);

    const visibleJobs = useMemo(() => {
        const bounds: Record<string, [number, number]> = { "90-100": [90, 100], "75-89": [75, 89], "50-74": [50, 74], below50: [0, 49] };
        const jobs = response?.jobs ?? [];
        const filtered = matchRange === "all" ? jobs : jobs.filter(job => { const [min, max] = bounds[matchRange]; return job.match_percentage >= min && job.match_percentage <= max; });
        if (filters.sort === "match") filtered.sort((a, b) => b.match_percentage - a.match_percentage);
        return filtered;
    }, [response, matchRange, filters.sort]);

    const setFilter = (key: keyof Filters, value: string) => setFilters(current => ({ ...current, [key]: value } as Filters));
    const handleSelectJob = useCallback(async (job: Job) => {
        selectJob({ id: job.id, title: job.title, company: job.company, location: job.location });
        try { setLearningPlan(await generateRoadmap(job.id)); }
        catch (err: unknown) { setError(err instanceof Error ? err.message : "Failed to calculate the skill gap"); }
    }, [selectJob, setLearningPlan]);

    return <Stack spacing={3}>
        <Typography variant="h4">Jobs</Typography>
        <Stack spacing={2} sx={{ p: 2, border: "1px solid", borderColor: "divider", borderRadius: 2, bgcolor: "background.paper" }}>
            <TextField fullWidth label="Search jobs" placeholder="Title, company, location, skill, or employment type" value={filters.keyword} onChange={e => setFilter("keyword", e.target.value)} slotProps={{ htmlInput: { "aria-label": "Search jobs" } }} />
            <Grid container spacing={1}>
                {(["company", "location", "employment_type", "required_skills"] as const).map(key => <Grid key={key} size={{ xs: 12, sm: 6, md: 3 }}><TextField fullWidth size="small" label={key === "required_skills" ? "Required skills" : key.replace("_", " ")} placeholder={key === "required_skills" ? "e.g. Python, React" : undefined} value={filters[key]} onChange={e => setFilter(key, e.target.value)} /></Grid>)}
                <Grid size={{ xs: 12, sm: 6, md: 3 }}><FormControl fullWidth size="small"><InputLabel>Sort by</InputLabel><Select label="Sort by" value={filters.sort} onChange={e => setFilter("sort", e.target.value)}><MenuItem value="newest">Newest jobs</MenuItem><MenuItem value="match">Highest match</MenuItem><MenuItem value="company">Company A-Z</MenuItem><MenuItem value="title">Job title A-Z</MenuItem></Select></FormControl></Grid>
                <Grid size={{ xs: 12, sm: 6, md: 3 }}><FormControl fullWidth size="small"><InputLabel>Match</InputLabel><Select label="Match" value={matchRange} onChange={e => setMatchRange(e.target.value)}><MenuItem value="all">All matches</MenuItem><MenuItem value="90-100">90–100%</MenuItem><MenuItem value="75-89">75–89%</MenuItem><MenuItem value="50-74">50–74%</MenuItem><MenuItem value="below50">Below 50%</MenuItem></Select></FormControl></Grid>
                {user?.role === "admin" && <Grid size={{ xs: 12, sm: 6, md: 3 }}><FormControl fullWidth size="small"><InputLabel>Status</InputLabel><Select label="Status" value={filters.status} onChange={e => setFilter("status", e.target.value)}><MenuItem value="ACTIVE">Active</MenuItem><MenuItem value="INACTIVE">Inactive</MenuItem><MenuItem value="ALL">All jobs</MenuItem></Select></FormControl></Grid>}
            </Grid>
            {!loading && <Typography variant="caption" color="text.secondary">Showing {visibleJobs.length} of {response?.total_count ?? 0} jobs</Typography>}
        </Stack>
        {error && <Alert severity="error" action={<Button color="inherit" size="small" onClick={() => void loadJobs()}>Retry</Button>}>{error}</Alert>}
        {loading && <Grid container spacing={2}>{Array.from({ length: 6 }, (_, index) => <Grid key={index} size={{ xs: 12, sm: 6, lg: 4 }}><Skeleton variant="rounded" height={360} /></Grid>)}</Grid>}
        {!loading && visibleJobs.length === 0 && <Box sx={{ textAlign: "center", py: 6 }}><Typography variant="h6" color="text.secondary">No jobs found</Typography><Typography variant="body2" color="text.secondary">Try adjusting your search or filters.</Typography></Box>}
        {!loading && visibleJobs.length > 0 && <><Grid container spacing={2}>{visibleJobs.map(job => <Grid key={job.id} size={{ xs: 12, sm: 6, lg: 4 }}><JobCard job={job} isSelected={selectedJob?.id === job.id} onSelect={handleSelectJob} /></Grid>)}</Grid><Box sx={{ display: "flex", justifyContent: "center" }}><Pagination count={Math.max(1, response?.total_pages ?? 1)} page={page} onChange={(_, value) => setPage(value)} /></Box></>}
    </Stack>;
}
