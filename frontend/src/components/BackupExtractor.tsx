import React, { useState } from 'react';

export function BackupExtractor() {
  const [backupPath, setBackupPath] = useState('');
  const [isExtracting, setIsExtracting] = useState(false);
  const [status, setStatus] = useState('');

  const handleExtract = async () => {
    if (!backupPath) {
      setStatus('Please enter a backup path');
      return;
    }
    
    setIsExtracting(true);
    setStatus('Starting extraction...');
    
    // Simulate extraction process
    setTimeout(() => setStatus('Extracting profile images...'), 1000);
    setTimeout(() => setStatus('Extracting contacts...'), 2000);
    setTimeout(() => setStatus('Extracting media files...'), 3000);
    setTimeout(() => {
      setStatus('Extraction complete!');
      setIsExtracting(false);
    }, 4000);
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-fuchsia-300">iPhone Backup Extractor</h2>
        <p className="text-stone-400">Extract profile images, contacts, and media from iPhone backups</p>
      </div>
      
      <div className="bg-stone-900 rounded-lg p-6 border border-stone-800">
        <div className="space-y-4">
          <div>
            <label className="block text-sm text-stone-400 mb-2">Backup Path</label>
            <input
              type="text"
              value={backupPath}
              onChange={(e) => setBackupPath(e.target.value)}
              placeholder="/path/to/iphone/backup"
              className="w-full bg-stone-800 border border-stone-700 rounded-lg px-4 py-2 text-white placeholder-stone-500"
            />
          </div>
          
          <button
            onClick={handleExtract}
            disabled={isExtracting}
            className="px-6 py-2 bg-fuchsia-700 hover:bg-fuchsia-600 disabled:bg-stone-700 rounded-lg text-white"
          >
            {isExtracting ? 'Extracting...' : 'Start Extraction'}
          </button>
          
          {status && (
            <div className="mt-4 p-4 bg-stone-800 rounded-lg">
              <p className="text-stone-300">{status}</p>
            </div>
          )}
        </div>
      </div>
      
      <div className="bg-stone-900 rounded-lg p-6 border border-stone-800">
        <h3 className="text-lg font-semibold text-white mb-4">Extraction Options</h3>
        <div className="space-y-2">
          <label className="flex items-center gap-2">
            <input type="checkbox" defaultChecked className="rounded" />
            <span className="text-stone-300">Profile Images</span>
          </label>
          <label className="flex items-center gap-2">
            <input type="checkbox" defaultChecked className="rounded" />
            <span className="text-stone-300">Contacts</span>
          </label>
          <label className="flex items-center gap-2">
            <input type="checkbox" defaultChecked className="rounded" />
            <span className="text-stone-300">Media Files</span>
          </label>
          <label className="flex items-center gap-2">
            <input type="checkbox" className="rounded" />
            <span className="text-stone-300">Notes</span>
          </label>
        </div>
      </div>
    </div>
  );
}
