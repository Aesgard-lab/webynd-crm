import * as React from "react";
import {
  List,
  Datagrid,
  TextField,
  BooleanField,
  NumberField,
  DateField,
  ReferenceField,
  SearchInput,
  SelectInput,
} from "react-admin";

const filters = [
  <SearchInput source="search" alwaysOn key="search" />,
  <SelectInput
    key="scope"
    source="scope"
    choices={[
      { id: "gym", name: "Gym" },
      { id: "franchise", name: "Franchise" },
    ]}
  />,
  <SelectInput
    key="is_active"
    source="is_active"
    choices={[
      { id: true, name: "Activas" },
      { id: false, name: "Inactivas" },
    ]}
  />,
  <SelectInput
    key="available_online"
    source="available_online"
    choices={[
      { id: true, name: "Online" },
      { id: false, name: "No online" },
    ]}
  />,
];

export default function BonusTemplateList(props) {
  return (
    <List
      {...props}
      filters={filters}
      perPage={25}
      sort={{ field: "id", order: "DESC" }}
      title="Bonos · Plantillas"
    >
      <Datagrid rowClick="edit">
        <TextField source="id" />
        <TextField source="name" label="Nombre" />
        <TextField source="scope" label="Scope" />

        <ReferenceField source="gym" reference="gyms" link={false} emptyText="—">
          <TextField source="name" />
        </ReferenceField>

        <ReferenceField source="franchise" reference="franchises" link={false} emptyText="—">
          <TextField source="name" />
        </ReferenceField>

        <NumberField source="duration_days" label="Duración (días)" />
        <TextField source="usage_limit_period" label="Límite" />
        <NumberField source="usage_limit_value" label="Valor límite" />
        <BooleanField source="is_recurring" label="Recurrente" />
        <BooleanField source="available_online" label="Online" />
        <BooleanField source="is_active" label="Activa" />
        <DateField source="created_at" label="Creada" showTime />
      </Datagrid>
    </List>
  );
}

