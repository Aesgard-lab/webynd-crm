import * as React from "react";
import {
  List,
  Datagrid,
  TextField,
  NumberField,
  BooleanField,
  ImageField,
  ReferenceField,
  EditButton,
  SearchInput,
} from "react-admin";

const filters = [<SearchInput source="search" alwaysOn key="search" />];

export default function ServiceList(props) {
  return (
    <List {...props} filters={filters} perPage={25} sort={{ field: "id", order: "DESC" }}>
      <Datagrid rowClick="edit">
        <TextField source="id" />
        <ImageField source="image" label="Imagen" sx={{ "& img": { height: 40, width: 40, objectFit: "cover", borderRadius: 8 } }} />
        <TextField source="name" label="Nombre" />

        <ReferenceField source="category" reference="service-categories" link={false} emptyText="—">
          <TextField source="name" />
        </ReferenceField>

        <NumberField source="duration_minutes" label="Min" />
        <NumberField source="price" label="Precio" />
        <BooleanField source="iva_included" label="IVA incl." />
        <NumberField source="final_price" label="Final" />

        <BooleanField source="available_online" label="Online" />
        <BooleanField source="is_active" label="Activo" />
        <EditButton />
      </Datagrid>
    </List>
  );
}
