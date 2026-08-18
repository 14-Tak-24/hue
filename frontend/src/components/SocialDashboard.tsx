import React from 'react';

interface SocialDashboardProps {
  souls: any[];
}

export function SocialDashboard({ souls }: SocialDashboardProps) {
  const platforms = [
    { name: 'Discord', accounts: 15, color: 'bg-indigo-500' },
    { name: 'Twitter', accounts: 20, color: 'bg-blue-500' },
    { name: 'Reddit', accounts: 10, color: 'bg-orange-500' },
    { name: 'Instagram', accounts: 8, color: 'bg-pink-500' },
  ];

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-fuchsia-300">Social Dashboard</h2>
        <p className="text-stone-400">Multi-platform social media management</p>
      </div>
      
      {/* Platform Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {platforms.map(platform => (
          <div key={platform.name} className="bg-stone-900 rounded-lg p-4 border border-stone-800">
            <div className={`w-10 h-10 rounded-lg ${platform.color} mb-2`}></div>
            <div className="text-2xl font-bold text-white">{platform.accounts}</div>
            <div className="text-sm text-stone-400">{platform.name}</div>
          </div>
        ))}
      </div>
      
      {/* Content Calendar */}
      <div className="bg-stone-900 rounded-lg p-6 border border-stone-800">
        <h3 className="text-lg font-semibold text-white mb-4">Content Calendar</h3>
        <div className="space-y-2">
          {['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'].map(day => (
            <div key={day} className="flex items-center justify-between py-2 border-b border-stone-800 last:border-0">
              <span className="text-stone-300">{day}</span>
              <div className="flex gap-2">
                <span className="px-2 py-1 bg-indigo-900 rounded text-xs text-indigo-300">3 posts</span>
                <span className="px-2 py-1 bg-blue-900 rounded text-xs text-blue-300">2 tweets</span>
              </div>
            </div>
          ))}
        </div>
      </div>
      
      {/* Analytics */}
      <div className="bg-stone-900 rounded-lg p-6 border border-stone-800">
        <h3 className="text-lg font-semibold text-white mb-4">Analytics Overview</h3>
        <div className="grid grid-cols-3 gap-4">
          <div>
            <div className="text-2xl font-bold text-fuchsia-300">12.5K</div>
            <div className="text-sm text-stone-400">Total Followers</div>
          </div>
          <div>
            <div className="text-2xl font-bold text-pink-300">8.2%</div>
            <div className="text-sm text-stone-400">Engagement Rate</div>
          </div>
          <div>
            <div className="text-2xl font-bold text-amber-300">+234</div>
            <div className="text-sm text-stone-400">New This Week</div>
          </div>
        </div>
      </div>
    </div>
  );
}
