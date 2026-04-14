"use client";

import { useState } from "react";
import { Users } from "lucide-react";

import Alert from "@/components/common/Alert/Alert";
import Button from "@/components/common/Button/Button";
import Input from "@/components/common/Input/Input";
import Spinner from "@/components/common/Spinner/Spinner";
import { useConsiliumStore } from "@/stores/useConsiliumStore";
import { usePatientStore } from "@/stores/usePatientStore";

import SpecialistCard from "./SpecialistCard";

export default function ConsiliumPage() {
  const { selectedPatientId } = usePatientStore();
  const { findings, isLoading, error, fetchConsilium, clearError } = useConsiliumStore();
  const [startDate, setStartDate] = useState("2024-01-01");

  return (
    <div className="flex flex-col gap-6">
      <div>
        <h1 className="text-xl font-semibold text-slate-800">Medical Consilium</h1>
        <p className="mt-1 text-sm text-slate-500">
          Multi-disciplinary team evaluation across 9 specialties.
        </p>
      </div>

      <div className="flex flex-wrap items-end gap-3 rounded-xl border border-slate-200 bg-white p-4">
        <Input
          label="Analyse visits from"
          type="date"
          value={startDate}
          onChange={setStartDate}
          className="w-44"
        />
        <Button
          loading={isLoading}
          onClick={() => fetchConsilium(selectedPatientId!!, startDate)}
          size="lg"
        >
          <Users className="h-4 w-4" />
          Get MDT Evaluation
        </Button>
        {isLoading && (
          <p className="text-sm text-slate-400">
            Consulting 9 specialists — this may take a moment…
          </p>
        )}
      </div>

      {error && <Alert message={error} onDismiss={clearError} />}

      {isLoading && (
        <div className="flex flex-col items-center gap-4 py-16">
          <Spinner size="lg" />
          <p className="text-sm text-slate-500">Running multi-disciplinary team evaluation…</p>
        </div>
      )}

      {!isLoading && findings.length > 0 && (
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {findings.map((f) => (
            <SpecialistCard key={f.specialty} finding={f} />
          ))}
        </div>
      )}

      {!isLoading && findings.length === 0 && !error && (
        <p className="text-center text-sm text-slate-400 py-6">
          No findings yet. Select a date range and run the MDT evaluation.
        </p>
      )}
    </div>
  );
}
