// frontend/src/resources/clients/ClientEditLayout.jsx
import * as React from 'react';
import {
  Edit,
  Create,
  TabbedForm,
  FormTab,
  TextInput,
  DateInput,
  BooleanInput,
  SelectInput,
  ImageField,
  ImageInput,
  useInput,
  useRecordContext,
  useGetIdentity,
  email,
  required,
  useRedirect,
  ReferenceInput,
  AutocompleteArrayInput,
} from 'react-admin';
import { Box } from '@mui/material';
import {
  computeAge,
  getActiveGymName,
  getCardLabel,
  getAlertLabelAndColor,
  getInitials,
} from './helpers';
import { ClientOverviewPanel } from './ClientOverviewPanel';

const TagsInput = () => {
  const record = useRecordContext();
  const seedChoices = (record?.notes_tags || []).map((t) => ({ id: t, name: t }));

  return (
    <AutocompleteArrayInput
      source="notes_tags"
      label="Etiquetas"
      choices={seedChoices}
      onCreate={(tagName) => ({ id: tagName, name: tagName })}
      optionText="name"
      optionValue="id"
      fullWidth
    />
  );
};

const GymInputIfSuper = () => {
  const { data: me } = useGetIdentity();
  if (!me || me.role !== 'superadmin') return null;

  return (
    <ReferenceInput
      source="gym"
      reference="gyms"
      sort={{ field: 'name', order: 'ASC' }}
      perPage={50}
    >
      <SelectInput optionText="name" />
    </ReferenceInput>
  );
};

const CameraFileInput = ({ source }) => {
  const { field } = useInput({ source });
  return (
    <Box sx={{ mt: 1 }}>
      <input
        type="file"
        accept="image/*"
        capture="environment"
        onChange={(e) => field.onChange(e.target.files?.[0] || null)}
      />
    </Box>
  );
};

const ClientFormTabs = () => (
  <TabbedForm>
    <FormTab label="INFORMACIÓN">
      <GymInputIfSuper />
      <TextInput
        source="first_name"
        label="Nombre"
        validate={required('Requerido')}
        fullWidth
      />
      <TextInput source="last_name" label="Apellidos" fullWidth />
      <DateInput source="date_of_birth" label="Fecha de nacimiento" fullWidth />
      <Box sx={{ display: 'grid', gridTemplateColumns: '1fr 120px', gap: 2, mt: 1 }}>
        <TextInput source="dni_number" label="DNI (número)" />
        <TextInput source="dni_letter" label="Letra" disabled />
      </Box>
      <Box sx={{ mt: 2 }}>
        <BooleanInput source="is_active" label="Cliente activo" />
      </Box>
      <Box sx={{ mt: 2 }}>
        <ImageField source="photo" label="Foto actual" />
        <ImageInput source="photo" label="Subir nueva foto" accept="image/*">
          <ImageField source="src" title="title" />
        </ImageInput>
        <CameraFileInput source="photo" />
      </Box>
    </FormTab>

    <FormTab label="CONTACTO">
      <TextInput
        source="email"
        label="Email"
        validate={[required('Requerido'), email('Email inválido')]}
        fullWidth
      />
      <TextInput source="phone" label="Teléfono" fullWidth />
      <TextInput source="address" label="Dirección" fullWidth />
      <TextInput source="zip_code" label="CP" fullWidth />
      <SelectInput
        source="alert_level"
        label="Alerta"
        choices={[
          { id: 'none', name: 'Sin alerta' },
          { id: 'vip', name: 'VIP' },
          { id: 'low', name: 'Alerta leve' },
          { id: 'medium', name: 'Alerta moderada' },
          { id: 'high', name: 'Alerta grave' },
        ]}
        fullWidth
      />
    </FormTab>

    <FormTab label="EMERGENCIA">
      <TextInput
        source="emergency_contact_name"
        label="Nombre contacto de emergencia"
        fullWidth
      />
      <TextInput
        source="emergency_contact_relation"
        label="Relación"
        fullWidth
      />
      <TextInput
        source="emergency_contact_phone"
        label="Teléfono de emergencia"
        fullWidth
      />
      <TextInput
        source="emergency_contact_notes"
        label="Notas de emergencia"
        multiline
        fullWidth
      />
    </FormTab>

    <FormTab label="NOTAS">
      <TextInput source="notes" label="Notas" multiline fullWidth />
      <TagsInput />
    </FormTab>
  </TabbedForm>
);

/* ---------------- CABECERA DEL CLIENTE ---------------- */

const ClientHeaderBar = () => {
  const record = useRecordContext();
  const redirect = useRedirect();

  if (!record) return null;

  const fullName =
    record.full_name ||
    `${record.first_name || ''} ${record.last_name || ''}`.trim() ||
    'Cliente';
  const age = computeAge(record.date_of_birth);
  const gymName = getActiveGymName();
  const cardLabel = getCardLabel(record);
  const { label: alertLabel, className: alertClass } = getAlertLabelAndColor(
    record.alert_level
  );
  const initials = getInitials(record.first_name, record.last_name);

  return (
    <div className="flex items-center justify-between gap-4 rounded-2xl bg-white px-4 py-3 shadow-sm ring-1 ring-black/5">
      <div className="flex min-w-0 items-center gap-3">
        {record.photo ? (
          <img
            src={record.photo}
            alt={fullName}
            className="h-14 w-14 rounded-2xl object-cover ring-1 ring-black/10"
          />
        ) : (
          <div className="grid h-14 w-14 place-items-center rounded-2xl bg-gray-100 ring-1 ring-black/10">
            <span className="text-lg font-semibold text-gray-600">{initials}</span>
          </div>
        )}

        <div className="min-w-0 space-y-1">
          <div className="flex flex-wrap items-center gap-2">
            <h1 className="truncate text-base font-semibold text-gray-900">
              {fullName}
            </h1>
            {age != null && (
              <span className="rounded-full bg-gray-100 px-2 py-0.5 text-xs font-medium text-gray-700">
                {age} años
              </span>
            )}
            <span
              className={`rounded-full px-2 py-0.5 text-xs font-medium ${
                record.is_active
                  ? 'bg-emerald-100 text-emerald-800'
                  : 'bg-gray-200 text-gray-700'
              }`}
            >
              {record.is_active ? 'Activo' : 'Inactivo'}
            </span>
            <span
              className={`rounded-full px-2 py-0.5 text-xs font-medium ${alertClass}`}
            >
              {alertLabel}
            </span>
          </div>

          <div className="flex flex-wrap items-center gap-x-3 gap-y-1 text-xs text-gray-600">
            <span className="truncate">
              Gimnasio:&nbsp;
              <span className="font-medium text-gray-800">{gymName}</span>
            </span>
            <span className="truncate">
              Pago:&nbsp;
              <span className="font-medium text-gray-800">{cardLabel}</span>
            </span>
          </div>
        </div>
      </div>

      <div className="flex flex-shrink-0 items-center gap-2">
        <button
          type="button"
          onClick={() => redirect('/scheduler')}
          className="inline-flex items-center rounded-xl border border-gray-200 bg-white px-3 py-1.5 text-xs font-medium text-gray-900 shadow-sm ring-1 ring-black/5 transition hover:bg-gray-50 active:scale-[0.99]"
        >
          Crear reserva
        </button>
        <button
          type="button"
          onClick={() => redirect('/backoffice/checkout')}
          className="inline-flex items-center rounded-xl bg-indigo-600 px-3 py-1.5 text-xs font-medium text-white shadow-sm ring-1 ring-indigo-500/60 transition hover:bg-indigo-700 active:scale-[0.99]"
        >
          Cobrar
        </button>
      </div>
    </div>
  );
};

/* ---------------- LAYOUT ---------------- */

const ClientEditLayoutInner = () => {
  const record = useRecordContext();
  if (!record) return null;

  return (
    <Box
      sx={{
        p: 2,
        bgcolor: '#f3f4f6',
      }}
    >
      <div className="mb-3">
        <ClientHeaderBar />
      </div>

      <div className="grid gap-3 lg:grid-cols-[minmax(0,2fr)_minmax(0,1.6fr)]">
        <div className="min-h-[400px] rounded-2xl bg-white p-2 shadow-sm ring-1 ring-black/5">
          <ClientFormTabs />
        </div>

        <div className="min-h-[300px]">
          <ClientOverviewPanel />
        </div>
      </div>
    </Box>
  );
};

/* ---------------- EXPORTS RA ---------------- */

export const ClientEdit = (props) => (
  <Edit {...props} component="div">
    <ClientEditLayoutInner />
  </Edit>
);

export const ClientCreate = (props) => (
  <Create {...props}>
    <ClientFormTabs />
  </Create>
);
