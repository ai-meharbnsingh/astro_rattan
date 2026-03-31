import { categoryTabs } from '../config';
import { useState } from 'react';

export default function CategoryTabs() {
  const [activeTab, setActiveTab] = useState('numerology');

  return (
    <section className="py-4 px-4">
      <div className="max-w-6xl mx-auto">
        <div className="vedic-card py-3 px-4">
          <div className="flex items-center justify-center flex-wrap gap-2 md:gap-4">
            {categoryTabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`vedic-tab ${activeTab === tab.id ? 'active' : ''}`}
              >
                <span className="text-lg">{tab.icon}</span>
                <span className="flex flex-col items-start">
                  <span>{tab.label}</span>
                  {tab.sublabel && (
                    <span className="text-[10px] opacity-70 -mt-1">{tab.sublabel}</span>
                  )}
                </span>
              </button>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
