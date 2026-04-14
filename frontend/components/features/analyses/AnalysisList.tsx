"use client";

import { useEffect, useState } from "react";
import { AlertTriangle, Pencil } from "lucide-react";

import Alert from "@/components/common/Alert/Alert";
import Button from "@/components/common/Button/Button";
import Input from "@/components/common/Input/Input";
import Spinner from "@/components/common/Spinner/Spinner";
import EditAnalysisModal from "@/components/features/analyses/EditAnalysisModal";
import { useRole } from "@/contexts/RoleContext";
import { useAnalysisStore } from "@/stores/useAnalysisStore";
import { usePatientStore } from "@/stores/usePatientStore";
import formatDate from "@/utils/formatDate";

const SNIPPET_LENGTH = 120;

function AnalysisCard({
  record,
  onEdit,
}: {
  record: Entity.AnalysisRecord;
  onEdit?: (r: Entity.AnalysisRecord) => void;
}) {
  const [expanded, setExpanded] = useState(false);
  const text = record.analysis_text ?? "";
  const dateLabel = record.analysis_date ? formatDate(record.analysis_date) : "No date";
  const created = formatDate(record.created_at);
  const isIncomplete = !text || !record.analysis_date;

  const isLong = text.length > SNIPPET_LENGTH;
  const displayed = expanded || !isLong ? text : `${text.slice(0, SNIPPET_LENGTH)}…`;

  return (
    <div
      className={
        isIncomplete
          ? "rounded-xl border border-red-300 bg-red-50 p-4"
          : "rounded-xl border border-slate-200 bg-white p-4"
      }
    >
      <div className="mb-2 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <span
            className={
              isIncomplete
                ? "rounded-md bg-red-100 px-2 py-0.5 text-xs font-medium text-red-700"
                : "rounded-md bg-blue-50 px-2 py-0.5 text-xs font-medium text-blue-700"
            }
          >
            {dateLabel}
          </span>
          {isIncomplete && (
            <AlertTriangle className="h-3.5 w-3.5 text-red-400" aria-label="Incomplete record" />
          )}
        </div>
        <div className="flex items-center gap-2">
          <span className="text-xs text-slate-400">{created}</span>
          {onEdit && (
            <button
              type="button"
              onClick={() => onEdit(record)}
              className="rounded p-1 text-slate-400 hover:bg-slate-200 hover:text-slate-600"
              aria-label="Edit analysis"
            >
              <Pencil className="h-3.5 w-3.5" />
            </button>
          )}
        </div>
      </div>
      {text ? (
        <>
          <p className="whitespace-pre-wrap text-sm text-slate-700">{displayed}</p>
          {isLong && (
            <button
              type="button"
              onClick={() => setExpanded((v) => !v)}
              className="mt-2 text-xs font-medium text-blue-600 hover:text-blue-700"
            >
              {expanded ? "Show less" : "Show more"}
            </button>
          )}
        </>
      ) : (
        <p className="text-sm italic text-red-400">No lab text — please edit manually.</p>
      )}
    </div>
  );
}

export default function AnalysisList() {
  const { selectedPatientId } = usePatientStore();
  const { analyses, isFetching, fetchError, fetchAnalyses, clearFetchError, refreshTrigger } =
    useAnalysisStore();
  const { role } = useRole();
  const [since, setSince] = useState(() => {
    const d = new Date();
    d.setMonth(d.getMonth() - 6);
    return d.toISOString().split("T")[0];
  });
  const [editingRecord, setEditingRecord] = useState<Entity.AnalysisRecord | null>(null);

  useEffect(() => {
    if (refreshTrigger > 0 && selectedPatientId) {
      fetchAnalyses(selectedPatientId, since);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [refreshTrigger]);

  const sorted = [...analyses].sort((a, b) => {
    if (!a.analysis_date && !b.analysis_date) return 0;
    if (!a.analysis_date) return 1;
    if (!b.analysis_date) return -1;
    return new Date(b.analysis_date).getTime() - new Date(a.analysis_date).getTime();
  });

  return (
    <div className="flex flex-col gap-4">
      <div className="flex items-end gap-3">
        <Input
          label="Results from"
          type="date"
          value={since}
          onChange={setSince}
          className="w-44"
        />
        <Button loading={isFetching} onClick={() => fetchAnalyses(selectedPatientId!, since)}>
          Refresh
        </Button>
      </div>

      {fetchError && <Alert message={fetchError} onDismiss={clearFetchError} />}

      {isFetching && (
        <div className="flex justify-center py-8">
          <Spinner />
        </div>
      )}

      {!isFetching && sorted.length > 0 && (
        <div className="flex flex-col gap-3">
          {sorted.map((record, i) => (
            <AnalysisCard
              key={`${record.analysis_date}-${i}`}
              record={record}
              onEdit={role === "doctor" ? setEditingRecord : undefined}
            />
          ))}
        </div>
      )}

      {!isFetching && sorted.length === 0 && !fetchError && (
        <p className="py-6 text-center text-sm text-slate-400">
          No lab results found. Adjust the date range or save a new analysis.
        </p>
      )}

      {editingRecord && (
        <EditAnalysisModal
          record={editingRecord}
          isOpen={!!editingRecord}
          onClose={() => setEditingRecord(null)}
        />
      )}
    </div>
  );
}
