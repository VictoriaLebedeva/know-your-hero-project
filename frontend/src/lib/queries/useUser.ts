import { useQuery } from "@tanstack/react-query";
import { fetchUser } from "@/lib/api/auth";
import { useUserStore } from "../../stores/userStore";
import { useEffect } from "react";
import type { CurrentUserType } from "../../types/user";

export const useUser = () => {
  const setUser = useUserStore((s) => s.setUser);

  const {
    data,
    error,
    isLoading,
    isError,
    status,
  } = useQuery<CurrentUserType>({
    queryKey: ['user'],
    queryFn: fetchUser,
    staleTime: 5 * 60 * 1000,
    retry: 1,
    refetchOnWindowFocus: false,
  });

  useEffect(() => {
    if (status === 'success' && data) {
      setUser(data);
    }
  }, [data, status, setUser]);

  return { data, error, isLoading, isError };
};