// src/hooks/useGym.ts
import * as React from "react";

export function useCurrentGym() {
  const [gymId, setGymId] = React.useState<number | null>(null);
  const [gymName, setGymName] = React.useState<string>("");

  const refresh = React.useCallback(() => {
    const idRaw = localStorage.getItem("currentGymId");
    const name = localStorage.getItem("currentGymName") || "";
    const id = idRaw ? Number(idRaw) : null;
    setGymId(Number.isFinite(id as number) ? (id as number) : null);
    setGymName(name);
  }, []);

  React.useEffect(() => {
    refresh();
    const onChange = () => refresh();
    const onStorage = (e: StorageEvent) => {
      if (e.key === "currentGymId" || e.key === "currentGymName") refresh();
    };
    window.addEventListener("gym-changed", onChange);
    window.addEventListener("storage", onStorage);
    return () => {
      window.removeEventListener("gym-changed", onChange);
      window.removeEventListener("storage", onStorage);
    };
  }, [refresh]);

  return { gymId, gymName, refresh };
}
