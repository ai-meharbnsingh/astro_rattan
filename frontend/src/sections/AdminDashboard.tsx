import { useState, useEffect } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Textarea } from '@/components/ui/textarea';
import { Shield, Users, Package, ShoppingCart, IndianRupee, Loader2, Brain, FileText, Plus, Pencil, Trash2, ImageIcon } from 'lucide-react';
import { api } from '@/lib/api';
import { useAuth } from '@/hooks/useAuth';

interface DashboardStats {
  total_users: number;
  total_orders: number;
  total_revenue: number;
  pending_orders: number;
}

interface AdminUser {
  id: number;
  name: string;
  email: string;
  role: string;
  is_active: boolean;
  created_at: string;
}

interface AdminOrder {
  id: number;
  order_number?: string;
  user_name: string;
  total: number;
  status: string;
  tracking_number?: string;
  created_at: string;
}

interface AdminProduct {
  id: number;
  name: string;
  description?: string;
  category: string;
  price: number;
  compare_price?: number;
  stock: number;
  is_active: boolean;
  image_url?: string;
  planet?: string;
  weight?: string;
}

const PRODUCT_CATEGORIES = [
  { value: 'gemstone', label: 'Gemstone' },
  { value: 'rudraksha', label: 'Rudraksha' },
  { value: 'bracelet', label: 'Bracelet' },
  { value: 'yantra', label: 'Yantra' },
  { value: 'vastu', label: 'Vastu' },
];

const emptyProductForm = {
  name: '',
  description: '',
  category: 'gemstone',
  price: '',
  compare_price: '',
  stock: '',
  planet: '',
  weight: '',
  image_url: '',
};

interface ContentItem {
  id: number;
  title: string;
  category: string;
  status: string;
  created_at: string;
}

interface AILog {
  id: number;
  user_name: string;
  question: string;
  endpoint: string;
  created_at: string;
}

interface BlogPost {
  id: string;
  title: string;
  slug: string;
  excerpt: string;
  author_name: string;
  is_published: boolean;
  published_at: string;
}

const formatPrice = (price: number) =>
  new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR', maximumFractionDigits: 0 }).format(price);

const normalizeDashboardStats = (data: any): DashboardStats => ({
  total_users: data?.total_users ?? data?.stats?.users ?? 0,
  total_orders: data?.total_orders ?? data?.stats?.orders ?? 0,
  total_revenue: data?.total_revenue ?? data?.stats?.revenue ?? 0,
  pending_orders: data?.pending_orders ?? data?.stats?.pending_orders ?? data?.stats?.pending ?? 0,
});

export default function AdminDashboard() {
  const { user, loading: authLoading } = useAuth();
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [users, setUsers] = useState<AdminUser[]>([]);
  const [orders, setOrders] = useState<AdminOrder[]>([]);
  const [products, setProducts] = useState<AdminProduct[]>([]);
  const [content, setContent] = useState<ContentItem[]>([]);
  const [blogPosts, setBlogPosts] = useState<BlogPost[]>([]);
  const [aiLogs, setAiLogs] = useState<AILog[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('overview');
  const [contentDialogOpen, setContentDialogOpen] = useState(false);
  const [blogDialogOpen, setBlogDialogOpen] = useState(false);
  const [productDialogOpen, setProductDialogOpen] = useState(false);
  const [editingProduct, setEditingProduct] = useState<AdminProduct | null>(null);
  const [productForm, setProductForm] = useState({ ...emptyProductForm });
  const [imageUploading, setImageUploading] = useState(false);
  const [productSaving, setProductSaving] = useState(false);
  const [newContent, setNewContent] = useState({ title: '', category: 'gita', content: '' });
  const [newBlogPost, setNewBlogPost] = useState({
    title: '',
    excerpt: '',
    content: '',
    tags: '',
    author_name: 'AstroVedic Editorial',
  });
  const [trackingUpdate, setTrackingUpdate] = useState<Record<number, string>>({});
  const contentCategories = [
    { value: 'gita', label: 'Gita' },
    { value: 'aarti', label: 'Aarti' },
    { value: 'mantra', label: 'Mantra' },
    { value: 'pooja', label: 'Pooja' },
    { value: 'vrat_katha', label: 'Vrat Katha' },
    { value: 'chalisa', label: 'Chalisa' },
    { value: 'festival', label: 'Festival' },
  ];

  useEffect(() => {
    if (user?.role !== 'admin') { setLoading(false); return; }
    let cancelled = false;
    const load = async () => {
      setLoading(true);
      try {
        const [statsData, usersData, ordersData, productsData, contentData, blogData, logsData] = await Promise.allSettled([
          api.get('/api/admin/dashboard'),
          api.get('/api/admin/users'),
          api.get('/api/admin/orders'),
          api.get('/api/admin/products'),
          api.get('/api/admin/content'),
          api.get('/api/admin/blog'),
          api.get('/api/admin/ai-logs'),
        ]);
        if (!cancelled) {
          if (statsData.status === 'fulfilled') setStats(normalizeDashboardStats(statsData.value));
          if (usersData.status === 'fulfilled') {
            const list = Array.isArray(usersData.value) ? usersData.value : usersData.value.users || [];
            setUsers(list.map((item: any) => ({ ...item, is_active: Boolean(item.is_active) })));
          }
          if (ordersData.status === 'fulfilled') setOrders(Array.isArray(ordersData.value) ? ordersData.value : ordersData.value.orders || []);
          if (productsData.status === 'fulfilled') {
            const list = Array.isArray(productsData.value) ? productsData.value : productsData.value.products || [];
            setProducts(list.map((item: any) => ({ ...item, is_active: Boolean(item.is_active) })));
          }
          if (contentData.status === 'fulfilled') {
            const items = Array.isArray(contentData.value) ? contentData.value : contentData.value.items || [];
            setContent(items.map((item: any) => ({
              id: item.id,
              title: item.title,
              category: item.category || 'gita',
              status: item.status || 'published',
              created_at: item.created_at,
            })));
          }
          if (blogData.status === 'fulfilled') {
            const items = Array.isArray(blogData.value) ? blogData.value : blogData.value.items || [];
            setBlogPosts(items.map((item: any) => ({
              id: item.id,
              title: item.title,
              slug: item.slug,
              excerpt: item.excerpt,
              author_name: item.author_name,
              is_published: Boolean(item.is_published),
              published_at: item.published_at || item.created_at,
            })));
          }
          if (logsData.status === 'fulfilled') setAiLogs(Array.isArray(logsData.value) ? logsData.value : logsData.value.logs || []);
        }
      } catch { /* empty */ }
      if (!cancelled) setLoading(false);
    };
    load();
    return () => { cancelled = true; };
  }, [user?.role]);

  const deactivateUser = async (userId: number) => {
    try {
      await api.patch(`/api/admin/users/${userId}/deactivate`, {});
      setUsers((prev) => prev.map((u) => (u.id === userId ? { ...u, is_active: false } : u)));
    } catch { /* empty */ }
  };

  const updateTracking = async (orderId: number) => {
    const num = trackingUpdate[orderId];
    if (!num) return;
    try {
      await api.patch(`/api/admin/orders/${orderId}`, { tracking_number: num });
      setOrders((prev) => prev.map((o) => (o.id === orderId ? { ...o, tracking_number: num } : o)));
      setTrackingUpdate((prev) => ({ ...prev, [orderId]: '' }));
    } catch { /* empty */ }
  };

  const toggleProduct = async (productId: number, isActive: boolean) => {
    try {
      await api.patch(`/api/admin/products/${productId}/toggle`, {});
      setProducts((prev) => prev.map((p) => (p.id === productId ? { ...p, is_active: !isActive } : p)));
    } catch { /* empty */ }
  };

  const addContent = async () => {
    try {
      const data = await api.post('/api/admin/content', {
        category: newContent.category,
        title: newContent.title,
        content: newContent.content,
      });
      setContent((prev) => [{
        id: data.id,
        title: data.title,
        category: data.category || newContent.category,
        status: 'published',
        created_at: data.created_at || new Date().toISOString(),
      }, ...prev]);
      setContentDialogOpen(false);
      setNewContent({ title: '', category: 'gita', content: '' });
    } catch { /* empty */ }
  };

  const addBlogPost = async () => {
    try {
      const data = await api.post('/api/admin/blog', {
        title: newBlogPost.title,
        excerpt: newBlogPost.excerpt,
        content: newBlogPost.content,
        author_name: newBlogPost.author_name,
        tags: newBlogPost.tags
          .split(',')
          .map((tag) => tag.trim())
          .filter(Boolean),
      });
      setBlogPosts((prev) => [{
        id: data.id,
        title: data.title,
        slug: data.slug,
        excerpt: data.excerpt,
        author_name: data.author_name,
        is_published: Boolean(data.is_published),
        published_at: data.published_at || data.created_at || new Date().toISOString(),
      }, ...prev]);
      setBlogDialogOpen(false);
      setNewBlogPost({
        title: '',
        excerpt: '',
        content: '',
        tags: '',
        author_name: 'AstroVedic Editorial',
      });
    } catch { /* empty */ }
  };

  const openAddProduct = () => {
    setEditingProduct(null);
    setProductForm({ ...emptyProductForm });
    setProductDialogOpen(true);
  };

  const openEditProduct = (p: AdminProduct) => {
    setEditingProduct(p);
    setProductForm({
      name: p.name,
      description: p.description ?? '',
      category: p.category,
      price: String(p.price),
      compare_price: p.compare_price != null ? String(p.compare_price) : '',
      stock: String(p.stock),
      planet: p.planet ?? '',
      weight: p.weight ?? '',
      image_url: p.image_url ?? '',
    });
    setProductDialogOpen(true);
  };

  const handleImageUpload = async (file: File) => {
    setImageUploading(true);
    try {
      const formData = new FormData();
      formData.append('file', file);
      const data = await api.postForm('/api/admin/upload-image', formData);
      setProductForm((prev) => ({ ...prev, image_url: data.url }));
    } catch { /* empty */ }
    setImageUploading(false);
  };

  const saveProduct = async () => {
    setProductSaving(true);
    try {
      const payload = {
        name: productForm.name,
        description: productForm.description,
        category: productForm.category,
        price: parseFloat(productForm.price) || 0,
        compare_price: productForm.compare_price ? parseFloat(productForm.compare_price) : undefined,
        stock: parseInt(productForm.stock, 10) || 0,
        planet: productForm.planet || undefined,
        weight: productForm.weight || undefined,
        image_url: productForm.image_url || undefined,
      };
      if (editingProduct) {
        const data = await api.put(`/api/admin/products/${editingProduct.id}`, payload);
        setProducts((prev) => prev.map((p) =>
          p.id === editingProduct.id
            ? { ...p, ...payload, id: editingProduct.id, is_active: p.is_active, image_url: data?.image_url ?? payload.image_url }
            : p
        ));
      } else {
        const data = await api.post('/api/admin/products', payload);
        setProducts((prev) => [{
          id: data.id,
          name: payload.name,
          description: payload.description,
          category: payload.category,
          price: payload.price,
          compare_price: payload.compare_price,
          stock: payload.stock,
          is_active: true,
          image_url: data.image_url ?? payload.image_url,
          planet: payload.planet,
          weight: payload.weight,
        }, ...prev]);
      }
      setProductDialogOpen(false);
      setProductForm({ ...emptyProductForm });
      setEditingProduct(null);
    } catch { /* empty */ }
    setProductSaving(false);
  };

  const deleteProduct = async (productId: number) => {
    if (!window.confirm('Delete this product? This cannot be undone.')) return;
    try {
      await api.delete(`/api/admin/products/${productId}`);
      setProducts((prev) => prev.filter((p) => p.id !== productId));
    } catch { /* empty */ }
  };

  if (authLoading) {
    return (
      <div className="max-w-4xl mx-auto py-24 px-4 text-center">
        <Loader2 className="w-8 h-8 text-sacred-gold mx-auto animate-spin" />
      </div>
    );
  }

  if (user?.role !== 'admin') {
    return (
      <div className="max-w-4xl mx-auto py-24 px-4 text-center">
        <Shield className="w-16 h-16 text-cosmic-text-muted mx-auto mb-4" />
        <h2 className="text-2xl font-display font-bold text-cosmic-text mb-2">Admin Access Required</h2>
        <p className="text-cosmic-text-secondary">You need admin privileges to view this page.</p>
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

  const statCards = [
    { label: 'Total Users', value: stats?.total_users ?? 0, icon: Users, color: 'bg-blue-500/20 text-blue-600' },
    { label: 'Total Orders', value: stats?.total_orders ?? 0, icon: ShoppingCart, color: 'bg-green-500/20 text-green-600' },
    { label: 'Revenue', value: formatPrice(stats?.total_revenue ?? 0), icon: IndianRupee, color: 'bg-purple-100 text-purple-600' },
    { label: 'Pending', value: stats?.pending_orders ?? 0, icon: Package, color: 'bg-yellow-100 text-yellow-600' },
  ];

  return (
    <section className="max-w-7xl mx-auto py-24 px-4">
      <div className="flex items-center gap-3 mb-8">
        <div className="w-10 h-10 rounded-full bg-sacred-gold flex items-center justify-center">
          <Shield className="w-5 h-5 text-[#1a1a2e]" />
        </div>
        <div>
          <h2 className="text-2xl font-display font-bold text-cosmic-text">Admin Dashboard</h2>
          <p className="text-sm text-cosmic-text-secondary">Manage users, orders, products, and content</p>
        </div>
      </div>

      <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
        <TabsList className="bg-cosmic-surface mb-6 flex-wrap">
          <TabsTrigger value="overview" className="data-[state=active]:bg-sacred-gold data-[state=active]:text-[#1a1a2e]">Overview</TabsTrigger>
          <TabsTrigger value="users" className="data-[state=active]:bg-sacred-gold data-[state=active]:text-[#1a1a2e]">Users</TabsTrigger>
          <TabsTrigger value="orders" className="data-[state=active]:bg-sacred-gold data-[state=active]:text-[#1a1a2e]">Orders</TabsTrigger>
          <TabsTrigger value="products" className="data-[state=active]:bg-sacred-gold data-[state=active]:text-[#1a1a2e]">Products</TabsTrigger>
          <TabsTrigger value="content" className="data-[state=active]:bg-sacred-gold data-[state=active]:text-[#1a1a2e]">Content</TabsTrigger>
          <TabsTrigger value="blog" className="data-[state=active]:bg-sacred-gold data-[state=active]:text-[#1a1a2e]">Blog</TabsTrigger>
          <TabsTrigger value="ai-logs" className="data-[state=active]:bg-sacred-gold data-[state=active]:text-[#1a1a2e]">AI Logs</TabsTrigger>
        </TabsList>

        <TabsContent value="overview">
          <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4">
            {statCards.map((s) => (
              <Card key={s.label} className="bg-cosmic-card border-0 shadow-soft">
                <CardContent className="p-5 flex items-center gap-4">
                  <div className={`w-12 h-12 rounded-xl flex items-center justify-center ${s.color}`}>
                    <s.icon className="w-6 h-6" />
                  </div>
                  <div>
                    <p className="text-sm text-cosmic-text-secondary">{s.label}</p>
                    <p className="text-2xl font-bold text-cosmic-text">{s.value}</p>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        <TabsContent value="users">
          <Card className="bg-cosmic-card border-0 shadow-soft">
            <CardContent className="p-4">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Name</TableHead>
                    <TableHead>Email</TableHead>
                    <TableHead>Role</TableHead>
                    <TableHead>Status</TableHead>
                    <TableHead>Actions</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {users.map((u) => (
                    <TableRow key={u.id}>
                      <TableCell className="font-medium text-cosmic-text">{u.name}</TableCell>
                      <TableCell className="text-cosmic-text-secondary">{u.email}</TableCell>
                      <TableCell><Badge variant="outline">{u.role}</Badge></TableCell>
                      <TableCell>
                        <Badge className={u.is_active ? 'bg-green-500/20 text-green-700' : 'bg-red-500/20 text-red-400'}>
                          {u.is_active ? 'Active' : 'Inactive'}
                        </Badge>
                      </TableCell>
                      <TableCell>
                        {u.is_active && u.role !== 'admin' && (
                          <Button variant="outline" size="sm" onClick={() => deactivateUser(u.id)} className="text-red-400 hover:text-red-700">
                            Deactivate
                          </Button>
                        )}
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="orders">
          <Card className="bg-cosmic-card border-0 shadow-soft">
            <CardContent className="p-4">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Order</TableHead>
                    <TableHead>Customer</TableHead>
                    <TableHead>Total</TableHead>
                    <TableHead>Status</TableHead>
                    <TableHead>Tracking</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {orders.map((o) => (
                    <TableRow key={o.id}>
                      <TableCell className="font-medium text-cosmic-text">{o.order_number || `#${o.id}`}</TableCell>
                      <TableCell className="text-cosmic-text-secondary">{o.user_name}</TableCell>
                      <TableCell className="font-semibold text-sacred-gold">{formatPrice(o.total)}</TableCell>
                      <TableCell><Badge variant="outline">{o.status}</Badge></TableCell>
                      <TableCell>
                        {o.tracking_number ? (
                          <span className="text-sm text-cosmic-text-secondary">{o.tracking_number}</span>
                        ) : (
                          <div className="flex gap-1">
                            <Input placeholder="Tracking #" value={trackingUpdate[o.id] || ''} onChange={(e) => setTrackingUpdate((prev) => ({ ...prev, [o.id]: e.target.value }))} className="h-8 w-28 text-xs bg-cosmic-card" />
                            <Button size="sm" onClick={() => updateTracking(o.id)} className="h-8 bg-sacred-gold text-[#1a1a2e] hover:bg-sacred-gold-dark text-xs">Set</Button>
                          </div>
                        )}
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="products">
          <div className="flex justify-end mb-4">
            <Button onClick={openAddProduct} className="bg-sacred-gold text-[#1a1a2e] hover:bg-sacred-gold-dark">
              <Plus className="w-4 h-4 mr-2" />Add Product
            </Button>
          </div>
          <Card className="bg-cosmic-card border-0 shadow-soft">
            <CardContent className="p-4">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Name</TableHead>
                    <TableHead>Category</TableHead>
                    <TableHead>Price</TableHead>
                    <TableHead>Stock</TableHead>
                    <TableHead>Status</TableHead>
                    <TableHead>Actions</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {products.map((p) => (
                    <TableRow key={p.id}>
                      <TableCell className="font-medium text-cosmic-text">
                        <div className="flex items-center gap-2">
                          {p.image_url && (
                            <img src={p.image_url} alt={p.name} className="w-8 h-8 rounded object-cover border border-sacred-gold/20" />
                          )}
                          {p.name}
                        </div>
                      </TableCell>
                      <TableCell className="text-cosmic-text-secondary capitalize">{p.category}</TableCell>
                      <TableCell className="text-sacred-gold font-semibold">{formatPrice(p.price)}</TableCell>
                      <TableCell>{p.stock}</TableCell>
                      <TableCell>
                        <Badge className={p.is_active ? 'bg-green-500/20 text-green-700' : 'bg-cosmic-surface text-cosmic-text-secondary'}>
                          {p.is_active ? 'Active' : 'Hidden'}
                        </Badge>
                      </TableCell>
                      <TableCell>
                        <div className="flex items-center gap-1">
                          <Button variant="outline" size="sm" onClick={() => toggleProduct(p.id, p.is_active)} className="text-xs">
                            {p.is_active ? 'Hide' : 'Show'}
                          </Button>
                          <Button variant="outline" size="sm" onClick={() => openEditProduct(p)} className="text-sacred-gold hover:text-sacred-gold border-sacred-gold/30 hover:border-sacred-gold/60">
                            <Pencil className="w-3.5 h-3.5" />
                          </Button>
                          <Button variant="outline" size="sm" onClick={() => deleteProduct(p.id)} className="text-red-400 hover:text-red-600 border-red-400/30 hover:border-red-400/60">
                            <Trash2 className="w-3.5 h-3.5" />
                          </Button>
                        </div>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </CardContent>
          </Card>

          <Dialog open={productDialogOpen} onOpenChange={(open) => { setProductDialogOpen(open); if (!open) { setEditingProduct(null); setProductForm({ ...emptyProductForm }); } }}>
            <DialogContent className="sm:max-w-2xl bg-cosmic-card border-sacred-gold/20">
              <DialogHeader>
                <DialogTitle className="text-cosmic-text font-display">
                  {editingProduct ? 'Edit Product' : 'Add New Product'}
                </DialogTitle>
              </DialogHeader>
              <div className="space-y-3 py-2 max-h-[65vh] overflow-y-auto pr-1">
                <div className="grid grid-cols-2 gap-3">
                  <div className="col-span-2">
                    <label className="text-xs text-cosmic-text-secondary mb-1 block">Name *</label>
                    <Input
                      placeholder="Product name"
                      value={productForm.name}
                      onChange={(e) => setProductForm({ ...productForm, name: e.target.value })}
                      className="bg-cosmic-surface border-sacred-gold/15 text-cosmic-text"
                    />
                  </div>
                  <div className="col-span-2">
                    <label className="text-xs text-cosmic-text-secondary mb-1 block">Description</label>
                    <Textarea
                      placeholder="Product description"
                      value={productForm.description}
                      onChange={(e) => setProductForm({ ...productForm, description: e.target.value })}
                      className="bg-cosmic-surface border-sacred-gold/15 text-cosmic-text min-h-20"
                    />
                  </div>
                  <div>
                    <label className="text-xs text-cosmic-text-secondary mb-1 block">Category *</label>
                    <Select value={productForm.category} onValueChange={(v) => setProductForm({ ...productForm, category: v })}>
                      <SelectTrigger className="w-full bg-cosmic-surface border-sacred-gold/15 text-cosmic-text">
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        {PRODUCT_CATEGORIES.map((cat) => (
                          <SelectItem key={cat.value} value={cat.value}>{cat.label}</SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>
                  <div>
                    <label className="text-xs text-cosmic-text-secondary mb-1 block">Stock *</label>
                    <Input
                      type="number"
                      min="0"
                      placeholder="0"
                      value={productForm.stock}
                      onChange={(e) => setProductForm({ ...productForm, stock: e.target.value })}
                      className="bg-cosmic-surface border-sacred-gold/15 text-cosmic-text"
                    />
                  </div>
                  <div>
                    <label className="text-xs text-cosmic-text-secondary mb-1 block">Price (₹) *</label>
                    <Input
                      type="number"
                      min="0"
                      step="0.01"
                      placeholder="0.00"
                      value={productForm.price}
                      onChange={(e) => setProductForm({ ...productForm, price: e.target.value })}
                      className="bg-cosmic-surface border-sacred-gold/15 text-cosmic-text"
                    />
                  </div>
                  <div>
                    <label className="text-xs text-cosmic-text-secondary mb-1 block">Compare Price (₹)</label>
                    <Input
                      type="number"
                      min="0"
                      step="0.01"
                      placeholder="Optional MRP"
                      value={productForm.compare_price}
                      onChange={(e) => setProductForm({ ...productForm, compare_price: e.target.value })}
                      className="bg-cosmic-surface border-sacred-gold/15 text-cosmic-text"
                    />
                  </div>
                  <div>
                    <label className="text-xs text-cosmic-text-secondary mb-1 block">Planet</label>
                    <Input
                      placeholder="e.g. Sun, Moon, Saturn"
                      value={productForm.planet}
                      onChange={(e) => setProductForm({ ...productForm, planet: e.target.value })}
                      className="bg-cosmic-surface border-sacred-gold/15 text-cosmic-text"
                    />
                  </div>
                  <div>
                    <label className="text-xs text-cosmic-text-secondary mb-1 block">Weight</label>
                    <Input
                      placeholder="e.g. 10g, 5 carats"
                      value={productForm.weight}
                      onChange={(e) => setProductForm({ ...productForm, weight: e.target.value })}
                      className="bg-cosmic-surface border-sacred-gold/15 text-cosmic-text"
                    />
                  </div>
                  <div className="col-span-2">
                    <label className="text-xs text-cosmic-text-secondary mb-1 block">Product Image</label>
                    <div className="flex items-center gap-3">
                      <label className="cursor-pointer">
                        <input
                          type="file"
                          accept="image/*"
                          className="hidden"
                          onChange={(e) => { const f = e.target.files?.[0]; if (f) handleImageUpload(f); }}
                        />
                        <div className="flex items-center gap-2 px-3 py-2 rounded-md border border-sacred-gold/30 bg-cosmic-surface hover:border-sacred-gold/60 transition-colors text-sm text-cosmic-text-secondary hover:text-cosmic-text">
                          {imageUploading ? <Loader2 className="w-4 h-4 animate-spin text-sacred-gold" /> : <ImageIcon className="w-4 h-4 text-sacred-gold" />}
                          {imageUploading ? 'Uploading…' : 'Upload Image'}
                        </div>
                      </label>
                      {productForm.image_url && (
                        <div className="flex items-center gap-2">
                          <img src={productForm.image_url} alt="Preview" className="w-14 h-14 rounded-lg object-cover border border-sacred-gold/30" />
                          <button
                            type="button"
                            onClick={() => setProductForm({ ...productForm, image_url: '' })}
                            className="text-xs text-red-400 hover:text-red-600"
                          >
                            Remove
                          </button>
                        </div>
                      )}
                    </div>
                    {productForm.image_url && !productForm.image_url.startsWith('blob') && (
                      <p className="text-xs text-cosmic-text-muted mt-1 truncate">{productForm.image_url}</p>
                    )}
                  </div>
                </div>
              </div>
              <DialogFooter>
                <Button variant="outline" onClick={() => setProductDialogOpen(false)} className="border-sacred-gold/20">Cancel</Button>
                <Button
                  onClick={saveProduct}
                  disabled={!productForm.name || !productForm.price || !productForm.stock || productSaving || imageUploading}
                  className="bg-sacred-gold text-[#1a1a2e] hover:bg-sacred-gold-dark"
                >
                  {productSaving ? <Loader2 className="w-4 h-4 animate-spin mr-2" /> : null}
                  {editingProduct ? 'Save Changes' : 'Create Product'}
                </Button>
              </DialogFooter>
            </DialogContent>
          </Dialog>
        </TabsContent>

        <TabsContent value="content">
          <div className="flex justify-end mb-4">
            <Button onClick={() => setContentDialogOpen(true)} className="bg-sacred-gold text-[#1a1a2e] hover:bg-sacred-gold-dark">
              <Plus className="w-4 h-4 mr-2" />Add Content
            </Button>
          </div>
          <Card className="bg-cosmic-card border-0 shadow-soft">
            <CardContent className="p-4">
              {content.length === 0 ? (
                <div className="text-center py-8 text-cosmic-text-secondary">
                  <FileText className="w-10 h-10 mx-auto mb-2 text-cosmic-text-muted" />
                  No content items yet.
                </div>
              ) : (
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Title</TableHead>
                      <TableHead>Category</TableHead>
                      <TableHead>Status</TableHead>
                      <TableHead>Created</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {content.map((c) => (
                      <TableRow key={c.id}>
                        <TableCell className="font-medium text-cosmic-text">{c.title}</TableCell>
                        <TableCell><Badge variant="outline">{c.category}</Badge></TableCell>
                        <TableCell><Badge variant="outline">{c.status}</Badge></TableCell>
                        <TableCell className="text-sm text-cosmic-text-secondary">{new Date(c.created_at).toLocaleDateString()}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              )}
            </CardContent>
          </Card>
          <Dialog open={contentDialogOpen} onOpenChange={setContentDialogOpen}>
              <DialogContent className="sm:max-w-lg">
                <DialogHeader>
                  <DialogTitle>Add New Content</DialogTitle>
                </DialogHeader>
                <div className="space-y-3 py-2">
                  <Input placeholder="Title" value={newContent.title} onChange={(e) => setNewContent({ ...newContent, title: e.target.value })} className="bg-cosmic-card border-sacred-gold/15" />
                <Select value={newContent.category} onValueChange={(v) => setNewContent({ ...newContent, category: v })}>
                  <SelectTrigger className="w-full bg-cosmic-card border-sacred-gold/15">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    {contentCategories.map((category) => (
                      <SelectItem key={category.value} value={category.value}>
                        {category.label}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
                <Textarea placeholder="Content" value={newContent.content} onChange={(e) => setNewContent({ ...newContent, content: e.target.value })} className="bg-cosmic-card border-sacred-gold/15 min-h-24" />
              </div>
              <DialogFooter>
                <Button variant="outline" onClick={() => setContentDialogOpen(false)}>Cancel</Button>
                <Button onClick={addContent} disabled={!newContent.title || !newContent.content} className="bg-sacred-gold text-[#1a1a2e] hover:bg-sacred-gold-dark">Create</Button>
              </DialogFooter>
            </DialogContent>
          </Dialog>
        </TabsContent>

        <TabsContent value="blog">
          <div className="flex justify-end mb-4">
            <Button onClick={() => setBlogDialogOpen(true)} className="bg-sacred-gold text-[#1a1a2e] hover:bg-sacred-gold-dark">
              <Plus className="w-4 h-4 mr-2" />Add Blog Post
            </Button>
          </div>
          <Card className="bg-cosmic-card border-0 shadow-soft">
            <CardContent className="p-4">
              {blogPosts.length === 0 ? (
                <div className="text-center py-8 text-cosmic-text-secondary">
                  <FileText className="w-10 h-10 mx-auto mb-2 text-cosmic-text-muted" />
                  No blog posts yet.
                </div>
              ) : (
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Title</TableHead>
                      <TableHead>Slug</TableHead>
                      <TableHead>Author</TableHead>
                      <TableHead>Status</TableHead>
                      <TableHead>Published</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {blogPosts.map((post) => (
                      <TableRow key={post.id}>
                        <TableCell className="font-medium text-cosmic-text">{post.title}</TableCell>
                        <TableCell className="text-cosmic-text-secondary">{post.slug}</TableCell>
                        <TableCell className="text-cosmic-text-secondary">{post.author_name}</TableCell>
                        <TableCell>
                          <Badge className={post.is_published ? 'bg-green-500/20 text-green-700' : 'bg-cosmic-surface text-cosmic-text-secondary'}>
                            {post.is_published ? 'Published' : 'Draft'}
                          </Badge>
                        </TableCell>
                        <TableCell className="text-sm text-cosmic-text-secondary">{new Date(post.published_at).toLocaleDateString()}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              )}
            </CardContent>
          </Card>
          <Dialog open={blogDialogOpen} onOpenChange={setBlogDialogOpen}>
            <DialogContent className="sm:max-w-2xl">
              <DialogHeader>
                <DialogTitle>Add Blog Post</DialogTitle>
              </DialogHeader>
              <div className="space-y-3 py-2">
                <Input placeholder="Title" value={newBlogPost.title} onChange={(e) => setNewBlogPost({ ...newBlogPost, title: e.target.value })} className="bg-cosmic-card border-sacred-gold/15" />
                <Input placeholder="Excerpt" value={newBlogPost.excerpt} onChange={(e) => setNewBlogPost({ ...newBlogPost, excerpt: e.target.value })} className="bg-cosmic-card border-sacred-gold/15" />
                <Input placeholder="Author" value={newBlogPost.author_name} onChange={(e) => setNewBlogPost({ ...newBlogPost, author_name: e.target.value })} className="bg-cosmic-card border-sacred-gold/15" />
                <Input placeholder="Tags (comma separated)" value={newBlogPost.tags} onChange={(e) => setNewBlogPost({ ...newBlogPost, tags: e.target.value })} className="bg-cosmic-card border-sacred-gold/15" />
                <Textarea placeholder="Article content" value={newBlogPost.content} onChange={(e) => setNewBlogPost({ ...newBlogPost, content: e.target.value })} className="bg-cosmic-card border-sacred-gold/15 min-h-40" />
              </div>
              <DialogFooter>
                <Button variant="outline" onClick={() => setBlogDialogOpen(false)}>Cancel</Button>
                <Button
                  onClick={addBlogPost}
                  disabled={!newBlogPost.title || !newBlogPost.excerpt || !newBlogPost.content}
                  className="bg-sacred-gold text-[#1a1a2e] hover:bg-sacred-gold-dark"
                >
                  Publish
                </Button>
              </DialogFooter>
            </DialogContent>
          </Dialog>
        </TabsContent>

        <TabsContent value="ai-logs">
          <Card className="bg-cosmic-card border-0 shadow-soft">
            <CardContent className="p-4">
              {aiLogs.length === 0 ? (
                <div className="text-center py-8 text-cosmic-text-secondary">
                  <Brain className="w-10 h-10 mx-auto mb-2 text-cosmic-text-muted" />
                  No AI logs yet.
                </div>
              ) : (
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>User</TableHead>
                      <TableHead>Question</TableHead>
                      <TableHead>Endpoint</TableHead>
                      <TableHead>Date</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {aiLogs.map((log) => (
                      <TableRow key={log.id}>
                        <TableCell className="font-medium text-cosmic-text">{log.user_name}</TableCell>
                        <TableCell className="text-cosmic-text-secondary max-w-xs truncate">{log.question}</TableCell>
                        <TableCell><Badge variant="outline" className="text-xs">{log.endpoint}</Badge></TableCell>
                        <TableCell className="text-sm text-cosmic-text-secondary">{new Date(log.created_at).toLocaleString()}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              )}
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </section>
  );
}
