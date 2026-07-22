import {
    TextField,
    InputAdornment,
    IconButton,
} from "@mui/material";

import SearchIcon from "@mui/icons-material/Search";
import ClearIcon from "@mui/icons-material/Clear";

interface Props {
    value: string;
    onChange: (value: string) => void;
    onSearch?: () => void;
}

export default function SearchBar({
    value,
    onChange,
    onSearch,
}: Props) {
    return (
        <TextField
            fullWidth
            variant="outlined"
            placeholder="Search jobs by title, company or location"
            value={value}
            onChange={(e) => onChange(e.target.value)}
            onKeyDown={(e) => {
                if (e.key === "Enter") {
                    onSearch?.();
                }
            }}
            slotProps={{
                input: {
                    endAdornment: (
                        <InputAdornment position="end">
                            {value.length > 0 && (
                                <IconButton
                                    size="small"
                                    onClick={() => onChange("")}
                                >
                                    <ClearIcon />
                                </IconButton>
                            )}

                            <IconButton
                                size="small"
                                onClick={() => onSearch?.()}
                            >
                                <SearchIcon />
                            </IconButton>
                        </InputAdornment>
                    ),
                },
            }}
        />
    );
}