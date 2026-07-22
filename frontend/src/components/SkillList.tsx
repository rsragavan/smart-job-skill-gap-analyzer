import { Chip, Stack } from "@mui/material";

interface Props {
    skills?: string[];
}

export default function SkillList({ skills = [] }: Props) {

    return (

        <Stack
            direction="row"
            spacing={1}
            useFlexGap
            sx={{
                flexWrap: "wrap"
            }}
        >

            {skills.map((skill) => (

                <Chip
                    key={skill}
                    label={skill}
                    color="primary"
                />

            ))}

        </Stack>

    );

}