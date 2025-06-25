import { useQuery } from '@tanstack/react-query';
import { fetchAllColleagues } from '../api/auth';
import { useColleagueStore } from '../../stores/colleagueStore';
import { useEffect } from 'react';
import type { ColleagueType } from '../../types/colleague';

export const useColleagues = () => {
  const setColleagues = useColleagueStore((s) => s.setColleagues);

  const {
    data,
    error,
    isLoading,
    isError,
    status,
  } = useQuery<ColleagueType[]>({
    queryKey: ['colleagues'],
    queryFn: fetchAllColleagues,
    staleTime: 5 * 60 * 1000,
    retry: 1,
    refetchOnWindowFocus: false,
  });

  useEffect(() => {
    if (status === 'success' && data) {
      setColleagues(data);
    }
  }, [data, status, setColleagues]);

  return { data, error, isLoading, isError };
};
