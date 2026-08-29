import { useCallback, useEffect, useMemo, useState } from "react";
import {
    Alert,
    Box,
    Button,
    Card,
    CardContent,
    Checkbox,
    Chip,
    CircularProgress,
    Divider,
    LinearProgress,
    List,
    ListItem,
    ListItemText,
    Stack,
    Typography,
} from "@mui/material";
import { Link as RouterLink } from "react-router-dom";

import { getLearningProgress, getLearningResources, syncLearningProgress, updateLearningProgress, type LearningProgress, type LearningProgressItem, type LearningResource } from "../api/learningApi";
import { useWorkflow } from "../contexts/WorkflowContext";
import type { RoadmapSkill, RoadmapTopic } from "../services/roadmapService";

const MISSIONS = [
    ["watch-course", "Watch Course"],
    ["read-documentation", "Read Documentation"],
    ["solve-problems", "Solve Problems"],
    ["complete-quiz", "Complete Quiz"],
    ["build-mini-project", "Build Mini Project"],
] as const;

function slug(value: string) {
    return value.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
}

function topicDetails(topic: RoadmapTopic, index: number) {
    if (typeof topic === "string") return { key: `topic-${index + 1}-${slug(topic)}`, title: topic, description: "" };
    const title = topic.title || topic.name || `Topic ${index + 1}`;
    return { key: `topic-${index + 1}-${slug(title)}`, title, description: topic.description || "" };
}

function projectDetails(project: RoadmapSkill["projects"][number], index: number) {
    const title = typeof project === "string" ? project : project.title || project.name || `Project ${index + 1}`;
    return { key: `project-${index + 1}-${slug(title)}`, title, description: typeof project === "string" ? "" : project.description || "" };
}

function statusLabel(status: LearningProgressItem["status"]) {
    return status === "completed" ? "Completed" : status === "in_progress" ? "In Progress" : "Not Started";
}

export default function LearningDashboard() {
    const { learningPlan, activeTarget } = useWorkflow();
    const [progress, setProgress] = useState<LearningProgress | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [resources, setResources] = useState<LearningResource[]>([]);

    useEffect(() => { void getLearningResources().then(setResources).catch(() => setError("Unable to load learning resources.")); }, []);

    const loadProgress = useCallback(async () => {
        if (!learningPlan) return;
        setLoading(true);
        setError(null);
        try {
            const synced = await syncLearningProgress(learningPlan.roadmap_id, learningPlan.roadmap);
            setProgress(synced);
        } catch (requestError) {
            try {
                setProgress(await getLearningProgress(learningPlan.roadmap_id));
            } catch {
                setError(requestError instanceof Error ? requestError.message : "Unable to load learning progress.");
            }
        } finally {
            setLoading(false);
        }
    }, [learningPlan]);

    useEffect(() => { void loadProgress(); }, [loadProgress]);

    const updateItem = useCallback(async (item: Omit<LearningProgressItem, "xp_earned">) => {
        if (!learningPlan) return;
        try {
            setProgress(await updateLearningProgress(learningPlan.roadmap_id, item));
        } catch (requestError) {
            setError(requestError instanceof Error ? requestError.message : "Unable to save progress.");
        }
    }, [learningPlan]);

    const progressMap = useMemo(() => new Map((progress?.items || []).map((item) => [`${item.skill_key}:${item.item_type}:${item.item_key}`, item])), [progress]);
    const totalTopics = learningPlan?.roadmap.reduce((total, skill) => total + skill.topics.length, 0) || 0;
    const completedTopics = learningPlan?.roadmap.reduce((total, skill) => total + skill.topics.filter((topic, index) => progressMap.get(`${skill.skill_key}:topic:${topicDetails(topic, index).key}`)?.status === "completed").length, 0) || 0;

    if (!learningPlan) {
        return <Alert severity="info" action={<Button component={RouterLink} to="/jobs" color="inherit">Choose Target</Button>}>Select a scraped company or paste a custom job description to start learning.</Alert>;
    }

    if (loading && !progress) {
        return <Box sx={{ display: "grid", placeItems: "center", minHeight: 300 }}><CircularProgress /></Box>;
    }

    return (
        <Stack spacing={3}>
            <Box>
                <Typography variant="h4" sx={{ fontWeight: 700 }}>Learning Dashboard</Typography>
                <Stack direction="row" spacing={1} alignItems="center" sx={{ mt: 0.5 }}>
                    <Typography color="text.secondary">{learningPlan.company} · {learningPlan.role}</Typography>
                    {activeTarget && (
                        <Chip
                            size="small"
                            label={activeTarget.source_type === "scraped" ? "Scraped Company" : "Custom Job Description"}
                        />
                    )}
                </Stack>
            </Box>
            {error && <Alert severity="error" onClose={() => setError(null)}>{error}</Alert>}
            <Card><CardContent><Stack spacing={1.25}>
                <Stack direction="row" sx={{ justifyContent: "space-between", alignItems: "center" }}>
                    <Typography variant="h6">Level {progress?.current_level.level ?? 1} · {progress?.current_level.title ?? "Beginner"}</Typography>
                    <Chip color="primary" label={`${progress?.total_xp ?? 0} XP`} />
                </Stack>
                <LinearProgress variant="determinate" value={totalTopics ? (completedTopics / totalTopics) * 100 : 0} />
                <Typography variant="body2" color="text.secondary">{completedTopics} of {totalTopics} topics completed · {learningPlan.estimated_days} estimated days</Typography>
                {progress?.next_level && <Typography variant="caption" color="text.secondary">Next level: {progress.next_level.title} at {progress.next_level.xp} XP</Typography>}
            </Stack></CardContent></Card>
            {progress?.gamification && <GamificationSummary gamification={progress.gamification} />}
            <Card><CardContent><Typography variant="h5" gutterBottom>Verified learning resources</Typography><Stack spacing={1}>{resources.map((resource) => <Box key={resource.id}><Typography component="a" href={resource.url} target="_blank" rel="noreferrer" fontWeight={700}>{resource.title}</Typography><Typography variant="body2" color="text.secondary">{resource.skill} · {resource.resource_type} · {resource.description}</Typography></Box>)}{!resources.length && <Typography color="text.secondary">No verified learning resources are available yet.</Typography>}</Stack></CardContent></Card>
            {learningPlan.roadmap.map((skill) => <LearningSkillCard key={skill.skill_key} skill={skill} progressMap={progressMap} onUpdate={updateItem} />)}
        </Stack>
    );
}

function GamificationSummary({ gamification }: { gamification: LearningProgress["gamification"] }) {
    const goalValue = (progressValue: number, target: number) => target ? Math.min(100, (progressValue / target) * 100) : 0;
    return <Stack spacing={2}>
        <Stack direction={{ xs: "column", md: "row" }} spacing={2}>
            <Card sx={{ flex: 1 }}><CardContent><Typography variant="h6">Learning Streak</Typography><Typography variant="h3" color="primary">{gamification.current_streak}</Typography><Typography color="text.secondary">days · best {gamification.longest_streak}</Typography></CardContent></Card>
            <Card sx={{ flex: 1 }}><CardContent><Typography variant="h6">Daily Goal</Typography><LinearProgress sx={{ my: 1 }} variant="determinate" value={goalValue(gamification.daily_goal.progress, gamification.daily_goal.target)} color={gamification.daily_goal.completed ? "success" : "primary"} /><Typography color="text.secondary">{gamification.daily_goal.progress} of {gamification.daily_goal.target} completions · +50 XP</Typography></CardContent></Card>
            <Card sx={{ flex: 1 }}><CardContent><Typography variant="h6">Weekly Goal</Typography><LinearProgress sx={{ my: 1 }} variant="determinate" value={goalValue(gamification.weekly_goal.progress, gamification.weekly_goal.target)} color={gamification.weekly_goal.completed ? "success" : "primary"} /><Typography color="text.secondary">{gamification.weekly_goal.progress} of {gamification.weekly_goal.target} completions · +300 XP</Typography></CardContent></Card>
        </Stack>
        <Card><CardContent><Typography variant="h6" gutterBottom>Badges & Achievements</Typography>{gamification.badges.length ? <Stack direction="row" flexWrap="wrap" useFlexGap spacing={1}>{gamification.badges.map((badge) => <Chip key={badge.key} color="secondary" label={badge.name} title={badge.description} />)}</Stack> : <Typography color="text.secondary">Complete learning activities to unlock badges.</Typography>}</CardContent></Card>
    </Stack>;
}

function LearningSkillCard({ skill, progressMap, onUpdate }: { skill: RoadmapSkill; progressMap: Map<string, LearningProgressItem>; onUpdate: (item: Omit<LearningProgressItem, "xp_earned">) => Promise<void> }) {
    const completedTopics = skill.topics.filter((topic, index) => progressMap.get(`${skill.skill_key}:topic:${topicDetails(topic, index).key}`)?.status === "completed").length;
    const topicProgress = skill.topics.length ? (completedTopics / skill.topics.length) * 100 : 0;
    const itemStatus = (type: LearningProgressItem["item_type"], key: string) => progressMap.get(`${skill.skill_key}:${type}:${key}`)?.status || "not_started";

    return <Card><CardContent><Stack spacing={2}>
        <Stack direction={{ xs: "column", sm: "row" }} sx={{ justifyContent: "space-between", gap: 1 }}>
            <Box><Typography variant="h5">{skill.skill}</Typography><Typography color="text.secondary">{skill.difficulty} · {skill.estimated_days} days · {skill.xp} roadmap XP</Typography></Box>
            <Chip label={`${Math.round(topicProgress)}%`} color={topicProgress === 100 ? "success" : "default"} />
        </Stack>
        <LinearProgress variant="determinate" value={topicProgress} />
        <Typography variant="h6">Topics</Typography>
        <List disablePadding>{skill.topics.map((topic, index) => { const details = topicDetails(topic, index); const status = itemStatus("topic", details.key); return <ListItem key={details.key} disableGutters secondaryAction={<Stack direction="row" sx={{ alignItems: "center" }}><Button size="small" onClick={() => void onUpdate({ skill_key: skill.skill_key, item_type: "topic", item_key: details.key, status: status === "not_started" ? "in_progress" : "not_started" })}>{status === "in_progress" ? "Pause" : status === "completed" ? "Review" : "Start"}</Button><Checkbox edge="end" checked={status === "completed"} onChange={(event) => void onUpdate({ skill_key: skill.skill_key, item_type: "topic", item_key: details.key, status: event.target.checked ? "completed" : "not_started" })} /></Stack>}><ListItemText primary={details.title} secondary={`${details.description || "Study this topic and apply it in practice."} · ${statusLabel(status)}`} /></ListItem>; })}</List>
        <Divider />
        <Typography variant="h6">Practice Missions</Typography>
        <Stack direction="row" flexWrap="wrap" useFlexGap spacing={1}>{MISSIONS.map(([key, title]) => { const status = itemStatus("mission", key); return <Button key={key} size="small" variant={status === "completed" ? "contained" : "outlined"} color={status === "completed" ? "success" : "primary"} onClick={() => void onUpdate({ skill_key: skill.skill_key, item_type: "mission", item_key: key, status: status === "completed" ? "not_started" : "completed" })}>{title}</Button>; })}</Stack>
        <Divider />
        <Typography variant="h6">Projects</Typography>
        <Stack spacing={1.25}>{skill.projects.map((project, index) => { const details = projectDetails(project, index); const status = itemStatus("project", details.key); const previous = index > 0 ? projectDetails(skill.projects[index - 1], index - 1) : null; const locked = Boolean(previous && itemStatus("project", previous.key) !== "completed"); const nextStatus = status === "not_started" ? "in_progress" : status === "in_progress" ? "completed" : "not_started"; return <Card key={details.key} variant="outlined"><CardContent><Stack direction={{ xs: "column", sm: "row" }} sx={{ justifyContent: "space-between", gap: 1 }}><Box><Typography fontWeight={700}>{details.title}</Typography><Typography variant="body2" color="text.secondary">{details.description}</Typography></Box><Button disabled={locked} variant={status === "completed" ? "contained" : "outlined"} color={status === "completed" ? "success" : "primary"} onClick={() => void onUpdate({ skill_key: skill.skill_key, item_type: "project", item_key: details.key, status: nextStatus })}>{locked ? "Locked" : status === "completed" ? "Completed" : status === "in_progress" ? "Complete Project" : "Start Project"}</Button></Stack></CardContent></Card>; })}</Stack>
    </Stack></CardContent></Card>;
}
