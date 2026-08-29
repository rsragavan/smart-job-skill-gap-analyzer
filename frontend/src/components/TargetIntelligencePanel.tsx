import { Alert, Chip, Divider, Link, List, ListItem, ListItemText, Paper, Skeleton, Stack, Typography } from "@mui/material";

const missing = (value: unknown) => value === null || value === undefined || value === "" ? "Not Available" : String(value);

export default function TargetIntelligencePanel({ data, loading }: { data: any | null; loading?: boolean }) {
    if (loading) return <Paper sx={{ mt: 4, p: 3 }}><Skeleton variant="text" width="40%" /><Skeleton variant="rounded" height={120} /></Paper>;
    if (!data?.company) return <Paper sx={{ mt: 4, p: 3 }}><Typography variant="h6">Interview Preparation</Typography><Alert severity="info" sx={{ mt: 2 }}>Verified company intelligence is not available for this target.</Alert></Paper>;
    const company = data.company;
    return <Paper sx={{ mt: 4, p: 3 }}>
        <Typography variant="h6">Interview Preparation</Typography>
        <Typography color="text.secondary">{company.name} · {missing(data.role?.title)}</Typography>
        <Stack direction="row" spacing={1} flexWrap="wrap" sx={{ my: 2 }}>{(data.skills || []).map((item: any) => <Chip key={item.skill} label={item.skill} />)}</Stack>
        <Divider />
        <Typography variant="subtitle1" sx={{ mt: 2 }}>Hiring Process</Typography>
        {data.selection_process?.length ? <List dense>{data.selection_process.map((round: any) => <ListItem key={round.id}><ListItemText primary={`${round.round_number}. ${round.title}`} secondary={round.description || round.purpose || "Not Available"} /></ListItem>)}</List> : <Typography color="text.secondary" sx={{ mt: 1 }}>Not Available</Typography>}
        <Typography variant="subtitle1" sx={{ mt: 2 }}>Preparation</Typography>
        {data.preparation?.length ? <List dense>{data.preparation.map((item: any) => <ListItem key={item.id}><ListItemText primary={item.topic} secondary={item.category} /></ListItem>)}</List> : <Typography color="text.secondary" sx={{ mt: 1 }}>Not Available</Typography>}
        <Typography variant="subtitle1" sx={{ mt: 2 }}>Questions and Resources</Typography>
        <Typography color="text.secondary">{data.questions?.length || 0} verified questions · {data.resources?.length || 0} verified resources</Typography>
        {data.resources?.map((resource: any) => <Link key={resource.id} href={resource.url} target="_blank" rel="noreferrer" display="block" sx={{ mt: 1 }}>{resource.title}</Link>)}
    </Paper>;
}
