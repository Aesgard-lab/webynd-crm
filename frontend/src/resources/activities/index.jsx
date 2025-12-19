// src/resources/activities/index.jsx
import * as React from "react";
import {
  List,
  Datagrid,
  TextField,
  BooleanField,
  TopToolbar,
  CreateButton,
  ExportButton,
  useListContext,
} from "react-admin";
import { FilterLiveSearch } from "ra-ui-materialui";
import { Box, Chip } from "@mui/material";

/** Barra de acciones con búsqueda + crear + exportar */
const Actions = () => {
  const { total } = useListContext();
  return (
    <TopToolbar>
      <Box sx={{ flex: 1, mr: 2 }}>
        <FilterLiveSearch source="q" placeholder="Buscar actividades..." />
      </Box>
      <CreateButton label="Crear" />
      <ExportButton disabled={!total} />
    </TopToolbar>
  );
};

/** Campo calculado de duración en h/min */
const DurationField = ({ record }) => {
  if (!record) return null;
  const minutes = record.duration_minutes ?? record.duration ?? null;
  if (minutes == null) return <span>—</span>;
  const m = Number(minutes);
  const h = Math.floor(m / 60);
  const mm = m % 60;
  return (
    <span>
      {h ? `${h}h ` : ""}
      {mm}min
    </span>
  );
};

/** Chip de intensidad (Alta, Media, Baja) */
const IntensityPill = ({ record }) => {
  if (!record?.intensity) return <span>—</span>;
  const v = String(record.intensity).toLowerCase();
  const color =
    v === "high" || v === "alta"
      ? "error"
      : v === "medium" || v === "media"
      ? "warning"
      : "success";
  const label =
    v === "high"
      ? "Alta"
      : v === "medium"
      ? "Media"
      : v === "low"
      ? "Baja"
      : record.intensity;
  return (
    <Chip size="small" label={label} color={color} variant="outlined" />
  );
};

/** Listado de actividades */
export const ActivityList = (props) => (
  <List
    {...props}
    title="Actividades"
    actions={<Actions />}
    perPage={10}
    sort={{ field: "id", order: "DESC" }}
  >
    <Datagrid rowClick="edit" bulkActionButtons={false}>
      <TextField source="name" label="Nombre" />
      <TextField source="category.name" label="Categoría" />
      <TextField source="subcategory.name" label="Subcategoría" />
      <DurationField label="Duración" />
      <IntensityPill label="Intensidad" />
      <BooleanField source="is_active" label="Activa" />
    </Datagrid>
  </List>
);

export default ActivityList;
