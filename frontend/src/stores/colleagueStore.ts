import { create } from "zustand";
import { persist, createJSONStorage } from "zustand/middleware";
import type { ColleagueType } from "../types/colleague";

type State = {
  colleagues: ColleagueType[];
  setColleagues: (colleagues: ColleagueType[]) => void;
  clearColleagues: () => void;
};

export const useColleagueStore = create<State>()(
  persist(
    (set) => ({
      colleagues: [],
      setColleagues: (colleagues) => set({ colleagues }),
      clearColleagues: () => set({ colleagues: [] }),
    }),
    {
      name: "colleague-storage",
      storage: createJSONStorage(() => localStorage),
    }
  )
);