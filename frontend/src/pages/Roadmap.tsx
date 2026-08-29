import { useLocation, Link as RouterLink } from "react-router-dom";
import {
    Alert,
    Box,
    Button,
    Card,
    CardContent,
    Chip,
    Divider,
    LinearProgress,
    Stack,
    Typography,
    List,
    ListItem,
    ListItemText,
    Link as MuiLink,
} from "@mui/material";
import { useEffect, useState } from "react";

import roadmapService from "../services/roadmapService";
import type { RoadmapResponse } from "../services/roadmapService";
import { useWorkflow } from "../contexts/WorkflowContext";

function textForTopic(topic: string | { title?: string; name?: string; description?: string }) {
    return typeof topic === "string" ? topic : topic.title || topic.name || "Unnamed Topic";
}

function descriptionForTopic(topic: string | { title?: string; name?: string; description?: string }) {
    return typeof topic === "string" ? "" : topic.description || "";
}

export default function Roadmap() {
    const location = useLocation();
    const { learningPlan, setLearningPlan, activeTarget } = useWorkflow();
    const [roadmap, setRoadmap] = useState<RoadmapResponse | null>(learningPlan);
    const [error, setError] = useState<string | null>(null);

    async function loadRoadmap(data: unknown) {
        setError(null);
        try {
            const result = await roadmapService.generate(data);
            setRoadmap(result);
            setLearningPlan(result);
        } catch (requestError) {
            setError(requestError instanceof Error ? requestError.message : "Failed to load roadmap.");
        }
    }

    useEffect(() => {
        if (location.state) {
            const state = location.state as RoadmapResponse;
            if (state?.roadmap_id && state?.roadmap) {
                setRoadmap(state);
                setLearningPlan(state);
                return;
            }
            void loadRoadmap(location.state);
        }
    }, [location.state]);

    useEffect(() => {
        if (!location.state && learningPlan) {
            setRoadmap(learningPlan);
        }
    }, [learningPlan, location.state]);

    if (!roadmap) {
        return (
            <Box display="flex" justifyContent="center" alignItems="center" minHeight="70vh">
                <Stack spacing={2} alignItems="center" sx={{ px: 2, maxWidth: 480, textAlign: "center" }}>
                    <Typography variant="h5" fontWeight={700}>No roadmap yet</Typography>
                    <Typography color="text.secondary">
                        Choose a scraped job or paste a custom job description to generate your plan.
                    </Typography>
                    {error && <Alert severity="error" sx={{ width: "100%" }}>{error}</Alert>}
                    <Button component={RouterLink} to="/jobs" variant="contained">
                        Choose Target
                    </Button>
                </Stack>
            </Box>
        );
    }

    return (
        <Box maxWidth={1200} mx="auto" mt={4} px={2}>
            {error && <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError(null)}>{error}</Alert>}
            <Stack direction="row" spacing={1} alignItems="center" sx={{ mb: 1 }} useFlexGap flexWrap="wrap">
                <Typography variant="h4" fontWeight="bold">
                    {roadmap.company}
                </Typography>
                {activeTarget && (
                    <Chip
                        size="small"
                        label={activeTarget.source_type === "scraped" ? "Scraped Company" : "Custom Job Description"}
                    />
                )}
            </Stack>

            <Typography color="text.secondary" mb={3}>
                {roadmap.role}
            </Typography>

            <Card>
                <CardContent>
                    <Typography variant="h6">Job Match</Typography>
                    <LinearProgress
                        variant="determinate"
                        value={roadmap.match_percentage}
                        sx={{ height: 10, borderRadius: 5, my: 2 }}
                    />
                    <Typography>{roadmap.match_percentage}%</Typography>

                    <Divider sx={{ my: 3 }} />

                    <Stack direction="row" spacing={2} mb={3}>
                        <Chip color="primary" label={`XP ${roadmap.total_xp}`} />
                        <Chip color="secondary" label={roadmap.current_level?.title || "N/A"} />
                        <Chip label={`${roadmap.estimated_days} Days`} />
                    </Stack>
                </CardContent>
            </Card>

            <Box mt={4}>
                {roadmap.roadmap.map((skill) => (
                    <Card key={skill.skill} sx={{ mb: 3 }}>
                        <CardContent>
                            <Stack direction="row" justifyContent="space-between">
                                <Typography variant="h5">
                                    {skill.skill}
                                </Typography>
                                <Chip label={skill.difficulty} />
                            </Stack>

                            <Typography color="text.secondary">
                                Priority {skill.priority} · {skill.category}
                            </Typography>

                            <Typography mt={2}>{skill.description}</Typography>

                            <Stack direction="row" spacing={2} mt={2} flexWrap="wrap" useFlexGap>
                                <Chip label={`XP ${skill.xp}`} color="primary" size="small" />
                                <Chip label={`${skill.estimated_days} days`} size="small" />
                                {skill.dependencies.map((dependency) => <Chip key={dependency} label={`Builds on ${dependency}`} size="small" variant="outlined" />)}
                            </Stack>

                            <Typography mt={2}>
                                Estimated Days: {skill.estimated_days}
                            </Typography>

                            <Divider sx={{ my: 2 }} />

                            <Typography variant="h6">Topics</Typography>
                            <List>
                                {skill.topics.map((topic, index) => (
                                    <ListItem key={index}>
                                        <ListItemText
                                            primary={textForTopic(topic)}
                                            secondary={descriptionForTopic(topic)}
                                        />
                                    </ListItem>
                                ))}
                            </List>

                            <Divider sx={{ my: 2 }} />

                            <Typography variant="h6">Resources</Typography>
                            <List>
                                {skill.resources.map((resource) => (
                                    <ListItem key={`${resource.type}-${resource.title}`}>
                                        <ListItemText
                                            primary={<MuiLink href={resource.url} target="_blank" rel="noopener noreferrer">{resource.title}</MuiLink>}
                                            secondary={resource.type}
                                        />
                                    </ListItem>
                                ))}
                            </List>

                            <Divider sx={{ my: 2 }} />

                            <Typography variant="h6">Projects</Typography>
                            <List>
                                {skill.projects.map((project, index) => (
                                    <ListItem key={index}>
                                        <ListItemText
                                            primary={project.title || project.name || "Unnamed Project"}
                                            secondary={project.description || ""}
                                        />
                                    </ListItem>
                                ))}
                            </List>

                            <Divider sx={{ my: 2 }} />

                            <Typography variant="h6">Milestones</Typography>
                            <List>
                                {skill.milestones.map((milestone) => (
                                    <ListItem key={milestone.title}>
                                        <ListItemText primary={milestone.title} secondary={milestone.description} />
                                    </ListItem>
                                ))}
                            </List>
                        </CardContent>
                    </Card>
                ))}
            </Box>
        </Box>
    );
}
