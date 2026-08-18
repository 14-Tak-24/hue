"""
Process Extracted iPhone Backup Media for Content Creation
Automates media organization, categorization, and content library integration
"""

import json
import os
import shutil
from pathlib import Path
from typing import Dict, List
from datetime import datetime

class MediaProcessor:
    """Process extracted media for content creation"""
    
    def __init__(self):
        self.base_path = Path("scripts/iphone_backup_data")
        self.media_dir = self.base_path / "media"
        self.processing_guide = self.media_dir / "processing_guide.json"
        self.guide_data = self.load_processing_guide()
        
    def load_processing_guide(self) -> Dict:
        """Load media processing guide"""
        if self.processing_guide.exists():
            with open(self.processing_guide, 'r') as f:
                return json.load(f)
        return {}
    
    def scan_extracted_media(self) -> Dict[str, List[Path]]:
        """Scan for extracted media files"""
        print("\n" + "=" * 60)
        print("Scanning for Extracted Media")
        print("=" * 60)
        
        media_extensions = {
            'video': ['.mp4', '.mov', '.avi', '.mkv', '.m4v'],
            'audio': ['.mp3', '.m4a', '.wav', '.aac', '.flac'],
            'image': ['.jpg', '.jpeg', '.png', '.heic', '.heif', '.gif']
        }
        
        found_media = {'video': [], 'audio': [], 'image': []}
        
        # Scan media directory for unorganized files
        all_files = []
        for ext_group, extensions in media_extensions.items():
            for ext in extensions:
                all_files.extend(self.media_dir.rglob(f"*{ext}"))
                all_files.extend(self.media_dir.rglob(f"*{ext.upper()}"))
        
        # Filter out files already in organized subdirectories
        organized_dirs = ['ritual_ceremonies', 'wisdom_teachings', 'community_events', 
                         'archetype_content', 'behind_scenes']
        
        unorganized_files = []
        for file_path in all_files:
            # Check if file is in an organized directory
            is_organized = any(organized_dir in str(file_path) for organized_dir in organized_dirs)
            if not is_organized:
                unorganized_files.append(file_path)
        
        print(f"Found {len(unorganized_files)} unorganized media files")
        
        # Categorize by type
        for file_path in unorganized_files:
            ext = file_path.suffix.lower()
            if ext in media_extensions['video']:
                found_media['video'].append(file_path)
            elif ext in media_extensions['audio']:
                found_media['audio'].append(file_path)
            elif ext in media_extensions['image']:
                found_media['image'].append(file_path)
        
        print(f"  Videos: {len(found_media['video'])}")
        print(f"  Audio: {len(found_media['audio'])}")
        print(f"  Images: {len(found_media['image'])}")
        
        return found_media
    
    def auto_categorize_media(self, media_files: Dict[str, List[Path]]) -> Dict[str, List[Path]]:
        """Auto-categorize media based on filename keywords"""
        print("\n" + "=" * 60)
        print("Auto-Categorizing Media")
        print("=" * 60)
        
        category_keywords = {
            'ritual_ceremonies': ['ritual', 'ceremony', 'rite', 'sacred', 'ceremonial', 'rituals'],
            'wisdom_teachings': ['teaching', 'wisdom', 'teach', 'lesson', 'class', 'workshop', 'talk'],
            'community_events': ['event', 'gathering', 'meetup', 'party', 'celebration', 'community'],
            'behind_scenes': ['bts', 'behind', 'behindthescenes', 'behind_scene', 'making', 'prep']
        }
        
        categorized_media = {
            'ritual_ceremonies': [],
            'wisdom_teachings': [],
            'community_events': [],
            'archetype_content': [],
            'behind_scenes': [],
            'uncategorized': []
        }
        
        categorized_count = 0
        for media_type, files in media_files.items():
            for file_path in files:
                filename = file_path.name.lower()
                categorized = False
                
                for category, keywords in category_keywords.items():
                    if any(keyword in filename for keyword in keywords):
                        categorized_media[category].append(file_path)
                        categorized_count += 1
                        print(f"✓ Categorized: {filename} → {category}")
                        categorized = True
                        break
                
                if not categorized:
                    categorized_media['uncategorized'].append(file_path)
        
        print(f"\n✓ Auto-categorized {categorized_count} media files")
        return categorized_media
    
    def organize_media_by_type(self, categorized_media: Dict[str, List[Path]]):
        """Organize media into proper directory structure"""
        print("\n" + "=" * 60)
        print("Organizing Media by Type")
        print("=" * 60)
        
        # Ensure directory structure exists
        subdirs = {
            'ritual_ceremonies': ['audio', 'video', 'photos'],
            'wisdom_teachings': ['audio', 'video', 'transcripts'],
            'community_events': ['audio', 'video', 'photos'],
            'archetype_content': ['high_priest', 'divine_mother', 'seductive_muse', 'cosmic_mystic'],
            'behind_scenes': ['bts_footage', 'bts_photos']
        }
        
        for category, subfolders in subdirs.items():
            category_dir = self.media_dir / category
            category_dir.mkdir(exist_ok=True)
            for subfolder in subfolders:
                (category_dir / subfolder).mkdir(exist_ok=True)
        
        # Move files to appropriate directories
        moved_count = 0
        for category, files in categorized_media.items():
            if category == 'uncategorized':
                continue
                
            for file_path in files:
                ext = file_path.suffix.lower()
                
                # Determine subdirectory based on file type
                if category in ['ritual_ceremonies', 'community_events']:
                    if ext in ['.mp4', '.mov', '.avi', '.mkv', '.m4v']:
                        subdir = 'video'
                    elif ext in ['.mp3', '.m4a', '.wav', '.aac', '.flac']:
                        subdir = 'audio'
                    else:
                        subdir = 'photos'
                elif category == 'wisdom_teachings':
                    if ext in ['.mp4', '.mov', '.avi', '.mkv', '.m4v']:
                        subdir = 'video'
                    elif ext in ['.mp3', '.m4a', '.wav', '.aac', '.flac']:
                        subdir = 'audio'
                    else:
                        subdir = 'transcripts'
                elif category == 'behind_scenes':
                    if ext in ['.mp4', '.mov', '.avi', '.mkv', '.m4v']:
                        subdir = 'bts_footage'
                    else:
                        subdir = 'bts_photos'
                else:
                    subdir = 'high_priest'  # default for archetype_content
                
                target_dir = self.media_dir / category / subdir
                target_path = target_dir / file_path.name
                
                # Move file
                try:
                    shutil.move(str(file_path), str(target_path))
                    moved_count += 1
                    print(f"✓ Moved: {file_path.name} → {category}/{subdir}/")
                except Exception as e:
                    print(f"✗ Error moving {file_path.name}: {e}")
        
        print(f"\n✓ Moved {moved_count} media files")
    
    def create_content_inventory(self) -> Dict:
        """Create an inventory of all organized media"""
        print("\n" + "=" * 60)
        print("Creating Content Inventory")
        print("=" * 60)
        
        inventory = {
            'total_files': 0,
            'categories': {},
            'file_types': {'video': 0, 'audio': 0, 'image': 0},
            'created_at': datetime.now().isoformat()
        }
        
        # Scan organized directories
        categories = ['ritual_ceremonies', 'wisdom_teachings', 'community_events', 
                     'archetype_content', 'behind_scenes']
        
        for category in categories:
            category_dir = self.media_dir / category
            if not category_dir.exists():
                continue
            
            category_files = list(category_dir.rglob('*'))
            category_files = [f for f in category_files if f.is_file()]
            
            inventory['categories'][category] = {
                'total_files': len(category_files),
                'subdirectories': {}
            }
            
            # Count by subdirectory
            for subdir in category_dir.iterdir():
                if subdir.is_dir():
                    subdir_files = list(subdir.rglob('*'))
                    subdir_files = [f for f in subdir_files if f.is_file()]
                    inventory['categories'][category]['subdirectories'][subdir.name] = len(subdir_files)
            
            inventory['total_files'] += len(category_files)
        
        # Count by file type
        media_extensions = {
            'video': ['.mp4', '.mov', '.avi', '.mkv', '.m4v'],
            'audio': ['.mp3', '.m4a', '.wav', '.aac', '.flac'],
            'image': ['.jpg', '.jpeg', '.png', '.heic', '.heif', '.gif']
        }
        
        for category in categories:
            category_dir = self.media_dir / category
            if category_dir.exists():
                for file_path in category_dir.rglob('*'):
                    if file_path.is_file():
                        ext = file_path.suffix.lower()
                        for file_type, extensions in media_extensions.items():
                            if ext in extensions:
                                inventory['file_types'][file_type] += 1
        
        # Save inventory
        inventory_file = self.media_dir / 'content_inventory.json'
        with open(inventory_file, 'w') as f:
            json.dump(inventory, f, indent=2)
        
        print(f"✓ Inventory saved: {inventory_file}")
        print(f"\nSummary:")
        print(f"  Total files: {inventory['total_files']}")
        print(f"  Videos: {inventory['file_types']['video']}")
        print(f"  Audio: {inventory['file_types']['audio']}")
        print(f"  Images: {inventory['file_types']['image']}")
        
        return inventory
    
    def generate_content_calendar_suggestions(self, inventory: Dict):
        """Generate content calendar suggestions based on available media"""
        print("\n" + "=" * 60)
        print("Generating Content Calendar Suggestions")
        print("=" * 60)
        
        suggestions = {
            'high_priority_content': [],
            'medium_priority_content': [],
            'low_priority_content': []
        }
        
        # Analyze inventory and generate suggestions
        for category, data in inventory['categories'].items():
            if data['total_files'] > 0:
                if category == 'ritual_ceremonies':
                    suggestions['high_priority_content'].append({
                        'type': 'Ritual Content',
                        'category': category,
                        'suggested_posts': data['total_files'],
                        'description': 'Share ritual recordings and ceremony highlights'
                    })
                elif category == 'wisdom_teachings':
                    suggestions['high_priority_content'].append({
                        'type': 'Wisdom Content',
                        'category': category,
                        'suggested_posts': data['total_files'],
                        'description': 'Share wisdom teachings and educational content'
                    })
                elif category == 'community_events':
                    suggestions['high_priority_content'].append({
                        'type': 'Event Content',
                        'category': category,
                        'suggested_posts': data['total_files'],
                        'description': 'Share community event highlights and memories'
                    })
                elif category == 'behind_scenes':
                    suggestions['medium_priority_content'].append({
                        'type': 'Behind-the-Scenes',
                        'category': category,
                        'suggested_posts': data['total_files'],
                        'description': 'Share behind-the-scenes content for engagement'
                    })
                elif category == 'archetype_content':
                    suggestions['medium_priority_content'].append({
                        'type': 'Archetype Content',
                        'category': category,
                        'suggested_posts': data['total_files'],
                        'description': 'Share archetype-specific content for targeted audiences'
                    })
        
        # Save suggestions
        suggestions_file = self.media_dir / 'content_calendar_suggestions.json'
        with open(suggestions_file, 'w') as f:
            json.dump(suggestions, f, indent=2)
        
        print(f"✓ Suggestions saved: {suggestions_file}")
        print(f"\nHigh Priority Content: {len(suggestions['high_priority_content'])} types")
        print(f"Medium Priority Content: {len(suggestions['medium_priority_content'])} types")
    
    def create_processing_report(self, inventory: Dict):
        """Create media processing report"""
        print("\n" + "=" * 60)
        print("Creating Media Processing Report")
        print("=" * 60)
        
        report = {
            'processing_summary': {
                'total_media_processed': inventory['total_files'],
                'categories_organized': len(inventory['categories']),
                'processing_complete': True,
                'processed_at': datetime.now().isoformat()
            },
            'content_breakdown': inventory['categories'],
            'next_steps': [
                'Review organized media in category directories',
                'Check content calendar suggestions for posting schedule',
                'Integrate media with social media content library',
                'Schedule posts across platforms'
            ]
        }
        
        report_file = self.media_dir / 'media_processing_report.json'
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"✓ Report saved: {report_file}")
    
    def run_full_processing(self):
        """Run complete media processing workflow"""
        print("=" * 60)
        print("iPhone Backup Media Processing Workflow")
        print("=" * 60)
        
        # Step 1: Scan for media
        media_files = self.scan_extracted_media()
        
        if not any(media_files.values()):
            print("\nNo media files found to process.")
            print("Please extract media from iPhone Backup Extractor to:")
            print(f"  {self.media_dir}")
            return
        
        # Step 2: Auto-categorize
        categorized_media = self.auto_categorize_media(media_files)
        
        # Step 3: Organize by type
        self.organize_media_by_type(categorized_media)
        
        # Step 4: Create inventory
        inventory = self.create_content_inventory()
        
        # Step 5: Generate suggestions
        self.generate_content_calendar_suggestions(inventory)
        
        # Step 6: Create report
        self.create_processing_report(inventory)
        
        print("\n" + "=" * 60)
        print("Media Processing Complete")
        print("=" * 60)
        print(f"\nOrganized media directory structure:")
        print(f"  {self.media_dir}/")
        print(f"    ├── ritual_ceremonies/")
        print(f"    ├── wisdom_teachings/")
        print(f"    ├── community_events/")
        print(f"    ├── archetype_content/")
        print(f"    └── behind_scenes/")

def main():
    """Main function"""
    print("iPhone Backup Media Processor")
    print("This script will process extracted media for content creation\n")
    
    processor = MediaProcessor()
    processor.run_full_processing()

if __name__ == "__main__":
    main()
