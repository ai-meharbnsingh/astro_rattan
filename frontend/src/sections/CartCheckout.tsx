import { useState, useEffect } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { ShoppingCart, Minus, Plus, Trash2, CreditCard, Truck, CheckCircle, Loader2, Package } from 'lucide-react';
import { api } from '@/lib/api';
import { useAuth } from '@/hooks/useAuth';

interface CartItem {
  id: number;
  product_id: number;
  name: string;
  price: number;
  quantity: number;
  image_url?: string;
}

interface OrderResult {
  id: number;
  order_number?: string;
  total: number;
  status: string;
  payment_url?: string;
  razorpay_key_id?: string;
  razorpay_order_id?: string;
}

type Step = 'cart' | 'shipping' | 'payment' | 'confirmation';

const formatPrice = (price: number) =>
  new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR', maximumFractionDigits: 0 }).format(price);

export default function CartCheckout() {
  const { isAuthenticated } = useAuth();
  const [items, setItems] = useState<CartItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [step, setStep] = useState<Step>('cart');
  const [placing, setPlacing] = useState(false);
  const [order, setOrder] = useState<OrderResult | null>(null);
  const [paymentMethod, setPaymentMethod] = useState('cod');
  const [address, setAddress] = useState({ name: '', line1: '', line2: '', city: '', state: '', pincode: '', phone: '' });

  const formatShippingAddress = () =>
    [address.name, address.line1, address.line2, address.city, address.state, address.pincode, address.phone]
      .map((part) => part.trim())
      .filter(Boolean)
      .join(', ');

  useEffect(() => {
    if (!isAuthenticated) { setLoading(false); return; }
    let cancelled = false;
    api.get('/api/cart').then((data) => {
      if (!cancelled) {
        const list = Array.isArray(data) ? data : data.items || [];
        setItems(list);
      }
    }).catch(() => {}).finally(() => { if (!cancelled) setLoading(false); });
    return () => { cancelled = true; };
  }, [isAuthenticated]);

  const updateQty = async (itemId: number, quantity: number) => {
    if (quantity < 1) return;
    try {
      await api.patch(`/api/cart/${itemId}`, { quantity });
      setItems((prev) => prev.map((i) => (i.id === itemId ? { ...i, quantity } : i)));
    } catch { /* keep current state */ }
  };

  const removeItem = async (itemId: number) => {
    try {
      await api.delete(`/api/cart/${itemId}`);
      setItems((prev) => prev.filter((i) => i.id !== itemId));
    } catch { /* keep current state */ }
  };

  const subtotal = items.reduce((s, i) => s + i.price * i.quantity, 0);
  const shipping = subtotal > 999 ? 0 : 99;
  const total = subtotal + shipping;

  const placeOrder = async () => {
    setPlacing(true);
    try {
      const orderData = await api.post('/api/orders', {
        shipping_address: formatShippingAddress(),
        payment_method: paymentMethod,
      });
      if (paymentMethod !== 'cod') {
        const payment = await api.post('/api/payments/initiate', {
          order_id: orderData.id,
          provider: paymentMethod,
        });
        if (paymentMethod === 'stripe' && payment.payment_url) {
          window.location.href = payment.payment_url;
          return;
        }
        setOrder({ ...orderData, ...payment });
      } else {
        setOrder(orderData);
      }
      setStep('confirmation');
      setItems([]);
    } catch {
      /* stay on payment step */
    } finally {
      setPlacing(false);
    }
  };

  if (!isAuthenticated) {
    return (
      <div className="max-w-4xl mx-auto py-24 px-4 text-center">
        <ShoppingCart className="w-16 h-16 text-cosmic-text-muted mx-auto mb-4" />
        <h2 className="text-2xl font-display font-bold text-cosmic-text mb-2">Sign in to view your cart</h2>
        <p className="text-cosmic-text-secondary">Please log in to manage your shopping cart.</p>
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

  return (
    <section className="max-w-5xl mx-auto py-24 px-4">
      <div className="text-center mb-8">
        <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-sacred-gold/10 text-sacred-gold text-sm font-medium mb-4">
          <ShoppingCart className="w-4 h-4" />Checkout
        </div>
        <h2 className="text-3xl font-display font-bold text-cosmic-text">
          Your <span className="text-gradient-indigo">Cart</span>
        </h2>
      </div>

      {/* Stepper */}
      <div className="flex items-center justify-center gap-2 mb-10">
        {(['cart', 'shipping', 'payment', 'confirmation'] as Step[]).map((s, idx) => (
          <div key={s} className="flex items-center gap-2">
            <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold ${step === s || idx < ['cart', 'shipping', 'payment', 'confirmation'].indexOf(step) ? 'bg-sacred-gold text-cosmic-bg' : 'bg-cosmic-surface text-cosmic-text-muted'}`}>
              {idx + 1}
            </div>
            <span className="hidden sm:inline text-sm text-cosmic-text-secondary capitalize">{s}</span>
            {idx < 3 && <div className="w-8 h-px bg-cosmic-surface" />}
          </div>
        ))}
      </div>

      {/* Cart Step */}
      {step === 'cart' && (
        <Card className="bg-cosmic-card border-0 shadow-soft">
          <CardContent className="p-6">
            {items.length === 0 ? (
              <div className="text-center py-12">
                <Package className="w-16 h-16 text-cosmic-text-muted mx-auto mb-4" />
                <p className="text-cosmic-text-secondary">Your cart is empty</p>
              </div>
            ) : (
              <>
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Product</TableHead>
                      <TableHead>Price</TableHead>
                      <TableHead>Quantity</TableHead>
                      <TableHead>Total</TableHead>
                      <TableHead />
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {items.map((item) => (
                      <TableRow key={item.id}>
                        <TableCell className="font-medium text-cosmic-text">{item.name}</TableCell>
                        <TableCell>{formatPrice(item.price)}</TableCell>
                        <TableCell>
                          <div className="flex items-center gap-2">
                            <Button variant="outline" size="sm" onClick={() => updateQty(item.id, item.quantity - 1)} disabled={item.quantity <= 1}>
                              <Minus className="w-3 h-3" />
                            </Button>
                            <span className="w-8 text-center">{item.quantity}</span>
                            <Button variant="outline" size="sm" onClick={() => updateQty(item.id, item.quantity + 1)}>
                              <Plus className="w-3 h-3" />
                            </Button>
                          </div>
                        </TableCell>
                        <TableCell className="font-semibold text-sacred-gold">{formatPrice(item.price * item.quantity)}</TableCell>
                        <TableCell>
                          <Button variant="ghost" size="sm" onClick={() => removeItem(item.id)} className="text-red-400 hover:text-red-700">
                            <Trash2 className="w-4 h-4" />
                          </Button>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
                <div className="mt-6 flex flex-col items-end gap-2 border-t border-sacred-gold/10 pt-4">
                  <div className="text-sm text-cosmic-text-secondary">Subtotal: {formatPrice(subtotal)}</div>
                  <div className="text-sm text-cosmic-text-secondary">Shipping: {shipping === 0 ? 'Free' : formatPrice(shipping)}</div>
                  <div className="text-lg font-bold text-cosmic-text">Total: {formatPrice(total)}</div>
                  <Button onClick={() => setStep('shipping')} className="bg-sacred-gold text-cosmic-bg hover:bg-sacred-gold-dark mt-2">
                    <Truck className="w-4 h-4 mr-2" />Proceed to Shipping
                  </Button>
                </div>
              </>
            )}
          </CardContent>
        </Card>
      )}

      {/* Shipping Step */}
      {step === 'shipping' && (
        <Card className="bg-cosmic-card border-0 shadow-soft max-w-xl mx-auto">
          <CardContent className="p-6">
            <h3 className="text-lg font-display font-semibold text-cosmic-text mb-4 flex items-center gap-2">
              <Truck className="w-5 h-5 text-sacred-gold" />Shipping Address
            </h3>
            <div className="space-y-3">
              <Input placeholder="Full Name" value={address.name} onChange={(e) => setAddress({ ...address, name: e.target.value })} className="bg-cosmic-card border-sacred-gold/15" />
              <Input placeholder="Address Line 1" value={address.line1} onChange={(e) => setAddress({ ...address, line1: e.target.value })} className="bg-cosmic-card border-sacred-gold/15" />
              <Input placeholder="Address Line 2 (optional)" value={address.line2} onChange={(e) => setAddress({ ...address, line2: e.target.value })} className="bg-cosmic-card border-sacred-gold/15" />
              <div className="grid grid-cols-2 gap-3">
                <Input placeholder="City" value={address.city} onChange={(e) => setAddress({ ...address, city: e.target.value })} className="bg-cosmic-card border-sacred-gold/15" />
                <Input placeholder="State" value={address.state} onChange={(e) => setAddress({ ...address, state: e.target.value })} className="bg-cosmic-card border-sacred-gold/15" />
              </div>
              <div className="grid grid-cols-2 gap-3">
                <Input placeholder="Pincode" value={address.pincode} onChange={(e) => setAddress({ ...address, pincode: e.target.value })} className="bg-cosmic-card border-sacred-gold/15" />
                <Input placeholder="Phone" value={address.phone} onChange={(e) => setAddress({ ...address, phone: e.target.value })} className="bg-cosmic-card border-sacred-gold/15" />
              </div>
            </div>
            <div className="flex gap-3 mt-6">
              <Button variant="outline" onClick={() => setStep('cart')}>Back</Button>
              <Button onClick={() => setStep('payment')} disabled={!address.name || !address.line1 || !address.city || !address.pincode || !address.phone} className="flex-1 bg-sacred-gold text-cosmic-bg hover:bg-sacred-gold-dark">
                <CreditCard className="w-4 h-4 mr-2" />Continue to Payment
              </Button>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Payment Step */}
      {step === 'payment' && (
        <Card className="bg-cosmic-card border-0 shadow-soft max-w-xl mx-auto">
          <CardContent className="p-6">
            <h3 className="text-lg font-display font-semibold text-cosmic-text mb-4 flex items-center gap-2">
              <CreditCard className="w-5 h-5 text-sacred-gold" />Payment Method
            </h3>
            <Select value={paymentMethod} onValueChange={setPaymentMethod}>
              <SelectTrigger className="w-full bg-cosmic-card border-sacred-gold/15">
                <SelectValue placeholder="Select payment method" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="cod">Cash on Delivery</SelectItem>
                <SelectItem value="razorpay">Razorpay</SelectItem>
                <SelectItem value="stripe">Stripe</SelectItem>
              </SelectContent>
            </Select>
            <div className="mt-6 p-4 bg-cosmic-card rounded-xl">
              <div className="flex justify-between text-sm text-cosmic-text-secondary mb-1">
                <span>Subtotal</span><span>{formatPrice(subtotal)}</span>
              </div>
              <div className="flex justify-between text-sm text-cosmic-text-secondary mb-1">
                <span>Shipping</span><span>{shipping === 0 ? 'Free' : formatPrice(shipping)}</span>
              </div>
              <div className="flex justify-between text-lg font-bold text-cosmic-text mt-2 pt-2 border-t border-sacred-gold/15">
                <span>Total</span><span className="text-sacred-gold">{formatPrice(total)}</span>
              </div>
            </div>
            <div className="flex gap-3 mt-6">
              <Button variant="outline" onClick={() => setStep('shipping')}>Back</Button>
              <Button onClick={placeOrder} disabled={placing} className="flex-1 bg-sacred-gold text-cosmic-bg hover:bg-sacred-gold-dark">
                {placing ? <><Loader2 className="w-4 h-4 mr-2 animate-spin" />Placing Order...</> : 'Place Order'}
              </Button>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Confirmation Step */}
      {step === 'confirmation' && order && (
        <Card className="bg-cosmic-card border-0 shadow-soft max-w-xl mx-auto text-center">
          <CardContent className="p-8">
            <CheckCircle className="w-16 h-16 text-green-500 mx-auto mb-4" />
            <h3 className="text-2xl font-display font-bold text-cosmic-text mb-2">Order Placed!</h3>
            <p className="text-cosmic-text-secondary mb-4">Your order has been placed successfully.</p>
            <div className="space-y-2 text-sm">
              {order.order_number && <p>Order Number: <Badge variant="outline">{order.order_number}</Badge></p>}
              <p>Total: <span className="font-bold text-sacred-gold">{formatPrice(order.total)}</span></p>
              <p>Status: <Badge className="bg-sacred-gold/10 text-sacred-gold">{order.status}</Badge></p>
              {order.razorpay_key_id && (
                <div className="mt-4 p-3 bg-cosmic-card rounded-lg text-left">
                  <p className="font-medium text-cosmic-text mb-1">Razorpay Payment</p>
                  <p className="text-xs text-cosmic-text-secondary">Key ID: {order.razorpay_key_id}</p>
                  {order.razorpay_order_id && <p className="text-xs text-cosmic-text-secondary">Order ID: {order.razorpay_order_id}</p>}
                </div>
              )}
            </div>
          </CardContent>
        </Card>
      )}
    </section>
  );
}
