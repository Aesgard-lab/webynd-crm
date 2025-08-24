import * as React from "react";

type Props = {
  title: string;
  value: React.ReactNode;
  subtitle?: string;
  icon?: React.ReactNode;
  delta?: { value: string; positive?: boolean }; // ej: { value: "+12%", positive: true }
  loading?: boolean;
};

export default function KpiCard({ title, value, subtitle, icon, delta, loading }: Props) {
  return (
    <div className="rounded-2xl border border-gray-200 bg-white p-5 shadow-sm ring-1 ring-black/5">
      <div className="flex items-start justify-between">
        <div className="text-sm text-gray-500">{title}</div>
        {icon && <div className="rounded-xl bg-gray-50 p-2 text-gray-600">{icon}</div>}
      </div>

      <div className="mt-2 text-3xl font-semibold tracking-tight text-gray-900">
        {loading ? <span className="inline-block h-7 w-24 animate-pulse rounded bg-gray-100" /> : value}
      </div>

      <div className="mt-2 flex items-center gap-3">
        {delta && (
          <span
            className={`inline-flex items-center gap-1 rounded-full px-2 py-0.5 text-xs font-medium ${
              delta.positive ? "bg-green-100 text-green-700" : "bg-red-100 text-red-700"
            }`}
          >
            {delta.positive ? "▲" : "▼"}
            {delta.value}
          </span>
        )}
        {subtitle && <div className="text-xs text-gray-500">{subtitle}</div>}
      </div>
    </div>
  );
}

