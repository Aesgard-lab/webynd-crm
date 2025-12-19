// frontend/src/resources/clients/ClientPlansTab.jsx
import * as React from 'react';
import { useRecordContext, useDataProvider } from 'react-admin';
import { Box } from '@mui/material';
import { AssignPlanDialog } from './AssignPlanDialog';
import { getActiveGymId, formatShortDate } from './helpers';

const useClientPlans = (clientId) => {
  const dataProvider = useDataProvider();
  const [state, setState] = React.useState({
    loading: false,
    error: null,
    subscriptions: [],
    bonuses: [],
  });
  const [version, setVersion] = React.useState(0);

  const refetch = React.useCallback(() => {
    setVersion((v) => v + 1);
  }, []);

  React.useEffect(() => {
    if (!clientId) return;
    let active = true;
    const gymId = getActiveGymId();

    setState((s) => ({ ...s, loading: true, error: null }));

    const subFilter = {
      client: clientId,
      ...(gymId ? { gym: gymId } : {}),
      is_active: true,
    };

    const bonusFilter = {
      client: clientId,
      ...(gymId ? { gym: gymId } : {}),
      status: 'active',
    };

    Promise.all([
      dataProvider.getList('subscriptions', {
        filter: subFilter,
        pagination: { page: 1, perPage: 50 },
        sort: { field: 'id', order: 'DESC' },
      }),
      dataProvider.getList('bonuses', {
        filter: bonusFilter,
        pagination: { page: 1, perPage: 50 },
        sort: { field: 'id', order: 'DESC' },
      }),
    ])
      .then(([subsRes, bonosRes]) => {
        if (!active) return;
        setState({
          loading: false,
          error: null,
          subscriptions: subsRes.data || [],
          bonuses: bonosRes.data || [],
        });
      })
      .catch((error) => {
        if (!active) return;
        setState((s) => ({
          ...s,
          loading: false,
          error,
          subscriptions: [],
          bonuses: [],
        }));
      });

    return () => {
      active = false;
    };
  }, [clientId, dataProvider, version]);

  return { ...state, refetch };
};

export const ClientPlansTab = () => {
  const record = useRecordContext();
  const [dialogOpen, setDialogOpen] = React.useState(false);

  const { loading, error, subscriptions, bonuses, refetch } = useClientPlans(
    record?.id
  );

  if (!record) return null;

  return (
    <div className="flex h-full flex-col">
      <div className="mb-3 flex items-center justify-between">
        <div>
          <p className="text-xs font-semibold uppercase tracking-wide text-gray-500">
            Planes del cliente
          </p>
          <p className="text-xs text-gray-500">
            Suscripciones y bonos activos asignados a este cliente.
          </p>
        </div>
        <button
          type="button"
          onClick={() => setDialogOpen(true)}
          className="inline-flex items-center rounded-xl bg-indigo-600 px-3 py-1.5 text-xs font-medium text-white shadow-sm ring-1 ring-indigo-500/60 transition hover:bg-indigo-700 active:scale-[0.99]"
        >
          Añadir plan
        </button>
      </div>

      <div className="flex-1 overflow-auto space-y-4 text-xs text-gray-700">
        {loading && (
          <p className="text-xs text-gray-500">
            Cargando planes activos del cliente…
          </p>
        )}
        {!loading && error && (
          <p className="text-xs text-red-500">
            No se han podido cargar los planes (suscripciones y bonos). Revisa los
            endpoints de API.
          </p>
        )}

        {/* Suscripciones */}
        <div>
          <p className="mb-1 text-xs font-semibold uppercase tracking-wide text-gray-500">
            Suscripciones activas
          </p>
          {(!subscriptions || subscriptions.length === 0) && (
            <p className="text-xs text-gray-500">
              No hay suscripciones activas para este cliente.
            </p>
          )}
          {subscriptions && subscriptions.length > 0 && (
            <table className="mt-1 w-full text-xs">
              <thead>
                <tr className="border-b border-gray-200">
                  <th className="py-1 text-left font-medium text-gray-500">Plan</th>
                  <th className="py-1 text-left font-medium text-gray-500">Inicio</th>
                  <th className="py-1 text-left font-medium text-gray-500">Fin</th>
                  <th className="py-1 text-left font-medium text-gray-500">Estado</th>
                </tr>
              </thead>
              <tbody>
                {subscriptions.map((s) => (
                  <tr key={s.id} className="border-b border-gray-50">
                    <td className="py-1 pr-2">
                      {s.plan_name || s.name || `Suscripción #${s.id}`}
                    </td>
                    <td className="py-1 pr-2">{formatShortDate(s.start_date)}</td>
                    <td className="py-1 pr-2">{formatShortDate(s.end_date)}</td>
                    <td className="py-1 text-gray-700">
                      {(s.status || s.is_active ? 'activa' : 'inactiva').toString()}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>

        {/* Bonos */}
        <div>
          <p className="mb-1 text-xs font-semibold uppercase tracking-wide text-gray-500">
            Bonos activos
          </p>
          {(!bonuses || bonuses.length === 0) && (
            <p className="text-xs text-gray-500">
              No hay bonos activos para este cliente.
            </p>
          )}
          {bonuses && bonuses.length > 0 && (
            <table className="mt-1 w-full text-xs">
              <thead>
                <tr className="border-b border-gray-200">
                  <th className="py-1 text-left font-medium text-gray-500">Bono</th>
                  <th className="py-1 text-left font-medium text-gray-500">Usos</th>
                  <th className="py-1 text-left font-medium text-gray-500">Inicio</th>
                  <th className="py-1 text-left font-medium text-gray-500">
                    Caducidad
                  </th>
                </tr>
              </thead>
              <tbody>
                {bonuses.map((b) => (
                  <tr key={b.id} className="border-b border-gray-50">
                    <td className="py-1 pr-2">
                      {b.plan_name || b.name || `Bono #${b.id}`}
                    </td>
                    <td className="py-1 pr-2">
                      {`${b.used_quantity || 0}/${b.assigned_quantity || 0}`}
                    </td>
                    <td className="py-1 pr-2">{formatShortDate(b.start_date)}</td>
                    <td className="py-1 pr-2">{formatShortDate(b.expires_at)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </div>

      <AssignPlanDialog
        open={dialogOpen}
        onClose={() => setDialogOpen(false)}
        client={record}
        onAssigned={refetch}
      />
    </div>
  );
};
