import { Edit, SimpleForm, TextInput, SelectInput, BooleanInput } from "react-admin";

export default function CatalogCategoryEdit() {
  return (
    <Edit>
      <SimpleForm>
        <TextInput source="name" label="Nombre" fullWidth />

        <SelectInput
          source="module"
          label="Módulo"
          choices={[
            { id: "bonus", name: "Bonos" },
            { id: "subscription", name: "Suscripciones" },
            { id: "service", name: "Servicios" },
            { id: "product", name: "Productos" },
            { id: "activity", name: "Actividades" },
          ]}
          fullWidth
        />

        <SelectInput
          source="scope"
          label="Scope"
          choices={[
            { id: "gym", name: "Gym" },
            { id: "franchise", name: "Franchise" },
          ]}
          fullWidth
        />

        <BooleanInput source="is_active" label="Activo" />
      </SimpleForm>
    </Edit>
  );
}
