// get all reviews
export const fetchAllReviews = async () => {
    const res = await fetch("/api/reviews", { credentials: "include" });
    if (!res.ok) throw new Error('Failed to fetch reviews');
    
    const data = await res.json();
    if (!Array.isArray(data)) throw new Error('Unexpected data format');
    return data;
}

// create review
export const createReview = async (reviewData: any) => {
  const response = await fetch("/api/reviews", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(reviewData),
  });
  const data = await response.json();
  if (!response.ok) throw new Error(data.message);
  return data;
};
