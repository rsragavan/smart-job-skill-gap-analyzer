import {
    Card,
    CardContent,
    Typography,
    Box,
    Chip,
    LinearProgress,
    Stack,
    Button,
} from "@mui/material";
import { useNavigate } from "react-router-dom";
import type { RecommendedJob } from "../types/resume";
import { useWorkflow } from "../contexts/WorkflowContext";

interface Props {
    job: RecommendedJob;
}

export default function RecommendedJobCard({ job }: Props) {
    const navigate = useNavigate();
    const { selectJob } = useWorkflow();

    const handleViewJob = () => {
        window.open(job.url, "_blank");
    };

    const handleGenerateRoadmap = () => {
        selectJob({
            id: job.job_id,
            title: job.job_title,
            company: job.company,
            location: job.location,
        });
        navigate("/learning");
    };

    return (
        <Card elevation={2} sx={{ borderRadius: 2, height: "100%" }}>
            <CardContent>
                <Box sx={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", mb: 1 }}>
                    <div>
                        <Typography variant="h6">{job.job_title}</Typography>
                        <Typography color="text.secondary" variant="body2">
                            {job.company}
                        </Typography>
                        <Typography color="text.secondary" variant="caption">
                            {job.location}
                        </Typography>
                    </div>

                    <Box sx={{ textAlign: "right" }}>
                        <Typography variant="subtitle1">{job.match_percentage}%</Typography>
                        <Typography variant="caption" color="text.secondary">
                            Match
                        </Typography>
                    </Box>
                </Box>

                <Box sx={{ mb: 1 }}>
                    <LinearProgress variant="determinate" value={job.match_percentage} />
                </Box>

                <Stack direction="row" spacing={1} useFlexGap sx={{ flexWrap: "wrap", mb: 1 }}>
                    {job.matched_skills.map((s) => (
                        <Chip
                            key={s}
                            label={s}
                            size="small"
                            sx={{
                                backgroundColor: "#c8e6c9",
                                color: "#1b5e20",
                                fontWeight: 500,
                            }}
                        />
                    ))}

                    {job.missing_skills.map((s) => (
                        <Chip
                            key={s}
                            label={s}
                            size="small"
                            sx={{
                                backgroundColor: "#ffcdd2",
                                color: "#b71c1c",
                                fontWeight: 500,
                            }}
                        />
                    ))}
                </Stack>

                <Box sx={{ mt: 2, display: "flex", gap: 1, justifyContent: "flex-end" }}>
                    <Button size="small" variant="outlined" onClick={handleViewJob}>
                        View Job
                    </Button>
                    <Button size="small" variant="contained" onClick={handleGenerateRoadmap}>
                        Generate Roadmap
                    </Button>
                </Box>
            </CardContent>
        </Card>
    );
}


