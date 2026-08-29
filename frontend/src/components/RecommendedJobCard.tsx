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
import { useState } from "react";
import type { RecommendedJob } from "../types/resume";
import { useWorkflow } from "../contexts/WorkflowContext";

interface Props {
    job: RecommendedJob;
}

export default function RecommendedJobCard({ job }: Props) {
    const navigate = useNavigate();
    const { selectScrapedTarget } = useWorkflow();
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const handleViewJob = () => {
        window.open(job.url, "_blank");
    };

    const handleGenerateRoadmap = async () => {
        setLoading(true);
        setError(null);
        try {
            const { roadmap } = await selectScrapedTarget(job.job_id);
            navigate("/learning", { state: roadmap });
        } catch (requestError) {
            setError(requestError instanceof Error ? requestError.message : "Could not generate the learning roadmap.");
        } finally {
            setLoading(false);
        }
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

                {error && (
                    <Typography color="error" variant="caption" display="block" sx={{ mb: 1 }}>
                        {error}
                    </Typography>
                )}

                <Stack direction="row" spacing={1}>
                    <Button size="small" onClick={handleViewJob}>
                        View Job
                    </Button>
                    <Button size="small" variant="contained" disabled={loading} onClick={() => void handleGenerateRoadmap()}>
                        {loading ? "Preparing…" : "Set Target & Learn"}
                    </Button>
                </Stack>
            </CardContent>
        </Card>
    );
}
