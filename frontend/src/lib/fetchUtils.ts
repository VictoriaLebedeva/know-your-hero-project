import { refreshToken } from '@/lib/api/auth';

let isRefreshing = false;

let failedQueue: (() => void)[] = [];

// Processes all queued requests after token refresh attempt
const processQueue = (error: Error | null) => {
    failedQueue.forEach(prom => {
        // If error, you could reject the promise here if needed
        prom();
    });
    failedQueue = [];
};

// Fetch wrapper that automatically refreshes tokens on 401 and retries the request
export const fetchWithAuth = async (url: string, options: RequestInit = {}): Promise<Response> => {
    const optionsWithCreds = {
        ...options,
        credentials: "include" as const, // Always send cookies
    };

    let response = await fetch(url, optionsWithCreds);

    // If unauthorized, try to refresh token
    if (response.status === 401) {
        if (!isRefreshing) {
            isRefreshing = true;
            try {
                // Attempt to refresh tokens
                await refreshToken();
                processQueue(null);

                console.log("Tokens refreshed, retrying original request...");
                // Retry the original request after successful refresh
                return fetch(url, optionsWithCreds);

            } catch (error) {
                // If refresh fails, log out user and redirect to login
                console.error("Session expired. Could not refresh token.", error);
                processQueue(error as Error);
                window.location.href = '/login'; // Hard redirect to login page
            
                throw error;

            } finally {
                isRefreshing = false;
            }
        } else {
            // If a refresh is already in progress, queue the request
            return new Promise((resolve) => {
                failedQueue.push(() => {
                    resolve(fetchWithAuth(url, options));
                });
            });
        }
    }

    // Return the response if not 401 or after successful retry
    return response;
};
