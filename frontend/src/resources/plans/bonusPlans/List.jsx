import {
  List,
  Datagrid,
  TextField,
  NumberField,
  BooleanField,
  EditButton,
} from "react-admin";

export default function BonusPlanList(props) {
  return (
    <List {...props}>
      <Datagrid rowClick="edit">
        <TextField source="id" />
        <TextField source="name" label="Nombre" />
        <TextField source="category" label="Categoría" />
        <TextField source="subcategory" label="Subcategoría" />
        <NumberField source="price" label="Precio" />
        <BooleanField source="is_active" label="Activo" />
        <EditButton />
      </Datagrid>
    </List>
  );
}
