"use client";

import { useEffect, useState } from "react";
import { Trash2 } from "lucide-react";

import Alert from "@/components/common/Alert/Alert";
import Button from "@/components/common/Button/Button";
import Input from "@/components/common/Input/Input";
import Modal from "@/components/common/Modal/Modal";
import TextArea from "@/components/common/TextArea/TextArea";
import { useVisitStore } from "@/stores/useVisitStore";

type Props = {
  visit: Entity.VisitRecord;
  isOpen: boolean;
  onClose: () => void;
};

const TODAY = new Date().toISOString().split("T")[0];

export default function EditVisitModal({ visit, isOpen, onClose }: Props) {
  const { isUpdating, isDeleting, editError, updateVisit, deleteVisit, clearEditError } = useVisitStore();
  const [form, setForm] = useState<Entity.UpdateVisit>({
    visit_at: visit.visit_at,
    subjective: visit.subjective,
    objective: visit.objective,
    assessment: visit.assessment,
    plan: visit.plan,
  });
  const [confirmDelete, setConfirmDelete] = useState(false);

  useEffect(() => {
    if (isOpen) {
      setForm({
        visit_at: visit.visit_at,
        subjective: visit.subjective,
        objective: visit.objective,
        assessment: visit.assessment,
        plan: visit.plan,
      });
      setConfirmDelete(false);
      clearEditError();
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isOpen]);

  const set = (key: keyof Entity.UpdateVisit, value: string) =>
    setForm((prev) => ({ ...prev, [key]: value }));

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const ok = await updateVisit(visit.visit_id, form);
    if (ok) onClose();
  };

  const handleDelete = async () => {
    if (!confirmDelete) {
      setConfirmDelete(true);
      return;
    }
    const ok = await deleteVisit(visit.visit_id);
    if (ok) onClose();
  };

  return (
    <Modal isOpen={isOpen} title="Edit Visit" onClose={onClose} className="max-w-2xl">
      <form onSubmit={handleSubmit} className="flex flex-col gap-4">
        <Input
          label="Visit Date"
          type="date"
          value={form.visit_at}
          min="2025-01-01"
          max={TODAY}
          onChange={(v) => set("visit_at", v)}
        />
        <TextArea
          label="Subjective — Patient complaints & history"
          value={form.subjective}
          onChange={(v) => set("subjective", v)}
        />
        <TextArea
          label="Objective — Clinical findings & vitals"
          value={form.objective}
          onChange={(v) => set("objective", v)}
        />
        <TextArea
          label="Assessment — Clinical impression"
          value={form.assessment}
          onChange={(v) => set("assessment", v)}
        />
        <TextArea
          label="Plan — Treatment & next steps"
          value={form.plan}
          onChange={(v) => set("plan", v)}
        />
        {editError && <Alert message={editError} onDismiss={clearEditError} />}
        <div className="flex items-center justify-between border-t border-slate-100 pt-4">
          <Button
            type="button"
            variant="ghost"
            loading={isDeleting}
            onClick={handleDelete}
            className={
              confirmDelete
                ? "text-red-600 bg-red-100 hover:bg-red-200"
                : "text-red-500 bg-red-50 hover:bg-red-100"
            }
          >
            <Trash2 className="h-4 w-4" />
            {confirmDelete ? "Confirm Delete" : "Delete"}
          </Button>
          <div className="flex items-center gap-2">
            <Button variant="ghost" type="button" onClick={onClose}>
              Cancel
            </Button>
            <Button type="submit" loading={isUpdating}>
              Save Changes
            </Button>
          </div>
        </div>
      </form>
    </Modal>
  );
}
