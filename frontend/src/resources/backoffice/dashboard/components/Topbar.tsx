import * as React from "react";

type Props = {
  title?: string;
  subtitle?: string;
  onRefresh?: () => void;
  extra?: React.ReactNode; // p.ej., filtros
};

export default function Topbar({ title = "Dashboard", subtitle, onRefresh, extra }: Props) {
  return (
    <div className="mb-6 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
      <div className="text-left">
        <h1 className="text-3xl font-bold text-gray-900">{title}</h1>
        {subtitle && <p className="text-gray-500">{subtitle}</p>}
      </div>

      <div className="flex items-center gap-3">
        {extra}
        <button
          onClick={onRefresh}
          className="inline-flex items-center gap-2 rounded-xl border border-gray-200 bg-white px-3 py-2 text-sm font-medium text-gray-700 shadow-sm ring-1 ring-black/5 transition hover:bg-gray-50 active:scale-[0.99]"
          title="Refrescar"
        >
          <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
            <path d="M3.172 7A7.001 7.001 0 0117 10a1 1 0 102 0A9 9 0 102 10h1.172z" />
            <path d="M5 8a1 1 0 011 1v3a1 1 0 102 0V9a3 3 0 10-3 3H3a1 1 0 110-2h2V9a1 1 0 011-1z" />
          </svg>
          Refrescar
        </button>
      </div>
    </div>
  );
}

