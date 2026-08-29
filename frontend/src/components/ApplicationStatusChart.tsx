import {
    PieChart,
    Pie,
    Cell,
    Tooltip,
    ResponsiveContainer,
    Legend,
} from "recharts";

interface Props {
    applied: number;
    reviewing: number;
    shortlisted: number;
    interview: number;
    offer: number;
    rejected: number;
}

const COLORS = [
    "#1976d2",
    "#ff9800",
    "#4caf50",
    "#9c27b0",
    "#2e7d32",
    "#d32f2f",
];

export default function ApplicationStatusChart({
    applied,
    reviewing,
    shortlisted,
    interview,
    offer,
    rejected,
}: Props) {
    const data = [
        { name: "Applied", value: applied },
        { name: "Reviewing", value: reviewing },
        { name: "Shortlisted", value: shortlisted },
        { name: "Interview", value: interview },
        { name: "Offer", value: offer },
        { name: "Rejected", value: rejected },
    ].filter((item) => item.value > 0);

    if (data.length === 0) {
        return <p>No application data available.</p>;
    }

    return (
        <ResponsiveContainer width="100%" height={350}>
            <PieChart>
                <Pie
                    data={data}
                    dataKey="value"
                    nameKey="name"
                    outerRadius={120}
                    label
                >
                    {data.map((_, index) => (
                        <Cell
                            key={index}
                            fill={COLORS[index % COLORS.length]}
                        />
                    ))}
                </Pie>

                <Tooltip />
                <Legend />
            </PieChart>
        </ResponsiveContainer>
    );
}