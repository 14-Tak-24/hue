import React from 'react';

interface PolarityMapProps {
  souls: any[];
  onSelectSoul: (soul: any) => void;
}

export function PolarityMap({ souls, onSelectSoul }: PolarityMapProps) {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-fuchsia-300">Polarity Map</h2>
        <p className="text-stone-400">Visualize soul positioning on polarity axes</p>
      </div>
      
      <div className="bg-stone-900 rounded-lg p-8 border border-stone-800">
        <div className="aspect-square max-w-2xl mx-auto relative bg-stone-950 rounded-lg border border-stone-700">
          {/* Axis lines */}
          <div className="absolute inset-0 flex items-center justify-center">
            <div className="w-full h-px bg-stone-700"></div>
          </div>
          <div className="absolute inset-0 flex items-center justify-center">
            <div className="h-full w-px bg-stone-700"></div>
          </div>
          
          {/* Labels */}
          <div className="absolute top-2 left-1/2 -translate-x-1/2 text-stone-400 text-sm">Light</div>
          <div className="absolute bottom-2 left-1/2 -translate-x-1/2 text-stone-400 text-sm">Shadow</div>
          <div className="absolute left-2 top-1/2 -translate-y-1/2 text-stone-400 text-sm">Chaos</div>
          <div className="absolute right-2 top-1/2 -translate-y-1/2 text-stone-400 text-sm">Order</div>
          
          {/* Soul dots */}
          {souls.slice(0, 10).map((soul, index) => {
            const x = 50 + (Math.random() - 0.5) * 80;
            const y = 50 + (Math.random() - 0.5) * 80;
            return (
              <div
                key={soul.id}
                onClick={() => onSelectSoul(soul)}
                className="absolute w-4 h-4 rounded-full bg-fuchsia-500 cursor-pointer hover:bg-fuchsia-400 transition"
                style={{ left: `${x}%`, top: `${y}%` }}
                title={soul.name}
              />
            );
          })}
        </div>
      </div>
      
      <div className="text-center text-stone-400">
        <p>Click on souls to view details</p>
      </div>
    </div>
  );
}
