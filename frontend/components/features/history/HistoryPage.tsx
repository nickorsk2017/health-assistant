"use client";

import { useState } from "react";
import { Sparkles } from "lucide-react";

import Alert from "@/components/common/Alert/Alert";
import Card from "@/components/common/Card/Card";
import { useRole } from "@/contexts/RoleContext";

import AddHistoryByPromptModal from "./AddHistoryByPromptModal";
import HistoryList from "./HistoryList";
import VisitForm from "./VisitForm";

export default function HistoryPage() {
  const { role } = useRole();
  const isDoctor = role === "doctor";
  const [modalOpen, setModalOpen] = useState(false);
  const [promptSuccess, setPromptSuccess] = useState(false);

  const handleSuccess = () => {
    setModalOpen(false);
    setPromptSuccess(true);
  };

  return (
    <div className="flex flex-col gap-6">
      <div className="flex items-start justify-between gap-4">
        <div>
          <h1 className="text-xl font-semibold text-slate-800">
            {isDoctor ? "Clinic History" : "My Health History"}
          </h1>
          <p className="mt-1 text-sm text-slate-500">
            {isDoctor
              ? "Record SOAP notes and review visit history."
              : "View your health visit records."}
          </p>
        </div>
        {isDoctor && (
          <button
            type="button"
            onClick={() => setModalOpen(true)}
            className="inline-flex animate-breathe cursor-pointer items-center gap-2 rounded-lg bg-violet-600 px-4 py-2 text-sm font-medium text-white will-change-transform hover:scale-105 hover:brightness-110 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-violet-500 focus-visible:ring-offset-1"
          >
            <Sparkles className="h-4 w-4" />
            Add history by prompt
          </button>
        )}
      </div>

      {promptSuccess && (
        <Alert
          variant="success"
          message="Visit records saved successfully. The history list has been refreshed."
          onDismiss={() => setPromptSuccess(false)}
        />
      )}

      {isDoctor ? (
        <div className="grid grid-cols-1 gap-6 xl:grid-cols-2">
          <Card className="p-6">
            <h2 className="mb-4 text-base font-semibold text-slate-700">New Visit</h2>
            <VisitForm />
          </Card>
          <Card className="p-6">
            <h2 className="mb-4 text-base font-semibold text-slate-700">Visit Records</h2>
            <HistoryList />
          </Card>
        </div>
      ) : (
        <Card className="p-6">
          <HistoryList />
        </Card>
      )}

      <AddHistoryByPromptModal
        isOpen={modalOpen}
        onClose={() => setModalOpen(false)}
        onSuccess={handleSuccess}
      />
    </div>
  );
}
