import AppRoutes from "./routes/AppRoutes";
import { ThemeProvider, CssBaseline } from "@mui/material";
import { getTheme } from "./theme/theme";
import { ThemeProviderWrapper, useThemeMode } from "./hooks/useTheme.tsx";
import ErrorBoundary from "./components/ErrorBoundary";
import { WorkflowProvider } from "./contexts/WorkflowContext";
import { AuthProvider } from "./contexts/AuthContext";


function AppInner() {
    const { mode } = useThemeMode();
    const theme = getTheme(mode);

    return (
        <ThemeProvider theme={theme}>
            <CssBaseline />
            <AuthProvider>
            <WorkflowProvider>
                <ErrorBoundary>
                    <AppRoutes />
                </ErrorBoundary>
            </WorkflowProvider>
            </AuthProvider>
        </ThemeProvider>
    );
}

function App() {
    return (
        <ThemeProviderWrapper>
            <AppInner />
        </ThemeProviderWrapper>
    );
}

export default App;
