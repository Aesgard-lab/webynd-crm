import { List, Datagrid, TextField, ReferenceField, EditButton, SearchInput } from "react-admin";

const filters = [<SearchInput source="search" alwaysOn key="search" />];

export default function CatalogSubcategoryList(props) {
  return (
    <List {...props} filters={filters} perPage={25} sort={{ field: "id", order: "DESC" }}>
      <Datagrid rowClick="edit">
        <TextField source="id" />
        <TextField source="name" />
        <ReferenceField source="category" reference="catalog-categories" link={false}>
          <TextField source="name" />
        </ReferenceField>
        <EditButton />
      </Datagrid>
    </List>
  );
}
