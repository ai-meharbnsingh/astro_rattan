import { useState, useEffect, createContext, useContext, useCallback, type ReactNode, createElement } from 'react';
import { api } from '../lib/api';

interface User {
  id: string;
  email: string;
  name: string;
  role?: string;
  phone?: string;
  date_of_birth?: string;
  gender?: string;
  city?: string;
  avatar_url?: string;
}

interface AuthContextValue {
  user: User | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<any>;
  register: (email: string, password: string, name: string, emailToken: string) => Promise<any>;
  logout: () => void;
  refreshUser: () => Promise<void>;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextValue>({
  user: null,
  loading: true,
  login: async () => {},
  register: async () => {},
  logout: () => {},
  refreshUser: async () => {},
  isAuthenticated: false,
});

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('astrorattan_token');
    if (token) {
      api.get('/api/auth/me').then(setUser).catch(() => {
        localStorage.removeItem('astrorattan_token');
        localStorage.removeItem('astrorattan_refresh_token');
      }).finally(() => setLoading(false));
    } else {
      setLoading(false);
    }
  }, []);

  const login = useCallback(async (email: string, password: string) => {
    const data = await api.post('/api/auth/login', { email, password });
    localStorage.setItem('astrorattan_token', data.token);
    if (data.refresh_token) localStorage.setItem('astrorattan_refresh_token', data.refresh_token);
    setUser(data.user);
    return data;
  }, []);

  const register = useCallback(async (email: string, password: string, name: string, emailToken: string) => {
    const data = await api.post('/api/auth/register', { email, password, name, email_token: emailToken });
    localStorage.setItem('astrorattan_token', data.token);
    if (data.refresh_token) localStorage.setItem('astrorattan_refresh_token', data.refresh_token);
    setUser(data.user);
    return data;
  }, []);

  const refreshUser = useCallback(async () => {
    try {
      const data = await api.get('/api/auth/me');
      setUser(data);
    } catch { /* ignore */ }
  }, []);

  const logout = useCallback(() => {
    localStorage.removeItem('astrorattan_token');
    localStorage.removeItem('astrorattan_refresh_token');
    setUser(null);
    window.location.href = '/';
  }, []);

  return createElement(
    AuthContext.Provider,
    { value: { user, loading, login, register, logout, refreshUser, isAuthenticated: !!user } },
    children
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
