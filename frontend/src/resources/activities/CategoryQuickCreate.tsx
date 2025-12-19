// src/resources/activities/CategoryQuickCreate.tsx
import * as React from "react";
import { useCreate, useNotify, useCreateSuggestionContext } from "react-admin";
import { Dialog, DialogTitle, DialogContent, DialogActions, Button, TextField } from "@mui/material";

export default function CategoryQuickCreate() {
  const { onCancel, onCreate } = useCreateSuggestionContext();
  const [name, setName] = React.useState("");
  const [create, { isLoading }] = useCreate();
  const notify = useNotify();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!name.trim()) return;

    try {
      const gymId = Number(localStorage.getItem("currentGymId")) || null;

      const result = await create(
        // ⚠️ ruta correcta en tu API
        "categories",
        { data: { name: name.trim(), is_active: true, gym: gymId } },
        { returnPromise: true }
      );

      const record = result?.data;
      if (!record) throw new Error("No se devolvió la categoría creada");

      notify("Categoría creada", { type: "success" });
      onCreate(record);
    } catch (error: any) {
      const msg =
        error?.body?.detail ||
        error?.body?.message ||
        error?.message ||
        "Error al crear categoría";
      notify(msg, { type: "warning" });
    }
  };

  return (
    <Dialog open onClose={onCancel}>
      <DialogTitle>Nueva categoría</DialogTitle>
      <form onSubmit={handleSubmit}>
        <DialogContent>
          <TextField
            autoFocus
            margin="dense"
            label="Nombre"
            fullWidth
            value={name}
            onChange={(e) => setName(e.target.value)}
            disabled={isLoading}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={onCancel}>Cancelar</Button>
          <Button type="submit" variant="contained" disabled={isLoading}>
            Crear
          </Button>
        </DialogActions>
      </form>
    </Dialog>
  );
}
