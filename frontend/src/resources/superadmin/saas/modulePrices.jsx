// src/resources/superadmin/saas/modulePrices.jsx
import {
  List, Datagrid, TextField, NumberField, BooleanField, DateField,
  TopToolbar, ExportButton, CreateButton,
  Create, Edit, SimpleForm,
  ReferenceInput, AutocompleteInput,
  SelectInput, NumberInput, BooleanInput, DateInput, TextInput,
  required, minValue,
} from "react-admin";

const cycleChoices = [
  { id: "monthly", name: "Mensual" },
  { id: "quarterly", name: "Trimestral" },
  { id: "annual", name: "Anual" },
];

const filters = [
  <TextInput key="q" source="q" label="Buscar" alwaysOn />,
  <ReferenceInput key="module" source="module" reference="saas/modules" perPage={50} label="Módulo">
    {/* ⬅️ la validación va EN EL HIJO */}
    <AutocompleteInput optionText="name" />
  </ReferenceInput>,
  <SelectInput key="cycle" source="cycle" label="Ciclo" choices={cycleChoices} />,
  <TextInput key="currency" source="currency" label="Moneda" />,
];

const ListActions = () => (
  <TopToolbar>
    <CreateButton />
    <ExportButton />
  </TopToolbar>
);

export function ModulePriceList() {
  return (
    <List
      perPage={20}
      filters={filters}
      sort={{ field: "module__code", order: "ASC" }}
      actions={<ListActions />}
    >
      <Datagrid rowClick="edit">
        <TextField source="id" />
        <TextField source="module_code" label="Código módulo" />
        <TextField source="module_name" label="Módulo" />
        <TextField source="cycle" label="Ciclo" />
        <NumberField source="amount" label="Importe" />
        <TextField source="currency" label="Moneda" />
        <BooleanField source="is_active" label="Activo" />
        <DateField source="effective_from" label="Vigente desde" />
        <DateField source="effective_to" label="Vigente hasta" />
        <DateField source="created_at" label="Creado" />
      </Datagrid>
    </List>
  );
}

export function ModulePriceCreate() {
  return (
    <Create>
      <SimpleForm>
        <ReferenceInput source="module" reference="saas/modules" label="Módulo" perPage={50}>
          {/* ⬅️ validación en el hijo */}
          <AutocompleteInput optionText="name" validate={[required()]} />
        </ReferenceInput>
        <SelectInput source="cycle" label="Ciclo" choices={cycleChoices} validate={[required()]} />
        <NumberInput source="amount" label="Importe" validate={[required(), minValue(0)]} />
        <TextInput source="currency" label="Moneda" defaultValue="EUR" />
        <BooleanInput source="is_active" label="Activo" defaultValue={true} />
        <DateInput source="effective_from" label="Vigente desde" />
        <DateInput source="effective_to" label="Vigente hasta" />
      </SimpleForm>
    </Create>
  );
}

export function ModulePriceEdit() {
  return (
    <Edit>
      <SimpleForm>
        <TextInput source="id" disabled />
        <ReferenceInput source="module" reference="saas/modules" label="Módulo" perPage={50}>
          {/* ⬅️ validación en el hijo */}
          <AutocompleteInput optionText="name" validate={[required()]} />
        </ReferenceInput>
        <SelectInput source="cycle" label="Ciclo" choices={cycleChoices} validate={[required()]} />
        <NumberInput source="amount" label="Importe" validate={[required(), minValue(0)]} />
        <TextInput source="currency" label="Moneda" />
        <BooleanInput source="is_active" label="Activo" />
        <DateInput source="effective_from" label="Vigente desde" />
        <DateInput source="effective_to" label="Vigente hasta" />
      </SimpleForm>
    </Edit>
  );
}
