// fetch information about current user
export const fetchUser = async () => {
    const res = await fetch("/api/me", { credentials: "include" });
    if (!res.ok) throw new Error('Failed to fetch user');
    return res.json();
};

// fech information about all reviews in a database
export const fetchAllColleagues = async () => {
    const res = await fetch("/api/users", { credentials: "include" });
    if (!res.ok) throw new Error('Failed to fetch colleagues');
    return res.json();
}

export const login = async (email: string, password: string) => {
    const response = await fetch("/api/auth/login", {
        method: "POST",
        credentials: "include",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ email, password }),
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.message);
    return data;
};
