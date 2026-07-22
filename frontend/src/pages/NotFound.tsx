import { Box, Typography, Button } from "@mui/material";
import { useNavigate } from "react-router-dom";

export default function NotFound() {
    const navigate = useNavigate();

    return (
        <Box sx={{ p: 3, textAlign: "center" }}>
            <Typography variant="h4" gutterBottom>
                404 — Page not found
            </Typography>
            <Typography sx={{ mb: 2 }}>The page you are looking for does not exist.</Typography>
            <Button variant="contained" onClick={() => navigate('/')}>Go to Dashboard</Button>
        </Box>
    );
}

