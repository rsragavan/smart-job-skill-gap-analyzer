import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import {
    Alert,
    Box,
    Button,
    Grid,
    Paper,
    Stack,
    Typography,
    Skeleton,
} from "@mui/material";
import CloudUploadOutlinedIcon from "@mui/icons-material/CloudUploadOutlined";
import SearchOutlinedIcon from "@mui/icons-material/SearchOutlined";
import TimelineOutlinedIcon from "@mui/icons-material/TimelineOutlined";

import DashboardCard from "../components/DashboardCard";
import { getResumeHistory } from "../api/resumeHistoryApi";
import { useWorkflow } from "../contexts/WorkflowContext";

interface ResumeHistoryItem {
    id: number;
    filename: string;
    skills: string[];
    recommended_jobs: number;
    uploaded_at: string;
}

interface SummaryCard {
    title: string;
    value: string | number;
}

export default function Dashboard() {
    const navigate = useNavigate();
    const { learningPlan, roadmapProgress, selectedJob } = useWorkflow();
    const [history, setHistory] = useState<ResumeHistoryItem[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        let active = true;

        const loadDashboard = async () => {
            try {
                const data: ResumeHistoryItem[] = await getResumeHistory();
                if (active) {
                    setHistory(data);
                }
            } catch (err: unknown) {
                if (active) {
                    const message = err instanceof Error ? err.message : "Failed to load dashboard data";
                    setError(message);
                }
            } finally {
                if (active) {
                    setLoading(false);
                }
            }
        };

        void loadDashboard();

        return () => {
            active = false;
        };
    }, []);

    const latestResume = history[0];
    const summaryCards: SummaryCard[] = [
        { title: "Resume Uploaded", value: latestResume ? "Yes" : "No" },
        { title: "Skills Extracted", value: latestResume?.skills.length ?? 0 },
        { title: "Recommended Jobs", value: latestResume?.recommended_jobs ?? 0 },
        { title: "Selected Job", value: selectedJob?.title ?? "Not selected" },
        { title: "Missing Skills", value: learningPlan?.total_missing_skills ?? "Not calculated" },
        { title: "Roadmap Progress", value: learningPlan ? `${roadmapProgress}%` : "Not started" },
    ];

    return (
        <Stack spacing={3}>
            <Box>
                <Typography variant="h4" sx={{ fontWeight: 700 }}>
                    Dashboard
                </Typography>
                <Typography color="text.secondary" sx={{ mt: 0.5 }}>
                    Track your resume analysis and plan your next career move.
                </Typography>
            </Box>

            {error && <Alert severity="error" action={<Button color="inherit" size="small" onClick={() => window.location.reload()}>Retry</Button>}>{error}</Alert>}

            {loading ? (
                <Grid container spacing={2}>{Array.from({ length: 6 }, (_, index) => <Grid key={index} size={{ xs: 12, sm: 6, lg: 4 }}><Skeleton variant="rounded" height={140} /></Grid>)}</Grid>
            ) : (
                <>
                    <Grid container spacing={2}>
                        {summaryCards.map((card) => (
                            <Grid key={card.title} size={{ xs: 12, sm: 6, lg: 4 }}>
                                <DashboardCard title={card.title} value={card.value} />
                            </Grid>
                        ))}
                    </Grid>

                    {selectedJob && (
                        <Paper variant="outlined" sx={{ p: { xs: 2, sm: 3 } }}>
                            <Typography variant="h6">Selected Job</Typography>
                            <Typography sx={{ mt: 1 }}>
                                {selectedJob.title}
                            </Typography>
                            <Typography color="text.secondary" variant="body2">
                                {selectedJob.company}
                            </Typography>
                            <Stack direction={{ xs: "column", sm: "row" }} spacing={{ xs: 0.5, sm: 3 }} sx={{ mt: 2 }}>
                                <Typography variant="body2">
                                    Match: {learningPlan ? `${learningPlan.match_percentage}%` : "Calculating..."}
                                </Typography>
                                <Typography variant="body2">
                                    Missing skills: {learningPlan?.total_missing_skills ?? "Calculating..."}
                                </Typography>
                            </Stack>
                        </Paper>
                    )}

                    {!latestResume && (
                        <Paper
                            variant="outlined"
                            sx={{ p: { xs: 3, sm: 4 }, textAlign: "center" }}
                        >
                            <Typography variant="h6">No resume data yet</Typography>
                            <Typography color="text.secondary" sx={{ mt: 1 }}>
                                Upload a resume to extract your skills and receive job recommendations.
                            </Typography>
                            <Button
                                sx={{ mt: 2 }}
                                variant="contained"
                                startIcon={<CloudUploadOutlinedIcon />}
                                onClick={() => navigate("/upload")}
                            >
                                Upload Resume
                            </Button>
                        </Paper>
                    )}

                    <Paper variant="outlined" sx={{ p: { xs: 2, sm: 3 } }}>
                        <Typography variant="h6">Quick Actions</Typography>
                        <Typography color="text.secondary" variant="body2" sx={{ mt: 0.5 }}>
                            Continue with the next step in your job search.
                        </Typography>
                        <Stack
                            direction={{ xs: "column", sm: "row" }}
                            spacing={1.5}
                            sx={{ mt: 2 }}
                        >
                            <Button
                                variant="contained"
                                startIcon={<CloudUploadOutlinedIcon />}
                                onClick={() => navigate("/upload")}
                            >
                                Upload Resume
                            </Button>
                            <Button
                                variant="outlined"
                                startIcon={<SearchOutlinedIcon />}
                                onClick={() => navigate("/jobs")}
                            >
                                Find Jobs
                            </Button>
                            <Button
                                variant="outlined"
                                startIcon={<TimelineOutlinedIcon />}
                                onClick={() => navigate("/learning")}
                            >
                                Generate Roadmap
                            </Button>
                        </Stack>
                    </Paper>
                </>
            )}
        </Stack>
    );
}
