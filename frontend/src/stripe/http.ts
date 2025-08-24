// frontend/src/stripe/http.ts
// frontend/src/stripe/http.ts
const API_BASE =
  (typeof import.meta !== 'undefined' && (import.meta as any).env?.VITE_API_BASE) ||
  
  '';


// Ej: VITE_API_BASE="/api/superadmin"

export function getAccessToken(): string | null {
  try {
    const authRaw = localStorage.getItem('auth');
    if (authRaw) {
      const parsed = JSON.parse(authRaw);
      if (parsed?.access) return parsed.access;
      if (parsed?.token) return parsed.token;
    }
  } catch {}
  return localStorage.getItem('access');
}

export async function postWithAuth(path: string, body?: any) {
  const token = getAccessToken();
  const res = await fetch(`${API_BASE}${path}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    },
    body: body ? JSON.stringify(body) : undefined,
  });
  if (!res.ok) {
    const txt = await res.text();
    throw new Error(`HTTP ${res.status}: ${txt}`);
  }
  return res.json();
}
