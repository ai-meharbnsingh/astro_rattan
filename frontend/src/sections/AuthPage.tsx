import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Stars, Mail, Lock, User, ChevronRight } from 'lucide-react';
import { useAuth } from '@/hooks/useAuth';

export default function AuthPage() {
  const navigate = useNavigate();
  const { login, register } = useAuth();
  const [loginForm, setLoginForm] = useState({ email: '', password: '' });
  const [registerForm, setRegisterForm] = useState({ name: '', email: '', password: '' });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleLogin = async () => {
    if (!loginForm.email || !loginForm.password) return;
    setLoading(true);
    setError('');
    try {
      await login(loginForm.email, loginForm.password);
      navigate('/');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Login failed');
    } finally {
      setLoading(false);
    }
  };

  const handleRegister = async () => {
    if (!registerForm.name || !registerForm.email || !registerForm.password) return;
    setLoading(true);
    setError('');
    try {
      await register(registerForm.email, registerForm.password, registerForm.name);
      navigate('/');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Registration failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-[80vh] flex items-center justify-center py-24 px-4">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <div className="w-16 h-16 rounded-full bg-gradient-to-br from-sacred-gold to-sacred-saffron flex items-center justify-center mx-auto mb-4">
            <Stars className="w-8 h-8 text-white" />
          </div>
          <h2 className="text-2xl sm:text-3xl font-sacred font-bold text-sacred-brown mb-2">Welcome to AstroVedic</h2>
          <p className="text-sacred-text-secondary">Sign in to access personalized cosmic insights</p>
        </div>

        {error && (
          <div className="mb-4 p-3 rounded-xl bg-red-50 text-red-600 text-sm text-center">{error}</div>
        )}

        <Tabs defaultValue="login" className="w-full">
          <TabsList className="grid grid-cols-2 bg-sacred-cream mb-6">
            <TabsTrigger value="login" className="data-[state=active]:bg-sacred-gold data-[state=active]:text-white">Sign In</TabsTrigger>
            <TabsTrigger value="register" className="data-[state=active]:bg-minimal-indigo data-[state=active]:text-white">Sign Up</TabsTrigger>
          </TabsList>

          <TabsContent value="login" className="mt-0">
            <div className="space-y-4">
              <div className="relative">
                <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-sacred-gold-dark" />
                <Input type="email" value={loginForm.email} onChange={(e) => setLoginForm({ ...loginForm, email: e.target.value })} placeholder="Email" className="pl-10 input-sacred" />
              </div>
              <div className="relative">
                <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-minimal-gray-400" />
                <Input type="password" value={loginForm.password} onChange={(e) => setLoginForm({ ...loginForm, password: e.target.value })} placeholder="Password" onKeyDown={(e) => e.key === 'Enter' && handleLogin()} className="pl-10 bg-minimal-gray-50 border-minimal-gray-200 text-minimal-gray-900" />
              </div>
              <Button onClick={handleLogin} disabled={loading || !loginForm.email || !loginForm.password} className="w-full btn-sacred disabled:opacity-50">
                {loading ? 'Signing in...' : 'Sign In'}<ChevronRight className="w-5 h-5 ml-2" />
              </Button>
            </div>
          </TabsContent>

          <TabsContent value="register" className="mt-0">
            <div className="space-y-4">
              <div className="relative">
                <User className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-minimal-gray-400" />
                <Input type="text" value={registerForm.name} onChange={(e) => setRegisterForm({ ...registerForm, name: e.target.value })} placeholder="Full Name" className="pl-10 bg-minimal-gray-50 border-minimal-gray-200 text-minimal-gray-900" />
              </div>
              <div className="relative">
                <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-minimal-gray-400" />
                <Input type="email" value={registerForm.email} onChange={(e) => setRegisterForm({ ...registerForm, email: e.target.value })} placeholder="Email" className="pl-10 bg-minimal-gray-50 border-minimal-gray-200 text-minimal-gray-900" />
              </div>
              <div className="relative">
                <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-minimal-gray-400" />
                <Input type="password" value={registerForm.password} onChange={(e) => setRegisterForm({ ...registerForm, password: e.target.value })} placeholder="Password" onKeyDown={(e) => e.key === 'Enter' && handleRegister()} className="pl-10 bg-minimal-gray-50 border-minimal-gray-200 text-minimal-gray-900" />
              </div>
              <Button onClick={handleRegister} disabled={loading || !registerForm.name || !registerForm.email || !registerForm.password} className="w-full bg-minimal-indigo text-white font-semibold hover:bg-minimal-violet disabled:opacity-50">
                {loading ? 'Creating account...' : 'Create Account'}<ChevronRight className="w-5 h-5 ml-2" />
              </Button>
            </div>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
}
