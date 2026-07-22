import { useEffect, useMemo, useRef, useState } from "react";
import {
    Alert,
    Box,
    Button,
    Card,
    CardContent,
    Chip,
    Divider,
    LinearProgress,
    Skeleton,
    Slider,
    Snackbar,
    Stack,
    Typography,
} from "@mui/material";
import CheckCircleIcon from "@mui/icons-material/CheckCircle";
import DownloadOutlinedIcon from "@mui/icons-material/DownloadOutlined";
import HourglassTopIcon from "@mui/icons-material/HourglassTop";
import LockOutlinedIcon from "@mui/icons-material/LockOutlined";
import MenuBookOutlinedIcon from "@mui/icons-material/MenuBookOutlined";
import NavigateNextIcon from "@mui/icons-material/NavigateNext";
import SaveOutlinedIcon from "@mui/icons-material/SaveOutlined";
import SchoolOutlinedIcon from "@mui/icons-material/SchoolOutlined";
import YouTubeIcon from "@mui/icons-material/YouTube";

import { generateRoadmap } from "../api/learningApi";
import { getResumeHistory } from "../api/resumeHistoryApi";
import { useWorkflow } from "../contexts/WorkflowContext";
import type { LearningResponse, RoadmapItem } from "../types/learning";

interface ResumeHistoryItem {
    id: number;
}

function calculateProgress(items: RoadmapItem[], progress: Record<string, number>): number {
    if (!items.length) return 100;

    return Math.round(items.reduce((total, item) => total + (progress[item.skill] ?? 0), 0) / items.length);
}

function getEstimatedFinishDate(items: RoadmapItem[], progress: Record<string, number>): string {
    const remainingDays = items.reduce((total, item) => {
        return total + (item.estimated_days * (100 - (progress[item.skill] ?? 0))) / 100;
    }, 0);
    const finishDate = new Date();
    finishDate.setDate(finishDate.getDate() + Math.ceil(remainingDays));
    return finishDate.toLocaleDateString();
}

export default function LearningRoadmap() {
    const { learningPlan, selectedJob, setLearningPlan, setRoadmapProgress } = useWorkflow();
    const [loading, setLoading] = useState(false);
    const [resumeAvailable, setResumeAvailable] = useState<boolean | null>(null);
    const [progress, setProgress] = useState<Record<string, number>>({});
    const [activeSkillIndex, setActiveSkillIndex] = useState(0);
    const [snackbarOpen, setSnackbarOpen] = useState(false);
    const [snackbarMsg, setSnackbarMsg] = useState("");
    const [snackbarSeverity, setSnackbarSeverity] = useState<"success" | "error" | "info">("info");
    const requestedJobId = useRef<number | null>(null);

    const roadmapItems = useMemo(() => (
        (learningPlan?.learning_roadmap ?? []).filter((item) => learningPlan?.missing_skills.includes(item.skill))
    ), [learningPlan]);
    const completedSkills = roadmapItems.filter((item) => (progress[item.skill] ?? 0) === 100).length;
    const roadmapPercentage = calculateProgress(roadmapItems, progress);
    const activeItem = roadmapItems[activeSkillIndex] ?? roadmapItems[0];

    useEffect(() => {
        const loadResumeAvailability = async () => {
            try {
                const history: ResumeHistoryItem[] = await getResumeHistory();
                setResumeAvailable(history.length > 0);
            } catch {
                setResumeAvailable(false);
            }
        };

        void loadResumeAvailability();
    }, []);

    const generatePlan = async (jobId: number) => {
        setLoading(true);
        try {
            const plan: LearningResponse = await generateRoadmap(jobId);
            setLearningPlan(plan);
            setSnackbarMsg("Roadmap generated successfully");
            setSnackbarSeverity("success");
            setSnackbarOpen(true);
        } catch (err: unknown) {
            const message = err instanceof Error ? err.message : String(err);
            setSnackbarMsg(message || "Failed to generate roadmap");
            setSnackbarSeverity("error");
            setSnackbarOpen(true);
            requestedJobId.current = null;
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        if (!selectedJob || !resumeAvailable || learningPlan || requestedJobId.current === selectedJob.id) return;

        requestedJobId.current = selectedJob.id;
        void generatePlan(selectedJob.id);
    }, [learningPlan, resumeAvailable, selectedJob]);

    useEffect(() => {
        if (!learningPlan || !selectedJob) return;

        const storageKey = `roadmap_progress_${selectedJob.id}`;
        let storedProgress: Record<string, number> = {};
        try {
            const storedValue = localStorage.getItem(storageKey);
            storedProgress = storedValue ? JSON.parse(storedValue) : {};
        } catch {
            localStorage.removeItem(storageKey);
        }

        const nextProgress = roadmapItems.reduce<Record<string, number>>((values, item) => {
            values[item.skill] = storedProgress[item.skill] ?? 0;
            return values;
        }, {});
        setProgress(nextProgress);
        setRoadmapProgress(calculateProgress(roadmapItems, nextProgress));
        const firstIncompleteIndex = roadmapItems.findIndex((item) => nextProgress[item.skill] < 100);
        setActiveSkillIndex(firstIncompleteIndex === -1 ? 0 : firstIncompleteIndex);
    }, [learningPlan, selectedJob, roadmapItems, setRoadmapProgress]);

    const updateProgress = (skill: string, value: number | number[]) => {
        const skillProgress = Array.isArray(value) ? value[0] : value;
        const nextProgress = { ...progress, [skill]: skillProgress };
        setProgress(nextProgress);
        setRoadmapProgress(calculateProgress(roadmapItems, nextProgress));
        if (selectedJob) localStorage.setItem(`roadmap_progress_${selectedJob.id}`, JSON.stringify(nextProgress));
    };

    const saveProgress = () => {
        if (selectedJob) localStorage.setItem(`roadmap_progress_${selectedJob.id}`, JSON.stringify(progress));
        setSnackbarMsg("Progress saved");
        setSnackbarSeverity("success");
        setSnackbarOpen(true);
    };

    const downloadRoadmap = () => {
        if (!learningPlan || !selectedJob) return;
        const content = [
            `Learning Roadmap: ${selectedJob.title} at ${selectedJob.company}`,
            `Match percentage: ${learningPlan.match_percentage}%`,
            "",
            ...roadmapItems.map((item, index) => `${index + 1}. ${item.skill} — ${item.estimated_days} days — ${progress[item.skill] ?? 0}% complete`),
        ].join("\n");
        const url = URL.createObjectURL(new Blob([content], { type: "text/plain" }));
        const anchor = document.createElement("a");
        anchor.href = url;
        anchor.download = "learning-roadmap.txt";
        anchor.click();
        URL.revokeObjectURL(url);
    };

    const moveToNextSkill = () => {
        const nextIndex = roadmapItems.findIndex((item, index) => index > activeSkillIndex && (progress[item.skill] ?? 0) < 100);
        setActiveSkillIndex(nextIndex === -1 ? activeSkillIndex : nextIndex);
    };

    if (!selectedJob) {
        return <EmptyState message="Select a job from the Jobs page to generate your roadmap." />;
    }

    if (resumeAvailable === false) {
        return <EmptyState message="Upload a resume before generating a learning roadmap." />;
    }

    return (
        <Stack spacing={3} sx={{ p: { xs: 0, sm: 1 } }}>
            <Box>
                <Typography variant="h4" sx={{ fontWeight: 700 }}>Your Learning Roadmap</Typography>
                <Typography color="text.secondary" sx={{ mt: 0.5 }}>A focused plan to close the skills gap for your selected role.</Typography>
            </Box>

            <Card elevation={0} sx={{ border: "1px solid", borderColor: "divider", boxShadow: 2 }}>
                <CardContent sx={{ p: { xs: 2.5, sm: 3 } }}>
                    <Stack direction={{ xs: "column", md: "row" }} spacing={2} sx={{ justifyContent: "space-between" }}>
                        <Box>
                            <Typography variant="overline" color="primary">Selected Job</Typography>
                            <Typography variant="h5" sx={{ fontWeight: 700 }}>{selectedJob.title}</Typography>
                            <Typography color="text.secondary">{selectedJob.company} · {selectedJob.location}</Typography>
                        </Box>
                        <Box sx={{ minWidth: 150, textAlign: { xs: "left", md: "right" } }}>
                            <Typography variant="overline" color="text.secondary">Match Percentage</Typography>
                            {learningPlan ? <Typography variant="h4" color="primary" sx={{ fontWeight: 700 }}>{learningPlan.match_percentage}%</Typography> : <Skeleton width={100} height={48} />}
                        </Box>
                    </Stack>
                    {learningPlan ? (
                        <>
                            <Divider sx={{ my: 2.5 }} />
                            <Typography variant="subtitle2" color="text.secondary">Matched Skills</Typography>
                            <Stack direction="row" spacing={1} useFlexGap sx={{ mt: 1, flexWrap: "wrap" }}>
                                {learningPlan.matched_skills.map((skill) => <Chip key={skill} label={skill} color="success" size="small" />)}
                            </Stack>
                            <Typography variant="subtitle2" color="text.secondary" sx={{ mt: 2 }}>Missing Skills · {learningPlan.total_missing_skills}</Typography>
                            <Stack direction="row" spacing={1} useFlexGap sx={{ mt: 1, flexWrap: "wrap" }}>
                                {learningPlan.missing_skills.map((skill) => <Chip key={skill} label={skill} color="error" variant="outlined" size="small" />)}
                            </Stack>
                        </>
                    ) : <Skeleton sx={{ mt: 3 }} height={88} />}
                </CardContent>
            </Card>

            {loading && <RoadmapSkeletons />}

            {!loading && learningPlan?.total_missing_skills === 0 && (
                <Alert severity="success">Your resume already matches this job. No additional learning required.</Alert>
            )}

            {!loading && roadmapItems.length > 0 && activeItem && (
                <>
                    <Box sx={{ display: "grid", gridTemplateColumns: { xs: "1fr", lg: "minmax(300px, 0.85fr) minmax(0, 1.15fr)" }, gap: 3 }}>
                        <Card elevation={0} sx={{ border: "1px solid", borderColor: "divider", boxShadow: 1 }}>
                            <CardContent>
                                <Typography variant="h6" sx={{ fontWeight: 700 }}>Learning Timeline</Typography>
                                <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>Follow one skill at a time.</Typography>
                                <Stack spacing={0}>
                                    {roadmapItems.map((item, index) => {
                                        const itemProgress = progress[item.skill] ?? 0;
                                        const isCompleted = itemProgress === 100;
                                        const isCurrent = index === activeSkillIndex;
                                        const statusIcon = isCompleted ? <CheckCircleIcon color="success" /> : isCurrent ? <HourglassTopIcon color="primary" /> : <LockOutlinedIcon color="disabled" />;
                                        const statusLabel = isCompleted ? "Completed" : isCurrent ? "Current" : "Locked";
                                        return (
                                            <Box key={item.skill} sx={{ display: "grid", gridTemplateColumns: "36px 1fr", gap: 1.5, minHeight: 86 }}>
                                                <Box sx={{ display: "flex", flexDirection: "column", alignItems: "center" }}>
                                                    {statusIcon}
                                                    {index < roadmapItems.length - 1 && <Box sx={{ width: 2, flexGrow: 1, bgcolor: "divider", my: 0.5 }} />}
                                                </Box>
                                                <Box sx={{ pb: 2, cursor: "pointer" }} onClick={() => setActiveSkillIndex(index)}>
                                                    <Stack direction="row" spacing={1} sx={{ justifyContent: "space-between" }}>
                                                        <Typography sx={{ fontWeight: isCurrent ? 700 : 500 }}>Step {index + 1}: {item.skill}</Typography>
                                                        <Chip label={statusLabel} size="small" color={isCompleted ? "success" : isCurrent ? "primary" : "default"} />
                                                    </Stack>
                                                    <Typography variant="caption" color="text.secondary">{item.difficulty} · {item.estimated_days} days</Typography>
                                                </Box>
                                            </Box>
                                        );
                                    })}
                                </Stack>
                            </CardContent>
                        </Card>

                        <Card elevation={0} sx={{ border: "1px solid", borderColor: "divider", boxShadow: 2 }}>
                            <CardContent sx={{ p: { xs: 2.5, sm: 3 } }}>
                                <Stack direction="row" spacing={2} sx={{ justifyContent: "space-between", alignItems: "flex-start" }}>
                                    <Box>
                                        <Typography variant="overline" color="primary">Current Learning Step</Typography>
                                        <Typography variant="h5" sx={{ fontWeight: 700 }}>{activeItem.skill}</Typography>
                                    </Box>
                                    <Chip label={activeItem.difficulty} color="primary" />
                                </Stack>
                                <Typography color="text.secondary" sx={{ mt: 1 }}>Estimated learning time: {activeItem.estimated_days} days</Typography>
                                <Divider sx={{ my: 2.5 }} />
                                <Typography variant="subtitle2">Key Topics</Typography>
                                <Stack direction="row" spacing={1} useFlexGap sx={{ mt: 1, flexWrap: "wrap" }}>
                                    {activeItem.topics.map((topic) => <Chip key={topic} label={topic} size="small" variant="outlined" />)}
                                </Stack>
                                <Typography variant="subtitle2" sx={{ mt: 2.5 }}>Practice Project</Typography>
                                <Typography variant="body2" color="text.secondary" sx={{ mt: 0.5 }}>
                                    Build a small project that applies {activeItem.skill} to a job-relevant use case.
                                </Typography>
                                <Typography variant="subtitle2" sx={{ mt: 2.5 }}>Learning Resources</Typography>
                                <Stack direction={{ xs: "column", sm: "row" }} spacing={1} sx={{ mt: 1 }}>
                                    <Button size="small" startIcon={<MenuBookOutlinedIcon />} href={activeItem.learning_resource} target="_blank" rel="noreferrer">Official Docs</Button>
                                    <Button size="small" startIcon={<YouTubeIcon />} href={`https://www.youtube.com/results?search_query=${encodeURIComponent(`${activeItem.skill} tutorial`)}`} target="_blank" rel="noreferrer">YouTube</Button>
                                </Stack>
                                <Box sx={{ mt: 3 }}>
                                    <Stack direction="row" sx={{ justifyContent: "space-between" }}><Typography variant="subtitle2">Skill Progress</Typography><Typography variant="body2">{progress[activeItem.skill] ?? 0}%</Typography></Stack>
                                    <Slider value={progress[activeItem.skill] ?? 0} onChange={(_, value) => updateProgress(activeItem.skill, value)} valueLabelDisplay="auto" />
                                    <Button size="small" onClick={() => updateProgress(activeItem.skill, 100)}>Mark Complete</Button>
                                </Box>
                            </CardContent>
                        </Card>
                    </Box>

                    <Card elevation={0} sx={{ border: "1px solid", borderColor: "divider", boxShadow: 1 }}>
                        <CardContent sx={{ p: { xs: 2.5, sm: 3 } }}>
                            <Stack direction={{ xs: "column", md: "row" }} spacing={2} sx={{ justifyContent: "space-between", alignItems: { md: "center" } }}>
                                <Box><Typography variant="h6" sx={{ fontWeight: 700 }}>Progress Dashboard</Typography><Typography variant="body2" color="text.secondary">Keep momentum with a clear view of your plan.</Typography></Box>
                                <Typography variant="h4" color="primary" sx={{ fontWeight: 700 }}>{roadmapPercentage}%</Typography>
                            </Stack>
                            <LinearProgress variant="determinate" value={roadmapPercentage} sx={{ height: 10, borderRadius: 5, mt: 2.5 }} />
                            <Box sx={{ display: "grid", gridTemplateColumns: { xs: "1fr 1fr", sm: "repeat(3, 1fr)" }, gap: 2, mt: 2.5 }}>
                                <Metric label="Completed Skills" value={`${completedSkills}/${roadmapItems.length}`} />
                                <Metric label="Remaining Skills" value={String(roadmapItems.length - completedSkills)} />
                                <Metric label="Estimated Finish" value={getEstimatedFinishDate(roadmapItems, progress)} />
                            </Box>
                        </CardContent>
                    </Card>

                    <Card elevation={0} sx={{ border: "1px solid", borderColor: "divider", boxShadow: 1 }}>
                        <CardContent>
                            <Typography variant="h6" sx={{ fontWeight: 700 }}>Quick Actions</Typography>
                            <Stack direction={{ xs: "column", sm: "row" }} spacing={1} useFlexGap sx={{ mt: 2, flexWrap: "wrap" }}>
                                <Button variant="outlined" startIcon={<DownloadOutlinedIcon />} onClick={downloadRoadmap}>Download Roadmap</Button>
                                <Button variant="outlined" startIcon={<MenuBookOutlinedIcon />} href={activeItem.learning_resource} target="_blank" rel="noreferrer">Open Documentation</Button>
                                <Button variant="outlined" startIcon={<SaveOutlinedIcon />} onClick={saveProgress}>Save Progress</Button>
                                <Button variant="contained" endIcon={<NavigateNextIcon />} onClick={moveToNextSkill}>Next Skill</Button>
                            </Stack>
                        </CardContent>
                    </Card>
                </>
            )}

            {!loading && !learningPlan && resumeAvailable && <Button variant="contained" startIcon={<SchoolOutlinedIcon />} onClick={() => selectedJob && void generatePlan(selectedJob.id)}>Generate Roadmap</Button>}

            <Snackbar open={snackbarOpen} autoHideDuration={5000} onClose={() => setSnackbarOpen(false)}>
                <Alert severity={snackbarSeverity} onClose={() => setSnackbarOpen(false)}>{snackbarMsg}</Alert>
            </Snackbar>
        </Stack>
    );
}

function Metric({ label, value }: { label: string; value: string }) {
    return <Box><Typography variant="caption" color="text.secondary">{label}</Typography><Typography sx={{ fontWeight: 700 }}>{value}</Typography></Box>;
}

function EmptyState({ message }: { message: string }) {
    return (
        <Box sx={{ p: 4, textAlign: "center" }}>
            <SchoolOutlinedIcon color="primary" sx={{ fontSize: 42 }} />
            <Typography variant="h5" sx={{ mt: 1 }}>Learning Roadmap</Typography>
            <Typography color="text.secondary" sx={{ mt: 1 }}>{message}</Typography>
        </Box>
    );
}

function RoadmapSkeletons() {
    return (
        <Box sx={{ display: "grid", gridTemplateColumns: { xs: "1fr", lg: "0.85fr 1.15fr" }, gap: 3 }}>
            <Skeleton variant="rounded" height={420} />
            <Skeleton variant="rounded" height={420} />
        </Box>
    );
}
