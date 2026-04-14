"use client";

import { Activity, Stethoscope, User } from "lucide-react";

type Props = {
  onSelect: (role: Entity.AppRole) => void;
};

export default function RoleSelectionOverlay({ onSelect }: Props) {
  return (
    <div className="fixed inset-0 z-50 flex flex-col items-center justify-center bg-slate-900 p-6">
      <div className="mb-10 flex flex-col items-center gap-3 text-center">
        <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-blue-600">
          <Activity className="h-7 w-7 text-white" />
        </div>
        <h1 className="text-2xl font-bold text-white">Personal Health OS</h1>
        <p className="text-sm text-slate-400">Choose your access mode to continue</p>
      </div>

      <div className="grid w-full max-w-2xl grid-cols-1 gap-4 sm:grid-cols-2">
        <button
          type="button"
          onClick={() => onSelect("doctor")}
          className="group flex flex-col items-start gap-4 rounded-2xl border border-slate-700 bg-slate-800 p-6 text-left transition-all hover:border-blue-500 hover:bg-slate-700 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500"
        >
          <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-blue-600 group-hover:bg-blue-500">
            <Stethoscope className="h-6 w-6 text-white" />
          </div>
          <div>
            <p className="text-base font-semibold text-white">Doctor</p>
            <p className="mt-1 text-sm text-slate-400">Full clinical access</p>
          </div>
          <ul className="flex flex-col gap-1 text-xs text-slate-500">
            <li>Manage patient records</li>
            <li>Record visits and lab results</li>
            <li>AI consilium and diagnosis</li>
          </ul>
          <span className="mt-auto inline-block rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white group-hover:bg-blue-500">
            I&apos;m a Healthcare Pro
          </span>
        </button>

        <button
          type="button"
          onClick={() => onSelect("patient")}
          className="group flex flex-col items-start gap-4 rounded-2xl border border-slate-700 bg-slate-800 p-6 text-left transition-all hover:border-emerald-500 hover:bg-slate-700 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-500"
        >
          <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-emerald-600 group-hover:bg-emerald-500">
            <User className="h-6 w-6 text-white" />
          </div>
          <div>
            <p className="text-base font-semibold text-white">Patient</p>
            <p className="mt-1 text-sm text-slate-400">View your health records</p>
          </div>
          <ul className="flex flex-col gap-1 text-xs text-slate-500">
            <li>View visit history</li>
            <li>Access lab results</li>
            <li>Review AI diagnosis</li>
          </ul>
          <span className="mt-auto inline-block rounded-lg bg-emerald-600 px-4 py-2 text-sm font-medium text-white group-hover:bg-emerald-500">
            I&apos;m a Patient
          </span>
        </button>
      </div>
    </div>
  );
}
