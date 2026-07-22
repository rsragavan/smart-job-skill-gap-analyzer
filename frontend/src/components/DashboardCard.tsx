 import { Card, CardContent, Typography } from "@mui/material";

interface DashboardCardProps {
    title: string;
    value: string | number;
}

export default function DashboardCard({
    title,
    value,
}: DashboardCardProps) {
    return (
        <Card elevation={3}>
            <CardContent>
                <Typography variant="body2" color="text.secondary">
                    {title}
                </Typography>

                <Typography variant="h4">
                    {value}
                </Typography>
            </CardContent>
        </Card>
    );
}