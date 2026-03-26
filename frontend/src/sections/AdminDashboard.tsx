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
import { Shield, Users, Package, ShoppingCart, IndianRupee, Loader2, Brain, FileText, Plus } from 'lucide-react';
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
  category: string;
  price: number;
  stock: number;
  is_active: boolean;
}

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
  const { user } = useAuth();
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

  if (user?.role !== 'admin') {
    return (
      <div className="max-w-4xl mx-auto py-24 px-4 text-center">
        <Shield className="w-16 h-16 text-minimal-gray-300 mx-auto mb-4" />
        <h2 className="text-2xl font-display font-bold text-minimal-gray-900 mb-2">Admin Access Required</h2>
        <p className="text-minimal-gray-500">You need admin privileges to view this page.</p>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center py-32">
        <Loader2 className="w-10 h-10 text-minimal-indigo animate-spin" />
      </div>
    );
  }

  const statCards = [
    { label: 'Total Users', value: stats?.total_users ?? 0, icon: Users, color: 'bg-blue-100 text-blue-600' },
    { label: 'Total Orders', value: stats?.total_orders ?? 0, icon: ShoppingCart, color: 'bg-green-100 text-green-600' },
    { label: 'Revenue', value: formatPrice(stats?.total_revenue ?? 0), icon: IndianRupee, color: 'bg-purple-100 text-purple-600' },
    { label: 'Pending', value: stats?.pending_orders ?? 0, icon: Package, color: 'bg-yellow-100 text-yellow-600' },
  ];

  return (
    <section className="max-w-7xl mx-auto py-24 px-4">
      <div className="flex items-center gap-3 mb-8">
        <div className="w-10 h-10 rounded-full bg-minimal-indigo flex items-center justify-center">
          <Shield className="w-5 h-5 text-white" />
        </div>
        <div>
          <h2 className="text-2xl font-display font-bold text-minimal-gray-900">Admin Dashboard</h2>
          <p className="text-sm text-minimal-gray-500">Manage users, orders, products, and content</p>
        </div>
      </div>

      <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
        <TabsList className="bg-minimal-gray-100 mb-6 flex-wrap">
          <TabsTrigger value="overview" className="data-[state=active]:bg-minimal-indigo data-[state=active]:text-white">Overview</TabsTrigger>
          <TabsTrigger value="users" className="data-[state=active]:bg-minimal-indigo data-[state=active]:text-white">Users</TabsTrigger>
          <TabsTrigger value="orders" className="data-[state=active]:bg-minimal-indigo data-[state=active]:text-white">Orders</TabsTrigger>
          <TabsTrigger value="products" className="data-[state=active]:bg-minimal-indigo data-[state=active]:text-white">Products</TabsTrigger>
          <TabsTrigger value="content" className="data-[state=active]:bg-minimal-indigo data-[state=active]:text-white">Content</TabsTrigger>
          <TabsTrigger value="blog" className="data-[state=active]:bg-minimal-indigo data-[state=active]:text-white">Blog</TabsTrigger>
          <TabsTrigger value="ai-logs" className="data-[state=active]:bg-minimal-indigo data-[state=active]:text-white">AI Logs</TabsTrigger>
        </TabsList>

        <TabsContent value="overview">
          <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4">
            {statCards.map((s) => (
              <Card key={s.label} className="bg-white border-0 shadow-soft">
                <CardContent className="p-5 flex items-center gap-4">
                  <div className={`w-12 h-12 rounded-xl flex items-center justify-center ${s.color}`}>
                    <s.icon className="w-6 h-6" />
                  </div>
                  <div>
                    <p className="text-sm text-minimal-gray-500">{s.label}</p>
                    <p className="text-2xl font-bold text-minimal-gray-900">{s.value}</p>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        <TabsContent value="users">
          <Card className="bg-white border-0 shadow-soft">
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
                      <TableCell className="font-medium text-minimal-gray-900">{u.name}</TableCell>
                      <TableCell className="text-minimal-gray-500">{u.email}</TableCell>
                      <TableCell><Badge variant="outline">{u.role}</Badge></TableCell>
                      <TableCell>
                        <Badge className={u.is_active ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-600'}>
                          {u.is_active ? 'Active' : 'Inactive'}
                        </Badge>
                      </TableCell>
                      <TableCell>
                        {u.is_active && u.role !== 'admin' && (
                          <Button variant="outline" size="sm" onClick={() => deactivateUser(u.id)} className="text-red-500 hover:text-red-700">
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
          <Card className="bg-white border-0 shadow-soft">
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
                      <TableCell className="font-medium text-minimal-gray-900">{o.order_number || `#${o.id}`}</TableCell>
                      <TableCell className="text-minimal-gray-500">{o.user_name}</TableCell>
                      <TableCell className="font-semibold text-minimal-indigo">{formatPrice(o.total)}</TableCell>
                      <TableCell><Badge variant="outline">{o.status}</Badge></TableCell>
                      <TableCell>
                        {o.tracking_number ? (
                          <span className="text-sm text-minimal-gray-600">{o.tracking_number}</span>
                        ) : (
                          <div className="flex gap-1">
                            <Input placeholder="Tracking #" value={trackingUpdate[o.id] || ''} onChange={(e) => setTrackingUpdate((prev) => ({ ...prev, [o.id]: e.target.value }))} className="h-8 w-28 text-xs bg-minimal-gray-50" />
                            <Button size="sm" onClick={() => updateTracking(o.id)} className="h-8 bg-minimal-indigo text-white hover:bg-minimal-violet text-xs">Set</Button>
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
          <Card className="bg-white border-0 shadow-soft">
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
                      <TableCell className="font-medium text-minimal-gray-900">{p.name}</TableCell>
                      <TableCell className="text-minimal-gray-500 capitalize">{p.category}</TableCell>
                      <TableCell className="text-minimal-indigo font-semibold">{formatPrice(p.price)}</TableCell>
                      <TableCell>{p.stock}</TableCell>
                      <TableCell>
                        <Badge className={p.is_active ? 'bg-green-100 text-green-700' : 'bg-minimal-gray-100 text-minimal-gray-500'}>
                          {p.is_active ? 'Active' : 'Hidden'}
                        </Badge>
                      </TableCell>
                      <TableCell>
                        <Button variant="outline" size="sm" onClick={() => toggleProduct(p.id, p.is_active)}>
                          {p.is_active ? 'Hide' : 'Show'}
                        </Button>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="content">
          <div className="flex justify-end mb-4">
            <Button onClick={() => setContentDialogOpen(true)} className="bg-minimal-indigo text-white hover:bg-minimal-violet">
              <Plus className="w-4 h-4 mr-2" />Add Content
            </Button>
          </div>
          <Card className="bg-white border-0 shadow-soft">
            <CardContent className="p-4">
              {content.length === 0 ? (
                <div className="text-center py-8 text-minimal-gray-500">
                  <FileText className="w-10 h-10 mx-auto mb-2 text-minimal-gray-300" />
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
                        <TableCell className="font-medium text-minimal-gray-900">{c.title}</TableCell>
                        <TableCell><Badge variant="outline">{c.category}</Badge></TableCell>
                        <TableCell><Badge variant="outline">{c.status}</Badge></TableCell>
                        <TableCell className="text-sm text-minimal-gray-500">{new Date(c.created_at).toLocaleDateString()}</TableCell>
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
                  <Input placeholder="Title" value={newContent.title} onChange={(e) => setNewContent({ ...newContent, title: e.target.value })} className="bg-minimal-gray-50 border-minimal-gray-200" />
                <Select value={newContent.category} onValueChange={(v) => setNewContent({ ...newContent, category: v })}>
                  <SelectTrigger className="w-full bg-minimal-gray-50 border-minimal-gray-200">
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
                <Textarea placeholder="Content" value={newContent.content} onChange={(e) => setNewContent({ ...newContent, content: e.target.value })} className="bg-minimal-gray-50 border-minimal-gray-200 min-h-24" />
              </div>
              <DialogFooter>
                <Button variant="outline" onClick={() => setContentDialogOpen(false)}>Cancel</Button>
                <Button onClick={addContent} disabled={!newContent.title || !newContent.content} className="bg-minimal-indigo text-white hover:bg-minimal-violet">Create</Button>
              </DialogFooter>
            </DialogContent>
          </Dialog>
        </TabsContent>

        <TabsContent value="blog">
          <div className="flex justify-end mb-4">
            <Button onClick={() => setBlogDialogOpen(true)} className="bg-minimal-indigo text-white hover:bg-minimal-violet">
              <Plus className="w-4 h-4 mr-2" />Add Blog Post
            </Button>
          </div>
          <Card className="bg-white border-0 shadow-soft">
            <CardContent className="p-4">
              {blogPosts.length === 0 ? (
                <div className="text-center py-8 text-minimal-gray-500">
                  <FileText className="w-10 h-10 mx-auto mb-2 text-minimal-gray-300" />
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
                        <TableCell className="font-medium text-minimal-gray-900">{post.title}</TableCell>
                        <TableCell className="text-minimal-gray-500">{post.slug}</TableCell>
                        <TableCell className="text-minimal-gray-500">{post.author_name}</TableCell>
                        <TableCell>
                          <Badge className={post.is_published ? 'bg-green-100 text-green-700' : 'bg-minimal-gray-100 text-minimal-gray-500'}>
                            {post.is_published ? 'Published' : 'Draft'}
                          </Badge>
                        </TableCell>
                        <TableCell className="text-sm text-minimal-gray-500">{new Date(post.published_at).toLocaleDateString()}</TableCell>
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
                <Input placeholder="Title" value={newBlogPost.title} onChange={(e) => setNewBlogPost({ ...newBlogPost, title: e.target.value })} className="bg-minimal-gray-50 border-minimal-gray-200" />
                <Input placeholder="Excerpt" value={newBlogPost.excerpt} onChange={(e) => setNewBlogPost({ ...newBlogPost, excerpt: e.target.value })} className="bg-minimal-gray-50 border-minimal-gray-200" />
                <Input placeholder="Author" value={newBlogPost.author_name} onChange={(e) => setNewBlogPost({ ...newBlogPost, author_name: e.target.value })} className="bg-minimal-gray-50 border-minimal-gray-200" />
                <Input placeholder="Tags (comma separated)" value={newBlogPost.tags} onChange={(e) => setNewBlogPost({ ...newBlogPost, tags: e.target.value })} className="bg-minimal-gray-50 border-minimal-gray-200" />
                <Textarea placeholder="Article content" value={newBlogPost.content} onChange={(e) => setNewBlogPost({ ...newBlogPost, content: e.target.value })} className="bg-minimal-gray-50 border-minimal-gray-200 min-h-40" />
              </div>
              <DialogFooter>
                <Button variant="outline" onClick={() => setBlogDialogOpen(false)}>Cancel</Button>
                <Button
                  onClick={addBlogPost}
                  disabled={!newBlogPost.title || !newBlogPost.excerpt || !newBlogPost.content}
                  className="bg-minimal-indigo text-white hover:bg-minimal-violet"
                >
                  Publish
                </Button>
              </DialogFooter>
            </DialogContent>
          </Dialog>
        </TabsContent>

        <TabsContent value="ai-logs">
          <Card className="bg-white border-0 shadow-soft">
            <CardContent className="p-4">
              {aiLogs.length === 0 ? (
                <div className="text-center py-8 text-minimal-gray-500">
                  <Brain className="w-10 h-10 mx-auto mb-2 text-minimal-gray-300" />
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
                        <TableCell className="font-medium text-minimal-gray-900">{log.user_name}</TableCell>
                        <TableCell className="text-minimal-gray-600 max-w-xs truncate">{log.question}</TableCell>
                        <TableCell><Badge variant="outline" className="text-xs">{log.endpoint}</Badge></TableCell>
                        <TableCell className="text-sm text-minimal-gray-500">{new Date(log.created_at).toLocaleString()}</TableCell>
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
