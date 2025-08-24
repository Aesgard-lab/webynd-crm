// src/dataProvider.js
import { fetchUtils } from 'react-admin';

const API_URL = import.meta.env.VITE_API_URL || '/api';
const SUPERADMIN_URL =
  import.meta.env.VITE_SUPERADMIN_URL || '/api/superadmin';

/** ----------------------------
 * Helpers de routing por recurso
 * ----------------------------- */
const isSuperadminResource = (resource) =>
  resource.startsWith('saas/') || resource.startsWith('orgs/');

const baseFor = (resource) =>
  isSuperadminResource(resource) ? SUPERADMIN_URL : API_URL;

/** ----------------------------
 * HTTP client with JWT + 401/403 handling
 * ----------------------------- */
const httpClient = (url, options = {}) => {
  const token = localStorage.getItem('access');
  const headers = new Headers(options.headers || {});
  headers.set('Accept', 'application/json');
  if (token) headers.set('Authorization', `Bearer ${token}`);
  // Solo establecemos Content-Type cuando NO es FormData
  if (!(options.body instanceof FormData)) {
    headers.set('Content-Type', 'application/json');
  }

  return fetchUtils.fetchJson(url, { ...options, headers }).catch((err) => {
    const status = err?.status;
    if (status === 401 || status === 403) {
      try {
        localStorage.removeItem('access');
        localStorage.removeItem('refresh');
      } catch (_) {}
      if (typeof window !== 'undefined') {
        window.location.hash = '#/login';
      }
    }
    throw err;
  });
};

/** ----------------------------
 * Query helpers
 * ----------------------------- */
const buildQuery = (resource, params) => {
  const { page, perPage } = params.pagination || { page: 1, perPage: 25 };
  const { field, order } = params.sort || { field: 'id', order: 'DESC' };
  const filter = params.filter || {};
  const search = filter.q || undefined;

  const q = {
    page,
    page_size: perPage,
    ordering: order === 'ASC' ? field : `-${field}`,
  };
  if (search) q.search = search;

  // Scoping por gimnasio SOLO para recursos NO-superadmin
  const currentGymId = localStorage.getItem('currentGymId');
  if (currentGymId && !isSuperadminResource(resource)) {
    q.gym = currentGymId;
  }

  // Pasa el resto de filtros (excepto q)
  Object.entries(filter).forEach(([k, v]) => {
    if (k !== 'q' && v !== undefined && v !== null && v !== '') q[k] = v;
  });

  return q;
};

/** ----------------------------
 * FormData helpers (foto + arrays)
 * ----------------------------- */
const isFileLike = (v) =>
  v instanceof File ||
  v instanceof Blob ||
  (v && typeof v === 'object' && v.rawFile instanceof File);

const shouldUseFormData = (data) => {
  if (!data || typeof data !== 'object') return false;
  return Object.values(data).some((v) => {
    if (isFileLike(v)) return true;
    if (v && typeof v === 'object' && 'rawFile' in v) return true; // ImageInput
    return false;
  });
};

const normalizeImageValue = (v) => {
  if (v && typeof v === 'object' && v.rawFile instanceof File) return v.rawFile;
  return v;
};

const toFormData = (data) => {
  const form = new FormData();
  Object.entries(data || {}).forEach(([key, value]) => {
    if (value === undefined || value === null) return;

    if (key === 'photo') {
      const file = normalizeImageValue(value);
      if (file instanceof File || file instanceof Blob) {
        form.append('photo', file);
        return;
      }
      form.append('photo', value);
      return;
    }

    if (Array.isArray(value)) {
      value.forEach((item) => form.append(key, item));
      return;
    }

    if (typeof value === 'object') {
      form.append(key, JSON.stringify(value));
      return;
    }

    form.append(key, value);
  });
  return form;
};

/** ----------------------------
 * Data Provider
 * ----------------------------- */
const dataProvider = {
  getList: (resource, params) => {
    const query = buildQuery(resource, params);
    const url = `${baseFor(resource)}/${resource}/?${fetchUtils.queryParameters(
      query
    )}`;
    return httpClient(url).then(({ json }) => ({
      data: json.results,
      total: json.count,
    }));
  },

  getOne: (resource, params) => {
    // Soporte especial KPIs de dashboard
    if (resource === 'dashboard/kpis') {
      const gym = params?.meta?.gym;
      const range = params?.meta?.range || 'last_30d';
      const url = `${API_URL}/dashboard/kpis/?${fetchUtils.queryParameters({
        gym,
        range,
      })}`;
      return httpClient(url).then(({ json }) => ({ data: json }));
    }

    return httpClient(`${baseFor(resource)}/${resource}/${params.id}/`).then(
      ({ json }) => ({ data: json })
    );
  },

  getMany: (resource, params) => {
    const url = `${baseFor(resource)}/${resource}/?${fetchUtils.queryParameters({
      id__in: params.ids,
    })}`;
    return httpClient(url).then(({ json }) => ({
      data: json.results || json,
    }));
  },

  getManyReference: (resource, params) => {
    const query = buildQuery(resource, params);
    query[params.target] = params.id;
    const url = `${baseFor(resource)}/${resource}/?${fetchUtils.queryParameters(
      query
    )}`;
    return httpClient(url).then(({ json }) => ({
      data: json.results,
      total: json.count,
    }));
  },

  update: (resource, params) => {
    let body = { ...params.data };

    const currentGymId = localStorage.getItem('currentGymId');
    if (
      currentGymId &&
      resource === 'clients' &&
      !isSuperadminResource(resource) &&
      !body.gym
    ) {
      body.gym = Number(currentGymId);
    }

    const useForm = shouldUseFormData(body);
    const payload = useForm ? toFormData(body) : JSON.stringify(body);

    return httpClient(`${baseFor(resource)}/${resource}/${params.id}/`, {
      method: 'PUT',
      body: payload,
    }).then(({ json }) => ({ data: json }));
  },

  create: (resource, params) => {
    let body = { ...params.data };

    const currentGymId = localStorage.getItem('currentGymId');
    if (
      currentGymId &&
      resource === 'clients' &&
      !isSuperadminResource(resource) &&
      !body.gym
    ) {
      body.gym = Number(currentGymId);
    }

    const useForm = shouldUseFormData(body);
    const payload = useForm ? toFormData(body) : JSON.stringify(body);

    return httpClient(`${baseFor(resource)}/${resource}/`, {
      method: 'POST',
      body: payload,
    }).then(({ json }) => ({ data: json }));
  },

  delete: (resource, params) =>
    httpClient(`${baseFor(resource)}/${resource}/${params.id}/`, {
      method: 'DELETE',
    }).then(() => ({ data: { id: params.id } })),

  deleteMany: (resource, params) =>
    Promise.all(
      params.ids.map((id) =>
        httpClient(`${baseFor(resource)}/${resource}/${id}/`, {
          method: 'DELETE',
        })
      )
    ).then(() => ({ data: params.ids })),
};

export default dataProvider;
