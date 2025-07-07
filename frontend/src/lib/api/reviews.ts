import { fetchWithAuth } from "@/lib/fetchUtils";

// get all reviews
export const fetchAllReviews = async () => {
  const res = await fetchWithAuth("/api/reviews");

  if (!res.ok) {
    const data = await res.json().catch(() => ({}));
    throw new Error(data.error?.message || 'Unknown error');
  }

  const data = await res.json();
  if (!Array.isArray(data)) {
    throw new Error("Unexpected data format");
  }

  return data;
};

// create review
export const createReview = async (reviewData: any) => {
  const res = await fetchWithAuth("/api/reviews", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(reviewData),
  });

  if (!res.ok) {
    const data = await res.json().catch(() => ({}));
    throw new Error(data.error?.message || 'Unknown error');
  }

  return res.json();
};
