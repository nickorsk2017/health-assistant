"use client";

import { createContext, useContext } from "react";

type RoleContextValue = {
  role: Entity.AppRole | null;
  setRole: (role: Entity.AppRole) => void;
  logout: () => void;
};

export const RoleContext = createContext<RoleContextValue>({
  role: null,
  setRole: () => {},
  logout: () => {},
});

export function useRole(): RoleContextValue {
  return useContext(RoleContext);
}
