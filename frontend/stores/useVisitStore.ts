"use client";

import { create } from "zustand";

import { VisitService } from "@/services/VisitService";

type State = {
  history: Entity.VisitRecord[];
  isSubmitting: boolean;
  isFetchingHistory: boolean;
  isProcessingPrompt: boolean;
  isUpdating: boolean;
  isDeleting: boolean;
  error: string | null;
  promptError: string | null;
  editError: string | null;
  refreshTrigger: number;
  submitVisit: (data: Entity.CreateVisit) => Promise<boolean>;
  fetchHistory: (userId: string, lastDateVisit: string) => Promise<void>;
  submitByPrompt: (data: Entity.VisitsByPromptRequest) => Promise<boolean>;
  updateVisit: (visitId: string, data: Entity.UpdateVisit) => Promise<boolean>;
  deleteVisit: (visitId: string) => Promise<boolean>;
  clearError: () => void;
  clearPromptError: () => void;
  clearEditError: () => void;
};

export const useVisitStore = create<State>((set) => ({
  history: [],
  isSubmitting: false,
  isFetchingHistory: false,
  isProcessingPrompt: false,
  isUpdating: false,
  isDeleting: false,
  error: null,
  promptError: null,
  editError: null,
  refreshTrigger: 0,

  submitVisit: async (data) => {
    set({ isSubmitting: true, error: null });
    try {
      await VisitService.recordVisit(data);
      set({ isSubmitting: false });
      return true;
    } catch (err) {
      set({ isSubmitting: false, error: (err as Error).message });
      return false;
    }
  },

  fetchHistory: async (userId, lastDateVisit) => {
    set({ isFetchingHistory: true, error: null, history: [] });
    try {
      const history = await VisitService.fetchHistory(userId, lastDateVisit);
      set({ history, isFetchingHistory: false });
    } catch (err) {
      set({ isFetchingHistory: false, error: (err as Error).message });
    }
  },

  submitByPrompt: async (data) => {
    set({ isProcessingPrompt: true, promptError: null });
    try {
      await VisitService.createByPrompt(data);
      set((s) => ({ isProcessingPrompt: false, refreshTrigger: s.refreshTrigger + 1 }));
      return true;
    } catch (err) {
      set({ isProcessingPrompt: false, promptError: (err as Error).message });
      return false;
    }
  },

  updateVisit: async (visitId, data) => {
    set({ isUpdating: true, editError: null });
    try {
      await VisitService.updateVisit(visitId, data);
      set((s) => ({ isUpdating: false, refreshTrigger: s.refreshTrigger + 1 }));
      return true;
    } catch (err) {
      set({ isUpdating: false, editError: (err as Error).message });
      return false;
    }
  },

  deleteVisit: async (visitId) => {
    set({ isDeleting: true, editError: null });
    try {
      await VisitService.deleteVisit(visitId);
      set((s) => ({ isDeleting: false, refreshTrigger: s.refreshTrigger + 1 }));
      return true;
    } catch (err) {
      set({ isDeleting: false, editError: (err as Error).message });
      return false;
    }
  },

  clearError: () => set({ error: null }),
  clearPromptError: () => set({ promptError: null }),
  clearEditError: () => set({ editError: null }),
}));
