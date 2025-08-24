// src/resources/clients.jsx
import {
  List, Datagrid, TextField,
  Edit, Create,
  TabbedForm, FormTab,
  TextInput, SelectInput, ReferenceInput,
  TopToolbar, CreateButton, ExportButton,
  useListContext, useGetIdentity, email, required,
  ImageField, ImageInput, AutocompleteArrayInput,
  FunctionField, useInput, useRecordContext,
} from 'react-admin';
import { FilterLiveSearch } from 'ra-ui-materialui';
import { Box, Chip, Stack } from '@mui/material';

/* ===== Toolbar con búsqueda ===== */
const ClientListActions = () => {
  const { total } = useListContext();
  return (
    <TopToolbar>
      <Box sx={{ flex: 1, mr: 2 }}>
        <FilterLiveSearch source="q" />
      </Box>
      <CreateButton />
      <ExportButton disabled={!total} />
    </TopToolbar>
  );
};

/* ===== Gym solo para superadmin ===== */
const GymInputIfSuper = () => {
  const { data: me } = useGetIdentity();
  if (!me?.roles?.superadmin) return null;
  return (
    <ReferenceInput source="gym" reference="gyms" sort={{ field: 'name', order: 'ASC' }} perPage={50}>
      <SelectInput optionText="name" />
    </ReferenceInput>
  );
};

/* ===== Input nativo para cámara (móvil) ===== */
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

/* ===== LIST ===== */
export const ClientList = (props) => {
  const currentGymId = localStorage.getItem('currentGymId') || 'none';
  return (
    <List
      key={`clients-${currentGymId}`}
      {...props}
      actions={<ClientListActions />}
      sort={{ field: 'id', order: 'DESC' }}
      perPage={10}
    >
      <Datagrid rowClick="edit">
        <TextField source="first_name" label="Nombre" />
        <TextField source="last_name" label="Apellidos" />
        <TextField source="email" />
        <TextField source="phone" label="Teléfono" />
        <FunctionField
          label="Etiquetas"
          render={(record) =>
            Array.isArray(record?.notes_tags) && record.notes_tags.length ? (
              <Stack direction="row" spacing={0.5} sx={{ flexWrap: 'wrap' }}>
                {record.notes_tags.map((t, i) => (
                  <Chip key={i} size="small" label={t} sx={{ mr: 0.5, mb: 0.5 }} />
                ))}
              </Stack>
            ) : ''
          }
        />
      </Datagrid>
    </List>
  );
};

/* ===== Campo de etiquetas con mapeo correcto ===== */
const TagsInput = () => {
  const record = useRecordContext();
  // Sembramos el desplegable con las etiquetas ya guardadas en el cliente,
  // para que se vean en la lista y al teclear se sugieran.
  const seedChoices = (record?.notes_tags || []).map((t) => ({ id: t, name: t }));

  return (
    <AutocompleteArrayInput
      source="notes_tags"
      label="Etiquetas"
      choices={seedChoices}
      onCreate={(tagName) => ({ id: tagName, name: tagName })}
      optionText="name"
      optionValue="id"
      // 👇 mapeo strings <-> objetos que espera el componente
      format={(value) => (value || []).map((t) => ({ id: t, name: t }))}
      parse={(value) => (value || []).map((o) => o.id)}
      helperText="Añade etiquetas y pulsa Enter"
      fullWidth
    />
  );
};

/* ===== Tabs del formulario ===== */
const ClientFormTabs = () => (
  <TabbedForm>
    <FormTab label="INFORMACIÓN">
      <GymInputIfSuper />
      <TextInput source="first_name" label="Nombre" validate={required('Requerido')} fullWidth />
      <TextInput source="last_name" label="Apellidos" fullWidth />

      {/* DNI */}
      <Box sx={{ display: 'grid', gridTemplateColumns: '1fr 120px', gap: 2 }}>
        <TextInput source="dni_number" label="DNI (número)" />
        <TextInput source="dni_letter" label="Letra" disabled />
      </Box>

      {/* Foto */}
      <ImageField source="photo" label="Foto actual" />
      <ImageInput source="photo" label="Subir nueva foto" accept="image/*">
        <ImageField source="src" title="title" />
      </ImageInput>
      <CameraFileInput source="photo" />
    </FormTab>

    <FormTab label="CONTACTO">
      <TextInput source="email" label="Email" validate={[required('Requerido'), email('Email inválido')]} fullWidth />
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

    <FormTab label="NOTAS">
      <TextInput source="notes" label="Notas" multiline fullWidth />
      <TagsInput />
    </FormTab>
  </TabbedForm>
);

/* ===== EDIT & CREATE ===== */
export const ClientEdit = (props) => (
  <Edit {...props}>
    <ClientFormTabs />
  </Edit>
);

export const ClientCreate = (props) => (
  <Create {...props}>
    <ClientFormTabs />
  </Create>
);

