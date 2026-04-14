"use client";

import { useEffect } from "react";
import { X } from "lucide-react";

import cx from "@/utils/cx";

type Props = {
  isOpen: boolean;
  title: string;
  onClose: () => void;
  children: React.ReactNode;
  className?: string;
  closable?: boolean;
};

export default function Modal({ isOpen, title, onClose, children, className, closable = true }: Props) {
  useEffect(() => {
    if (!isOpen || !closable) return;
    const onKey = (e: KeyboardEvent) => e.key === "Escape" && onClose();
    document.addEventListener("keydown", onKey);
    return () => document.removeEventListener("keydown", onKey);
  }, [isOpen, onClose, closable]);

  if (!isOpen) return null;

  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-labelledby="modal-title"
      className="fixed inset-0 z-50 flex items-center justify-center p-4"
    >
      <div
        className="absolute inset-0 bg-slate-900/40 backdrop-blur-sm"
        onClick={closable ? onClose : undefined}
        aria-hidden="true"
      />
      <div
        className={cx(
          "relative z-10 w-full max-w-md rounded-2xl border border-slate-200 bg-white shadow-xl",
          className,
        )}
      >
        <div className="flex items-center justify-between border-b border-slate-100 px-6 py-4">
          <h2 id="modal-title" className="text-base font-semibold text-slate-800">
            {title}
          </h2>
          {closable && (
            <button
              onClick={onClose}
              className="rounded-lg p-1 text-slate-400 transition-colors hover:bg-slate-100 hover:text-slate-600"
            >
              <X className="h-4 w-4" />
            </button>
          )}
        </div>
        <div className="px-6 py-5">{children}</div>
      </div>
    </div>
  );
}
