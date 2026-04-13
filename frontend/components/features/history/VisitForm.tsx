"use client";

import { useState } from "react";

import Alert from "@/components/common/Alert/Alert";
import Button from "@/components/common/Button/Button";
import Input from "@/components/common/Input/Input";
import Select from "@/components/common/Select/Select";
import TextArea from "@/components/common/TextArea/TextArea";
import { usePatientStore } from "@/stores/usePatientStore";
import { useVisitStore } from "@/stores/useVisitStore";

const DOCTOR_OPTIONS = [
  { value: "oncology", label: "Oncology" },
  { value: "gastroenterology", label: "Gastroenterology" },
  { value: "cardiology", label: "Cardiology" },
  { value: "hematology", label: "Hematology" },
  { value: "nephrology", label: "Nephrology" },
  { value: "nutrition", label: "Nutrition" },
  { value: "endocrinology", label: "Endocrinology" },
  { value: "mental_health", label: "Mental Health" },
  { value: "pulmonology", label: "Pulmonology" },
  { value: "general_practitioner", label: "General Practitioner" },
];

const TODAY = new Date().toISOString().split("T")[0];

const EMPTY = {
  doctor_type: "oncology" as Entity.DoctorType,
  visit_at: TODAY,
  subjective: "",
  objective: "",
  assessment: "",
  plan: "",
};

export default function VisitForm() {
  const { selectedPatientId } = usePatientStore();
  const { isSubmitting, error, submitVisit, clearError } = useVisitStore();
  const [form, setForm] = useState(EMPTY);
  const [success, setSuccess] = useState(false);

  const set = (key: keyof typeof EMPTY, value: string) =>
    setForm((prev) => ({ ...prev, [key]: value }));

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSuccess(false);
    const ok = await submitVisit({ ...form, user_id: selectedPatientId! });
    if (ok) {
      setSuccess(true);
      setForm(EMPTY);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-4">
      <div className="grid grid-cols-2 gap-4">
        <Select
          label="Specialty"
          value={form.doctor_type}
          options={DOCTOR_OPTIONS}
          onChange={(v) => set("doctor_type", v)}
        />
        <Input
          label="Visit Date"
          type="date"
          value={form.visit_at}
          min="2025-01-01"
          max={TODAY}
          onChange={(v) => set("visit_at", v)}
        />
      </div>
      <TextArea
        label="Subjective — Patient complaints & history"
        value={form.subjective}
        placeholder="Chief complaint, history of present illness..."
        onChange={(v) => set("subjective", v)}
      />
      <TextArea
        label="Objective — Clinical findings & vitals"
        value={form.objective}
        placeholder="Physical examination, lab results, vitals..."
        onChange={(v) => set("objective", v)}
      />
      <TextArea
        label="Assessment — Clinical impression"
        value={form.assessment}
        placeholder="Diagnosis or differential diagnosis..."
        onChange={(v) => set("assessment", v)}
      />
      <TextArea
        label="Plan — Treatment & next steps"
        value={form.plan}
        placeholder="Medications, follow-up, referrals..."
        onChange={(v) => set("plan", v)}
      />
      {error && <Alert message={error} onDismiss={clearError} />}
      {success && (
        <Alert variant="success" message="Visit recorded successfully." onDismiss={() => setSuccess(false)} />
      )}
      <Button type="submit" loading={isSubmitting} className="self-end">
        Save Visit
      </Button>
    </form>
  );
}
