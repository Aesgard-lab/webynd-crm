import { List, Datagrid, TextField, EditButton, SearchInput } from "react-admin";

const filters = [<SearchInput source="search" alwaysOn key="search" />];

export default function CatalogCategoryList(props) {
  return (
    <List {...props} filters={filters} perPage={25} sort={{ field: "id", order: "DESC" }}>
      <Datagrid rowClick="edit">
        <TextField source="id" />
        <TextField source="name" />
        <TextField source="module" />
        <TextField source="scope" />
        <EditButton />
      </Datagrid>
    </List>
  );
}
