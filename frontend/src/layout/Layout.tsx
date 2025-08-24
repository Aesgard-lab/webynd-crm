// src/layout/Layout.tsx
import * as React from "react";
import { Layout as RaLayout, useRefresh } from "react-admin";
import MyAppBar from "./AppBar";
import MyMenu from "./Menu"; // ← menú compatible con RA (Drawer)

/** Escucha cambios del gym seleccionado (UserChip/localStorage) y refresca la UI */
function GymScopeListener() {
  const refresh = useRefresh();

  React.useEffect(() => {
    const onStorage = (e: StorageEvent) => {
      if (e.key === "currentGymId" || e.key === "me") refresh();
    };
    const onChange = () => refresh();

    window.addEventListener("storage", onStorage);
    window.addEventListener("gym-changed", onChange);

    return () => {
      window.removeEventListener("storage", onStorage);
      window.removeEventListener("gym-changed", onChange);
    };
  }, [refresh]);

  return null;
}

export default function Layout(props: any) {
  return (
    <>
      <GymScopeListener />
      <RaLayout
        {...props}
        appBar={MyAppBar}
        menu={MyMenu}  // ← renderiza el Drawer con permisos/roles
      />
    </>
  );
}
