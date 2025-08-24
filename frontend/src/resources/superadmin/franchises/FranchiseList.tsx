import * as React from "react";
import {
  List,
  Datagrid,
  TextField,
  BooleanField,
  DateField,
  ReferenceField,
  FunctionField,
  EditButton,
} from "react-admin";
import { Box, Avatar } from "@mui/material";

export default function FranchiseList(props: any) {
  return (
    <List {...props} title="Franquicias" sort={{ field: "name", order: "ASC" }}>
      <Datagrid rowClick="edit">
        <FunctionField
          label="Logo"
          render={(record: any) =>
            record.logo ? (
              <Avatar src={record.logo} alt={record.name} />
            ) : (
              <Avatar>{record.name?.[0]}</Avatar>
            )
          }
        />
        <TextField source="name" label="Nombre" />
        <TextField source="slug" />
        <ReferenceField source="owner" reference="users" label="Propietario" link="show">
          <TextField source="email" />
        </ReferenceField>
        <FunctionField
          label="Colores"
          render={(record: any) => (
            <Box display="flex" gap={1}>
              <Box sx={{ width: 24, height: 24, bgcolor: record.primary_color, borderRadius: "50%" }} />
              <Box sx={{ width: 24, height: 24, bgcolor: record.secondary_color, borderRadius: "50%" }} />
            </Box>
          )}
        />
        <BooleanField source="is_active" label="Activo" />
        <TextField source="gyms_count" label="#Gyms" />
        <DateField source="created_at" label="Creado" />
        <EditButton />
      </Datagrid>
    </List>
  );
}
