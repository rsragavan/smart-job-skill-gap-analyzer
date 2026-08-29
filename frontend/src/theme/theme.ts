import { createTheme } from "@mui/material/styles";

export function getTheme(mode: "light" | "dark") {
    const light = mode === "light";
    return createTheme({
        palette: {
            mode,
            primary: { main: light ? "#3659d9" : "#aebdff" },
            secondary: { main: light ? "#008a72" : "#5de1c3" },
            background: { default: light ? "#f6f7fb" : "#10131a", paper: light ? "#ffffff" : "#181d27" },
        },
        components: {
            MuiCard: { styleOverrides: { root: { borderRadius: 18, border: `1px solid ${light ? "#e5e8f0" : "#2a3241"}`, boxShadow: light ? "0 4px 18px rgba(22, 34, 61, 0.07)" : "0 6px 20px rgba(0, 0, 0, 0.2)", transition: "transform 180ms ease, box-shadow 180ms ease, border-color 180ms ease", "&:hover": { boxShadow: light ? "0 10px 28px rgba(22, 34, 61, 0.12)" : "0 10px 28px rgba(0, 0, 0, 0.32)" } } } },
            MuiPaper: { styleOverrides: { rounded: { borderRadius: 18 } } },
            MuiButton: { styleOverrides: { root: { minHeight: 42, borderRadius: 11, textTransform: "none", fontWeight: 700, boxShadow: "none" }, contained: { "&:hover": { boxShadow: "0 6px 16px rgba(54, 89, 217, 0.22)" } } } },
            MuiIconButton: { styleOverrides: { root: { borderRadius: 11 } } },
            MuiOutlinedInput: { styleOverrides: { root: { borderRadius: 11 } } },
            MuiChip: { styleOverrides: { root: { borderRadius: 9, fontWeight: 650 } } },
            MuiLinearProgress: { styleOverrides: { root: { height: 8, borderRadius: 99 }, bar: { borderRadius: 99 } } },
            MuiAlert: { styleOverrides: { root: { borderRadius: 12 } } },
            MuiTableHead: { styleOverrides: { root: { "& .MuiTableCell-head": { fontWeight: 750, backgroundColor: light ? "#f4f6fb" : "#202734" } } } },
            MuiCssBaseline: { styleOverrides: { "*": { scrollbarWidth: "thin" }, body: { overflowX: "hidden", minHeight: "100vh" }, "button:focus-visible, a:focus-visible, input:focus-visible, [tabindex]:focus-visible": { outline: `3px solid ${light ? "#3659d9" : "#aebdff"}`, outlineOffset: 2 } } },
        },
        typography: { fontFamily: "Inter, Roboto, Arial, sans-serif", h4: { fontWeight: 750, letterSpacing: "-0.025em" }, h6: { fontWeight: 700 } },
    });
}
