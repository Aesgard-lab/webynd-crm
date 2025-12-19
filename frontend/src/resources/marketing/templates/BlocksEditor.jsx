// frontend/src/resources/marketing/templates/BlocksEditor.jsx
import * as React from "react";
import { useInput, useNotify } from "react-admin";
import {
  Box,
  Paper,
  Stack,
  Typography,
  Divider,
  TextField,
  Button,
  IconButton,
  MenuItem,
} from "@mui/material";

import DeleteIcon from "@mui/icons-material/Delete";
import ContentCopyIcon from "@mui/icons-material/ContentCopy";
import AddIcon from "@mui/icons-material/Add";

import {
  DndContext,
  DragOverlay,
  PointerSensor,
  useSensor,
  useSensors,
  closestCenter,
} from "@dnd-kit/core";
import {
  SortableContext,
  verticalListSortingStrategy,
  useSortable,
  arrayMove,
} from "@dnd-kit/sortable";
import { CSS } from "@dnd-kit/utilities";

const PALETTE = [
  { type: "heading", label: "Heading" },
  { type: "text", label: "Text" },
  { type: "button", label: "Button" },
  { type: "image", label: "Image" },
  { type: "divider", label: "Divider" },
];

function uid() {
  return Math.random().toString(16).slice(2) + Date.now().toString(16);
}

function safeParseArray(jsonStr) {
  try {
    const v = JSON.parse(jsonStr || "[]");
    return { ok: Array.isArray(v), value: Array.isArray(v) ? v : [], error: Array.isArray(v) ? null : "No es un array" };
  } catch (e) {
    return { ok: false, value: [], error: e?.message || "JSON inválido" };
  }
}

function fromStored(b) {
  return { _id: uid(), ...(b || {}) };
}

function toStored(b) {
  const { _id, ...rest } = b || {};
  return rest;
}

function makeBlock(type) {
  switch (type) {
    case "heading":
      return { _id: uid(), type: "heading", content: "Título" };
    case "text":
      return { _id: uid(), type: "text", content: "Texto..." };
    case "button":
      return { _id: uid(), type: "button", label: "Reservar", url: "https://webynd.app" };
    case "image":
      return { _id: uid(), type: "image", url: "https://via.placeholder.com/700x260", alt: "Imagen" };
    case "divider":
    default:
      return { _id: uid(), type: "divider" };
  }
}

function blockTitle(b) {
  if (!b) return "";
  if (b.type === "heading") return `Heading: ${String(b.content || "").slice(0, 30)}`;
  if (b.type === "text") return `Text: ${String(b.content || "").slice(0, 30)}`;
  if (b.type === "button") return `Button: ${String(b.label || "").slice(0, 30)}`;
  if (b.type === "image") return `Image: ${String(b.alt || b.url || "").slice(0, 30)}`;
  return "Divider";
}

function SortableCard({ block, selected, onSelect, onDelete, onDuplicate }) {
  const { attributes, listeners, setNodeRef, transform, transition, isDragging } = useSortable({
    id: block._id,
  });

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
    opacity: isDragging ? 0.4 : 1,
  };

  return (
    <Paper
      ref={setNodeRef}
      variant="outlined"
      style={style}
      onClick={() => onSelect(block._id)}
      {...attributes}
      {...listeners}
      sx={{
        p: 1.25,
        borderRadius: 2,
        borderColor: selected ? "primary.main" : "divider",
        boxShadow: selected ? 2 : 0,
        cursor: "grab",
        userSelect: "none",
      }}
    >
      <Stack direction="row" alignItems="center" justifyContent="space-between" spacing={1}>
        <Box>
          <Typography variant="subtitle2">{blockTitle(block)}</Typography>
          <Typography variant="caption" sx={{ opacity: 0.7 }}>
            {block.type}
          </Typography>
        </Box>

        <Stack direction="row" spacing={0.5}>
          <IconButton size="small" onClick={(e) => (e.stopPropagation(), onDuplicate(block._id))}>
            <ContentCopyIcon fontSize="inherit" />
          </IconButton>
          <IconButton size="small" onClick={(e) => (e.stopPropagation(), onDelete(block._id))}>
            <DeleteIcon fontSize="inherit" />
          </IconButton>
        </Stack>
      </Stack>
    </Paper>
  );
}

function EditorPanel({ block, onChange }) {
  if (!block) {
    return (
      <Paper variant="outlined" sx={{ p: 2, borderRadius: 2 }}>
        <Typography variant="subtitle1">Editar bloque</Typography>
        <Typography variant="body2" sx={{ opacity: 0.7 }}>
          Selecciona un bloque del canvas.
        </Typography>
      </Paper>
    );
  }

  const set = (patch) => onChange({ ...block, ...patch });

  return (
    <Paper variant="outlined" sx={{ p: 2, borderRadius: 2 }}>
      <Stack spacing={1.5}>
        <Typography variant="subtitle1">Editar bloque</Typography>

        <TextField
          select
          size="small"
          label="Tipo"
          value={block.type || "divider"}
          onChange={(e) => {
            const next = makeBlock(e.target.value);
            next._id = block._id; // mantener id interno
            set(next);
          }}
          fullWidth
        >
          <MenuItem value="heading">Heading</MenuItem>
          <MenuItem value="text">Text</MenuItem>
          <MenuItem value="button">Button</MenuItem>
          <MenuItem value="image">Image</MenuItem>
          <MenuItem value="divider">Divider</MenuItem>
        </TextField>

        {block.type === "heading" && (
          <TextField
            label="Texto"
            value={block.content || ""}
            onChange={(e) => set({ content: e.target.value })}
            fullWidth
          />
        )}

        {block.type === "text" && (
          <TextField
            label="Texto"
            value={block.content || ""}
            onChange={(e) => set({ content: e.target.value })}
            fullWidth
            multiline
            minRows={6}
          />
        )}

        {block.type === "button" && (
          <>
            <TextField
              label="Label"
              value={block.label || ""}
              onChange={(e) => set({ label: e.target.value })}
              fullWidth
            />
            <TextField
              label="URL"
              value={block.url || ""}
              onChange={(e) => set({ url: e.target.value })}
              fullWidth
            />
          </>
        )}

        {block.type === "image" && (
          <>
            <TextField
              label="URL imagen"
              value={block.url || ""}
              onChange={(e) => set({ url: e.target.value })}
              fullWidth
            />
            <TextField
              label="Alt"
              value={block.alt || ""}
              onChange={(e) => set({ alt: e.target.value })}
              fullWidth
            />
          </>
        )}

        {block.type === "divider" && (
          <Typography variant="body2" sx={{ opacity: 0.7 }}>
            Divider no tiene campos.
          </Typography>
        )}

        <Divider />
        <Typography variant="caption" sx={{ opacity: 0.7 }}>
          Variables: {"{{client.first_name}}"} · {"{{gym.name}}"}
        </Typography>
      </Stack>
    </Paper>
  );
}

/**
 * Componente RA “input”:
 * - se engancha a blocks_json (string JSON)
 * - mantiene estado interno blocks[]
 * - persiste al form como JSON string (sin _id)
 */
export default function BlocksEditor(props) {
  const notify = useNotify();
  const { field } = useInput({ ...props, source: props.source || "blocks_json" });

  const sensors = useSensors(useSensor(PointerSensor, { activationConstraint: { distance: 6 } }));

  const [blocks, setBlocks] = React.useState([]);
  const [selectedId, setSelectedId] = React.useState(null);
  const [activeId, setActiveId] = React.useState(null);
  const [activePaletteType, setActivePaletteType] = React.useState(null);

  // Init from field.value (solo una vez)
  React.useEffect(() => {
    const parsed = safeParseArray(field.value);
    if (!parsed.ok && field.value) {
      notify(`blocks_json inválido: ${parsed.error}`, { type: "warning" });
    }
    const initial = parsed.value.map(fromStored);
    setBlocks(initial);
    setSelectedId(initial[0]?._id || null);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // Persist to form
  React.useEffect(() => {
    const clean = blocks.map(toStored);
    field.onChange(JSON.stringify(clean, null, 2));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [blocks]);

  const selected = blocks.find((b) => b._id === selectedId) || null;

  const addBlock = (type) => {
    const b = makeBlock(type);
    setBlocks((prev) => [...prev, b]);
    setSelectedId(b._id);
  };

  const deleteBlock = (id) => {
    setBlocks((prev) => prev.filter((b) => b._id !== id));
    setSelectedId((cur) => (cur === id ? null : cur));
  };

  const duplicateBlock = (id) => {
    setBlocks((prev) => {
      const idx = prev.findIndex((b) => b._id === id);
      if (idx === -1) return prev;
      const copy = { ...prev[idx], _id: uid() };
      const next = [...prev];
      next.splice(idx + 1, 0, copy);
      return next;
    });
  };

  const updateSelected = (nextBlock) => {
    setBlocks((prev) => prev.map((b) => (b._id === nextBlock._id ? nextBlock : b)));
  };

  const onDragStart = (event) => {
    const id = event.active.id;
    setActiveId(id);

    if (typeof id === "string" && id.startsWith("palette:")) {
      setActivePaletteType(id.split(":")[1] || null);
    } else {
      setActivePaletteType(null);
    }
  };

  const onDragEnd = (event) => {
    const { active, over } = event;
    setActiveId(null);

    if (!over) {
      setActivePaletteType(null);
      return;
    }

    const aId = active.id;
    const oId = over.id;

    // Paleta -> insertar
    if (typeof aId === "string" && aId.startsWith("palette:")) {
      const type = aId.split(":")[1];
      const newBlock = makeBlock(type);

      setBlocks((prev) => {
        const overIdx = prev.findIndex((b) => b._id === oId);
        if (overIdx === -1) return [...prev, newBlock];
        const next = [...prev];
        next.splice(overIdx, 0, newBlock);
        return next;
      });

      setSelectedId(newBlock._id);
      setActivePaletteType(null);
      return;
    }

    // Reordenar
    if (aId !== oId) {
      setBlocks((prev) => {
        const oldIndex = prev.findIndex((b) => b._id === aId);
        const newIndex = prev.findIndex((b) => b._id === oId);
        if (oldIndex === -1 || newIndex === -1) return prev;
        return arrayMove(prev, oldIndex, newIndex);
      });
    }

    setActivePaletteType(null);
  };

  const onDragCancel = () => {
    setActiveId(null);
    setActivePaletteType(null);
  };

  return (
    <Paper variant="outlined" sx={{ p: 2, borderRadius: 2 }}>
      <Stack spacing={1}>
        <Typography variant="h6">Editor de bloques (columna)</Typography>
        <Typography variant="caption" sx={{ opacity: 0.7 }}>
          Arrastra y suelta para insertar/reordenar. Se guarda en <code>blocks_json</code>.
        </Typography>
      </Stack>

      <Divider sx={{ my: 2 }} />

      <DndContext
        sensors={sensors}
        collisionDetection={closestCenter}
        onDragStart={onDragStart}
        onDragEnd={onDragEnd}
        onDragCancel={onDragCancel}
      >
        <Box
          sx={{
            display: "grid",
            gridTemplateColumns: { xs: "1fr", md: "260px 1fr 320px" },
            gap: 2,
            alignItems: "start",
          }}
        >
          {/* Palette */}
          <Stack spacing={1}>
            <Typography variant="subtitle2" sx={{ opacity: 0.8 }}>
              Componentes
            </Typography>

            {PALETTE.map((p) => (
              <Paper
                key={p.type}
                id={`palette:${p.type}`}
                variant="outlined"
                sx={{
                  p: 1.25,
                  borderRadius: 2,
                  cursor: "grab",
                  userSelect: "none",
                  "&:active": { cursor: "grabbing" },
                }}
              >
                <Stack direction="row" alignItems="center" justifyContent="space-between">
                  <Box>
                    <Typography variant="subtitle2">{p.label}</Typography>
                    <Typography variant="caption" sx={{ opacity: 0.7 }}>
                      Arrastra al canvas
                    </Typography>
                  </Box>
                  <Button size="small" variant="text" onClick={() => addBlock(p.type)} startIcon={<AddIcon />}>
                    Añadir
                  </Button>
                </Stack>
              </Paper>
            ))}
          </Stack>

          {/* Canvas */}
          <Paper variant="outlined" sx={{ p: 2, borderRadius: 2, minHeight: 420, background: "#fafafa" }}>
            <Typography variant="subtitle2" sx={{ opacity: 0.8, mb: 1 }}>
              Canvas
            </Typography>

            {blocks.length === 0 ? (
              <Box
                sx={{
                  border: "2px dashed #d1d5db",
                  borderRadius: 2,
                  p: 3,
                  textAlign: "center",
                  color: "text.secondary",
                }}
              >
                Arrastra un bloque desde la izquierda…
              </Box>
            ) : (
              <SortableContext items={blocks.map((b) => b._id)} strategy={verticalListSortingStrategy}>
                <Stack spacing={1}>
                  {blocks.map((b) => (
                    <SortableCard
                      key={b._id}
                      block={b}
                      selected={b._id === selectedId}
                      onSelect={setSelectedId}
                      onDelete={deleteBlock}
                      onDuplicate={duplicateBlock}
                    />
                  ))}
                </Stack>
              </SortableContext>
            )}
          </Paper>

          {/* Editor */}
          <EditorPanel block={selected} onChange={updateSelected} />
        </Box>

        <DragOverlay>
          {activePaletteType ? (
            <Paper variant="outlined" sx={{ p: 1.25, borderRadius: 2 }}>
              <Typography variant="subtitle2">{activePaletteType}</Typography>
              <Typography variant="caption" sx={{ opacity: 0.7 }}>
                Insertar bloque
              </Typography>
            </Paper>
          ) : null}
        </DragOverlay>
      </DndContext>

      {/* Campo “real” del formulario (opcional mostrarlo, yo lo oculto) */}
      <Box sx={{ display: "none" }}>
        <TextField value={field.value || ""} onChange={() => {}} />
      </Box>
    </Paper>
  );
}
