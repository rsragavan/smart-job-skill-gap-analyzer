import { useCallback, useEffect, useState } from "react";
import {
    Alert, Box, Button, Card, CardContent, Chip, CircularProgress, Divider, LinearProgress, Stack, TextField, Typography,
} from "@mui/material";
import { Link as RouterLink } from "react-router-dom";
import { getCareerGPS, updateCareerGoals, type CareerGPSData } from "../api/careerGpsApi";
import { getActiveSkillGap, type SkillGapAnalysis } from "../api/targetApi";

const panel = { border: "1px solid", borderColor: "divider", borderRadius: 3, boxShadow: 1 };

export default function CareerGPS() {
    const [data, setData] = useState<CareerGPSData | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [role, setRole] = useState("");
    const [company, setCompany] = useState("");
    const [skillGap, setSkillGap] = useState<SkillGapAnalysis | null>(null);

    const load = useCallback(async () => {
        setLoading(true); setError(null);
        try { const result = await getCareerGPS(); setData(result); setRole(result.goals.goal_role || ""); setCompany(result.goals.target_company || ""); setSkillGap(result.active_target ? await getActiveSkillGap() : null); }
        catch (err) { setError(err instanceof Error ? err.message : "Unable to load Career GPS."); }
        finally { setLoading(false); }
    }, []);
    useEffect(() => { void load(); }, [load]);

    const saveGoals = async () => {
        try { setData(await updateCareerGoals({ goal_role: role || null, target_company: company || null })); }
        catch (err) { setError(err instanceof Error ? err.message : "Unable to save career goals."); }
    };

    if (loading && !data) return <Box sx={{ minHeight: 320, display: "grid", placeItems: "center" }}><CircularProgress /></Box>;
    if (!data) return <Alert severity="error">{error || "Career GPS is unavailable."}</Alert>;

    const sourceLabel = data.source_type === "scraped"
        ? "Scraped Company"
        : data.source_type === "custom"
            ? "Custom Job Description"
            : null;

    return <Stack spacing={3}>
        <Box><Typography variant="h4" sx={{ fontWeight: 700 }}>Career GPS</Typography><Typography color="text.secondary">Personalized guidance based on your resume, target, learning activity, job market, and applications.</Typography></Box>
        {error && <Alert severity="error" onClose={() => setError(null)}>{error}</Alert>}
        {data.active_target ? (
            <Alert severity="info" action={<Button component={RouterLink} to="/jobs" color="inherit" size="small">Change Target</Button>}>
                Target: <strong>{data.active_target.company}</strong> · {data.active_target.role_title}
                {sourceLabel && <Chip size="small" sx={{ ml: 1 }} label={sourceLabel} />}
                {" · "}{data.current_match_percentage}% current match
            </Alert>
        ) : (
            <Alert severity="warning" action={<Button component={RouterLink} to="/jobs" color="inherit" size="small">Choose Target</Button>}>
                No active target yet. Select a scraped job or paste a custom JD so Career GPS can track company-specific readiness.
            </Alert>
        )}
        {data.readiness && <>
            <Card sx={panel}><CardContent><Stack direction={{ xs: "column", md: "row" }} spacing={3} sx={{ alignItems: { md: "center" } }}><ScoreCard title="Career Readiness" value={data.readiness.score} color="primary" /><Box sx={{ flex: 2 }}><Typography variant="h6">Next Best Action</Typography><Typography fontWeight={700}>{data.next_action?.title || "No action available"}</Typography><Typography color="text.secondary">{data.next_action?.reason || "Complete more career activity to receive a recommendation."}</Typography></Box></Stack></CardContent></Card>
            <Stack direction={{ xs: "column", md: "row" }} spacing={2}><MetricCard title="Skill Match" value={formatMetric(data.readiness.components.skill_match)} detail="Active target coverage" /><MetricCard title="Learning" value={formatMetric(data.readiness.components.learning)} detail="Roadmap progress" /><MetricCard title="Coding" value={formatMetric(data.readiness.components.coding)} detail={`${data.coding?.solved ?? 0} solved / ${data.coding?.attempted ?? 0} attempted`} /><MetricCard title="Interview" value={formatMetric(data.readiness.components.interview)} detail={`${data.interview?.completed ?? 0} completed`} /></Stack>
            <Stack direction={{ xs: "column", md: "row" }} spacing={2}><Section title="High Priority Gaps" items={(data.skills?.high_priority || []).map(skill => <Chip key={skill} label={skill} color="error" />)} empty="No high-priority gaps." /><Section title="Learning Progress" items={data.learning?.items.slice(0, 6).map(item => <Typography key={`${item.skill}-${item.item}`} variant="body2">{item.status === "completed" ? "✓" : "○"} {item.skill} · {item.item}</Typography>) || []} empty="Learning progress unavailable." /><Section title="Gamification" items={[<Typography key="xp">{data.gamification?.xp ?? 0} XP · {data.gamification?.current_streak ?? 0} day streak</Typography>, <Typography key="badges">{data.gamification?.badges.length ?? 0} badges unlocked</Typography>]} /></Stack>
        </>}
        {data.skill_analysis && <Card sx={panel}><CardContent><Typography variant="h6" gutterBottom>Smart Skill Gap Analysis</Typography><Stack direction={{ xs: "column", md: "row" }} spacing={3}><Box sx={{ flex: 1 }}><Typography color="text.secondary">Current skills</Typography><Stack direction="row" flexWrap="wrap" useFlexGap spacing={1} sx={{ mt: 1 }}>{data.skill_analysis.current_skills.map(skill => <Chip key={skill} label={skill} color="success" variant="outlined" />)}</Stack></Box><Box sx={{ flex: 1 }}><Typography color="text.secondary">Priority skills</Typography><Stack direction="row" flexWrap="wrap" useFlexGap spacing={1} sx={{ mt: 1 }}>{data.skill_analysis.priority_skills.map(skill => <Chip key={skill} label={skill} color="warning" />)}</Stack></Box></Stack><Typography sx={{ mt: 2 }}>Skill match: <strong>{data.skill_analysis.skill_match_percentage}%</strong> · Estimated learning time: <strong>{data.learning_plan?.estimated_days ?? 0} days</strong></Typography></CardContent></Card>}
        {skillGap && <Card sx={panel}><CardContent><Typography variant="h6" gutterBottom>Explainable Target Skill Gap</Typography><Typography color="text.secondary">{skillGap.match_percentage}% match · Matched skills are present in both your resume and target requirements.</Typography><Stack direction={{ xs: "column", md: "row" }} spacing={3} sx={{ mt: 2 }}><Box sx={{ flex: 1 }}><Typography fontWeight={700}>Matched Skills</Typography><Stack direction="row" flexWrap="wrap" useFlexGap spacing={1} sx={{ mt: 1 }}>{skillGap.matched_skills.map(skill => <Chip key={skill} label={skill} color="success" variant="outlined" />)}</Stack></Box><Box sx={{ flex: 1 }}><Typography fontWeight={700}>Missing Skills</Typography><Stack direction="row" flexWrap="wrap" useFlexGap spacing={1} sx={{ mt: 1 }}>{skillGap.missing_skill_details.map(item => <Chip key={item.skill} label={`${item.skill} · ${item.priority}`} color={item.priority === "HIGH" ? "error" : "warning"} />)}</Stack></Box></Stack><Stack direction={{ xs: "column", md: "row" }} spacing={2} sx={{ mt: 2 }}><RecommendationCard title="Learning" items={skillGap.learning_recommendations.map(item => `${item.title}: ${item.reason}`)} /><RecommendationCard title="Coding Practice" items={skillGap.coding_recommendations.map(item => `${item.title}: ${item.reason}`)} /><RecommendationCard title="Mock Interview" items={skillGap.interview_recommendations.map(item => `${item.question}: ${item.reason}`)} /></Stack></CardContent></Card>}
        {data.application_insights && <Card sx={panel}><CardContent><Typography variant="h6" gutterBottom>Application Insights</Typography><Stack direction={{ xs: "column", sm: "row" }} spacing={3} flexWrap="wrap"><MetricCard title="Applications" value={String(data.application_insights.applications_sent)} detail={`${data.application_insights.companies_applied} companies`} /><MetricCard title="Interview Rate" value={`${data.application_insights.interview_rate}%`} detail={`${data.application_insights.interviews} interviews`} /><MetricCard title="Rejection Rate" value={`${data.application_insights.rejection_rate}%`} detail={`${data.application_insights.rejections} rejected`} /><MetricCard title="Offer Rate" value={`${data.application_insights.offer_rate}%`} detail={`${data.application_insights.offers} offers`} /></Stack></CardContent></Card>}
        {data.interview_preparation && <Card sx={panel}><CardContent><Typography variant="h6" gutterBottom>Personalized Interview Preparation</Typography><Typography color="text.secondary">Required skills: {data.interview_preparation.required_skills.length ? data.interview_preparation.required_skills.join(", ") : "Not Available"}</Typography><Stack direction="row" flexWrap="wrap" useFlexGap spacing={1} sx={{ mt: 2 }}>{data.interview_preparation.topics.slice(0, 12).map(topic => <Chip key={topic} label={topic} />)}</Stack><Typography sx={{ mt: 2 }}>Coding questions: {data.interview_preparation.coding_questions.length} · Behavioral questions: {data.interview_preparation.behavioral_questions.length} · Checklist items: {data.interview_preparation.checklist.length}</Typography></CardContent></Card>}
        <Stack direction={{ xs: "column", md: "row" }} spacing={2}>
            <MetricCard title="Current Match" value={`${data.current_match_percentage}%`} detail="Versus active target job skills" />
            <MetricCard title="Interview Readiness" value={`${data.interview_readiness}%`} detail="Projects, skills, and XP" />
            <MetricCard title="Job Readiness Score" value={`${data.job_readiness_score}%`} detail="Role and company fit" />
            <MetricCard title="Estimated Salary Growth" value={`+${data.estimated_salary_growth.percentage}%`} detail={data.estimated_salary_growth.basis} />
        </Stack>
        <Card sx={panel}><CardContent><Typography variant="h6">Career Goals</Typography><Stack direction={{ xs: "column", sm: "row" }} spacing={2} sx={{ mt: 2 }}><TextField label="Target role" value={role} onChange={(event) => setRole(event.target.value)} fullWidth /><TextField label="Target company" value={company} onChange={(event) => setCompany(event.target.value)} fullWidth /><Button variant="contained" onClick={() => void saveGoals()}>Save</Button></Stack><Typography sx={{ mt: 2 }} color="text.secondary">Current path: <strong>{data.career_path}</strong> · Estimated learning time: <strong>{data.estimated_learning_days} days</strong> · {data.xp} XP · Learning progress: <strong>{data.learning_progress}%</strong></Typography></CardContent></Card>
        <Stack direction={{ xs: "column", lg: "row" }} spacing={2}>
            <Section title="Remaining Skills" items={(data.remaining_skills.length ? data.remaining_skills : data.skill_gaps).map((skill) => <Chip key={skill} label={skill} color="warning" variant="outlined" />)} empty="No remaining skills for this target." />
            <Section title="Resume & Learning" items={[<Typography key="resume">{data.resume_skills.length} resume skills · {data.completed_skills.length} completed skills · {data.completed_projects} projects</Typography>, <LinearProgress key="progress" variant="determinate" value={data.learning_progress} />, <Typography key="percent" variant="caption">{data.learning_progress}% learning progress</Typography>]} />
        </Stack>
        <Stack direction={{ xs: "column", lg: "row" }} spacing={2}>
            <RecommendationCard title="Recommended Skills" items={data.recommendations.skills.map((item) => `${item.name} — ${item.reason}`)} />
            <RecommendationCard title="Recommended Certifications" items={data.recommendations.certifications.map((item) => `${item.name} (${item.skill})`)} />
            <RecommendationCard title="Recommended Projects" items={data.recommendations.projects.map((item) => `${item.title} · ${item.estimated_days} days`)} />
        </Stack>
        <Stack direction={{ xs: "column", lg: "row" }} spacing={2}>
            <Card sx={{ ...panel, flex: 1 }}><CardContent><Typography variant="h6" gutterBottom>Career Paths</Typography><Stack spacing={1.5}>{data.career_paths.slice(0, 6).map((path) => <Box key={path.path}><Stack direction="row" sx={{ justifyContent: "space-between" }}><Typography>{path.path}</Typography><Typography>{path.score}%</Typography></Stack><LinearProgress variant="determinate" value={path.score} /></Box>)}</Stack></CardContent></Card>
            <Card sx={{ ...panel, flex: 1 }}><CardContent><Typography variant="h6" gutterBottom>Technology Trends & Market Demand</Typography><Stack spacing={1}>{data.market_demand.map((item) => <Stack key={item.skill} direction="row" sx={{ justifyContent: "space-between" }}><Typography>{item.skill}</Typography><Chip size="small" label={`${item.jobs} jobs`} /></Stack>)}</Stack></CardContent></Card>
        </Stack>
        <Card sx={panel}><CardContent><Typography variant="h6" gutterBottom>Career Timeline</Typography><Stack divider={<Divider flexItem />} spacing={1}>{data.career_timeline.length ? data.career_timeline.map((event) => <Stack key={`${event.date}-${event.title}`} direction={{ xs: "column", sm: "row" }} spacing={2}><Typography color="text.secondary" sx={{ minWidth: 180 }}>{new Date(event.date).toLocaleDateString()}</Typography><Box><Typography fontWeight={600}>{event.title}</Typography><Typography variant="body2" color="text.secondary">{event.detail}</Typography></Box></Stack>) : <Typography color="text.secondary">Upload a resume or begin learning to start your timeline.</Typography>}</Stack></CardContent></Card>
    </Stack>;
}

function formatMetric(value: number | null | undefined) { return value == null ? "Not enough data" : `${value}%`; }

function ScoreCard({ title, value, color }: { title: string; value: number | null | undefined; color: "primary" | "success" | "secondary" }) {
    return <Card sx={{ ...panel, flex: 1 }}><CardContent><Stack direction="row" spacing={2} sx={{ alignItems: "center" }}>{value == null ? <Typography variant="h6">Not enough data</Typography> : <Box sx={{ position: "relative", display: "inline-flex" }}><CircularProgress variant="determinate" value={value} color={color} size={82} thickness={5} /><Box sx={{ inset: 0, position: "absolute", display: "grid", placeItems: "center" }}><Typography fontWeight={700}>{value}%</Typography></Box></Box>}<Box><Typography color="text.secondary">{title}</Typography><Typography variant="body2">Measured from available activity</Typography></Box></Stack></CardContent></Card>;
}

function MetricCard({ title, value, detail }: { title: string; value: string; detail: string }) {
    return <Card sx={{ ...panel, flex: 1 }}><CardContent><Typography color="text.secondary">{title}</Typography><Typography variant="h4" sx={{ my: 1, fontWeight: 700 }}>{value}</Typography><Typography variant="body2" color="text.secondary">{detail}</Typography></CardContent></Card>;
}

function Section({ title, items, empty }: { title: string; items: React.ReactNode[]; empty?: string }) {
    return <Card sx={{ ...panel, flex: 1 }}><CardContent><Typography variant="h6" gutterBottom>{title}</Typography>{items.length ? <Stack spacing={1.25}>{items}</Stack> : <Typography color="text.secondary">{empty}</Typography>}</CardContent></Card>;
}

function RecommendationCard({ title, items }: { title: string; items: string[] }) {
    return <Card sx={{ ...panel, flex: 1 }}><CardContent><Typography variant="h6" gutterBottom>{title}</Typography>{items.length ? <Stack spacing={1}>{items.map((item) => <Typography key={item} variant="body2">• {item}</Typography>)}</Stack> : <Typography color="text.secondary">No recommendations yet.</Typography>}</CardContent></Card>;
}
