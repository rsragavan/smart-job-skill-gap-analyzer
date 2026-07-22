import { memo } from "react";
import type { ReactElement, ReactNode } from "react";
import { Box, Card, CardContent, CircularProgress, Stack, Typography } from "@mui/material";
import { Bar, BarChart, CartesianGrid, Cell, Line, LineChart, Pie, PieChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

const COLORS = ["#5b7cfa", "#36b37e", "#ffab00", "#ff7452", "#6554c0", "#00b8d9", "#ff8b00", "#00875a"];
const cardSx = { height: "100%", border: "1px solid", borderColor: "divider", borderRadius: 3, boxShadow: 1 };

interface ChartDatum { name: string; count: number; }
interface Props { skills: ChartDatum[]; companies: ChartDatum[]; roadmapProgress: number | null; }

export default memo(function AnalyticsCharts({ skills, companies, roadmapProgress }: Props) {
    return <Box sx={{ display: "grid", gridTemplateColumns: { xs: "1fr", lg: "repeat(2, minmax(0, 1fr))" }, gap: 2.5 }}>
        <ChartCard title="Top Required Skills"><ChartArea><BarChart data={skills.slice(0, 8)} layout="vertical" margin={{ left: 18 }}><CartesianGrid strokeDasharray="3 3" /><XAxis type="number" allowDecimals={false} /><YAxis dataKey="name" type="category" width={110} tick={{ fontSize: 12 }} /><Tooltip /><Bar dataKey="count" fill="#5b7cfa" radius={[0, 4, 4, 0]} /></BarChart></ChartArea></ChartCard>
        <ChartCard title="Top Companies"><ChartArea><BarChart data={companies.slice(0, 8)}><CartesianGrid strokeDasharray="3 3" /><XAxis dataKey="name" tick={{ fontSize: 11 }} interval={0} angle={-25} textAnchor="end" height={62} /><YAxis allowDecimals={false} /><Tooltip /><Bar dataKey="count" fill="#36b37e" radius={[4, 4, 0, 0]} /></BarChart></ChartArea></ChartCard>
        <UnavailableChart title="Resume Match Distribution" message="The overview provides one average match value, not a distribution." />
        <ChartCard title="Most Common Skills"><ChartArea><PieChart><Pie data={skills.slice(0, 8)} dataKey="count" nameKey="name" innerRadius={52} outerRadius={92} paddingAngle={3}>{skills.slice(0, 8).map((skill, index) => <Cell key={skill.name} fill={COLORS[index % COLORS.length]} />)}</Pie><Tooltip /></PieChart></ChartArea></ChartCard>
        <ChartCard title="Roadmap Progress"><Box sx={{ height: 250, display: "grid", placeItems: "center" }}>{roadmapProgress === null ? <Typography color="text.secondary">No active roadmap progress.</Typography> : <Box sx={{ position: "relative", display: "inline-flex" }}><CircularProgress variant="determinate" value={roadmapProgress} size={150} thickness={4} /><Box sx={{ position: "absolute", inset: 0, display: "grid", placeItems: "center" }}><Typography variant="h5" sx={{ fontWeight: 700 }}>{roadmapProgress}%</Typography></Box></Box>}</Box></ChartCard>
        <ChartCard title="Skills Frequency"><ChartArea><LineChart data={skills.slice(0, 12)}><CartesianGrid strokeDasharray="3 3" /><XAxis dataKey="name" tick={{ fontSize: 11 }} interval={0} angle={-25} textAnchor="end" height={62} /><YAxis allowDecimals={false} /><Tooltip /><Line type="monotone" dataKey="count" stroke="#6554c0" strokeWidth={3} dot={{ r: 3 }} /></LineChart></ChartArea></ChartCard>
    </Box>;
});

function ChartCard({ title, children }: { title: string; children: ReactNode }) { return <Card elevation={0} sx={cardSx}><CardContent><Typography variant="h6" sx={{ fontWeight: 700 }}>{title}</Typography><Box sx={{ mt: 2 }}>{children}</Box></CardContent></Card>; }
function ChartArea({ children }: { children: ReactElement }) { return <Box sx={{ width: "100%", height: 250 }}><ResponsiveContainer width="100%" height="100%">{children}</ResponsiveContainer></Box>; }
function UnavailableChart({ title, message }: { title: string; message: string }) { return <ChartCard title={title}><Stack sx={{ height: 250, justifyContent: "center", alignItems: "center", textAlign: "center" }}><Typography color="text.secondary">{message}</Typography></Stack></ChartCard>; }
