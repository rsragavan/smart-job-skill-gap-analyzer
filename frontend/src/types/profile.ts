export interface Profile {
    id: number;
    full_name: string;
    email: string;
    role: string;
    joined_date: string;
    last_login: string | null;
    uploaded_resume_count: number;
}

export interface UpdateProfileRequest {
    full_name: string;
}

export interface ChangePasswordRequest {
    current_password: string;
    new_password: string;
    confirm_password: string;
}