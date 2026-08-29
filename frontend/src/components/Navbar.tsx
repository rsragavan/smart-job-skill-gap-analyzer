import {
    AppBar,
    Toolbar,
    Typography,
    Box,
    IconButton,
    Menu,
    MenuItem,
    Avatar,
    Divider,
} from "@mui/material";
import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import MenuIcon from "@mui/icons-material/Menu";
import Brightness4Icon from "@mui/icons-material/Brightness4";
import Brightness7Icon from "@mui/icons-material/Brightness7";
import PersonIcon from "@mui/icons-material/Person";
import LogoutIcon from "@mui/icons-material/Logout";

import { useThemeMode } from "../hooks/useTheme";
import { useAuth } from "../contexts/AuthContext";

export default function Navbar() {
    const { mode, toggle } = useThemeMode();
    const { user, logout } = useAuth();
    const navigate = useNavigate();

    const [mobileMenu, setMobileMenu] =
        useState<HTMLElement | null>(null);

    const [profileMenu, setProfileMenu] =
        useState<HTMLElement | null>(null);

    async function handleLogout() {
        setProfileMenu(null);

        await logout();

        navigate("/login", {
            replace: true,
        });
    }

    const mobileItems =
        user?.role === "admin"
            ? [
                  {
                      label: "Admin Dashboard",
                      path: "/admin",
                  },
              ]
            : [
                  {
                      label: "Dashboard",
                      path: "/",
                  },
                  {
                      label: "Upload Resume",
                      path: "/upload",
                  },
                  {
                      label: "Target",
                      path: "/jobs",
                  },
                  {
                      label: "Learning",
                      path: "/learning",
                  },
                  {
                      label: "Roadmap",
                      path: "/roadmap",
                  },
                  {
                      label: "Career GPS",
                      path: "/career-gps",
                  },
                  {
                      label: "History",
                      path: "/history",
                  },
                  {
                      label: "Analytics",
                      path: "/analytics",
                  },
              ];

    return (
        <AppBar
            position="static"
            elevation={1}
            sx={{
                bgcolor: "background.paper",
                color: "text.primary",
                borderBottom: "1px solid",
                borderColor: "divider",
            }}
        >
            <Toolbar>

                <Typography
                    variant="h6"
                    fontWeight="bold"
                    sx={{ flexGrow: 1 }}
                >
                    Smart Job Skill Gap Analyzer
                </Typography>

                {/* Mobile Navigation */}

                <IconButton
                    aria-label="Open navigation menu"
                    sx={{
                        display: {
                            xs: "inline-flex",
                            md: "none",
                        },
                    }}
                    onClick={(e) =>
                        setMobileMenu(e.currentTarget)
                    }
                >
                    <MenuIcon />
                </IconButton>

                <Menu
                    anchorEl={mobileMenu}
                    open={Boolean(mobileMenu)}
                    onClose={() => setMobileMenu(null)}
                >
                    {mobileItems.map((item) => (
                        <MenuItem
                            key={item.path}
                            component={Link}
                            to={item.path}
                            onClick={() =>
                                setMobileMenu(null)
                            }
                        >
                            {item.label}
                        </MenuItem>
                    ))}
                </Menu>

                {/* Theme */}

                <IconButton
                    color="inherit"
                    aria-label={mode === "dark" ? "Switch to light mode" : "Switch to dark mode"}
                    onClick={toggle}
                    sx={{ ml: 1 }}
                >
                    {mode === "dark"
                        ? <Brightness7Icon />
                        : <Brightness4Icon />}
                </IconButton>

                {/* Profile */}

                <IconButton
                    aria-label="Open profile menu"
                    sx={{ ml: 1 }}
                    onClick={(e) =>
                        setProfileMenu(e.currentTarget)
                    }
                >
                    <Avatar
                        sx={{
                            width: 38,
                            height: 38,
                            bgcolor: "primary.main",
                        }}
                    >
                        {user?.full_name
                            ? user.full_name
                                  .charAt(0)
                                  .toUpperCase()
                            : <PersonIcon />}
                    </Avatar>
                </IconButton>

                <Menu
                    anchorEl={profileMenu}
                    open={Boolean(profileMenu)}
                    onClose={() =>
                        setProfileMenu(null)
                    }
                >
                    <Box
                        sx={{
                            px: 2,
                            py: 1,
                        }}
                    >
                        <Typography
                            fontWeight={600}
                        >
                            {user?.full_name}
                        </Typography>

                        <Typography
                            variant="body2"
                            color="text.secondary"
                        >
                            {user?.email}
                        </Typography>
                    </Box>

                    <Divider />

                    <MenuItem
                        component={Link}
                        to="/profile"
                        onClick={() =>
                            setProfileMenu(null)
                        }
                    >
                        <PersonIcon
                            sx={{
                                mr: 1,
                                fontSize: 20,
                            }}
                        />
                        My Profile
                    </MenuItem>

                    <MenuItem
                        onClick={handleLogout}
                    >
                        <LogoutIcon
                            sx={{
                                mr: 1,
                                fontSize: 20,
                            }}
                        />
                        Logout
                    </MenuItem>
                </Menu>

            </Toolbar>
        </AppBar>
    );
}
