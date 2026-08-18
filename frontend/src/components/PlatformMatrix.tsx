import React from 'react';

interface PlatformMatrixProps {
  souls: any[];
}

export function PlatformMatrix({ souls }: PlatformMatrixProps) {
  const platforms = ['Discord', 'Twitter', 'Reddit', 'Instagram'];
  
  const platformCounts = platforms.reduce((acc, platform) => {
    acc[platform] = souls.filter(s => s.platforms?.includes(platform.toLowerCase())).length;
    return acc;
  }, {} as Record<string, number>);

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-fuchsia-300">Platform Matrix</h2>
        <p className="text-stone-400">Soul-to-platform assignment overview</p>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {platforms.map(platform => (
          <div key={platform} className="bg-stone-900 rounded-lg p-6 border border-stone-800">
            <h3 className="text-lg font-semibold text-white mb-2">{platform}</h3>
            <div className="text-3xl font-bold text-fuchsia-300">{platformCounts[platform]}</div>
            <div className="text-sm text-stone-400">souls assigned</div>
          </div>
        ))}
      </div>
      
      <div className="bg-stone-900 rounded-lg p-6 border border-stone-800">
        <h3 className="text-lg font-semibold text-white mb-4">Soul Assignments</h3>
        <div className="space-y-2">
          {souls.slice(0, 10).map(soul => (
            <div key={soul.id} className="flex items-center justify-between py-2 border-b border-stone-800 last:border-0">
              <span className="text-white">{soul.name}</span>
              <div className="flex gap-2">
                {soul.platforms?.map((platform: string) => (
                  <span
                    key={platform}
                    className="px-2 py-1 bg-stone-800 rounded text-xs text-stone-300 capitalize"
                  >
                    {platform}
                  </span>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
