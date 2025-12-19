// frontend/src/resources/marketing/templates/Edit.jsx
import * as React from "react";
import {
  Edit,
  SimpleForm,
  TextInput,
  ReferenceInput,
  SelectInput,
  BooleanInput,
  useNotify,
  useDataProvider,
  required,
  Toolbar,
  SaveButton,
  Button,
} from "react-admin";
import { Dialog, DialogTitle, DialogContent, DialogActions } from "@mui/material";
import { useFormContext } from "react-hook-form";

import BlocksEditor from "./BlocksEditor";

function safeJsonParse(str) {
  try {
    return { ok: true, value: JSON.parse(str || "[]") };
  } catch (e) {
    return { ok: false, error: e?.message || "JSON inválido" };
  }
}

function PreviewDialog({ open, onClose, html, text }) {
  return (
    <Dialog open={open} onClose={onClose} maxWidth="md" fullWidth>
      <DialogTitle>Preview</DialogTitle>
      <DialogContent dividers>
        <div style={{ display: "grid", gridTemplateColumns: "1fr", gap: 16 }}>
          <div>
            <div style={{ fontSize: 12, opacity: 0.7, marginBottom: 8 }}>HTML</div>
            <div
              style={{
                border: "1px solid #e5e7eb",
                borderRadius: 12,
                padding: 12,
                overflow: "auto",
              }}
              dangerouslySetInnerHTML={{ __html: html || "" }}
            />
          </div>
          <div>
            <div style={{ fontSize: 12, opacity: 0.7, marginBottom: 8 }}>Texto plano</div>
            <pre
              style={{
                whiteSpace: "pre-wrap",
                border: "1px solid #e5e7eb",
                borderRadius: 12,
                padding: 12,
                margin: 0,
              }}
            >
              {text || ""}
            </pre>
          </div>
        </div>
      </DialogContent>
      <DialogActions>
        <Button label="Cerrar" onClick={onClose} />
      </DialogActions>
    </Dialog>
  );
}

function TemplateToolbar({ onPreviewClick }) {
  return (
    <Toolbar>
      <SaveButton />
      <Button label="Preview (sin guardar)" onClick={onPreviewClick} />
    </Toolbar>
  );
}

function PreviewToolbarBridge({ onPreview }) {
  const form = useFormContext();
  return <TemplateToolbar onPreviewClick={() => onPreview(form.getValues())} />;
}

export default function MarketingTemplateEdit(props) {
  const notify = useNotify();
  const dataProvider = useDataProvider();

  const [previewOpen, setPreviewOpen] = React.useState(false);
  const [previewHtml, setPreviewHtml] = React.useState("");
  const [previewText, setPreviewText] = React.useState("");

  const handlePreviewFromValues = async (values) => {
    const blocksStr = values?.blocks_json ?? "[]";
    const parsed = safeJsonParse(blocksStr);
    if (!parsed.ok) {
      notify(`Blocks JSON inválido: ${parsed.error}`, { type: "warning" });
      return;
    }

    try {
      const res = await dataProvider.create("marketing/templates/preview", {
        data: { blocks: parsed.value },
      });
      setPreviewHtml(res?.data?.html || "");
      setPreviewText(res?.data?.text || "");
      setPreviewOpen(true);
    } catch (e) {
      notify(e?.message || "Error generando preview", { type: "error" });
    }
  };

  const transform = (data) => {
    const parsed = safeJsonParse(data.blocks_json || "[]");
    if (!parsed.ok) return data;

    const payload = { ...data };
    delete payload.blocks_json;
    payload.blocks = parsed.value;
    return payload;
  };

  const validate = (values) => {
    const errors = {};
    if (!values.gym) errors.gym = "Obligatorio";
    if (!values.name) errors.name = "Obligatorio";

    const parsed = safeJsonParse(values.blocks_json || "[]");
    if (!parsed.ok) errors.blocks_json = `JSON inválido: ${parsed.error}`;
    return errors;
  };

  // Para Edit: blocks_json se construye desde record.blocks
  const defaultValues = (record) => ({
    blocks_json: JSON.stringify(record?.blocks ?? [], null, 2),
  });

  return (
    <>
      <Edit {...props} transform={transform}>
        <SimpleForm
          validate={validate}
          defaultValues={defaultValues}
          toolbar={<PreviewToolbarBridge onPreview={handlePreviewFromValues} />}
        >
          <ReferenceInput source="gym" reference="gyms">
            <SelectInput optionText="name" validate={[required()]} />
          </ReferenceInput>

          <TextInput source="name" label="Nombre" fullWidth validate={[required()]} />

          <SelectInput
            source="channel"
            label="Canal"
            choices={[{ id: "email", name: "Email" }]}
            fullWidth
          />

          <TextInput source="subject" label="Asunto" fullWidth />

          <BlocksEditor source="blocks_json" />

          <BooleanInput source="is_active" label="Activa" />
        </SimpleForm>
      </Edit>

      <PreviewDialog
        open={previewOpen}
        onClose={() => setPreviewOpen(false)}
        html={previewHtml}
        text={previewText}
      />
    </>
  );
}
