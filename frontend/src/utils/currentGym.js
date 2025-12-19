// src/utils/currentGym.js
export function getCurrentGymId() {
  // claves típicas
  const direct =
    localStorage.getItem("currentGymId") ||
    localStorage.getItem("current_gym_id");

  if (direct) {
    const n = Number(direct);
    return Number.isFinite(n) ? n : null;
  }

  // intenta objeto guardado
  const objRaw =
    localStorage.getItem("currentGym") ||
    localStorage.getItem("current_gym");

  if (!objRaw) return null;

  try {
    const obj = JSON.parse(objRaw);
    const n = Number(obj?.id || obj?.gym?.id || obj?.current_gym?.id);
    return Number.isFinite(n) ? n : null;
  } catch {
    return null;
  }
}
