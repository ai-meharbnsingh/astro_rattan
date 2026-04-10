const API_BASE = import.meta.env.VITE_API_URL || '';

/** Map raw/technical error messages to user-friendly text */
function friendlyError(msg: string): string {
  const map: Record<string, string> = {
    'Failed to fetch': 'Unable to connect. Please check your internet connection.',
    'NetworkError when attempting to fetch resource.': 'Unable to connect. Please check your internet connection.',
    'Load failed': 'Unable to connect. Please check your internet connection.',
    'Internal Server Error': 'Something went wrong on our end. Please try again.',
    'Not authenticated': 'Your session has expired. Please log in again.',
  };
  return map[msg] || msg;
}

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

async function fetchWithRetry(url: string, options: RequestInit, retries = 2): Promise<Response> {
  for (let i = 0; i <= retries; i++) {
    try {
      const res = await fetch(url, options);
      // Retry on 500/502/503/504 (cold start / transient errors)
      if (res.status >= 500 && i < retries) {
        await new Promise((r) => setTimeout(r, 1000 * (i + 1)));
        continue;
      }
      return res;
    } catch (err) {
      // Network error (backend unreachable during cold start)
      if (i < retries) {
        await new Promise((r) => setTimeout(r, 1000 * (i + 1)));
        continue;
      }
      throw new Error(friendlyError(err instanceof Error ? err.message : String(err)));
    }
  }
  return fetch(url, options); // unreachable, satisfies TS
}

export async function apiFetch(endpoint: string, options: RequestInit = {}) {
  const token = localStorage.getItem('astrovedic_token');
  const headers = new Headers(options.headers || {});
  if (token) headers.set('Authorization', `Bearer ${token}`);
  if (!(options.body instanceof FormData) && !headers.has('Content-Type')) {
    headers.set('Content-Type', 'application/json');
  }

  const res = await fetchWithRetry(`${API_BASE}${endpoint}`, { ...options, headers });

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
        throw new Error(friendlyError(detail));
      }
      const ct = retryRes.headers.get('content-type') || '';
      return ct.includes('application/json') ? retryRes.json() : retryRes.text();
    }
    // Refresh failed — clear stale tokens, throw (don't redirect — let components handle it)
    localStorage.removeItem('astrovedic_token');
    localStorage.removeItem('astrovedic_refresh_token');
    throw new Error(friendlyError('Not authenticated'));
  }

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    const detail = typeof err.detail === 'string' ? err.detail : Array.isArray(err.detail) ? err.detail.map((d: any) => d.msg || d).join('; ') : JSON.stringify(err.detail) || res.statusText;
    throw new Error(friendlyError(detail));
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

/** Convert YYYY-MM-DD to DD/MM/YYYY (astrologer-friendly format) */
export function formatDate(d: string | null | undefined): string {
  if (!d) return '';
  const str = d.toString();
  // Handle YYYY-MM-DD
  const match = str.match(/^(\d{4})-(\d{2})-(\d{2})/);
  if (match) return `${match[3]}/${match[2]}/${match[1]}`;
  return str;
}

/** Format a timestamp (ISO or Date) to DD/MM/YYYY HH:MM */
export function formatDateTime(d: string | null | undefined): string {
  if (!d) return '';
  const date = new Date(d);
  if (isNaN(date.getTime())) return String(d);
  const dd = String(date.getDate()).padStart(2, '0');
  const mm = String(date.getMonth() + 1).padStart(2, '0');
  const yyyy = date.getFullYear();
  const hh = String(date.getHours()).padStart(2, '0');
  const min = String(date.getMinutes()).padStart(2, '0');
  return `${dd}/${mm}/${yyyy} ${hh}:${min}`;
}
