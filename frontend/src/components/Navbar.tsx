import {
    AppBar,
    Toolbar,
    Typography,
    Box,
    IconButton,
    Menu,
    MenuItem,
    Button,
} from "@mui/material";
import { useState } from "react";
import { Link } from "react-router-dom";
import MenuIcon from "@mui/icons-material/Menu";

import Brightness4Icon from "@mui/icons-material/Brightness4";
import Brightness7Icon from "@mui/icons-material/Brightness7";

import { useThemeMode } from "../hooks/useTheme";
import { useAuth } from "../contexts/AuthContext";
import { useNavigate } from "react-router-dom";

export default function Navbar() {

    const { mode, toggle } = useThemeMode();
    const [menuAnchor, setMenuAnchor] = useState<HTMLElement | null>(null);
    const { user, logout } = useAuth();
    const navigate = useNavigate();
    const handleLogout = async () => { await logout(); navigate("/login", { replace: true }); };

    return (
        <AppBar
            position="static"
            color="primary"
            elevation={1}
            sx={{ bgcolor: "background.paper", color: "text.primary", borderBottom: "1px solid", borderColor: "divider" }}
        >
            <Toolbar>

                <Box
                    sx={{
                        flexGrow: 1,
                    }}
                >
                    <Typography variant="h6" noWrap>
                        Smart Job Skill Gap Analyzer
                    </Typography>
                </Box>

                <IconButton aria-label="Open navigation" onClick={(event) => setMenuAnchor(event.currentTarget)} sx={{ display: { xs: "inline-flex", md: "none" } }}><MenuIcon /></IconButton>

                <IconButton
                    color="inherit"
                    onClick={toggle}
                    aria-label="Toggle theme"
                >
                    {mode === "dark"
                        ? <Brightness7Icon />
                        : <Brightness4Icon />
                    }
                </IconButton>
                <Button color="inherit" onClick={() => void handleLogout()} sx={{ ml: 1 }}>Log out</Button>

                <Menu anchorEl={menuAnchor} open={Boolean(menuAnchor)} onClose={() => setMenuAnchor(null)}>
                    {(user?.role === "admin" ? [['Admin Dashboard', '/admin']] : [['Dashboard', '/'], ['Upload Resume', '/upload'], ['Jobs', '/jobs'], ['Learning', '/learning'], ['History', '/history'], ['Analytics', '/analytics'], ['Profile', '/profile']]).map(([label, path]) => <MenuItem key={path} component={Link} to={path} onClick={() => setMenuAnchor(null)}>{label}</MenuItem>)}
                    <MenuItem onClick={() => void handleLogout()}>Log out</MenuItem>
                </Menu>

            </Toolbar>
        </AppBar>
    );
}
