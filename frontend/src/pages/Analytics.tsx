import { lazy, Suspense, useCallback, useEffect, useState } from "react";
import { Alert, Box, Button, Card, CardContent, Chip, CircularProgress, Grid, Stack, TextField, Typography } from "@mui/material";
import RefreshOutlinedIcon from "@mui/icons-material/RefreshOutlined";
import UploadFileOutlinedIcon from "@mui/icons-material/UploadFileOutlined";
import { useNavigate } from "react-router-dom";
import { downloadPlacementReport, getAnalyticsDashboard, getAnalyticsNotifications, getPlacementAnalytics, type AnalyticsDashboard, type AnalyticsNotification, type PlacementAnalytics } from "../api/analyticsApi";
import { useWorkflow } from "../contexts/WorkflowContext";

const Charts = lazy(() => import("../components/ProfessionalAnalyticsCharts"));
const panel = { border: "1px solid", borderColor: "divider", borderRadius: 3, boxShadow: 1 };

export default function Analytics() {
    const navigate = useNavigate();
    const { activeTarget } = useWorkflow();
    const [data, setData] = useState<AnalyticsDashboard | null>(null);
    const [placement, setPlacement] = useState<PlacementAnalytics | null>(null);
    const [notifications, setNotifications] = useState<AnalyticsNotification[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [filters, setFilters] = useState({ company: "", role: "", skill: "", date_from: "", date_to: "" });
    const [filtersSeeded, setFiltersSeeded] = useState(false);

    useEffect(() => {
        if (filtersSeeded || !activeTarget) return;
        setFilters((current) => ({
            ...current,
            company: current.company || activeTarget.company,
            role: current.role || activeTarget.role_title,
        }));
        setFiltersSeeded(true);
    }, [activeTarget, filtersSeeded]);

    const load = useCallback(async () => {
        setLoading(true); setError(null);
        try {
            const [dashboard, placementData, notificationData] = await Promise.all([getAnalyticsDashboard(filters), getPlacementAnalytics(), getAnalyticsNotifications()]);
            setData(dashboard); setPlacement(placementData); setNotifications(notificationData);
        } catch (err) { setError(err instanceof Error ? err.message : "Unable to load analytics."); }
        finally { setLoading(false); }
    }, [filters]);
    useEffect(() => {
        const timer = window.setTimeout(() => { void load(); }, 300);
        return () => window.clearTimeout(timer);
    }, [load]);

    const setFilter = (key: keyof typeof filters, value: string) => setFilters((current) => ({ ...current, [key]: value }));
    return <Stack spacing={3}>
        <Stack direction={{ xs: "column", sm: "row" }} sx={{ justifyContent: "space-between", gap: 2, alignItems: { sm: "center" } }}><Box><Typography variant="h4" sx={{ fontWeight: 700 }}>Analytics Dashboard</Typography><Typography color="text.secondary">One source of truth for resume, job market, learning, roadmap, career, and XP analytics.</Typography></Box><Button variant="outlined" startIcon={<RefreshOutlinedIcon />} onClick={() => void load()} disabled={loading}>Refresh</Button></Stack>
        {activeTarget && (
            <Alert severity="info">
                Filters defaulted from active target: <strong>{activeTarget.company}</strong> · {activeTarget.role_title}
            </Alert>
        )}
        <Card sx={panel}><CardContent><Stack direction={{ xs: "column", sm: "row" }} spacing={1.5}><TextField size="small" label="Company" value={filters.company} onChange={(event) => setFilter("company", event.target.value)} /><TextField size="small" label="Role" value={filters.role} onChange={(event) => setFilter("role", event.target.value)} /><TextField size="small" label="Skill" value={filters.skill} onChange={(event) => setFilter("skill", event.target.value)} /><TextField size="small" type="date" label="From" InputLabelProps={{ shrink: true }} value={filters.date_from} onChange={(event) => setFilter("date_from", event.target.value)} /><TextField size="small" type="date" label="To" InputLabelProps={{ shrink: true }} value={filters.date_to} onChange={(event) => setFilter("date_to", event.target.value)} /></Stack></CardContent></Card>
        {error && <Alert severity="error" action={<Button color="inherit" onClick={() => void load()}>Retry</Button>}>{error}</Alert>}
        {loading && !data ? <Box sx={{ minHeight: 350, display: "grid", placeItems: "center" }}><CircularProgress /></Box> : data ? <>
            <Grid container spacing={2}>{[
                ["Resume Statistics", `${data.resume_statistics.uploads} uploads · ${data.resume_statistics.skills} skills`], ["Job Statistics", `${data.job_statistics.jobs} jobs · ${data.job_statistics.companies} companies`], ["Skill Match %", `${data.skill_statistics.match_percentage}%`], ["Learning Statistics", `${data.learning_statistics.progress}% complete`], ["Roadmap Statistics", `${data.roadmap_statistics.completed_skills}/${data.roadmap_statistics.skills} skills`], ["Career Statistics", `${data.career_statistics.readiness}% readiness`], ["XP Statistics", `${data.xp_statistics.total} XP · Level ${data.xp_statistics.level}`], ["Badge Statistics", `${data.badge_statistics.unlocked} badges · ${data.badge_statistics.achievements} achievements`], ["Mission Statistics", `${data.mission_statistics.completed}/${data.mission_statistics.total} completed`],
            ].map(([title, value]) => <Grid key={title} size={{ xs: 12, sm: 6, lg: 4 }}><Card sx={{ ...panel, height: "100%" }}><CardContent><Typography color="text.secondary">{title}</Typography><Typography variant="h5" sx={{ mt: 1, fontWeight: 700 }}>{value}</Typography></CardContent></Card></Grid>)}</Grid>
            <Card sx={panel}><CardContent><Typography variant="h6" gutterBottom>Matched and Missing Skills</Typography><Stack direction="row" flexWrap="wrap" useFlexGap spacing={1}><Chip color="success" label={`${data.skill_statistics.matched.length} matched`} />{data.skill_statistics.missing.slice(0, 8).map((skill) => <Chip key={skill} color="warning" variant="outlined" label={skill} />)}</Stack></CardContent></Card>
            {placement && <>
                <Stack direction={{ xs: "column", sm: "row" }} sx={{ justifyContent: "space-between", alignItems: { sm: "center" }, gap: 2 }}>
                    <Box><Typography variant="h5" sx={{ fontWeight: 700 }}>Placement Analytics</Typography><Typography color="text.secondary">Personalized readiness, applications, company fit, interviews, and next actions.</Typography></Box>
                    <Stack direction="row" spacing={1} flexWrap="wrap"><Button size="small" variant="outlined" onClick={() => void downloadPlacementReport("placement")}>PDF report</Button><Button size="small" variant="outlined" onClick={() => void downloadPlacementReport("skill")}>Skills PDF</Button></Stack>
                </Stack>
                {notifications.length > 0 && <Stack spacing={1}>{notifications.map((item) => <Alert key={`${item.type}-${item.title}`} severity={item.severity}>{item.title}: {item.detail}</Alert>)}</Stack>}
                <Grid container spacing={2}>{Object.entries({ Overall: placement.readiness.overall, Company: placement.readiness.company, Interview: placement.readiness.interview, Coding: placement.readiness.coding, Resume: placement.readiness.resume, Communication: placement.readiness.communication, Learning: placement.readiness.learning }).map(([label, value]) => <Grid key={label} size={{ xs: 6, sm: 3, md: 1.7 }}><Card sx={{ ...panel, height: "100%" }}><CardContent><Typography color="text.secondary" variant="body2">{label}</Typography><Typography variant="h5" sx={{ mt: 1, fontWeight: 700 }}>{value}%</Typography></CardContent></Card></Grid>)}</Grid>
                <Grid container spacing={2}>{[
                    ["Applications", `${placement.applications.submitted} submitted`, `${placement.applications.response_rate}% response`], ["Offers", `${placement.applications.offers}`, `${placement.applications.offer_rate}% offer rate`], ["Interviews", `${placement.interviews.completed}/${placement.interviews.mock_interviews} completed`, `${placement.interviews.average_score}% average`], ["Learning", `${placement.skills.learning_progress}% complete`, `${placement.skills.missing.length} market gaps`],
                ].map(([title, value, detail]) => <Grid key={title} size={{ xs: 12, sm: 6, md: 3 }}><Card sx={{ ...panel, height: "100%" }}><CardContent><Typography color="text.secondary">{title}</Typography><Typography variant="h5" sx={{ mt: 1, fontWeight: 700 }}>{value}</Typography><Typography variant="body2" color="text.secondary">{detail}</Typography></CardContent></Card></Grid>)}</Grid>
                <Grid container spacing={2}>{[
                    ["Top hiring", placement.companies.top_hiring.map(([name, count]) => `${name} (${count})`)], ["Most requested skills", placement.skills.most_requested.map(([name, count]) => `${name} (${count})`)], ["Strong skills", placement.skills.strong], ["Missing skills", placement.skills.missing], ["Remote-friendly", placement.companies.remote_friendly], ["Interview focus", placement.interviews.weak_areas],
                ].map(([title, values]) => <Grid key={String(title)} size={{ xs: 12, sm: 6, md: 4 }}><Card sx={{ ...panel, height: "100%" }}><CardContent><Typography variant="h6" gutterBottom>{String(title)}</Typography><Stack direction="row" flexWrap="wrap" useFlexGap spacing={1}>{(values as string[]).length ? (values as string[]).slice(0, 8).map((value) => <Chip key={value} label={value} size="small" variant="outlined" />) : <Typography color="text.secondary">No verified data yet.</Typography>}</Stack></CardContent></Card></Grid>)}</Grid>
                <Card sx={panel}><CardContent><Typography variant="h6" gutterBottom>Recommendations</Typography><Stack spacing={1}>{[...placement.recommendations.skills.map((item) => `Learn ${item.skill}: ${item.reason}`), ...placement.recommendations.mock_interviews.map((item) => `Practice ${item.type}: ${item.reason}`), ...placement.recommendations.coding_practice.map((item) => `Code ${item.topic}: ${item.reason}`)].slice(0, 8).map((item) => <Typography key={item} variant="body2">• {item}</Typography>)}</Stack></CardContent></Card>
            </>}
            <Suspense fallback={<CircularProgress />}><Charts data={data} /></Suspense>
        </> : <Card sx={panel}><CardContent sx={{ textAlign: "center", py: 8 }}><Typography variant="h6">No analytics available</Typography><Typography color="text.secondary" sx={{ mt: 1 }}>Upload a resume and begin a roadmap to generate analytics.</Typography><Button variant="contained" startIcon={<UploadFileOutlinedIcon />} sx={{ mt: 2 }} onClick={() => navigate("/upload")}>Upload Resume</Button></CardContent></Card>}
    </Stack>;
}
