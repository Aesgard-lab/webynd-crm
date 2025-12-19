// src/resources/scheduler/index.jsx
import * as React from "react";
import {
  Title,
  useGetList,
  useDataProvider,
  useNotify,
  useRefresh,
} from "react-admin";

const startOfWeekMonday = (d) => {
  const date = new Date(d);
  const day = date.getDay(); // 0 = domingo, 1 = lunes...
  const diff = (day === 0 ? -6 : 1) - day; // llevar a lunes
  date.setDate(date.getDate() + diff);
  date.setHours(0, 0, 0, 0);
  return date;
};

const addDays = (d, days) => {
  const copy = new Date(d);
  copy.setDate(copy.getDate() + days);
  return copy;
};

const formatDateISO = (d) => d.toISOString().split("T")[0];

const formatTime = (value) => {
  if (!value) return "";
  const d = new Date(value);
  if (Number.isNaN(d.getTime())) return value;
  return d.toLocaleTimeString(undefined, {
    hour: "2-digit",
    minute: "2-digit",
  });
};

const weekdayLabels = [
  "Lunes",
  "Martes",
  "Miércoles",
  "Jueves",
  "Viernes",
  "Sábado",
  "Domingo",
];

const SessionsCalendarInner = () => {
  const [weekStart, setWeekStart] = React.useState(() =>
    startOfWeekMonday(new Date())
  );
  const weekEnd = addDays(weekStart, 6);
  const dateFrom = formatDateISO(weekStart);
  const dateTo = formatDateISO(weekEnd);

  // Sesiones de la semana
  const { data: sessionsData, isLoading } = useGetList("scheduler/sessions", {
    filter: { date_from: dateFrom, date_to: dateTo },
    pagination: { page: 1, perPage: 500 },
    sort: { field: "start_time", order: "ASC" },
  });
  const sessions = sessionsData || [];

  // Actividades para el selector (cuando tengas el módulo listo)
  const { data: activitiesData } = useGetList("activities", {
    filter: {},
    pagination: { page: 1, perPage: 100 },
    sort: { field: "name", order: "ASC" },
  });
  const activities = activitiesData || [];

  // Staff / entrenadores para el multi-select
  const { data: staffData } = useGetList("staff", {
    filter: {},
    pagination: { page: 1, perPage: 200 },
    sort: { field: "first_name", order: "ASC" },
  });
  const staffList = staffData || [];

  const sessionsByDay = React.useMemo(() => {
    const map = {};
    sessions.forEach((s) => {
      const start = s.start_time || s.start || s.starts_at;
      if (!start) return;
      const d = new Date(start);
      if (Number.isNaN(d.getTime())) return;
      const dayKey = formatDateISO(d);
      if (!map[dayKey]) map[dayKey] = [];
      map[dayKey].push(s);
    });

    Object.keys(map).forEach((key) => {
      map[key].sort((a, b) => {
        const da = new Date(a.start_time || a.start || a.starts_at).getTime();
        const db = new Date(b.start_time || b.start || b.starts_at).getTime();
        return da - db;
      });
    });

    return map;
  }, [sessions]);

  const goPrevWeek = () => setWeekStart((prev) => addDays(prev, -7));
  const goNextWeek = () => setWeekStart((prev) => addDays(prev, 7));
  const goThisWeek = () => setWeekStart(startOfWeekMonday(new Date()));

  // -------- Crear sesión desde el calendario --------
  const [dialogOpen, setDialogOpen] = React.useState(false);
  const [selectedDate, setSelectedDate] = React.useState(null);
  const [form, setForm] = React.useState({
    activity: "",
    start: "09:00",
    end: "10:00",
    max_capacity: 8,
    is_recurrent: false,
    repeat_until: "",
    staff_ids: [],
  });

  const dataProvider = useDataProvider();
  const notify = useNotify();
  const refresh = useRefresh();

  const openCreateDialog = (dayDate) => {
    setSelectedDate(dayDate);
    setForm((prev) => ({
      ...prev,
      start: "09:00",
      end: "10:00",
      is_recurrent: false,
      repeat_until: "",
    }));
    setDialogOpen(true);
  };

  const closeDialog = () => {
    setDialogOpen(false);
    setSelectedDate(null);
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleCheckboxChange = (e) => {
    const { name, checked } = e.target;
    setForm((prev) => ({ ...prev, [name]: checked }));
  };

  const handleStaffChange = (e) => {
    const options = Array.from(e.target.selectedOptions || []);
    const values = options.map((opt) => opt.value);
    setForm((prev) => ({ ...prev, staff_ids: values }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!selectedDate) return;

    const gymIdRaw = localStorage.getItem("currentGymId");
    const gymId = gymIdRaw ? Number(gymIdRaw) : null;
    if (!gymId) {
      notify("Selecciona primero una sede (gym) desde tu avatar.", {
        type: "warning",
      });
      return;
    }

    if (!form.activity) {
      notify("Selecciona una actividad.", { type: "warning" });
      return;
    }

    const [startHour, startMin] = form.start.split(":").map((n) => Number(n));
    const [endHour, endMin] = form.end.split(":").map((n) => Number(n));

    if (
      Number.isNaN(startHour) ||
      Number.isNaN(startMin) ||
      Number.isNaN(endHour) ||
      Number.isNaN(endMin)
    ) {
      notify("Formato de hora no válido.", { type: "warning" });
      return;
    }

    const startDate = new Date(selectedDate);
    startDate.setHours(startHour, startMin, 0, 0);
    const endDate = new Date(selectedDate);
    endDate.setHours(endHour, endMin, 0, 0);

    if (endDate <= startDate) {
      notify("La hora de fin debe ser posterior a la de inicio.", {
        type: "warning",
      });
      return;
    }

    // Recurrencia
    const isRecurrent = !!form.is_recurrent;
    const weekdayIndex = (selectedDate.getDay() + 6) % 7; // 0=Lun..6=Dom
    const repeatUntil =
      isRecurrent && form.repeat_until ? form.repeat_until : null;
    const repeatDays = isRecurrent ? String(weekdayIndex) : "";

    // Staff
    const staffIds =
      form.staff_ids && form.staff_ids.length
        ? form.staff_ids.map((id) => Number(id))
        : [];

    try {
      await dataProvider.create("scheduler/sessions", {
        data: {
          gym: gymId,
          activity: Number(form.activity),
          start_time: startDate.toISOString(),
          end_time: endDate.toISOString(),
          max_capacity:
            form.max_capacity !== "" ? Number(form.max_capacity) : null,
          is_recurrent: isRecurrent,
          repeat_until: repeatUntil,
          repeat_days: repeatDays,
          staff: staffIds,
        },
      });
      notify("Sesión creada correctamente.", { type: "info" });
      closeDialog();
      refresh();
    } catch (error) {
      console.error(error);
      notify("No se ha podido crear la sesión.", { type: "warning" });
    }
  };

  // Helper para pintar entrenadores en la tarjeta
  const getStaffNamesFromSession = (session) => {
    // 1) si el backend devuelve objetos en session.staff
    if (Array.isArray(session.staff) && session.staff.length) {
      return session.staff
        .map((s) => s.first_name || s.name || s.email || `ID ${s.id}`)
        .filter(Boolean);
    }

    // 2) otros nombres típicos
    if (Array.isArray(session.instructors) && session.instructors.length) {
      return session.instructors
        .map((s) => s.first_name || s.name || s.email || `ID ${s.id}`)
        .filter(Boolean);
    }
    if (
      Array.isArray(session.staff_detail) &&
      session.staff_detail.length
    ) {
      return session.staff_detail
        .map((s) => s.first_name || s.name || s.email || `ID ${s.id}`)
        .filter(Boolean);
    }

    // 3) si solo tenemos ids, intentamos mapear contra staffList
    if (Array.isArray(session.staff_ids) && session.staff_ids.length) {
      const ids = session.staff_ids;
      return staffList
        .filter((st) => ids.includes(st.id))
        .map((st) => st.first_name || st.name || st.email || `ID ${st.id}`);
    }

    if (Array.isArray(session.staff) && session.staff.length) {
      // lista de ids crudos
      const ids = session.staff;
      return staffList
        .filter((st) => ids.includes(st.id))
        .map((st) => st.first_name || st.name || st.email || `ID ${st.id}`);
    }

    return [];
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
          Semana del{" "}
          <span className="font-semibold">
            {weekStart.toLocaleDateString()}
          </span>{" "}
          al{" "}
          <span className="font-semibold">{weekEnd.toLocaleDateString()}</span>
        </div>
      </div>

      {/* Calendario semanal: 7 columnas */}
      <div className="grid gap-2 md:grid-cols-7 grid-cols-1">
        {Array.from({ length: 7 }).map((_, idx) => {
          const dayDate = addDays(weekStart, idx);
          const dayKey = formatDateISO(dayDate);
          const daySessions = sessionsByDay[dayKey] || [];

          return (
            <div
              key={dayKey}
              className="flex flex-col rounded-2xl bg-white p-2 shadow-sm ring-1 ring-black/5 min-h-[140px]"
            >
              <div className="mb-2 flex items-start justify-between border-b border-gray-100 pb-1">
                <div>
                  <p className="text-xs font-semibold uppercase tracking-wide text-gray-500">
                    {weekdayLabels[idx]}
                  </p>
                  <p className="text-xs text-gray-600">
                    {dayDate.toLocaleDateString()}
                  </p>
                </div>
                <button
                  type="button"
                  onClick={() => openCreateDialog(dayDate)}
                  className="rounded-full bg-indigo-50 px-2 py-[2px] text-[11px] font-medium text-indigo-700 hover:bg-indigo-100"
                >
                  + Añadir
                </button>
              </div>

              {isLoading && idx === 0 && (
                <p className="text-xs text-gray-500">Cargando sesiones…</p>
              )}

              {!isLoading && daySessions.length === 0 && (
                <p className="text-xs text-gray-400">Sin clases.</p>
              )}

              {!isLoading && daySessions.length > 0 && (
                <div className="flex-1 space-y-1 overflow-auto">
                  {daySessions.map((s) => {
                    const start = s.start_time || s.start || s.starts_at;
                    const end = s.end_time || s.end || s.ends_at;
                    const activityName =
                      s.activity_name ||
                      s.activity?.name ||
                      s.activity ||
                      "Sesión";

                    const capacity = s.max_capacity ?? s.capacity;
                    const reserved =
                      s.reservation_count ?? s.reservations_count ?? 0;
                    const staffNames = getStaffNamesFromSession(s);

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

                        {staffNames.length > 0 && (
                          <div className="mt-0.5 text-[11px] text-gray-500 truncate">
                            {staffNames.slice(0, 2).join(", ")}
                            {staffNames.length > 2 &&
                              ` +${staffNames.length - 2} más`}
                          </div>
                        )}
                      </div>
                    );
                  })}
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* Modal sencillo para crear sesión */}
      {dialogOpen && selectedDate && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/20">
          <div className="w-full max-w-md rounded-2xl bg-white p-4 shadow-xl">
            <h2 className="mb-3 text-sm font-semibold text-gray-800">
              Crear sesión – {selectedDate.toLocaleDateString()}
            </h2>

            <form onSubmit={handleSubmit} className="space-y-3 text-sm">
              <div>
                <label className="mb-1 block text-xs font-medium text-gray-600">
                  Actividad
                </label>
                <select
                  name="activity"
                  value={form.activity}
                  onChange={handleChange}
                  className="w-full rounded-xl border border-gray-300 px-2 py-1.5 text-sm focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500"
                >
                  <option value="">Selecciona actividad</option>
                  {activities.map((a) => (
                    <option key={a.id} value={a.id}>
                      {a.name}
                    </option>
                  ))}
                </select>
              </div>

              <div className="flex gap-2">
                <div className="flex-1">
                  <label className="mb-1 block text-xs font-medium text-gray-600">
                    Hora inicio
                  </label>
                  <input
                    type="time"
                    name="start"
                    value={form.start}
                    onChange={handleChange}
                    className="w-full rounded-xl border border-gray-300 px-2 py-1.5 text-sm focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500"
                  />
                </div>
                <div className="flex-1">
                  <label className="mb-1 block text-xs font-medium text-gray-600">
                    Hora fin
                  </label>
                  <input
                    type="time"
                    name="end"
                    value={form.end}
                    onChange={handleChange}
                    className="w-full rounded-xl border border-gray-300 px-2 py-1.5 text-sm focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500"
                  />
                </div>
              </div>

              <div>
                <label className="mb-1 block text-xs font-medium text-gray-600">
                  Aforo máximo
                </label>
                <input
                  type="number"
                  name="max_capacity"
                  value={form.max_capacity}
                  onChange={handleChange}
                  className="w-full rounded-xl border border-gray-300 px-2 py-1.5 text-sm focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500"
                  min={1}
                />
              </div>

              {/* Recurrencia */}
              <div className="rounded-xl bg-slate-50 px-3 py-2">
                <label className="flex items-center gap-2 text-xs font-medium text-gray-700">
                  <input
                    type="checkbox"
                    name="is_recurrent"
                    checked={form.is_recurrent}
                    onChange={handleCheckboxChange}
                  />
                  Repetir semanalmente
                </label>
                {form.is_recurrent && (
                  <div className="mt-2">
                    <label className="mb-1 block text-[11px] font-medium text-gray-600">
                      Hasta (incluido)
                    </label>
                    <input
                      type="date"
                      name="repeat_until"
                      value={form.repeat_until}
                      onChange={handleChange}
                      className="w-full rounded-xl border border-gray-300 px-2 py-1.5 text-sm focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500"
                    />
                    <p className="mt-1 text-[11px] text-gray-500">
                      Se creará esta misma clase cada semana, el mismo día, hasta
                      la fecha indicada.
                    </p>
                  </div>
                )}
              </div>

              {/* Entrenadores */}
              <div>
                <label className="mb-1 block text-xs font-medium text-gray-600">
                  Entrenador/es
                </label>
                <select
                  multiple
                  name="staff_ids"
                  value={form.staff_ids}
                  onChange={handleStaffChange}
                  className="h-24 w-full rounded-xl border border-gray-300 px-2 py-1.5 text-sm focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500"
                >
                  {staffList.map((s) => (
                    <option key={s.id} value={s.id}>
                      {s.first_name || s.name || s.email || `Staff #${s.id}`}
                    </option>
                  ))}
                </select>
                <p className="mt-1 text-[11px] text-gray-500">
                  Mantén pulsado Ctrl (o Cmd en Mac) para seleccionar varios.
                </p>
              </div>

              <div className="mt-4 flex justify-end gap-2">
                <button
                  type="button"
                  onClick={closeDialog}
                  className="rounded-xl border border-gray-300 bg-white px-3 py-1.5 text-xs font-medium text-gray-700 hover:bg-gray-50"
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  className="rounded-xl bg-indigo-600 px-3 py-1.5 text-xs font-medium text-white hover:bg-indigo-700"
                >
                  Guardar sesión
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

// Este es el componente que React-Admin usará como list del recurso
export const SchedulerSessionsList = (props) => {
  return <SessionsCalendarInner />;
};

export default SchedulerSessionsList;
