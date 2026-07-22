import {
    createContext,
    useContext,
    useEffect,
    useState,
    type ReactNode,
} from "react";

type Mode = "light" | "dark";

interface ThemeContextValue {
    mode: Mode;
    toggle: () => void;
}

const ThemeContext = createContext<ThemeContextValue | undefined>(undefined);

interface ThemeProviderWrapperProps {
    children: ReactNode;
}

export function ThemeProviderWrapper({
    children,
}: ThemeProviderWrapperProps) {

    const [mode, setMode] = useState<Mode>(() => {

        const stored = localStorage.getItem("themeMode");

        return stored === "dark"
            ? "dark"
            : "light";

    });

    useEffect(() => {

        localStorage.setItem(
            "themeMode",
            mode
        );

    }, [mode]);

    function toggle() {

        setMode((previous) =>
            previous === "light"
                ? "dark"
                : "light"
        );

    }

    return (
        <ThemeContext.Provider
            value={{
                mode,
                toggle,
            }}
        >
            {children}
        </ThemeContext.Provider>
    );
}

export function useThemeMode() {

    const context = useContext(ThemeContext);

    if (!context) {

        throw new Error(
            "useThemeMode must be used inside ThemeProviderWrapper"
        );

    }

    return context;

}

export default ThemeProviderWrapper;