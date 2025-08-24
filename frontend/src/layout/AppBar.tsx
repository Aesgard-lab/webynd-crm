// src/layout/AppBar.tsx
import * as React from "react";
import { AppBar } from "react-admin";
import UserChip from "../components/UserChip"; // ← tu avatar con menú

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
    window.addEventListener("storage", onStorage);
    return () => window.removeEventListener("storage", onStorage);
  }, []);
  return me;
}

export default function MyAppBar(props: any) {
  const me = useMeFromCache();
  const brand = {
    logo: me?.currentGym?.logo || null,
    name: me?.currentGym?.name || "GYM",
  };

  return (
    <AppBar
      {...props}
      color="default"
      elevation={0}
      userMenu={false} // ← desactiva el user menu de RA (evita avatar duplicado)
      sx={{
        backgroundColor: "#fff",
        borderBottom: "1px solid #e5e7eb",
        // oculta el título "React Admin" del centro y el icono de refresco
        "& #react-admin-title": { display: "none" },
        "& .RaLoadingIndicator-root": { display: "none" },
        position: "relative",
        minHeight: 64,
      }}
    >
      {/* IZQUIERDA: logo + nombre (dejando hueco al botón hamburguesa) */}
      <div
        style={{
          position: "absolute",
          left: 56, // ancho aprox. del botón hamburguesa
          top: 0,
          bottom: 0,
          display: "flex",
          alignItems: "center",
          gap: 12,
        }}
      >
        {brand.logo ? (
          <img
            src={brand.logo}
            alt={brand.name}
            className="h-9 w-9 rounded-xl object-cover ring-1 ring-black/10"
          />
        ) : (
          <div className="grid h-9 w-9 place-items-center rounded-xl bg-gray-100 ring-1 ring-black/10">
            <span className="text-sm font-semibold text-gray-600">
              {brand.name?.[0] ?? "G"}
            </span>
          </div>
        )}
        <span className="hidden text-base font-semibold text-gray-900 sm:inline">
          {brand.name}
        </span>
      </div>

      {/* DERECHA: botón Cobrar + avatar funcional (UserChip) */}
      <div
        style={{
          position: "absolute",
          right: 16,
          top: 0,
          bottom: 0,
          display: "flex",
          alignItems: "center",
          gap: 14,
        }}
      >
        <button
  onClick={() => (window.location.hash = "#/backoffice/checkout")}
  className="inline-flex items-center gap-2 rounded-xl border border-gray-200 bg-white px-4 py-2 text-sm font-medium text-gray-900 shadow-sm ring-1 ring-black/5 transition hover:bg-gray-50 active:scale-[0.99]"
  title="Cobrar"
>
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="h-4 w-4">
    <path d="M2.25 7.5A2.25 2.25 0 0 1 4.5 5.25h15a2.25 2.25 0 0 1 2.25 2.25v9A2.25 2.25 0 0 1 19.5 19.5h-15A2.25 2.25 0 0 1 2.25 16.5v-9zm1.5 0v1.5h16.5V7.5a.75.75 0 0 0-.75-.75h-15a.75.75 0 0 0-.75.75zm16.5 4.5H3.75v4.5c0 .414.336.75.75.75h15a.75.75 0 0 0 .75-.75V12zM6 14.25h3a.75.75 0 0 1 0 1.5H6a.75.75 0 0 1 0-1.5z" />
  </svg>
  Cobrar
</button>

        {/* Este es tu avatar con menú (logout / cambiar sede) */}
        <UserChip />
      </div>
    </AppBar>
  );
}
