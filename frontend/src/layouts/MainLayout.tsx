import { Box, Toolbar } from "@mui/material";
import { Outlet } from "react-router-dom";

import Sidebar from "../components/Sidebar";
import Navbar from "../components/Navbar";

const drawerWidth = 240;

export default function MainLayout() {
    return (
        <Box sx={{ display: "flex", minHeight: "100vh", bgcolor: "background.default" }}>
            <Sidebar />

            <Box
                component="main"
                sx={{
                    flexGrow: 1,
                    ml: { xs: 0, md: `${drawerWidth}px` },
                    minWidth: 0,
                }}
            >
                <Navbar />

                <Toolbar />

                <Box sx={{ p: { xs: 2, sm: 3, lg: 4 }, maxWidth: 1680, mx: "auto", width: "100%" }}>
                    <Outlet />
                </Box>
            </Box>
        </Box>
    );
}
