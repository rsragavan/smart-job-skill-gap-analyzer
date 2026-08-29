import { Box, Typography, Button, Stack } from "@mui/material";
import { useNavigate } from "react-router-dom";

export default function NotFound() {
    const navigate = useNavigate();

    return (
        <Box
            sx={{
                minHeight: "70vh",
                display: "grid",
                placeItems: "center",
                px: 2,
                textAlign: "center",
            }}
        >
            <Stack spacing={2} alignItems="center" sx={{ maxWidth: 420 }}>
                <Typography variant="h3" fontWeight={700}>
                    404
                </Typography>
                <Typography variant="h5">Page not found</Typography>
                <Typography color="text.secondary">
                    The page you requested does not exist or the link may be outdated.
                </Typography>
                <Stack direction={{ xs: "column", sm: "row" }} spacing={1.5}>
                    <Button variant="contained" onClick={() => navigate("/")}>
                        Go to Dashboard
                    </Button>
                    <Button variant="outlined" onClick={() => navigate("/jobs")}>
                        Choose Target
                    </Button>
                </Stack>
            </Stack>
        </Box>
    );
}
