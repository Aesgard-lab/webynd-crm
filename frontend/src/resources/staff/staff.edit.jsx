import * as React from "react";
import {
  Edit,
  SimpleForm,
  TextInput,
  DateInput,
  BooleanInput,
  SelectInput,
  NumberInput,
} from "react-admin";

const roles = [
  { id: "instructor", name: "Instructor" },
  { id: "reception", name: "Recepción" },
  { id: "manager", name: "Manager" },
  { id: "admin", name: "Administrador" },
];

export default function StaffEdit() {
  return (
    <Edit title="Editar empleado">
      <SimpleForm>
        <TextInput source="first_name" label="Nombre" />
        <TextInput source="last_name" label="Apellidos" />
        <TextInput source="email" label="Email" />
        <TextInput source="phone" label="Teléfono" />
        <SelectInput source="job_role" label="Rol" choices={roles} />

        <BooleanInput source="active" label="Activo" />

        <DateInput source="hire_date" label="Fecha de contratación" />
        <DateInput source="termination_date" label="Fecha de baja" />

        <NumberInput source="hourly_cost" label="Coste hora (€)" />

        <TextInput source="internal_notes" label="Notas internas" multiline />
      </SimpleForm>
    </Edit>
  );
}
