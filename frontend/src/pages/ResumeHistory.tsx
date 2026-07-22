import { useCallback, useEffect, useMemo, useState } from "react";
import type { ReactNode } from "react";
import { useNavigate } from "react-router-dom";
import {
    Alert,
    Box,
    Button,
    Card,
    CardActionArea,
    CardActions,
    CardContent,
    Chip,
    Dialog,
    DialogActions,
    DialogContent,
    DialogTitle,
    Divider,
    Grid,
    InputAdornment,
    LinearProgress,
    MenuItem,
    Skeleton,
    Snackbar,
    Stack,
    TextField,
    Tooltip,
    Typography,
} from "@mui/material";
import ArticleOutlinedIcon from "@mui/icons-material/ArticleOutlined";
import AutoGraphOutlinedIcon from "@mui/icons-material/AutoGraphOutlined";
import CheckCircleOutlineIcon from "@mui/icons-material/CheckCircleOutlined";
import DeleteOutlineIcon from "@mui/icons-material/DeleteOutlined";
import DescriptionOutlinedIcon from "@mui/icons-material/DescriptionOutlined";
import FolderOffOutlinedIcon from "@mui/icons-material/FolderOffOutlined";
import SearchOutlinedIcon from "@mui/icons-material/SearchOutlined";
import SchoolOutlinedIcon from "@mui/icons-material/SchoolOutlined";
import UploadFileOutlinedIcon from "@mui/icons-material/UploadFileOutlined";
import VisibilityOutlinedIcon from "@mui/icons-material/VisibilityOutlined";

import { deleteResumeHistory, getResumeHistory } from "../api/resumeHistoryApi";
import { useWorkflow } from "../contexts/WorkflowContext";

interface ResumeHistoryItem {
    id: number;
    filename: string;
    uploaded_at: string;
    skills?: string[];
    recommended_jobs?: number;
}

type HistoryStatus = "Uploaded" | "Learning" | "Completed";
type StatusFilter = "All" | HistoryStatus;
type SortOption = "newest" | "oldest" | "match";

function formatDate(date: string): string {
    return new Date(date).toLocaleString(undefined, { dateStyle: "medium", timeStyle: "short" });
}

function statusColor(status: HistoryStatus): "default" | "primary" | "success" {
    return status === "Completed" ? "success" : status === "Learning" ? "primary" : "default";
}

export default function ResumeHistory() {
    const navigate = useNavigate();
    const { learningPlan, roadmapProgress } = useWorkflow();
    const [history, setHistory] = useState<ResumeHistoryItem[]>([]);
    const [loading, setLoading] = useState(true);
    const [selected, setSelected] = useState<ResumeHistoryItem | null>(null);
    const [pendingDelete, setPendingDelete] = useState<ResumeHistoryItem | null>(null);
    const [search, setSearch] = useState("");
    const [filter, setFilter] = useState<StatusFilter>("All");
    const [sort, setSort] = useState<SortOption>("newest");
    const [snackbar, setSnackbar] = useState<{ message: string; severity: "success" | "error" } | null>(null);

    const getStatus = useCallback((item: ResumeHistoryItem): HistoryStatus => {
        // The API does not persist roadmap state per resume. The current in-session plan can only
        // be associated with the latest history item; every other stored item remains Uploaded.
        if (item.id !== history[0]?.id || !learningPlan) return "Uploaded";
        return roadmapProgress >= 100 ? "Completed" : "Learning";
    }, [history, learningPlan, roadmapProgress]);

    const loadHistory = useCallback(async () => {
        setLoading(true);
        try {
            setHistory(await getResumeHistory());
        } catch (err: unknown) {
            const message = err instanceof Error ? err.message : "Failed to load resume history";
            setSnackbar({ message, severity: "error" });
        } finally {
            setLoading(false);
        }
    }, []);

    useEffect(() => {
        const loadTimer = window.setTimeout(() => {
            void loadHistory();
        }, 0);

        return () => window.clearTimeout(loadTimer);
    }, [loadHistory]);

    const visibleHistory = useMemo(() => {
        const normalizedSearch = search.trim().toLowerCase();
        return [...history]
            .filter((item) => !normalizedSearch || item.filename.toLowerCase().includes(normalizedSearch))
            .filter((item) => filter === "All" || getStatus(item) === filter)
            .sort((first, second) => {
                if (sort === "oldest") return new Date(first.uploaded_at).getTime() - new Date(second.uploaded_at).getTime();
                if (sort === "match") return 0; // Match percentage is not supplied by the history endpoint.
                return new Date(second.uploaded_at).getTime() - new Date(first.uploaded_at).getTime();
            });
    }, [filter, getStatus, history, search, sort]);

    const statusCounts = useMemo(() => history.reduce<Record<HistoryStatus, number>>((counts, item) => {
        counts[getStatus(item)] += 1;
        return counts;
    }, { Uploaded: 0, Learning: 0, Completed: 0 }), [getStatus, history]);

    const confirmDelete = async () => {
        if (!pendingDelete) return;
        try {
            await deleteResumeHistory(pendingDelete.id);
            setHistory((items) => items.filter((item) => item.id !== pendingDelete.id));
            setSnackbar({ message: "Resume history entry deleted.", severity: "success" });
        } catch (err: unknown) {
            const message = err instanceof Error ? err.message : "Failed to delete the history entry";
            setSnackbar({ message, severity: "error" });
        } finally {
            setPendingDelete(null);
        }
    };

    return (
        <Stack spacing={3}>
            <Box>
                <Typography variant="h4" sx={{ fontWeight: 700 }}>Resume History</Typography>
                <Typography color="text.secondary" sx={{ mt: 0.5 }}>Review your uploaded resumes and continue your career plan.</Typography>
            </Box>

            <Grid container spacing={2}>
                <SummaryCard icon={<DescriptionOutlinedIcon />} label="Total Uploaded Resumes" value={history.length} description="Resumes saved to your history" loading={loading} />
                <SummaryCard icon={<CheckCircleOutlineIcon />} label="Completed Roadmaps" value={statusCounts.Completed} description="Completed in this session" loading={loading} />
                <SummaryCard icon={<SchoolOutlinedIcon />} label="Active Learning Plans" value={statusCounts.Learning} description="Current learning activity" loading={loading} />
                <SummaryCard icon={<AutoGraphOutlinedIcon />} label="Average Match Percentage" value="N/A" description="Match data is not stored in history" loading={loading} />
            </Grid>

            <Card elevation={0} sx={{ border: "1px solid", borderColor: "divider", borderRadius: 3, boxShadow: 1 }}>
                <CardContent>
                    <Stack direction={{ xs: "column", md: "row" }} spacing={1.5}>
                        <TextField
                            fullWidth
                            size="small"
                            label="Search by filename"
                            value={search}
                            onChange={(event) => setSearch(event.target.value)}
                            slotProps={{ input: { startAdornment: <InputAdornment position="start"><SearchOutlinedIcon fontSize="small" /></InputAdornment> } }}
                        />
                        <TextField select size="small" label="Status" value={filter} onChange={(event) => setFilter(event.target.value as StatusFilter)} sx={{ minWidth: { md: 160 } }}>
                            {(["All", "Uploaded", "Learning", "Completed"] as StatusFilter[]).map((option) => <MenuItem key={option} value={option}>{option}</MenuItem>)}
                        </TextField>
                        <TextField select size="small" label="Sort" value={sort} onChange={(event) => setSort(event.target.value as SortOption)} sx={{ minWidth: { md: 180 } }}>
                            <MenuItem value="newest">Newest First</MenuItem>
                            <MenuItem value="oldest">Oldest First</MenuItem>
                            <MenuItem value="match">Highest Match %</MenuItem>
                        </TextField>
                    </Stack>
                    {sort === "match" && <Typography variant="caption" color="text.secondary" sx={{ display: "block", mt: 1 }}>Match percentages are not available from the stored history, so the original order is retained.</Typography>}
                </CardContent>
            </Card>

            {loading ? <HistorySkeletons /> : history.length === 0 ? <EmptyState onUpload={() => navigate("/upload")} /> : visibleHistory.length === 0 ? (
                <Box sx={{ textAlign: "center", py: 7 }}><SearchOutlinedIcon color="disabled" sx={{ fontSize: 42 }} /><Typography variant="h6" sx={{ mt: 1 }}>No matching resume history</Typography><Typography color="text.secondary">Try a different filename or filter.</Typography></Box>
            ) : (
                <Grid container spacing={2.5}>
                    {visibleHistory.map((item) => <Grid key={item.id} size={{ xs: 12, sm: 6, lg: 4 }}><HistoryCard item={item} status={getStatus(item)} roadmapProgress={item.id === history[0]?.id && learningPlan ? roadmapProgress : null} onView={() => setSelected(item)} onRoadmap={() => navigate("/learning")} onDelete={() => setPendingDelete(item)} /></Grid>)}
                </Grid>
            )}

            <DetailsDialog item={selected} status={selected ? getStatus(selected) : "Uploaded"} roadmapProgress={selected?.id === history[0]?.id && learningPlan ? roadmapProgress : null} onClose={() => setSelected(null)} />
            <Dialog open={Boolean(pendingDelete)} onClose={() => setPendingDelete(null)}>
                <DialogTitle>Delete resume history?</DialogTitle>
                <DialogContent><Typography color="text.secondary">This will permanently remove <strong>{pendingDelete?.filename}</strong> from your history.</Typography></DialogContent>
                <DialogActions><Button onClick={() => setPendingDelete(null)}>Cancel</Button><Button color="error" variant="contained" onClick={() => void confirmDelete()}>Delete History</Button></DialogActions>
            </Dialog>
            <Snackbar open={Boolean(snackbar)} autoHideDuration={5000} onClose={() => setSnackbar(null)}><Alert severity={snackbar?.severity} onClose={() => setSnackbar(null)}>{snackbar?.message}</Alert></Snackbar>
        </Stack>
    );
}

function SummaryCard({ icon, label, value, description, loading }: { icon: ReactNode; label: string; value: string | number; description: string; loading: boolean }) {
    return <Grid size={{ xs: 12, sm: 6, lg: 3 }}><Card elevation={0} sx={{ height: "100%", border: "1px solid", borderColor: "divider", borderRadius: 3, boxShadow: 1, transition: "transform 160ms ease, box-shadow 160ms ease", "&:hover": { transform: "translateY(-4px)", boxShadow: 4 } }}><CardContent><Stack direction="row" spacing={1.5} sx={{ alignItems: "center" }}><Box sx={{ display: "grid", placeItems: "center", p: 1, color: "primary.main", bgcolor: "primary.50", borderRadius: 2 }}>{icon}</Box><Typography variant="body2" color="text.secondary">{label}</Typography></Stack>{loading ? <Skeleton width="45%" height={48} /> : <Typography variant="h4" sx={{ mt: 2, fontWeight: 700 }}>{value}</Typography>}<Typography variant="caption" color="text.secondary">{description}</Typography></CardContent></Card></Grid>;
}

function HistoryCard({ item, status, roadmapProgress, onView, onRoadmap, onDelete }: { item: ResumeHistoryItem; status: HistoryStatus; roadmapProgress: number | null; onView: () => void; onRoadmap: () => void; onDelete: () => void }) {
    return <Card elevation={0} sx={{ height: "100%", border: "1px solid", borderColor: "divider", borderRadius: 3, overflow: "hidden", boxShadow: 1, transition: "transform 160ms ease, box-shadow 160ms ease", "&:hover": { transform: "translateY(-4px)", boxShadow: 4 } }}><CardActionArea onClick={onView} sx={{ alignItems: "stretch", height: "calc(100% - 52px)" }}><CardContent><Stack direction="row" spacing={1.5} sx={{ justifyContent: "space-between", alignItems: "flex-start" }}><Stack direction="row" spacing={1.25} sx={{ minWidth: 0 }}><ArticleOutlinedIcon color="primary" /><Box sx={{ minWidth: 0 }}><Tooltip title={item.filename}><Typography noWrap sx={{ fontWeight: 700 }}>{item.filename}</Typography></Tooltip><Typography variant="caption" color="text.secondary">{formatDate(item.uploaded_at)}</Typography></Box></Stack><Chip label={status} color={statusColor(status)} size="small" /></Stack><Divider sx={{ my: 2 }} /><Box sx={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 1.5 }}><Metric label="Extracted skills" value={item.skills?.length ?? 0} /><Metric label="Recommended jobs" value={item.recommended_jobs ?? 0} /><Metric label="Selected job" value="Not stored" /><Metric label="Match percentage" value="N/A" /></Box><Box sx={{ mt: 2.25 }}><Stack direction="row" sx={{ justifyContent: "space-between" }}><Typography variant="body2" color="text.secondary">Roadmap completion</Typography><Typography variant="body2" sx={{ fontWeight: 700 }}>{roadmapProgress === null ? "N/A" : `${roadmapProgress}%`}</Typography></Stack>{roadmapProgress === null ? <Typography variant="caption" color="text.secondary">Not stored with this resume</Typography> : <LinearProgress variant="determinate" value={roadmapProgress} sx={{ height: 7, borderRadius: 4, mt: 0.75 }} />}</Box></CardContent></CardActionArea><CardActions sx={{ px: 2, pb: 1.5, justifyContent: "space-between" }}><Button size="small" startIcon={<VisibilityOutlinedIcon />} onClick={onView}>View Analysis</Button><Stack direction="row"><Tooltip title="View Roadmap"><Button size="small" onClick={onRoadmap}>Roadmap</Button></Tooltip><Tooltip title="Delete History"><Button size="small" color="error" onClick={onDelete} aria-label={`Delete ${item.filename}`}><DeleteOutlineIcon fontSize="small" /></Button></Tooltip></Stack></CardActions></Card>;
}

function Metric({ label, value }: { label: string; value: string | number }) { return <Box sx={{ minWidth: 0 }}><Typography variant="caption" color="text.secondary">{label}</Typography><Typography variant="body2" noWrap sx={{ fontWeight: 600 }}>{value}</Typography></Box>; }

function DetailsDialog({ item, status, roadmapProgress, onClose }: { item: ResumeHistoryItem | null; status: HistoryStatus; roadmapProgress: number | null; onClose: () => void }) {
    return <Dialog open={Boolean(item)} onClose={onClose} maxWidth="sm" fullWidth><DialogTitle>Resume Analysis</DialogTitle><DialogContent dividers>{item && <Stack spacing={2.25}><Box><Typography variant="h6" noWrap title={item.filename}>{item.filename}</Typography><Typography variant="body2" color="text.secondary">Uploaded {formatDate(item.uploaded_at)}</Typography></Box><Chip label={status} color={statusColor(status)} size="small" sx={{ alignSelf: "flex-start" }} /><DetailSkills title="Extracted Skills" skills={item.skills ?? []} color="primary" /><DetailSkills title="Matched Skills" skills={[]} color="success" unavailable /><DetailSkills title="Missing Skills" skills={[]} color="error" unavailable /><Box><Typography variant="subtitle2">Recommended Jobs</Typography><Typography variant="body2" color="text.secondary" sx={{ mt: 0.5 }}>{item.recommended_jobs ?? 0} recommendation{item.recommended_jobs === 1 ? "" : "s"} were generated. Individual job details are not stored in history.</Typography></Box><Box><Typography variant="subtitle2">Selected Job</Typography><Typography variant="body2" color="text.secondary" sx={{ mt: 0.5 }}>Not available in history.</Typography></Box><Box><Stack direction="row" sx={{ justifyContent: "space-between" }}><Typography variant="subtitle2">Roadmap Progress</Typography><Typography variant="body2">{roadmapProgress === null ? "Not available in history" : `${roadmapProgress}%`}</Typography></Stack>{roadmapProgress !== null && <LinearProgress variant="determinate" value={roadmapProgress} sx={{ mt: 1, borderRadius: 4 }} />}</Box></Stack>}</DialogContent><DialogActions><Button onClick={onClose}>Close</Button></DialogActions></Dialog>;
}

function DetailSkills({ title, skills, color, unavailable = false }: { title: string; skills: string[]; color: "primary" | "success" | "error"; unavailable?: boolean }) { return <Box><Typography variant="subtitle2">{title}</Typography>{unavailable ? <Typography variant="body2" color="text.secondary" sx={{ mt: 0.5 }}>Not available in history.</Typography> : skills.length ? <Stack direction="row" useFlexGap spacing={0.75} sx={{ mt: 1, flexWrap: "wrap" }}>{skills.map((skill) => <Chip key={skill} label={skill} color={color} size="small" variant={color === "primary" ? "outlined" : "filled"} />)}</Stack> : <Typography variant="body2" color="text.secondary" sx={{ mt: 0.5 }}>No skills were extracted.</Typography>}</Box>; }

function EmptyState({ onUpload }: { onUpload: () => void }) { return <Card elevation={0} sx={{ border: "1px dashed", borderColor: "divider", borderRadius: 3 }}><CardContent sx={{ py: 7, textAlign: "center" }}><FolderOffOutlinedIcon color="primary" sx={{ fontSize: 52 }} /><Typography variant="h6" sx={{ mt: 1.5, fontWeight: 700 }}>No Resume History Found</Typography><Typography color="text.secondary" sx={{ mt: 0.75 }}>Upload a resume to start tracking skills, job recommendations, and learning plans.</Typography><Button variant="contained" startIcon={<UploadFileOutlinedIcon />} onClick={onUpload} sx={{ mt: 2.5 }}>Upload Resume</Button></CardContent></Card>; }

function HistorySkeletons() { return <Grid container spacing={2.5}>{Array.from({ length: 6 }, (_, index) => <Grid key={index} size={{ xs: 12, sm: 6, lg: 4 }}><Skeleton variant="rounded" height={300} /></Grid>)}</Grid>; }
