"use client";

import { useState } from "react";

import Button from "@/components/common/Button/Button";
import Input from "@/components/common/Input/Input";
import Modal from "@/components/common/Modal/Modal";
import TextArea from "@/components/common/TextArea/TextArea";
import { useAppointmentStore } from "@/stores/useAppointmentStore";
import { useComplaintStore } from "@/stores/useComplaintStore";

const DOCTOR_TYPES = [
  "General Practitioner",
  "Cardiologist",
  "Endocrinologist",
  "Neurologist",
  "Pulmonologist",
  "Gastroenterologist",
  "Dermatologist",
  "Orthopedist",
  "Psychiatrist",
  "Other",
];

type Props = {
  isOpen: boolean;
  complaint: Entity.Complaint;
  onClose: () => void;
};

export default function ScheduleAppointmentModal({ isOpen, complaint, onClose }: Props) {
  const { isCreating, createError, createAppointment, clearCreateError } = useAppointmentStore();
  const { markRead } = useComplaintStore();
  const [appointmentDate, setAppointmentDate] = useState("");
  const [doctorType, setDoctorType] = useState(DOCTOR_TYPES[0]);
  const [problemNotes, setProblemNotes] = useState("");

  const handleClose = () => {
    setAppointmentDate("");
    setDoctorType(DOCTOR_TYPES[0]);
    setProblemNotes("");
    clearCreateError();
    onClose();
  };

  const handleSubmit = async () => {
    if (!appointmentDate || !doctorType) return;
    const ok = await createAppointment({
      complaint_id: complaint.complaint_id,
      user_id: complaint.user_id,
      appointment_date: appointmentDate,
      doctor_type: doctorType,
      problem_notes: problemNotes.trim(),
    });
    if (ok) {
      await markRead(complaint.complaint_id, complaint.user_id);
      handleClose();
    }
  };

  return (
    <Modal isOpen={isOpen} title="Schedule Appointment" onClose={handleClose} className="max-w-lg">
      <div className="flex flex-col gap-4">
        <div className="rounded-lg border border-slate-100 bg-slate-50 px-4 py-3">
          <p className="text-xs font-medium text-slate-500">Complaint</p>
          <p className="mt-0.5 text-sm text-slate-700">{complaint.problem_health}</p>
        </div>

        <div className="flex flex-col gap-1">
          <label htmlFor="doctor-type" className="text-sm font-medium text-slate-700">
            Doctor Type
          </label>
          <select
            id="doctor-type"
            value={doctorType}
            onChange={(e) => setDoctorType(e.target.value)}
            className="rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm text-slate-800 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/20"
          >
            {DOCTOR_TYPES.map((t) => (
              <option key={t} value={t}>
                {t}
              </option>
            ))}
          </select>
        </div>

        <Input
          label="Appointment Date & Time"
          id="appointment-date"
          type="datetime-local"
          value={appointmentDate}
          onChange={setAppointmentDate}
        />

        <TextArea
          label="Notes (optional)"
          id="problem-notes"
          value={problemNotes}
          placeholder="Any additional context for the appointment..."
          rows={3}
          onChange={setProblemNotes}
        />

        {createError && <p className="text-sm text-red-600">{createError}</p>}

        <div className="flex justify-end gap-2 pt-1">
          <Button variant="secondary" onClick={handleClose} disabled={isCreating}>
            Cancel
          </Button>
          <Button
            onClick={handleSubmit}
            loading={isCreating}
            disabled={!appointmentDate || !doctorType}
          >
            Schedule
          </Button>
        </div>
      </div>
    </Modal>
  );
}
