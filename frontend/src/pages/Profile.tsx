import { useEffect, useState } from "react";
import {
    Alert,
    Avatar,
    Box,
    Button,
    Card,
    CardContent,
    CircularProgress,
    Divider,
    Stack,
    Typography,
    Chip,
} from "@mui/material";
import PersonIcon from "@mui/icons-material/Person";
import LogoutIcon from "@mui/icons-material/Logout";
import EmailIcon from "@mui/icons-material/Email";
import BadgeIcon from "@mui/icons-material/Badge";
import CalendarMonthIcon from "@mui/icons-material/CalendarMonth";
import HistoryIcon from "@mui/icons-material/History";
import DescriptionIcon from "@mui/icons-material/Description";
import { useNavigate } from "react-router-dom";

import { useAuth } from "../contexts/AuthContext";
import profileService from "../services/profileService";
import type { Profile } from "../types/profile";

export default function ProfilePage() {
    const { logout } = useAuth();
    const navigate = useNavigate();

    const [profile, setProfile] = useState<Profile | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    async function loadProfile() {
        setError(null);
        try {
            const data = await profileService.getProfile();
            setProfile(data);
        } catch (err) {
            setError(err instanceof Error ? err.message : "Unable to load profile.");
        } finally {
            setLoading(false);
        }
    }

    useEffect(() => {
        void loadProfile();
    }, []);

    async function handleLogout() {
        await logout();
        navigate("/login");
    }

    if (loading) {
        return (
            <Box
                display="flex"
                justifyContent="center"
                mt={8}
            >
                <CircularProgress />
            </Box>
        );
    }

    if (!profile) {
        return (
            <Box sx={{ maxWidth: 480, mx: "auto", mt: 6, px: 2 }}>
                <Alert
                    severity="error"
                    action={<Button color="inherit" size="small" onClick={() => { setLoading(true); void loadProfile(); }}>Retry</Button>}
                >
                    {error || "Unable to load profile."}
                </Alert>
            </Box>
        );
    }

    return (
        <Box
            sx={{
                maxWidth: 750,
                mx: "auto",
                mt: 4,
            }}
        >
            <Card elevation={4}>

                <CardContent>

                    <Stack
                        spacing={2}
                        alignItems="center"
                    >
                        <Avatar
                            sx={{
                                width: 90,
                                height: 90,
                            }}
                        >
                            <PersonIcon fontSize="large" />
                        </Avatar>

                        <Typography
                            variant="h5"
                            fontWeight="bold"
                        >
                            {profile.full_name}
                        </Typography>

                        <Chip
                            label={profile.role.toUpperCase()}
                            color="primary"
                        />
                    </Stack>

                    <Divider sx={{ my: 4 }} />

                    <Stack spacing={3}>

                        <Box>
                            <Stack direction="row" spacing={1}>
                                <EmailIcon color="primary" />
                                <Typography fontWeight={600}>
                                    Email
                                </Typography>
                            </Stack>

                            <Typography color="text.secondary">
                                {profile.email}
                            </Typography>
                        </Box>

                        <Box>
                            <Stack direction="row" spacing={1}>
                                <BadgeIcon color="primary" />
                                <Typography fontWeight={600}>
                                    User ID
                                </Typography>
                            </Stack>

                            <Typography color="text.secondary">
                                {profile.id}
                            </Typography>
                        </Box>

                        <Box>
                            <Stack direction="row" spacing={1}>
                                <CalendarMonthIcon color="primary" />
                                <Typography fontWeight={600}>
                                    Joined
                                </Typography>
                            </Stack>

                            <Typography color="text.secondary">
                                {new Date(
                                    profile.joined_date
                                ).toLocaleDateString()}
                            </Typography>
                        </Box>

                        <Box>
                            <Stack direction="row" spacing={1}>
                                <HistoryIcon color="primary" />
                                <Typography fontWeight={600}>
                                    Last Login
                                </Typography>
                            </Stack>

                            <Typography color="text.secondary">
                                {profile.last_login
                                    ? new Date(
                                          profile.last_login
                                      ).toLocaleString()
                                    : "Never"}
                            </Typography>
                        </Box>

                        <Box>
                            <Stack direction="row" spacing={1}>
                                <DescriptionIcon color="primary" />
                                <Typography fontWeight={600}>
                                    Uploaded Resumes
                                </Typography>
                            </Stack>

                            <Typography color="text.secondary">
                                {profile.uploaded_resume_count}
                            </Typography>
                        </Box>

                    </Stack>

                    <Divider sx={{ my: 4 }} />

                    <Button
                        fullWidth
                        color="error"
                        variant="contained"
                        startIcon={<LogoutIcon />}
                        onClick={handleLogout}
                    >
                        Logout
                    </Button>

                </CardContent>

            </Card>
        </Box>
    );
}
