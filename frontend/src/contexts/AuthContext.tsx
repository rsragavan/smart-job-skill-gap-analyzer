import { createContext, useCallback, useContext, useEffect, useMemo, useState, type ReactNode } from "react";
import api from "../api/api";

export type AuthUser = { id: number; full_name: string; email: string; role: "admin" | "user"; is_active: boolean; created_at: string; updated_at: string; last_login: string | null };
type Tokens = { access_token: string; refresh_token: string; user: AuthUser };
type AuthContextValue = { user: AuthUser | null; ready: boolean; login: (email: string, password: string) => Promise<void>; register: (fullName: string, email: string, password: string, confirmPassword: string) => Promise<void>; logout: () => Promise<void> };
const AuthContext = createContext<AuthContextValue | undefined>(undefined);

const storage = { get: () => localStorage.getItem("auth"), set: (value: string) => localStorage.setItem("auth", value), clear: () => localStorage.removeItem("auth") };

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<AuthUser | null>(null); const [ready, setReady] = useState(false);
  const clear = useCallback(() => { storage.clear(); delete api.defaults.headers.common.Authorization; setUser(null); }, []);
  const save = useCallback((tokens: Tokens) => { api.defaults.headers.common.Authorization = `Bearer ${tokens.access_token}`; storage.set(JSON.stringify(tokens)); setUser(tokens.user); }, []);
  useEffect(() => {
    const restore = async () => {
      const raw = storage.get();
      if (!raw) { setReady(true); return; }
      try {
        save(JSON.parse(raw) as Tokens);
        const { data } = await api.get<AuthUser>("/auth/me");
        const tokens = JSON.parse(raw) as Tokens;
        save({ ...tokens, user: data });
      } catch { clear(); }
      setReady(true);
    };
    void restore();
  }, [clear, save]);
  useEffect(() => { const onExpired = () => clear(); window.addEventListener("auth:expired", onExpired); return () => window.removeEventListener("auth:expired", onExpired); }, [clear]);
  const login = async (email: string, password: string) => { const { data } = await api.post<Tokens>("/auth/login", { email, password }); save(data); };
  const register = async (full_name: string, email: string, password: string, confirm_password: string) => { const { data } = await api.post<Tokens>("/auth/register", { full_name, email, password, confirm_password }); save(data); };
  const logout = async () => { const raw = storage.get(); try { if (raw) await api.post("/auth/logout", { refresh_token: (JSON.parse(raw) as Tokens).refresh_token }); } finally { clear(); } };
  const value = useMemo(() => ({ user, ready, login, register, logout }), [user, ready, login, register, logout]);
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
export const useAuth = () => { const value = useContext(AuthContext); if (!value) throw new Error("useAuth must be used inside AuthProvider"); return value; };
