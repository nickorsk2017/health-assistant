"use client";

import { create } from "zustand";

import { ComplaintService } from "@/services/ComplaintService";

type State = {
  complaints: Entity.Complaint[];
  isFetching: boolean;
  isSubmitting: boolean;
  fetchError: string | null;
  submitError: string | null;
  fetchComplaints: (userId: string) => Promise<void>;
  createComplaint: (userId: string, form: Entity.CreateComplaint) => Promise<boolean>;
  updateComplaint: (complaintId: string, form: Entity.UpdateComplaint, userId: string) => Promise<boolean>;
  markRead: (complaintId: string, userId: string) => Promise<void>;
  removeComplaint: (complaintId: string, userId: string) => Promise<boolean>;
  clearSubmitError: () => void;
  clearFetchError: () => void;
};

export const useComplaintStore = create<State>((set, get) => ({
  complaints: [],
  isFetching: false,
  isSubmitting: false,
  fetchError: null,
  submitError: null,

  fetchComplaints: async (userId) => {
    set({ isFetching: true, fetchError: null });
    try {
      const complaints = await ComplaintService.getAll(userId);
      set({ complaints, isFetching: false });
    } catch (err) {
      set({ isFetching: false, fetchError: (err as Error).message });
    }
  },

  createComplaint: async (userId, form) => {
    set({ isSubmitting: true, submitError: null });
    try {
      await ComplaintService.create(userId, form);
      await get().fetchComplaints(userId);
      set({ isSubmitting: false });
      return true;
    } catch (err) {
      set({ isSubmitting: false, submitError: (err as Error).message });
      return false;
    }
  },

  updateComplaint: async (complaintId, form, userId) => {
    set({ isSubmitting: true, submitError: null });
    try {
      await ComplaintService.update(complaintId, userId, form);
      await get().fetchComplaints(userId);
      set({ isSubmitting: false });
      return true;
    } catch (err) {
      set({ isSubmitting: false, submitError: (err as Error).message });
      return false;
    }
  },

  markRead: async (complaintId, userId) => {
    try {
      await ComplaintService.markRead(complaintId);
      await get().fetchComplaints(userId);
    } catch (err) {
      set({ fetchError: (err as Error).message });
    }
  },

  removeComplaint: async (complaintId, userId) => {
    set({ isSubmitting: true, submitError: null });
    try {
      await ComplaintService.remove(complaintId);
      await get().fetchComplaints(userId);
      set({ isSubmitting: false });
      return true;
    } catch (err) {
      set({ isSubmitting: false, submitError: (err as Error).message });
      return false;
    }
  },

  clearSubmitError: () => set({ submitError: null }),
  clearFetchError: () => set({ fetchError: null }),
}));
