// src/resources/activities/Form.jsx
import * as React from "react";
import {
  TextInput,
  BooleanInput,
  ReferenceInput,
  AutocompleteInput,
  ImageInput,
  ImageField,
  required,
  FormDataConsumer,
} from "react-admin";
import CategoryQuickCreate from "./CategoryQuickCreate";
import SubcategoryQuickCreate from "./SubcategoryQuickCreate";

export default function ActivityForm() {
  return (
    <>
      {/* Nombre */}
      <TextInput
        source="name"
        label="Nombre"
        validate={required()}
        fullWidth
      />

      {/* Categoría con QuickCreate */}
      <ReferenceInput
        source="category_id"
        reference="categories"
        label="Categoría"
      >
        <AutocompleteInput
          optionText="name"
          fullWidth
          create={<CategoryQuickCreate />}
          // Texto de búsqueda -> filtro para tu API
          filterToQuery={(searchText) => ({ name__icontains: searchText })}
        />
      </ReferenceInput>

      {/* Subcategoría dependiente de la categoría seleccionada */}
      <FormDataConsumer>
        {({ formData }) => (
          <ReferenceInput
            source="subcategory_id"
            reference="subcategories"
            label="Subcategoría"
            // Se recalcula con el formData sin necesidad de useWatch
            filter={formData?.category_id ? { category: formData.category_id } : {}}
          >
            <AutocompleteInput
              optionText="name"
              fullWidth
              create={<SubcategoryQuickCreate />}
              filterToQuery={(searchText) => ({ name__icontains: searchText })}
            />
          </ReferenceInput>
        )}
      </FormDataConsumer>

      {/* Activa / Inactiva */}
      <BooleanInput source="is_active" label="Activo" />

      {/* Imagen (accept debe ser objeto con react-dropzone v14+) */}
      <ImageInput
        source="image"
        label="Imagen"
        accept={{ "image/*": [] }}
      >
        <ImageField source="src" title="title" />
      </ImageInput>
    </>
  );
}
