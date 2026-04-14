"use client";

import { useEffect, useState } from "react";
import { ChevronDown, ChevronUp, Pencil } from "lucide-react";

import Alert from "@/components/common/Alert/Alert";
import Button from "@/components/common/Button/Button";
import Input from "@/components/common/Input/Input";
import Spinner from "@/components/common/Spinner/Spinner";
import EditVisitModal from "@/components/features/history/EditVisitModal";
import { useRole } from "@/contexts/RoleContext";
import { usePatientStore } from "@/stores/usePatientStore";
import { useVisitStore } from "@/stores/useVisitStore";
import formatDate from "@/utils/formatDate";

function VisitRow({
  visit,
  onEdit,
}: {
  visit: Entity.VisitRecord;
  onEdit?: (v: Entity.VisitRecord) => void;
}) {
  const [open, setOpen] = useState(false);
  return (
    <div className="border-b border-slate-100 last:border-0">
      <button
        type="button"
        onClick={() => setOpen((o) => !o)}
        className="flex w-full items-center justify-between px-4 py-3 text-left hover:bg-slate-50"
      >
        <div className="flex items-center gap-4">
          <span className="rounded-md bg-blue-50 px-2 py-0.5 text-xs font-medium capitalize text-blue-700">
            {visit.doctor_type.replace("_", " ")}
          </span>
          <span className="text-sm font-medium text-slate-800">{formatDate(visit.visit_at)}</span>
          <span className="max-w-xs truncate text-sm text-slate-500">{visit.assessment}</span>
        </div>
        <div className="flex items-center gap-2">
          {onEdit && (
            <span
              role="button"
              tabIndex={0}
              onClick={(e) => {
                e.stopPropagation();
                onEdit(visit);
              }}
              onKeyDown={(e) => {
                if (e.key === "Enter") {
                  e.stopPropagation();
                  onEdit(visit);
                }
              }}
              className="rounded p-1 text-slate-400 hover:bg-slate-200 hover:text-slate-600"
              aria-label="Edit visit"
            >
              <Pencil className="h-3.5 w-3.5" />
            </span>
          )}
          {open ? (
            <ChevronUp className="h-4 w-4 shrink-0 text-slate-400" />
          ) : (
            <ChevronDown className="h-4 w-4 shrink-0 text-slate-400" />
          )}
        </div>
      </button>
      {open && (
        <div className="grid grid-cols-2 gap-4 bg-slate-50 px-4 py-3 text-sm">
          {[
            ["Subjective", visit.subjective],
            ["Objective", visit.objective],
            ["Assessment", visit.assessment],
            ["Plan", visit.plan],
          ].map(([label, value]) => (
            <div key={label}>
              <p className="mb-1 font-medium text-slate-500">{label}</p>
              <p className="text-slate-700">{value || "—"}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default function HistoryList() {
  const { selectedPatientId } = usePatientStore();
  const { history, isFetchingHistory, error, fetchHistory, clearError, refreshTrigger } =
    useVisitStore();
  const { role } = useRole();
  const [since, setSince] = useState("2024-01-01");
  const [editingVisit, setEditingVisit] = useState<Entity.VisitRecord | null>(null);

  useEffect(() => {
    if (refreshTrigger > 0 && selectedPatientId) {
      fetchHistory(selectedPatientId, since);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [refreshTrigger]);

  return (
    <div className="flex flex-col gap-4">
      <div className="flex items-end gap-3">
        <Input
          label="Visits from"
          type="date"
          value={since}
          onChange={setSince}
          className="w-44"
        />
        <Button loading={isFetchingHistory} onClick={() => fetchHistory(selectedPatientId!, since)}>
          Get Patient History
        </Button>
      </div>
      {error && <Alert message={error} onDismiss={clearError} />}
      {isFetchingHistory && (
        <div className="flex justify-center py-8">
          <Spinner />
        </div>
      )}
      {!isFetchingHistory && history.length > 0 && (
        <div className="overflow-hidden rounded-xl border border-slate-200 bg-white">
          {history.map((v) => (
            <VisitRow
              key={v.visit_id}
              visit={v}
              onEdit={role === "doctor" ? setEditingVisit : undefined}
            />
          ))}
        </div>
      )}
      {!isFetchingHistory && history.length === 0 && !error && (
        <p className="py-6 text-center text-sm text-slate-400">
          No visits loaded. Select a date range and click &quot;Get Patient History&quot;.
        </p>
      )}
      {editingVisit && (
        <EditVisitModal
          visit={editingVisit}
          isOpen={!!editingVisit}
          onClose={() => setEditingVisit(null)}
        />
      )}
    </div>
  );
}
