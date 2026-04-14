"use client";

import { useState } from "react";
import { Stethoscope, TrendingUp, FileText, ListChecks } from "lucide-react";

import Alert from "@/components/common/Alert/Alert";
import Button from "@/components/common/Button/Button";
import Card from "@/components/common/Card/Card";
import Input from "@/components/common/Input/Input";
import Spinner from "@/components/common/Spinner/Spinner";
import { useDiagnosisStore } from "@/stores/useDiagnosisStore";
import { usePatientStore } from "@/stores/usePatientStore";

function TreatmentList({ raw }: { raw: string }) {
  const steps = raw
    .split(/\n|(?<=\.)\s+(?=\d)/)
    .map((s) => s.replace(/^\d+\.\s*/, "").trim())
    .filter(Boolean);

  return (
    <ol className="flex flex-col gap-2">
      {steps.map((step, i) => (
        <li key={i} className="flex gap-3 text-sm text-slate-700">
          <span className="flex h-5 w-5 shrink-0 items-center justify-center rounded-full bg-blue-100 text-xs font-semibold text-blue-700">
            {i + 1}
          </span>
          {step}
        </li>
      ))}
    </ol>
  );
}

export default function DiagnosisPage() {
  const { selectedPatientId } = usePatientStore();
  const { consultation, isLoading, error, fetchDiagnosis, clearError } = useDiagnosisStore();
  const [startDate, setStartDate] = useState("2024-01-01");

  return (
    <div className="flex flex-col gap-6">
      <div>
        <h1 className="text-xl font-semibold text-slate-800">General Practitioner Diagnosis</h1>
        <p className="mt-1 text-sm text-slate-500">
          Synthesised GP recommendation based on specialist consilium.
        </p>
      </div>

      <div className="flex flex-wrap items-end gap-3 rounded-xl border border-slate-200 bg-white p-4">
        <Input
          label="Synthesise visits from"
          type="date"
          value={startDate}
          onChange={setStartDate}
          className="w-44"
        />
        <Button
          loading={isLoading}
          onClick={() => {if(selectedPatientId) fetchDiagnosis(selectedPatientId, startDate)}}
          size="lg"
        >
          <Stethoscope className="h-4 w-4" />
          Get GP Recommendation
        </Button>
      </div>

      {error && <Alert message={error} onDismiss={clearError} />}

      {isLoading && (
        <div className="flex flex-col items-center gap-4 py-16">
          <Spinner size="lg" />
          <p className="text-sm text-slate-500">Running GP synthesis…</p>
        </div>
      )}

      {!isLoading && consultation && (
        <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
          <Card accent="border-t-blue-500" className="p-6 lg:col-span-2">
            <div className="flex items-center gap-2 mb-3">
              <Stethoscope className="h-5 w-5 text-blue-600" />
              <h2 className="text-base font-semibold text-slate-800">Final Diagnosis</h2>
            </div>
            <p className="text-lg font-medium text-blue-700">{consultation.diagnosis}</p>
          </Card>

          <Card className="p-6">
            <div className="flex items-center gap-2 mb-4">
              <ListChecks className="h-5 w-5 text-green-600" />
              <h2 className="text-base font-semibold text-slate-800">Treatment Plan</h2>
            </div>
            <TreatmentList raw={consultation.treatment} />
          </Card>

          <Card accent="border-t-amber-400" className="p-6">
            <div className="flex items-center gap-2 mb-3">
              <TrendingUp className="h-5 w-5 text-amber-500" />
              <h2 className="text-base font-semibold text-slate-800">Prognosis</h2>
            </div>
            <p className="text-sm leading-relaxed text-slate-700">{consultation.prognosis}</p>
          </Card>

          <Card className="p-6 lg:col-span-2">
            <div className="flex items-center gap-2 mb-3">
              <FileText className="h-5 w-5 text-slate-500" />
              <h2 className="text-base font-semibold text-slate-800">Doctor&apos;s Summary</h2>
            </div>
            <p className="text-sm leading-relaxed text-slate-700">{consultation.summary}</p>
          </Card>
        </div>
      )}

      {!isLoading && !consultation && !error && (
        <p className="text-center text-sm text-slate-400 py-6">
          No recommendation yet. Select a date range and request a GP consultation.
        </p>
      )}
    </div>
  );
}
