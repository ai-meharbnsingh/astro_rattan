import { useState, useEffect, createContext, useContext, useCallback, type ReactNode, createElement } from 'react';
import { api } from '../lib/api';

interface User {
  id: string;
  email: string;
  name: string;
  role?: string;
}

interface AuthContextValue {
  user: User | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<any>;
  register: (email: string, password: string, name: string, emailToken: string) => Promise<any>;
  logout: () => void;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextValue>({
  user: null,
  loading: true,
  login: async () => {},
  register: async () => {},
  logout: () => {},
  isAuthenticated: false,
});

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('astrovedic_token');
    if (token) {
      api.get('/api/auth/me').then(setUser).catch(() => {
        localStorage.removeItem('astrovedic_token');
        localStorage.removeItem('astrovedic_refresh_token');
      }).finally(() => setLoading(false));
    } else {
      setLoading(false);
    }
  }, []);

  const login = useCallback(async (email: string, password: string) => {
    const data = await api.post('/api/auth/login', { email, password });
    localStorage.setItem('astrovedic_token', data.token);
    if (data.refresh_token) localStorage.setItem('astrovedic_refresh_token', data.refresh_token);
    setUser(data.user);
    return data;
  }, []);

  const register = useCallback(async (email: string, password: string, name: string, emailToken: string) => {
    const data = await api.post('/api/auth/register', { email, password, name, email_token: emailToken });
    localStorage.setItem('astrovedic_token', data.token);
    if (data.refresh_token) localStorage.setItem('astrovedic_refresh_token', data.refresh_token);
    setUser(data.user);
    return data;
  }, []);

  const logout = useCallback(() => {
    localStorage.removeItem('astrovedic_token');
    localStorage.removeItem('astrovedic_refresh_token');
    setUser(null);
  }, []);

  return createElement(
    AuthContext.Provider,
    { value: { user, loading, login, register, logout, isAuthenticated: !!user } },
    children
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
