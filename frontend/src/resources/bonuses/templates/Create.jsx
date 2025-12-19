import * as React from "react";
import {
  Create,
  SimpleForm,
  TextInput,
  NumberInput,
  BooleanInput,
  SelectInput,
  ReferenceInput,
  AutocompleteInput,
  ArrayInput,
  SimpleFormIterator,
  required,
  FormDataConsumer,
} from "react-admin";

import { getCurrentGymId } from "../../../utils/currentGym";
;

export default function BonusTemplateCreate() {
  const currentGymId = getCurrentGymId();

  return (
    <Create title="Crear plantilla de bono">
      <SimpleForm
        defaultValues={{
          scope: "gym",
          gym: currentGymId || null,
          franchise: null,
          is_active: true,
          available_online: false,
          usage_limit_period: "none",
          usage_limit_value: null,
          is_recurring: false,
          recurrence_period_days: null,
          allow_freeze: false,
          freeze_fee: null,
          allow_transfer: false,
          transfer_fee: null,
          items: [],
        }}
      >
        <TextInput source="name" label="Nombre" validate={required()} fullWidth />
        <TextInput source="description" label="Descripción" multiline fullWidth />

        <SelectInput
          source="scope"
          label="Scope"
          validate={required()}
          choices={[
            { id: "gym", name: "Gym" },
            { id: "franchise", name: "Franchise" },
          ]}
        />

        {/* SOLO un selector según scope */}
        <FormDataConsumer>
          {({ formData }) =>
            formData.scope === "gym" ? (
              <ReferenceInput source="gym" reference="gyms" label="Gym">
                <AutocompleteInput optionText="name" validate={required()} />
              </ReferenceInput>
            ) : (
              <ReferenceInput source="franchise" reference="franchises" label="Franchise">
                <AutocompleteInput optionText="name" validate={required()} />
              </ReferenceInput>
            )
          }
        </FormDataConsumer>

        <NumberInput source="duration_days" label="Duración (días)" validate={required()} />

        <SelectInput
          source="usage_limit_period"
          label="Restricción de uso (bono completo)"
          choices={[
            { id: "none", name: "Sin límite" },
            { id: "day", name: "Por día" },
            { id: "week", name: "Por semana" },
            { id: "month", name: "Por mes" },
          ]}
        />

        <FormDataConsumer>
          {({ formData }) =>
            formData.usage_limit_period && formData.usage_limit_period !== "none" ? (
              <NumberInput
                source="usage_limit_value"
                label="Valor del límite"
                validate={required()}
              />
            ) : null
          }
        </FormDataConsumer>

        <BooleanInput source="is_recurring" label="Recurrente" />
        <FormDataConsumer>
          {({ formData }) =>
            formData.is_recurring ? (
              <NumberInput
                source="recurrence_period_days"
                label="Periodo recurrente (días, ej 30)"
                validate={required()}
              />
            ) : null
          }
        </FormDataConsumer>

        <BooleanInput source="allow_freeze" label="Permite congelar" />
        <FormDataConsumer>
          {({ formData }) =>
            formData.allow_freeze ? (
              <NumberInput source="freeze_fee" label="Precio congelación (€)" />
            ) : null
          }
        </FormDataConsumer>

        <BooleanInput source="allow_transfer" label="Permite transferir" />
        <FormDataConsumer>
          {({ formData }) =>
            formData.allow_transfer ? (
              <NumberInput source="transfer_fee" label="Precio transferencia (€)" />
            ) : null
          }
        </FormDataConsumer>

        <BooleanInput source="available_online" label="Disponible online" />
        <BooleanInput source="is_active" label="Activa" />

        <ArrayInput source="items" label="Items (actividades/servicios)" validate={required()}>
          <SimpleFormIterator inline>
            <SelectInput
              source="item_type"
              label="Tipo"
              choices={[
                { id: "activity", name: "Actividad" },
                { id: "service", name: "Servicio" },
              ]}
              validate={required()}
            />

            <FormDataConsumer>
              {({ scopedFormData }) =>
                scopedFormData?.item_type === "activity" ? (
                  <ReferenceInput source="activity" reference="activities" label="Actividad">
                    <AutocompleteInput optionText="name" validate={required()} />
                  </ReferenceInput>
                ) : (
                  <ReferenceInput source="service" reference="services" label="Servicio">
                    <AutocompleteInput optionText="name" validate={required()} />
                  </ReferenceInput>
                )
              }
            </FormDataConsumer>

            <NumberInput source="total_uses" label="Usos" validate={required()} />
          </SimpleFormIterator>
        </ArrayInput>
      </SimpleForm>
    </Create>
  );
}
