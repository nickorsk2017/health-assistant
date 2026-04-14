"use client";

import { useEffect, useState } from "react";

import Spinner from "@/components/common/Spinner/Spinner";
import PatientGuard from "@/components/features/patient/PatientGuard";
import PatientOnboardingGuard from "@/components/features/patient/PatientOnboardingGuard";
import RoleSelectionOverlay from "@/components/features/role/RoleSelectionOverlay";
import Sidebar from "@/components/layout/Sidebar/Sidebar";
import TopBar from "@/components/layout/TopBar/TopBar";
import PatientSelector from "@/components/features/patient/PatientSelector";
import { RoleContext } from "@/contexts/RoleContext";

const ROLE_KEY = "app_role";

type Props = {
  children: React.ReactNode;
};

export default function AppShell({ children }: Props) {
  const [role, setRoleState] = useState<Entity.AppRole | null>(null);
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    const stored = localStorage.getItem(ROLE_KEY) as Entity.AppRole | null;
    setRoleState(stored);
    setMounted(true);
  }, []);

  const setRole = (newRole: Entity.AppRole) => {
    localStorage.setItem(ROLE_KEY, newRole);
    setRoleState(newRole);
  };

  const logout = () => {
    localStorage.clear();
    setRoleState(null);
  };

  if (!mounted) {
    return (
      <div className="fixed inset-0 flex items-center justify-center bg-white">
        <Spinner size="lg" />
      </div>
    );
  }

  if (role === null) {
    return <RoleSelectionOverlay onSelect={setRole} />;
  }

  return (
    <RoleContext.Provider value={{ role, setRole, logout }}>
      {role === "doctor" ? <PatientGuard /> : <PatientOnboardingGuard />}
      <div className="flex h-screen overflow-hidden">
        <Sidebar />
        <div className="flex flex-1 flex-col overflow-hidden">
          {role === "doctor" ? (
            <TopBar>
              <PatientSelector />
            </TopBar>
          ) : (
            <TopBar />
          )}
          <main className="flex-1 overflow-y-auto p-6">{children}</main>
        </div>
      </div>
    </RoleContext.Provider>
  );
}
