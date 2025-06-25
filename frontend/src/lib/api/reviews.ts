// fech information about all reviews in a database
export const fetchAllReviews = async () => {
    const res = await fetch("/api/reviews", { credentials: "include" });
    if (!res.ok) throw new Error('Failed to fetch reviews');
    
    const data = await res.json();
    if (!Array.isArray(data)) throw new Error('Unexpected data format');
    return data;
}
