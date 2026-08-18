"""
Profile Setup Automation for Tiapma'atzu HueMan-i-Terry
Automated profile configuration scripts for all platforms
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

class ProfileSetupAutomation:
    """Automate profile setup for all souls across platforms"""
    
    def __init__(self):
        self.souls_data = self.load_souls_data()
        self.automation_scripts = self.create_automation_scripts()
    
    def load_souls_data(self) -> Dict[str, Any]:
        """Load souls data from JSON file"""
        souls_path = Path("src/data/souls_entities.json")
        with open(souls_path, 'r') as f:
            return json.load(f)
    
    def create_automation_scripts(self) -> Dict[str, Any]:
        """Create automation scripts for profile setup"""
        return {
            'discord_automation': self.create_discord_automation(),
            'twitter_automation': self.create_twitter_automation(),
            'reddit_automation': self.create_reddit_automation(),
            'instagram_automation': self.create_instagram_automation(),
            'batch_processing': self.create_batch_processing()
        }
    
    def create_discord_automation(self) -> Dict[str, Any]:
        """Create Discord profile automation"""
        return {
            'platform': 'Discord',
            'automation_type': 'manual_scripted',
            'steps': [
                {
                    'step': 1,
                    'action': 'Set Username',
                    'description': 'Configure Discord username with soul name',
                    'template': '{soul_name}#Tiapmaatzu',
                    'automation_level': 'manual'
                },
                {
                    'step': 2,
                    'action': 'Upload Profile Picture',
                    'description': 'Upload soul image as profile picture',
                    'image_specs': '512x512px',
                    'automation_level': 'manual'
                },
                {
                    'step': 3,
                    'action': 'Set Display Name',
                    'description': 'Configure display name as soul name',
                    'template': '{soul_name}',
                    'automation_level': 'manual'
                },
                {
                    'step': 4,
                    'action': 'Set Status Message',
                    'description': 'Configure status message with archetype and hook',
                    'template': '{archetype} | {hook}',
                    'automation_level': 'manual'
                },
                {
                    'step': 5,
                    'action': 'Configure Privacy Settings',
                    'description': 'Set privacy settings for optimal security',
                    'settings': {
                        'direct_messages': 'HueMan-i-Terry members only',
                        'friend_requests': 'Auto-accept HueMan-i-Terry members',
                        'activity_status': 'Visible to HueMan-i-Terry'
                    },
                    'automation_level': 'manual'
                }
            ],
            'prerequisites': [
                'Discord account created',
                'Email verified',
                '2FA enabled',
                'Profile image prepared'
            ],
            'estimated_time_per_account': '5 minutes'
        }
    
    def create_twitter_automation(self) -> Dict[str, Any]:
        """Create Twitter profile automation"""
        return {
            'platform': 'Twitter',
            'automation_type': 'manual_scripted',
            'steps': [
                {
                    'step': 1,
                    'action': 'Set Display Name',
                    'description': 'Configure display name as soul name',
                    'template': '{soul_name}',
                    'automation_level': 'manual'
                },
                {
                    'step': 2,
                    'action': 'Upload Profile Picture',
                    'description': 'Upload soul image as profile picture',
                    'image_specs': '400x400px',
                    'automation_level': 'manual'
                },
                {
                    'step': 3,
                    'action': 'Upload Header Image',
                    'description': 'Upload archetype-themed header image',
                    'image_specs': '1500x500px',
                    'automation_level': 'manual'
                },
                {
                    'step': 4,
                    'action': 'Write Bio',
                    'description': 'Write optimized bio with archetype and hook',
                    'template': '{archetype} | {hook} | {tribute_impact_short} | Join the transformation',
                    'max_length': 160,
                    'automation_level': 'semi_automated'
                },
                {
                    'step': 5,
                    'action': 'Set Website Link',
                    'description': 'Configure website link to HueMan-i-Terry landing page',
                    'template': 'https://tiapmaatzu.web.app',
                    'automation_level': 'manual'
                },
                {
                    'step': 6,
                    'action': 'Set Location',
                    'description': 'Set location to archetype location',
                    'template': '{archetype_location}',
                    'automation_level': 'manual'
                },
                {
                    'step': 7,
                    'action': 'Pin Introduction Tweet',
                    'description': 'Create and pin introduction tweet',
                    'template': 'Welcome to my journey as {archetype} of the Tiapma\'atzu HueMan-i-Terry. {hook}',
                    'automation_level': 'manual'
                }
            ],
            'prerequisites': [
                'Twitter account created',
                'Email verified',
                'Phone verified',
                '2FA enabled',
                'Profile and header images prepared'
            ],
            'estimated_time_per_account': '8 minutes'
        }
    
    def create_reddit_automation(self) -> Dict[str, Any]:
        """Create Reddit profile automation"""
        return {
            'platform': 'Reddit',
            'automation_type': 'manual_scripted',
            'steps': [
                {
                    'step': 1,
                    'action': 'Set Username',
                    'description': 'Username is set during account creation',
                    'template': '{soul_name_no_spaces}_Tiapmaatzu',
                    'automation_level': 'manual'
                },
                {
                    'step': 2,
                    'action': 'Write Bio',
                    'description': 'Write detailed bio with archetype and role',
                    'template': '{archetype} of the Tiapma\'atzu HueMan-i-Terry. {hook}. {tribute_impact}. Join the transformation: Discord link',
                    'max_length': 500,
                    'automation_level': 'semi_automated'
                },
                {
                    'step': 3,
                    'action': 'Configure Profile Settings',
                    'description': 'Set profile preferences and settings',
                    'settings': {
                        'allow_followers': 'True',
                        'content_visibility': 'Public',
                        'profile_over_18': 'Set based on content nature'
                    },
                    'automation_level': 'manual'
                },
                {
                    'step': 4,
                    'action': 'Add Social Media Links',
                    'description': 'Add links to other social media profiles',
                    'links': ['Twitter', 'Discord', 'Instagram'],
                    'automation_level': 'manual'
                },
                {
                    'step': 5,
                    'action': 'Set Location',
                    'description': 'Set location to archetype location',
                    'template': '{archetype_location}',
                    'automation_level': 'manual'
                }
            ],
            'prerequisites': [
                'Reddit account created',
                'Email verified',
                '2FA enabled',
                'Initial karma built'
            ],
            'estimated_time_per_account': '6 minutes'
        }
    
    def create_instagram_automation(self) -> Dict[str, Any]:
        """Create Instagram profile automation"""
        return {
            'platform': 'Instagram',
            'automation_type': 'manual_scripted',
            'steps': [
                {
                    'step': 1,
                    'action': 'Switch to Creator Account',
                    'description': 'Switch account type to Creator',
                    'automation_level': 'manual'
                },
                {
                    'step': 2,
                    'action': 'Set Display Name',
                    'description': 'Configure display name as soul name',
                    'template': '{soul_name}',
                    'automation_level': 'manual'
                },
                {
                    'step': 3,
                    'action': 'Upload Profile Picture',
                    'description': 'Upload soul image as profile picture',
                    'image_specs': '110x110px minimum, 1080x1080px recommended',
                    'automation_level': 'manual'
                },
                {
                    'step': 4,
                    'action': 'Write Bio',
                    'description': 'Write optimized bio with archetype and hook',
                    'template': '{archetype} | {hook} | {tribute_impact_short} | Link in bio for HueMan-i-Terry',
                    'max_length': 150,
                    'automation_level': 'semi_automated'
                },
                {
                    'step': 5,
                    'action': 'Set Website Link',
                    'description': 'Configure website link to HueMan-i-Terry landing page',
                    'template': 'https://tiapmaatzu.web.app',
                    'automation_level': 'manual'
                },
                {
                    'step': 6,
                    'action': 'Set Contact Button',
                    'description': 'Configure contact button for email',
                    'template': 'Email',
                    'automation_level': 'manual'
                },
                {
                    'step': 7,
                    'action': 'Create Story Highlights',
                    'description': 'Create initial story highlights',
                    'highlights': ['About Me', 'Wisdom', 'Rituals', 'HueMan-i-Terry', 'Impact'],
                    'automation_level': 'manual'
                },
                {
                    'step': 8,
                    'action': 'Configure Category',
                    'description': 'Set account category',
                    'template': 'Creator',
                    'automation_level': 'manual'
                }
            ],
            'prerequisites': [
                'Instagram account created',
                'Email verified',
                'Phone verified',
                '2FA enabled',
                'Creator account enabled',
                'Profile image prepared'
            ],
            'estimated_time_per_account': '10 minutes'
        }
    
    def create_batch_processing(self) -> Dict[str, Any]:
        """Create batch processing automation"""
        return {
            'description': 'Batch processing for multiple accounts',
            'strategy': 'Process accounts in batches by platform',
            'batch_sizes': {
                'discord': 5,
                'twitter': 5,
                'reddit': 3,
                'instagram': 2
            },
            'processing_order': [
                'Phase 1: Process Discord accounts (3 batches)',
                'Phase 2: Process Twitter accounts (4 batches)',
                'Phase 3: Process Reddit accounts (4 batches)',
                'Phase 4: Process Instagram accounts (4 batches)'
            ],
            'quality_control': {
                'inter_batch_review': 'Review each batch before proceeding',
                'final_verification': 'Final verification of all accounts',
                'error_handling': 'Document and resolve errors immediately'
            }
        }
    
    def generate_soul_profile_automation(self, soul_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate profile automation for a specific soul"""
        soul_id = soul_data['id']
        soul_name = soul_data['name']
        archetype = soul_data['archetype']
        platforms = soul_data.get('platforms', [])
        hooks = soul_data.get('hooks', [])
        tribute_impact = soul_data.get('tribute_impact', '')
        
        automation = {
            'soul_id': soul_id,
            'name': soul_name,
            'archetype': archetype,
            'platform_automation': {},
            'estimated_total_time': 0
        }
        
        total_time = 0
        
        for platform in platforms:
            platform_automation = self.get_platform_automation(platform)
            
            # Fill in templates with soul data
            filled_automation = self.fill_templates(platform_automation, soul_data)
            
            automation['platform_automation'][platform] = filled_automation
            
            # Add estimated time
            if 'estimated_time_per_account' in platform_automation:
                time_str = platform_automation['estimated_time_per_account']
                time_value = int(time_str.split()[0])
                total_time += time_value
        
        automation['estimated_total_time'] = f"{total_time} minutes"
        
        return automation
    
    def get_platform_automation(self, platform: str) -> Dict[str, Any]:
        """Get automation for specific platform"""
        platform_automations = {
            'Discord': self.automation_scripts['discord_automation'],
            'Twitter': self.automation_scripts['twitter_automation'],
            'Reddit': self.automation_scripts['reddit_automation'],
            'Instagram': self.automation_scripts['instagram_automation']
        }
        
        return platform_automations.get(platform, {})
    
    def fill_templates(self, automation: Dict[str, Any], soul_data: Dict[str, Any]) -> Dict[str, Any]:
        """Fill templates with soul data"""
        soul_name = soul_data['name']
        archetype = soul_data['archetype']
        hooks = soul_data.get('hooks', [])
        tribute_impact = soul_data.get('tribute_impact', '')
        
        # Get archetype location
        archetype_location = self.get_archetype_location(archetype)
        
        # Shorten tribute impact for bios
        tribute_impact_short = tribute_impact[:30] if tribute_impact else 'Building HueMan-i-Terry prosperity'
        
        filled_automation = automation.copy()
        
        # Fill templates in steps
        if 'steps' in filled_automation:
            for step in filled_automation['steps']:
                if 'template' in step:
                    template = step['template']
                    filled_template = template.format(
                        soul_name=soul_name,
                        soul_name_no_spaces=soul_name.replace(' ', ''),
                        archetype=archetype,
                        hook=hooks[0] if hooks else 'Transforming through primal wisdom',
                        tribute_impact_short=tribute_impact_short,
                        tribute_impact=tribute_impact,
                        archetype_location=archetype_location
                    )
                    step['filled_value'] = filled_template
        
        return filled_automation
    
    def get_archetype_location(self, archetype: str) -> str:
        """Get location based on archetype"""
        locations = {
            'High Priest': 'Temple of Transformation',
            'Divine Mother': 'Garden of Nurturing',
            'Seductive Muse': 'Gallery of Desire',
            'Cosmic Mystic': 'Observatory of Stars',
            'Revolutionary Warrior': 'Barricade of Change',
            'Crypto Sorceress': 'Vault of Secrets',
            'Community Healer': 'Sanctuary of Healing',
            'Digital Guardian': 'Fortress of Protection',
            'Digital Phantom': 'Shadow Network',
            'Connection Curator': 'Web of Connection',
            'Viral Prophet': 'Amplifier of Truth',
            'Cyber Guardian': 'Shield of Code',
            'Visual Alchemist': 'Canvas of Vision',
            'Prism Enchantress': 'Palace of Light',
            'Desert Storyteller': 'Oasis of Tales',
            'Ephemeral Artist': 'House of Moments',
            'Mirror Architect': 'Hall of Reflections',
            'Sage Writer': 'Library of Wisdom',
            'Scavenger Strategist': 'Den of Opportunity',
            'Wild Surrender': 'Wilderness of Freedom',
            'Contractual Warden': 'Court of Order',
            'Ephemeral Phantom': 'Veil of Mystery',
            'Temporal Architect': 'Tower of Time',
            'Digital Deity': 'Grid of Energy',
            'Gothic Matriarch': 'Manor of Shadows',
            'Hyper-Capitalist': 'Empire of Wealth',
            'Machine Spirit': 'Factory of Output'
        }
        
        return locations.get(archetype, 'Tiapma\'atzu HueMan-i-Terry')
    
    def generate_master_automation_plan(self) -> Dict[str, Any]:
        """Generate master automation plan"""
        master_plan = {
            'automation_scripts': self.automation_scripts,
            'soul_automation': {},
            'execution_timeline': self.create_execution_timeline(),
            'quality_control': self.create_quality_control(),
            'generated_at': datetime.now().isoformat()
        }
        
        for soul in self.souls_data['souls']:
            soul_automation = self.generate_soul_profile_automation(soul)
            master_plan['soul_automation'][soul['id']] = soul_automation
        
        return master_plan
    
    def create_execution_timeline(self) -> Dict[str, Any]:
        """Create execution timeline for profile setup"""
        return {
            'day_1': {
                'focus': 'Discord Profile Setup',
                'platform': 'Discord',
                'accounts': 15,
                'batches': 3,
                'estimated_time': '75 minutes (5 min per account)',
                'process': 'Process 5 accounts per batch with quality review'
            },
            'day_2': {
                'focus': 'Twitter Profile Setup',
                'platform': 'Twitter',
                'accounts': 20,
                'batches': 4,
                'estimated_time': '160 minutes (8 min per account)',
                'process': 'Process 5 accounts per batch with quality review'
            },
            'day_3': {
                'focus': 'Reddit Profile Setup',
                'platform': 'Reddit',
                'accounts': 10,
                'batches': 4,
                'estimated_time': '60 minutes (6 min per account)',
                'process': 'Process 3 accounts per batch with quality review'
            },
            'day_4': {
                'focus': 'Instagram Profile Setup',
                'platform': 'Instagram',
                'accounts': 8,
                'batches': 4,
                'estimated_time': '80 minutes (10 min per account)',
                'process': 'Process 2 accounts per batch with quality review'
            },
            'day_5': {
                'focus': 'Final Verification',
                'platform': 'All',
                'accounts': 66,
                'estimated_time': '120 minutes',
                'process': 'Final quality check and cross-platform verification'
            }
        }
    
    def create_quality_control(self) -> Dict[str, Any]:
        """Create quality control procedures"""
        return {
            'pre_setup_checks': [
                'Verify account is created and accessible',
                'Confirm email/phone verification',
                'Verify 2FA is enabled',
                'Check profile images are ready',
                'Confirm soul data is accurate'
            ],
            'during_setup_checks': [
                'Verify each step is completed correctly',
                'Check character limits are respected',
                'Confirm images upload successfully',
                'Verify links work correctly',
                'Check formatting is consistent'
            ],
            'post_setup_checks': [
                'Review complete profile',
                'Verify all fields are filled',
                'Check cross-platform consistency',
                'Test account functionality',
                'Document any issues'
            ],
            'error_handling': [
                'Document errors immediately',
                'Create error log with details',
                'Implement fix and verify',
                'Prevent similar errors in future'
            ]
        }

def main():
    """Main function to generate profile automation"""
    print("=" * 60)
    print("Tiapma'atzu HueMan-i-Terry Profile Setup Automation")
    print("=" * 60)
    
    automation = ProfileSetupAutomation()
    
    # Generate master automation plan
    master_plan = automation.generate_master_automation_plan()
    
    print(f"\nTotal Souls: {len(master_plan['soul_automation'])}")
    print(f"Total Accounts to Configure: 66 (15 Discord + 20 Twitter + 10 Reddit + 8 Instagram)")
    
    print("\nExecution Timeline:")
    for day, details in master_plan['execution_timeline'].items():
        print(f"  {day}: {details['focus']} ({details['accounts']} accounts, {details['estimated_time']})")
    
    total_time = sum(int(details['estimated_time'].split()[0]) for details in master_plan['execution_timeline'].values())
    print(f"\nTotal Estimated Time: {total_time} minutes ({total_time/60:.1f} hours)")
    
    # Save master automation plan
    output_path = Path("scripts/profile_automation_master_plan.json")
    with open(output_path, 'w') as f:
        json.dump(master_plan, f, indent=2, default=str)
    
    print(f"\n✓ Master automation plan saved to {output_path}")
    
    # Generate individual automation scripts
    for soul_id, soul_automation in master_plan['soul_automation'].items():
        individual_path = Path(f"scripts/profile_automation_{soul_id}.json")
        with open(individual_path, 'w') as f:
            json.dump(soul_automation, f, indent=2, default=str)
    
    print(f"✓ Individual automation scripts saved for all {len(master_plan['soul_automation'])} souls")
    
    print("\n" + "=" * 60)
    print("Profile Setup Automation Complete")
    print("=" * 60)

if __name__ == "__main__":
    main()