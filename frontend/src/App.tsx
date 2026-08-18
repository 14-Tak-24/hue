import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import axios from 'axios';

// Import components
import { Explorer } from './components/Explorer';
import { PolarityMap } from './components/PolarityMap';
import { PlatformMatrix } from './components/PlatformMatrix';
import { ShadowEngine } from './components/ShadowEngine';
import { SocialDashboard } from './components/SocialDashboard';
import { BackupExtractor } from './components/BackupExtractor';
import { AIContentGenerator } from './components/AIContentGenerator';

// Import API
import { soulsApi, Soul } from './api/souls';

// Main Tabs
const TABS = [
  { id: 'explorer', label: '🕯️ Explorer', icon: '🕯️' },
  { id: 'polarity', label: '⚖️ Polarity Map', icon: '⚖️' },
  { id: 'matrix', label: '📡 Platform Matrix', icon: '📡' },
  { id: 'shadow-engine', label: '🧠 Shadow Engine', icon: '🧠' },
  { id: 'social', label: '📱 Social Dashboard', icon: '📱' },
  { id: 'ai-generator', label: '🤖 AI Generator', icon: '🤖' },
  { id: 'backup', label: '📲 Backup Extractor', icon: '📲' },
];

interface AppState {
  souls: Soul[];
  selectedSoul: Soul | null;
  editingSoul: Soul | null;
  tab: string;
  viewMode: 'persona' | 'shadow';
}

function App() {
  const [state, setState] = useState<AppState>({
    souls: [],
    selectedSoul: null,
    editingSoul: null,
    tab: 'explorer',
    viewMode: 'persona',
  });

  // Load souls on mount
  useEffect(() => {
    const loadSouls = async () => {
      try {
        const response = await axios.get('/api/souls');
        setState(prev => ({ ...prev, souls: response.data.souls || [] }));
      } catch (error) {
        console.error('Failed to load souls:', error);
        // Load from local file if API fails
        try {
          const localResponse = await fetch('/src/data/souls_entities.json');
          const data = await localResponse.json();
          setState(prev => ({ ...prev, souls: data.souls || [] }));
        } catch (localError) {
          console.error('Failed to load local souls:', localError);
        }
      }
    };
    loadSouls();
  }, []);

  // Handle soul selection
  const selectSoul = (soul: any) => {
    setState(prev => ({ ...prev, selectedSoul: soul, editingSoul: null }));
  };

  // Handle tab switching
  const switchTab = (tabId: string) => {
    setState(prev => ({ ...prev, tab: tabId }));
  };

  // Render the current tab content
  const renderContent = () => {
    switch (state.tab) {
      case 'explorer':
        return (
          <Explorer 
            souls={state.souls}
            viewMode={state.viewMode}
            onSelectSoul={selectSoul}
          />
        );
      case 'polarity':
        return (
          <PolarityMap 
            souls={state.souls}
            onSelectSoul={selectSoul}
          />
        );
      case 'matrix':
        return <PlatformMatrix souls={state.souls} />;
      case 'shadow-engine':
        return (
          <ShadowEngine 
            souls={state.souls}
            onSelectSoul={selectSoul}
          />
        );
      case 'social':
        return <SocialDashboard souls={state.souls} />;
      case 'ai-generator':
        return <AIContentGenerator />;
      case 'backup':
        return <BackupExtractor />;
      default:
        return null;
    }
  };

  return (
    <div className="min-h-screen bg-stone-950 text-stone-100">
      {/* Header */}
      <header className="border-b border-stone-800 bg-stone-900/50 backdrop-blur-sm sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center gap-3">
              <span className="text-2xl">🔮</span>
              <h1 className="text-xl font-display font-bold bg-clip-text text-transparent bg-gradient-to-r from-fuchsia-300 via-pink-300 to-amber-200">
                Soul Registry Studio
              </h1>
            </div>
            <div className="flex items-center gap-3 text-sm text-stone-400">
              <span>{state.souls.length} Souls</span>
              <button className="px-3 py-1.5 rounded-lg bg-fuchsia-700 hover:bg-fuchsia-600 text-white">
                Export
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Navigation */}
      <nav className="border-b border-stone-800 bg-stone-900/30">
        <div className="max-w-7xl mx-auto px-4">
          <div className="flex gap-1 overflow-x-auto py-2">
            {TABS.map(tab => (
              <button
                key={tab.id}
                onClick={() => switchTab(tab.id)}
                className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm whitespace-nowrap transition ${
                  state.tab === tab.id
                    ? 'bg-stone-800 text-fuchsia-300 border border-stone-700'
                    : 'text-stone-400 hover:text-stone-200 hover:bg-stone-800/50'
                }`}
              >
                <span>{tab.icon}</span> {tab.label}
              </button>
            ))}
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 py-6">
        {renderContent()}
      </main>

      {/* Detail Modal */}
      {state.selectedSoul && (
        <SoulDetailModal
          soul={state.selectedSoul}
          onClose={() => setState(prev => ({ ...prev, selectedSoul: null }))}
          onEdit={() => setState(prev => ({ ...prev, editingSoul: prev.selectedSoul }))}
          onSave={(updated: Soul) => {
            setState(prev => ({
              ...prev,
              souls: prev.souls.map(s => s.id === updated.id ? updated : s),
              selectedSoul: updated,
              editingSoul: null,
            }));
          }}
        />
      )}
    </div>
  );
}

// Soul Detail Modal Component
function SoulDetailModal({ soul, onClose, onEdit, onSave }: any) {
  const [editing, setEditing] = useState(false);
  const [editedSoul, setEditedSoul] = useState(soul);

  const handleSave = () => {
    onSave(editedSoul);
    setEditing(false);
  };

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4"
      onClick={onClose}
    >
      <motion.div
        initial={{ scale: 0.95, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        exit={{ scale: 0.95, opacity: 0 }}
        className="bg-stone-900 rounded-xl max-w-2xl w-full max-h-[80vh] overflow-y-auto border border-stone-700"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="p-6">
          <div className="flex items-start justify-between mb-6">
            <div>
              <h2 className="text-2xl font-bold text-fuchsia-300">{soul.name}</h2>
              <p className="text-stone-400">{soul.archetype}</p>
            </div>
            <button
              onClick={onClose}
              className="text-stone-400 hover:text-white text-2xl"
            >
              ×
            </button>
          </div>

          {editing ? (
            <div className="space-y-4">
              <div>
                <label className="block text-sm text-stone-400 mb-1">Name</label>
                <input
                  type="text"
                  value={editedSoul.name}
                  onChange={(e) => setEditedSoul({ ...editedSoul, name: e.target.value })}
                  className="w-full bg-stone-800 border border-stone-700 rounded-lg px-4 py-2 text-white"
                />
              </div>
              <div>
                <label className="block text-sm text-stone-400 mb-1">Archetype</label>
                <input
                  type="text"
                  value={editedSoul.archetype}
                  onChange={(e) => setEditedSoul({ ...editedSoul, archetype: e.target.value })}
                  className="w-full bg-stone-800 border border-stone-700 rounded-lg px-4 py-2 text-white"
                />
              </div>
              <div className="flex gap-2">
                <button
                  onClick={handleSave}
                  className="px-4 py-2 bg-fuchsia-700 hover:bg-fuchsia-600 rounded-lg text-white"
                >
                  Save
                </button>
                <button
                  onClick={() => setEditing(false)}
                  className="px-4 py-2 bg-stone-700 hover:bg-stone-600 rounded-lg text-white"
                >
                  Cancel
                </button>
              </div>
            </div>
          ) : (
            <div className="space-y-4">
              <div>
                <h3 className="text-lg font-semibold text-stone-200 mb-2">Persona</h3>
                <p className="text-stone-400">{soul.persona?.description || 'No persona data'}</p>
              </div>
              <div>
                <h3 className="text-lg font-semibold text-stone-200 mb-2">Shadow</h3>
                <p className="text-stone-400">{soul.shadow?.description || 'No shadow data'}</p>
              </div>
              <div>
                <h3 className="text-lg font-semibold text-stone-200 mb-2">Platforms</h3>
                <div className="flex flex-wrap gap-2">
                  {soul.platforms?.map((platform: string) => (
                    <span
                      key={platform}
                      className="px-3 py-1 bg-stone-800 rounded-full text-sm text-stone-300"
                    >
                      {platform}
                    </span>
                  )) || <span className="text-stone-400">No platforms assigned</span>}
                </div>
              </div>
              <button
                onClick={() => setEditing(true)}
                className="px-4 py-2 bg-stone-700 hover:bg-stone-600 rounded-lg text-white"
              >
                Edit
              </button>
            </div>
          )}
        </div>
      </motion.div>
    </motion.div>
  );
}

export default App;
