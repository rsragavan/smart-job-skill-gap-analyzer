import { Box, Button, Card, CardContent, Divider, Stack, Typography } from "@mui/material";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";

export default function Profile() {
  const { user, logout } = useAuth(); const navigate = useNavigate();
  if (!user) return null;
  const signOut = async () => { await logout(); navigate("/login"); };
  return <Box sx={{ maxWidth: 620, mx: "auto", pt: { xs: 1, sm: 4 } }}><Card sx={{ borderRadius: 3, boxShadow: 4 }}><CardContent sx={{ p: { xs: 3, sm: 4 } }}><Stack spacing={1.5} sx={{ alignItems: "center" }}><Typography variant="h5">{user.full_name}</Typography><Typography color="text.secondary">{user.email}</Typography></Stack><Divider sx={{ my: 3 }} /><Stack spacing={2}><Box><Typography variant="caption" color="text.secondary">LAST LOGIN</Typography><Typography>{user.last_login ? new Date(user.last_login).toLocaleString() : "Not available"}</Typography></Box><Button variant="outlined" color="error" onClick={signOut}>Logout</Button></Stack></CardContent></Card></Box>;
}
