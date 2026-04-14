"use client";

import { useState } from "react";

import Alert from "@/components/common/Alert/Alert";
import Button from "@/components/common/Button/Button";
import Input from "@/components/common/Input/Input";
import Modal from "@/components/common/Modal/Modal";
import { usePatientStore } from "@/stores/usePatientStore";

const TODAY = new Date().toISOString().split("T")[0];

type Props = {
  isOpen: boolean;
};

const GENDER_OPTIONS: { value: Entity.Gender; label: string }[] = [
  { value: "male", label: "Male" },
  { value: "female", label: "Female" },
  { value: "other", label: "Other" },
];

export default function PatientRegistrationModal({ isOpen }: Props) {
  const { isCreating, createError, registerAsPatient, clearCreateError } = usePatientStore();
  const [form, setForm] = useState<Entity.NewPatientForm>({
    name: "",
    date_of_birth: "",
    gender: "male",
    email: "",
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await registerAsPatient(form);
  };

  return (
    <Modal isOpen={isOpen} title="Create Your Profile" onClose={() => {}} closable={false} className="max-w-lg">
      <p className="mb-4 text-sm text-slate-500">
        Set up your patient profile to access your health records.
      </p>
      <form onSubmit={handleSubmit} className="flex flex-col gap-4">
        <Input
          label="Full Name"
          value={form.name}
          placeholder="Your full name"
          onChange={(v) => setForm((p) => ({ ...p, name: v }))}
        />
        <Input
          label="Date of Birth"
          type="date"
          value={form.date_of_birth}
          max={TODAY}
          onChange={(v) => setForm((p) => ({ ...p, date_of_birth: v }))}
        />
        <div className="flex flex-col gap-1.5">
          <label className="text-xs font-medium text-slate-600">Gender</label>
          <select
            value={form.gender}
            onChange={(e) => setForm((p) => ({ ...p, gender: e.target.value as Entity.Gender }))}
            className="rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm text-slate-800 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/20"
          >
            {GENDER_OPTIONS.map((o) => (
              <option key={o.value} value={o.value}>
                {o.label}
              </option>
            ))}
          </select>
        </div>
        <Input
          label="Email"
          type="email"
          value={form.email}
          placeholder="your@email.com"
          onChange={(v) => setForm((p) => ({ ...p, email: v }))}
        />
        {createError && <Alert message={createError} onDismiss={clearCreateError} />}
        <Button type="submit" loading={isCreating} className="mt-1">
          Create Profile
        </Button>
      </form>
    </Modal>
  );
}
