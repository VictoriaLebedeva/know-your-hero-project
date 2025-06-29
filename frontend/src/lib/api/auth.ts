// get informaton abot current user
export const fetchUser = async () => {
  try {
    const res = await fetch("/api/me", { credentials: "include" });

    if (res.status === 401) {
      try {
        await refreshToken();
        const retryRes = await fetch("/api/me", { credentials: "include" });
        if (!retryRes.ok) throw new Error("Failed to fetch user after refresh");
        return retryRes.json();
      } catch (refreshError) {
        throw new Error("Session expired, please log in again.");
      }
    }

    if (!res.ok) {
      throw new Error("Failed to fetch user");
    }

    return res.json();
  } catch (error: any) {
    throw error;
  }
};

// get list of all users
export const fetchAllColleagues = async () => {
  const res = await fetch("/api/users", { credentials: "include" });
  if (!res.ok) throw new Error('Failed to fetch colleagues');
  return res.json();
}

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
  if (!response.ok) throw new Error(data.message);
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
  if (!response.ok) throw new Error(data.message);
  return data;
};

// requiest refresh_token
export const refreshToken = async () => {
  const response = await fetch("/api/auth/refresh", {
    method: "POST",
    credentials: "include"
  });
  const data = await response.json();
  if (!response.ok) throw new Error(data.message);
  return data;
};
