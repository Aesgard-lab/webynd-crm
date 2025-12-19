// src/resources/scheduler/SessionsCalendar.tsx
import * as React from 'react';
import { useGetList, Title } from 'react-admin';

const startOfWeekMonday = (d: Date) => {
  const date = new Date(d);
  const day = date.getDay(); // 0 = domingo, 1 = lunes, ...
  const diff = (day === 0 ? -6 : 1) - day; // llevar a lunes
  date.setDate(date.getDate() + diff);
  date.setHours(0, 0, 0, 0);
  return date;
};

const addDays = (d: Date, days: number) => {
  const copy = new Date(d);
  copy.setDate(copy.getDate() + days);
  return copy;
};

const formatDateISO = (d: Date) => d.toISOString().split('T')[0];

const formatTime = (value?: string) => {
  if (!value) return '';
  const d = new Date(value);
  if (Number.isNaN(d.getTime())) return value;
  return d.toLocaleTimeString(undefined, {
    hour: '2-digit',
    minute: '2-digit',
  });
};

const weekdayLabels = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo'];

const SessionsCalendar: React.FC = () => {
  const [weekStart, setWeekStart] = React.useState<Date>(() =>
    startOfWeekMonday(new Date())
  );

  const weekEnd = addDays(weekStart, 6);
  const dateFrom = formatDateISO(weekStart);
  const dateTo = formatDateISO(weekEnd);

  // Llamamos al backend usando el recurso estándar "scheduler/sessions"
  const { data, isLoading } = useGetList('scheduler/sessions', {
    filter: {
      date_from: dateFrom,
      date_to: dateTo,
    },
    pagination: { page: 1, perPage: 500 },
    sort: { field: 'start_time', order: 'ASC' },
  });

  const sessions = data || [];

  // Agrupar por día (YYYY-MM-DD)
  const sessionsByDay: Record<string, any[]> = React.useMemo(() => {
    const map: Record<string, any[]> = {};
    sessions.forEach((s: any) => {
      const start = s.start_time || s.start || s.starts_at;
      if (!start) return;
      const d = new Date(start);
      if (Number.isNaN(d.getTime())) return;
      const dayKey = formatDateISO(d);
      if (!map[dayKey]) map[dayKey] = [];
      map[dayKey].push(s);
    });

    // ordenar las sesiones de cada día por hora
    Object.keys(map).forEach((key) => {
      map[key].sort((a, b) => {
        const da = new Date(a.start_time || a.start || a.starts_at).getTime();
        const db = new Date(b.start_time || b.start || b.starts_at).getTime();
        return da - db;
      });
    });

    return map;
  }, [sessions]);

  const goPrevWeek = () => {
    setWeekStart((prev) => addDays(prev, -7));
  };
  const goNextWeek = () => {
    setWeekStart((prev) => addDays(prev, 7));
  };
  const goThisWeek = () => {
    setWeekStart(startOfWeekMonday(new Date()));
  };

  return (
    <div className="p-3 bg-slate-100 min-h-[calc(100vh-80px)]">
      <Title title="Horario semanal" />
      {/* Controles de navegación */}
      <div className="mb-3 flex flex-wrap items-center justify-between gap-2">
        <div className="flex items-center gap-2">
          <button
            type="button"
            onClick={goPrevWeek}
            className="rounded-xl border border-gray-300 bg-white px-3 py-1 text-xs font-medium text-gray-700 shadow-sm hover:bg-gray-50"
          >
            ◀ Semana anterior
          </button>
          <button
            type="button"
            onClick={goThisWeek}
            className="rounded-xl border border-indigo-500 bg-indigo-50 px-3 py-1 text-xs font-medium text-indigo-700 shadow-sm hover:bg-indigo-100"
          >
            Hoy
          </button>
          <button
            type="button"
            onClick={goNextWeek}
            className="rounded-xl border border-gray-300 bg-white px-3 py-1 text-xs font-medium text-gray-700 shadow-sm hover:bg-gray-50"
          >
            Semana siguiente ▶
          </button>
        </div>
        <div className="text-xs text-gray-600">
          Semana del{' '}
          <span className="font-semibold">
            {weekStart.toLocaleDateString()}
          </span>{' '}
          al{' '}
          <span className="font-semibold">
            {weekEnd.toLocaleDateString()}
          </span>
        </div>
      </div>

      {/* Calendario semanal: 7 columnas (cada día) */}
      <div className="grid gap-2 md:grid-cols-7 grid-cols-1">
        {Array.from({ length: 7 }).map((_, idx) => {
          const dayDate = addDays(weekStart, idx);
          const dayKey = formatDateISO(dayDate);
          const daySessions = sessionsByDay[dayKey] || [];

          return (
            <div
              key={dayKey}
              className="flex flex-col rounded-2xl bg-white p-2 shadow-sm ring-1 ring-black/5 min-h-[120px]"
            >
              <div className="mb-2 border-b border-gray-100 pb-1">
                <p className="text-xs font-semibold uppercase tracking-wide text-gray-500">
                  {weekdayLabels[idx]}
                </p>
                <p className="text-xs text-gray-600">
                  {dayDate.toLocaleDateString()}
                </p>
              </div>

              {isLoading && idx === 0 && (
                <p className="text-xs text-gray-500">Cargando sesiones…</p>
              )}

              {!isLoading && daySessions.length === 0 && (
                <p className="text-xs text-gray-400">Sin clases.</p>
              )}

              {!isLoading && daySessions.length > 0 && (
                <div className="flex-1 space-y-1 overflow-auto">
                  {daySessions.map((s: any) => {
                    const start = s.start_time || s.start || s.starts_at;
                    const end = s.end_time || s.end || s.ends_at;
                    const activityName =
                      s.activity_name ||
                      s.activity?.name ||
                      s.activity ||
                      'Sesión';

                    const capacity = s.max_capacity ?? s.capacity;
                    const reserved =
                      s.reservation_count ?? s.reservations_count ?? 0;

                    return (
                      <div
                        key={s.id}
                        className="rounded-xl border border-gray-100 bg-slate-50 px-2 py-1 text-xs text-gray-800"
                      >
                        <div className="flex items-center justify-between">
                          <span className="font-medium truncate">
                            {activityName}
                          </span>
                          <span className="ml-2 text-[11px] text-gray-500">
                            {formatTime(start)} – {formatTime(end)}
                          </span>
                        </div>
                        <div className="mt-0.5 flex items-center justify-between text-[11px] text-gray-600">
                          {capacity != null && (
                            <span>
                              Aforo: {reserved}/{capacity}
                            </span>
                          )}
                          {s.is_recurrent && (
                            <span className="rounded-full bg-indigo-50 px-2 py-[1px] text-[10px] font-medium text-indigo-700">
                              Recurrente
                            </span>
                          )}
                        </div>
                      </div>
                    );
                  })}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default SessionsCalendar;
