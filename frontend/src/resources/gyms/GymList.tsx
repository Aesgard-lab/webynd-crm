// frontend/src/resources/gyms/GymList.tsx
import * as React from 'react';
import {
  List, Datagrid, TextField, FunctionField, useNotify,
} from 'react-admin';
import { Button, Stack } from '@mui/material';
import CheckoutDialog from './CheckoutDialog';
import { openBillingPortal } from '../../stripe/api';

export default function GymList() {
  const [dialogGymId, setDialogGymId] = React.useState<number | null>(null);
  const notify = useNotify();

  const onPortal = async (gymId: number) => {
    try {
      const resp = await openBillingPortal(gymId);
      const url = resp.url || resp.portal_url;
      if (!url) throw new Error('Respuesta sin URL de portal');
      window.open(url, '_blank', 'noopener,noreferrer');
    } catch (e: any) {
      notify(e.message || 'Error abriendo portal', { type: 'error' });
    }
  };

  return (
    <>
      <List resource="gyms">
        <Datagrid rowClick="show">
          <TextField source="id" />
          <TextField source="name" />
          <TextField source="franchise_name" label="Franquicia" />
          <FunctionField
            label="Billing"
            render={(record: any) => (
              <Stack direction="row" spacing={1}>
                <Button size="small" variant="outlined" onClick={() => setDialogGymId(record.id)}>
                  Checkout
                </Button>
                <Button size="small" variant="contained" onClick={() => onPortal(record.id)}>
                  Portal
                </Button>
              </Stack>
            )}
          />
        </Datagrid>
      </List>

      {dialogGymId !== null && (
        <CheckoutDialog
          open={dialogGymId !== null}
          gymId={dialogGymId}
          onClose={() => setDialogGymId(null)}
        />
      )}
    </>
  );
}
