import { Box, Card, CardContent, Stack, Typography } from "@mui/material";

interface DashboardCardProps {
    title: string;
    value: string | number;
}

export default function DashboardCard({
    title,
    value,
}: DashboardCardProps) {
    return (
        <Card elevation={0} sx={{ height: "100%", transition: "transform 180ms ease", "&:hover": { transform: "translateY(-3px)" } }}>
            <CardContent sx={{ p: { xs: 2, sm: 2.5 }, "&:last-child": { pb: { xs: 2, sm: 2.5 } } }}>
                <Stack direction="row" spacing={1.25} sx={{ alignItems: "center" }}>
                    <Box sx={{ width: 8, height: 32, borderRadius: 99, bgcolor: "primary.main" }} aria-hidden="true" />
                    <Typography variant="body2" color="text.secondary">
                        {title}
                    </Typography>
                </Stack>

                <Typography variant="h4" sx={{ mt: 1.5, fontWeight: 750 }}>
                    {value}
                </Typography>
            </CardContent>
        </Card>
    );
}
