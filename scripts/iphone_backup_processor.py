"""
iPhone Backup Data Processor for Tiapma'atzu HueMan-i-Terry
Process extracted iPhone backup data for social media setup
"""

import json
import sys
import os
import shutil
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

class iPhoneBackupProcessor:
    """Process iPhone backup data for social media setup"""
    
    def __init__(self, backup_path: str = None):
        self.backup_path = backup_path or self.find_backup_path()
        self.output_path = Path("scripts/iphone_backup_data")
        self.souls_data = self.load_souls_data()
        
    def find_backup_path(self) -> str:
        """Find iPhone backup path"""
        # Common iPhone backup locations
        common_paths = [
            os.path.expanduser("~/Library/Application Support/MobileSync/Backup/"),
            os.path.expanduser("~/AppData/Roaming/Apple Computer/MobileSync/Backup/"),
            "/Applications/iPhone Backup Extractor.app/Contents/MacOS/",
        ]
        
        for path in common_paths:
            if os.path.exists(path):
                print(f"Found backup path: {path}")
                return path
        
        return "/Applications/iPhone Backup Extractor.app/"
    
    def load_souls_data(self) -> Dict[str, Any]:
        """Load souls data from JSON file"""
        souls_path = Path("src/data/souls_entities.json")
        if souls_path.exists():
            with open(souls_path, 'r') as f:
                return json.load(f)
        return {}
    
    def create_output_structure(self):
        """Create output directory structure"""
        directories = [
            self.output_path,
            self.output_path / "profile_images",
            self.output_path / "header_images",
            self.output_path / "contacts",
            self.output_path / "media",
            self.output_path / "other_data"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
        
        print(f"✓ Created output structure at {self.output_path}")
    
    def process_profile_images(self):
        """Process and organize profile images for souls"""
        print("\n" + "=" * 60)
        print("Processing Profile Images for Souls")
        print("=" * 60)
        
        souls = self.souls_data.get('souls', [])
        profile_images_dir = self.output_path / "profile_images"
        
        # Create mapping of soul names to their expected image files
        soul_image_mapping = {}
        for soul in souls:
            soul_id = soul['id']
            soul_name = soul['name']
            current_image = soul.get('image', '')
            
            if current_image:
                # Extract filename from URL if it's a URL
                if current_image.startswith('http'):
                    filename = current_image.split('/')[-1]
                else:
                    filename = current_image
                
                soul_image_mapping[soul_id] = {
                    'name': soul_name,
                    'current_image': current_image,
                    'expected_filename': filename,
                    'archetype': soul['archetype']
                }
        
        # Instructions for manual extraction
        print(f"\nProfile Image Processing Instructions:")
        print(f"Total Souls: {len(souls)}")
        print(f"Expected Images: {len(soul_image_mapping)}")
        
        print(f"\nSteps to extract profile images:")
        print(f"1. Open iPhone Backup Extractor")
        print(f"2. Select your iPhone backup")
        print(f"3. Navigate to Media/Photos")
        print(f"4. Extract photos to: {profile_images_dir}")
        print(f"5. Rename images to match soul IDs:")
        
        for soul_id, mapping in soul_image_mapping.items():
            print(f"   - {soul_id}: {mapping['name']} ({mapping['archetype']})")
            print(f"     Expected: {mapping['expected_filename']}")
        
        # Create mapping file
        mapping_file = self.output_path / "profile_images" / "image_mapping.json"
        with open(mapping_file, 'w') as f:
            json.dump(soul_image_mapping, f, indent=2)
        
        print(f"\n✓ Created image mapping file: {mapping_file}")
        print(f"✓ Profile images directory ready: {profile_images_dir}")
    
    def process_contacts(self):
        """Process contacts for community building"""
        print("\n" + "=" * 60)
        print("Processing Contacts for Community Building")
        print("=" * 60)
        
        contacts_dir = self.output_path / "contacts"
        
        print(f"\nContact Processing Instructions:")
        print(f"1. Open iPhone Backup Extractor")
        print(f"2. Select your iPhone backup")
        print(f"3. Navigate to Contacts/Address Book")
        print(f"4. Export contacts to: {contacts_dir}")
        
        # Create contact categorization template
        contact_categories = {
            'potential_members': {
                'description': 'People who might be interested in joining the HueMan-i-Terry',
                'criteria': ['Interest in spirituality', 'Interest in personal growth', 'Kink community members', 'Alt community members']
            },
            'current_members': {
                'description': 'Current HueMan-i-Terry members',
                'criteria': ['Already part of community', 'Discord members', 'Twitter followers']
            },
            'collaborators': {
                'description': 'Potential collaborators and partners',
                'criteria': ['Content creators', 'Community leaders', 'Spiritual teachers', 'Artists']
            },
            'influencers': {
                'description': 'Influencers for amplification',
                'criteria': ['Social media presence', 'Relevant following', 'Authentic voice']
            }
        }
        
        # Create categorization file
        categorization_file = contacts_dir / "contact_categorization.json"
        with open(categorization_file, 'w') as f:
            json.dump(contact_categories, f, indent=2)
        
        # Create contact import template
        import_template = {
            'contact_import_template': {
                'name': 'Contact Name',
                'phone': 'Phone Number',
                'email': 'Email Address',
                'category': 'Category (potential_members, current_members, collaborators, influencers)',
                'notes': 'Notes about contact',
                'platform': 'Platform where connected (Twitter, Discord, etc.)',
                'archetype_interest': 'If interested, which archetype resonates?'
            }
        }
        
        template_file = contacts_dir / "import_template.json"
        with open(template_file, 'w') as f:
            json.dump(import_template, f, indent=2)
        
        print(f"\n✓ Created contact categorization guide: {categorization_file}")
        print(f"✓ Created contact import template: {template_file}")
        print(f"✓ Contacts directory ready: {contacts_dir}")
    
    def process_media(self):
        """Process media for content creation"""
        print("\n" + "=" * 60)
        print("Processing Media for Content Creation")
        print("=" * 60)
        
        media_dir = self.output_path / "media"
        
        # Create media organization structure
        media_structure = {
            'ritual_ceremonies': {
                'description': 'Recordings of rituals and ceremonies',
                'subfolders': ['audio', 'video', 'photos']
            },
            'wisdom_teachings': {
                'description': 'Wisdom teaching recordings',
                'subfolders': ['audio', 'video', 'transcripts']
            },
            'community_events': {
                'description': 'Community event recordings',
                'subfolders': ['audio', 'video', 'photos']
            },
            'archetype_content': {
                'description': 'Archetype-specific content',
                'subfolders': ['high_priest', 'divine_mother', 'seductive_muse', 'cosmic_mystic']
            },
            'behind_scenes': {
                'description': 'Behind-the-scenes content',
                'subfolders': ['bts_footage', 'bts_photos']
            }
        }
        
        # Create directory structure
        for category, details in media_structure.items():
            category_path = media_dir / category
            category_path.mkdir(exist_ok=True)
            
            for subfolder in details['subfolders']:
                (category_path / subfolder).mkdir(exist_ok=True)
        
        print(f"\nMedia Organization Structure:")
        for category, details in media_structure.items():
            print(f"  {category}/")
            print(f"    - {details['description']}")
            for subfolder in details['subfolders']:
                print(f"    - {subfolder}/")
        
        # Create media processing guide
        processing_guide = {
            'media_extraction': {
                'steps': [
                    'Open iPhone Backup Extractor',
                    'Select iPhone backup',
                    'Navigate to Media folder',
                    'Extract relevant media to organized folders'
                ]
            },
            'content_priorities': {
                'high_priority': [
                    'High-quality profile images for souls',
                    'Ritual ceremony recordings',
                    'Wisdom teaching videos',
                    'Community event footage'
                ],
                'medium_priority': [
                    'Behind-the-scenes content',
                    'Archetype-specific media',
                    'Audio recordings'
                ],
                'low_priority': [
                    'Personal photos',
                    'Random videos',
                    'Uncategorized media'
                ]
            },
            'formatting_requirements': {
                'profile_images': '400x400px minimum, 1080x1080px recommended',
                'header_images': '1500x500px for Twitter',
                'video_content': 'MP4 format, 1080p recommended',
                'audio_content': 'MP3 format, high quality'
            }
        }
        
        guide_file = media_dir / "processing_guide.json"
        with open(guide_file, 'w') as f:
            json.dump(processing_guide, f, indent=2)
        
        print(f"\n✓ Created media processing guide: {guide_file}")
        print(f"✓ Media directory structure created: {media_dir}")
    
    def process_other_data(self):
        """Process other useful data"""
        print("\n" + "=" * 60)
        print("Processing Other Useful Data")
        print("=" * 60)
        
        other_data_dir = self.output_path / "other_data"
        
        useful_data_types = {
            'notes': {
                'description': 'Notes app content for wisdom and teachings',
                'uses': ['Content creation', 'Wisdom posts', 'Teaching material']
            },
            'messages': {
                'description': 'Message threads for community insights',
                'uses': ['Community understanding', 'Common questions', 'Engagement insights']
            },
            'calendar': {
                'description': 'Calendar events for ritual scheduling',
                'uses': ['Event planning', 'Ritual timing', 'Community events']
            },
            'voice_memos': {
                'description': 'Voice memos for audio content',
                'uses': ['Podcast content', 'Wisdom recordings', 'Ritual audio']
            },
            'safari_bookmarks': {
                'description': 'Browser bookmarks for resources',
                'uses': ['Resource curation', 'Reference material', 'Sharing content']
            }
        }
        
        print(f"\nUseful Data Types to Extract:")
        for data_type, details in useful_data_types.items():
            print(f"  {data_type}:")
            print(f"    - {details['description']}")
            print(f"    - Uses: {', '.join(details['uses'])}")
        
        # Create data extraction guide
        extraction_guide = {
            'data_types': useful_data_types,
            'extraction_priority': {
                'high': ['notes', 'voice_memos'],
                'medium': ['calendar', 'safari_bookmarks'],
                'low': ['messages']
            },
            'privacy_considerations': [
                'Review all extracted data for personal information',
                'Remove sensitive data before sharing',
                'Obtain consent for using community messages',
                'Blur personal information in shared content'
            ],
            'processing_workflow': [
                'Extract data from iPhone backup',
                'Review and categorize extracted content',
                'Remove sensitive information',
                'Organize by content type and use case',
                'Integrate with content library'
            ]
        }
        
        guide_file = other_data_dir / "extraction_guide.json"
        with open(guide_file, 'w') as f:
            json.dump(extraction_guide, f, indent=2)
        
        print(f"\n✓ Created data extraction guide: {guide_file}")
        print(f"✓ Other data directory ready: {other_data_dir}")
    
    def create_integration_script(self):
        """Create script to integrate extracted data with social media setup"""
        print("\n" + "=" * 60)
        print("Creating Integration Script")
        print("=" * 60)
        
        integration_script = {
            'description': 'Integration workflow for iPhone backup data',
            'steps': [
                {
                    'step': 1,
                    'action': 'Extract profile images',
                    'tool': 'iPhone Backup Extractor',
                    'output': 'scripts/iphone_backup_data/profile_images/',
                    'integration': 'Rename images to match soul IDs for profile setup'
                },
                {
                    'step': 2,
                    'action': 'Extract contacts',
                    'tool': 'iPhone Backup Extractor',
                    'output': 'scripts/iphone_backup_data/contacts/',
                    'integration': 'Categorize contacts for community building outreach'
                },
                {
                    'step': 3,
                    'action': 'Extract media',
                    'tool': 'iPhone Backup Extractor',
                    'output': 'scripts/iphone_backup_data/media/',
                    'integration': 'Organize for content creation and posting'
                },
                {
                    'step': 4,
                    'action': 'Extract other data',
                    'tool': 'iPhone Backup Extractor',
                    'output': 'scripts/iphone_backup_data/other_data/',
                    'integration': 'Process for wisdom teachings and resources'
                },
                {
                    'step': 5,
                    'action': 'Integrate with social media setup',
                    'tool': 'Custom scripts',
                    'output': 'Updated social media setup files',
                    'integration': 'Update setup files with extracted data'
                }
            ],
            'next_actions': [
                'Run iPhone Backup Extractor and extract data',
                'Review extracted data and organize according to guides',
                'Process profile images for social media setup',
                'Categorize contacts for community building',
                'Organize media for content creation'
            ]
        }
        
        integration_file = self.output_path / "integration_workflow.json"
        with open(integration_file, 'w') as f:
            json.dump(integration_script, f, indent=2)
        
        print(f"\n✓ Created integration workflow: {integration_file}")
    
    def generate_master_plan(self):
        """Generate master processing plan"""
        print("\n" + "=" * 60)
        print("iPhone Backup Data Processing Master Plan")
        print("=" * 60)
        
        self.create_output_structure()
        self.process_profile_images()
        self.process_contacts()
        self.process_media()
        self.process_other_data()
        self.create_integration_script()
        
        # Create summary
        summary = {
            'backup_path': self.backup_path,
            'output_path': str(self.output_path),
            'processing_status': 'Ready for extraction',
            'next_steps': [
                'Open iPhone Backup Extractor application',
                'Select iPhone backup',
                'Extract data according to guides in each directory',
                'Organize extracted data',
                'Integrate with social media setup'
            ],
            'estimated_time': '2-4 hours for complete extraction and organization',
            'generated_at': datetime.now().isoformat()
        }
        
        summary_file = self.output_path / "processing_summary.json"
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"\n" + "=" * 60)
        print("iPhone Backup Processing Setup Complete")
        print("=" * 60)
        print(f"\nOutput Directory: {self.output_path}")
        print(f"Processing Status: Ready for extraction")
        print(f"\nNext Steps:")
        print(f"1. Open iPhone Backup Extractor at: {self.backup_path}")
        print(f"2. Follow guides in each subdirectory")
        print(f"3. Extract and organize data")
        print(f"4. Integrate with social media setup")

def main():
    """Main function to setup iPhone backup processing"""
    print("=" * 60)
    print("Tiapma'atzu HueMan-i-Terry iPhone Backup Data Processor")
    print("=" * 60)
    
    processor = iPhoneBackupProcessor()
    processor.generate_master_plan()

if __name__ == "__main__":
    main()