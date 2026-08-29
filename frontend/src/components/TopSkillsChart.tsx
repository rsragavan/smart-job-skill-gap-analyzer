import {
    ResponsiveContainer,
    BarChart,
    Bar,
    XAxis,
    YAxis,
    Tooltip,
    CartesianGrid,
} from "recharts";

interface Props {
    python: number;
    java: number;
    docker: number;
    linux: number;
    remote: number;
}

export default function TopSkillsChart({
    python,
    java,
    docker,
    linux,
    remote,
}: Props) {
    const data = [
        {
            skill: "Python",
            jobs: python,
        },
        {
            skill: "Java",
            jobs: java,
        },
        {
            skill: "Docker",
            jobs: docker,
        },
        {
            skill: "Linux",
            jobs: linux,
        },
        {
            skill: "Remote",
            jobs: remote,
        },
    ];

    return (
        <ResponsiveContainer width="100%" height={350}>
            <BarChart data={data}>
                <CartesianGrid strokeDasharray="3 3" />

                <XAxis dataKey="skill" />

                <YAxis />

                <Tooltip />

                <Bar
                    dataKey="jobs"
                    radius={[6, 6, 0, 0]}
                />
            </BarChart>
        </ResponsiveContainer>
    );
}