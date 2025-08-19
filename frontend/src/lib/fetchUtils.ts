import { refreshToken } from '@/lib/api/auth';
import { toast } from 'sonner';

let isRefreshing = false;

let failedQueue: (() => void)[] = [];

// processes all queued requests after token refresh attempt
const processQueue = (error: Error | null) => {
    failedQueue.forEach(prom => {
        prom();
    });
    failedQueue = [];
};

export const fetchWithAuth = async (url: string, options: RequestInit = {}): Promise<Response> => {
    const optionsWithCreds = {
        ...options,
        credentials: "include" as const,
    };

    let response = await fetch(url, optionsWithCreds);

    // if unauthorized, try to refresh token
    if (response.status === 401) {
        if (!isRefreshing) {
            isRefreshing = true;
            try {
                await refreshToken();
                processQueue(null);

                console.log("Tokens refreshed, retrying original request...");
                // retry the original request after successful refresh
                return fetch(url, optionsWithCreds);

            } catch (error) {
                console.error("Session expired. Could not refresh token.", error);
                processQueue(error as Error);

                sessionStorage.setItem('flash:sessionExpired', '1');
                await fetch('/api/auth/logout', { method: 'POST', credentials: 'include' });

                window.location.href = '/login'; // hard redirect to login page
                throw error;

            } finally {
                isRefreshing = false;
            }
        } else {
            return new Promise((resolve) => {
                failedQueue.push(() => {
                    resolve(fetchWithAuth(url, options));
                });
            });
        }
    }

    return response;
};
