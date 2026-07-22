 import { Button } from "@mui/material";

interface Props {
    onFileSelected: (file: File) => void;
}

export default function FileUpload({ onFileSelected }: Props) {
    return (
        <Button
            variant="contained"
            component="label"
            aria-label="Choose a PDF or Word resume file"
        >
            Select Resume

            <input
                hidden
                type="file"
                accept=".pdf,.doc,.docx"
                onChange={(e) => {
                    const file = e.target.files?.[0];

                    if (file) {
                        onFileSelected(file);
                    }
                }}
            />
        </Button>
    );
}
