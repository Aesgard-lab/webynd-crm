// src/App.tsx
import { Admin, Resource } from "react-admin";
import MyLayout from "./layout/Layout";
import dataProvider from "./dataProvider";
import authProvider from "./authProvider";
import theme from "./theme";

// Dashboard (Back Office Gym)
import Dashboard from "./resources/backoffice/dashboard/BackofficeDashboard";

// Recursos existentes
import { ClientList, ClientEdit, ClientCreate } from "./resources/clients";

// SUPERADMIN · Franchises
import FranchiseList from "./resources/superadmin/franchises/FranchiseList";
import FranchiseCreate from "./resources/superadmin/franchises/FranchiseCreate";
import FranchiseEdit from "./resources/superadmin/franchises/FranchiseEdit";

// SUPERADMIN · Modules
import {
  ModuleList,
  ModuleCreate,
  ModuleEdit,
} from "./resources/superadmin/saas/modules";

// SUPERADMIN · Module Prices
import {
  ModulePriceList,
  ModulePriceCreate,
  ModulePriceEdit,
} from "./resources/superadmin/saas/modulePrices";

import "./App.css";

export default function App() {
  return (
    <Admin
      layout={MyLayout}
      dataProvider={dataProvider}
      authProvider={authProvider}
      dashboard={Dashboard}
      theme={theme}
    >
      {/* Área normal */}
      <Resource
        name="clients"
        list={ClientList}
        edit={ClientEdit}
        create={ClientCreate}
      />

      {/* Necesario para el selector de sede en la AppBar (recurso oculto al no tener list) */}
      <Resource name="gyms" />

      {/* SUPERADMIN · Franchises */}
      <Resource
        name="franchises"
        list={FranchiseList}
        create={FranchiseCreate}
        edit={FranchiseEdit}
        options={{ label: "Superadmin · Franchises" }}
      />

      {/* SUPERADMIN · Modules */}
      <Resource
        name="saas/modules"
        list={ModuleList}
        create={ModuleCreate}
        edit={ModuleEdit}
        options={{ label: "Superadmin · Modules" }}
        recordRepresentation="name"
      />

      {/* SUPERADMIN · Module Prices */}
      <Resource
        name="saas/module-prices"
        list={ModulePriceList}
        create={ModulePriceCreate}
        edit={ModulePriceEdit}
        options={{ label: "Superadmin · Prices" }}
      />
    </Admin>
  );
}
