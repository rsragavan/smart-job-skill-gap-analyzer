import { Navigate, Outlet, useLocation } from "react-router-dom";
import { CircularProgress, Box } from "@mui/material";
import { useAuth } from "../contexts/AuthContext";
export default function ProtectedRoute({ role }: { role?: "admin" | "user" }) { const { user, ready } = useAuth(); const location = useLocation(); if (!ready) return <Box sx={{ display: "grid", placeItems: "center", minHeight: "100vh" }}><CircularProgress /></Box>; if (!user) return <Navigate to="/login" replace state={{ from: location }} />; if (role && user.role !== role) return <Navigate to={user.role === "admin" ? "/admin" : "/"} replace />; return <Outlet />; }
