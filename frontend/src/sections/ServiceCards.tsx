import { serviceCards } from '../config';
import { Star } from 'lucide-react';

export default function ServiceCards() {
  return (
    <section className="py-8 px-4">
      <div className="max-w-7xl mx-auto">
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4">
          {serviceCards.map((card, index) => (
            <div
              key={card.id}
              className="vedic-card p-4 flex flex-col items-center text-center relative group hover:scale-105 transition-transform duration-300"
              style={{ animationDelay: `${index * 100}ms` }}
            >
              {/* Corner Ornaments */}
              <div className="corner-ornament corner-ornament-tl" />
              <div className="corner-ornament corner-ornament-tr" />
              <div className="corner-ornament corner-ornament-bl" />
              <div className="corner-ornament corner-ornament-br" />
              
              {/* Icon/Image */}
              <div className="w-16 h-16 mb-3 rounded-full overflow-hidden border-2 border-amber-400 shadow-lg">
                <img
                  src={card.image}
                  alt={card.title}
                  className="w-full h-full object-cover"
                />
              </div>
              
              {/* Title */}
              <h3 className="font-serif font-semibold text-sm text-amber-900 mb-1">
                {card.title}
              </h3>
              
              {/* Subtitle */}
              {card.rating && (
                <div className="flex items-center justify-center gap-1 text-xs text-amber-700 mb-1">
                  <Star className="w-3 h-3 fill-amber-500 text-amber-500" />
                  <span>{card.rating}</span>
                  <Star className="w-3 h-3 fill-amber-500 text-amber-500" />
                </div>
              )}
              
              <p className="text-xs text-amber-700/80 mb-3 leading-tight">
                {card.subtitle}
              </p>
              
              {/* Button */}
              <button className="btn-vedic text-xs py-2 px-4 mt-auto">
                {card.buttonText}
              </button>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
