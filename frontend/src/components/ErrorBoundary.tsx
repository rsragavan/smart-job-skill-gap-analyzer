import React from "react";
import { Box, Button, Typography } from "@mui/material";

type Props = { children: React.ReactNode };

type State = { hasError: boolean; error?: Error };

export default class ErrorBoundary extends React.Component<Props, State> {
    constructor(props: Props) {
        super(props);
        this.state = { hasError: false };
    }

    static getDerivedStateFromError(error: Error) {
        return { hasError: true, error };
    }

    reset = () => {
        this.setState({ hasError: false, error: undefined });
    };

    render() {
        if (this.state.hasError) {
            return (
                <Box sx={{ p: 3, maxWidth: 560, mx: "auto", textAlign: "center" }}>
                    <Typography variant="h5" gutterBottom>
                        Something went wrong
                    </Typography>
                    <Typography color="text.secondary" sx={{ mb: 2 }}>{this.state.error?.message ?? "Please try again."}</Typography>
                    <Button variant="contained" onClick={this.reset}>
                        Try again
                    </Button>
                </Box>
            );
        }

        return this.props.children as React.ReactElement;
    }
}

