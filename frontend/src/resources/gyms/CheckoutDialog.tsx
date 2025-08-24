// frontend/src/resources/gyms/CheckoutDialog.tsx
import * as React from 'react';
import {
  Dialog, DialogTitle, DialogContent, DialogActions,
  Button, Box, FormGroup, FormControlLabel, Checkbox, CircularProgress,
} from '@mui/material';
import { useGetList, useNotify } from 'react-admin';
import { createCheckoutSession } from '../../stripe/api';

type Props = {
  open: boolean;
  onClose: () => void;
  gymId: number;
};

export default function CheckoutDialog({ open, onClose, gymId }: Props) {
  const notify = useNotify();
  const { data, isLoading } = useGetList('saas/prices', {
    pagination: { page: 1, perPage: 100 },
    sort: { field: 'id', order: 'ASC' },
    filter: {},
  });

  const [selected, setSelected] = React.useState<number[]>([]);
  React.useEffect(() => {
    if (!open) setSelected([]);
  }, [open]);

  const toggle = (id: number) =>
    setSelected((prev) =>
      prev.includes(id) ? prev.filter((x) => x !== id) : [...prev, id]
    );

  const onConfirm = async () => {
    if (selected.length === 0) {
      notify('Selecciona al menos un precio', { type: 'warning' });
      return;
    }
    try {
      const resp = await createCheckoutSession(gymId, selected);
      const url = resp.url || resp.checkout_url;
      if (!url) throw new Error('Respuesta sin URL de checkout');
      window.location.href = url; // redirige al Checkout
    } catch (e: any) {
      notify(e.message || 'Error creando checkout', { type: 'error' });
    }
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
      <DialogTitle>Crear Checkout</DialogTitle>
      <DialogContent dividers>
        {isLoading ? (
          <Box display="flex" justifyContent="center" py={4}>
            <CircularProgress />
          </Box>
        ) : (
          <FormGroup>
            {(data || []).map((p: any) => (
              <FormControlLabel
                key={p.id}
                control={
                  <Checkbox
                    checked={selected.includes(p.id)}
                    onChange={() => toggle(p.id)}
                  />
                }
                // Muestra info útil (ajusta campos si tus Prices tienen otros)
                label={`${p.id} · ${p.module ?? ''} · ${p.nickname ?? p.cycle ?? ''} · ${p.currency?.toUpperCase() ?? ''} ${p.unit_amount != null ? (p.unit_amount / 100).toFixed(2) : ''}`}

              />
            ))}
          </FormGroup>
        )}
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>Cancelar</Button>
        <Button variant="contained" onClick={onConfirm}>
          Ir a Checkout
        </Button>
      </DialogActions>
    </Dialog>
  );
}
