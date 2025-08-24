import * as React from "react";

type Row = {
  time: string;
  className: string;
  instructor: string;
  capacity: string; // ej: "75 / 88"
  progressPct?: number; // 0..100
  status: "Scheduled" | "Full" | "Filling Fast";
};

export default function ScheduleTable({ rows }: { rows: Row[] }) {
  return (
    <div className="mt-8">
      <h2 className="text-xl font-bold text-gray-900">Agenda de hoy</h2>

      <div className="mt-4 overflow-hidden rounded-2xl border border-gray-200 bg-white shadow-sm ring-1 ring-black/5">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                {["Hora", "Clase", "Instructor", "Aforo", "Estado"].map((h) => (
                  <th
                    key={h}
                    className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500"
                    scope="col"
                  >
                    {h}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200 bg-white">
              {rows.map((r, idx) => (
                <tr key={idx}>
                  <td className="whitespace-nowrap px-6 py-4 text-sm font-medium text-gray-900">{r.time}</td>
                  <td className="whitespace-nowrap px-6 py-4 text-sm text-gray-700">{r.className}</td>
                  <td className="whitespace-nowrap px-6 py-4 text-sm text-gray-500">{r.instructor}</td>
                  <td className="whitespace-nowrap px-6 py-4 text-sm text-gray-500">
                    <div className="flex items-center gap-2">
                      <div className="w-24 overflow-hidden rounded-full bg-gray-200">
                        <div
                          className="h-2 rounded-full"
                          style={{
                            width: `${Math.min(Math.max(r.progressPct ?? 0, 0), 100)}%`,
                            background:
                              r.status === "Full"
                                ? "#ef4444" // rojo
                                : r.status === "Filling Fast"
                                ? "#f59e0b" // amarillo
                                : "#3b82f6", // azul
                          }}
                        />
                      </div>
                      <span className="text-sm font-medium text-gray-700">{r.capacity}</span>
                    </div>
                  </td>
                  <td className="whitespace-nowrap px-6 py-4 text-sm">
                    {r.status === "Full" && (
                      <span className="inline-flex rounded-full bg-red-100 px-2 text-xs font-semibold leading-5 text-red-700">
                        Full
                      </span>
                    )}
                    {r.status === "Filling Fast" && (
                      <span className="inline-flex rounded-full bg-yellow-100 px-2 text-xs font-semibold leading-5 text-yellow-700">
                        Filling Fast
                      </span>
                    )}
                    {r.status === "Scheduled" && (
                      <span className="inline-flex rounded-full bg-blue-100 px-2 text-xs font-semibold leading-5 text-blue-700">
                        Scheduled
                      </span>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
