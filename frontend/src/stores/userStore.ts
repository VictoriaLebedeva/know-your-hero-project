import { create } from "zustand";
import { persist, createJSONStorage } from "zustand/middleware";
import type { CurrentUserType } from "../types/user";

type State = {
  user: CurrentUserType | null;
  setUser: (user: CurrentUserType) => void;
  clearUser: () => void;
};

export const useUserStore = create<State>()(
  persist(
    (set) => ({
      user: null,
      setUser: (user) => set({ user }),
      clearUser: () => set({ user: null }),
    }),
    {
      name: "user-storage",
      storage: createJSONStorage(() => localStorage),
    }
  )
);