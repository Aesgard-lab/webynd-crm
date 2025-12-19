// frontend/src/resources/marketing/templates/Create.jsx
import * as React from "react";
import {
  Create,
  SimpleForm,
  TextInput,
  ReferenceInput,
  SelectInput,
  BooleanInput,
  useNotify,
  useDataProvider,
  useRedirect,
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

function defaultBlocksJson() {
  return JSON.stringify(
    [
      { type: "heading", content: "Hola {{client.first_name}}" },
      { type: "text", content: "Te escribimos desde {{gym.name}}." },
      { type: "button", label: "Reservar", url: "https://webynd.app" },
      { type: "divider" },
      { type: "text", content: "— Equipo {{gym.name}}" },
    ],
    null,
    2
  );
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

export default function MarketingTemplateCreate(props) {
  const notify = useNotify();
  const dataProvider = useDataProvider();
  const redirect = useRedirect();

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
      // Backend: endpoint preview (ya lo tienes)
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

  // Transform: blocks_json -> blocks (array) para tu serializer/model
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

  return (
    <>
      <Create
        {...props}
        transform={transform}
        mutationOptions={{
          onSuccess: () => {
            notify("Plantilla creada", { type: "info" });
            redirect("list", "marketing/templates");
          },
          onError: (e) => notify(e?.message || "Error creando plantilla", { type: "error" }),
        }}
      >
        <SimpleForm
          validate={validate}
          defaultValues={{
            channel: "email",
            is_active: true,
            subject: "Asunto",
            blocks_json: defaultBlocksJson(),
          }}
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

          {/* Editor DnD: escribe sobre blocks_json */}
          <BlocksEditor source="blocks_json" />

          <BooleanInput source="is_active" label="Activa" />
        </SimpleForm>
      </Create>

      <PreviewDialog
        open={previewOpen}
        onClose={() => setPreviewOpen(false)}
        html={previewHtml}
        text={previewText}
      />
    </>
  );
}
