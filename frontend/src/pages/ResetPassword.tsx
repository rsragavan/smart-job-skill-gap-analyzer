import { useState } from "react";
import { Alert, Box, Button, Paper, TextField, Typography } from "@mui/material";
import { useNavigate, useSearchParams } from "react-router-dom";

import api from "../api/api";

export default function ResetPassword() {
    const [searchParams] = useSearchParams();
    const navigate = useNavigate();
    const [password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);

    const submit = async (event: React.FormEvent) => {
        event.preventDefault();
        const token = searchParams.get("token");
        if (!token) { setError("This password-reset link is invalid."); return; }
        if (password !== confirmPassword) { setError("Passwords do not match."); return; }
        setLoading(true); setError("");
        try {
            const { data } = await api.post<{ message: string }>("/auth/reset-password", { token, password, confirm_password: confirmPassword });
            navigate("/login", { replace: true, state: { message: data.message } });
        } catch {
            setError("The reset link is invalid, expired, or the password does not meet the requirements.");
        } finally { setLoading(false); }
    };

    return <Box sx={{ minHeight: "100vh", display: "grid", placeItems: "center", p: 2 }}><Paper component="form" onSubmit={submit} sx={{ p: 4, width: "100%", maxWidth: 440, borderRadius: 3 }}><Typography variant="h4" sx={{ fontWeight: 700 }}>Choose a new password</Typography><Typography color="text.secondary" sx={{ mt: 1, mb: 3 }}>Use uppercase, lowercase, a number, and a special character.</Typography>{error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}<TextField label="New password" type="password" value={password} onChange={event => setPassword(event.target.value)} fullWidth required autoComplete="new-password" /><TextField label="Confirm new password" type="password" value={confirmPassword} onChange={event => setConfirmPassword(event.target.value)} fullWidth required autoComplete="new-password" sx={{ mt: 2 }} /><Button type="submit" variant="contained" fullWidth disabled={loading} sx={{ mt: 2 }}>{loading ? "Updating…" : "Update password"}</Button></Paper></Box>;
}
