import {
  List,
  Datagrid,
  TextField,
  DateField,
  BooleanField,
  ReferenceField,
  EditButton,
} from "react-admin";

export default function ListView(props) {
  return (
    <List {...props} sort={{ field: "updated_at", order: "DESC" }}>
      <Datagrid rowClick="edit">
        <TextField source="id" />
        <TextField source="name" label="Nombre" />
        <TextField source="channel" label="Canal" />
        <TextField source="subject" label="Asunto" />
        <ReferenceField source="gym" reference="gyms" link={false}>
          <TextField source="name" />
        </ReferenceField>
        <BooleanField source="is_active" label="Activa" />
        <DateField source="updated_at" showTime label="Actualizada" />
        <EditButton />
      </Datagrid>
    </List>
  );
}
