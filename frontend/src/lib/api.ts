// fetch information about current user
export const fetchUser = async () => {
    const res = await fetch("/api/me", { credentials: "include" });
    if (!res.ok) throw new Error('Failed to fetch user');
    return res.json();
};

// fech information about all reviews in a database
export const fetchAllReviews = async () => {
    const res = await fetch("/api/reviews", { credentials: "include" });
    if (!res.ok) throw new Error('Failed to fetch reviews');
    return res.json();
}

// fech information about all reviews in a database
export const fetchAllColleagues = async () => {
    const res = await fetch("/api/users", { credentials: "include" });
    if (!res.ok) throw new Error('Failed to fetch colleagues');
    return res.json();
}