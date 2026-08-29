import {
    Card,
    CardContent,
    Typography,
    Box,
    Button,
    Chip,
    Stack,
} from "@mui/material";

import LaunchIcon from "@mui/icons-material/Launch";
import WorkIcon from "@mui/icons-material/Work";

import { Snackbar, Alert } from "@mui/material";
import { useState } from "react";
import { isAxiosError } from "axios";
import applicationService from "../services/applicationService";
import type { Job } from "../types/job";

interface Props {
    job: Job;
    isSelected?: boolean;
    onSelect?: (job: Job) => void;
}

function isValidChipValue(value: string | null | undefined): value is string {
    const normalizedValue = value?.trim().toLowerCase();

    return Boolean(
        normalizedValue &&
        normalizedValue !== "unknown" &&
        normalizedValue !== "null" &&
        normalizedValue !== "undefined",
    );
}

export default function JobCard({ job, isSelected = false, onSelect }: Props) {
    const matchedSkills = job.matched_skills.filter(isValidChipValue);
    const missingSkills = job.missing_skills.filter(isValidChipValue);
    const [applying, setApplying] = useState(false);
const [applied, setApplied] = useState(false);

const [snackbar, setSnackbar] = useState({
    open: false,
    message: "",
    severity: "success" as "success" | "error",
});

const applyForJob = async () => {
    try {
        setApplying(true);

        await applicationService.applyForJob(job.id);

        setApplied(true);

        setSnackbar({
            open: true,
            message: "Application submitted successfully.",
            severity: "success",
        });

    } catch (error: unknown) {

        if (isAxiosError(error) && error.response?.status === 400) {
            setApplied(true);

            setSnackbar({
                open: true,
                message: "You have already applied for this job.",
                severity: "error",
            });
        } else {

            setSnackbar({
                open: true,
                message: "Failed to apply.",
                severity: "error",
            });

        }

    } finally {
        setApplying(false);
    }
};
    return (
        <>
        <Card
            elevation={3}
            sx={{
                borderRadius: 3,
                height: "100%",
                transition: "0.25s",
                "&:hover": {
                    transform: "translateY(-4px)",
                    boxShadow: 8,
                },
            }}
        >
            <CardContent>

                <Stack
                    direction="row"
                    sx={{
                        justifyContent: "space-between",
                        alignItems: "flex-start",
                    }}
                >

                    <Box>

                        <Typography
                            variant="h6"
                            sx={{
                                fontWeight: 700,
                            }}
                        >
                            {job.title}
                        </Typography>

                        <Typography
                            color="text.secondary"
                            sx={{
                                mt: 0.5,
                            }}
                        >
                            {job.company}
                        </Typography>

                        <Typography
                            variant="body2"
                            color="text.secondary"
                            sx={{
                                mt: 0.5,
                            }}
                        >
                            {job.location}
                        </Typography>
                        <Typography variant="caption" color="text.secondary" sx={{ display: "block", mt: 0.5 }}>
                            Posted {new Date(job.posted_date).toLocaleDateString()}
                        </Typography>

                    </Box>

                    <WorkIcon color="primary" />

                </Stack>

                <Typography variant="subtitle2" color="primary" sx={{ mt: 2 }}>
                    Match: {job.match_percentage}%
                </Typography>
                <Chip label={job.status} size="small" color={job.status === "ACTIVE" ? "success" : "default"} sx={{ mt: 1 }} />

                <Box sx={{ mt: 2 }}>
                    <Typography variant="body2" color="text.secondary">Matched Skills</Typography>
                    <Stack direction="row" spacing={1} useFlexGap sx={{ mt: 1, flexWrap: "wrap" }}>
                        {matchedSkills.length ? matchedSkills.map((skill) => (
                            <Chip key={skill} label={skill} size="small" color="success" />
                        )) : <Typography variant="caption" color="text.secondary">No matched skills yet</Typography>}
                    </Stack>
                </Box>

                <Box sx={{ mt: 2 }}>
                    <Typography variant="body2" color="text.secondary">Missing Skills</Typography>
                    <Stack direction="row" spacing={1} useFlexGap sx={{ mt: 1, flexWrap: "wrap" }}>
                        {missingSkills.length ? missingSkills.map((skill) => (
                            <Chip key={skill} label={skill} size="small" color="error" variant="outlined" />
                        )) : <Typography variant="caption" color="text.secondary">No missing skills identified</Typography>}
                    </Stack>
                </Box>

                <Stack
                    direction="row"
                    spacing={1}
                    useFlexGap
                    sx={{
                        mt: 2,
                        flexWrap: "wrap",
                    }}
                >
                    {isValidChipValue(job.location) && (
                        <Chip
                            label={job.location}
                            size="small"
                            variant="outlined"
                        />
                    )}
                    {isValidChipValue(job.department) && (
                        <Chip
                            label={job.department}
                            size="small"
                            variant="outlined"
                        />
                    )}
                    {isValidChipValue(job.employment_type) && (
                        <Chip
                            label={job.employment_type}
                            size="small"
                            color="primary"
                        />
                    )}
                </Stack>

                <Box
                    sx={{
                        display: "flex",
                        justifyContent: "flex-end",
                        gap: 1,
                        mt: 3,
                        flexWrap: "wrap",
                    }}
                >
                    {onSelect && (
                        <Button
                            variant={isSelected ? "contained" : "outlined"}
                            onClick={() => onSelect(job)}
                        >
                            {isSelected ? "Selected" : "Select Job"}
                        </Button>
                    )}
                    <Button
    variant="contained"
    color={applied ? "success" : "primary"}
    disabled={applying || applied}
    onClick={applyForJob}
>
    {applying
        ? "Applying..."
        : applied
        ? "Applied"
        : "Apply"}
</Button>

<Button
    variant="outlined"
    endIcon={<LaunchIcon />}
    href={job.url}
    target="_blank"
    rel="noopener noreferrer"
    disabled={!job.url}
>
    View Job
</Button>
                </Box>

            </CardContent>
        </Card>
        <Snackbar
    open={snackbar.open}
    autoHideDuration={3000}
    onClose={() =>
        setSnackbar({
            ...snackbar,
            open: false,
        })
    }
>
    <Alert
        severity={snackbar.severity}
        variant="filled"
    >
        {snackbar.message}
    </Alert>
</Snackbar>
    </>
    );
}
