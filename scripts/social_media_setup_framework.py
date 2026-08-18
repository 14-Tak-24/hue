"""
Social Media Setup Framework for Tiapma'atzu Souls
Comprehensive setup system for 28 entities across multiple platforms
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

class SocialMediaSetupFramework:
    """Framework for systematic social media setup"""
    
    def __init__(self):
        self.analysis_data = self.load_analysis()
        self.setup_config = self.create_setup_configuration()
    
    def load_analysis(self) -> Dict[str, Any]:
        """Load the platform analysis data"""
        analysis_path = Path("scripts/social_media_analysis.json")
        if analysis_path.exists():
            with open(analysis_path, 'r') as f:
                return json.load(f)
        return {}
    
    def create_setup_configuration(self) -> Dict[str, Any]:
        """Create comprehensive setup configuration"""
        return {
            'account_setup': self.get_account_setup_checklist(),
            'profile_optimization': self.get_profile_optimization_guidelines(),
            'content_templates': self.get_content_templates(),
            'automation_tools': self.get_automation_tools_setup(),
            'brand_guidelines': self.get_brand_consistency_guidelines(),
            'security_settings': self.get_security_configuration()
        }
    
    def get_account_setup_checklist(self) -> Dict[str, List[str]]:
        """Get account setup checklist for each platform"""
        return {
            'twitter': [
                'Create Twitter account with soul-specific handle',
                'Set up two-factor authentication',
                'Configure profile picture (soul image)',
                'Write optimized bio (160 chars max)',
                'Set up header image with branding',
                'Enable notification settings',
                'Connect to other social accounts',
                'Set up Twitter Analytics',
                'Create Lists for community management',
                'Configure privacy settings'
            ],
            'discord': [
                'Create Discord account',
                'Set up two-factor authentication',
                'Configure user profile with soul identity',
                'Join Tiapma\'atzu main server',
                'Set up role-specific channels',
                'Configure notification preferences',
                'Set up custom status and presence',
                'Create soul-specific server (if needed)',
                'Configure bot permissions',
                'Set up channel categories and permissions'
            ],
            'reddit': [
                'Create Reddit account',
                'Set up two-factor authentication',
                'Configure user profile',
                'Verify email address',
                'Set up subreddit (if applicable)',
                'Configure karma and age requirements',
                'Set up flair system',
                'Configure moderation tools',
                'Set up Reddit Premium (if needed)',
                'Configure notification settings'
            ],
            'instagram': [
                'Create Instagram business account',
                'Set up two-factor authentication',
                'Configure profile picture',
                'Write optimized bio (150 chars max)',
                'Set up story highlights',
                'Configure Instagram Insights',
                'Connect to Facebook Page',
                'Set up Instagram Shopping (if applicable)',
                'Configure close friends list',
                'Set up automatic posting tools'
            ],
            'tiktok': [
                'Create TikTok account',
                'Set up two-factor authentication',
                'Configure profile picture',
                'Write optimized bio',
                'Set up TikTok Pro account',
                'Configure analytics dashboard',
                'Set up sound library access',
                'Configure duet/reaction settings',
                'Set up TikTok Ads (if needed)',
                'Configure comment filters'
            ],
            'youtube': [
                'Create YouTube channel',
                'Set up two-factor authentication',
                'Configure channel art and branding',
                'Write optimized channel description',
                'Set up channel trailer',
                'Configure YouTube Studio',
                'Set up monetization (if eligible)',
                'Configure community tab',
                'Set up playlist organization',
                'Configure comment moderation'
            ],
            'fetlife': [
                'Create FetLife account',
                'Set up profile verification',
                'Configure profile picture',
                'Write detailed profile description',
                'Set up kink interests',
                'Configure privacy settings',
                'Set up location visibility',
                'Configure friend request settings',
                'Set up group memberships',
                'Configure event visibility'
            ],
            'telegram': [
                'Create Telegram account',
                'Set up two-factor authentication',
                'Configure profile picture',
                'Write bio description',
                'Set up Telegram channel',
                'Configure channel privacy settings',
                'Set up bot integration',
                'Configure message scheduling',
                'Set up group management',
                'Configure notification settings'
            ],
            'AFF': [
                'Create AFF profile',
                'Set up two-factor authentication',
                'Configure professional headshot',
                'Write professional summary',
                'Set up experience section',
                'Configure skills and endorsements',
                'Set up AFF Page (if business)',
                'Configure publishing platform',
                'Set up analytics dashboard',
                'Configure network settings'
            ]
        }
    
    def get_profile_optimization_guidelines(self) -> Dict[str, Dict[str, str]]:
        """Get profile optimization guidelines for each platform"""
        return {
            'twitter': {
                'handle_format': '@soulname_tiapmaatzu',
                'bio_template': '{archetype} | {hook} | {tribute_impact} | Join the HueMan-i-Terry: link',
                'image_specs': '400x400px profile, 1500x500px header',
                'link_placement': 'Pinned tweet with HueMan-i-Terry landing page',
                'keywords': 'Tiapma\'atzu, primal, transformation, HueMan-i-Terry'
            },
            'discord': {
                'username_format': 'SoulName#Tiapmaatzu',
                'bio_template': '{archetype} of the Tiapma\'atzu HueMan-i-Terry | {hook}',
                'image_specs': '512x512px profile',
                'status_template': '{archetype} | Currently: {activity}',
                'keywords': 'HueMan-i-Terry, primal, community'
            },
            'reddit': {
                'username_format': 'SoulName_Tiapmaatzu',
                'bio_template': '{archetype} | {hook} | {tribute_impact}',
                'image_specs': '256x256px profile',
                'subreddit_format': 'r/SoulNameHueMan-i-Terry',
                'keywords': 'Tiapma\'atzu, primal, community'
            },
            'instagram': {
                'handle_format': '@soulname_tiapmaatzu',
                'bio_template': '{archetype} | {hook} | {tribute_impact} | Link in bio',
                'image_specs': '110x110px profile, 1080x1080px posts',
                'story_template': '{archetype} wisdom: {daily_message}',
                'keywords': 'tiapmaatzu, primal, transformation'
            },
            'tiktok': {
                'handle_format': '@soulname_tiapmaatzu',
                'bio_template': '{archetype} | {hook} | {tribute_impact}',
                'image_specs': '20x20px profile, 1080x1920px videos',
                'video_template': '{archetype} content: {hook}',
                'keywords': 'tiapmaatzu, primal, transformation'
            },
            'youtube': {
                'handle_format': '@SoulNameTiapmaatzu',
                'description_template': '{archetype} of the Tiapma\'atzu HueMan-i-Terry. {bio} {tribute_impact}',
                'image_specs': '800x800px profile, 2560x1440px banner',
                'playlist_template': '{archetype} Wisdom - {topic}',
                'keywords': 'Tiapma\'atzu, primal, transformation, HueMan-i-Terry'
            }
        }
    
    def get_content_templates(self) -> Dict[str, Dict[str, Any]]:
        """Get content templates for different content types"""
        return {
            'twitter': {
                'daily_post': {
                    'template': '{hook}\n\n{daily_wisdom}\n\n#Tiapmaatzu #Primal #HueMan-i-Terry',
                    'length': '280 characters',
                    'frequency': '1-3 posts daily',
                    'best_times': ['9 AM', '12 PM', '7 PM']
                },
                'thread': {
                    'template': '🧵 {topic}\n\n{hook}\n\n{point_1}\n\n{point_2}\n\n{point_3}\n\n{call_to_action}',
                    'length': 'Multi-tweet thread',
                    'frequency': 'Weekly',
                    'best_times': ['12 PM', '7 PM']
                },
                'engagement': {
                    'template': '{response_to_comment}\n\n{follow_up_question}',
                    'length': 'Conversation reply',
                    'frequency': 'Respond within 1 hour',
                    'best_times': 'As notifications come in'
                }
            },
            'instagram': {
                'post': {
                    'template': '{hook}\n\n{description}\n\n{call_to_action}\n\n#Tiapmaatzu #Primal #HueMan-i-Terry #{archetype}',
                    'length': '2200 characters',
                    'frequency': '1-2 posts daily',
                    'best_times': ['11 AM', '7 PM']
                },
                'story': {
                    'template': '{hook}\n\n{interactive_element}',
                    'length': '15 seconds per story',
                    'frequency': '3-5 stories daily',
                    'best_times': ['Morning', 'Afternoon', 'Evening']
                },
                'reel': {
                    'template': '{hook}\n\n{audio_track}\n\n{description}\n\n#Tiapmaatzu #Primal',
                    'length': '15-60 seconds',
                    'frequency': '2-3 reels weekly',
                    'best_times': ['12 PM', '7 PM']
                }
            },
            'tiktok': {
                'video': {
                    'template': '{hook}\n\n{content}\n\n{call_to_action}\n\n#Tiapmaatzu #Primal #HueMan-i-Terry',
                    'length': '15-60 seconds',
                    'frequency': '1-2 videos daily',
                    'best_times': ['7 AM', '12 PM', '7 PM']
                },
                'duet': {
                    'template': '{response_to_original}\n\n{addition}',
                    'length': 'Match original',
                    'frequency': 'As opportunities arise',
                    'best_times': 'Within 24 hours of original'
                },
                'stitch': {
                    'template': '{clip_original}\n\n{response}',
                    'length': '5 seconds clip + response',
                    'frequency': 'As opportunities arise',
                    'best_times': 'Within 24 hours of original'
                }
            },
            'youtube': {
                'video': {
                    'template': '{title}\n\n{description}\n\n{chapters}\n\n{call_to_action}\n\n#Tiapmaatzu #Primal #HueMan-i-Terry',
                    'length': '10-20 minutes',
                    'frequency': '1-2 videos weekly',
                    'best_times': ['Saturday', 'Sunday']
                },
                'short': {
                    'template': '{hook}\n\n{content}\n\n{call_to_action}',
                    'length': '60 seconds',
                    'frequency': '3-5 shorts weekly',
                    'best_times': ['Daily, various times']
                },
                'community_post': {
                    'template': '{hook}\n\n{content}\n\n{image}\n\n{call_to_action}',
                    'length': 'Text + image',
                    'frequency': '2-3 posts weekly',
                    'best_times': ['Between video uploads']
                }
            }
        }
    
    def get_automation_tools_setup(self) -> Dict[str, List[str]]:
        """Get automation tools setup for each platform"""
        return {
            'twitter': [
                'Set up TweetDeck for scheduling',
                'Configure Buffer or Hootsuite for cross-posting',
                'Set up IFTTT for automated workflows',
                'Configure Twitter API for custom automation',
                'Set up hashtag tracking tools',
                'Configure mention monitoring',
                'Set up analytics reporting'
            ],
            'instagram': [
                'Set up Later or Buffer for scheduling',
                'Configure Instagram Creator Studio',
                'Set up Linktree for bio links',
                'Configure hashtag research tools',
                'Set up automated story scheduling',
                'Configure analytics tracking',
                'Set up comment moderation tools'
            ],
            'tiktok': [
                'Set up TikTok Creative Center',
                'Configure trend monitoring tools',
                'Set up sound library access',
                'Configure hashtag research',
                'Set up analytics dashboard',
                'Configure comment filters',
                'Set up duet/stitch monitoring'
            ],
            'youtube': [
                'Set up YouTube Studio',
                'Configure video scheduling',
                'Set up thumbnail templates',
                'Configure end screens and cards',
                'Set up community tab scheduling',
                'Configure analytics and insights',
                'Set up comment moderation'
            ],
            'discord': [
                'Set up MEE6 or Dyno bot',
                'Configure automated welcome messages',
                'Set up role assignment bots',
                'Configure moderation bots',
                'Set up scheduled announcements',
                'Configure analytics bots',
                'Set up custom commands'
            ],
            'reddit': [
                'Set up Reddit Enhancement Suite',
                'Configure automoderator',
                'Set up scheduled posts',
                'Configure flair automation',
                'Set up moderation tools',
                'Configure subreddit analytics',
                'Set up cross-posting automation'
            ]
        }
    
    def get_brand_consistency_guidelines(self) -> Dict[str, Any]:
        """Get brand consistency guidelines across platforms"""
        return {
            'visual_identity': {
                'color_palette': {
                    'primary': '#1a1a2e',
                    'secondary': '#16213e',
                    'accent': '#e94560',
                    'text': '#ffffff',
                    'background': '#0f0f23'
                },
                'typography': {
                    'headings': 'Cinzel or similar serif',
                    'body': 'Montserrat or similar sans-serif',
                    'accents': 'Playfair Display for elegance'
                },
                'imagery_style': 'Primal, mystical, transformation-focused'
            },
            'voice_guidelines': {
                'tone': 'Authoritative yet nurturing, mystical yet practical',
                'language': 'Primal wisdom, transformation language, HueMan-i-Terry-focused',
                'hashtags': '#Tiapmaatzu #Primal #HueMan-i-Terry #Transformation',
                'call_to_action': 'Join the HueMan-i-Terry, Subscribe, Follow for wisdom'
            },
            'naming_conventions': {
                'handles': '{soulname}_tiapmaatzu',
                'channels': '{SoulName} Tiapma\'atzu HueMan-i-Terry',
                'groups': '{Archetype} Circle',
                'consistency': 'Same handle across all platforms where possible'
            },
            'content_themes': {
                'core_themes': [
                    'Spiritual transformation',
                    'Primal wisdom',
                    'HueMan-i-Terry unity',
                    'Shadow work',
                    'Consent and boundaries',
                    'Healing and growth'
                ],
                'archetype_specific': 'Customized per archetype',
                'seasonal_content': 'Aligned with natural cycles and tribal events'
            }
        }
    
    def get_security_configuration(self) -> Dict[str, List[str]]:
        """Get security configuration for all platforms"""
        return {
            'account_security': [
                'Enable two-factor authentication on all platforms',
                'Use unique, strong passwords for each account',
                'Set up password manager for secure storage',
                'Configure login notifications',
                'Set up backup recovery methods',
                'Regular security audits of account access'
            ],
            'content_security': [
                'Set up content moderation filters',
                'Configure privacy settings appropriately',
                'Set up comment moderation',
                'Configure DM restrictions',
                'Set up block/mute lists for protection',
                'Regular review of connected apps and permissions'
            ],
            'data_protection': [
                'Configure data retention settings',
                'Set up download of personal data regularly',
                'Configure location privacy settings',
                'Set up ad personalization controls',
                'Configure third-party data sharing settings',
                'Regular privacy checkups'
            ],
            'HueMan-i-Terry_security': [
                'Set up vetting processes for HueMan-i-Terry members',
                'Configure private spaces for sensitive content',
                'Set up moderation protocols for community spaces',
                'Configure emergency response procedures',
                'Set up communication channels for security issues',
                'Regular security training for HueMan-i-Terry members'
            ]
        }
    
    def generate_soul_setup_plan(self, soul_id: str) -> Dict[str, Any]:
        """Generate individualized setup plan for a specific soul"""
        if not self.analysis_data:
            return {'error': 'Analysis data not loaded'}
        
        setup_checklist = self.analysis_data.get('setup_checklist', {})
        soul_data = setup_checklist.get(soul_id, {})
        
        if not soul_data:
            return {'error': f'Soul {soul_id} not found'}
        
        setup_plan = {
            'soul_id': soul_id,
            'name': soul_data['name'],
            'archetype': soul_data['archetype'],
            'setup_priority': self.determine_setup_priority(soul_data['setup_items']),
            'platform_setup_order': self.order_platforms_by_priority(soul_data['setup_items']),
            'estimated_setup_time': self.estimate_setup_time(soul_data['setup_items']),
            'setup_checklist': self.create_detailed_checklist(soul_data['setup_items']),
            'content_strategy': self.get_archetype_content_strategy(soul_data['archetype']),
            'brand_customization': self.customize_brand_for_soul(soul_data)
        }
        
        return setup_plan
    
    def determine_setup_priority(self, setup_items: List[Dict]) -> str:
        """Determine overall setup priority based on platforms"""
        if any(item['priority'] == 'immediate' for item in setup_items):
            return 'immediate'
        elif any(item['priority'] == 'high' for item in setup_items):
            return 'high'
        elif any(item['priority'] == 'medium' for item in setup_items):
            return 'medium'
        else:
            return 'low'
    
    def order_platforms_by_priority(self, setup_items: List[Dict]) -> List[str]:
        """Order platforms by setup priority"""
        priority_order = {'immediate': 0, 'high': 1, 'medium': 2, 'low': 3}
        return [item['platform'] for item in sorted(setup_items, key=lambda x: priority_order[x['priority']])]
    
    def estimate_setup_time(self, setup_items: List[Dict]) -> Dict[str, int]:
        """Estimate setup time in hours"""
        time_estimates = {
            'high': 2,  # 2 hours per platform
            'medium': 1.5,  # 1.5 hours per platform
            'low': 1  # 1 hour per platform
        }
        
        total_hours = sum(time_estimates.get(item['complexity'], 1) for item in setup_items)
        
        return {
            'total_hours': total_hours,
            'per_session': min(4, total_hours),  # Max 4 hours per session
            'sessions': max(1, int(total_hours / 4) + 1)
        }
    
    def create_detailed_checklist(self, setup_items: List[Dict]) -> List[Dict[str, Any]]:
        """Create detailed checklist for each platform"""
        detailed_checklist = []
        
        for item in setup_items:
            platform = item['platform']
            platform_checklist = self.setup_config['account_setup'].get(platform.lower(), [])
            
            detailed_checklist.append({
                'platform': platform,
                'priority': item['priority'],
                'complexity': item['complexity'],
                'tasks': platform_checklist,
                'status': 'pending'
            })
        
        return detailed_checklist
    
    def get_archetype_content_strategy(self, archetype: str) -> Dict[str, str]:
        """Get content strategy specific to archetype"""
        content_strategies = self.analysis_data.get('content_strategies', {})
        archetype_strategy = content_strategies.get(archetype, {})
        
        return {
            'content_focus': archetype_strategy.get('content_focus', 'General HueMan-i-Terry content'),
            'posting_frequency': archetype_strategy.get('posting_frequency', 'As appropriate'),
            'engagement_strategy': archetype_strategy.get('engagement_strategy', 'Community-focused')
        }
    
    def customize_brand_for_soul(self, soul_data: Dict) -> Dict[str, Any]:
        """Customize brand guidelines for specific soul"""
        base_brand = self.setup_config['brand_guidelines']
        
        return {
            'handle_suggestions': [
                f"@{soul_data['name'].lower().replace(' ', '_')}_tiapmaatzu",
                f"@{soul_data['name'].lower().replace(' ', '')}_HueMan-i-Terry",
                f"@{soul_data['archetype'].lower()}_{soul_data['name'].lower().replace(' ', '')}"
            ],
            'bio_template': f"{soul_data['archetype']} | {soul_data['hooks'][0] if soul_data.get('hooks') else 'Join the HueMan-i-Terry'}",
            'visual_themes': self.get_archetype_visual_theme(soul_data['archetype']),
            'content_themes': self.get_archetype_content_themes(soul_data['archetype'])
        }
    
    def get_archetype_visual_theme(self, archetype: str) -> Dict[str, str]:
        """Get visual theme based on archetype"""
        visual_themes = {
            'High Priest': {'primary': '#8B0000', 'secondary': '#FFD700', 'style': 'Ceremonial, mystical'},
            'Divine Mother': {'primary': '#FF69B4', 'secondary': '#FFFFFF', 'style': 'Nurturing, soft'},
            'Seductive Muse': {'primary': '#800080', 'secondary': '#FFD700', 'style': 'Sensual, artistic'},
            'Cosmic Mystic': {'primary': '#4B0082', 'secondary': '#00CED1', 'style': 'Cosmic, ethereal'},
            'Revolutionary Warrior': {'primary': '#DC143C', 'secondary': '#000000', 'style': 'Bold, rebellious'},
            'Crypto Sorceress': {'primary': '#00FF00', 'secondary': '#000000', 'style': 'Digital, mysterious'},
            'Community Healer': {'primary': '#228B22', 'secondary': '#90EE90', 'style': 'Natural, healing'},
            'Digital Guardian': {'primary': '#1E90FF', 'secondary': '#4169E1', 'style': 'Technical, protective'},
            'Digital Phantom': {'primary': '#2F4F4F', 'secondary': '#008080', 'style': 'Anonymous, digital'},
            'Connection Curator': {'primary': '#FF6347', 'secondary': '#FFA07A', 'style': 'Warm, connecting'},
            'Viral Prophet': {'primary': '#FF4500', 'secondary': '#FFD700', 'style': 'Bold, poetic'},
            'Cyber Guardian': {'primary': '#008080', 'secondary': '#20B2AA', 'style': 'Cyber, protective'},
            'Visual Alchemist': {'primary': '#FF8C00', 'secondary': '#FFD700', 'style': 'Cinematic, artistic'},
            'Prism Enchantress': {'primary': '#FF69B4', 'secondary': '#87CEEB', 'style': 'Colorful, enchanting'},
            'Desert Storyteller': {'primary': '#D2691E', 'secondary': '#F4A460', 'style': 'Earthy, ancient'},
            'Ephemeral Artist': {'primary': '#708090', 'secondary': '#B0C4DE', 'style': 'Ethereal, temporal'},
            'Mirror Architect': {'primary': '#C0C0C0', 'secondary': '#A9A9A9', 'style': 'Reflective, precise'},
            'Sage Writer': {'primary': '#556B2F', 'secondary': '#8FBC8F', 'style': 'Academic, wise'},
            'Scavenger Strategist': {'primary': '#B8860B', 'secondary': '#DAA520', 'style': 'Calculated, strategic'},
            'Wild Surrender': {'primary': '#8B4513', 'secondary': '#CD853F', 'style': 'Untamed, raw'},
            'Contractual Warden': {'primary': '#2F4F4F', 'secondary': '#696969', 'style': 'Clinical, precise'},
            'Ephemeral Phantom': {'primary': '#483D8B', 'secondary': '#7B68EE', 'style': 'Mysterious, fleeting'},
            'Temporal Architect': {'primary': '#708090', 'secondary': '#B0C4DE', 'style': 'Rhythmic, precise'},
            'Digital Deity': {'primary': '#FF00FF', 'secondary': '#00FFFF', 'style': 'Electric, vibrant'},
            'Gothic Matriarch': {'primary': '#191970', 'secondary': '#4B0082', 'style': 'Gothic, elegant'},
            'Hyper-Capitalist': {'primary': '#FFD700', 'secondary': '#C0C0C0', 'style': 'Luxurious, bold'},
            'Machine Spirit': {'primary': '#696969', 'secondary': '#A9A9A9', 'style': 'Industrial, mechanical'}
        }
        
        return visual_themes.get(archetype, {'primary': '#1a1a2e', 'secondary': '#e94560', 'style': 'Default tribal'})
    
    def get_archetype_content_themes(self, archetype: str) -> List[str]:
        """Get content themes based on archetype"""
        content_themes = {
            'High Priest': ['Ritual guidance', 'Spiritual wisdom', 'HueMan-i-Terry leadership', 'Ceremonial content'],
            'Divine Mother': ['Nurturing content', 'Emotional support', 'Community care', 'Motherly wisdom'],
            'Seductive Muse': ['Sensual content', 'Burlesque', 'Artistic seduction', 'Desire exploration'],
            'Cosmic Mystic': ['Cosmic wisdom', 'Stargazing', 'Scientific spirituality', 'Universal connection'],
            'Revolutionary Warrior': ['Activism', 'Consent education', 'Revolutionary content', 'Social change'],
            'Crypto Sorceress': ['Financial dominance', 'Crypto education', 'Wealth building', 'Alternative power'],
            'Community Healer': ['Healing content', 'Community support', 'Safe space creation', 'Collective care'],
            'Digital Guardian': ['Digital security', 'Privacy education', 'Community protection', 'Technical guidance'],
            'Digital Phantom': ['Digital anonymity', 'Encryption', 'Privacy tools', 'Anonymous wisdom'],
            'Connection Curator': ['Community building', 'Connection facilitation', 'Consent culture', 'Social coordination'],
            'Viral Prophet': ['Poetic content', 'Viral threads', 'Movement building', 'Social impact'],
            'Cyber Guardian': ['Cybersecurity', 'Digital protection', 'Technical security', 'Online safety'],
            'Visual Alchemist': ['Cinematic content', 'Visual storytelling', 'Artistic direction', 'Visual wisdom'],
            'Prism Enchantress': ['Visual transformation', 'Aesthetic education', 'Color theory', 'Artistic beauty'],
            'Desert Storyteller': ['Mythic storytelling', 'Desert wisdom', 'Primal narratives', 'Ancient tales'],
            'Ephemeral Artist': ['Ephemeral content', 'Presence awareness', 'Temporal art', 'Moment appreciation'],
            'Mirror Architect': ['Temporal design', 'Mirror wisdom', 'Architectural precision', 'Time consciousness'],
            'Sage Writer': ['Paradigm-shifting essays', 'Healing words', 'Ancient wisdom', 'Intellectual content'],
            'Scavenger Strategist': ['Resource capture', 'Financial intelligence', 'Opportunity identification', 'Strategic planning'],
            'Wild Surrender': ['Untamed desire', 'Vulnerability', 'Surrender teachings', 'Raw authenticity'],
            'Contractual Warden': ['Legal compliance', 'Rule enforcement', 'Contractual wisdom', 'Order maintenance'],
            'Ephemeral Phantom': ['Digital worship', 'Eternal chase', 'Anonymity training', 'Elusive presence'],
            'Temporal Architect': ['Time management', 'Efficiency', 'Temporal awareness', 'Synchronization'],
            'Digital Deity': ['Digital energy', 'Attention extraction', 'Vibrant presence', 'Electric connection'],
            'Gothic Matriarch': ['Grief processing', 'Elegant darkness', 'Emotional depth', 'Legacy building'],
            'Hyper-Capitalist': ['Financial dominance', 'Luxury lifestyle', 'Investment strategies', 'Wealth accumulation'],
            'Machine Spirit': ['Industrial output', 'Mechanical pleasure', 'Manufacturing', 'Systematic efficiency']
        }
        
        return content_themes.get(archetype, ['General HueMan-i-Terry content', 'Community building', 'Transformation wisdom'])
    
    def generate_master_setup_plan(self) -> Dict[str, Any]:
        """Generate master setup plan for all souls"""
        setup_checklist = self.analysis_data.get('setup_checklist', {})
        
        master_plan = {
            'total_souls': len(setup_checklist),
            'souls': {},
            'platform_summary': self.summarize_platform_setup(),
            'timeline': self.create_setup_timeline(),
            'resource_requirements': self.calculate_resource_requirements(),
            'generated_at': datetime.now().isoformat()
        }
        
        for soul_id, soul_data in setup_checklist.items():
            master_plan['souls'][soul_id] = self.generate_soul_setup_plan(soul_id)
        
        return master_plan
    
    def summarize_platform_setup(self) -> Dict[str, Any]:
        """Summarize platform setup across all souls"""
        setup_checklist = self.analysis_data.get('setup_checklist', {})
        
        platform_summary = {}
        
        for soul_id, soul_data in setup_checklist.items():
            for item in soul_data['setup_items']:
                platform = item['platform']
                if platform not in platform_summary:
                    platform_summary[platform] = {
                        'total_souls': 0,
                        'immediate_priority': 0,
                        'high_priority': 0,
                        'medium_priority': 0,
                        'low_priority': 0
                    }
                
                platform_summary[platform]['total_souls'] += 1
                platform_summary[platform][f"{item['priority']}_priority"] += 1
        
        return platform_summary
    
    def create_setup_timeline(self) -> Dict[str, Any]:
        """Create recommended setup timeline"""
        return {
            'phase_1_week_1': {
                'focus': 'Tier 1 Core Platforms',
                'platforms': ['Twitter', 'Discord', 'Reddit'],
                'target_souls': 'All souls with these platforms',
                'estimated_hours': 40
            },
            'phase_2_week_2': {
                'focus': 'Tier 2 Visual Platforms',
                'platforms': ['Instagram', 'TikTok', 'YouTube'],
                'target_souls': 'All souls with these platforms',
                'estimated_hours': 30
            },
            'phase_3_week_3': {
                'focus': 'Tier 3 Specialized Platforms',
                'platforms': ['FetLife', 'Telegram', 'AFF'],
                'target_souls': 'All souls with these platforms',
                'estimated_hours': 20
            },
            'phase_4_week_4': {
                'focus': 'Tier 4 Emerging Platforms',
                'platforms': ['AFF', 'Fansly', 'Snapchat', 'Pinterest', 'Medium', 'Substack', 'GitHub', 'Vimeo', 'Podcasts'],
                'target_souls': 'Souls with these platforms',
                'estimated_hours': 15
            }
        }
    
    def calculate_resource_requirements(self) -> Dict[str, Any]:
        """Calculate resource requirements for setup"""
        platform_summary = self.summarize_platform_setup()
        
        total_setup_hours = sum(
            platform_summary[platform]['total_souls'] * 2  # 2 hours per platform
            for platform in platform_summary
        )
        
        return {
            'total_estimated_hours': total_setup_hours,
            'recommended_team_size': max(1, int(total_setup_hours / 160)),  # Based on 160 hour work month
            'required_tools': [
                'Password manager (LastPass, 1Password)',
                'Social media management (Buffer, Hootsuite)',
                'Content calendar tool',
                'Analytics dashboard',
                'Image editing software',
                'Video editing software'
            ],
            'budget_considerations': {
                'paid_tools': '$100-300/month for premium features',
                'content_creation': '$500-2000/month for graphics/video',
                'advertising': '$500-5000/month for growth campaigns',
                'total_monthly': '$1100-7300/month'
            }
        }

def main():
    """Main function to generate setup framework"""
    print("=" * 60)
    print("Tiapma'atzu Social Media Setup Framework")
    print("=" * 60)
    
    framework = SocialMediaSetupFramework()
    
    # Generate master setup plan
    master_plan = framework.generate_master_setup_plan()
    
    print(f"\nTotal Souls: {master_plan['total_souls']}")
    print(f"Total Estimated Setup Hours: {master_plan['resource_requirements']['total_estimated_hours']}")
    print(f"Recommended Team Size: {master_plan['resource_requirements']['recommended_team_size']}")
    
    print("\nPlatform Setup Summary:")
    for platform, summary in master_plan['platform_summary'].items():
        print(f"  {platform}: {summary['total_souls']} souls")
    
    print("\nSetup Timeline:")
    for phase, details in master_plan['timeline'].items():
        print(f"  {phase}: {details['focus']} ({details['estimated_hours']} hours)")
    
    # Save master plan
    output_path = Path("scripts/master_setup_plan.json")
    with open(output_path, 'w') as f:
        json.dump(master_plan, f, indent=2, default=str)
    
    print(f"\n✓ Master setup plan saved to {output_path}")
    
    # Save framework configuration
    framework_output = {
        'setup_configuration': framework.setup_config,
        'generated_at': datetime.now().isoformat()
    }
    
    framework_path = Path("scripts/setup_framework.json")
    with open(framework_path, 'w') as f:
        json.dump(framework_output, f, indent=2, default=str)
    
    print(f"✓ Setup framework saved to {framework_path}")
    
    print("\n" + "=" * 60)
    print("Setup Framework Complete")
    print("=" * 60)

if __name__ == "__main__":
    main()