import * as React from "react";
import {
  List,
  Datagrid,
  TextField,
  BooleanField,
  EditButton,
  TextInput,
  BooleanInput,
  ReferenceField,
} from "react-admin";

/**
 * Filtros:
 * - q: búsqueda por nombre (DRF -> ?search=)
 * - is_active: activar/desactivar filtro rápido
 */
const filters = [
  <TextInput key="q" source="q" label="Buscar" alwaysOn />,
  <BooleanInput key="active" source="is_active" label="Activa" />,
];

export default function ActivityCategoryList() {
  return (
    <List
      filters={filters}
      perPage={25}
      sort={{ field: "name", order: "ASC" }}
      title="Categorías de actividad"
    >
      <Datagrid rowClick="edit" bulkActionButtons={false}>
        <TextField source="id" />
        <TextField source="name" label="Nombre" />
        {/* Si tu API devuelve gym como id numérico, este ReferenceField lo resuelve */}
        <ReferenceField
          source="gym"
          reference="gyms"
          label="Gimnasio"
          link={false}
        >
          <TextField source="name" />
        </ReferenceField>
        <BooleanField source="is_active" label="Activa" />
        <EditButton />
      </Datagrid>
    </List>
  );
}
