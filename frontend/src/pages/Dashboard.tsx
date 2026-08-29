import { useEffect, useState } from "react";

import {
    Container,
    Box,
    Typography,
    Grid,
    Paper,
    List,
    ListItem,
    ListItemText,
    Divider,
    Alert,
    Button,
    Skeleton,
    Stack,
    Chip,
} from "@mui/material";
import { Link as RouterLink } from "react-router-dom";

import DashboardCard from "../components/DashboardCard";
import dashboardService from "../services/dashboardService";
import type { DashboardData } from "../types/dashboard";
import ApplicationStatusChart from "../components/ApplicationStatusChart";
import TopSkillsChart from "../components/TopSkillsChart";
import { useWorkflow } from "../contexts/WorkflowContext";
import TargetIntelligencePanel from "../components/TargetIntelligencePanel";
import { getCareerGPS, type CareerGPSData } from "../api/careerGpsApi";

export default function DashboardPage() {
    const { activeTarget, targetIntelligence } = useWorkflow();
    const [dashboard, setDashboard] = useState<DashboardData | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [coach, setCoach] = useState<CareerGPSData | null>(null);

    const loadDashboard = async () => {
        try {
            setError(null);
            const data = await dashboardService.getDashboard();
            setDashboard(data);
            void getCareerGPS().then(setCoach).catch(() => undefined);
        } catch (requestError) {
            setError(requestError instanceof Error ? requestError.message : "Unable to load your dashboard.");
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        void loadDashboard();
    }, []);

    if (loading) {
        return (
            <Container maxWidth="xl" sx={{ mt: 2 }}>
                <Stack spacing={2}><Skeleton variant="text" width={240} height={56} /><Skeleton variant="text" width={420} height={28} /><Grid container spacing={2}>{Array.from({ length: 8 }, (_, index) => <Grid key={index} size={{ xs: 12, sm: 6, md: 3 }}><Skeleton variant="rounded" height={126} /></Grid>)}</Grid><Skeleton variant="rounded" height={220} /></Stack>
            </Container>
        );
    }

    if (!dashboard) {
        return (
            <Container sx={{ mt: 4 }}>
                <Alert severity="error" action={<Button color="inherit" onClick={() => { setLoading(true); void loadDashboard(); }}>Retry</Button>}>{error || "Dashboard data is not available."}</Alert>
            </Container>
        );
    }

    return (
        <Container maxWidth="xl" sx={{ mt: 4 }}>

            <Typography
                variant="h4"
                fontWeight="bold"
                gutterBottom
            >
                Dashboard
            </Typography>

            <Typography
                color="text.secondary"
                sx={{ mb: 4 }}
            >
                Track your job applications and progress.
            </Typography>

            {activeTarget ? (
                <Alert
                    severity="info"
                    sx={{ mb: 3 }}
                    action={
                        <Stack direction="row" spacing={1}>
                            <Button component={RouterLink} to="/learning" color="inherit" size="small">Learning</Button>
                            <Button component={RouterLink} to="/career-gps" color="inherit" size="small">Career GPS</Button>
                            <Button component={RouterLink} to="/jobs" color="inherit" size="small">Change</Button>
                        </Stack>
                    }
                >
                    Active target: <strong>{activeTarget.company}</strong> · {activeTarget.role_title}{" "}
                    <Chip size="small" sx={{ ml: 1 }} label={activeTarget.source_type === "scraped" ? "Scraped" : "Custom"} />
                    {" · "}{activeTarget.match_percentage}% match
                </Alert>
            ) : (
                <Alert
                    severity="warning"
                    sx={{ mb: 3 }}
                    action={<Button component={RouterLink} to="/jobs" color="inherit" size="small">Choose Target</Button>}
                >
                    Start by choosing a scraped company or pasting a custom job description.
                </Alert>
            )}

            {activeTarget && <TargetIntelligencePanel data={targetIntelligence} />}

            {coach && <Paper sx={{ mt: 4, p: 3 }}><Stack direction={{ xs: "column", md: "row" }} spacing={3} sx={{ alignItems: { md: "center" } }}><Box sx={{ flex: 1 }}><Typography variant="h6">Career Guidance</Typography><Typography color="text.secondary">{coach.goals.goal_role || "Choose a target role"} · {coach.goals.target_company || "Choose a target company"}</Typography><Typography sx={{ mt: 1 }}>Next priority: {coach.skill_analysis?.priority_skills?.[0] || coach.skill_gaps[0] || "Keep building your roadmap"}</Typography></Box><Stack direction="row" spacing={2}><Chip label={`${coach.readiness_score}% readiness`} color="primary" /><Chip label={`${coach.learning_progress}% learning`} color="success" variant="outlined" /><Button component={RouterLink} to="/career-gps" variant="outlined">Open Career GPS</Button></Stack></Stack></Paper>}

            <Grid container spacing={3}>

                <Grid size={{ xs: 12, sm: 6, md: 3 }}>
                    <DashboardCard
                        title="Applications"
                        value={dashboard.total_applications}
                    />
                </Grid>

                <Grid size={{ xs: 12, sm: 6, md: 3 }}><DashboardCard title="Interviews" value={dashboard.interviews_completed ?? 0} /></Grid>
                <Grid size={{ xs: 12, sm: 6, md: 3 }}><DashboardCard title="Average Interview Score" value={dashboard.average_interview_score ?? 0} /></Grid>

                <Grid size={{ xs: 12, sm: 6, md: 3 }}>
                    <DashboardCard
                        title="Applied"
                        value={dashboard.applied}
                    />
                </Grid>

                <Grid size={{ xs: 12, sm: 6, md: 3 }}>
                    <DashboardCard
                        title="Interview"
                        value={dashboard.interview}
                    />
                </Grid>

                <Grid size={{ xs: 12, sm: 6, md: 3 }}>
                    <DashboardCard
                        title="Offers"
                        value={dashboard.offer}
                    />
                </Grid>

                <Grid size={{ xs: 12, sm: 6, md: 3 }}>
                    <DashboardCard
                        title="Rejected"
                        value={dashboard.rejected}
                    />
                </Grid>

                <Grid size={{ xs: 12, sm: 6, md: 3 }}>
                    <DashboardCard
                        title="Shortlisted"
                        value={dashboard.shortlisted}
                    />
                </Grid>

                <Grid size={{ xs: 12, sm: 6, md: 3 }}>
                    <DashboardCard
                        title="Jobs"
                        value={dashboard.total_jobs}
                    />
                </Grid>

                <Grid size={{ xs: 12, sm: 6, md: 3 }}>
                    <DashboardCard
                        title="Companies"
                        value={dashboard.total_companies}
                    />
                </Grid>

            </Grid>

            {dashboard.recommended_interviews?.length ? <Paper sx={{ mt: 4, p: 3 }}><Typography variant="h6">Recommended Interviews</Typography><Stack spacing={1} sx={{ mt: 1 }}>{dashboard.recommended_interviews.map(item => <Typography key={item.application_id}>{item.type} interview · {item.company || "Company not available"} · {item.role || "Role not available"}</Typography>)}</Stack></Paper> : null}

            <Paper sx={{ mt: 5, p: 3 }}>

                <Typography
                    variant="h6"
                    gutterBottom
                >
                    Recent Applications
                </Typography>

                <List>

                    {dashboard.recent.length === 0 ? (
                        <Typography color="text.secondary">
                            No applications yet.
                        </Typography>
                    ) : (
                        dashboard.recent.map((application) => (
                            <div key={application.id}>

                                <ListItem>

                                    <ListItemText
                                        primary={application.job_title}
                                        secondary={`${application.company} • ${application.status}`}
                                    />

                                </ListItem>

                                <Divider />

                            </div>
                        ))
                    )}

                </List>

            </Paper>

<Paper sx={{ mt: 4, p: 3 }}>

    <Typography
        variant="h6"
        gutterBottom
    >
        Application Status
    </Typography>

    <ApplicationStatusChart
        applied={dashboard.applied}
        reviewing={dashboard.reviewing}
        shortlisted={dashboard.shortlisted}
        interview={dashboard.interview}
        offer={dashboard.offer}
        rejected={dashboard.rejected}
    />

</Paper>
            <Paper sx={{ mt: 4, p: 3 }}>

    <Typography
        variant="h6"
        gutterBottom
    >
        Top Skills in Current Jobs
    </Typography>

    <TopSkillsChart
        python={dashboard.python_jobs}
        java={dashboard.java_jobs}
        docker={dashboard.docker_jobs}
        linux={dashboard.linux_jobs}
        remote={dashboard.remote_jobs}
    />

</Paper>

        </Container>

    );
}
