import { useState } from "react";
import { Alert, Box, Button, Paper, TextField, Typography } from "@mui/material";
import { Link as RouterLink } from "react-router-dom";

import api from "../api/api";

export default function ForgotPassword() {
    const [email, setEmail] = useState("");
    const [message, setMessage] = useState("");
    const [resetUrl, setResetUrl] = useState("");
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);

    const submit = async (event: React.FormEvent) => {
        event.preventDefault();
        setLoading(true); setError("");
        try {
            const { data } = await api.post<{ message: string; reset_url?: string }>("/auth/forgot-password", { email });
            setMessage(data.message);
            setResetUrl(data.reset_url ?? "");
        } catch {
            setError("We could not process the password-reset request.");
        } finally { setLoading(false); }
    };

    return <Box sx={{ minHeight: "100vh", display: "grid", placeItems: "center", p: 2 }}><Paper component="form" onSubmit={submit} sx={{ p: 4, width: "100%", maxWidth: 440, borderRadius: 3 }}><Typography variant="h4" sx={{ fontWeight: 700 }}>Reset password</Typography><Typography color="text.secondary" sx={{ mt: 1, mb: 3 }}>Enter your email and we will send a reset link.</Typography>{message && <Alert severity="success" sx={{ mb: 2 }}>{message}</Alert>}{resetUrl && <Button href={resetUrl} variant="outlined" fullWidth sx={{ mb: 2 }}>Continue to reset password</Button>}{error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}<TextField label="Email" type="email" value={email} onChange={event => setEmail(event.target.value)} fullWidth required autoComplete="email" /><Button type="submit" variant="contained" fullWidth disabled={loading} sx={{ mt: 2 }}>{loading ? "Sending…" : "Send reset link"}</Button><Button component={RouterLink} to="/login" fullWidth sx={{ mt: 1 }}>Back to login</Button></Paper></Box>;
}
