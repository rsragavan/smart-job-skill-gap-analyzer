import { memo } from "react";
import { Box, Card, CardContent, Typography } from "@mui/material";
import { Bar, BarChart, CartesianGrid, Cell, Line, LineChart, Pie, PieChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import type { AnalyticsDashboard } from "../api/analyticsApi";

const colors = ["#5b7cfa", "#36b37e", "#ffab00", "#ff7452", "#6554c0", "#00b8d9", "#ff8b00", "#00875a"];
const cardSx = { height: "100%", border: "1px solid", borderColor: "divider", borderRadius: 3, boxShadow: 1 };

export default memo(function ProfessionalAnalyticsCharts({ data }: { data: AnalyticsDashboard }) {
    const trend = data.xp_statistics.growth;
    return <Box sx={{ display: "grid", gridTemplateColumns: { xs: "1fr", lg: "repeat(2, minmax(0, 1fr))" }, gap: 2.5 }}>
        <Chart title="Skill Match %"><PieChart><Pie data={data.charts.skill_match} dataKey="value" nameKey="name" innerRadius={55} outerRadius={92}>{data.charts.skill_match.map((item, index) => <Cell key={item.name} fill={colors[index]} />)}</Pie><Tooltip /></PieChart></Chart>
        <Chart title="Learning Progress"><PieChart><Pie data={data.charts.learning_progress} dataKey="value" nameKey="name" innerRadius={55} outerRadius={92}>{data.charts.learning_progress.map((item, index) => <Cell key={item.name} fill={colors[index + 1]} />)}</Pie><Tooltip /></PieChart></Chart>
        <Chart title="XP Growth"><LineChart data={trend}><CartesianGrid strokeDasharray="3 3" /><XAxis dataKey="date" tick={{ fontSize: 11 }} /><YAxis /><Tooltip /><Line type="monotone" dataKey="xp" stroke="#5b7cfa" strokeWidth={3} /></LineChart></Chart>
        <Chart title="Career Readiness"><BarChart data={[{ name: "Career", value: data.career_statistics.readiness }, { name: "Role", value: data.career_statistics.role_readiness }]}><CartesianGrid strokeDasharray="3 3" /><XAxis dataKey="name" /><YAxis domain={[0, 100]} /><Tooltip /><Bar dataKey="value" fill="#36b37e" radius={[5, 5, 0, 0]} /></BarChart></Chart>
        <Chart title="Completed Skills"><BarChart data={data.charts.completed_skills}><CartesianGrid strokeDasharray="3 3" /><XAxis dataKey="name" /><YAxis allowDecimals={false} /><Tooltip /><Bar dataKey="value" fill="#6554c0" /></BarChart></Chart>
        <Chart title="Missing Skills"><BarChart data={data.charts.missing_skills} layout="vertical" margin={{ left: 20 }}><CartesianGrid strokeDasharray="3 3" /><XAxis type="number" /><YAxis dataKey="name" type="category" width={100} tick={{ fontSize: 11 }} /><Tooltip /><Bar dataKey="value" fill="#ff7452" /></BarChart></Chart>
        <Chart title="Projects Completed"><BarChart data={data.charts.projects_completed}><CartesianGrid strokeDasharray="3 3" /><XAxis dataKey="name" /><YAxis allowDecimals={false} /><Tooltip /><Bar dataKey="value" fill="#00b8d9" /></BarChart></Chart>
        <Chart title="Daily Activity"><LineChart data={data.charts.daily_activity}><CartesianGrid strokeDasharray="3 3" /><XAxis dataKey="date" tick={{ fontSize: 10 }} /><YAxis allowDecimals={false} /><Tooltip /><Line type="monotone" dataKey="activity" stroke="#ffab00" strokeWidth={2} /></LineChart></Chart>
        <Chart title="Weekly Activity"><BarChart data={data.charts.weekly_activity}><CartesianGrid strokeDasharray="3 3" /><XAxis dataKey="period" /><YAxis allowDecimals={false} /><Tooltip /><Bar dataKey="activity" fill="#00875a" /></BarChart></Chart>
        <Chart title="Monthly Activity"><BarChart data={data.charts.monthly_activity}><CartesianGrid strokeDasharray="3 3" /><XAxis dataKey="period" /><YAxis allowDecimals={false} /><Tooltip /><Bar dataKey="activity" fill="#5b7cfa" /></BarChart></Chart>
    </Box>;
});

function Chart({ title, children }: { title: string; children: React.ReactElement }) { return <Card elevation={0} sx={cardSx}><CardContent><Typography variant="h6" sx={{ fontWeight: 700 }}>{title}</Typography><Box sx={{ mt: 2, width: "100%", height: 250 }}><ResponsiveContainer>{children}</ResponsiveContainer></Box></CardContent></Card>; }
