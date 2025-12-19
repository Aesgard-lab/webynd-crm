import * as React from "react";
import {
  List,
  Datagrid,
  TextField,
  BooleanField,
  EditButton,
  Create,
  Edit,
  SimpleForm,
  TextInput,
  BooleanInput,
  NumberInput,
  ReferenceInput,
  SelectInput,
  useNotify,
  useDataProvider,
  useRecordContext,
  TopToolbar,
  CreateButton,
} from "react-admin";
import { Button } from "@mui/material";

const ListActions = () => (
  <TopToolbar>
    <CreateButton />
  </TopToolbar>
);

function reminderFallbackEmail() {
  return "test@webynd.local";
}

function TestSmtpButton() {
  const record = useRecordContext();
  const notify = useNotify();
  const dataProvider = useDataProvider();

  const handleClick = async () => {
    try {
      const to_email =
        localStorage.getItem("webynd_user_email") || reminderFallbackEmail();

      await dataProvider.create("marketing/smtp/test", {
        data: {
          to_email,
          smtp_settings_id: record?.id,
          subject: "Test SMTP Webynd",
          message: "Email de prueba: SMTP OK.",
        },
      });

      notify("SMTP OK: email enviado", { type: "success" });
    } catch (e) {
      notify(`SMTP ERROR: ${e?.message || e}`, { type: "error" });
    }
  };

  return (
    <Button variant="outlined" size="small" onClick={handleClick}>
      Probar SMTP
    </Button>
  );
}

export const SmtpSettingsList = (props) => (
  <List {...props} actions={<ListActions />}>
    <Datagrid rowClick="edit">
      <TextField source="id" />
      <TextField source="name" />
      <TextField source="host" />
      <TextField source="port" />
      <TextField source="from_email" />
      <BooleanField source="use_tls" />
      <BooleanField source="use_ssl" />
      <BooleanField source="is_active" />
      <TestSmtpButton />
      <EditButton />
    </Datagrid>
  </List>
);

export const SmtpSettingsCreate = (props) => (
  <Create {...props}>
    <SimpleForm>
      <ReferenceInput source="gym" reference="gyms" perPage={200}>
        <SelectInput optionText="name" />
      </ReferenceInput>

      <TextInput source="name" fullWidth defaultValue="SMTP principal" />
      <BooleanInput source="is_active" defaultValue />

      <TextInput source="host" fullWidth />
      <NumberInput source="port" defaultValue={587} />

      <TextInput source="username" fullWidth />
      <TextInput source="password" fullWidth type="password" />

      <BooleanInput source="use_tls" defaultValue />
      <BooleanInput source="use_ssl" />

      <TextInput source="from_email" fullWidth />
      <TextInput source="reply_to" fullWidth />
    </SimpleForm>
  </Create>
);

export const SmtpSettingsEdit = (props) => (
  <Edit {...props}>
    <SimpleForm>
      <ReferenceInput source="gym" reference="gyms" perPage={200}>
        <SelectInput optionText="name" />
      </ReferenceInput>

      <TextInput source="name" fullWidth />
      <BooleanInput source="is_active" />

      <TextInput source="host" fullWidth />
      <NumberInput source="port" />

      <TextInput source="username" fullWidth />
      <TextInput
        source="password"
        fullWidth
        type="password"
        helperText="Déjalo vacío si no quieres cambiarlo"
      />

      <BooleanInput source="use_tls" />
      <BooleanInput source="use_ssl" />

      <TextInput source="from_email" fullWidth />
      <TextInput source="reply_to" fullWidth />
    </SimpleForm>
  </Edit>
);
