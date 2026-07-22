import { lazy, memo, Suspense, useCallback, useEffect, useMemo, useState } from "react";
import type { ReactNode } from "react";
import { useNavigate } from "react-router-dom";
import {
    Alert, Box, Button, Card, CardContent, Grid, MenuItem, Skeleton, Stack, TextField, Tooltip, Typography,
} from "@mui/material";
import AssessmentOutlinedIcon from "@mui/icons-material/AssessmentOutlined";
import BusinessOutlinedIcon from "@mui/icons-material/BusinessOutlined";
import CheckCircleOutlineIcon from "@mui/icons-material/CheckCircleOutlined";
import DownloadOutlinedIcon from "@mui/icons-material/DownloadOutlined";
import PsychologyOutlinedIcon from "@mui/icons-material/PsychologyOutlined";
import RefreshOutlinedIcon from "@mui/icons-material/RefreshOutlined";
import SchoolOutlinedIcon from "@mui/icons-material/SchoolOutlined";
import TrendingDownOutlinedIcon from "@mui/icons-material/TrendingDownOutlined";
import TrendingUpOutlinedIcon from "@mui/icons-material/TrendingUpOutlined";
import UploadFileOutlinedIcon from "@mui/icons-material/UploadFileOutlined";
import WorkOutlineIcon from "@mui/icons-material/WorkOutlined";

import { getOverview } from "../api/analyticsApi";
import { useWorkflow } from "../contexts/WorkflowContext";

const AnalyticsCharts = lazy(() => import("../components/AnalyticsCharts"));

interface AnalyticsData {
    top_skills?: Record<string, number>;
    top_companies?: Record<string, number>;
    jobs_per_company?: Record<string, Array<{ id: number; title: string }>>;
    average_match_percentage?: number;
}

type TimeRange = "all" | "last" | "current";
type SortOption = "highest" | "lowest" | "newest" | "oldest";

export default function Analytics() {
    const navigate = useNavigate();
    const { learningPlan, roadmapProgress, selectedJob } = useWorkflow();
    const [data, setData] = useState<AnalyticsData | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [timeRange, setTimeRange] = useState<TimeRange>("all");
    const [sort, setSort] = useState<SortOption>("highest");

    const loadAnalytics = useCallback(async () => {
        setLoading(true);
        setError(null);
        try {
            setData(await getOverview());
        } catch (err: unknown) {
            setData(null);
            setError(err instanceof Error ? err.message : "We could not load analytics right now.");
        } finally {
            setLoading(false);
        }
    }, []);

    useEffect(() => {
        const loadTimer = window.setTimeout(() => { void loadAnalytics(); }, 0);
        return () => window.clearTimeout(loadTimer);
    }, [loadAnalytics]);

    const analytics = useMemo(() => {
        const skills = Object.entries(data?.top_skills ?? {}).map(([name, count]) => ({ name, count }));
        const companies = Object.entries(data?.top_companies ?? {}).map(([name, count]) => ({ name, count }));
        const companyJobs = Object.entries(data?.jobs_per_company ?? {}).map(([name, jobs]) => ({ name, count: jobs.length }));
        const totalJobs = companyJobs.reduce((total, company) => total + company.count, 0);
        const totalExtractedSkills = skills.reduce((total, skill) => total + skill.count, 0);
        const descending = sort !== "lowest";
        const byCount = (first: { count: number }, second: { count: number }) => descending ? second.count - first.count : first.count - second.count;

        return {
            skills: [...skills].sort(byCount),
            companies: [...companies].sort(byCount),
            companyJobs,
            totalJobs,
            totalCompanies: companyJobs.length,
            totalExtractedSkills,
            averageMatch: data?.average_match_percentage ?? 0,
        };
    }, [data, sort]);

    const hasAnalytics = Boolean(data && (analytics.totalJobs > 0 || analytics.skills.length > 0 || analytics.companies.length > 0));
    const completedRoadmaps = learningPlan && roadmapProgress >= 100 ? 1 : 0;
    const totalMissingSkills = learningPlan?.total_missing_skills;
    const filterNote = timeRange === "all" ? null : "The analytics endpoint provides an all-time overview only; this view remains based on the available overview data.";

    const exportCsv = useCallback(() => {
        if (!data) return;
        const rows = [
            ["Metric", "Value"],
            ["Total jobs", String(analytics.totalJobs)],
            ["Total companies", String(analytics.totalCompanies)],
            ["Total extracted skills (top skills)", String(analytics.totalExtractedSkills)],
            ["Average resume match percentage", String(analytics.averageMatch)],
            [],
            ["Top required skill", "Frequency"],
            ...analytics.skills.map((skill) => [skill.name, String(skill.count)]),
            [],
            ["Top company", "Job count"],
            ...analytics.companies.map((company) => [company.name, String(company.count)]),
        ];
        const csv = rows.map((row) => row.map((value) => `"${value.replaceAll("\"", "\"\"")}"`).join(",")).join("\n");
        const url = URL.createObjectURL(new Blob([csv], { type: "text/csv;charset=utf-8" }));
        const anchor = document.createElement("a");
        anchor.href = url;
        anchor.download = "skill-gap-analytics.csv";
        anchor.click();
        URL.revokeObjectURL(url);
    }, [analytics, data]);

    return <Stack spacing={3}>
        <Stack direction={{ xs: "column", sm: "row" }} spacing={2} sx={{ justifyContent: "space-between", alignItems: { sm: "center" } }}>
            <Box><Typography variant="h4" sx={{ fontWeight: 700 }}>Analytics Dashboard</Typography><Typography color="text.secondary" sx={{ mt: 0.5 }}>Insights from uploaded resumes and job market analysis.</Typography></Box>
            <Button variant="outlined" startIcon={<RefreshOutlinedIcon />} onClick={() => void loadAnalytics()} disabled={loading}>Refresh</Button>
        </Stack>

        <Grid container spacing={2}>
            <KpiCard icon={<WorkOutlineIcon />} title="Total Jobs" value={analytics.totalJobs} description="Jobs currently included in analysis" trend="Available job records" loading={loading} />
            <KpiCard icon={<BusinessOutlinedIcon />} title="Total Companies" value={analytics.totalCompanies} description="Companies represented in job data" trend="Company coverage" loading={loading} />
            <KpiCard icon={<PsychologyOutlinedIcon />} title="Total Skills Extracted" value={analytics.totalExtractedSkills} description="Frequency across reported top skills" trend="Top skills dataset" loading={loading} />
            <KpiCard icon={<AssessmentOutlinedIcon />} title="Average Resume Match %" value={`${analytics.averageMatch}%`} description="Latest resume against available jobs" trend="Latest resume analysis" loading={loading} />
            <KpiCard icon={<WorkOutlineIcon />} title="Selected Job" value={selectedJob?.title ?? "None"} description={selectedJob ? selectedJob.company : "Choose a job to begin a roadmap"} trend={selectedJob ? "Current workflow" : "No job selected"} loading={loading} textValue />
            <KpiCard icon={<CheckCircleOutlineIcon />} title="Completed Roadmaps" value={completedRoadmaps} description="Completed in the current session" trend={learningPlan ? `${roadmapProgress}% current progress` : "No active roadmap"} loading={loading} />
        </Grid>

        <Card elevation={0} sx={panelSx}><CardContent><Stack direction={{ xs: "column", md: "row" }} spacing={1.5}><TextField select size="small" label="Time Range" value={timeRange} onChange={(event) => setTimeRange(event.target.value as TimeRange)} sx={{ minWidth: { md: 180 } }}><MenuItem value="all">All Time</MenuItem><MenuItem value="last">Last Upload</MenuItem><MenuItem value="current">Current Resume</MenuItem></TextField><TextField select size="small" label="Sort" value={sort} onChange={(event) => setSort(event.target.value as SortOption)} sx={{ minWidth: { md: 180 } }}><MenuItem value="highest">Highest Match</MenuItem><MenuItem value="lowest">Lowest Match</MenuItem><MenuItem value="newest">Newest</MenuItem><MenuItem value="oldest">Oldest</MenuItem></TextField></Stack>{filterNote && <Typography variant="caption" color="text.secondary" sx={{ display: "block", mt: 1 }}>{filterNote}</Typography>}</CardContent></Card>

        {error && <Alert severity="error" action={<Button color="inherit" size="small" onClick={() => void loadAnalytics()}>Retry</Button>}>{error}</Alert>}

        {loading ? <AnalyticsSkeletons /> : !hasAnalytics ? <EmptyAnalytics onUpload={() => navigate("/upload")} /> : <>
            <Suspense fallback={<ChartSkeletons />}><AnalyticsCharts skills={analytics.skills} companies={analytics.companies} roadmapProgress={learningPlan ? roadmapProgress : null} /></Suspense>
            <Insights skills={analytics.skills} companies={analytics.companies} averageMatch={analytics.averageMatch} missingSkills={totalMissingSkills} />
            <Stack direction={{ xs: "column", sm: "row" }} spacing={1.25} useFlexGap sx={{ flexWrap: "wrap" }}><Button variant="outlined" startIcon={<DownloadOutlinedIcon />} onClick={() => window.print()} disabled={!hasAnalytics}>Export PDF</Button><Button variant="outlined" startIcon={<DownloadOutlinedIcon />} onClick={exportCsv} disabled={!hasAnalytics}>Export CSV</Button><Button variant="contained" startIcon={<RefreshOutlinedIcon />} onClick={() => void loadAnalytics()} disabled={loading || !hasAnalytics}>Refresh Analytics</Button></Stack>
        </>}
    </Stack>;
}

const panelSx = { border: "1px solid", borderColor: "divider", borderRadius: 3, boxShadow: 1 };

const KpiCard = memo(function KpiCard({ icon, title, value, description, trend, loading, textValue = false }: { icon: ReactNode; title: string; value: string | number; description: string; trend: string; loading: boolean; textValue?: boolean }) {
    return <Grid size={{ xs: 12, sm: 6, lg: 4 }}><Card elevation={0} sx={{ ...panelSx, height: "100%", transition: "transform 160ms ease, box-shadow 160ms ease", "&:hover": { transform: "translateY(-4px)", boxShadow: 4 } }}><CardContent><Stack direction="row" spacing={1.25} sx={{ alignItems: "center" }}><Box sx={{ display: "grid", placeItems: "center", p: 1, borderRadius: 2, color: "primary.main", bgcolor: "primary.50" }}>{icon}</Box><Typography variant="body2" color="text.secondary">{title}</Typography></Stack>{loading ? <Skeleton width="60%" height={48} /> : <Tooltip title={String(value)}><Typography variant={textValue ? "h6" : "h4"} noWrap sx={{ mt: 2, fontWeight: 700 }}>{value}</Typography></Tooltip>}<Typography variant="body2" color="text.secondary" noWrap sx={{ mt: 0.5 }}>{description}</Typography><Stack direction="row" spacing={0.5} sx={{ alignItems: "center", mt: 1.25, color: "text.secondary" }}><TrendingUpOutlinedIcon fontSize="inherit" /><Typography variant="caption">{trend}</Typography></Stack></CardContent></Card></Grid>;
});

function Insights({ skills, companies, averageMatch, missingSkills }: { skills: Array<{ name: string; count: number }>; companies: Array<{ name: string; count: number }>; averageMatch: number; missingSkills: number | undefined }) {
    const insights = [
        { icon: <TrendingUpOutlinedIcon color="success" />, label: "Most demanded skill", value: skills[0]?.name ?? "Not available" },
        { icon: <BusinessOutlinedIcon color="primary" />, label: "Highest matching company", value: "Not available from analytics data" },
        { icon: <TrendingDownOutlinedIcon color="warning" />, label: "Lowest matching skill", value: "Not available from analytics data" },
        { icon: <AssessmentOutlinedIcon color="primary" />, label: "Average resume match", value: `${averageMatch}%` },
        { icon: <SchoolOutlinedIcon color="error" />, label: "Total missing skills", value: missingSkills === undefined ? "Not available" : String(missingSkills) },
        { icon: <PsychologyOutlinedIcon color="success" />, label: "Strongest resume", value: "Not available from analytics data" },
        { icon: <PsychologyOutlinedIcon color="warning" />, label: "Weakest resume", value: "Not available from analytics data" },
        { icon: <BusinessOutlinedIcon color="primary" />, label: "Most represented company", value: companies[0]?.name ?? "Not available" },
    ];
    return <Card elevation={0} sx={panelSx}><CardContent><Typography variant="h6" sx={{ fontWeight: 700 }}>Insights</Typography><Typography variant="body2" color="text.secondary" sx={{ mt: 0.5 }}>What the available analytics data shows.</Typography><Box sx={{ display: "grid", gridTemplateColumns: { xs: "1fr", sm: "1fr 1fr", lg: "repeat(4, 1fr)" }, gap: 2, mt: 2.5 }}>{insights.map((insight) => <Stack key={insight.label} direction="row" spacing={1} sx={{ minWidth: 0, alignItems: "center" }}>{insight.icon}<Box sx={{ minWidth: 0 }}><Typography variant="caption" color="text.secondary">{insight.label}</Typography><Typography variant="body2" noWrap sx={{ fontWeight: 600 }} title={insight.value}>{insight.value}</Typography></Box></Stack>)}</Box></CardContent></Card>;
}

function EmptyAnalytics({ onUpload }: { onUpload: () => void }) { return <Card elevation={0} sx={{ ...panelSx, borderStyle: "dashed" }}><CardContent sx={{ py: 7, textAlign: "center" }}><AssessmentOutlinedIcon color="primary" sx={{ fontSize: 52 }} /><Typography variant="h6" sx={{ mt: 1.5, fontWeight: 700 }}>No analytics available.</Typography><Typography color="text.secondary" sx={{ mt: 0.75 }}>Upload a resume and add jobs to generate useful analytics.</Typography><Button variant="contained" startIcon={<UploadFileOutlinedIcon />} sx={{ mt: 2.5 }} onClick={onUpload}>Upload Resume</Button></CardContent></Card>; }

function ChartSkeletons() { return <Grid container spacing={2.5}>{Array.from({ length: 6 }, (_, index) => <Grid key={index} size={{ xs: 12, md: 6 }}><Skeleton variant="rounded" height={330} /></Grid>)}</Grid>; }
function AnalyticsSkeletons() { return <><ChartSkeletons /><Skeleton variant="rounded" height={180} /></>; }
