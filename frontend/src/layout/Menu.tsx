import * as React from "react";
import { Menu, MenuItemLink } from "react-admin";

type Role = "superadmin" | "admin" | "staff" | "client";
type PermKey =
  | "can_manage_clients"
  | "can_manage_cash"
  | "can_manage_activities"
  | "can_manage_bonuses";

function useMeFromCache() {
  const [me, setMe] = React.useState<any>(() => {
    try { return JSON.parse(localStorage.getItem("me") || "null"); } catch { return null; }
  });

  React.useEffect(() => {
    const onStorage = (e: StorageEvent) => {
      if (e.key === "me") {
        try { setMe(JSON.parse(localStorage.getItem("me") || "null")); } catch { setMe(null); }
      }
    };
    const onGymChange = () => {
      try { setMe(JSON.parse(localStorage.getItem("me") || "null")); } catch { setMe(null); }
    };
    window.addEventListener("storage", onStorage);
    window.addEventListener("gym-changed", onGymChange);
    return () => {
      window.removeEventListener("storage", onStorage);
      window.removeEventListener("gym-changed", onGymChange);
    };
  }, []);

  return me;
}

export default function MyMenu() {
  const me = useMeFromCache();

  // Normalizamos el rol (por si llega "ADMIN", "Staff", etc.)
  const roleRaw = (me?.role ?? "client") + "";
  const role = roleRaw.toLowerCase() as Role;

  const currentGymId = me?.currentGym?.id ?? null;

  const activeMembership =
    me?.memberships?.find((m: any) => m?.gym?.id === currentGymId) || null;

  const perms: Record<PermKey, boolean> = {
    can_manage_clients: !!activeMembership?.can_manage_clients,
    can_manage_cash: !!activeMembership?.can_manage_cash,
    can_manage_activities: !!activeMembership?.can_manage_activities,
    can_manage_bonuses: !!activeMembership?.can_manage_bonuses,
  };

  const MENU = [
    { key: "dashboard", label: "Dashboard", to: "/", roles: ["admin", "staff", "superadmin"] as Role[] },
    { key: "clients", label: "Clients", to: "/clients", roles: ["admin", "staff"] as Role[], require: "can_manage_clients" as PermKey },
    { key: "finances", label: "Finances", to: "/backoffice/finances", roles: ["admin", "staff"] as Role[], require: "can_manage_cash" as PermKey },
    { key: "activities", label: "Activities", to: "/backoffice/activities", roles: ["admin", "staff"] as Role[], require: "can_manage_activities" as PermKey },
    { key: "bonuses", label: "Bonuses", to: "/backoffice/bonuses", roles: ["admin", "staff"] as Role[], require: "can_manage_bonuses" as PermKey },
    { key: "settings", label: "Settings", to: "/backoffice/settings", roles: ["admin", "superadmin"] as Role[] },
    // Superadmin
    { key: "franchises", label: "Superadmin · Franchises", to: "/franchises", roles: ["superadmin"] as Role[] },
    { key: "modules", label: "Superadmin · Modules", to: "/saas/modules", roles: ["superadmin"] as Role[] },
    { key: "prices", label: "Superadmin · Prices", to: "/saas/module-prices", roles: ["superadmin"] as Role[] },
  ] as const;

  let visible = MENU.filter((i) => {
    if (!i.roles.includes(role)) return false;
    // superadmin ve todo
    if (role === "superadmin") return true;
    // sin permiso requerido
    if (!("require" in i)) return true;
    // con permiso requerido
    return perms[i.require as PermKey];
  });

  // Si es admin/staff/superadmin y por sede/permiso no pasa nada, muestra Dashboard al menos
  if (visible.length === 0 && ["admin", "staff", "superadmin"].includes(role)) {
    visible = MENU.filter((i) => i.key === "dashboard");
  }

  return (
    <Menu>
      {visible.map((i) => (
        <MenuItemLink key={i.key} to={i.to} primaryText={i.label} />
      ))}
      {role !== "superadmin" && !currentGymId && (
        <div style={{ padding: 12, fontSize: 12, color: "#8a6d3b" }}>
          Selecciona una sede desde tu avatar para ver más módulos.
        </div>
      )}
    </Menu>
  );
}
