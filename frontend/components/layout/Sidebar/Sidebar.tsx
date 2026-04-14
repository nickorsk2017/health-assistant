"use client";

import { useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  Activity,
  ArrowLeftRight,
  ClipboardList,
  FlaskConical,
  LogOut,
  Stethoscope,
} from "lucide-react";

import { useRole } from "@/contexts/RoleContext";
import cx from "@/utils/cx";

const DOCTOR_NAV = [
  { href: "/history", label: "Clinic History", icon: ClipboardList },
  { href: "/analyses", label: "Lab Analyses", icon: FlaskConical },
  { href: "/consilium", label: "AI Consilium", icon: Activity },
  { href: "/diagnosis", label: "AI Diagnosis PB", icon: Stethoscope },
];

const PATIENT_NAV = [
  { href: "/history", label: "My Health History", icon: ClipboardList },
  { href: "/analyses", label: "My Lab Results", icon: FlaskConical },
  { href: "/diagnosis", label: "My Diagnosis", icon: Stethoscope },
];

export default function Sidebar() {
  const pathname = usePathname();
  const { role, logout } = useRole();
  const [confirmingLogout, setConfirmingLogout] = useState(false);

  const navItems = role === "patient" ? PATIENT_NAV : DOCTOR_NAV;

  const handleSwitchRole = () => {
    if (typeof window !== "undefined") {
      localStorage.removeItem("app_role");
      window.location.reload();
    }
  };

  return (
    <aside className="flex h-screen w-56 shrink-0 flex-col border-r border-slate-200 bg-white">
      <div className="flex items-center gap-2 border-b border-slate-200 px-5 py-4">
        <div className="flex h-7 w-7 items-center justify-center rounded-lg bg-blue-600">
          <Activity className="h-4 w-4 text-white" />
        </div>
        <span className="text-sm font-semibold text-slate-800">Health OS</span>
      </div>

      <nav className="flex flex-1 flex-col gap-0.5 p-3">
        {navItems.map(({ href, label, icon: Icon }) => {
          const active = pathname.startsWith(href);
          return (
            <Link
              key={href}
              href={href}
              className={cx(
                "flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors",
                active
                  ? "bg-blue-50 text-blue-700"
                  : "text-slate-600 hover:bg-slate-100 hover:text-slate-800",
              )}
            >
              <Icon className="h-4 w-4 shrink-0" />
              {label}
            </Link>
          );
        })}
      </nav>

      <div className="flex flex-col gap-0.5 border-t border-slate-100 p-3">
        {confirmingLogout ? (
          <div className="rounded-lg bg-red-50 p-3">
            <p className="mb-3 text-xs text-red-700">
              Are you sure? All local session data will be cleared.
            </p>
            <div className="flex gap-2">
              <button
                type="button"
                onClick={logout}
                className="flex-1 rounded-md bg-red-600 px-2 py-1.5 text-xs font-medium text-white hover:bg-red-700"
              >
                Confirm
              </button>
              <button
                type="button"
                onClick={() => setConfirmingLogout(false)}
                className="flex-1 rounded-md bg-white px-2 py-1.5 text-xs font-medium text-slate-600 ring-1 ring-slate-200 hover:bg-slate-50"
              >
                Cancel
              </button>
            </div>
          </div>
        ) : (
          <>
            <button
              type="button"
              onClick={handleSwitchRole}
              className="flex w-full items-center gap-2 rounded-lg px-3 py-2 text-xs font-medium text-slate-400 transition-colors hover:bg-slate-100 hover:text-slate-600"
            >
              <ArrowLeftRight className="h-3.5 w-3.5" />
              Switch Role
            </button>
            <button
              type="button"
              onClick={() => setConfirmingLogout(true)}
              className="flex w-full items-center gap-2 rounded-lg px-3 py-2 text-xs font-medium text-red-400 transition-colors hover:bg-red-50 hover:text-red-600"
            >
              <LogOut className="h-3.5 w-3.5" />
              Log Out
            </button>
          </>
        )}
      </div>
    </aside>
  );
}
