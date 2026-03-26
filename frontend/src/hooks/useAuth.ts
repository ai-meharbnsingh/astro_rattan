import { useState, useEffect } from 'react';
import { api } from '../lib/api';

interface User {
  id: string;
  email: string;
  name: string;
  role?: string;
}

export function useAuth() {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('astrovedic_token');
    if (token) {
      api.get('/api/auth/me').then(setUser).catch(() => {
        localStorage.removeItem('astrovedic_token');
      }).finally(() => setLoading(false));
    } else {
      setLoading(false);
    }
  }, []);

  const login = async (email: string, password: string) => {
    const data = await api.post('/api/auth/login', { email, password });
    localStorage.setItem('astrovedic_token', data.token);
    setUser(data.user);
    return data;
  };

  const register = async (email: string, password: string, name: string) => {
    const data = await api.post('/api/auth/register', { email, password, name });
    localStorage.setItem('astrovedic_token', data.token);
    setUser(data.user);
    return data;
  };

  const logout = () => {
    localStorage.removeItem('astrovedic_token');
    setUser(null);
  };

  return { user, loading, login, register, logout, isAuthenticated: !!user };
}
