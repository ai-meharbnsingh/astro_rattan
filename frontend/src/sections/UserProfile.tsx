import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { User, Loader2, Save, Lock, ShoppingBag, FileText, Activity, Star, Download, Sparkles } from 'lucide-react';
import { api } from '@/lib/api';
import { useAuth } from '@/hooks/useAuth';

interface Profile {
  name: string;
  email: string;
  date_of_birth?: string;
  gender?: string;
  city?: string;
  phone?: string;
}

interface ActivityHistory {
  kundli_count: number;
  order_count: number;
  consultation_count: number;
  ai_chats: number;
}

interface HistoryResponse {
  kundlis?: { count?: number };
  orders?: { count?: number };
  consultations?: { count?: number };
  ai_chats?: { count?: number };
  reports?: { count?: number };
}

interface Order {
  id: number;
  order_number?: string;
  total: number;
  status: string;
  created_at: string;
}

interface Report {
  id: number;
  title: string;
  type: string;
  created_at: string;
  status: string;
  pdf_url?: string;
  price?: number;
}

const formatPrice = (price: number) =>
  new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR', maximumFractionDigits: 0 }).format(price);

export default function UserProfile() {
  const { user, isAuthenticated } = useAuth();
  const [profile, setProfile] = useState<Profile>({ name: '', email: '' });
  const [activity, setActivity] = useState<ActivityHistory>({ kundli_count: 0, order_count: 0, consultation_count: 0, ai_chats: 0 });
  const [orders, setOrders] = useState<Order[]>([]);
  const [reports, setReports] = useState<Report[]>([]);
  const [loading, setLoading] = useState(true);
  const [editing, setEditing] = useState(false);
  const [saving, setSaving] = useState(false);

  // Change password
  const [passwordForm, setPasswordForm] = useState({ current_password: '', new_password: '', confirm_password: '' });
  const [passwordMsg, setPasswordMsg] = useState('');
  const [changingPassword, setChangingPassword] = useState(false);

  useEffect(() => {
    if (!isAuthenticated) { setLoading(false); return; }
    let cancelled = false;
    const load = async () => {
      setLoading(true);
      const [meRes, historyRes, ordersRes, reportsRes] = await Promise.allSettled([
        api.get('/api/auth/me'),
        api.get('/api/auth/history'),
        api.get('/api/orders'),
        api.get('/api/reports'),
      ]);
      if (!cancelled) {
        if (meRes.status === 'fulfilled') {
          const me = meRes.value as Partial<Profile>;
          setProfile({
            name: me.name || '',
            email: me.email || '',
            date_of_birth: me.date_of_birth || '',
            gender: me.gender || '',
            city: me.city || '',
            phone: me.phone || '',
          });
        }
        if (historyRes.status === 'fulfilled') {
          const history = historyRes.value as HistoryResponse;
          setActivity({
            kundli_count: history.kundlis?.count ?? 0,
            order_count: history.orders?.count ?? 0,
            consultation_count: history.consultations?.count ?? 0,
            ai_chats: history.ai_chats?.count ?? 0,
          });
        }
        if (ordersRes.status === 'fulfilled') {
          const list = Array.isArray(ordersRes.value) ? ordersRes.value : ordersRes.value.orders || [];
          setOrders(list);
        }
        if (reportsRes.status === 'fulfilled') {
          const list = Array.isArray(reportsRes.value) ? reportsRes.value : reportsRes.value.reports || [];
          setReports(list);
        }
        setLoading(false);
      }
    };
    load();
    return () => { cancelled = true; };
  }, [isAuthenticated]);

  const saveProfile = async () => {
    setSaving(true);
    try {
      await api.patch('/api/auth/profile', {
        name: profile.name,
        date_of_birth: profile.date_of_birth || undefined,
        gender: profile.gender || undefined,
        city: profile.city || undefined,
        phone: profile.phone || undefined,
      });
      setEditing(false);
    } catch { /* empty */ }
    setSaving(false);
  };

  const changePassword = async () => {
    setPasswordMsg('');
    if (passwordForm.new_password !== passwordForm.confirm_password) {
      setPasswordMsg('Passwords do not match');
      return;
    }
    if (passwordForm.new_password.length < 6) {
      setPasswordMsg('Password must be at least 6 characters');
      return;
    }
    setChangingPassword(true);
    try {
      await api.post('/api/auth/change-password', {
        current_password: passwordForm.current_password,
        new_password: passwordForm.new_password,
      });
      setPasswordMsg('Password changed successfully');
      setPasswordForm({ current_password: '', new_password: '', confirm_password: '' });
    } catch (err) {
      setPasswordMsg(err instanceof Error ? err.message : 'Failed to change password');
    }
    setChangingPassword(false);
  };

  if (!isAuthenticated) {
    return (
      <div className="max-w-4xl mx-auto py-24 px-4 text-center">
        <User className="w-16 h-16 text-cosmic-text-muted mx-auto mb-4" />
        <h2 className="text-2xl font-display font-bold text-cosmic-text mb-2">Sign In Required</h2>
        <p className="text-cosmic-text-secondary">Please log in to view your profile.</p>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center py-32">
        <Loader2 className="w-10 h-10 text-sacred-gold animate-spin" />
      </div>
    );
  }

  const activityCards = [
    { label: 'Kundli Generated', value: activity.kundli_count, icon: Star, color: 'bg-purple-100 text-purple-600' },
    { label: 'Orders', value: activity.order_count, icon: ShoppingBag, color: 'bg-blue-500/20 text-blue-600' },
    { label: 'Consultations', value: activity.consultation_count, icon: Activity, color: 'bg-green-500/20 text-green-400' },
    { label: 'AI Chats', value: activity.ai_chats, icon: Activity, color: 'bg-yellow-100 text-yellow-600' },
  ];

  return (
    <section className="max-w-4xl mx-auto py-24 px-4">
      <div className="flex items-center gap-3 mb-8">
        <div className="w-12 h-12 rounded-full bg-sacred-gold flex items-center justify-center text-[#1a1a2e] font-bold text-xl">
          {(user?.name || 'U').charAt(0).toUpperCase()}
        </div>
        <div>
          <h2 className="text-2xl font-display font-bold text-cosmic-text">{profile.name || 'My Profile'}</h2>
          <p className="text-sm text-cosmic-text-secondary">{profile.email}</p>
        </div>
      </div>

      {/* Activity summary */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-8">
        {activityCards.map((a) => (
          <Card key={a.label} className="bg-cosmic-card border-0 shadow-soft">
            <CardContent className="p-4 text-center">
              <div className={`w-10 h-10 rounded-xl flex items-center justify-center mx-auto mb-2 ${a.color}`}>
                <a.icon className="w-5 h-5" />
              </div>
              <p className="text-2xl font-bold text-cosmic-text">{a.value}</p>
              <p className="text-xs text-cosmic-text-secondary">{a.label}</p>
            </CardContent>
          </Card>
        ))}
      </div>

      <Tabs defaultValue="profile">
        <TabsList className="bg-cosmic-surface mb-6">
          <TabsTrigger value="profile" className="data-[state=active]:bg-sacred-gold data-[state=active]:text-[#1a1a2e]">Profile</TabsTrigger>
          <TabsTrigger value="password" className="data-[state=active]:bg-sacred-gold data-[state=active]:text-[#1a1a2e]">Password</TabsTrigger>
          <TabsTrigger value="orders" className="data-[state=active]:bg-sacred-gold data-[state=active]:text-[#1a1a2e]">Orders</TabsTrigger>
          <TabsTrigger value="reports" className="data-[state=active]:bg-sacred-gold data-[state=active]:text-[#1a1a2e]">Reports</TabsTrigger>
        </TabsList>

        <TabsContent value="profile">
          <Card className="bg-cosmic-card border-0 shadow-soft">
            <CardContent className="p-6">
              <div className="flex justify-between items-center mb-4">
                <h3 className="font-display font-semibold text-cosmic-text">Personal Information</h3>
                {!editing ? (
                  <Button variant="outline" size="sm" onClick={() => setEditing(true)}>Edit</Button>
                ) : (
                  <Button size="sm" onClick={saveProfile} disabled={saving} className="bg-sacred-gold text-[#1a1a2e] hover:bg-sacred-gold-dark">
                    <Save className="w-4 h-4 mr-1" />{saving ? 'Saving...' : 'Save'}
                  </Button>
                )}
              </div>
              <div className="grid sm:grid-cols-2 gap-4">
                <div>
                  <label className="text-sm font-medium text-cosmic-text mb-1 block">Name</label>
                  {editing ? (
                    <Input value={profile.name} onChange={(e) => setProfile({ ...profile, name: e.target.value })} className="bg-cosmic-card border-sacred-gold/15" />
                  ) : (
                    <p className="text-cosmic-text-secondary">{profile.name}</p>
                  )}
                </div>
                <div>
                  <label className="text-sm font-medium text-cosmic-text mb-1 block">Email</label>
                  <p className="text-cosmic-text-secondary">{profile.email}</p>
                </div>
                <div>
                  <label className="text-sm font-medium text-cosmic-text mb-1 block">Date of Birth</label>
                  {editing ? (
                    <Input type="date" value={profile.date_of_birth || ''} onChange={(e) => setProfile({ ...profile, date_of_birth: e.target.value })} className="bg-cosmic-card border-sacred-gold/15" />
                  ) : (
                    <p className="text-cosmic-text-secondary">{profile.date_of_birth || 'Not set'}</p>
                  )}
                </div>
                <div>
                  <label className="text-sm font-medium text-cosmic-text mb-1 block">Gender</label>
                  {editing ? (
                    <Input value={profile.gender || ''} onChange={(e) => setProfile({ ...profile, gender: e.target.value })} placeholder="Male / Female / Other" className="bg-cosmic-card border-sacred-gold/15" />
                  ) : (
                    <p className="text-cosmic-text-secondary">{profile.gender || 'Not set'}</p>
                  )}
                </div>
                <div>
                  <label className="text-sm font-medium text-cosmic-text mb-1 block">City</label>
                  {editing ? (
                    <Input value={profile.city || ''} onChange={(e) => setProfile({ ...profile, city: e.target.value })} className="bg-cosmic-card border-sacred-gold/15" />
                  ) : (
                    <p className="text-cosmic-text-secondary">{profile.city || 'Not set'}</p>
                  )}
                </div>
                <div>
                  <label className="text-sm font-medium text-cosmic-text mb-1 block">Phone</label>
                  {editing ? (
                    <Input value={profile.phone || ''} onChange={(e) => setProfile({ ...profile, phone: e.target.value })} className="bg-cosmic-card border-sacred-gold/15" />
                  ) : (
                    <p className="text-cosmic-text-secondary">{profile.phone || 'Not set'}</p>
                  )}
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="password">
          <Card className="bg-cosmic-card border-0 shadow-soft max-w-md">
            <CardContent className="p-6">
              <h3 className="font-display font-semibold text-cosmic-text mb-4 flex items-center gap-2">
                <Lock className="w-5 h-5 text-sacred-gold" />Change Password
              </h3>
              {passwordMsg && (
                <div className={`mb-4 p-3 rounded-xl text-sm text-center ${passwordMsg.includes('success') ? 'bg-green-900/20 text-green-400' : 'bg-red-900/20 text-red-400'}`}>
                  {passwordMsg}
                </div>
              )}
              <div className="space-y-3">
                <Input type="password" placeholder="Current Password" value={passwordForm.current_password} onChange={(e) => setPasswordForm({ ...passwordForm, current_password: e.target.value })} className="bg-cosmic-card border-sacred-gold/15" />
                <Input type="password" placeholder="New Password" value={passwordForm.new_password} onChange={(e) => setPasswordForm({ ...passwordForm, new_password: e.target.value })} className="bg-cosmic-card border-sacred-gold/15" />
                <Input type="password" placeholder="Confirm New Password" value={passwordForm.confirm_password} onChange={(e) => setPasswordForm({ ...passwordForm, confirm_password: e.target.value })} className="bg-cosmic-card border-sacred-gold/15" />
                <Button onClick={changePassword} disabled={changingPassword || !passwordForm.current_password || !passwordForm.new_password} className="w-full bg-sacred-gold text-[#1a1a2e] hover:bg-sacred-gold-dark">
                  {changingPassword ? 'Changing...' : 'Change Password'}
                </Button>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="orders">
          <Card className="bg-cosmic-card border-0 shadow-soft">
            <CardContent className="p-4">
              {orders.length === 0 ? (
                <div className="text-center py-8">
                  <ShoppingBag className="w-10 h-10 text-cosmic-text-muted mx-auto mb-2" />
                  <p className="text-cosmic-text-secondary">No orders yet.</p>
                </div>
              ) : (
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Order</TableHead>
                      <TableHead>Total</TableHead>
                      <TableHead>Status</TableHead>
                      <TableHead>Date</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {orders.map((o) => (
                      <TableRow key={o.id}>
                        <TableCell className="font-medium text-cosmic-text">{o.order_number || `#${o.id}`}</TableCell>
                        <TableCell className="text-sacred-gold font-semibold">{formatPrice(o.total)}</TableCell>
                        <TableCell><Badge variant="outline">{o.status}</Badge></TableCell>
                        <TableCell className="text-sm text-cosmic-text-secondary">{new Date(o.created_at).toLocaleDateString()}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="reports">
          <Card className="bg-cosmic-card border-0 shadow-soft">
            <CardContent className="p-6">
              <div className="flex items-center justify-between mb-6">
                <h3 className="font-display font-semibold text-cosmic-text">My Reports</h3>
                <Link to="/reports">
                  <Button size="sm" className="bg-sacred-gold text-[#1a1a2e]">
                    <Sparkles className="w-4 h-4 mr-2" />Get New Report
                  </Button>
                </Link>
              </div>
              
              {reports.length === 0 ? (
                <div className="text-center py-12 bg-cosmic-card rounded-xl">
                  <FileText className="w-12 h-12 text-cosmic-text-muted mx-auto mb-3" />
                  <p className="text-cosmic-text-secondary mb-2">No reports yet</p>
                  <p className="text-sm text-cosmic-text-secondary mb-4">Unlock deep insights with personalized PDF reports</p>
                  <Link to="/reports">
                    <Button className="bg-sacred-gold text-[#1a1a2e]">
                      Browse Reports
                    </Button>
                  </Link>
                </div>
              ) : (
                <div className="space-y-3">
                  {reports.map((r) => (
                    <div key={r.id} className="flex items-center justify-between p-4 bg-cosmic-card rounded-xl">
                      <div className="flex items-center gap-3">
                        <div className="w-10 h-10 rounded-lg bg-sacred-gold/10 flex items-center justify-center">
                          <FileText className="w-5 h-5 text-sacred-gold" />
                        </div>
                        <div>
                          <p className="font-medium text-cosmic-text">{r.title}</p>
                          <div className="flex items-center gap-2 text-sm text-cosmic-text-secondary">
                            <Badge variant="outline" className="text-xs">{r.type}</Badge>
                            <span>•</span>
                            <span>{new Date(r.created_at).toLocaleDateString()}</span>
                          </div>
                        </div>
                      </div>
                      <div className="flex items-center gap-2">
                        {r.status === 'ready' && r.pdf_url ? (
                          <a 
                            href={r.pdf_url} 
                            target="_blank" 
                            rel="noopener noreferrer"
                          >
                            <Button size="sm" variant="outline" className="border-green-500/30 text-green-400 hover:bg-green-900/20">
                              <Download className="w-4 h-4 mr-1" />Download
                            </Button>
                          </a>
                        ) : r.status === 'generating' ? (
                          <Badge className="bg-amber-100 text-amber-700">
                            <Loader2 className="w-3 h-3 mr-1 animate-spin" />Generating
                          </Badge>
                        ) : r.status === 'paid' ? (
                          <Badge className="bg-blue-500/20 text-blue-700">Processing</Badge>
                        ) : (
                          <Badge className="bg-cosmic-surface text-cosmic-text-secondary">{r.status}</Badge>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </section>
  );
}
