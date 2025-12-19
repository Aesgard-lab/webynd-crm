// frontend/src/resources/clients/ClientList.jsx
import * as React from 'react';
import {
  List,
  Datagrid,
  TextField,
  BooleanField,
  FunctionField,
  TopToolbar,
  CreateButton,
  ExportButton,
  useListContext,
} from 'react-admin';
import { FilterLiveSearch } from 'ra-ui-materialui';
import { Box } from '@mui/material';
import { getAlertLabelAndColor } from './helpers';

const ClientListActions = () => {
  const { total } = useListContext();
  return (
    <TopToolbar>
      <Box sx={{ flex: 1, mr: 2 }}>
        <FilterLiveSearch source="q" />
      </Box>
      <CreateButton />
      <ExportButton disabled={!total} />
    </TopToolbar>
  );
};

export const ClientList = (props) => {
  const currentGymId = localStorage.getItem('currentGymId') || 'none';

  return (
    <List
      key={`clients-${currentGymId}`}
      {...props}
      actions={<ClientListActions />}
      sort={{ field: 'id', order: 'DESC' }}
      perPage={10}
    >
      <Datagrid rowClick="edit">
        <TextField source="first_name" label="Nombre" />
        <TextField source="last_name" label="Apellidos" />
        <TextField source="email" label="Email" />
        <BooleanField source="is_active" label="Activo" />
        <FunctionField
          source="alert_level"
          label="Alerta"
          render={(record) => {
            const { label, className } = getAlertLabelAndColor(record.alert_level);
            return (
              <span
                className={`inline-flex items-center rounded-full px-2 py-0.5 text-xs font-medium ${className}`}
              >
                {label}
              </span>
            );
          }}
        />
      </Datagrid>
    </List>
  );
};
