import { shopSection } from '../config';
import { Star } from 'lucide-react';

export default function ShopSection() {
  return (
    <section className="py-8 px-4">
      <div className="max-w-6xl mx-auto">
        <div className="vedic-card p-0 overflow-hidden relative">
          {/* Background Image */}
          <div className="absolute inset-0">
            <img
              src={shopSection.backgroundImage}
              alt="Temple Background"
              className="w-full h-full object-cover opacity-30"
            />
            <div className="absolute inset-0 bg-gradient-to-t from-amber-100/90 via-amber-50/80 to-amber-100/90" />
          </div>
          
          {/* Content */}
          <div className="relative z-10 p-6">
            {/* Label */}
            <p className="text-xs text-amber-600/70 text-center mb-2 tracking-widest uppercase">
              {shopSection.label}
            </p>
            
            {/* Title */}
            <h2 className="text-2xl md:text-3xl font-serif font-bold text-amber-900 text-center mb-6">
              {shopSection.title}
            </h2>
            
            {/* Star Rating Decoration */}
            <div className="flex items-center justify-center gap-1 mb-6">
              {[...Array(5)].map((_, i) => (
                <Star key={i} className="w-4 h-4 text-amber-500 fill-amber-500" />
              ))}
            </div>
            
            {/* Product Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {shopSection.products.map((product) => (
                <div
                  key={product.id}
                  className="bg-white/80 backdrop-blur-sm rounded-xl p-4 border border-amber-200 shadow-lg"
                >
                  <div className="flex items-center gap-4">
                    {/* Product Image */}
                    <div className="w-20 h-20 rounded-lg overflow-hidden border border-amber-300 flex-shrink-0">
                      <img
                        src={product.image}
                        alt={product.name}
                        className="w-full h-full object-cover"
                      />
                    </div>
                    
                    {/* Product Info */}
                    <div className="flex-1">
                      <h3 className="font-medium text-amber-900">{product.name}</h3>
                      <div className="flex items-center gap-1 mt-1">
                        {[...Array(product.rating)].map((_, i) => (
                          <Star key={i} className="w-3 h-3 text-amber-500 fill-amber-500" />
                        ))}
                      </div>
                      <p className="text-xs text-amber-600/70 mt-1">{product.reviews}</p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
