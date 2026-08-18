"""
Master Integration Script for iPhone Backup Data
Integrates extracted images, contacts, and media with social media setup
"""

import json
import os
import shutil
from pathlib import Path
from typing import Dict, List
from datetime import datetime

class DataIntegrator:
    """Integrate extracted iPhone backup data with social media setup"""
    
    def __init__(self):
        self.base_path = Path("scripts/iphone_backup_data")
        self.project_root = Path(".")
        self.souls_data_file = self.project_root / "src/data/souls_entities.json"
        self.social_media_setup_dir = self.project_root / "scripts/social_media_setup"
        
    def load_souls_data(self) -> Dict:
        """Load souls entities data"""
        if self.souls_data_file.exists():
            with open(self.souls_data_file, 'r') as f:
                return json.load(f)
        return {}
    
    def check_extraction_status(self) -> Dict:
        """Check status of all extractions"""
        print("\n" + "=" * 60)
        print("Checking Extraction Status")
        print("=" * 60)
        
        status = {
            'profile_images': False,
            'contacts': False,
            'media': False,
            'other_data': False
        }
        
        # Check profile images
        profile_images_dir = self.base_path / "profile_images"
        image_mapping = profile_images_dir / "image_mapping.json"
        if image_mapping.exists():
            with open(image_mapping, 'r') as f:
                mapping = json.load(f)
            found_images = len(list(profile_images_dir.glob("*.png")))
            status['profile_images'] = found_images > 0
            print(f"Profile Images: {found_images} found (need {len(mapping)})")
        
        # Check contacts
        contacts_dir = self.base_path / "contacts"
        contact_files = list(contacts_dir.glob("*.vcf")) + list(contacts_dir.glob("*.csv"))
        status['contacts'] = len(contact_files) > 0
        print(f"Contacts: {len(contact_files)} files found")
        
        # Check media
        media_dir = self.base_path / "media"
        media_files = list(media_dir.rglob("*"))
        media_files = [f for f in media_files if f.is_file()]
        status['media'] = len(media_files) > 0
        print(f"Media: {len(media_files)} files found")
        
        # Check other data
        other_data_dir = self.base_path / "other_data"
        other_files = list(other_data_dir.rglob("*"))
        other_files = [f for f in other_files if f.is_file()]
        status['other_data'] = len(other_files) > 0
        print(f"Other Data: {len(other_files)} files found")
        
        return status
    
    def integrate_profile_images(self):
        """Integrate profile images with social media setup"""
        print("\n" + "=" * 60)
        print("Integrating Profile Images with Social Media Setup")
        print("=" * 60)
        
        profile_images_dir = self.base_path / "profile_images"
        platform_dirs = ['discord', 'twitter_profile', 'reddit', 'instagram']
        
        # Check if platform-specific directories exist
        integrated_count = 0
        for platform in platform_dirs:
            platform_dir = profile_images_dir / platform
            if platform_dir.exists():
                images = list(platform_dir.glob("*.png"))
                integrated_count += len(images)
                print(f"✓ {platform}: {len(images)} images ready")
        
        if integrated_count > 0:
            print(f"\n✓ {integrated_count} profile images integrated")
            
            # Update souls data with local image paths
            souls_data = self.load_souls_data()
            if souls_data and 'souls' in souls_data:
                for soul in souls_data['souls']:
                    soul_id = soul['id']
                    expected_image = soul.get('image', '').split('/')[-1]
                    
                    # Check if image exists in any platform directory
                    for platform in platform_dirs:
                        platform_dir = profile_images_dir / platform
                        image_path = platform_dir / expected_image
                        if image_path.exists():
                            # Add local path to soul data
                            if 'local_images' not in soul:
                                soul['local_images'] = {}
                            soul['local_images'][platform] = str(image_path)
                
                # Backup and update souls data
                backup_file = self.souls_data_file.with_suffix('.json.backup')
                shutil.copy(self.souls_data_file, backup_file)
                
                with open(self.souls_data_file, 'w') as f:
                    json.dump(souls_data, f, indent=2)
                
                print(f"✓ Updated souls data with local image paths")
                print(f"✓ Backup created: {backup_file}")
        else:
            print("⚠ No platform-specific images found. Run image processing first.")
    
    def integrate_contacts(self):
        """Integrate contacts with community building setup"""
        print("\n" + "=" * 60)
        print("Integrating Contacts with Community Building")
        print("=" * 60)
        
        contacts_dir = self.base_path / "contacts"
        outreach_files = ['immediate_outreach.json', 'collaboration_opportunities.json', 
                         'influencer_outreach.json']
        
        integrated_count = 0
        for outreach_file in outreach_files:
            file_path = contacts_dir / outreach_file
            if file_path.exists():
                with open(file_path, 'r') as f:
                    data = json.load(f)
                contact_count = len(data.get('contacts', []))
                integrated_count += contact_count
                print(f"✓ {outreach_file}: {contact_count} contacts")
        
        if integrated_count > 0:
            print(f"\n✓ {integrated_count} contacts integrated for outreach")
            
            # Create community building plan
            community_plan = {
                'outreach_strategy': {
                    'immediate_outreach': {
                        'description': 'Reach out to potential members',
                        'estimated_contacts': 0,
                        'platforms': ['Twitter', 'Discord', 'Instagram']
                    },
                    'collaboration_outreach': {
                        'description': 'Connect with potential collaborators',
                        'estimated_contacts': 0,
                        'platforms': ['Twitter DM', 'Email', 'Discord']
                    },
                    'influencer_outreach': {
                        'description': 'Engage influencers for amplification',
                        'estimated_contacts': 0,
                        'platforms': ['Twitter', 'Instagram', 'Email']
                    }
                },
                'created_at': datetime.now().isoformat()
            }
            
            # Update counts from actual data
            for outreach_file in outreach_files:
                file_path = contacts_dir / outreach_file
                if file_path.exists():
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                    key = outreach_file.replace('.json', '')
                    if key in community_plan['outreach_strategy']:
                        community_plan['outreach_strategy'][key]['estimated_contacts'] = len(data.get('contacts', []))
            
            plan_file = contacts_dir / 'community_outreach_plan.json'
            with open(plan_file, 'w') as f:
                json.dump(community_plan, f, indent=2)
            
            print(f"✓ Community outreach plan created: {plan_file}")
        else:
            print("⚠ No organized contacts found. Run contact processing first.")
    
    def integrate_media(self):
        """Integrate media with content library"""
        print("\n" + "=" * 60)
        print("Integrating Media with Content Library")
        print("=" * 60)
        
        media_dir = self.base_path / "media"
        inventory_file = media_dir / "content_inventory.json"
        
        if inventory_file.exists():
            with open(inventory_file, 'r') as f:
                inventory = json.load(f)
            
            print(f"✓ Total media files: {inventory['total_files']}")
            print(f"✓ Categories organized: {len(inventory['categories'])}")
            
            # Create content library integration
            content_library = {
                'media_inventory': inventory,
                'posting_schedule': {
                    'high_priority': [],
                    'medium_priority': [],
                    'low_priority': []
                },
                'platform_distribution': {
                    'twitter': {'video': True, 'image': True, 'text': True},
                    'instagram': {'video': True, 'image': True, 'stories': True},
                    'discord': {'video': True, 'image': True, 'audio': True},
                    'reddit': {'image': True, 'text': True, 'video': True}
                },
                'created_at': datetime.now().isoformat()
            }
            
            # Load content calendar suggestions
            suggestions_file = media_dir / "content_calendar_suggestions.json"
            if suggestions_file.exists():
                with open(suggestions_file, 'r') as f:
                    suggestions = json.load(f)
                content_library['posting_schedule'] = suggestions
            
            # Save integrated content library
            library_file = media_dir / 'integrated_content_library.json'
            with open(library_file, 'w') as f:
                json.dump(content_library, f, indent=2)
            
            print(f"✓ Integrated content library created: {library_file}")
        else:
            print("⚠ No media inventory found. Run media processing first.")
    
    def create_master_integration_report(self, status: Dict):
        """Create comprehensive integration report"""
        print("\n" + "=" * 60)
        print("Creating Master Integration Report")
        print("=" * 60)
        
        report = {
            'integration_summary': {
                'extraction_status': status,
                'integration_complete': all(status.values()),
                'integrated_at': datetime.now().isoformat()
            },
            'components': {
                'profile_images': {
                    'status': 'integrated' if status['profile_images'] else 'pending',
                    'description': 'Profile images ready for social media setup'
                },
                'contacts': {
                    'status': 'integrated' if status['contacts'] else 'pending',
                    'description': 'Contacts organized for community outreach'
                },
                'media': {
                    'status': 'integrated' if status['media'] else 'pending',
                    'description': 'Media organized for content library'
                },
                'other_data': {
                    'status': 'integrated' if status['other_data'] else 'pending',
                    'description': 'Additional data extracted for reference'
                }
            },
            'next_steps': [],
            'social_media_setup_readiness': {
                'discord': status['profile_images'],  # Needs profile images
                'twitter': status['profile_images'],   # Needs profile images
                'reddit': status['profile_images'],   # Needs profile images
                'instagram': status['profile_images']  # Needs profile images
            }
        }
        
        # Generate next steps based on status
        if not status['profile_images']:
            report['next_steps'].append('Extract and process profile images from iPhone backup')
        if not status['contacts']:
            report['next_steps'].append('Export and categorize contacts from iPhone backup')
        if not status['media']:
            report['next_steps'].append('Extract and organize media from iPhone backup')
        
        if all(status.values()):
            report['next_steps'].extend([
                'Run social media account creation scripts',
                'Execute profile setup automation',
                'Begin content posting using integrated media library',
                'Start community outreach using contact lists'
            ])
        
        # Save report
        report_file = self.base_path / 'master_integration_report.json'
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"✓ Master integration report saved: {report_file}")
        
        # Print summary
        print(f"\nIntegration Summary:")
        print(f"  Profile Images: {'✓' if status['profile_images'] else '○'}")
        print(f"  Contacts: {'✓' if status['contacts'] else '○'}")
        print(f"  Media: {'✓' if status['media'] else '○'}")
        print(f"  Other Data: {'✓' if status['other_data'] else '○'}")
        print(f"\nIntegration Complete: {'Yes' if all(status.values()) else 'Partial'}")
        
        if not all(status.values()):
            print(f"\nNext Steps:")
            for step in report['next_steps']:
                print(f"  - {step}")
    
    def run_full_integration(self):
        """Run complete integration workflow"""
        print("=" * 60)
        print("iPhone Backup Data Master Integration")
        print("=" * 60)
        
        # Step 1: Check extraction status
        status = self.check_extraction_status()
        
        # Step 2: Integrate components
        if status['profile_images']:
            self.integrate_profile_images()
        
        if status['contacts']:
            self.integrate_contacts()
        
        if status['media']:
            self.integrate_media()
        
        # Step 3: Create master report
        self.create_master_integration_report(status)
        
        print("\n" + "=" * 60)
        print("Integration Workflow Complete")
        print("=" * 60)
        print(f"\nAll integration files saved to: {self.base_path}")
        print(f"Master report: {self.base_path}/master_integration_report.json")

def main():
    """Main function"""
    print("iPhone Backup Data Master Integration")
    print("This script integrates extracted data with social media setup\n")
    
    integrator = DataIntegrator()
    integrator.run_full_integration()

if __name__ == "__main__":
    main()
