import { Box, Toolbar } from "@mui/material";
import { Outlet } from "react-router-dom";

import Sidebar from "../components/Sidebar";
import Navbar from "../components/Navbar";

const drawerWidth = 240;

export default function MainLayout() {
    return (
        <Box sx={{ display: "flex" }}>
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

                <Box sx={{ p: { xs: 2, sm: 3 }, maxWidth: 1600, mx: "auto" }}>
                    <Outlet />
                </Box>
            </Box>
        </Box>
    );
}
