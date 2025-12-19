import {
  Edit,
  SimpleForm,
  TextInput,
  SelectInput,
  NumberInput,
  BooleanInput,
} from "react-admin";

const CATEGORY_CHOICES = [
  { id: "mensual", name: "Mensual" },
  { id: "trimestral", name: "Trimestral" },
  { id: "bono", name: "Bono" },
];

const SUBCATEGORY_CHOICES = [
  { id: "reformer", name: "Reformer" },
  { id: "fitness", name: "Fitness" },
  { id: "pilates", name: "Pilates" },
];

export default function BonusPlanEdit(props) {
  return (
    <Edit {...props}>
      <SimpleForm>
        <TextInput source="name" fullWidth />
        <SelectInput source="category" choices={CATEGORY_CHOICES} fullWidth />
        <SelectInput source="subcategory" choices={SUBCATEGORY_CHOICES} fullWidth />

        <NumberInput source="price" />
        <NumberInput source="signup_fee" />

        <BooleanInput source="is_active" />
        <BooleanInput source="can_be_purchased_online" />
        <BooleanInput source="is_shared_with_gyms" />
      </SimpleForm>
    </Edit>
  );
}
