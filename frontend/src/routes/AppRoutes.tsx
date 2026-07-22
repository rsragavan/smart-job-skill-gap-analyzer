import { lazy, Suspense } from "react";
import { Box, CircularProgress } from "@mui/material";
import { BrowserRouter, Route, Routes } from "react-router-dom";

import MainLayout from "../layouts/MainLayout";

import ProtectedRoute from "../components/ProtectedRoute";
const Dashboard = lazy(() => import("../pages/Dashboard"));
const UploadResume = lazy(() => import("../pages/UploadResume"));
const Jobs = lazy(() => import("../pages/Jobs"));
const LearningRoadmap = lazy(() => import("../pages/LearningRoadmap"));
const ResumeHistory = lazy(() => import("../pages/ResumeHistory"));
const Analytics = lazy(() => import("../pages/Analytics"));
const NotFound = lazy(() => import("../pages/NotFound"));
const Login = lazy(() => import("../pages/Login"));
const Register = lazy(() => import("../pages/Register"));
const Profile = lazy(() => import("../pages/Profile"));
const ForgotPassword = lazy(() => import("../pages/ForgotPassword"));
const ResetPassword = lazy(() => import("../pages/ResetPassword"));
const AdminDashboard = lazy(() => import("../pages/AdminDashboard"));

export default function AppRoutes() {
    return (
        <BrowserRouter>
            <Suspense fallback={<Box sx={{ minHeight: "100vh", display: "grid", placeItems: "center" }}><CircularProgress /></Box>}><Routes>

                <Route path="/login" element={<Login />} />
                <Route path="/register" element={<Register />} />
                <Route path="/forgot-password" element={<ForgotPassword />} />
                <Route path="/reset-password" element={<ResetPassword />} />
                <Route element={<ProtectedRoute />}>
                <Route element={<MainLayout />}>

                    <Route path="/" element={<Dashboard />} />

                    <Route path="/upload" element={<UploadResume />} />

                    <Route path="/jobs" element={<Jobs />} />

                    <Route path="/learning" element={<LearningRoadmap />} />

                    <Route path="/history" element={<ResumeHistory />} />

                    <Route path="/analytics" element={<Analytics />} />
                    <Route path="/profile" element={<Profile />} />

                    <Route path="*" element={<NotFound />} />

                </Route>
                </Route>
                <Route element={<ProtectedRoute role="admin" />}>
                    <Route path="/admin" element={<MainLayout />}>
                        <Route index element={<AdminDashboard />} />
                    </Route>
                </Route>

            </Routes></Suspense>
        </BrowserRouter>
    );
}
