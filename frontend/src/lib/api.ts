const API_BASE = import.meta.env.VITE_API_URL || '';

export async function apiFetch(endpoint: string, options: RequestInit = {}) {
  const token = localStorage.getItem('astrovedic_token');
  const headers = new Headers(options.headers || {});
  if (token) headers.set('Authorization', `Bearer ${token}`);
  if (!(options.body instanceof FormData) && !headers.has('Content-Type')) {
    headers.set('Content-Type', 'application/json');
  }

  const res = await fetch(`${API_BASE}${endpoint}`, { ...options, headers });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || res.statusText);
  }
  const contentType = res.headers.get('content-type') || '';
  if (contentType.includes('application/json')) {
    return res.json();
  }
  return res.text();
}

export const resolveApiUrl = (path?: string | null) => {
  if (!path) return '';
  if (/^https?:\/\//i.test(path)) return path;
  return `${API_BASE}${path.startsWith('/') ? path : `/${path}`}`;
};

export const api = {
  get: (url: string) => apiFetch(url),
  post: (url: string, data: unknown) => apiFetch(url, { method: 'POST', body: JSON.stringify(data) }),
  postForm: (url: string, data: FormData) => apiFetch(url, { method: 'POST', body: data }),
  put: (url: string, data: unknown) => apiFetch(url, { method: 'PUT', body: JSON.stringify(data) }),
  patch: (url: string, data: unknown) => apiFetch(url, { method: 'PATCH', body: JSON.stringify(data) }),
  delete: (url: string) => apiFetch(url, { method: 'DELETE' }),
};
