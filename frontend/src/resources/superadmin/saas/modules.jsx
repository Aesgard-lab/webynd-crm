// frontend/src/resources/superadmin/saas/modules.jsx
import * as React from 'react';
import {
  List,
  Datagrid,
  TextField,
  BooleanField,
  DateField,
  Edit,
  Create,
  SimpleForm,
  TextInput,
  BooleanInput,
  EditButton,
} from 'react-admin';

// LISTA
export const ModuleList = (props) => (
  <List {...props} title="Módulos">
    <Datagrid rowClick="edit">
      <TextField source="id" />
      <TextField source="code" label="Código" />
      <TextField source="name" label="Nombre" />
      <BooleanField source="is_active" label="Activo" />
      <DateField source="created_at" label="Creado" />
      <EditButton />
    </Datagrid>
  </List>
);

// EDITAR
export const ModuleEdit = (props) => (
  <Edit {...props} title="Editar Módulo">
    <SimpleForm>
      <TextInput source="code" label="Código" fullWidth />
      <TextInput source="name" label="Nombre" fullWidth />
      <TextInput source="description" label="Descripción" fullWidth multiline />
      <BooleanInput source="is_active" label="Activo" />
    </SimpleForm>
  </Edit>
);

// CREAR
export const ModuleCreate = (props) => (
  <Create {...props} title="Crear Módulo">
    <SimpleForm>
      <TextInput source="code" label="Código" fullWidth />
      <TextInput source="name" label="Nombre" fullWidth />
      <TextInput source="description" label="Descripción" fullWidth multiline />
      <BooleanInput source="is_active" label="Activo" />
    </SimpleForm>
  </Create>
);
