// src/resources/activities/SubcategoryQuickCreate.tsx
import * as React from "react";
import {
  useCreate,
  useNotify,
  useCreateSuggestionContext,
} from "react-admin";
import {
  Dialog, DialogTitle, DialogContent, DialogActions,
  Button, TextField, Alert,
} from "@mui/material";

export default function SubcategoryQuickCreate() {
  const { onCancel, onCreate, filter } = useCreateSuggestionContext();
  const [name, setName] = React.useState("");
  const [create, { isLoading }] = useCreate();
  const notify = useNotify();

  const categoryId =
    (filter && (filter as any).category) ??
    (filter && (filter as any).category_id) ??
    null;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!name.trim() || !categoryId) return;

    try {
      const result = await create(
        "subcategories",
        { data: { name: name.trim(), category: categoryId, is_active: true } },
        { returnPromise: true }
      );

      const record = (result as any)?.data;
      if (!record) throw new Error("No se devolvió la subcategoría creada");

      notify("Subcategoría creada", { type: "success" });
      onCreate(record);
    } catch (error: any) {
      const msg =
        error?.body?.detail ||
        error?.body?.message ||
        error?.message ||
        "Error al crear subcategoría";
      notify(msg, { type: "warning" });
    }
  };

  return (
    <Dialog open onClose={onCancel}>
      <DialogTitle>Nueva subcategoría</DialogTitle>
      <form onSubmit={handleSubmit}>
        <DialogContent>
          {!categoryId && (
            <Alert severity="info">Selecciona primero una categoría.</Alert>
          )}
          <TextField
            autoFocus
            margin="dense"
            label="Nombre"
            fullWidth
            value={name}
            onChange={(e) => setName(e.target.value)}
            disabled={!categoryId || isLoading}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={onCancel}>Cancelar</Button>
          <Button type="submit" variant="contained" disabled={!categoryId || isLoading}>
            Crear
          </Button>
        </DialogActions>
      </form>
    </Dialog>
  );
}

