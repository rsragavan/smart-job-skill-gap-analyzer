import { createTheme } from "@mui/material/styles";

export function getTheme(mode: 'light' | 'dark') {
	return createTheme({
		palette: {
			mode,
			primary: {
				main: mode === 'light' ? '#3659d9' : '#aebdff',
			},
			secondary: { main: mode === 'light' ? '#008a72' : '#5de1c3' },
			background: {
				default: mode === 'light' ? '#f6f7fb' : '#10131a',
				paper: mode === 'light' ? '#ffffff' : '#181d27',
			},
		},
		components: {
			MuiCard: {
				styleOverrides: {
					root: {
						borderRadius: 16,
						border: `1px solid ${mode === 'light' ? '#e5e8f0' : '#2a3241'}`,
						boxShadow: mode === 'light' ? '0 4px 18px rgba(22, 34, 61, 0.07)' : '0 6px 20px rgba(0, 0, 0, 0.2)',
					},
				},
			},
			MuiPaper: { styleOverrides: { rounded: { borderRadius: 16 } } },
			MuiButton: { styleOverrides: { root: { borderRadius: 10, textTransform: 'none', fontWeight: 700 } } },
			MuiOutlinedInput: { styleOverrides: { root: { borderRadius: 10 } } },
			MuiCssBaseline: { styleOverrides: { '*': { scrollbarWidth: 'thin' }, body: { overflowX: 'hidden' } } },
		},
		typography: {
			fontFamily: 'Inter, Roboto, Arial, sans-serif',
			h4: { fontWeight: 750, letterSpacing: '-0.025em' },
			h6: { fontWeight: 700 },
		},
	});
}
