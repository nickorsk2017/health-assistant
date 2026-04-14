"use client";

import ComplaintList from "@/components/features/complaints/ComplaintList";
import { useRole } from "@/contexts/RoleContext";
import { usePatientStore } from "@/stores/usePatientStore";

export default function ComplaintsPage() {
  const { role } = useRole();
  const { selectedPatientId } = usePatientStore();

  const isDoctor = role === "doctor";
  const userId = selectedPatientId ?? "";

  if (!selectedPatientId) {
    return (
      <div className="flex items-center justify-center py-20 text-sm text-slate-500">
        Select a patient to view complaints.
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-6 p-6">
      <ComplaintList userId={userId} isDoctor={isDoctor} />
    </div>
  );
}
