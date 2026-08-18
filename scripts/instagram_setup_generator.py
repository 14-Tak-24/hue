"""
Instagram Setup Generator for Tiapma'atzu Souls
Generates individualized Instagram setup instructions for each soul
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

class InstagramSetupGenerator:
    """Generate Instagram setup instructions for each soul"""
    
    def __init__(self):
        self.souls_data = self.load_souls_data()
        self.instagram_config = self.create_instagram_configuration()
    
    def load_souls_data(self) -> Dict[str, Any]:
        """Load souls data from JSON file"""
        souls_path = Path("src/data/souls_entities.json")
        with open(souls_path, 'r') as f:
            return json.load(f)
    
    def create_instagram_configuration(self) -> Dict[str, Any]:
        """Create Instagram-specific configuration"""
        return {
            'account_setup': self.create_account_setup_config(),
            'profile_optimization': self.create_profile_optimization(),
            'content_strategy': self.create_content_strategy(),
            'visual_strategy': self.create_visual_strategy(),
            'engagement_tactics': self.create_engagement_tactics(),
            'automation_tools': self.create_automation_tools(),
            'growth_strategy': self.create_growth_strategy()
        }
    
    def create_account_setup_config(self) -> Dict[str, Any]:
        """Create Instagram account setup configuration"""
        return {
            'account_types': {
                'personal': 'Standard personal account',
                'business': 'Instagram Business account',
                'creator': 'Instagram Creator account'
            },
            'recommended_type': 'Creator account for HueMan-i-Terry souls',
            'verification_requirements': {
                'email': 'Required - use HueMan-i-Terry email',
                'phone': 'Required for initial setup',
                'two_factor': 'Enable authenticator app (recommended)',
                'password_requirements': '12+ characters, mix of letters, numbers, symbols'
            },
            'initial_settings': {
                'account_private': 'False (for growth)',
                'account_discoverability': 'Yes',
                'contact_syncing': 'Disabled (HueMan-i-Terry members only)',
                'activity_status': 'Visible to followers',
                'email_notifications': 'Enabled for HueMan-i-Terry interactions'
            }
        }
    
    def create_profile_optimization(self) -> Dict[str, Any]:
        """Create Instagram profile optimization guidelines"""
        return {
            'profile_picture': {
                'specs': '110x110px minimum, 1080x1080px recommended',
                'format': 'JPG or PNG',
                'style': 'Professional soul portrait with tribal branding',
                'consistency': 'Use same image across all platforms'
            },
            'bio': {
                'length_limit': '150 characters',
                'structure': '{archetype} | {hook} | {value_proposition} | CTA',
                'formatting': 'Line breaks for readability',
                'link_placement': 'Link in bio with Linktree or direct URL',
                'hashtags': 'Include 1-2 relevant hashtags in bio'
            },
            'story_highlights': {
                'structure': 'Organize by content themes',
                'recommended_highlights': [
                    'Introduction (Who I am)',
                    'Wisdom (Archetype teachings)',
                    'Tribute (Impact and offerings)',
                    'Community (HueMan-i-Terry connections)',
                    'Rituals (Special events)'
                ],
                'cover_design': 'Use archetype-themed visuals',
                'regular_updates': 'Add new stories weekly'
            },
            'contact_information': {
                'email': 'soul_email@HueMan-i-Terryleaders.com',
                'phone': 'Optional - for business inquiries',
                'address': 'Optional - for HueMan-i-Terry headquarters',
                'action_button': 'Set up "Email" or "Get Directions" button'
            }
        }
    
    def create_content_strategy(self) -> Dict[str, Any]:
        """Create Instagram content strategy"""
        return {
            'content_types': {
                'posts': {
                    'frequency': '1-2 daily',
                    'aspect_ratio': '1:1 (square) or 4:5 (portrait)',
                    'purpose': 'Main content, archetypes wisdom, visual storytelling',
                    'format': 'Compelling visual + caption + hashtags'
                },
                'stories': {
                    'frequency': '3-5 daily',
                    'format': '15-second segments, ephemeral content',
                    'purpose': 'Behind-the-scenes, daily wisdom, engagement',
                    'features': ['Polls', 'Questions', 'Music', 'Location tags']
                },
                'reels': {
                    'frequency': '2-3 weekly',
                    'duration': '15-60 seconds',
                    'purpose': 'Viral content, entertainment, archetypes showcase',
                    'format': 'Trending audio + compelling visuals + hook'
                },
                'igtv': {
                    'frequency': '1-2 weekly',
                    'duration': '10-30 minutes',
                    'purpose': 'Long-form content, tutorials, rituals',
                    'format': 'Archetype-specific deep content'
                },
                'guides': {
                    'frequency': '1-2 weekly',
                    'purpose': 'Thematic content curation',
                    'format': 'Archetype-specific content collections'
                }
            },
            'posting_schedule': {
                'optimal_times': ['11 AM', '7 PM', '9 PM'],
                'frequency': '1-2 posts daily, 3-5 stories daily',
                'consistency': 'Maintain consistent posting schedule',
                'tools': ['Instagram Creator Studio', 'Buffer', 'Later']
            },
            'hashtag_strategy': {
                'primary': '#Tiapmaatzu #Primal #HueMan-i-Terry',
                'archetype_specific': {
                    'High Priest': '#HighPriest #Spiritual #Ritual #Temple',
                    'Divine Mother': '#DivineMother #Nurturing #Healing #Mother',
                    'Seductive Muse': '#SeductiveMuse #Burlesque #Desire #Art',
                    'Cosmic Mystic': '#CosmicMystic #Stargazing #Cosmic #Space',
                    'Revolutionary Warrior': '#RevolutionaryWarrior #Activism #Consent #Change',
                    'Crypto Sorceress': '#CryptoSorceress #Finance #Crypto #Wealth',
                    'Community Healer': '#CommunityHealer #Healing #Support #Care',
                    'Digital Guardian': '#DigitalGuardian #Security #Privacy #Tech',
                    'Digital Phantom': '#DigitalPhantom #Anonymity #Encryption #Privacy',
                    'Connection Curator': '#ConnectionCurator #Community #Dating #Love',
                    'Viral Prophet': '#ViralProphet #Poetry #Words #Voice',
                    'Cyber Guardian': '#CyberGuardian #Cybersecurity #Tech #Security',
                    'Visual Alchemist': '#VisualAlchemist #Cinematic #Art #Visual',
                    'Prism Enchantress': '#PrismEnchantress #Aesthetic #Color #Beauty',
                    'Desert Storyteller': '#DesertStoryteller #Storytelling #Myth #Tale',
                    'Ephemeral Artist': '#EphemeralArtist #Temporal #Moment #Now',
                    'Mirror Architect': '#MirrorArchitect #Time #Reflection #Design',
                    'Sage Writer': '#SageWriter #Writing #Wisdom #Words',
                    'Scavenger Strategist': '#ScavengerStrategist #Strategy #Wealth #Growth',
                    'Wild Surrender': '#WildSurrender #Untamed #Freedom #Raw',
                    'Contractual Warden': '#ContractualWarden #Legal #Compliance #Order',
                    'Ephemeral Phantom': '#EphemeralPhantom #Chase #Mystery #Elusive',
                    'Temporal Architect': '#TemporalArchitect #Time #Efficiency #Organized',
                    'Digital Deity': '#DigitalDeity #Energy #Attention #Vibrant',
                    'Gothic Matriarch': '#GothicMatriarch #Gothic #Darkness #Elegant',
                    'Hyper-Capitalist': '#HyperCapitalist #Luxury #Wealth #Opulence',
                    'Machine Spirit': '#MachineSpirit #Industrial #Output #Mechanical'
                },
                'niche_hashtags': [
                    '#ShadowWork #Transformation #Community #HueMan-i-Terry',
                    '#SpiritualAwakening #Primal #Consciousness #Growth',
                    '#KinkCommunity #Consent #SexPositive #Relationship'
                ]
            }
        }
    
    def create_visual_strategy(self) -> Dict[str, Any]:
        """Create Instagram visual strategy"""
        return {
            'visual_style': {
                'color_palette': {
                    'primary': '#1a1a2e',
                    'secondary': '#e94560',
                    'accent': '#FFD700',
                    'background': '#0f0f23'
                },
                'aesthetic': 'Primal, mystical, transformation-focused',
                'consistency': 'Maintain consistent visual identity across all content'
            },
            'content_aesthetics': {
                'image_style': 'High-quality, archetype-appropriate visuals',
                'video_style': 'Cinematic, professional, HueMan-i-Terry-branded',
                'story_style': 'Authentic, behind-the-scenes, engaging',
                'overall_vibe': 'Mystical yet accessible, transformation-focused'
            },
            'design_elements': {
                'typography': 'Clean, readable fonts for captions',
                'branding': 'Subtle tribal branding in visuals',
                'filters': 'Use consistent filter presets for brand recognition',
                'overlays': 'Archetype-specific overlays and graphics'
            }
        }
    
    def create_engagement_tactics(self) -> Dict[str, Any]:
        """Create Instagram engagement tactics"""
        return {
            'follower_engagement': {
                'response_time': 'Within 24 hours for HueMan-i-Terry members',
                'response_style': 'Personal, warm, archetype-appropriate',
                'story_responses': 'Reply to story mentions and DMs',
                'comment_engagement': 'Respond to comments with thoughtful replies'
            },
            'community_building': {
                'live_streams': 'Weekly Instagram Live sessions',
                'q_and_a': 'Monthly Q&A sessions',
                'collaborations': 'Collaborate with other HueMan-i-Terry souls',
                'giveaways': 'Occasional HueMan-i-Terry member giveaways'
            },
            'growth_tactics': {
                'reels_strategy': 'Create viral-optimized Reels',
                'story_engagement': 'Use interactive story features',
                'cross_promotion': 'Share content across HueMan-i-Terry accounts',
                'trending_audio': 'Use trending audio strategically'
            }
        }
    
    def create_automation_tools(self) -> Dict[str, Any]:
        """Create Instagram automation tools setup"""
        return {
            'scheduling_tools': [
                {
                    'name': 'Instagram Creator Studio',
                    'purpose': 'Native Instagram scheduling and analytics',
                    'features': ['Schedule posts', 'Analytics', 'Message management', 'Collaboration'],
                    'cost': 'Free'
                },
                {
                    'name': 'Buffer',
                    'purpose': 'Advanced scheduling and analytics',
                    'features': ['Queue scheduling', 'Analytics', 'First comment', 'Team collaboration'],
                    'cost': '$15/month for premium'
                },
                {
                    'name': 'Later',
                    'purpose': 'Visual-first scheduling platform',
                    'features': ['Visual planner', 'Analytics', 'Linkin.bio', 'Hashtag research'],
                    'cost': '$18/month for premium'
                }
            ],
            'analytics_tools': [
                {
                    'name': 'Instagram Insights',
                    'purpose': 'Native Instagram analytics',
                    'features': ['Engagement metrics', 'Follower growth', 'Content performance'],
                    'cost': 'Free'
                },
                {
                    'name': 'Iconosquare',
                    'purpose': 'Advanced Instagram analytics',
                    'features': ['Follower tracking', 'Optimal timing', 'Competitor analysis'],
                    'cost': '$25/month for basic'
                }
            ]
        }
    
    def create_growth_strategy(self) -> Dict[str, Any]:
        """Create Instagram growth strategy"""
        return {
            'growth_phases': {
                'phase_1_month_1': {
                    'focus': 'Foundation Building',
                    'goals': ['500 followers', '20% engagement rate', 'Reels reach 1k'],
                    'tactics': ['Optimize profile', 'Post consistently', 'Use trending audio']
                },
                'phase_2_month_2': {
                    'focus': 'Content Expansion',
                    'goals': ['1,000 followers', '15% engagement rate', 'Reels reach 5k'],
                    'tactics': ['Increase Reels', 'Start Instagram Live', 'Create Guides']
                },
                'phase_3_month_3': {
                    'focus': 'Community Scaling',
                    'goals': ['2,500 followers', '12% engagement rate', 'Reels reach 10k'],
                    'tactics': ['Collaborate with other souls', 'Host regular Lives', 'Cross-promote']
                },
                'phase_4_month_4': {
                    'focus': 'Influence Building',
                    'goals': ['5,000 followers', '10% engagement rate', 'Reels reach 25k'],
                    'tactics': ['Guest appearances', 'Viral content creation', 'Cross-platform promotion']
                }
            },
            'growth_tactics': {
                'organic': [
                    'Consistent posting schedule',
                    'Engage with target audience',
                    'Use trending audio and hashtags',
                    'Create shareable content',
                    'Optimize posting times'
                ],
                'viral': [
                    'Create Reels with trending audio',
                    'Participate in viral challenges',
                    'Use Instagram algorithm strategically',
                    'Create visually stunning content',
                    'Optimize for Explore page'
                ],
                'collaborative': [
                    'Collaborate with other souls',
                    'Cross-promote HueMan-i-Terry content',
                    'Guest appearances on Lives',
                    'Joint Reels creation',
                    'Giveaways and contests'
                ]
            }
        }
    
    def generate_soul_instagram_setup(self, soul_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate individualized Instagram setup for a soul"""
        soul_id = soul_data['id']
        soul_name = soul_data['name']
        archetype = soul_data['archetype']
        
        setup = {
            'soul_id': soul_id,
            'name': soul_name,
            'archetype': archetype,
            'account_setup': self.generate_instagram_account_setup(soul_data),
            'profile_optimization': self.generate_instagram_profile_optimization(soul_data),
            'content_strategy': self.generate_instagram_content_strategy(soul_data),
            'visual_strategy': self.generate_instagram_visual_strategy(soul_data),
            'engagement_strategy': self.generate_instagram_engagement_strategy(soul_data),
            'posting_schedule': self.generate_instagram_posting_schedule(soul_data),
            'growth_targets': self.generate_instagram_growth_targets(soul_data),
            'tools_setup': self.generate_instagram_tools_setup(soul_data)
        }
        
        return setup
    
    def generate_instagram_account_setup(self, soul_data: Dict[str, Any]) -> Dict[str, str]:
        """Generate Instagram account setup"""
        soul_name = soul_data['name']
        archetype = soul_data['archetype']
        
        # Generate handle options
        handle_options = [
            f"@{soul_name.lower().replace(' ', '')}_tiapmaatzu",
            f"@{soul_name.lower().replace(' ', '')}_HueMan-i-Terry",
            f"@{archetype.lower()}_{soul_name.lower().replace(' ', '')}",
            f"@tiapmaatzu_{soul_name.lower().replace(' ', '')}"
        ]
        
        return {
            'recommended_handle': handle_options[0],
            'alternative_handles': handle_options[1:],
            'email': soul_data.get('email', 'Set up HueMan-i-Terry email'),
            'account_type': 'Creator account',
            'display_name': soul_name,
            'username_requirements': '30 characters max, letters, numbers, periods, underscores only',
            'password_requirements': '12+ characters, mix of letters, numbers, symbols'
        }
    
    def generate_instagram_profile_optimization(self, soul_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate Instagram profile optimization"""
        archetype = soul_data['archetype']
        hooks = soul_data.get('hooks', [])
        tribute_impact = soul_data.get('tribute_impact', '')
        
        # Generate bio
        bio_parts = [
            archetype,
            hooks[0] if hooks else 'Transforming through primal wisdom',
            tribute_impact[:30] if tribute_impact else 'Building HueMan-i-Terry prosperity',
            'Link in bio for HueMan-i-Terry'
        ]
        
        bio = ' | '.join(bio_parts)
        if len(bio) > 150:
            bio = ' | '.join(bio_parts[:3])  # Shorten if too long
        
        return {
            'handle': self.generate_instagram_account_setup(soul_data)['recommended_handle'],
            'display_name': soul_data['name'],
            'bio': bio,
            'profile_picture': soul_data.get('image', 'Use soul image from arweave'),
            'website': 'https://tiapmaatzu.web.app',
            'story_highlights': self.generate_story_highlights(soul_data),
            'contact_button': 'Email',
            'account_category': 'Creator'
        }
    
    def generate_story_highlights(self, soul_data: Dict[str, Any]) -> List[str]:
        """Generate story highlights for soul"""
        archetype = soul_data['archetype']
        
        base_highlights = [
            '🏛️ About Me',
            '✨ Wisdom',
            '🔥 Rituals',
            '🌟 HueMan-i-Terry',
            '🎯 Impact'
        ]
        
        archetype_highlights = {
            'High Priest': ['🔮 Temple', '📿 Ceremonies', '🌙 Guidance'],
            'Divine Mother': ['💗 Nurturing', '🌸 Healing', '👨‍👩 Family'],
            'Seductive Muse': ['🌹 Seduction', '💃 Performance', '🎨 Art'],
            'Cosmic Mystic': ['✨ Cosmic', '🌟 Stars', '🔭 Universe'],
            'Revolutionary Warrior': ['⚔️ Revolution', '🗣️ Activism', '🤝 Solidarity'],
            'Crypto Sorceress': ['💰 Finance', '📈 Growth', '🔮 Strategy'],
            'Community Healer': ['🌿 Healing', '🤗 Support', '🏡 Sanctuary'],
            'Digital Guardian': ['🛡️ Security', '🔒 Privacy', '👀 Protection'],
            'Digital Phantom': ['👻 Anonymity', '🔐 Encryption', '🌐 Digital'],
            'Connection Curator': ['🔗 Connections', '💞 Community', '🎭 Social'],
            'Viral Prophet': ['📢 Prophecy', '✍️ Poetry', '🌊 Movement'],
            'Cyber Guardian': ['🛡️ Cybersecurity', '🔒 Protection', '💻 Tech'],
            'Visual Alchemist': ['🎨 Visuals', '🎬 Cinema', '📸 Art'],
            'Prism Enchantress': ['🌈 Aesthetic', '💎 Color', '✨ Beauty'],
            'Desert Storyteller': ['📖 Stories', '🏜️ Desert', '🌙 Ancient'],
            'Ephemeral Artist': ['⏳ Moments', '🌅 Temporal', '💫 Presence'],
            'Mirror Architect': ['🪞 Reflection', '⏰ Time', '🏛️ Design'],
            'Sage Writer': ['📚 Writing', '📝 Wisdom', '🧠 Intellect'],
            'Scavenger Strategist': ['🦅 Strategy', '💎 Resources', '📈 Growth'],
            'Wild Surrender': ['🐺 Untamed', '🌲 Freedom', '💪 Strength'],
            'Contractual Warden': ['⚖️ Legal', '📋 Compliance', '🏛️ Order'],
            'Ephemeral Phantom': ['🌫️ Mystery', '👻 Chase', '💫 Ephemeral'],
            'Temporal Architect': ['⏰ Time', '⚡ Efficiency', '📅 Schedule'],
            'Digital Deity': ['⚡ Energy', '🌐 Digital', '✨ Vibrant'],
            'Gothic Matriarch': ['🏰 Gothic', '🌙 Darkness', '💎 Elegance'],
            'Hyper-Capitalist': ['💎 Luxury', '💰 Wealth', '🏰 Empire'],
            'Machine Spirit': ['⚙️ Industrial', '🏭 Output', '🔧 Mechanical']
        }
        
        return base_highlights + archetype_highlights.get(archetype, [])
    
    def generate_instagram_content_strategy(self, soul_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate Instagram content strategy"""
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
                'posts': f"{hooks[0] if hooks else 'Archetype wisdom'} with visuals",
                'stories': f"Daily {archetype} insights and behind-the-scenes",
                'reels': f"Viral {archetype} content with trending audio",
                'igtv': f"Long-form {archetype} teachings and rituals"
            },
            'posting_frequency': '1-2 posts daily, 3-5 stories daily',
            'best_times': ['11 AM', '7 PM', '9 PM'],
            'hashtags': self.generate_instagram_hashtags(soul_data),
            'visual_theme': f"{archetype} aesthetic with tribal branding"
        }
    
    def generate_instagram_hashtags(self, soul_data: Dict[str, Any]) -> List[str]:
        """Generate Instagram hashtags for soul"""
        archetype = soul_data['archetype']
        
        base_hashtags = ['#Tiapmaatzu', '#Primal', '#HueMan-i-Terry', '#Transformation']
        archetype_hashtag = f"#{archetype.replace(' ', '')}"
        
        all_hashtags = base_hashtags + [archetype_hashtag]
        
        # Add niche hashtags based on desires
        desires = soul_data.get('desires', [])
        for desire in desires:
            niche_tag = f"#{desire.replace(' ', '')}"
            if len(niche_tag) <= 30:  # Instagram hashtag limit
                all_hashtags.append(niche_tag)
        
        return all_hashtags[:15]  # Limit to 15 hashtags
    
    def generate_instagram_visual_strategy(self, soul_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate Instagram visual strategy"""
        archetype = soul_data['archetype']
        
        return {
            'color_scheme': self.get_archetype_color_scheme(archetype),
            'visual_themes': self.get_archetype_visual_themes(archetype),
            'content_style': f"{self.get_archetype_content_style(archetype)} aesthetic",
            'consistency': 'Maintain consistent visual identity across all content'
        }
    
    def get_archetype_color_scheme(self, archetype: str) -> Dict[str, str]:
        """Get color scheme based on archetype"""
        color_schemes = {
            'High Priest': {'primary': '#FFD700', 'secondary': '#8B0000', 'accent': '#FFFFFF'},
            'Divine Mother': {'primary': '#FF69B4', 'secondary': '#FFB6C1', 'accent': '#FFFFFF'},
            'Seductive Muse': {'primary': '#800080', 'secondary': '#DDA0DD', 'accent': '#FFD700'},
            'Cosmic Mystic': {'primary': '#4B0082', 'secondary': '#9370DB', 'accent': '#00CED1'},
            'Revolutionary Warrior': {'primary': '#DC143C', 'secondary': '#FF6347', 'accent': '#FFD700'},
            'Crypto Sorceress': {'primary': '#00FF00', 'secondary': '#32CD32', 'accent': '#FFD700'},
            'Community Healer': {'primary': '#228B22', 'secondary': '#32CD32', 'accent': '#90EE90'},
            'Digital Guardian': {'primary': '#1E90FF', 'secondary': '#4169E1', 'accent': '#87CEEB'},
            'Digital Phantom': {'primary': '#2F4F4F', 'secondary': '#708090', 'accent': '#00CED1'},
            'Connection Curator': {'primary': '#FF6347', 'secondary': '#FFA07A', 'accent': '#FFD700'},
            'Viral Prophet': {'primary': '#FF4500', 'secondary': '#FF6347', 'accent': '#FFD700'},
            'Cyber Guardian': {'primary': '#008080', 'secondary': '#20B2AA', 'accent': '#87CEEB'},
            'Visual Alchemist': {'primary': '#FF8C00', 'secondary': '#FFA500', 'accent': '#FFD700'},
            'Prism Enchantress': {'primary': '#FF69B4', 'secondary': '#FFB6C1', 'accent': '#87CEEB'},
            'Desert Storyteller': {'primary': '#D2691E', 'secondary': '#CD853F', 'accent': '#FFD700'},
            'Ephemeral Artist': {'primary': '#708090', 'secondary': '#B0C4DE', 'accent': '#E0FFFF'},
            'Mirror Architect': {'primary': '#C0C0C0', 'secondary': '#D3D3D3', 'accent': '#F0F0F0'},
            'Sage Writer': {'primary': '#556B2F', 'secondary': '#8FBC8F', 'accent': '#90EE90'},
            'Scavenger Strategist': {'primary': '#B8860B', 'secondary': '#DAA520', 'accent': '#FFD700'},
            'Wild Surrender': {'primary': '#8B4513', 'secondary': '#CD853F', 'accent': '#D2691E'},
            'Contractual Warden': {'primary': '#2F4F4F', 'secondary': '#696969', 'accent': '#A9A9A9'},
            'Ephemeral Phantom': {'primary': '#483D8B', 'secondary': '#7B68EE', 'accent': '#87CEEB'},
            'Temporal Architect': {'primary': '#708090', 'secondary': '#B0C4DE', 'accent': '#E0FFFF'},
            'Digital Deity': {'primary': '#FF00FF', 'secondary': '#FF69B4', 'accent': '#00FFFF'},
            'Gothic Matriarch': {'primary': '#191970', 'secondary': '#4B0082', 'accent': '#E6E6FA'},
            'Hyper-Capitalist': {'primary': '#FFD700', 'secondary': '#C0C0C0', 'accent': '#FF69B4'},
            'Machine Spirit': {'primary': '#696969', 'secondary': '#A9A9A9', 'accent': '#D3D3D3'}
        }
        
        return color_schemes.get(archetype, {'primary': '#1a1a2e', 'secondary': '#e94560', 'accent': '#FFD700'})
    
    def get_archetype_visual_themes(self, archetype: str) -> List[str]:
        """Get visual themes based on archetype"""
        visual_themes = {
            'High Priest': ['Ceremonial', 'Mystical', 'Temple', 'Ancient', 'Spiritual'],
            'Divine Mother': ['Nurturing', 'Soft', 'Floral', 'Warm', 'Motherly'],
            'Seductive Muse': ['Sensual', 'Artistic', 'Burlesque', 'Elegant', 'Mysterious'],
            'Cosmic Mystic': ['Cosmic', 'Stellar', 'Celestial', 'Ethereal', 'Scientific'],
            'Revolutionary Warrior': ['Bold', 'Revolutionary', 'Red', 'Strong', 'Activist'],
            'Crypto Sorceress': ['Digital', 'Financial', 'Cryptic', 'Green', 'Strategic'],
            'Community Healer': ['Natural', 'Healing', 'Soft', 'Warm', 'Supportive'],
            'Digital Guardian': ['Technical', 'Security', 'Blue', 'Clean', 'Protective'],
            'Digital Phantom': ['Dark', 'Anonymous', 'Encrypted', 'Hidden', 'Digital'],
            'Connection Curator': ['Social', 'Warm', 'Connecting', 'Colorful', 'Community'],
            'Viral Prophet': ['Bold', 'Poetic', 'Artistic', 'Raw', 'Powerful'],
            'Cyber Guardian': ['Technical', 'Secure', 'Teal', 'Clean', 'Defensive'],
            'Visual Alchemist': ['Cinematic', 'Artistic', 'Golden', 'Dramatic', 'Creative'],
            'Prism Enchantress': ['Colorful', 'Light', 'Rainbow', 'Refraction', 'Beautiful'],
            'Desert Storyteller': ['Earthy', 'Ancient', 'Warm', 'Storytelling', 'Mystical'],
            'Ephemeral Artist': ['Temporal', 'Fleeting', 'Subtle', 'Ethereal', 'Present'],
            'Mirror Architect': ['Reflective', 'Precise', 'Geometric', 'Temporal', 'Architectural'],
            'Sage Writer': ['Academic', 'Wise', 'Literary', 'Thoughtful', 'Intellectual'],
            'Scavenger Strategist': ['Strategic', 'Opportunistic', 'Golden', 'Sharp', 'Tactical'],
            'Wild Surrender': ['Untamed', 'Raw', 'Natural', 'Free', 'Wild'],
            'Contractual Warden': ['Clinical', 'Precise', 'Formal', 'Structured', 'Legal'],
            'Ephemeral Phantom': ['Mysterious', 'Elusive', 'Dark', 'Fleeting', 'Digital'],
            'Temporal Architect': ['Precise', 'Organized', 'Rhythmic', 'Time-focused', 'Efficient'],
            'Digital Deity': ['Electric', 'Vibrant', 'Colorful', 'High-energy', 'Digital'],
            'Gothic Matriarch': ['Dark', 'Elegant', 'Sophisticated', 'Mourning', 'Classic'],
            'Hyper-Capitalist': ['Luxurious', 'Golden', 'Expensive', 'Bold', 'Opulent'],
            'Machine Spirit': ['Industrial', 'Mechanical', 'Technical', 'Structured', 'Efficient']
        }
        
        return visual_themes.get(archetype, ['Mystical', 'Transformational', 'Tribal', 'Archetype-specific'])
    
    def get_archetype_content_style(self, archetype: str) -> str:
        """Get content style based on archetype"""
        content_styles = {
            'High Priest': 'Ceremonial and authoritative',
            'Divine Mother': 'Nurturing and warm',
            'Seductive Muse': 'Seductive and artistic',
            'Cosmic Mystic': 'Transcendent and philosophical',
            'Revolutionary Warrior': 'Passionate and bold',
            'Crypto Sorceress': 'Mysterious and calculating',
            'Community Healer': 'Gentle and supportive',
            'Digital Guardian': 'Technical and protective',
            'Digital Phantom': 'Anonymous and encrypted',
            'Connection Curator': 'Warm and social',
            'Viral Prophet': 'Poetic and powerful',
            'Cyber Guardian': 'Technical and secure',
            'Visual Alchemist': 'Artistic and visionary',
            'Prism Enchantress': 'Aesthetic and enchanting',
            'Desert Storyteller': 'Ancient and storytelling',
            'Ephemeral Artist': 'Ethereal and temporal',
            'Mirror Architect': 'Precise and architectural',
            'Sage Writer': 'Intellectual and wise',
            'Scavenger Strategist': 'Strategic and tactical',
            'Wild Surrender': 'Untamed and authentic',
            'Contractual Warden': 'Clinical and precise',
            'Ephemeral Phantom': 'Mysterious and elusive',
            'Temporal Architect': 'Organized and efficient',
            'Digital Deity': 'Electric and vibrant',
            'Gothic Matriarch': 'Sophisticated and elegant',
            'Hyper-Capitalist': 'Bold and luxurious',
            'Machine Spirit': 'Industrial and mechanical'
        }
        
        return content_styles.get(archetype, 'Mystical and transformative')
    
    def generate_instagram_engagement_strategy(self, soul_data: Dict[str, Any]) -> Dict[str, str]:
        """Generate Instagram engagement strategy"""
        rarity = soul_data.get('rarity', 'Common')
        
        return {
            'response_time': 'Within 24 hours for HueMan-i-Terry member comments and DMs',
            'engagement_style': 'Personal, warm, archetype-appropriate',
            'story_responses': 'Respond to story mentions and DMs within 12 hours',
            'live_streams': 'Host weekly Instagram Live sessions',
            'collaboration': 'Collaborate with other HueMan-i-Terry souls weekly'
        }
    
    def generate_instagram_posting_schedule(self, soul_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate Instagram posting schedule"""
        archetype = soul_data['archetype']
        
        return {
            'daily_posts': 1,
            'daily_stories': 3,
            'weekly_reels': 2,
            'monthly_igtv': 1,
            'weekly_lives': 1,
            'optimal_times': ['11 AM', '7 PM', '9 PM'],
            'content_mix': {
                'posts': '40%',
                'stories': '40%',
                'reels': '15%',
                'igtv': '5%'
            }
        }
    
    def generate_instagram_growth_targets(self, soul_data: Dict[str, Any]) -> Dict[str, int]:
        """Generate Instagram growth targets"""
        rarity = soul_data.get('rarity', 'Common')
        
        targets = {
            'month_1': 500,
            'month_3': 1000,
            'month_6': 2500,
            'month_12': 5000
        }
        
        # Adjust targets based on rarity
        if rarity == 'Legendary':
            targets = {k: v * 2 for k, v in targets.items()}
        elif rarity == 'Rare':
            targets = {k: int(v * 1.5) for k, v in targets.items()}
        
        return targets
    
    def generate_instagram_tools_setup(self, soul_data: Dict[str, Any]) -> Dict[str, List[str]]:
        """Generate tools setup for soul"""
        rarity = soul_data.get('rarity', 'Common')
        
        if rarity == 'Legendary':
            return {
                'essential': ['Instagram Creator Studio', 'Instagram Insights'],
                'recommended': ['Buffer', 'Later', 'Iconosquare'],
                'advanced': ['Hootsuite', 'Sprout Social', 'Canva']
            }
        elif rarity == 'Rare':
            return {
                'essential': ['Instagram Creator Studio', 'Instagram Insights'],
                'recommended': ['Buffer', 'Later'],
                'advanced': ['Canva', 'Iconosquare']
            }
        else:
            return {
                'essential': ['Instagram Creator Studio', 'Instagram Insights'],
                'recommended': ['Buffer'],
                'advanced': ['Canva']
            }
    
    def generate_master_instagram_setup(self) -> Dict[str, Any]:
        """Generate master Instagram setup for all souls"""
        souls = self.souls_data['souls']
        
        master_setup = {
            'instagram_configuration': self.instagram_config,
            'soul_setups': {},
            'setup_timeline': self.create_instagram_setup_timeline(),
            'resource_requirements': self.calculate_instagram_resources(),
            'coordination_strategy': self.create_coordination_strategy(),
            'generated_at': datetime.now().isoformat()
        }
        
        for soul in souls:
            if 'Instagram' in soul.get('platforms', []):
                soul_setup = self.generate_soul_instagram_setup(soul)
                master_setup['soul_setups'][soul['id']] = soul_setup
        
        return master_setup
    
    def create_instagram_setup_timeline(self) -> Dict[str, Any]:
        """Create Instagram setup timeline"""
        return {
            'phase_1_day_1': {
                'focus': 'Account Creation & Basic Setup',
                'tasks': [
                    'Create all Instagram accounts',
                    'Set up Creator accounts',
                    'Configure two-factor authentication',
                    'Set up basic profile information',
                    'Switch to Creator account'
                ],
                'estimated_hours': 4
            },
            'phase_2_day_2': {
                'focus': 'Profile Optimization',
                'tasks': [
                    'Upload profile pictures',
                    'Write optimized bios',
                    'Set up website links',
                    'Create initial story highlights',
                    'Configure contact buttons'
                ],
                'estimated_hours': 3
            },
            'phase_3_day_3': {
                'focus': 'Content Calendar Setup',
                'tasks': [
                    'Create content templates for each soul',
                    'Set up posting schedules',
                    'Configure hashtag strategies',
                    'Create initial content queue',
                    'Set up automation tools'
                ],
                'estimated_hours': 4
            },
            'phase_4_day_4': {
                'focus': 'Visual Content Creation',
                'tasks': [
                    'Create initial post images',
                    'Design story highlight covers',
                    'Create Reels templates',
                    'Set up visual style guide',
                    'Create brand assets'
                ],
                'estimated_hours': 5
            },
            'phase_5_day_5': {
                'focus': 'Engagement & Community',
                'tasks': [
                    'Set up Instagram Live schedule',
                    'Configure engagement protocols',
                    'Set up collaboration strategy',
                    'Create cross-promotion plan',
                    'Train on Instagram best practices'
                ],
                'estimated_hours': 3
            }
        }
    
    def calculate_instagram_resources(self) -> Dict[str, Any]:
        """Calculate resource requirements for Instagram setup"""
        return {
            'total_estimated_hours': 19,
            'financial_requirements': {
                'basic_tools': 'Free (Instagram Creator Studio, Insights)',
                'recommended_tools': '$15-35/month (Buffer, Later)',
                'advanced_tools': '$50-150/month (Hootsuite, Sprout Social)',
                'advertising': '$500-2000/month for growth campaigns',
                'content_creation': '$200-1000/month for graphics and video'
            },
            'human_resources': {
                'instagram_manager': '1 primary Instagram manager',
                'content_creators': '2-3 content creators for visuals/Reels',
                'photographer': '1 photographer for high-quality content',
                'video_editor': '1 video editor for Reels and content'
            },
            'ongoing_maintenance': {
                'daily': 'Post 1-2 posts, 3-5 stories, engage with community',
                'weekly': 'Review analytics, optimize content, host Live',
                'monthly': 'Deep analytics review, strategy adjustment, content planning',
                'quarterly': 'Comprehensive strategy review and optimization'
            }
        }
    
    def create_coordination_strategy(self) -> Dict[str, Any]:
        """Create cross-soul coordination strategy"""
        return {
            'cross_promotion': {
                'collaborative_reels': 'Monthly collaborative Reels between souls',
                'story_sharing': 'Share HueMan-i-Terry content across stories',
                'live_collaboration': 'Co-hosted Instagram Live sessions',
                'giveaway_coordination': 'Coordinated HueMan-i-Terry giveaways'
            },
            'content_coordination': {
                'content_calendar': 'Master content calendar for all souls',
                'thematic_weeks': 'Weekly themes coordinated across souls',
                'hashtag_coordination': 'Coordinated hashtag campaigns',
                'visual_consistency': 'Unified visual identity guidelines'
            },
            'community_management': {
                'shared_highlight': 'Shared story highlight for HueMan-i-Terry announcements',
                'unified_responses': 'Coordinated responses to HueMan-i-Terry member questions',
                'escalation_procedures': 'Clear escalation procedures for issues',
                'success_sharing': 'Share and celebrate community wins'
            }
        }

def main():
    """Main function to generate Instagram setup"""
    print("=" * 60)
    print("Tiapma'atzu Instagram Setup Generator")
    print("=" * 60)
    
    generator = InstagramSetupGenerator()
    
    # Generate master setup
    master_setup = generator.generate_master_instagram_setup()
    
    print(f"\nTotal Souls with Instagram: {len(master_setup['soul_setups'])}")
    print(f"Total Estimated Setup Hours: {master_setup['resource_requirements']['total_estimated_hours']}")
    
    print("\nInstagram Setup Timeline:")
    for phase, details in master_setup['setup_timeline'].items():
        print(f"  {phase}: {details['focus']} ({details['estimated_hours']} hours)")
    
    # Save master setup
    output_path = Path("scripts/instagram_master_setup.json")
    with open(output_path, 'w') as f:
        json.dump(master_setup, f, indent=2, default=str)
    
    print(f"\n✓ Master Instagram setup saved to {output_path}")
    
    # Generate individual setup guides
    for soul_id, soul_setup in master_setup['soul_setups'].items():
        soul_name = soul_setup['name']
        individual_path = Path(f"scripts/instagram_setup_{soul_id}.json")
        with open(individual_path, 'w') as f:
            json.dump(soul_setup, f, indent=2, default=str)
    
    print(f"✓ Individual setup guides saved for all {len(master_setup['soul_setups'])} Instagram souls")
    
    print("\n" + "=" * 60)
    print("Instagram Setup Generation Complete")
    print("=" * 60)

if __name__ == "__main__":
    main()