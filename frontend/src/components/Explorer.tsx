import React, { useState } from 'react';
import { motion } from 'framer-motion';

interface ExplorerProps {
  souls: any[];
  viewMode: 'persona' | 'shadow';
  onSelectSoul: (soul: any) => void;
}

export function Explorer({ souls, viewMode, onSelectSoul }: ExplorerProps) {
  const [searchTerm, setSearchTerm] = useState('');
  const [filterArchetype, setFilterArchetype] = useState('all');

  const archetypes = [...new Set(souls.map(s => s.archetype))];

  const filteredSouls = souls.filter(soul => {
    const matchesSearch = soul.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         soul.archetype.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesArchetype = filterArchetype === 'all' || soul.archetype === filterArchetype;
    return matchesSearch && matchesArchetype;
  });

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-fuchsia-300">Soul Explorer</h2>
          <p className="text-stone-400">Browse and manage soul entities</p>
        </div>
        <div className="flex gap-2">
          <button
            onClick={() => setSearchTerm('')}
            className="px-4 py-2 bg-stone-800 hover:bg-stone-700 rounded-lg text-white text-sm"
          >
            Clear Filters
          </button>
        </div>
      </div>

      {/* Filters */}
      <div className="flex gap-4 flex-wrap">
        <div className="flex-1 min-w-[200px]">
          <input
            type="text"
            placeholder="Search souls..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full bg-stone-800 border border-stone-700 rounded-lg px-4 py-2 text-white placeholder-stone-500"
          />
        </div>
        <select
          value={filterArchetype}
          onChange={(e) => setFilterArchetype(e.target.value)}
          className="bg-stone-800 border border-stone-700 rounded-lg px-4 py-2 text-white"
        >
          <option value="all">All Archetypes</option>
          {archetypes.map(archetype => (
            <option key={archetype} value={archetype}>{archetype}</option>
          ))}
        </select>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-4 gap-4">
        <div className="bg-stone-900 rounded-lg p-4 border border-stone-800">
          <div className="text-2xl font-bold text-fuchsia-300">{souls.length}</div>
          <div className="text-sm text-stone-400">Total Souls</div>
        </div>
        <div className="bg-stone-900 rounded-lg p-4 border border-stone-800">
          <div className="text-2xl font-bold text-pink-300">{archetypes.length}</div>
          <div className="text-sm text-stone-400">Archetypes</div>
        </div>
        <div className="bg-stone-900 rounded-lg p-4 border border-stone-800">
          <div className="text-2xl font-bold text-amber-300">
            {souls.filter(s => s.platforms?.length > 0).length}
          </div>
          <div className="text-sm text-stone-400">With Platforms</div>
        </div>
        <div className="bg-stone-900 rounded-lg p-4 border border-stone-800">
          <div className="text-2xl font-bold text-cyan-300">
            {souls.filter(s => s.shadow?.description).length}
          </div>
          <div className="text-sm text-stone-400">With Shadow Data</div>
        </div>
      </div>

      {/* Soul Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {filteredSouls.map((soul, index) => (
          <motion.div
            key={soul.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.05 }}
            onClick={() => onSelectSoul(soul)}
            className="bg-stone-900 rounded-lg p-4 border border-stone-800 hover:border-fuchsia-700 cursor-pointer transition"
          >
            <div className="flex items-start gap-3">
              <div className="w-12 h-12 rounded-full bg-gradient-to-br from-fuchsia-500 to-pink-500 flex items-center justify-center text-white font-bold">
                {soul.name.charAt(0)}
              </div>
              <div className="flex-1 min-w-0">
                <h3 className="font-semibold text-white truncate">{soul.name}</h3>
                <p className="text-sm text-stone-400 truncate">{soul.archetype}</p>
              </div>
            </div>
            
            <div className="mt-3 flex flex-wrap gap-1">
              {soul.platforms?.slice(0, 3).map((platform: string) => (
                <span
                  key={platform}
                  className="px-2 py-0.5 bg-stone-800 rounded text-xs text-stone-300"
                >
                  {platform}
                </span>
              ))}
              {soul.platforms?.length > 3 && (
                <span className="px-2 py-0.5 bg-stone-800 rounded text-xs text-stone-300">
                  +{soul.platforms.length - 3}
                </span>
              )}
            </div>

            {viewMode === 'shadow' && soul.shadow?.description && (
              <div className="mt-3 pt-3 border-t border-stone-800">
                <p className="text-xs text-stone-500 line-clamp-2">
                  {soul.shadow.description}
                </p>
              </div>
            )}
          </motion.div>
        ))}
      </div>

      {filteredSouls.length === 0 && (
        <div className="text-center py-12 text-stone-400">
          <div className="text-4xl mb-4">🔍</div>
          <p>No souls found matching your filters</p>
        </div>
      )}
    </div>
  );
}
