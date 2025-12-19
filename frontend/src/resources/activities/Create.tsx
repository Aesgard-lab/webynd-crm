// src/resources/activities/Create.tsx
import * as React from "react";
import { Create, useNotify } from "react-admin";
import ActivityForm from "./Form";

type AnyObj = Record<string, any>;

const cleanPayload = (data: AnyObj): AnyObj => {
  const out: AnyObj = { ...data };

  // Campos de solo lectura que no deben viajar
  delete out.gym;
  delete out.created_at;
  delete out.updated_at;

  const toNullIfEmpty = (v: any) =>
    v === "" || v === undefined ? null : v;

  // Coerción numérica (evita strings vacíos)
  const intFields = [
    "duration_minutes",
    "capacity",
    "booking_opening_minutes_before",
    "booking_opening_days_ahead",
    "booking_cutoff_minutes_before",
    "cancellation_limit_minutes",
    "waitlist_capacity",
    "waitlist_promote_window_minutes",
    "max_bookings_per_user_per_day",
  ];
  intFields.forEach((k) => {
    if (k in out) {
      const v = out[k];
      out[k] =
        v === "" || v === undefined || v === null ? null : Number(v);
    }
  });

  if ("drop_in_price" in out) {
    const v = out.drop_in_price;
    out.drop_in_price =
      v === "" || v === undefined || v === null ? null : Number(v);
  }

  // TimeInput => "HH:MM" (si vacío -> null)
  out.booking_opening_time = toNullIfEmpty(out.booking_opening_time);

  // Subcategoría opcional
  out.subcategory_id = toNullIfEmpty(out.subcategory_id);

  // Color opcional
  out.color_hex = out.color_hex || "";

  // Normalizar tags (ArrayInput simple)
  if (Array.isArray(out.tags)) {
    out.tags = out.tags
      .map((t: any) =>
        typeof t === "string" ? t : t?.value ?? t?.[0] ?? ""
      )
      .filter(Boolean);
  }

  return out;
};

export default function ActivityCreate() {
  const notify = useNotify();

  return (
    <Create
      title="Crear actividad"
      mutationMode="pessimistic"
      redirect="edit"
      transform={cleanPayload}
      mutationOptions={{
        onSuccess: () => {
          notify("Actividad creada", { type: "success" });
        },
        onError: (error: any) => {
          const msg =
            error?.body?.detail ||
            error?.message ||
            "Error al crear la actividad";
          notify(msg, { type: "warning" });
        },
      }}
    >
      <ActivityForm />
    </Create>
  );
}
