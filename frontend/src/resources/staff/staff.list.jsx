import * as React from "react";
import {
  List,
  Datagrid,
  TextField,
  EmailField,
  BooleanField,
  DateField,
} from "react-admin";

export default function StaffList() {
  return (
    <List>
      <Datagrid rowClick="edit">
        <TextField source="full_name" label="Nombre" />
        <TextField source="job_role" label="Rol" />
        <EmailField source="email" label="Email" />
        <TextField source="phone" label="Teléfono" />
        <BooleanField source="active" label="Activo" />
        <DateField source="hire_date" label="Fecha contratación" />
      </Datagrid>
    </List>
  );
}
