// src/resources/backoffice/dashboard/BackofficeDashboard.tsx
import * as React from "react";
import Topbar from "./components/Topbar";
import KpiCard from "./components/KpiCard";
import ScheduleTable from "./components/ScheduleTable";
import BillingChart from "./components/BillingChart"; // usa valores normalizados 0..1

type Kpis = {
  activeClients: number;
  activeMemberships: number;
  monthlyRevenue: number;
  churnThisMonth: number;
};

export default function BackofficeDashboard() {
  const [kpis, setKpis] = React.useState<Kpis>({
    activeClients: 0,
    activeMemberships: 0,
    monthlyRevenue: 0,
    churnThisMonth: 0,
  });

  // BillingChart espera un array de 7 valores normalizados (0..1)
  const [bars, setBars] = React.useState<number[]>([0.8, 0.6, 0.7, 0.6, 0.9, 1, 0.4]);
  const [loading, setLoading] = React.useState(true);

  const load = React.useCallback(async () => {
    setLoading(true);
    try {
      const me = JSON.parse(localStorage.getItem("me") || "null");
      const token = localStorage.getItem("access"); // ajusta si usas otra clave
      const gymId = me?.currentGym?.id;

      if (!token) throw new Error("Falta token");
      if (!gymId) throw new Error("Falta currentGym");

      const headers: HeadersInit = {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      };
      const qs = `?gym=${gymId}`;

      const [ovRes, facRes] = await Promise.all([
        fetch(`/api/dashboard/kpi/overview/${qs}`, { headers }),
        fetch(`/api/dashboard/kpi/facturacion/${qs}`, { headers }),
      ]);

      if (ovRes.status === 401 || facRes.status === 401) {
        throw new Error("No autorizado");
      }
      if (!ovRes.ok) throw new Error("overview failed");
      if (!facRes.ok) throw new Error("facturacion failed");

      const ov = await ovRes.json();
      const fac = await facRes.json();

      setKpis({
        activeClients: ov.activeClients ?? 0,
        activeMemberships: ov.activeMemberships ?? 0,
        monthlyRevenue: ov.monthlyRevenue ?? 0,
        churnThisMonth: ov.churnThisMonth ?? 0,
      });

      // BillingChart ya espera valores normalizados 0..1
      setBars(Array.isArray(fac.bars) ? fac.bars : [0.8, 0.6, 0.7, 0.6, 0.9, 1, 0.4]);
    } catch (e) {
      console.error(e);
      // Fallback visual si falla la carga
      setKpis({
        activeClients: 0,
        activeMemberships: 0,
        monthlyRevenue: 9000,
        churnThisMonth: 3,
      });
      setBars([0.8, 0.6, 0.7, 0.6, 0.9, 1, 0.4]);
    } finally {
      setLoading(false);
    }
  }, []);

  React.useEffect(() => {
    load();
  }, [load]);

  // Agenda dummy (solo UI de ejemplo)
  const scheduleRows = [
    { time: "8:00",  className: "Yoga Flow",          instructor: "Emily Carter", capacity: "75 / 88", progressPct: 85, status: "Scheduled" as const },
    { time: "9:30",  className: "Strength Training",  instructor: "Mark Johnson",  capacity: "90 / 90", progressPct: 100, status: "Full" as const },
    { time: "11:00", className: "Pilates",            instructor: "Olivia Brown",  capacity: "60 / 88", progressPct: 68, status: "Scheduled" as const },
    { time: "12:30", className: "Spin Class",         instructor: "Ethan Davis",   capacity: "85 / 88", progressPct: 97, status: "Filling Fast" as const },
    { time: "14:00", className: "Zumba",              instructor: "Sophia Wilson", capacity: "70 / 88", progressPct: 80, status: "Scheduled" as const },
  ];

  return (
    <div className="mx-auto max-w-7xl p-6">
      <Topbar
        title="Dashboard"
        subtitle="Bienvenido de nuevo. Así va tu gimnasio hoy."
        onRefresh={load}
      />

      {/* KPIs */}
      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
        <KpiCard
          title="Clientes activos"
          value={kpis.activeClients.toLocaleString("es-ES")}
          loading={loading}
          icon={
            <svg className="h-5 w-5" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
              <path d="M16 11a3 3 0 100-6 3 3 0 000 6zM8 11a3 3 0 100-6 3 3 0 000 6zM8 13c-2.66 0-8 1.34-8 4v2h16v-2c0-2.66-5.34-4-8-4zm8 0c-.33 0-.68.02-1.03.05 1.77.86 3.03 2.09 3.03 3.95v2h6v-2c0-2.66-5.34-4-8-4z" />
            </svg>
          }
          delta={{ value: "+12%", positive: true }}
          subtitle="vs ayer"
        />
        <KpiCard
          title="Suscripciones activas"
          value={kpis.activeMemberships.toLocaleString("es-ES")}
          loading={loading}
          icon={
            <svg className="h-5 w-5" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
              <path d="M20 6H4v12h16V6zM2 6a2 2 0 012-2h16a2 2 0 012 2v2H2V6z" />
            </svg>
          }
          delta={{ value: "+3%", positive: true }}
          subtitle="últimos 7 días"
        />
        <KpiCard
          title="Facturación mensual"
          value={`${kpis.monthlyRevenue.toLocaleString("es-ES")} €`}
          loading={loading}
          icon={
            <svg className="h-5 w-5" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
              <path d="M12 1a11 11 0 1011 11A11 11 0 0012 1zm1 17.93V20h-2v-1.07A8 8 0 014.07 13H3v-2h1.07A8 8 0 0111 4.07V3h2v1.07A8 8 0 0119.93 11H21v2h-1.07A8 8 0 0113 18.93z" />
            </svg>
          }
          delta={{ value: "+8%", positive: true }}
          subtitle="vs mes anterior"
        />
        <KpiCard
          title="Bajas del mes"
          value={kpis.churnThisMonth.toLocaleString("es-ES")}
          loading={loading}
          icon={
            <svg className="h-5 w-5" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
              <path d="M12 2a10 10 0 1010 10A10.011 10.011 0 0012 2zm1 15h-2v-2h2zm0-4h-2V7h2z" />
            </svg>
          }
          // Ejemplo: descenso de bajas es positivo
          delta={{ value: "-2%", positive: true }}
          subtitle="vs mes anterior"
        />
      </div>

      {/* Gráfica de facturación */}
      <div className="mt-6">
        <BillingChart bars={bars} title="Facturación últimos 7 meses" />
      </div>

      {/* Agenda */}
      <div className="mt-2">
        <ScheduleTable rows={scheduleRows} />
      </div>
    </div>
  );
}
