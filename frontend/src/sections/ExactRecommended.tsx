import { useNavigate } from 'react-router-dom';
import { ArrowRight, Gem, Star } from 'lucide-react';

export default function ExactRecommended() {
  const navigate = useNavigate();

  return (
    <section className="py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        {/* Decorative divider */}
        <div className="flex items-center justify-center mb-8">
          <div className="h-px w-16" style={{ background: 'linear-gradient(to right, transparent, #D4A052)' }} />
          <span className="mx-3 text-[#8B6914] text-sm font-serif tracking-widest uppercase">Shop</span>
          <div className="h-px w-16" style={{ background: 'linear-gradient(to left, transparent, #D4A052)' }} />
        </div>

        {/* Shop Section */}
        <div className="rounded-xl p-8 border"
             style={{ background: '#FFF8EE', borderColor: '#D4A052', boxShadow: '0 4px 14px rgba(139, 105, 20, 0.08)' }}>
          <div className="flex flex-col md:flex-row md:items-center md:justify-between mb-6">
            <div>
              <h2 className="font-serif text-3xl font-bold" style={{ color: '#3D2B1F' }}>
                Shop Astrovedic
              </h2>
              <p className="text-sm mt-1" style={{ color: '#7A6548' }}>
                Authentic gemstones, yantras, and spiritual products
              </p>
            </div>
            <button onClick={() => navigate('/shop')}
                    className="mt-4 md:mt-0 flex items-center gap-2 font-serif font-medium text-sm transition-colors"
                    style={{ color: '#8B6914' }}>
              Browse All
              <ArrowRight className="w-4 h-4" />
            </button>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            {/* Featured Gemstone */}
            <div onClick={() => navigate('/shop')}
                 className="rounded-xl p-5 border cursor-pointer transition-all duration-300 hover:-translate-y-1"
                 style={{
                   background: 'linear-gradient(135deg, #F5E6C8, #EDE0C8)',
                   borderColor: '#D4A052',
                   boxShadow: '0 2px 8px rgba(139, 105, 20, 0.08)',
                 }}
                 onMouseEnter={(e) => {
                   e.currentTarget.style.boxShadow = '0 8px 20px rgba(139, 105, 20, 0.16)';
                 }}
                 onMouseLeave={(e) => {
                   e.currentTarget.style.boxShadow = '0 2px 8px rgba(139, 105, 20, 0.08)';
                 }}>
              <div className="w-16 h-16 rounded-full mx-auto mb-3 flex items-center justify-center"
                   style={{ background: 'linear-gradient(135deg, #D4A052, #B8860B)', border: '2px solid #8B6914' }}>
                <Gem className="w-8 h-8 text-white" />
              </div>
              <div className="flex items-center justify-center gap-0.5 mb-2">
                {[...Array(5)].map((_, i) => (
                  <Star key={i} className="w-3 h-3 fill-current" style={{ color: '#D4A052' }} />
                ))}
              </div>
              <h4 className="font-serif font-bold text-center text-sm" style={{ color: '#3D2B1F' }}>Gemstone Order</h4>
              <p className="text-xs text-center" style={{ color: '#7A6548' }}>Frame Solitaire</p>
            </div>

            {/* Category links */}
            {['Gemstones', 'Rudraksha', 'Yantras'].map((category) => (
              <button key={category}
                      onClick={() => navigate('/shop')}
                      className="flex items-center justify-between p-5 rounded-xl border
                                 transition-all duration-200 hover:-translate-y-0.5 text-left"
                      style={{
                        background: '#FFF8EE',
                        borderColor: '#D4A052',
                        boxShadow: '0 2px 6px rgba(139, 105, 20, 0.06)',
                      }}
                      onMouseEnter={(e) => {
                        e.currentTarget.style.boxShadow = '0 6px 16px rgba(139, 105, 20, 0.14)';
                      }}
                      onMouseLeave={(e) => {
                        e.currentTarget.style.boxShadow = '0 2px 6px rgba(139, 105, 20, 0.06)';
                      }}>
                <div>
                  <span className="font-serif font-semibold text-sm" style={{ color: '#3D2B1F' }}>{category}</span>
                  <p className="text-xs mt-0.5" style={{ color: '#7A6548' }}>Explore collection</p>
                </div>
                <ArrowRight className="w-4 h-4 flex-shrink-0" style={{ color: '#8B6914' }} />
              </button>
            ))}
          </div>

          {/* Bottom CTA */}
          <div className="text-center mt-8">
            <button onClick={() => navigate('/shop')}
                    className="inline-flex items-center gap-2 px-8 py-3 rounded-full text-white font-serif font-medium
                             transition-all duration-200 hover:shadow-lg hover:-translate-y-0.5"
                    style={{ background: 'linear-gradient(to right, #D4A052, #B8860B)', boxShadow: '0 4px 12px rgba(139, 105, 20, 0.2)' }}>
              Browse All Products
              <ArrowRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>
    </section>
  );
}
