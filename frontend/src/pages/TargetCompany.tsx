import { useEffect, useState } from "react";
import { Accordion, AccordionDetails, AccordionSummary, Alert, Button, Chip, Container, LinearProgress, Paper, Stack, Typography } from "@mui/material";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import { Link as RouterLink } from "react-router-dom";
import companyService, { type TargetPreparation } from "../services/companyIntelligenceService";
import { useWorkflow } from "../contexts/WorkflowContext";

export default function TargetCompany() {
    const { activeTarget } = useWorkflow();
    const [result, setResult] = useState<TargetPreparation | null>(null);
    const [error, setError] = useState("");

    useEffect(() => {
        if (!activeTarget) { setResult(null); return; }
        void companyService.activeTargetPreparation().then(setResult).catch(() => setError("Target preparation could not be loaded."));
    }, [activeTarget?.id]);

    if (!activeTarget) return <Alert severity="info" action={<Button component={RouterLink} to="/jobs" color="inherit">Choose Target Job</Button>}>Select a scraped job or enter a user-provided job description before opening company preparation.</Alert>;
    if (error) return <Alert severity="error">{error}</Alert>;
    if (!result) return <LinearProgress />;

    return <Container maxWidth="lg" sx={{ py: 4 }}>
        <Typography variant="h4" fontWeight={700}>Target Company</Typography>
        <Typography color="text.secondary" sx={{ mb: 3 }}>Preparation is based on the active Target Job. There is one shared target context across roadmap, coding, interviews, and Career GPS.</Typography>
        <Paper sx={{ p: 3, mb: 3 }}><Typography variant="h5">{result.company}</Typography><Typography variant="h6" sx={{ mt: 1 }}>{result.role} · {result.experience_level === "fresher" ? "Fresher" : result.experience_level}</Typography><Typography color="text.secondary" sx={{ mt: 1 }}>Target Job source: {activeTarget.source_type === "scraped" ? "Scraped Job" : "User-provided Job"}</Typography><Typography color="text.secondary">{result.company_info.industry || "Industry not available"} · {result.company_info.location || "Location not available"}</Typography><Chip label={result.data_status} size="small" sx={{ mt: 1 }} /></Paper>
        <Paper sx={{ p: 3, mb: 3 }}><Typography variant="h6">Preparation Readiness: {result.readiness.overall}%</Typography><LinearProgress variant="determinate" value={result.readiness.overall} sx={{ my: 1, height: 9, borderRadius: 4 }} />{result.readiness.provisional && <Alert severity="info" sx={{ mt: 2 }}>Readiness is provisional because verified company-process evidence is limited.</Alert>}<Stack direction="row" flexWrap="wrap" gap={1} sx={{ mt: 2 }}>{result.readiness.components && Object.entries(result.readiness.components).map(([name, score]) => <Chip key={name} label={`${name}: ${score}%`} />)}</Stack></Paper>
        <Paper sx={{ p: 3, mb: 3 }}><Typography variant="h6">Skill Gap</Typography><Typography sx={{ mt: 1 }}>Matched skills</Typography><Stack direction="row" flexWrap="wrap" gap={1} sx={{ mt: 1 }}>{result.readiness.matched_skills.map(item => <Chip key={item} label={item} color="success" />)}</Stack><Typography sx={{ mt: 2 }}>Missing skills</Typography><Stack direction="row" flexWrap="wrap" gap={1} sx={{ mt: 1 }}>{result.readiness.missing_skills.map(item => <Chip key={item} label={item} color="warning" />)}</Stack></Paper>
        <Typography variant="h5" sx={{ mb: 1 }}>Recommended Preparation Stages</Typography>{result.rounds.map(round => <Accordion key={round.round_number}><AccordionSummary expandIcon={<ExpandMoreIcon />}><Typography fontWeight={700}>Stage {round.round_number} — {round.round_name}</Typography></AccordionSummary><AccordionDetails><Typography>{round.purpose || "Role-based preparation stage."}</Typography><Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>Evidence: {round.source_type}</Typography><Stack direction="row" flexWrap="wrap" gap={1} sx={{ mt: 2 }}>{round.topics.map(topic => <Chip key={topic} label={topic} />)}</Stack></AccordionDetails></Accordion>)}
        <Stack direction={{ xs: "column", sm: "row" }} spacing={2} sx={{ mt: 3 }}><Button component={RouterLink} to="/coding-practice?start=1" variant="contained">Start Coding Assessment</Button><Button component={RouterLink} to="/interviews?experience=fresher" variant="outlined">Start Technical Mock Interview</Button><Button component={RouterLink} to="/interviews?type=hr" variant="outlined">Start HR Interview</Button><Button component={RouterLink} to="/career-gps" variant="outlined">Career GPS</Button></Stack>
    </Container>;
}
