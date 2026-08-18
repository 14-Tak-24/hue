import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import axios from 'axios';

interface Soul {
  id: string;
  name: string;
  archetype: string;
  platforms: string[];
  voice: string;
  bio: string;
}

interface GeneratedContent {
  soul_id: string;
  platform: string;
  content_type: string;
  content: string;
  model_used: string;
  tokens_used: number;
  cost_estimate: number;
  generated_at: string;
}

interface ContentSchedule {
  soul_id: string;
  platform: string;
  content_type: string;
  frequency: string;
  preferred_times: string[];
  active: boolean;
  last_generated: string | null;
  next_due: string | null;
}

export function AIContentGenerator() {
  const [souls, setSouls] = useState<Soul[]>([]);
  const [selectedSoul, setSelectedSoul] = useState<Soul | null>(null);
  const [selectedPlatform, setSelectedPlatform] = useState('Twitter');
  const [contentType, setContentType] = useState('post');
  const [context, setContext] = useState('');
  const [generatedContent, setGeneratedContent] = useState<GeneratedContent | null>(null);
  const [isGenerating, setIsGenerating] = useState(false);
  const [schedules, setSchedules] = useState<ContentSchedule[]>([]);
  const [activeTab, setActiveTab] = useState<'generate' | 'schedule' | 'history'>('generate');
  const [generationHistory, setGenerationHistory] = useState<GeneratedContent[]>([]);

  // Load souls on mount
  useEffect(() => {
    const loadSouls = async () => {
      try {
        const response = await axios.get('/api/souls');
        setSouls(response.data.souls || []);
      } catch (error) {
        console.error('Failed to load souls:', error);
      }
    };
    loadSouls();
  }, []);

  // Load schedules
  useEffect(() => {
    const loadSchedules = async () => {
      try {
        const response = await axios.get('/api/content/schedules');
        setSchedules(response.data.schedules || []);
      } catch (error) {
        console.error('Failed to load schedules:', error);
      }
    };
    loadSchedules();
  }, []);

  const handleGenerate = async () => {
    if (!selectedSoul) return;

    setIsGenerating(true);
    try {
      const response = await axios.post('/api/ai/generate', {
        soul_id: selectedSoul.id,
        platform: selectedPlatform,
        content_type: contentType,
        context: context || undefined,
        tone: 'authentic to soul voice',
        length: 'medium'
      });

      setGeneratedContent(response.data);
      setGenerationHistory(prev => [response.data, ...prev]);
    } catch (error) {
      console.error('Failed to generate content:', error);
      alert('Failed to generate content. Please try again.');
    } finally {
      setIsGenerating(false);
    }
  };

  const handleScheduleToggle = async (scheduleId: string, active: boolean) => {
    try {
      await axios.put(`/api/content/schedules/${scheduleId}`, { active });
      setSchedules(prev =>
        prev.map(s => s.soul_id === scheduleId ? { ...s, active } : s)
      );
    } catch (error) {
      console.error('Failed to update schedule:', error);
    }
  };

  const availablePlatforms = selectedSoul?.platforms || [];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-fuchsia-300">🤖 AI Content Generator</h2>
          <p className="text-stone-400">Generate autonomous content for souls across platforms</p>
        </div>
        <div className="flex gap-2">
          <button
            onClick={() => setActiveTab('generate')}
            className={`px-4 py-2 rounded-lg transition ${
              activeTab === 'generate'
                ? 'bg-fuchsia-700 text-white'
                : 'bg-stone-800 text-stone-300 hover:bg-stone-700'
            }`}
          >
            Generate
          </button>
          <button
            onClick={() => setActiveTab('schedule')}
            className={`px-4 py-2 rounded-lg transition ${
              activeTab === 'schedule'
                ? 'bg-fuchsia-700 text-white'
                : 'bg-stone-800 text-stone-300 hover:bg-stone-700'
            }`}
          >
            Schedules
          </button>
          <button
            onClick={() => setActiveTab('history')}
            className={`px-4 py-2 rounded-lg transition ${
              activeTab === 'history'
                ? 'bg-fuchsia-700 text-white'
                : 'bg-stone-800 text-stone-300 hover:bg-stone-700'
            }`}
          >
            History
          </button>
        </div>
      </div>

      {/* Generate Tab */}
      {activeTab === 'generate' && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Configuration Panel */}
          <div className="bg-stone-900 rounded-xl p-6 border border-stone-700">
            <h3 className="text-lg font-semibold text-stone-200 mb-4">Content Configuration</h3>
            
            <div className="space-y-4">
              {/* Soul Selection */}
              <div>
                <label className="block text-sm text-stone-400 mb-2">Select Soul</label>
                <select
                  value={selectedSoul?.id || ''}
                  onChange={(e) => setSelectedSoul(souls.find(s => s.id === e.target.value) || null)}
                  className="w-full bg-stone-800 border border-stone-700 rounded-lg px-4 py-2 text-white"
                >
                  <option value="">Choose a soul...</option>
                  {souls.map(soul => (
                    <option key={soul.id} value={soul.id}>
                      {soul.name} ({soul.archetype})
                    </option>
                  ))}
                </select>
              </div>

              {/* Platform Selection */}
              <div>
                <label className="block text-sm text-stone-400 mb-2">Platform</label>
                <select
                  value={selectedPlatform}
                  onChange={(e) => setSelectedPlatform(e.target.value)}
                  disabled={!selectedSoul}
                  className="w-full bg-stone-800 border border-stone-700 rounded-lg px-4 py-2 text-white disabled:opacity-50"
                >
                  {availablePlatforms.map(platform => (
                    <option key={platform} value={platform}>{platform}</option>
                  ))}
                </select>
              </div>

              {/* Content Type */}
              <div>
                <label className="block text-sm text-stone-400 mb-2">Content Type</label>
                <select
                  value={contentType}
                  onChange={(e) => setContentType(e.target.value)}
                  className="w-full bg-stone-800 border border-stone-700 rounded-lg px-4 py-2 text-white"
                >
                  <option value="post">Post</option>
                  <option value="thread">Thread</option>
                  <option value="caption">Caption</option>
                  <option value="message">Message</option>
                  <option value="story">Story</option>
                  <option value="bio">Bio</option>
                </select>
              </div>

              {/* Context */}
              <div>
                <label className="block text-sm text-stone-400 mb-2">Context (Optional)</label>
                <textarea
                  value={context}
                  onChange={(e) => setContext(e.target.value)}
                  placeholder="Add context for the content generation..."
                  className="w-full bg-stone-800 border border-stone-700 rounded-lg px-4 py-2 text-white h-24 resize-none"
                />
              </div>

              {/* Generate Button */}
              <button
                onClick={handleGenerate}
                disabled={!selectedSoul || isGenerating}
                className="w-full py-3 bg-gradient-to-r from-fuchsia-700 to-pink-700 hover:from-fuchsia-600 hover:to-pink-600 rounded-lg text-white font-semibold disabled:opacity-50 disabled:cursor-not-allowed transition"
              >
                {isGenerating ? 'Generating...' : 'Generate Content'}
              </button>
            </div>
          </div>

          {/* Result Panel */}
          <div className="bg-stone-900 rounded-xl p-6 border border-stone-700">
            <h3 className="text-lg font-semibold text-stone-200 mb-4">Generated Content</h3>
            
            {generatedContent ? (
              <div className="space-y-4">
                <div className="bg-stone-800 rounded-lg p-4 border border-stone-700">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm text-fuchsia-300">{selectedSoul?.name}</span>
                    <span className="text-xs text-stone-400">{selectedPlatform}</span>
                  </div>
                  <p className="text-stone-200 whitespace-pre-wrap">{generatedContent.content}</p>
                </div>

                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div className="bg-stone-800 rounded-lg p-3">
                    <span className="text-stone-400">Model:</span>
                    <span className="text-stone-200 ml-2">{generatedContent.model_used}</span>
                  </div>
                  <div className="bg-stone-800 rounded-lg p-3">
                    <span className="text-stone-400">Tokens:</span>
                    <span className="text-stone-200 ml-2">{generatedContent.tokens_used}</span>
                  </div>
                  <div className="bg-stone-800 rounded-lg p-3">
                    <span className="text-stone-400">Cost:</span>
                    <span className="text-stone-200 ml-2">${generatedContent.cost_estimate.toFixed(4)}</span>
                  </div>
                  <div className="bg-stone-800 rounded-lg p-3">
                    <span className="text-stone-400">Time:</span>
                    <span className="text-stone-200 ml-2">{new Date(generatedContent.generated_at).toLocaleTimeString()}</span>
                  </div>
                </div>

                <div className="flex gap-2">
                  <button className="flex-1 py-2 bg-stone-700 hover:bg-stone-600 rounded-lg text-white text-sm">
                    Copy to Clipboard
                  </button>
                  <button className="flex-1 py-2 bg-fuchsia-700 hover:bg-fuchsia-600 rounded-lg text-white text-sm">
                    Post to Platform
                  </button>
                </div>
              </div>
            ) : (
              <div className="flex items-center justify-center h-64 text-stone-400">
                <div className="text-center">
                  <span className="text-4xl mb-2 block">✨</span>
                  <p>Select a soul and generate content to see results here</p>
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Schedule Tab */}
      {activeTab === 'schedule' && (
        <div className="bg-stone-900 rounded-xl p-6 border border-stone-700">
          <h3 className="text-lg font-semibold text-stone-200 mb-4">Content Schedules</h3>
          
          {schedules.length > 0 ? (
            <div className="space-y-3">
              {schedules.map((schedule, index) => {
                const soul = souls.find(s => s.id === schedule.soul_id);
                return (
                  <div key={index} className="bg-stone-800 rounded-lg p-4 border border-stone-700">
                    <div className="flex items-center justify-between">
                      <div>
                        <span className="text-stone-200 font-medium">{soul?.name || 'Unknown Soul'}</span>
                        <span className="text-stone-400 text-sm ml-2">{schedule.platform} - {schedule.content_type}</span>
                      </div>
                      <div className="flex items-center gap-4">
                        <span className="text-xs text-stone-400">{schedule.frequency}</span>
                        <button
                          onClick={() => handleScheduleToggle(schedule.soul_id, !schedule.active)}
                          className={`px-3 py-1 rounded-full text-xs ${
                            schedule.active
                              ? 'bg-green-700 text-white'
                              : 'bg-stone-700 text-stone-400'
                          }`}
                        >
                          {schedule.active ? 'Active' : 'Paused'}
                        </button>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          ) : (
            <div className="text-center text-stone-400 py-8">
              <p>No schedules configured yet</p>
            </div>
          )}
        </div>
      )}

      {/* History Tab */}
      {activeTab === 'history' && (
        <div className="bg-stone-900 rounded-xl p-6 border border-stone-700">
          <h3 className="text-lg font-semibold text-stone-200 mb-4">Generation History</h3>
          
          {generationHistory.length > 0 ? (
            <div className="space-y-3">
              {generationHistory.map((item, index) => {
                const soul = souls.find(s => s.id === item.soul_id);
                return (
                  <div key={index} className="bg-stone-800 rounded-lg p-4 border border-stone-700">
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-stone-200 font-medium">{soul?.name || 'Unknown Soul'}</span>
                      <span className="text-xs text-stone-400">{new Date(item.generated_at).toLocaleString()}</span>
                    </div>
                    <p className="text-stone-400 text-sm mb-2">{item.platform} - {item.content_type}</p>
                    <p className="text-stone-200 text-sm">{item.content.substring(0, 100)}...</p>
                  </div>
                );
              })}
            </div>
          ) : (
            <div className="text-center text-stone-400 py-8">
              <p>No generation history yet</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}