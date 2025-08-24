// src/api/axios.js
import axios from "axios";
const API = import.meta.env.VITE_API_URL; // p.ej. http://localhost:8000/api

const api = axios.create({ baseURL: API });
api.interceptors.request.use((config) => {
  const t = localStorage.getItem("access");
  if (t) config.headers.Authorization = `Bearer ${t}`;
  return config;
});

export default api;

