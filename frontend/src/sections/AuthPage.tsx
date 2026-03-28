import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Stars, Mail, Lock, User, ChevronRight, Star } from 'lucide-react';
import { useAuth } from '@/hooks/useAuth';
import { useTranslation } from '@/lib/i18n';
import { api } from '@/lib/api';

export default function AuthPage() {
  const navigate = useNavigate();
  const { login, register } = useAuth();
  const { t } = useTranslation();
  const [loginForm, setLoginForm] = useState({ email: '', password: '' });
  const [registerForm, setRegisterForm] = useState({ name: '', email: '', password: '' });
  const [isAstrologer, setIsAstrologer] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleLogin = async () => {
    if (!loginForm.email || !loginForm.password) return;
    setLoading(true); setError('');
    try { await login(loginForm.email, loginForm.password); navigate('/'); }
    catch (err) { setError(err instanceof Error ? err.message : 'Login failed'); }
    finally { setLoading(false); }
  };

  const handleRegister = async () => {
    if (!registerForm.name || !registerForm.email || !registerForm.password) return;
    setLoading(true); setError('');
    try {
      if (isAstrologer) {
        // Use astrologer registration endpoint
        const data = await api.post('/api/auth/register-astrologer', {
          email: registerForm.email,
          password: registerForm.password,
          name: registerForm.name,
        });
        localStorage.setItem('astrovedic_token', data.token);
        // Force reload to pick up the new user
        window.location.href = '/astrologer-panel';
      } else {
        await register(registerForm.email, registerForm.password, registerForm.name);
        navigate('/');
      }
    }
    catch (err) { setError(err instanceof Error ? err.message : 'Registration failed'); }
    finally { setLoading(false); }
  };

  return (
    <div className="min-h-[80vh] flex items-center justify-center py-24 px-4 bg-transparent">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <div className="w-16 h-16 rounded-full bg-gradient-to-br from-sacred-gold to-sacred-saffron flex items-center justify-center mx-auto mb-4 shadow-glow-gold">
            <Stars className="w-8 h-8 text-cosmic-bg" />
          </div>
          <h2 className="text-2xl sm:text-3xl font-sacred font-bold text-cosmic-text mb-2">{t('auth.welcome')}</h2>
          <p className="text-cosmic-text-secondary">{t('auth.subtitle')}</p>
        </div>
        {error && <div className="mb-4 p-3 rounded-xl bg-red-900/30 border border-red-500/30 text-red-400 text-sm text-center">{error}</div>}
        <Tabs defaultValue="login" className="w-full">
          <TabsList className="grid grid-cols-2 bg-cosmic-card mb-6 border border-sacred-gold/10">
            <TabsTrigger value="login" className="data-[state=active]:bg-sacred-gold data-[state=active]:text-cosmic-bg text-cosmic-text-secondary">{t('auth.signIn')}</TabsTrigger>
            <TabsTrigger value="register" className="data-[state=active]:bg-sacred-gold data-[state=active]:text-cosmic-bg text-cosmic-text-secondary">{t('auth.signUp')}</TabsTrigger>
          </TabsList>
          <TabsContent value="login" className="mt-0">
            <div className="space-y-4">
              <div className="relative">
                <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-sacred-gold" />
                <Input type="email" value={loginForm.email} onChange={(e) => setLoginForm({ ...loginForm, email: e.target.value })} placeholder={t('auth.email')} className="pl-10 input-sacred" />
              </div>
              <div className="relative">
                <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-sacred-gold" />
                <Input type="password" value={loginForm.password} onChange={(e) => setLoginForm({ ...loginForm, password: e.target.value })} placeholder={t('auth.password')} onKeyDown={(e) => e.key === 'Enter' && handleLogin()} className="pl-10 input-sacred" />
              </div>
              <Button onClick={handleLogin} disabled={loading || !loginForm.email || !loginForm.password} className="w-full btn-sacred disabled:opacity-50">
                {loading ? t('common.loading') : t('auth.signIn')}<ChevronRight className="w-5 h-5 ml-2" />
              </Button>
            </div>
          </TabsContent>
          <TabsContent value="register" className="mt-0">
            <div className="space-y-4">
              <div className="relative">
                <User className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-sacred-gold" />
                <Input type="text" value={registerForm.name} onChange={(e) => setRegisterForm({ ...registerForm, name: e.target.value })} placeholder={t('auth.fullName')} className="pl-10 input-sacred" />
              </div>
              <div className="relative">
                <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-sacred-gold" />
                <Input type="email" value={registerForm.email} onChange={(e) => setRegisterForm({ ...registerForm, email: e.target.value })} placeholder={t('auth.email')} className="pl-10 input-sacred" />
              </div>
              <div className="relative">
                <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-sacred-gold" />
                <Input type="password" value={registerForm.password} onChange={(e) => setRegisterForm({ ...registerForm, password: e.target.value })} placeholder={t('auth.password')} onKeyDown={(e) => e.key === 'Enter' && handleRegister()} className="pl-10 input-sacred" />
              </div>
              {/* Astrologer toggle */}
              <button
                onClick={() => setIsAstrologer(!isAstrologer)}
                className={`w-full flex items-center gap-3 p-3 border transition-colors rounded-lg ${
                  isAstrologer
                    ? 'border-sacred-gold bg-sacred-gold/10 text-sacred-gold'
                    : 'border-sacred-gold/20 text-cosmic-text-secondary hover:border-sacred-gold/40'
                }`}
              >
                <Star className={`w-5 h-5 ${isAstrologer ? 'text-sacred-gold' : 'text-cosmic-text-muted'}`} />
                <span className="text-sm font-medium">{t('astrologer.registerAsAstrologer')}</span>
                <div className={`ml-auto w-10 h-5 rounded-full transition-colors ${isAstrologer ? 'bg-sacred-gold' : 'bg-cosmic-surface'}`}>
                  <div className={`w-4 h-4 rounded-full bg-white shadow-sm transform transition-transform mt-0.5 ${isAstrologer ? 'translate-x-5.5 ml-[22px]' : 'ml-0.5'}`} />
                </div>
              </button>
              <Button onClick={handleRegister} disabled={loading || !registerForm.name || !registerForm.email || !registerForm.password} className="w-full btn-sacred disabled:opacity-50">
                {loading ? t('common.loading') : (isAstrologer ? t('astrologer.registerAsAstrologer') : t('auth.signUp'))}<ChevronRight className="w-5 h-5 ml-2" />
              </Button>
            </div>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
}
