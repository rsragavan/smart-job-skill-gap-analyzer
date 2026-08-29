import { useCallback, useEffect, useMemo, useState } from "react";
import {
    Alert, Box, Button, Chip, FormControl, Grid, InputLabel, MenuItem, Pagination,
    Select, Skeleton, Stack, Tab, Tabs, TextField, Typography,
} from "@mui/material";
import { useNavigate } from "react-router-dom";
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

type Mode = "scraped" | "custom";

export default function Jobs() {
    const { user } = useAuth();
    const navigate = useNavigate();
    const { activeTarget, selectScrapedTarget, selectCustomTarget, clearTarget } = useWorkflow();
    const [mode, setMode] = useState<Mode>("scraped");
    const [filters, setFilters] = useState<Filters>({ keyword: "", company: "", location: "", employment_type: "", required_skills: "", status: "ACTIVE", sort: "newest" });
    const [response, setResponse] = useState<JobsResponse | null>(null);
    const [matchRange, setMatchRange] = useState("all");
    const [loading, setLoading] = useState(true);
    const [submitting, setSubmitting] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [page, setPage] = useState(1);
    const [customCompany, setCustomCompany] = useState("");
    const [customRole, setCustomRole] = useState("");
    const [customLocation, setCustomLocation] = useState("");
    const [customJd, setCustomJd] = useState("");

    const loadJobs = useCallback(async () => {
        setLoading(true); setError(null);
        try { setResponse(await fetchJobs({ ...filters, page })); }
        catch (err: unknown) { setError(err instanceof Error ? err.message : "Failed to load jobs"); setResponse(null); }
        finally { setLoading(false); }
    }, [filters, page]);

    useEffect(() => {
        if (mode !== "scraped") return;
        const timer = window.setTimeout(() => void loadJobs(), 250);
        return () => window.clearTimeout(timer);
    }, [loadJobs, mode]);
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
        if (submitting) return;
        setSubmitting(true);
        setError(null);
        try {
            const { roadmap } = await selectScrapedTarget(job.id);
            navigate("/roadmap", { state: roadmap });
        } catch (err: unknown) {
            setError(err instanceof Error ? err.message : "Failed to set target and generate roadmap");
        } finally {
            setSubmitting(false);
        }
    }, [selectScrapedTarget, navigate, submitting]);

    const handleCustomSubmit = useCallback(async () => {
        if (!customCompany.trim() || !customRole.trim() || customJd.trim().length < 20) {
            setError("Company, role, and a job description (at least 20 characters) are required.");
            return;
        }
        setSubmitting(true);
        setError(null);
        try {
            const { roadmap } = await selectCustomTarget({
                company: customCompany.trim(),
                role: customRole.trim(),
                job_description: customJd.trim(),
                location: customLocation.trim() || undefined,
            });
            navigate("/roadmap", { state: roadmap });
        } catch (err: unknown) {
            setError(err instanceof Error ? err.message : "Failed to create custom target");
        } finally {
            setSubmitting(false);
        }
    }, [customCompany, customRole, customJd, customLocation, selectCustomTarget, navigate]);

    return (
        <Stack spacing={3}>
            <Box>
                <Typography variant="h4" sx={{ fontWeight: 700 }}>Choose Target</Typography>
                <Typography color="text.secondary">
                    Select a scraped company job or paste any company&apos;s job description. Every feature uses this target.
                </Typography>
            </Box>

            {activeTarget && (
                <Alert
                    severity="info"
                    action={
                        <Button color="inherit" size="small" onClick={() => void clearTarget()}>
                            Clear
                        </Button>
                    }
                >
                    Active target: <strong>{activeTarget.company}</strong> · {activeTarget.role_title}{" "}
                    <Chip
                        size="small"
                        sx={{ ml: 1 }}
                        label={activeTarget.source_type === "scraped" ? "Scraped Target Job" : "User-provided Target Job"}
                    />
                    {" · "}{activeTarget.match_percentage}% match
                </Alert>
            )}

            <Tabs value={mode} onChange={(_, value: Mode) => setMode(value)} aria-label="Target selection mode">
                <Tab value="scraped" label="Scraped Target Job" />
                <Tab value="custom" label="User-provided Target Job" />
            </Tabs>

            {error && (
                <Alert severity="error" action={<Button color="inherit" size="small" onClick={() => setError(null)}>Dismiss</Button>}>
                    {error}
                </Alert>
            )}

            {mode === "scraped" && (
                <>
                    <Stack spacing={2} sx={{ p: 2, border: "1px solid", borderColor: "divider", borderRadius: 2, bgcolor: "background.paper" }}>
                        <TextField fullWidth label="Search jobs" placeholder="Title, company, location, skill, or employment type" value={filters.keyword} onChange={e => setFilter("keyword", e.target.value)} slotProps={{ htmlInput: { "aria-label": "Search jobs" } }} />
                        <Grid container spacing={1}>
                            {(["company", "location", "employment_type", "required_skills"] as const).map(key => (
                                <Grid key={key} size={{ xs: 12, sm: 6, md: 3 }}>
                                    <TextField fullWidth size="small" label={key === "required_skills" ? "Required skills" : key.replace("_", " ")} placeholder={key === "required_skills" ? "e.g. Python, React" : undefined} value={filters[key]} onChange={e => setFilter(key, e.target.value)} />
                                </Grid>
                            ))}
                            <Grid size={{ xs: 12, sm: 6, md: 3 }}>
                                <FormControl fullWidth size="small">
                                    <InputLabel>Sort by</InputLabel>
                                    <Select label="Sort by" value={filters.sort} onChange={e => setFilter("sort", e.target.value)}>
                                        <MenuItem value="newest">Newest jobs</MenuItem>
                                        <MenuItem value="match">Highest match</MenuItem>
                                        <MenuItem value="company">Company A-Z</MenuItem>
                                        <MenuItem value="title">Job title A-Z</MenuItem>
                                    </Select>
                                </FormControl>
                            </Grid>
                            <Grid size={{ xs: 12, sm: 6, md: 3 }}>
                                <FormControl fullWidth size="small">
                                    <InputLabel>Match</InputLabel>
                                    <Select label="Match" value={matchRange} onChange={e => setMatchRange(e.target.value)}>
                                        <MenuItem value="all">All matches</MenuItem>
                                        <MenuItem value="90-100">90–100%</MenuItem>
                                        <MenuItem value="75-89">75–89%</MenuItem>
                                        <MenuItem value="50-74">50–74%</MenuItem>
                                        <MenuItem value="below50">Below 50%</MenuItem>
                                    </Select>
                                </FormControl>
                            </Grid>
                            {user?.role === "admin" && (
                                <Grid size={{ xs: 12, sm: 6, md: 3 }}>
                                    <FormControl fullWidth size="small">
                                        <InputLabel>Status</InputLabel>
                                        <Select label="Status" value={filters.status} onChange={e => setFilter("status", e.target.value)}>
                                            <MenuItem value="ACTIVE">Active</MenuItem>
                                            <MenuItem value="INACTIVE">Inactive</MenuItem>
                                            <MenuItem value="ALL">All jobs</MenuItem>
                                        </Select>
                                    </FormControl>
                                </Grid>
                            )}
                        </Grid>
                        {!loading && <Typography variant="caption" color="text.secondary">Showing {visibleJobs.length} of {response?.total_count ?? 0} jobs</Typography>}
                    </Stack>
                    {loading && <Grid container spacing={2}>{Array.from({ length: 6 }, (_, index) => <Grid key={index} size={{ xs: 12, sm: 6, lg: 4 }}><Skeleton variant="rounded" height={360} /></Grid>)}</Grid>}
                    {!loading && visibleJobs.length === 0 && (
                        <Box sx={{ textAlign: "center", py: 6 }}>
                            <Typography variant="h6" color="text.secondary">No jobs found</Typography>
                            <Typography variant="body2" color="text.secondary">Try adjusting filters, or create a user-provided Target Job.</Typography>
                        </Box>
                    )}
                    {!loading && visibleJobs.length > 0 && (
                        <>
                            <Grid container spacing={2}>
                                {visibleJobs.map(job => (
                                    <Grid key={job.id} size={{ xs: 12, sm: 6, lg: 4 }}>
                                        <JobCard
                                            job={job}
                                            isSelected={activeTarget?.job_id === job.id}
                                            onSelect={handleSelectJob}
                                        />
                                    </Grid>
                                ))}
                            </Grid>
                            <Box sx={{ display: "flex", justifyContent: "center" }}>
                                <Pagination count={Math.max(1, response?.total_pages ?? 1)} page={page} onChange={(_, value) => setPage(value)} />
                            </Box>
                        </>
                    )}
                </>
            )}

            {mode === "custom" && (
                <Stack spacing={2} sx={{ p: 2, border: "1px solid", borderColor: "divider", borderRadius: 2, bgcolor: "background.paper", maxWidth: 800 }}>
                    <Typography variant="h6">Create a Target Job from a Job Description</Typography>
                    <Typography variant="body2" color="text.secondary">
                        Paste a job description from Zoho, Microsoft, TCS, or any startup. The same skill-gap, roadmap, learning, and Career GPS pipeline runs.
                    </Typography>
                    <TextField
                        label="Company"
                        required
                        value={customCompany}
                        onChange={(e) => setCustomCompany(e.target.value)}
                        placeholder="e.g. Zoho"
                        fullWidth
                    />
                    <TextField
                        label="Role"
                        required
                        value={customRole}
                        onChange={(e) => setCustomRole(e.target.value)}
                        placeholder="e.g. Software Developer"
                        fullWidth
                    />
                    <TextField
                        label="Location (optional)"
                        value={customLocation}
                        onChange={(e) => setCustomLocation(e.target.value)}
                        fullWidth
                    />
                    <TextField
                        label="Job Description"
                        required
                        value={customJd}
                        onChange={(e) => setCustomJd(e.target.value)}
                        placeholder="Paste the complete job description here..."
                        fullWidth
                        multiline
                        minRows={10}
                        helperText={`${customJd.trim().length} characters (minimum 20)`}
                    />
                    <Box>
                        <Button variant="contained" disabled={submitting} onClick={() => void handleCustomSubmit()}>
                            {submitting ? "Generating…" : "Generate Analysis & Roadmap"}
                        </Button>
                    </Box>
                </Stack>
            )}
        </Stack>
    );
}
