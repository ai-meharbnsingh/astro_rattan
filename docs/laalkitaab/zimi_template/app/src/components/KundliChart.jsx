import React from 'react';
import { planets, houses } from '../utils/astroData';

const KundliChart = ({ planetaryPositions }) => {
  // Create a map of house to planets
  const housePlanets = {};
  for (let i = 1; i <= 12; i++) {
    housePlanets[i] = [];
  }
  
  if (planetaryPositions) {
    planetaryPositions.forEach(pos => {
      if (housePlanets[pos.house]) {
        housePlanets[pos.house].push(pos);
      }
    });
  }

  // Get planet display info
  const getPlanetInfo = (planetId) => {
    return planets.find(p => p.id === planetId) || { name: planetId, symbol: '●', color: '#666' };
  };

  return (
    <div className="bg-white rounded-xl shadow-lg p-6">
      <h3 className="text-xl font-bold text-gray-800 mb-4 text-center">कुंडली चार्ट (Kundli Chart)</h3>
      
      {/* North Indian Style Kundli */}
      <div className="relative w-full max-w-lg mx-auto aspect-square">
        <svg viewBox="0 0 400 400" className="w-full h-full">
          {/* Outer square */}
          <rect x="20" y="20" width="360" height="360" fill="none" stroke="#8B4513" strokeWidth="3" />
          
          {/* Inner diamond */}
          <polygon points="200,20 380,200 200,380 20,200" fill="none" stroke="#8B4513" strokeWidth="2" />
          
          {/* Cross lines */}
          <line x1="20" y1="20" x2="380" y2="380" stroke="#8B4513" strokeWidth="1" />
          <line x1="380" y1="20" x2="20" y2="380" stroke="#8B4513" strokeWidth="1" />
          
          {/* Horizontal and vertical center lines */}
          <line x1="20" y1="200" x2="380" y2="200" stroke="#8B4513" strokeWidth="1" />
          <line x1="200" y1="20" x2="200" y2="380" stroke="#8B4513" strokeWidth="1" />
          
          {/* House numbers and planets */}
          {/* House 1 - Center Top */}
          <text x="200" y="50" textAnchor="middle" className="text-sm font-bold fill-orange-600">1</text>
          <foreignObject x="170" y="60" width="60" height="60">
            <div className="flex flex-wrap justify-center gap-1">
              {housePlanets[1].map((pos, idx) => {
                const planet = getPlanetInfo(pos.planet);
                return (
                  <span key={idx} style={{ color: planet.color }} className="text-lg font-bold" title={planet.name}>
                    {planet.symbol}
                  </span>
                );
              })}
            </div>
          </foreignObject>
          
          {/* House 2 - Top Right */}
          <text x="320" y="80" textAnchor="middle" className="text-sm font-bold fill-orange-600">2</text>
          <foreignObject x="290" y="90" width="60" height="60">
            <div className="flex flex-wrap justify-center gap-1">
              {housePlanets[2].map((pos, idx) => {
                const planet = getPlanetInfo(pos.planet);
                return (
                  <span key={idx} style={{ color: planet.color }} className="text-lg font-bold" title={planet.name}>
                    {planet.symbol}
                  </span>
                );
              })}
            </div>
          </foreignObject>
          
          {/* House 3 - Right Top */}
          <text x="350" y="170" textAnchor="middle" className="text-sm font-bold fill-orange-600">3</text>
          <foreignObject x="320" y="180" width="60" height="60">
            <div className="flex flex-wrap justify-center gap-1">
              {housePlanets[3].map((pos, idx) => {
                const planet = getPlanetInfo(pos.planet);
                return (
                  <span key={idx} style={{ color: planet.color }} className="text-lg font-bold" title={planet.name}>
                    {planet.symbol}
                  </span>
                );
              })}
            </div>
          </foreignObject>
          
          {/* House 4 - Right Center */}
          <text x="350" y="200" textAnchor="middle" className="text-sm font-bold fill-orange-600">4</text>
          <foreignObject x="320" y="210" width="60" height="60">
            <div className="flex flex-wrap justify-center gap-1">
              {housePlanets[4].map((pos, idx) => {
                const planet = getPlanetInfo(pos.planet);
                return (
                  <span key={idx} style={{ color: planet.color }} className="text-lg font-bold" title={planet.name}>
                    {planet.symbol}
                  </span>
                );
              })}
            </div>
          </foreignObject>
          
          {/* House 5 - Right Bottom */}
          <text x="350" y="270" textAnchor="middle" className="text-sm font-bold fill-orange-600">5</text>
          <foreignObject x="320" y="280" width="60" height="60">
            <div className="flex flex-wrap justify-center gap-1">
              {housePlanets[5].map((pos, idx) => {
                const planet = getPlanetInfo(pos.planet);
                return (
                  <span key={idx} style={{ color: planet.color }} className="text-lg font-bold" title={planet.name}>
                    {planet.symbol}
                  </span>
                );
              })}
            </div>
          </foreignObject>
          
          {/* House 6 - Bottom Right */}
          <text x="320" y="350" textAnchor="middle" className="text-sm font-bold fill-orange-600">6</text>
          <foreignObject x="290" y="320" width="60" height="60">
            <div className="flex flex-wrap justify-center gap-1">
              {housePlanets[6].map((pos, idx) => {
                const planet = getPlanetInfo(pos.planet);
                return (
                  <span key={idx} style={{ color: planet.color }} className="text-lg font-bold" title={planet.name}>
                    {planet.symbol}
                  </span>
                );
              })}
            </div>
          </foreignObject>
          
          {/* House 7 - Center Bottom */}
          <text x="200" y="370" textAnchor="middle" className="text-sm font-bold fill-orange-600">7</text>
          <foreignObject x="170" y="300" width="60" height="60">
            <div className="flex flex-wrap justify-center gap-1">
              {housePlanets[7].map((pos, idx) => {
                const planet = getPlanetInfo(pos.planet);
                return (
                  <span key={idx} style={{ color: planet.color }} className="text-lg font-bold" title={planet.name}>
                    {planet.symbol}
                  </span>
                );
              })}
            </div>
          </foreignObject>
          
          {/* House 8 - Bottom Left */}
          <text x="80" y="350" textAnchor="middle" className="text-sm font-bold fill-orange-600">8</text>
          <foreignObject x="50" y="320" width="60" height="60">
            <div className="flex flex-wrap justify-center gap-1">
              {housePlanets[8].map((pos, idx) => {
                const planet = getPlanetInfo(pos.planet);
                return (
                  <span key={idx} style={{ color: planet.color }} className="text-lg font-bold" title={planet.name}>
                    {planet.symbol}
                  </span>
                );
              })}
            </div>
          </foreignObject>
          
          {/* House 9 - Left Bottom */}
          <text x="50" y="270" textAnchor="middle" className="text-sm font-bold fill-orange-600">9</text>
          <foreignObject x="20" y="280" width="60" height="60">
            <div className="flex flex-wrap justify-center gap-1">
              {housePlanets[9].map((pos, idx) => {
                const planet = getPlanetInfo(pos.planet);
                return (
                  <span key={idx} style={{ color: planet.color }} className="text-lg font-bold" title={planet.name}>
                    {planet.symbol}
                  </span>
                );
              })}
            </div>
          </foreignObject>
          
          {/* House 10 - Left Center */}
          <text x="50" y="200" textAnchor="middle" className="text-sm font-bold fill-orange-600">10</text>
          <foreignObject x="20" y="210" width="60" height="60">
            <div className="flex flex-wrap justify-center gap-1">
              {housePlanets[10].map((pos, idx) => {
                const planet = getPlanetInfo(pos.planet);
                return (
                  <span key={idx} style={{ color: planet.color }} className="text-lg font-bold" title={planet.name}>
                    {planet.symbol}
                  </span>
                );
              })}
            </div>
          </foreignObject>
          
          {/* House 11 - Left Top */}
          <text x="50" y="130" textAnchor="middle" className="text-sm font-bold fill-orange-600">11</text>
          <foreignObject x="20" y="140" width="60" height="60">
            <div className="flex flex-wrap justify-center gap-1">
              {housePlanets[11].map((pos, idx) => {
                const planet = getPlanetInfo(pos.planet);
                return (
                  <span key={idx} style={{ color: planet.color }} className="text-lg font-bold" title={planet.name}>
                    {planet.symbol}
                  </span>
                );
              })}
            </div>
          </foreignObject>
          
          {/* House 12 - Top Left */}
          <text x="80" y="80" textAnchor="middle" className="text-sm font-bold fill-orange-600">12</text>
          <foreignObject x="50" y="90" width="60" height="60">
            <div className="flex flex-wrap justify-center gap-1">
              {housePlanets[12].map((pos, idx) => {
                const planet = getPlanetInfo(pos.planet);
                return (
                  <span key={idx} style={{ color: planet.color }} className="text-lg font-bold" title={planet.name}>
                    {planet.symbol}
                  </span>
                );
              })}
            </div>
          </foreignObject>
        </svg>
      </div>

      {/* Legend */}
      <div className="mt-6 grid grid-cols-3 sm:grid-cols-5 gap-2">
        {planets.map(planet => (
          <div key={planet.id} className="flex items-center space-x-2 text-sm">
            <span style={{ color: planet.color }} className="text-lg font-bold">{planet.symbol}</span>
            <span className="text-gray-700">{planet.name}</span>
          </div>
        ))}
      </div>
    </div>
  );
};

export default KundliChart;
