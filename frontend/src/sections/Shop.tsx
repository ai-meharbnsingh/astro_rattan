import { useState, useEffect } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { ShoppingBag, Gem, Star, ShoppingCart, Loader2 } from 'lucide-react';
import { api } from '@/lib/api';
import { useAuth } from '@/hooks/useAuth';

interface Product {
  id: number;
  name: string;
  category: string;
  price: number;
  rating?: number;
  reviews?: number;
  badge?: string;
  description?: string;
  image_url?: string;
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

  const addToCart = async (id: number) => {
    if (!isAuthenticated) {
      if (!cart.includes(id)) setCart([...cart, id]);
      return;
    }
    try {
      const data = await api.post('/api/cart/add', { product_id: id, quantity: 1 });
      const items = Array.isArray(data?.items) ? data.items : [];
      setCartCount(items.reduce((total: number, item: any) => total + Number(item.quantity || 0), 0));
    } catch {
      /* keep current state */
    }
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
        if (!cancelled && items.length > 0) {
          setProducts(items);
        } else if (!cancelled) {
          setProducts(activeCategory === 'all' ? fallbackProducts : fallbackProducts.filter(p => p.category === activeCategory));
        }
      } catch {
        if (!cancelled) {
          setProducts(activeCategory === 'all' ? fallbackProducts : fallbackProducts.filter(p => p.category === activeCategory));
        }
      } finally {
        if (!cancelled) setLoading(false);
      }
    };
    fetchProducts();
    return () => { cancelled = true; };
  }, [activeCategory]);

  useEffect(() => {
    if (!isAuthenticated) {
      setCartCount(0);
      return;
    }
    let cancelled = false;
    api.get('/api/cart')
      .then((data) => {
        if (cancelled) return;
        const items = Array.isArray(data?.items) ? data.items : [];
        setCartCount(items.reduce((total: number, item: any) => total + Number(item.quantity || 0), 0));
      })
      .catch(() => {})
      .finally(() => {});
    return () => { cancelled = true; };
  }, [isAuthenticated]);

  return (
    <section id="shop" className="relative py-24 bg-sacred-cream bg-mandala">
      <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-sacred-gold/10 text-sacred-gold-dark text-sm font-medium mb-6 border border-sacred-gold/30">
            <ShoppingBag className="w-4 h-4" />Astro Shop
          </div>
          <h2 className="text-3xl sm:text-4xl lg:text-5xl font-sacred font-bold text-sacred-brown mb-4">
            Sacred<span className="text-gradient-gold"> Products</span>
          </h2>
        </div>
        <div className="flex items-center justify-between mb-8">
          <div className="flex gap-2 overflow-x-auto">
            {categories.map((cat) => (
              <button key={cat} onClick={() => setActiveCategory(cat)} className={`px-4 py-2 rounded-full text-sm font-medium transition-colors whitespace-nowrap ${activeCategory === cat ? 'bg-sacred-gold text-white shadow-sacred' : 'bg-white text-sacred-brown hover:bg-sacred-gold/10 border border-sacred-gold/30'}`}>
                {cat.charAt(0).toUpperCase() + cat.slice(1)}
              </button>
            ))}
          </div>
          <button className="relative">
            <ShoppingCart className="w-6 h-6 text-sacred-gold-dark" />
            {(isAuthenticated ? cartCount : cart.length) > 0 && <span className="absolute -top-2 -right-2 w-5 h-5 rounded-full bg-sacred-saffron text-white text-xs flex items-center justify-center">{isAuthenticated ? cartCount : cart.length}</span>}
          </button>
        </div>
        {loading ? (
          <div className="flex items-center justify-center py-20">
            <Loader2 className="w-10 h-10 text-sacred-gold animate-spin" />
          </div>
        ) : (
          <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {products.map((product) => (
              <Card key={product.id} className="group card-sacred border-0 transition-all hover:-translate-y-1">
                <CardContent className="p-0">
                  <div className="relative aspect-square bg-sacred-cream flex items-center justify-center">
                    <Gem className="w-12 h-12 text-sacred-gold" />
                    {product.badge && <Badge className="absolute top-3 left-3 bg-sacred-saffron text-white">{product.badge}</Badge>}
                  </div>
                  <div className="p-4">
                    <p className="text-xs text-sacred-text-secondary mb-1 uppercase tracking-wide">{product.category}</p>
                    <h3 className="font-sacred font-semibold text-sacred-brown mb-2">{product.name}</h3>
                    <div className="flex items-center gap-1 mb-3">
                      <Star className="w-4 h-4 text-sacred-saffron fill-sacred-saffron" />
                      <span className="text-sm text-sacred-text-secondary">{product.rating || '4.5'}</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-lg font-bold text-sacred-gold-dark">{formatPrice(product.price)}</span>
                      <Button size="sm" onClick={() => addToCart(product.id)} className="bg-sacred-gold/10 text-sacred-gold-dark hover:bg-sacred-gold hover:text-white">
                        <ShoppingCart className="w-4 h-4" />
                      </Button>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        )}
      </div>
    </section>
  );
}
