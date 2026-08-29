import {
    Box,
    Drawer,
    List,
    ListItemButton,
    ListItemText,
    Toolbar,
    Divider,
} from "@mui/material";
import { Link, useLocation } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";
import DashboardOutlinedIcon from "@mui/icons-material/DashboardOutlined";
import WorkOutlineIcon from "@mui/icons-material/WorkOutline";
import UploadFileOutlinedIcon from "@mui/icons-material/UploadFileOutlined";
import SchoolOutlinedIcon from "@mui/icons-material/SchoolOutlined";
import RouteOutlinedIcon from "@mui/icons-material/RouteOutlined";
import GpsFixedOutlinedIcon from "@mui/icons-material/GpsFixedOutlined";
import HistoryOutlinedIcon from "@mui/icons-material/HistoryOutlined";
import AnalyticsOutlinedIcon from "@mui/icons-material/AnalyticsOutlined";
import AdminPanelSettingsOutlinedIcon from "@mui/icons-material/AdminPanelSettingsOutlined";
import PersonOutlineOutlinedIcon from "@mui/icons-material/PersonOutlineOutlined";
import BusinessOutlinedIcon from "@mui/icons-material/BusinessOutlined";
import TimelineOutlinedIcon from "@mui/icons-material/TimelineOutlined";
import RecordVoiceOverOutlinedIcon from "@mui/icons-material/RecordVoiceOverOutlined";
import CodeOutlinedIcon from "@mui/icons-material/CodeOutlined";
import { Tooltip } from "@mui/material";

const drawerWidth = 240;

const userMenuItems = [
    { text: "Dashboard", path: "/", icon: <DashboardOutlinedIcon /> },
    { text: "Upload Resume", path: "/upload", icon: <UploadFileOutlinedIcon /> },
    { text: "Target", path: "/jobs", icon: <WorkOutlineIcon /> },
    { text: "Target Company", path: "/companies", icon: <BusinessOutlinedIcon /> },
    { text: "Applications", path: "/applications", icon: <TimelineOutlinedIcon /> },
    { text: "Mock Interview", path: "/interviews", icon: <RecordVoiceOverOutlinedIcon /> },
    { text: "Coding Practice", path: "/coding-practice", icon: <CodeOutlinedIcon /> },
    { text: "Roadmap", path: "/roadmap", icon: <RouteOutlinedIcon /> },
    { text: "Learning", path: "/learning", icon: <SchoolOutlinedIcon /> },
    { text: "Career GPS", path: "/career-gps", icon: <GpsFixedOutlinedIcon /> },
    { text: "History", path: "/history", icon: <HistoryOutlinedIcon /> },
    { text: "Analytics", path: "/analytics", icon: <AnalyticsOutlinedIcon /> },
];

const adminMenuItems = [
    { text: "Admin Dashboard", path: "/admin", icon: <AdminPanelSettingsOutlinedIcon /> },
    { text: "Profile", path: "/profile", icon: <PersonOutlineOutlinedIcon /> },
];

export default function Sidebar() {
    const location = useLocation();
    const { user } = useAuth();

    const visibleItems =
        user?.role === "admin"
            ? adminMenuItems
            : userMenuItems;

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

            <Divider />

            <List>
                {visibleItems.map((item) => (
                    <ListItemButton
                        key={item.text}
                        component={Link}
                        to={item.path}
                        selected={item.path === "/" ? location.pathname === "/" : location.pathname.startsWith(item.path)}
                        aria-current={location.pathname === item.path ? "page" : undefined}
                        sx={{ mx: 1, mb: 0.5, borderRadius: 2, minHeight: 46, "&.Mui-selected": { bgcolor: "primary.main", color: "primary.contrastText", "&:hover": { bgcolor: "primary.dark" }, "& .MuiListItemIcon-root": { color: "inherit" } } }}
                    >
                        <Tooltip title={item.text} placement="right"><Box sx={{ display: "flex", alignItems: "center", mr: 1.5 }} aria-hidden="true">{item.icon}</Box></Tooltip>
                        <ListItemText primary={item.text} primaryTypographyProps={{ fontWeight: 650 }} />
                    </ListItemButton>
                ))}
            </List>
        </Drawer>
    );
}
