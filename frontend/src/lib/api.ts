// fetch information about current user
export const fetchUser = async () => {
    const res = await fetch("/api/me", { credentials: "include" });
    if (!res.ok) throw new Error('Failed to fetch user');
    return res.json();
};
