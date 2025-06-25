import { create } from 'zustand';
import type { CurrentUserType } from '../types/user';

type State = {
  user: CurrentUserType | null;
  setUser: (user: CurrentUserType) => void;
  clearUser: () => void;
};

export const useUserStore = create<State>((set) => ({
  user: null,
  setUser: (user) => set({ user }),
  clearUser: () => set({ user: null }),
}));