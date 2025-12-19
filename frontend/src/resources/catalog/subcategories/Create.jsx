import { Create, SimpleForm, TextInput, ReferenceInput, SelectInput } from "react-admin";

export default function CatalogSubcategoryCreate() {
  return (
    <Create>
      <SimpleForm>
        <TextInput source="name" label="Nombre" fullWidth />

        <ReferenceInput source="category" reference="catalog-categories" label="Categoría">
          <SelectInput optionText="name" fullWidth />
        </ReferenceInput>
      </SimpleForm>
    </Create>
  );
}
