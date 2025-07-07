import { fetchWithAuth } from '@/lib/fetchUtils';

// get informaton abot current user
export const fetchUser = async () => {
  try {

    const res = await fetchWithAuth("/api/me");

    if (!res.ok) {
      const errorData = await res.json().catch(() => ({ message: "Failed to fetch user data" }));
      throw new Error(errorData.message || "Failed to fetch user data");
    }

    return res.json();

  } catch (error: any) {
    console.error("Could not fetch user:", error.message);
    throw error;
  }
};


// get list of all users
export const fetchAllColleagues = async () => {
  const res = await fetchWithAuth("/api/users");

  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.message || 'Failed to fetch colleagues');
  }

  return res.json();
};

// log in to the system
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
  if (!response.ok) throw new Error(data.error?.message || 'Unknown error');
  return data;
};

// register in the system
export const register = async (
  email: string,
  password: string,
  name: string
) => {
  const response = await fetch("/api/auth/register", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ email, password, name }),
  });
  const data = await response.json();
  if (!response.ok) throw new Error(data.error?.message || 'Unknown error');
  return data;
};

// requiest refresh_token
export const refreshToken = async () => {
  const response = await fetch("/api/auth/refresh", {
    method: "POST",
    credentials: "include"
  });
  const data = await response.json();
  if (!response.ok) throw new Error(data.error?.message || 'Unknown error');
  return data;
};
