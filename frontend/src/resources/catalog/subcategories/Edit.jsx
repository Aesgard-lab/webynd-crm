import { Edit, SimpleForm, TextInput, ReferenceInput, SelectInput } from "react-admin";

export default function CatalogSubcategoryEdit() {
  return (
    <Edit>
      <SimpleForm>
        <TextInput source="name" label="Nombre" fullWidth />

        <ReferenceInput source="category" reference="catalog-categories" label="Categoría">
          <SelectInput optionText="name" fullWidth />
        </ReferenceInput>
      </SimpleForm>
    </Edit>
  );
}
