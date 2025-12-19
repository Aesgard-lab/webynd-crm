import * as React from "react";

export default function Finances() {
  return (
    <div className="p-6">
      <h1 className="text-xl font-semibold text-gray-900">Finanzas</h1>
      <p className="mt-1 text-sm text-gray-500">
        Placeholder de Finanzas. Aquí irán cobros, facturas, arqueos, etc.
      </p>

      <div className="mt-6 grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {[...Array(6)].map((_, i) => (
          <div key={i} className="rounded-2xl border border-gray-200 bg-white p-4">
            <div className="h-4 w-32 animate-pulse rounded bg-gray-100" />
            <div className="mt-3 h-7 w-24 animate-pulse rounded bg-gray-100" />
            <div className="mt-2 h-3 w-40 animate-pulse rounded bg-gray-100" />
          </div>
        ))}
      </div>
    </div>
  );
}
