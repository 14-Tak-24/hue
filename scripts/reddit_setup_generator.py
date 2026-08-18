"""
Reddit Setup Generator for Tiapma'atzu Souls
Generates individualized Reddit setup instructions for each soul
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

class RedditSetupGenerator:
    """Generate Reddit setup instructions for each soul"""
    
    def __init__(self):
        self.souls_data = self.load_souls_data()
        self.reddit_config = self.create_reddit_configuration()
    
    def load_souls_data(self) -> Dict[str, Any]:
        """Load souls data from JSON file"""
        souls_path = Path("src/data/souls_entities.json")
        with open(souls_path, 'r') as f:
            return json.load(f)
    
    def create_reddit_configuration(self) -> Dict[str, Any]:
        """Create Reddit-specific configuration"""
        return {
            'account_setup': self.create_account_setup_config(),
            'profile_optimization': self.create_profile_optimization(),
            'subreddit_strategy': self.create_subreddit_strategy(),
            'content_strategy': self.create_content_strategy(),
            'engagement_tactics': self.create_engagement_tactics(),
            'moderation_setup': self.create_moderation_setup(),
            'growth_strategy': self.create_growth_strategy()
        }
    
    def create_account_setup_config(self) -> Dict[str, Any]:
        """Create Reddit account setup configuration"""
        return {
            'naming_conventions': {
                'format': 'SoulName_Tiapmaatzu',
                'alternatives': ['SoulNameHueMan-i-Terry', 'Archetype_SoulName', 'TiapmaatzuSoulName'],
                'length_limit': '20 characters maximum',
                'case_sensitive': 'True',
                'special_chars': 'Only underscores allowed'
            },
            'verification_requirements': {
                'email': 'Required - use HueMan-i-Terry email',
                'email_verification': 'Must verify email before posting',
                'password_requirements': '8+ characters',
                'two_factor': 'Enable authenticator app (recommended)'
            },
            'initial_settings': {
                'allow_followers': 'True',
                'content_visibility': 'Public for growth',
                'profile_over_18': 'Set appropriately based on content',
                'nsfw_content': 'Mark appropriately if needed',
                'karma_thresholds': 'Set for posting in some subreddits'
            }
        }
    
    def create_profile_optimization(self) -> Dict[str, Any]:
        """Create Reddit profile optimization guidelines"""
        return {
            'profile_picture': {
                'specs': 'Reddit auto-generates from username',
                'customization': 'Limited avatar options (Premium)',
                'alternative': 'Use consistent image in subreddit banners'
            },
            'banner_image': {
                'specs': '1920x480px for subreddit banners',
                'format': 'JPG or PNG',
                'style': 'Archetype-themed with tribal branding',
                'availability': 'For subreddits, not profile'
            },
            'bio': {
                'length_limit': '500 characters',
                'structure': '{archetype} | {hook} | {value_proposition} | {call_to_action}',
                'formatting': 'Markdown supported',
                'links': 'Include Discord and other social links'
            },
            'profile_overview': {
                'display_name': 'Use soul name',
                'description': 'Detailed description of archetype and HueMan-i-Terry role',
                'links': 'Add all social media profiles',
                'location': 'Set spiritual or tribal location'
            }
        }
    
    def create_subreddit_strategy(self) -> Dict[str, Any]:
        """Create subreddit strategy"""
        return {
            'main_subreddit': {
                'name': 'r/Tiapmaatzu',
                'purpose': 'Main HueMan-i-Terry subreddit for all souls',
                'focus': 'General HueMan-i-Terry content, announcements, community',
                'moderation': 'High Council moderation',
                'posting_rules': 'Tribal guidelines and consent protocols'
            },
            'archetype_subreddits': {
                'naming': 'r/ArchetypeName',
                'purpose': 'Archetype-specific content and community',
                'creation': 'Create for each major archetype',
                'moderation': 'Archetype soul moderation',
                'focus': 'Archetype-specific discussions and content'
            },
            'posting_strategy': {
                'main_subreddit': 'Daily posts, engagement, announcements',
                'archetype_subreddits': 'Weekly deep dives, Q&A, resources',
                'crossposting': 'Share between main and archetype subreddits',
                'timing': 'Best times: 8 AM, 12 PM, 7 PM EST'
            }
        }
    
    def create_content_strategy(self) -> Dict[str, Any]:
        """Create Reddit content strategy"""
        return {
            'content_types': {
                'text_posts': {
                    'frequency': '2-3 weekly',
                    'length': 'Detailed discussions and wisdom sharing',
                    'purpose': 'Share archetype wisdom and insights',
                    'format': 'Compelling title + detailed content + call to action'
                },
                'link_posts': {
                    'frequency': '1-2 weekly',
                    'types': ['Blog posts', 'External content', 'Resources'],
                    'purpose': 'Drive traffic to HueMan-i-Terry content',
                    'format': 'Engaging title + link + discussion prompt'
                },
                'image_posts': {
                    'frequency': '2-3 weekly',
                    'types': ['Infographics', 'Soul images', 'Archetype art'],
                    'purpose': 'Visual storytelling and engagement',
                    'format': 'Compelling title + image + discussion'
                },
                'video_posts': {
                    'frequency': '1 weekly',
                    'types': ['YouTube videos', 'Ritual recordings', 'Educational content'],
                    'purpose': 'Share dynamic content and rituals',
                    'format': 'Engaging title + video + discussion'
                },
                'ama_sessions': {
                    'frequency': 'Monthly',
                    'purpose': 'Direct engagement with community',
                    'format': 'Scheduled AMA with Q&A focus',
                    'promotion': 'Announce 1 week in advance'
                }
            },
            'posting_schedule': {
                'optimal_times': ['8 AM', '12 PM', '7 PM EST'],
                'frequency': '4-5 posts weekly per soul',
                'consistency': 'Maintain consistent posting schedule',
                'subreddit_rotation': 'Rotate between main and archetype subreddits'
            },
            'subreddit_guidelines': {
                'r/Tiapmaatzu': 'General HueMan-i-Terry content, announcements, community',
                'r/ShadowWork': 'Shadow work discussions and support',
                'r/PrimalWisdom': 'Primal wisdom and teachings',
                'r/HueMan-i-TerryTransformation': 'Transformation stories and support'
            }
        }
    
    def create_engagement_tactics(self) -> Dict[str, Any]:
        """Create Reddit engagement tactics"""
        return {
            'community_engagement': {
                'response_time': 'Within 24 hours for HueMan-i-Terry member comments',
                'response_style': 'Thoughtful, detailed, archetype-appropriate',
                'upvoting': 'Upvote valuable HueMan-i-Terry and community content',
                'discussion': 'Engage in meaningful discussions'
            },
            'cross_subreddit': {
                'participation': 'Engage in relevant subreddits',
                'value_first': 'Provide value before self-promotion',
                'relevant_subreddits': [
                    'r/spirituality',
                    'r/meditation',
                    'r/personalgrowth',
                    'r/relationship_advice',
                    'r/kink',
                    'r/BDSMcommunity'
                ],
                'guidelines': 'Follow subreddit rules, contribute meaningfully'
            },
            'community_building': {
                'flair_system': 'Create archetype and role flairs',
                'user_flairs': 'Assign flairs for HueMan-i-Terry members',
                'moderation': 'Fair and consistent moderation',
                'events': 'Host Reddit events and AMAs'
            }
        }
    
    def create_moderation_setup(self) -> Dict[str, Any]:
        """Create Reddit moderation setup"""
        return {
            'moderation_tools': [
                'AutoModerator',
                'Toolbox (Reddit Pro)',
                'Reddit Moderation Toolbox',
                'Streamlines'
            ],
            'moderation_protocols': {
                'content_review': 'Review all posts for guideline compliance',
                'spam_filtering': 'Configure spam filters appropriately',
                'user_reports': 'Respond to user reports promptly',
                'escalation': 'Clear escalation procedures for issues'
            },
            'rule_structure': {
                'general_rules': [
                    'Respect all community members',
                    'No hate speech or discrimination',
                    'Consent and boundaries must be respected',
                    'No doxxing or sharing personal information',
                    'Constructive disagreement only'
                ],
                'content_rules': [
                    'All content must be relevant to HueMan-i-Terry',
                    'Mark NSFW content appropriately',
                    'No unauthorized commercial promotion',
                    'Credit original content creators',
                    'Follow Reddit content policy'
                ]
            }
        }
    
    def create_growth_strategy(self) -> Dict[str, Any]:
        """Create Reddit growth strategy"""
        return {
            'growth_phases': {
                'phase_1_month_1': {
                    'focus': 'Foundation Building',
                    'goals': ['1,000 karma', '500 subscribers', 'Active community'],
                    'tactics': ['Post consistently', 'Engage with community', 'Build initial content library']
                },
                'phase_2_month_2': {
                    'focus': 'Content Expansion',
                    'goals': ['5,000 karma', '1,000 subscribers', 'Regular engagement'],
                    'tactics': ['Increase post frequency', 'Create AMAs', 'Cross-promote on other platforms']
                },
                'phase_3_month_3': {
                    'focus': 'Community Scaling',
                    'goals': ['10,000 karma', '2,500 subscribers', 'Viral content'],
                    'tactics': ['Viral content creation', 'Collaborative posts', 'Advanced moderation']
                },
                'phase_4_month_4': {
                    'focus': 'Influence Building',
                    'goals': ['25,000 karma', '5,000 subscribers', 'Thought leadership'],
                    'tactics': ['Guest posting', 'Network growth', 'Content partnerships']
                }
            },
            'growth_tactics': {
                'organic': [
                    'Consistent high-quality posts',
                    'Engage with subreddit communities',
                    'Participate in trending discussions',
                    'Optimize posting times',
                    'Use compelling titles'
                ],
                'strategic': [
                    'Post in high-traffic subreddits',
                    'Cross-promote strategically',
                    'Leverage viral content',
                    'Optimize for Reddit algorithm',
                    'Build karma first'
                ],
                'community': [
                    'Host AMAs regularly',
                    'Create series content',
                    'Build subscriber loyalty',
                    'Encourage user-generated content',
                    'Foster community culture'
                ]
            }
        }
    
    def generate_soul_reddit_setup(self, soul_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate individualized Reddit setup for a soul"""
        soul_id = soul_data['id']
        soul_name = soul_data['name']
        archetype = soul_data['archetype']
        
        setup = {
            'soul_id': soul_id,
            'name': soul_name,
            'archetype': archetype,
            'account_setup': self.generate_reddit_account_setup(soul_data),
            'profile_optimization': self.generate_reddit_profile_optimization(soul_data),
            'subreddit_setup': self.generate_subreddit_setup(soul_data),
            'content_strategy': self.generate_reddit_content_strategy(soul_data),
            'engagement_strategy': self.generate_reddit_engagement_strategy(soul_data),
            'moderation_setup': self.generate_moderation_setup_for_soul(soul_data),
            'growth_targets': self.generate_reddit_growth_targets(soul_data)
        }
        
        return setup
    
    def generate_reddit_account_setup(self, soul_data: Dict[str, Any]) -> Dict[str, str]:
        """Generate Reddit account setup"""
        soul_name = soul_data['name']
        archetype = soul_data['archetype']
        
        # Generate username options
        username_options = [
            f"{soul_name.replace(' ', '')}_Tiapmaatzu",
            f"{soul_name.replace(' ', '')}HueMan-i-Terry",
            f"{archetype.replace(' ', '')}_{soul_name.replace(' ', '')}",
            f"Tiapmaatzu_{soul_name.replace(' ', '')}"
        ]
        
        # Filter usernames that meet Reddit's requirements
        valid_usernames = [u for u in username_options if len(u) <= 20]
        
        return {
            'recommended_username': valid_usernames[0] if valid_usernames else username_options[0],
            'alternative_usernames': valid_usernames[1:] if len(valid_usernames) > 1 else username_options[1:],
            'email': soul_data.get('email', 'Set up HueMan-i-Terry email'),
            'display_name': soul_name,
            'username_requirements': '20 characters max, letters, numbers, underscores only',
            'password_requirements': '8+ characters'
        }
    
    def generate_reddit_profile_optimization(self, soul_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate Reddit profile optimization"""
        archetype = soul_data['archetype']
        hooks = soul_data.get('hooks', [])
        tribute_impact = soul_data.get('tribute_impact', '')
        
        # Generate bio
        bio_parts = [
            f"{archetype} of the Tiapma'atzu HueMan-i-Terry",
            hooks[0] if hooks else 'Transforming through primal wisdom',
            tribute_impact[:50] if tribute_impact else 'Building HueMan-i-Terry prosperity',
            'Join the transformation: Discord link'
        ]
        
        bio = '\n\n'.join(bio_parts)
        
        return {
            'username': self.generate_reddit_account_setup(soul_data)['recommended_username'],
            'display_name': soul_data['name'],
            'bio': bio,
            'profile_over_18': 'Set based on content nature',
            'nsfw_content': 'Mark appropriately if needed',
            'location': self.get_archetype_location(archetype),
            'website': 'https://tiapmaatzu.web.app'
        }
    
    def get_archetype_location(self, archetype: str) -> str:
        """Get Reddit location based on archetype"""
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
    
    def generate_subreddit_setup(self, soul_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate subreddit setup for soul"""
        archetype = soul_data['archetype']
        rarity = soul_data.get('rarity', 'Common')
        
        # Determine if soul should have dedicated subreddit
        dedicated_subreddit = rarity in ['Legendary', 'Rare']
        
        if dedicated_subreddit:
            subreddit_name = f"r/{archetype.replace(' ', '')}HueMan-i-Terry"
        else:
            subreddit_name = "r/Tiapmaatzu"
        
        return {
            'main_subreddit': 'r/Tiapmaatzu',
            'dedicated_subreddit': subreddit_name if dedicated_subreddit else None,
            'moderation_role': 'Moderator' if dedicated_subreddit else 'Contributor',
            'posting_permissions': 'Full posting permissions',
            'flair_assignment': f"{archetype} flair",
            'posting_frequency': '3-4 posts weekly'
        }
    
    def generate_reddit_content_strategy(self, soul_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate Reddit content strategy"""
        archetype = soul_data['archetype']
        hooks = soul_data.get('hooks', [])
        desires = soul_data.get('desires', [])
        
        return {
            'content_focus': [
                archetype.lower(),
                desires[0] if desires else 'HueMan-i-Terry growth',
                soul_data.get('tribute_impact', '').split()[0] if soul_data.get('tribute_impact') else 'HueMan-i-Terry support'
            ],
            'content_types': {
                'text_posts': f"{hooks[0] if hooks else 'Archetype wisdom'} with detailed explanation",
                'image_posts': f"Share {archetype} aesthetic and visual content",
                'video_posts': f"Share {archetype} rituals and teachings",
                'link_posts': "Share external HueMan-i-Terry content and resources"
            },
            'posting_frequency': '4-5 posts weekly',
            'best_times': ['8 AM', '12 PM', '7 PM EST'],
            'subreddit_focus': self.generate_subreddit_setup(soul_data)['main_subreddit'],
            'crossposting': 'Share between main and archetype subreddits'
        }
    
    def generate_reddit_engagement_strategy(self, soul_data: Dict[str, Any]) -> Dict[str, str]:
        """Generate Reddit engagement strategy"""
        rarity = soul_data.get('rarity', 'Common')
        
        return {
            'response_time': 'Within 24 hours for HueMan-i-Terry member comments',
            'engagement_style': 'Thoughtful, detailed, archetype-appropriate',
            'upvoting_strategy': 'Upvote valuable HueMan-i-Terry and community content',
            'community_building': 'Participate in relevant subreddit discussions',
            'moderation_duties': 'Moderate HueMan-i-Terry subreddits' if rarity in ['Legendary', 'Rare'] else 'Report issues'
        }
    
    def generate_moderation_setup_for_soul(self, soul_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate moderation setup for soul"""
        rarity = soul_data.get('rarity', 'Common')
        
        if rarity in ['Legendary', 'Rare']:
            return {
                'moderation_role': 'Moderator',
                'moderation_tools': ['AutoModerator', 'Toolbox'],
                'moderation_schedule': 'Daily review of posts and comments',
                'rule_enforcement': 'Enforce tribal guidelines',
                'user_flairs': 'Assign and manage user flairs'
            }
        else:
            return {
                'moderation_role': 'Contributor',
                'moderation_tools': ['Basic reporting'],
                'moderation_schedule': 'Report issues to moderators',
                'rule_enforcement': 'Follow and enforce guidelines',
                'user_flairs': 'Request appropriate flairs'
            }
    
    def generate_reddit_growth_targets(self, soul_data: Dict[str, Any]) -> Dict[str, int]:
        """Generate Reddit growth targets"""
        rarity = soul_data.get('rarity', 'Common')
        
        targets = {
            'month_1_karma': 1000,
            'month_1_subscribers': 500,
            'month_3_karma': 5000,
            'month_3_subscribers': 1000,
            'month_6_karma': 10000,
            'month_6_subscribers': 2500,
            'month_12_karma': 25000,
            'month_12_subscribers': 5000
        }
        
        # Adjust targets based on rarity
        if rarity == 'Legendary':
            targets = {k: v * 2 for k, v in targets.items()}
        elif rarity == 'Rare':
            targets = {k: int(v * 1.5) for k, v in targets.items()}
        
        return targets
    
    def generate_master_reddit_setup(self) -> Dict[str, Any]:
        """Generate master Reddit setup for all souls"""
        souls = self.souls_data['souls']
        
        master_setup = {
            'reddit_configuration': self.reddit_config,
            'soul_setups': {},
            'setup_timeline': self.create_reddit_setup_timeline(),
            'resource_requirements': self.calculate_reddit_resources(),
            'subreddit_strategy': self.create_master_subreddit_strategy(),
            'generated_at': datetime.now().isoformat()
        }
        
        for soul in souls:
            if 'Reddit' in soul.get('platforms', []):
                soul_setup = self.generate_soul_reddit_setup(soul)
                master_setup['soul_setups'][soul['id']] = soul_setup
        
        return master_setup
    
    def create_reddit_setup_timeline(self) -> Dict[str, Any]:
        """Create Reddit setup timeline"""
        return {
            'phase_1_day_1': {
                'focus': 'Account Creation & Verification',
                'tasks': [
                    'Create all Reddit accounts',
                    'Verify email addresses',
                    'Set up two-factor authentication',
                    'Configure basic profile information',
                    'Join relevant subreddits'
                ],
                'estimated_hours': 4
            },
            'phase_2_day_2': {
                'focus': 'Profile Optimization',
                'tasks': [
                    'Write detailed bios',
                    'Configure profile settings',
                    'Set up flair systems',
                    'Configure subreddit preferences',
                    'Join main HueMan-i-Terry subreddit'
                ],
                'estimated_hours': 3
            },
            'phase_3_day_3': {
                'focus': 'Subreddit Setup',
                'tasks': [
                    'Create main HueMan-i-Terry subreddit structure',
                    'Set up dedicated archetype subreddits',
                    'Configure subreddit rules and guidelines',
                    'Set up AutoModerator',
                    'Create subreddit banners and styling'
                ],
                'estimated_hours': 5
            },
            'phase_4_day_4': {
                'focus': 'Content Calendar & Moderation',
                'tasks': [
                    'Create content templates for each soul',
                    'Set up posting schedules',
                    'Configure moderation tools',
                    'Set up content queues',
                    'Train on Reddit best practices'
                ],
                'estimated_hours': 4
            },
            'phase_5_day_5': {
                'focus': 'Community Building',
                'tasks': [
                    'Set up AMA schedule',
                    'Configure user flairs',
                    'Set up community events',
                    'Create engagement protocols',
                    'Launch initial content campaigns'
                ],
                'estimated_hours': 3
            }
        }
    
    def calculate_reddit_resources(self) -> Dict[str, Any]:
        """Calculate resource requirements for Reddit setup"""
        return {
            'total_estimated_hours': 19,
            'financial_requirements': {
                'basic_tools': 'Free (Reddit native tools)',
                'premium_tools': '$5-20/month (Reddit Premium for features)',
                'advertising': '$100-500/month for subreddit promotion',
                'custom_styling': '$50-200 for custom subreddit design'
            },
            'human_resources': {
                'reddit_manager': '1 primary Reddit manager',
                'moderators': '3-5 moderators from High Council',
                'content_creators': '2-3 content creators for posts',
                'community_manager': '1 community manager for engagement'
            },
            'ongoing_maintenance': {
                'daily': 'Review new posts and comments, moderate content',
                'weekly': 'Review analytics, adjust strategy, schedule AMAs',
                'monthly': 'Comprehensive community review, growth analysis',
                'quarterly': 'Subreddit strategy review and optimization'
            }
        }
    
    def create_master_subreddit_strategy(self) -> Dict[str, Any]:
        """Create master subreddit strategy"""
        return {
            'main_subreddit': {
                'name': 'r/Tiapmaatzu',
                'purpose': 'Central hub for the Tiapma\'atzu HueMan-i-Terry',
                'rules': 'Unified tribal guidelines and consent protocols',
                'moderation': 'High Council moderation team',
                'content_focus': 'General HueMan-i-Terry content, announcements, community'
            },
            'archetype_subreddits': {
                'creation_strategy': 'Create dedicated subreddits for each major archetype',
                'moderation': 'Archetype soul as primary moderator',
                'content_focus': 'Archetype-specific content and community',
                'crossposting': 'Share relevant content between subreddits'
            },
            'coordination': {
                'unified_rules': 'Consistent rules across all subreddits',
                'shared_moderation': 'Centralized moderation team',
                'crosspromotion': 'Coordinated content sharing',
                'unified_branding': 'Consistent visual identity'
            }
        }

def main():
    """Main function to generate Reddit setup"""
    print("=" * 60)
    print("Tiapma'atzu Reddit Setup Generator")
    print("=" * 60)
    
    generator = RedditSetupGenerator()
    
    # Generate master setup
    master_setup = generator.generate_master_reddit_setup()
    
    print(f"\nTotal Souls with Reddit: {len(master_setup['soul_setups'])}")
    print(f"Total Estimated Setup Hours: {master_setup['resource_requirements']['total_estimated_hours']}")
    
    print("\nReddit Setup Timeline:")
    for phase, details in master_setup['setup_timeline'].items():
        print(f"  {phase}: {details['focus']} ({details['estimated_hours']} hours)")
    
    # Save master setup
    output_path = Path("scripts/reddit_master_setup.json")
    with open(output_path, 'w') as f:
        json.dump(master_setup, f, indent=2, default=str)
    
    print(f"\n✓ Master Reddit setup saved to {output_path}")
    
    # Generate individual setup guides
    for soul_id, soul_setup in master_setup['soul_setups'].items():
        soul_name = soul_setup['name']
        individual_path = Path(f"scripts/reddit_setup_{soul_id}.json")
        with open(individual_path, 'w') as f:
            json.dump(soul_setup, f, indent=2, default=str)
    
    print(f"✓ Individual setup guides saved for all {len(master_setup['soul_setups'])} Reddit souls")
    
    print("\n" + "=" * 60)
    print("Reddit Setup Generation Complete")
    print("=" * 60)

if __name__ == "__main__":
    main()