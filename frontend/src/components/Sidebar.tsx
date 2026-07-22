import { Drawer, List, ListItemButton, ListItemText, Toolbar } from "@mui/material";
import { Link, useLocation } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";

const drawerWidth = 240;

const menuItems = [
    { text: "Dashboard", path: "/" },
    { text: "Upload Resume", path: "/upload" },
    { text: "Jobs", path: "/jobs" },
    { text: "Learning", path: "/learning" },
    { text: "History", path: "/history" },
    { text: "Analytics", path: "/analytics" },
];

export default function Sidebar() {
    const location = useLocation();
    const { user } = useAuth();
    const visibleItems = user?.role === "admin" ? [{ text: "Admin Dashboard", path: "/admin" }] : menuItems;

    return (
        <Drawer
            variant="permanent"
            sx={{
                width: drawerWidth,
                display: { xs: "none", md: "block" },
                "& .MuiDrawer-paper": {
                    width: drawerWidth,
                    boxSizing: "border-box",
                },
            }}
        >
            <Toolbar>
                <h2>Skill Gap</h2>
            </Toolbar>

            <List>
                {visibleItems.map((item) => (
                    <ListItemButton
                        key={item.text}
                        component={Link}
                        to={item.path}
                        selected={location.pathname === item.path}
                    >
                        <ListItemText primary={item.text} />
                    </ListItemButton>
                ))}
            </List>
        </Drawer>
    );
}
