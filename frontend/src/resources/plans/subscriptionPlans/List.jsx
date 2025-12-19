import {
  List,
  Datagrid,
  TextField,
  NumberField,
  BooleanField,
} from "react-admin";

import { getCurrentGymId } from "../../../utils/currentGym";

export default function SubscriptionPlanList(props) {
  const gymId = getCurrentGymId?.() || null;

  return (
    <List
      {...props}
      filter={gymId ? { gym: gymId } : {}}
      sort={{ field: "name", order: "ASC" }}
    >
      <Datagrid>
        <TextField source="id" />
        <TextField source="name" label="Nombre" />
        <TextField source="category" label="Categoría" />
        <TextField source="subcategory" label="Subcategoría" />
        <NumberField source="price" label="Precio" />
        <BooleanField source="is_active" label="Activo" />
        <BooleanField source="is_shared_with_gyms" label="Compartido" />
      </Datagrid>
    </List>
  );
}
