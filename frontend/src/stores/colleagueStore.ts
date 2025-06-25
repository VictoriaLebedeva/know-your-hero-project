import { create } from 'zustand';
import type { ColleagueType } from '../types/colleagues';

type State = {
    colleagues: ColleagueType[];
    setColleagues: (colleagues: ColleagueType[]) => void;
    clearColleagues: () => void;
};

export const useColleagueStore = create<State>((set) => ({
    colleagues: [],
    setColleagues: (colleagues) => set({ colleagues }),
    clearColleagues: () => set({ colleagues: [] }),
}));
