"use client";

import { create } from "zustand";

import { AppointmentService } from "@/services/AppointmentService";

type State = {
  appointments: Entity.Appointment[];
  isFetching: boolean;
  isCreating: boolean;
  fetchError: string | null;
  createError: string | null;
  fetchAppointments: (userId: string) => Promise<void>;
  createAppointment: (form: Entity.CreateAppointment) => Promise<boolean>;
  clearCreateError: () => void;
  clearFetchError: () => void;
};

export const useAppointmentStore = create<State>((set, get) => ({
  appointments: [],
  isFetching: false,
  isCreating: false,
  fetchError: null,
  createError: null,

  fetchAppointments: async (userId) => {
    set({ isFetching: true, fetchError: null });
    try {
      const appointments = await AppointmentService.getAll(userId);
      set({ appointments, isFetching: false });
    } catch (err) {
      set({ isFetching: false, fetchError: (err as Error).message });
    }
  },

  createAppointment: async (form) => {
    set({ isCreating: true, createError: null });
    try {
      await AppointmentService.create(form);
      await get().fetchAppointments(form.user_id);
      set({ isCreating: false });
      return true;
    } catch (err) {
      set({ isCreating: false, createError: (err as Error).message });
      return false;
    }
  },

  clearCreateError: () => set({ createError: null }),
  clearFetchError: () => set({ fetchError: null }),
}));
