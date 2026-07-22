import { useCallback, useState } from "react";
import {
    Button,
    Typography,
    Paper,
    Box,
    Snackbar,
    Alert,
    Skeleton,
    Stack,
    Chip,
} from "@mui/material";

import FileUpload from "../components/FileUpload";
import RecommendedJobCard from "../components/RecommendedJobCard";
import { uploadResumeService } from "../services/resumeService";
import type { ResumeResponse } from "../types/resume";

export default function UploadResume() {

    const [selectedFile, setSelectedFile] = useState<File | null>(null);

    const [response, setResponse] = useState<ResumeResponse | null>(null);

    const [loading, setLoading] = useState(false);

    const [error, setError] = useState<string | null>(null);

    const [openSnackbar, setOpenSnackbar] = useState(false);

    const handleUpload = useCallback(async () => {

        if (!selectedFile) {
            setError("Please select a resume.");
            setOpenSnackbar(true);
            return;
        }

        setLoading(true);
        setError(null);

        try {

            const result = await uploadResumeService(selectedFile);

            setResponse(result);
            setOpenSnackbar(true);

        } catch (err: unknown) {
            setError(err instanceof Error ? err.message : "Upload failed. Check your connection and try again.");
            setOpenSnackbar(true);
        } finally {
            setLoading(false);
        }

    }, [selectedFile]);

    return (

        <Paper sx={{ p: { xs: 2, sm: 3 }, borderRadius: 4 }}>

            <Typography variant="h4" gutterBottom>Upload Resume</Typography>

            <Box sx={{ display: 'grid', gridTemplateColumns: { xs: '1fr', md: '320px 1fr' }, gap: 3 }}>

                <Box>
                    <Box sx={{ mb: 2 }}>
                        <FileUpload onFileSelected={setSelectedFile} />
                    </Box>

                    <Box sx={{ mb: 2 }}>
                        {loading ? <Skeleton variant="rounded" width={150} height={40} /> : <Button variant="contained" onClick={() => void handleUpload()} disabled={!selectedFile} aria-label="Upload selected resume">Upload Resume</Button>}
                    </Box>

                    <Box>
                        <Typography variant="subtitle1">Selected File</Typography>

                        {selectedFile ? (
                            <Typography>{selectedFile.name}</Typography>
                        ) : (
                            <Typography color="text.secondary">No file selected</Typography>
                        )}
                    </Box>
                </Box>

                <Box>
                    <Box sx={{ mb: 3 }}>
                        <Typography variant="h6" gutterBottom>Extracted Skills</Typography>

                        {loading && !response ? (
                            <Stack direction="row" spacing={1} useFlexGap sx={{ flexWrap: 'wrap' }}>
                                {[1, 2, 3].map((i) => (
                                    <Skeleton key={i} variant="rounded" width={80} height={32} />
                                ))}
                            </Stack>
                        ) : response?.resume_skills?.length ? (
                            <Stack direction="row" spacing={1} useFlexGap sx={{ flexWrap: 'wrap' }}>
                                {response.resume_skills.map((skill) => (
                                    <Chip
                                        key={skill}
                                        label={skill}
                                        size="small"
                                        sx={{
                                            backgroundColor: "#e3f2fd",
                                            color: "#1565c0",
                                            fontWeight: 500,
                                        }}
                                    />
                                ))}
                            </Stack>
                        ) : (
                            <Typography color="text.secondary">No skills extracted yet.</Typography>
                        )}
                    </Box>

                    <Box>
                        <Typography variant="h6" gutterBottom>Recommended Jobs</Typography>

                        {loading && !response ? (
                            <Box sx={{ display: 'grid', gridTemplateColumns: { xs: '1fr', sm: '1fr 1fr' }, gap: 2 }}>
                                {[1, 2, 3].map((i) => (
                                    <Skeleton key={i} variant="rectangular" height={120} />
                                ))}
                            </Box>
                        ) : (
                            <Box sx={{ display: 'grid', gridTemplateColumns: { xs: '1fr', sm: '1fr 1fr' }, gap: 2 }}>
                                {response?.recommended_jobs?.length ? (
                                    response.recommended_jobs.map((job) => (
                                        <RecommendedJobCard
                                            key={`${job.job_id}-${job.company}`}
                                            job={job}
                                        />
                                    ))
                                ) : (
                                    <Typography color="text.secondary">No recommended jobs yet.</Typography>
                                )}
                            </Box>
                        )}

                    </Box>

                </Box>

            </Box>

            <Snackbar open={openSnackbar} autoHideDuration={5000} onClose={() => setOpenSnackbar(false)}>
                {error ? (
                    <Alert severity="error" onClose={() => setOpenSnackbar(false)}>{error}</Alert>
                ) : (
                    <Alert severity="success" onClose={() => setOpenSnackbar(false)}>Resume processed successfully</Alert>
                )}
            </Snackbar>

        </Paper>

    );

}
