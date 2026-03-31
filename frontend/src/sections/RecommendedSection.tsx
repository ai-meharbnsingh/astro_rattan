import { recommendedSection } from '../config';

export default function RecommendedSection() {
  return (
    <section className="py-6 px-4">
      <div className="max-w-6xl mx-auto">
        {/* Bottom Categories */}
        <div className="vedic-card p-4">
          <div className="grid grid-cols-4 gap-4">
            {recommendedSection.bottomCategories.map((cat) => (
              <div key={cat.id} className="flex flex-col items-center">
                <div className="w-14 h-14 rounded-xl overflow-hidden border-2 border-amber-300 shadow-md mb-2 hover:scale-110 transition-transform cursor-pointer">
                  <img
                    src={cat.icon}
                    alt={cat.label}
                    className="w-full h-full object-cover"
                  />
                </div>
                <span className="text-xs text-amber-800 text-center font-medium">
                  {cat.label}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
