import * as React from "react";
import {
  Edit,
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

export default function ServiceEdit() {
  return (
    <Edit>
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

        <NumberInput source="duration_minutes" label="Duración (min)" />
        <NumberInput source="price" label="Precio base" />
        <NumberInput source="iva_percent" label="IVA (%)" />
        <BooleanInput source="iva_included" label="Precio con IVA" />

        <FinalPricePreview />

        <ImageInput source="image" label="Imagen" accept="image/*">
          <ImageField source="src" />
        </ImageInput>

        <NumberInput source="max_capacity" label="Capacidad máxima" />
        <BooleanInput source="available_online" label="Disponible online" />
        <BooleanInput source="is_active" label="Activo" />

        {/* ✅ STAFF */}
        <ReferenceArrayInput source="staff" reference="staff" label="Staff asignable">
          <AutocompleteArrayInput optionText="full_name" />
        </ReferenceArrayInput>

        {/* Opcional: mostrar gym/franchise solo lectura si quieres */}
        {/* <TextInput source="gym" disabled /> */}
        {/* <TextInput source="franchise" disabled /> */}
      </SimpleForm>
    </Edit>
  );
}
