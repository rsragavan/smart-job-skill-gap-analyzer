import { useEffect, useState } from "react";
import { Link as RouterLink, useSearchParams } from "react-router-dom";
import axios from "axios";
import { Alert, Button, Card, CardContent, Chip, CircularProgress, Container, MenuItem, Paper, Select, Stack, Step, StepLabel, Stepper, Tab, Tabs, TextField, Typography } from "@mui/material";
import { answerInterviewQuestion, completeInterview, getInterviewHistory, startInterview, type MockInterview as Interview } from "../api/mockInterviewApi";
import { getActiveTarget } from "../api/targetApi";
import type { ActiveTarget } from "../types/target";

const types = ["technical", "hr", "behavioral", "situational", "communication", "system-design", "frontend", "backend", "database", "cloud"];

const apiErrorMessage = (err: unknown, fallback: string) => {
  if (axios.isAxiosError(err)) {
    const detail = err.response?.data?.detail;
    if (typeof detail === "string") return detail;
    if (Array.isArray(detail) && detail.length) return "Please check the interview options and try again.";
  }
  return err instanceof Error && !err.message.startsWith("Request failed") ? err.message : fallback;
};

export default function MockInterview() {
  const [searchParams] = useSearchParams();
  const [tab, setTab] = useState(0);
  const [type, setType] = useState(searchParams.get("type") === "hr" ? "hr" : "technical");
  const [level, setLevel] = useState(searchParams.get("experience") || "fresher");
  const [interview, setInterview] = useState<Interview | null>(null);
  const [activeTarget, setActiveTarget] = useState<ActiveTarget | null>(null);
  const [answers, setAnswers] = useState<Record<number, string>>({});
  const [history, setHistory] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    void getInterviewHistory().then(setHistory).catch(() => setError("Interview history could not be loaded."));
    void getActiveTarget().then(setActiveTarget).catch(() => undefined);
  }, []);

  const start = async () => {
    setLoading(true);
    setError("");
    try {
      setInterview(await startInterview({ interview_type: type, experience_level: level }));
      setAnswers({});
    } catch (err) {
      setError(apiErrorMessage(err, "No verified questions are available for this interview."));
    } finally {
      setLoading(false);
    }
  };

  const saveAnswer = async (questionId: number) => {
    if (!interview || !answers[questionId]?.trim()) return;
    try {
      setInterview(await answerInterviewQuestion(interview.id, questionId, answers[questionId]));
    } catch (err) {
      setError(apiErrorMessage(err, "Answer could not be saved."));
    }
  };

  const finish = async () => {
    if (!interview) return;
    try {
      setInterview(await completeInterview(interview.id));
      setHistory(await getInterviewHistory());
    } catch (err) {
      setError(apiErrorMessage(err, "Interview could not be completed."));
    }
  };

  return <Container maxWidth="lg" sx={{ py: 4 }}>
    <Typography variant="h4" fontWeight={700}>Mock Interview</Typography>
    <Typography color="text.secondary" sx={{ mb: 2 }}>Questions use the active Target Job and verified question bank. Coding problems open in the dedicated practice IDE.</Typography>
    {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
    {loading && <Alert severity="info" sx={{ mb: 2 }}>Loading interview...</Alert>}
    <Tabs value={tab} onChange={(_, value) => setTab(value)} sx={{ mb: 3 }}><Tab label="Mock Interview" /><Tab label="History" /></Tabs>
    {tab === 0 && <Stack spacing={3}>
      <Paper sx={{ p: 3 }}>
        <Stack spacing={2}>
          <Typography variant="subtitle1" fontWeight={700}>Target: {activeTarget ? `${activeTarget.role_title} at ${activeTarget.company}` : "No active target selected"}</Typography>
          <Stack direction={{ xs: "column", sm: "row" }} spacing={2}>
            <Select value={type} onChange={event => setType(event.target.value)}>{types.map(item => <MenuItem key={item} value={item}>{item.replace("-", " ")}</MenuItem>)}</Select>
            <Select value={level} onChange={event => setLevel(event.target.value)}>
              <MenuItem value="fresher">Fresher</MenuItem>
              <MenuItem value="entry">Entry level</MenuItem>
              <MenuItem value="intermediate">Intermediate</MenuItem>
              <MenuItem value="advanced">Advanced</MenuItem>
              <MenuItem value="mid">Mid level</MenuItem>
              <MenuItem value="senior">Senior level</MenuItem>
            </Select>
            <Button variant="contained" onClick={() => void start()} disabled={loading}>{loading ? <CircularProgress size={20} /> : "Start Interview"}</Button>
            <Button component={RouterLink} to="/coding-practice" variant="outlined">Open Coding Practice</Button>
          </Stack>
        </Stack>
        <Typography variant="body2" color="text.secondary" sx={{ mt: 2 }}>Change the shared target context from the Jobs page when preparing for another role.</Typography>
      </Paper>
      {interview && <Paper sx={{ p: 3 }}>
        <Typography variant="h6">{interview.company_name || "Target company"} - {interview.role_title || "Target role"}</Typography>
        <Stepper activeStep={interview.status === "completed" ? interview.questions.length : Math.max(0, interview.questions.filter(item => item.answer).length)} sx={{ my: 3 }} alternativeLabel>{interview.questions.map(question => <Step key={question.id}><StepLabel>{question.category}</StepLabel></Step>)}</Stepper>
        <Stack spacing={2}>{interview.questions.map(question => <Card key={question.id} variant="outlined"><CardContent>
          <Typography variant="body2" color="text.secondary">Question {question.sequence} of {interview.questions.length}</Typography>
          <Typography fontWeight={700}>{question.question}</Typography>
          {question.recommendation_reason && <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>Why this question: {question.recommendation_reason}</Typography>}
          <Stack direction="row" spacing={1} sx={{ mt: 1 }} flexWrap="wrap" useFlexGap>
            {question.source_type && <Chip size="small" label={question.source_type} />}
            {question.topic && <Chip size="small" label={`Topic: ${question.topic}`} variant="outlined" />}
            {question.difficulty && <Chip size="small" label={question.difficulty} variant="outlined" />}
            {question.skill && <Chip size="small" label={question.skill} variant="outlined" />}
          </Stack>
          <TextField fullWidth multiline minRows={3} sx={{ mt: 2 }} label="Your answer" value={answers[question.id] ?? question.answer ?? ""} onChange={event => setAnswers(current => ({ ...current, [question.id]: event.target.value }))} />
          <Button size="small" sx={{ mt: 1 }} onClick={() => void saveAnswer(question.id)}>Save answer</Button>
          {question.score != null && <Chip size="small" label={`${question.score}/100`} color={question.score >= 70 ? "success" : "warning"} sx={{ ml: 1 }} />}
          {question.feedback && <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>{question.feedback}</Typography>}
        </CardContent></Card>)}</Stack>
        <Button variant="contained" sx={{ mt: 3 }} onClick={() => void finish()} disabled={interview.status === "completed"}>Complete Interview</Button>
        {interview.status === "completed" && <Alert severity="success" sx={{ mt: 2 }}>
          <Typography fontWeight={700}>Interview Completed</Typography>
          <Typography>Score: {interview.feedback?.overall_score ?? "Not Available"}%</Typography>
          <Typography>Questions: {interview.questions.length}</Typography>
          <Typography>Answered: {interview.questions.filter(item => item.answer).length}</Typography>
          <Typography>Strong Areas: {interview.feedback?.strengths?.length ? interview.feedback.strengths.join(", ") : "Not Available"}</Typography>
          <Typography>Areas to Improve: {interview.feedback?.weaknesses?.length ? interview.feedback.weaknesses.join(", ") : "Not Available"}</Typography>
          {interview.feedback?.next_steps?.length ? <Typography>Learning Recommendation: {interview.feedback.next_steps.join(" ")}</Typography> : null}
        </Alert>}
      </Paper>}
    </Stack>}
    {tab === 1 && <Stack spacing={2}>{history.map(item => <Card key={item.id}><CardContent><Typography variant="h6">{item.company_name || "Company not specified"} - {item.role_title || "Role not specified"}</Typography><Typography color="text.secondary">{item.interview_type} - {item.status} - {item.overall_score == null ? "Score not available" : `${item.overall_score}/100`}</Typography></CardContent></Card>)}{!history.length && <Alert severity="info">No mock interviews completed yet. Start with the interview tab.</Alert>}</Stack>}
  </Container>;
}
