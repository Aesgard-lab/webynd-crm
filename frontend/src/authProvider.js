// src/api/authProvider.js
 import api from "./api/axios"; // ← instancia con baseURL e interceptor Authorization

const API = import.meta.env.VITE_API_URL; // ej: http://localhost:8000/api

// -------- Utils --------
function normalizeMe(data) {
  const me = {
    id: data.id,
    email: data.email,
    fullName: data.fullName || data.full_name || data.username || data.email,
    avatar: data.avatar || null,
    role: data.role || "client",
    memberships: Array.isArray(data.memberships) ? data.memberships : [],
    currentGym: data.currentGym || null,
  };

  const currentGymId = me.currentGym?.id ?? null;
  const activeMembership =
    me.memberships.find((m) => m.gym?.id === currentGymId) || null;

  me.activeMembership = activeMembership;
  me.permissions = {
    can_manage_clients: !!activeMembership?.can_manage_clients,
    can_manage_cash: !!activeMembership?.can_manage_cash,
    can_manage_activities: !!activeMembership?.can_manage_activities,
    can_manage_bonuses: !!activeMembership?.can_manage_bonuses,
  };

  return me;
}

function storeAuth({ access, refresh, me }) {
  if (access) localStorage.setItem("access", access);
  if (refresh !== undefined) localStorage.setItem("refresh", refresh || "");
  if (me) localStorage.setItem("me", JSON.stringify(me));
}

function readMe() {
  try {
    const raw = localStorage.getItem("me");
    return raw ? JSON.parse(raw) : null;
  } catch {
    return null;
  }
}

// -------- authProvider --------
const authProvider = {
  // React-Admin pasa { username, password } (tu backend usa email)
  login: async ({ username, password }) => {
    // 1) Obtener token
    const payload = { email: username, password };
    // /token/ no requiere Authorization; usar la misma instancia no molesta
    const { data } = await api.post(`/token/`, payload, {
      baseURL: API,
      headers: { "Content-Type": "application/json" },
    });

    if (!data?.access) throw new Error("Credenciales inválidas");
    localStorage.setItem("access", data.access);
    localStorage.setItem("refresh", data.refresh || "");

    // 2) Obtener /me con Authorization: Bearer <access> (lo añade el interceptor)
    const meResp = await api.get(`/me/`);
    const me = normalizeMe(meResp.data);

    storeAuth({ access: data.access, refresh: data.refresh || "", me });
    return Promise.resolve();
  },

  logout: () => {
    localStorage.removeItem("access");
    localStorage.removeItem("refresh");
    localStorage.removeItem("me");
    return Promise.resolve();
  },

  checkAuth: () =>
    localStorage.getItem("access") ? Promise.resolve() : Promise.reject(),

  checkError: ({ status }) => {
    if (status === 401 || status === 403) {
      localStorage.removeItem("access");
      localStorage.removeItem("refresh");
      localStorage.removeItem("me");
      return Promise.reject();
    }
    return Promise.resolve();
  },

  // Roles/Permisos para RA (solo desde caché; no bloquea la UI)
  getPermissions: async () => {
    const cached = readMe();
    if (cached) {
      return {
        role: cached.role,
        currentGym: cached.currentGym,
        activeMembership: cached.activeMembership || null,
        permissions: cached.permissions || {},
      };
    }
    return { role: "client", currentGym: null, activeMembership: null, permissions: {} };
  },

  // Identidad para RA (solo desde caché; evita llamadas tempranas a /me)
  getIdentity: async () => {
    const me = readMe();
    if (me) {
      return {
        id: me.id ?? me.email ?? "user",
        fullName: me.fullName || me.email || "Usuario",
        avatar: me.avatar || null,
        email: me.email,
        role: me.role,
        currentGym: me.currentGym,
        memberships: me.memberships,
        permissions: me.permissions,
      };
    }
    // Identidad mínima si aún no hay caché
    return {
      id: "user",
      fullName: "Usuario",
      avatar: null,
      email: null,
      role: "client",
      currentGym: null,
      memberships: [],
      permissions: {},
    };
  },

  // Cambiar sede activa desde el avatar
  setCurrentGym: async (gymId) => {
    await api.post(`/set-current-gym/`, { gym_id: gymId });
    const { data } = await api.get(`/me/`);
    const me = normalizeMe(data);
    storeAuth({ me });
    return me;
  },
};

export default authProvider;
