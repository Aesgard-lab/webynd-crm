import * as React from "react";
import {
  Create,
  SimpleForm,
  TextInput,
  NumberInput,
  BooleanInput,
  ReferenceInput,
  SelectInput,
  ReferenceArrayInput,
  AutocompleteArrayInput,
  ImageInput,
  ImageField,
  useGetList,
} from "react-admin";
import { useWatch, useFormContext } from "react-hook-form";

function FinalPricePreview() {
  const { control } = useFormContext();
  const price = useWatch({ control, name: "price" });
  const iva = useWatch({ control, name: "iva_percent" });
  const ivaIncluded = useWatch({ control, name: "iva_included" });

  let finalPrice = "";
  const p = Number(price);
  const t = Number(iva);

  if (!Number.isNaN(p) && !Number.isNaN(t) && price !== undefined && iva !== undefined) {
    finalPrice = ivaIncluded ? p.toFixed(2) : (p * (1 + t / 100)).toFixed(2);
  }

  return (
    <TextInput
      source="final_price_preview"
      label="Precio final (calculado)"
      disabled
      defaultValue={finalPrice}
      value={finalPrice}
      helperText="No se guarda: se calcula con Precio base + IVA."
    />
  );
}

function CatalogSubcategoryInput() {
  const { control } = useFormContext();
  const catalogCategoryId = useWatch({ control, name: "catalog_category" });

  // Filtramos subcategorías por category=<id>
  const filter = catalogCategoryId ? { category: catalogCategoryId } : { category: -1 };

  return (
    <ReferenceInput
      source="catalog_subcategory"
      reference="catalog-subcategories"
      label="Subcategoría"
      filter={filter}
      sort={{ field: "name", order: "ASC" }}
    >
      <SelectInput optionText="name" fullWidth />
    </ReferenceInput>
  );
}

export default function ServiceCreate() {
  return (
    <Create>
      <SimpleForm>
        <TextInput source="name" label="Nombre" fullWidth />
        <TextInput source="description" label="Descripción" multiline fullWidth />

        <ReferenceInput
          source="catalog_category"
          reference="catalog-categories"
          filter={{ module: "service" }}
          label="Categoría"
          sort={{ field: "name", order: "ASC" }}
        >
          <SelectInput optionText="name" fullWidth />
        </ReferenceInput>

        <CatalogSubcategoryInput />

        <NumberInput source="duration_minutes" label="Duración (min)" defaultValue={60} />
        <NumberInput source="price" label="Precio base" />
        <NumberInput source="iva_percent" label="IVA (%)" defaultValue={21} />
        <BooleanInput source="iva_included" label="Precio con IVA" defaultValue />

        <FinalPricePreview />

        <ImageInput source="image" label="Imagen" accept="image/*">
          <ImageField source="src" />
        </ImageInput>

        <NumberInput source="max_capacity" label="Capacidad máxima" defaultValue={1} />
        <BooleanInput source="available_online" label="Disponible online" />
        <BooleanInput source="is_active" label="Activo" defaultValue />

        {/* ✅ STAFF (lo que te faltaba vs admin) */}
        <ReferenceArrayInput source="staff" reference="staff" label="Staff asignable">
          <AutocompleteArrayInput optionText="full_name" />
        </ReferenceArrayInput>
      </SimpleForm>
    </Create>
  );
}
