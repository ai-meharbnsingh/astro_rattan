const API_BASE = import.meta.env.VITE_API_URL || '';

let isRefreshing = false;
let refreshPromise: Promise<boolean> | null = null;

async function tryRefreshToken(): Promise<boolean> {
  const refreshToken = localStorage.getItem('astrovedic_refresh_token');
  if (!refreshToken) return false;

  try {
    const res = await fetch(`${API_BASE}/api/auth/refresh`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ refresh_token: refreshToken }),
    });
    if (!res.ok) return false;
    const data = await res.json();
    localStorage.setItem('astrovedic_token', data.token);
    localStorage.setItem('astrovedic_refresh_token', data.refresh_token);
    return true;
  } catch {
    return false;
  }
}

export async function apiFetch(endpoint: string, options: RequestInit = {}) {
  const token = localStorage.getItem('astrovedic_token');
  const headers = new Headers(options.headers || {});
  if (token) headers.set('Authorization', `Bearer ${token}`);
  if (!(options.body instanceof FormData) && !headers.has('Content-Type')) {
    headers.set('Content-Type', 'application/json');
  }

  const res = await fetch(`${API_BASE}${endpoint}`, { ...options, headers });

  if (res.status === 401 && !endpoint.includes('/api/auth/')) {
    // Try to refresh the token silently
    if (!isRefreshing) {
      isRefreshing = true;
      refreshPromise = tryRefreshToken().finally(() => { isRefreshing = false; });
    }
    const refreshed = await refreshPromise;
    if (refreshed) {
      // Retry original request with new token
      const newToken = localStorage.getItem('astrovedic_token');
      const retryHeaders = new Headers(options.headers || {});
      if (newToken) retryHeaders.set('Authorization', `Bearer ${newToken}`);
      if (!(options.body instanceof FormData) && !retryHeaders.has('Content-Type')) {
        retryHeaders.set('Content-Type', 'application/json');
      }
      const retryRes = await fetch(`${API_BASE}${endpoint}`, { ...options, headers: retryHeaders });
      if (!retryRes.ok) {
        const err = await retryRes.json().catch(() => ({ detail: retryRes.statusText }));
        const detail = typeof err.detail === 'string' ? err.detail : Array.isArray(err.detail) ? err.detail.map((d: any) => d.msg || d).join('; ') : JSON.stringify(err.detail) || retryRes.statusText;
        throw new Error(detail);
      }
      const ct = retryRes.headers.get('content-type') || '';
      return ct.includes('application/json') ? retryRes.json() : retryRes.text();
    }
    // Refresh failed — clear stale tokens, throw (don't redirect — let components handle it)
    localStorage.removeItem('astrovedic_token');
    localStorage.removeItem('astrovedic_refresh_token');
    throw new Error('Not authenticated');
  }

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    const detail = typeof err.detail === 'string' ? err.detail : Array.isArray(err.detail) ? err.detail.map((d: any) => d.msg || d).join('; ') : JSON.stringify(err.detail) || res.statusText;
    throw new Error(detail);
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
