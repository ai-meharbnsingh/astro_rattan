import { useState, useEffect } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { ShoppingBag, Gem, Star, ShoppingCart, Loader2, Package, Sparkles } from 'lucide-react';
import { api } from '@/lib/api';
import { useAuth } from '@/hooks/useAuth';

interface Product { id: number; name: string; category: string; price: number; rating?: number; reviews?: number; badge?: string; description?: string; image_url?: string; }

interface BundleItem { product_id: number; product_name: string; quantity: number; }
interface Bundle {
  id: number;
  name: string;
  description: string;
  items: BundleItem[];
  original_price: number;
  discounted_price: number;
  savings_percentage: number;
}

const fallbackProducts: Product[] = [
  { id: 1, name: 'Yellow Sapphire', category: 'gemstone', price: 12999, rating: 4.8, reviews: 234, badge: 'Bestseller' },
  { id: 2, name: 'Blue Sapphire', category: 'gemstone', price: 18999, rating: 4.9, reviews: 189, badge: 'Premium' },
  { id: 3, name: 'Rudraksha Mala', category: 'rudraksha', price: 1299, rating: 4.7, reviews: 567, badge: 'Popular' },
  { id: 4, name: 'Navratna Bracelet', category: 'bracelet', price: 3499, rating: 4.6, reviews: 312, badge: 'New' },
];

const categories = ['all', 'gemstone', 'rudraksha', 'bracelet', 'yantra', 'vastu'];

export default function Shop() {
  const { isAuthenticated } = useAuth();
  const [products, setProducts] = useState<Product[]>(fallbackProducts);
  const [cart, setCart] = useState<number[]>([]);
  const [cartCount, setCartCount] = useState(0);
  const [loading, setLoading] = useState(true);
  const [activeCategory, setActiveCategory] = useState('all');
  const [activeTab, setActiveTab] = useState<'products' | 'bundles'>('products');
  const [bundles, setBundles] = useState<Bundle[]>([]);
  const [bundlesLoading, setBundlesLoading] = useState(false);
  const [addingBundleId, setAddingBundleId] = useState<number | null>(null);

  const addToCart = async (id: number) => {
    if (!isAuthenticated) { if (!cart.includes(id)) setCart([...cart, id]); return; }
    try {
      const data = await api.post('/api/cart/add', { product_id: id, quantity: 1 });
      const items = Array.isArray(data?.items) ? data.items : [];
      setCartCount(items.reduce((total: number, item: any) => total + Number(item.quantity || 0), 0));
    } catch { /* keep current state */ }
  };

  const addBundleToCart = async (bundleId: number) => {
    setAddingBundleId(bundleId);
    try {
      const data = await api.post(`/api/cart/add-bundle/${bundleId}`, {});
      const items = Array.isArray(data?.items) ? data.items : [];
      setCartCount(items.reduce((total: number, item: any) => total + Number(item.quantity || 0), 0));
    } catch { /* keep current state */ }
    finally { setAddingBundleId(null); }
  };

  const formatPrice = (price: number) => new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR', maximumFractionDigits: 0 }).format(price);

  useEffect(() => {
    let cancelled = false;
    const fetchProducts = async () => {
      setLoading(true);
      try {
        const endpoint = activeCategory === 'all' ? '/api/products' : `/api/products?category=${activeCategory}`;
        const data = await api.get(endpoint);
        const items = Array.isArray(data) ? data : data.products || data.items || [];
        if (!cancelled && items.length > 0) setProducts(items);
        else if (!cancelled) setProducts(activeCategory === 'all' ? fallbackProducts : fallbackProducts.filter(p => p.category === activeCategory));
      } catch {
        if (!cancelled) setProducts(activeCategory === 'all' ? fallbackProducts : fallbackProducts.filter(p => p.category === activeCategory));
      } finally { if (!cancelled) setLoading(false); }
    };
    fetchProducts();
    return () => { cancelled = true; };
  }, [activeCategory]);

  useEffect(() => {
    if (!isAuthenticated) { setCartCount(0); return; }
    let cancelled = false;
    api.get('/api/cart').then((data) => {
      if (cancelled) return;
      const items = Array.isArray(data?.items) ? data.items : [];
      setCartCount(items.reduce((total: number, item: any) => total + Number(item.quantity || 0), 0));
    }).catch(() => {});
    return () => { cancelled = true; };
  }, [isAuthenticated]);

  useEffect(() => {
    if (activeTab !== 'bundles') return;
    let cancelled = false;
    const fetchBundles = async () => {
      setBundlesLoading(true);
      try {
        const data = await api.get('/api/bundles');
        const items = Array.isArray(data) ? data : data.bundles || data.items || [];
        if (!cancelled) setBundles(items);
      } catch {
        if (!cancelled) setBundles([]);
      } finally { if (!cancelled) setBundlesLoading(false); }
    };
    fetchBundles();
    return () => { cancelled = true; };
  }, [activeTab]);

  return (
    <section id="shop" className="relative py-24 bg-cosmic-bg bg-mandala">
      <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-sacred-gold/10 text-sacred-gold text-sm font-medium mb-6 border border-sacred-gold/30">
            <ShoppingBag className="w-4 h-4" />Astro Shop
          </div>
          <h2 className="text-3xl sm:text-4xl lg:text-5xl font-sacred font-bold text-cosmic-text mb-4">
            Sacred<span className="text-gradient-gold"> Products</span>
          </h2>
        </div>

        {/* Tab Switcher */}
        <div className="flex items-center justify-center gap-4 mb-8">
          <button onClick={() => setActiveTab('products')} className={`px-6 py-3 rounded-full text-sm font-medium transition-colors flex items-center gap-2 ${activeTab === 'products' ? 'bg-sacred-gold text-cosmic-bg shadow-glow-gold' : 'bg-cosmic-card text-cosmic-text-secondary hover:bg-sacred-gold/10 border border-sacred-gold/20'}`}>
            <Gem className="w-4 h-4" />Products
          </button>
          <button onClick={() => setActiveTab('bundles')} className={`px-6 py-3 rounded-full text-sm font-medium transition-colors flex items-center gap-2 ${activeTab === 'bundles' ? 'bg-sacred-gold text-cosmic-bg shadow-glow-gold' : 'bg-cosmic-card text-cosmic-text-secondary hover:bg-sacred-gold/10 border border-sacred-gold/20'}`}>
            <Package className="w-4 h-4" />Bundles
          </button>
        </div>

        {activeTab === 'products' && (
          <>
            <div className="flex items-center justify-between mb-8">
              <div className="flex gap-2 overflow-x-auto">
                {categories.map((cat) => (
                  <button key={cat} onClick={() => setActiveCategory(cat)} className={`px-4 py-2 rounded-full text-sm font-medium transition-colors whitespace-nowrap ${activeCategory === cat ? 'bg-sacred-gold text-cosmic-bg shadow-glow-gold' : 'bg-cosmic-card text-cosmic-text-secondary hover:bg-sacred-gold/10 border border-sacred-gold/20'}`}>
                    {cat.charAt(0).toUpperCase() + cat.slice(1)}
                  </button>
                ))}
              </div>
              <button className="relative">
                <ShoppingCart className="w-6 h-6 text-sacred-gold" />
                {(isAuthenticated ? cartCount : cart.length) > 0 && <span className="absolute -top-2 -right-2 w-5 h-5 rounded-full bg-sacred-saffron text-cosmic-bg text-xs flex items-center justify-center font-bold">{isAuthenticated ? cartCount : cart.length}</span>}
              </button>
            </div>
            {loading ? (
              <div className="flex items-center justify-center py-20"><Loader2 className="w-10 h-10 text-sacred-gold animate-spin" /></div>
            ) : (
              <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-6">
                {products.map((product) => (
                  <Card key={product.id} className="group card-sacred border-sacred-gold/15 hover:border-sacred-gold/40 transition-all hover:-translate-y-1">
                    <CardContent className="p-0">
                      <div className="relative aspect-square bg-cosmic-card flex items-center justify-center rounded-t-lg border-b border-sacred-gold/10">
                        <Gem className="w-12 h-12 text-sacred-gold/50" />
                        {product.badge && <Badge className="absolute top-3 left-3 bg-sacred-saffron text-cosmic-bg font-bold">{product.badge}</Badge>}
                      </div>
                      <div className="p-4">
                        <p className="text-xs text-cosmic-text-muted mb-1 uppercase tracking-wide">{product.category}</p>
                        <h3 className="font-sacred font-semibold text-cosmic-text mb-2">{product.name}</h3>
                        <div className="flex items-center gap-1 mb-3">
                          <Star className="w-4 h-4 text-sacred-saffron fill-sacred-saffron" />
                          <span className="text-sm text-cosmic-text-secondary">{product.rating || '4.5'}</span>
                        </div>
                        <div className="flex items-center justify-between">
                          <span className="text-lg font-bold text-sacred-gold">{formatPrice(product.price)}</span>
                          <Button size="sm" onClick={() => addToCart(product.id)} className="bg-sacred-gold/10 text-sacred-gold hover:bg-sacred-gold hover:text-cosmic-bg border border-sacred-gold/30">
                            <ShoppingCart className="w-4 h-4" />
                          </Button>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            )}
          </>
        )}

        {activeTab === 'bundles' && (
          <>
            <div className="flex items-center justify-end mb-8">
              <button className="relative">
                <ShoppingCart className="w-6 h-6 text-sacred-gold" />
                {(isAuthenticated ? cartCount : cart.length) > 0 && <span className="absolute -top-2 -right-2 w-5 h-5 rounded-full bg-sacred-saffron text-cosmic-bg text-xs flex items-center justify-center font-bold">{isAuthenticated ? cartCount : cart.length}</span>}
              </button>
            </div>
            {bundlesLoading ? (
              <div className="flex items-center justify-center py-20"><Loader2 className="w-10 h-10 text-sacred-gold animate-spin" /></div>
            ) : bundles.length === 0 ? (
              <div className="text-center py-20">
                <Package className="w-16 h-16 text-sacred-gold/30 mx-auto mb-4" />
                <p className="text-cosmic-text-secondary text-lg">No bundles available at the moment.</p>
              </div>
            ) : (
              <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
                {bundles.map((bundle) => (
                  <Card key={bundle.id} className="group card-sacred border-sacred-gold/20 hover:border-sacred-gold/50 transition-all hover:-translate-y-1 relative overflow-hidden">
                    <CardContent className="p-0">
                      {/* Special Offers badge */}
                      <div className="absolute top-3 right-3 z-10">
                        <Badge className="bg-gradient-to-r from-sacred-saffron to-sacred-gold text-cosmic-bg font-bold flex items-center gap-1 px-3 py-1">
                          <Sparkles className="w-3 h-3" />Special Offer
                        </Badge>
                      </div>

                      {/* Bundle header */}
                      <div className="relative bg-cosmic-card p-6 border-b border-sacred-gold/10">
                        <div className="flex items-center gap-3 mb-3">
                          <div className="w-12 h-12 rounded-xl bg-sacred-gold/10 flex items-center justify-center border border-sacred-gold/20">
                            <Package className="w-6 h-6 text-sacred-gold" />
                          </div>
                          <div>
                            <h3 className="font-sacred font-semibold text-cosmic-text text-lg">{bundle.name}</h3>
                          </div>
                        </div>
                        {bundle.description && (
                          <p className="text-sm text-cosmic-text-secondary leading-relaxed">{bundle.description}</p>
                        )}
                      </div>

                      {/* Included items */}
                      <div className="p-6">
                        <p className="text-xs text-cosmic-text-muted uppercase tracking-wide mb-3">Included Items</p>
                        <div className="space-y-2 mb-5">
                          {(bundle.items || []).map((item, idx) => (
                            <div key={idx} className="flex items-center gap-2 p-2 rounded-lg bg-cosmic-card border border-sacred-gold/10">
                              <Gem className="w-4 h-4 text-sacred-gold/60 flex-shrink-0" />
                              <span className="text-sm text-cosmic-text flex-1">{item.product_name}</span>
                              {item.quantity > 1 && <span className="text-xs text-cosmic-text-secondary">x{item.quantity}</span>}
                            </div>
                          ))}
                        </div>

                        {/* Pricing */}
                        <div className="p-4 rounded-xl bg-cosmic-card border border-sacred-gold/15 mb-4">
                          <div className="flex items-center justify-between mb-1">
                            <span className="text-sm text-cosmic-text-secondary">Original Price</span>
                            <span className="text-sm text-cosmic-text-secondary line-through">{formatPrice(bundle.original_price)}</span>
                          </div>
                          <div className="flex items-center justify-between mb-1">
                            <span className="text-sm font-medium text-cosmic-text">Bundle Price</span>
                            <span className="text-lg font-bold text-sacred-gold">{formatPrice(bundle.discounted_price)}</span>
                          </div>
                          <div className="flex items-center justify-end">
                            <span className="text-xs font-bold text-green-400 bg-green-400/10 px-2 py-0.5 rounded-full">
                              Save {bundle.savings_percentage}%
                            </span>
                          </div>
                        </div>

                        {/* Add to cart button */}
                        <Button
                          onClick={() => addBundleToCart(bundle.id)}
                          disabled={addingBundleId === bundle.id}
                          className="w-full bg-sacred-gold/10 text-sacred-gold hover:bg-sacred-gold hover:text-cosmic-bg border border-sacred-gold/30 transition-all font-medium"
                        >
                          {addingBundleId === bundle.id ? (
                            <Loader2 className="w-4 h-4 animate-spin mr-2" />
                          ) : (
                            <ShoppingCart className="w-4 h-4 mr-2" />
                          )}
                          Add Bundle to Cart
                        </Button>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            )}
          </>
        )}
      </div>
    </section>
  );
}
