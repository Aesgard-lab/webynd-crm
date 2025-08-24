import * as React from "react";
import {
  Create,
  SimpleForm,
  TextInput,
  BooleanInput,
  ReferenceInput,
  SelectInput,
  ImageInput,
  ImageField,
} from "react-admin";

export default function FranchiseCreate(props: any) {
  return (
    <Create {...props} title="Crear Franquicia">
      <SimpleForm>
        <TextInput source="name" label="Nombre" fullWidth />
        <TextInput source="slug" label="Slug" fullWidth helperText="Dejar vacío para autogenerar" />

        {/* Si no tienes el recurso 'users', comenta este bloque */}
        <ReferenceInput source="owner" reference="users" label="Propietario">
          <SelectInput optionText="email" />
        </ReferenceInput>

        <ImageInput
          source="logo"
          label="Logo"
          accept={{ "image/*": [] }}
          multiple={false}
          maxSize={5_000_000}
        >
          <ImageField source="src" title="title" />
        </ImageInput>

        <TextInput source="primary_color" label="Color Primario" type="color" />
        <TextInput source="secondary_color" label="Color Secundario" type="color" />
        <BooleanInput source="is_active" label="Activo" defaultValue />
      </SimpleForm>
    </Create>
  );
}
