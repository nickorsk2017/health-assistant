"use client";

import { useState } from "react";
import { Sparkles } from "lucide-react";

import Card from "@/components/common/Card/Card";
import { useRole } from "@/contexts/RoleContext";

import AnalysisForm from "./AnalysisForm";
import AnalysisList from "./AnalysisList";
import ImportLabsModal from "./ImportLabsModal";

export default function AnalysesPage() {
  const { role } = useRole();
  const isDoctor = role === "doctor";
  const [importOpen, setImportOpen] = useState(false);

  return (
    <div className="flex flex-col gap-6">
      <div className="flex items-start justify-between">
        <div>
          <h1 className="text-xl font-semibold text-slate-800">
            {isDoctor ? "Laboratory Analyses" : "My Lab Results"}
          </h1>
          <p className="mt-1 text-sm text-slate-500">
            {isDoctor
              ? "Record lab results and review the patient's analysis history."
              : "View your laboratory analysis records."}
          </p>
        </div>
        {isDoctor && (
          <button
            type="button"
            onClick={() => setImportOpen(true)}
            className="inline-flex animate-breathe cursor-pointer items-center gap-2 rounded-lg bg-violet-600 px-4 py-2 text-sm font-medium text-white will-change-transform hover:scale-105 hover:brightness-110 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-violet-500 focus-visible:ring-offset-1"
          >
            <Sparkles className="h-4 w-4" />
            Add Labs by prompt
          </button>
        )}
      </div>

      {isDoctor ? (
        <div className="grid grid-cols-1 gap-6 xl:grid-cols-2">
          <Card className="p-6">
            <h2 className="mb-4 text-base font-semibold text-slate-700">New Analysis</h2>
            <AnalysisForm />
          </Card>

          <Card className="p-6">
            <h2 className="mb-4 text-base font-semibold text-slate-700">Analysis History</h2>
            <AnalysisList />
          </Card>
        </div>
      ) : (
        <Card className="p-6">
          <AnalysisList />
        </Card>
      )}

      <ImportLabsModal isOpen={importOpen} onClose={() => setImportOpen(false)} />
    </div>
  );
}
