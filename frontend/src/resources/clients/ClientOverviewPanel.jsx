// frontend/src/resources/clients/ClientOverviewPanel.jsx
import * as React from 'react';
import { useRecordContext } from 'react-admin';
import { ClientPlansTab } from './ClientPlansTab';

export const ClientOverviewPanel = () => {
  const record = useRecordContext();
  const [tab, setTab] = React.useState('summary');

  if (!record) return null;

  const tabs = [
    { id: 'summary', label: 'Resumen' },
    { id: 'plans', label: 'Planes' },
  ];

  return (
    <div className="flex h-full flex-col rounded-2xl bg-white shadow-sm ring-1 ring-black/5">
      <div className="flex border-b border-gray-100 px-4 pt-3">
        {tabs.map((t) => (
          <button
            key={t.id}
            type="button"
            onClick={() => setTab(t.id)}
            className={`mr-3 border-b-2 px-1 pb-2 text-sm font-medium ${
              tab === t.id
                ? 'border-indigo-500 text-indigo-600'
                : 'border-transparent text-gray-500 hover:text-gray-800'
            }`}
          >
            {t.label}
          </button>
        ))}
      </div>

      <div className="flex-1 overflow-auto px-4 py-3 text-sm text-gray-700">
        {tab === 'summary' && (
          <p className="text-xs text-gray-500">
            Aquí mostraremos próximas reservas, suscripciones activas y últimos pagos.
          </p>
        )}
        {tab === 'plans' && <ClientPlansTab />}
      </div>
    </div>
  );
};
