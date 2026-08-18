"""
Twitter Setup Generator for Tiapma'atzu Souls
Generates individualized Twitter setup instructions for each soul
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

class TwitterSetupGenerator:
    """Generate Twitter setup instructions for each soul"""
    
    def __init__(self):
        self.souls_data = self.load_souls_data()
        self.twitter_config = self.create_twitter_configuration()
    
    def load_souls_data(self) -> Dict[str, Any]:
        """Load souls data from JSON file"""
        souls_path = Path("src/data/souls_entities.json")
        with open(souls_path, 'r') as f:
            return json.load(f)
    
    def create_twitter_configuration(self) -> Dict[str, Any]:
        """Create Twitter-specific configuration"""
        return {
            'account_setup': self.create_account_setup_config(),
            'profile_optimization': self.create_profile_optimization(),
            'content_strategy': self.create_content_strategy(),
            'engagement_tactics': self.create_engagement_tactics(),
            'automation_tools': self.create_automation_tools(),
            'analytics_setup': self.create_analytics_setup(),
            'growth_strategy': self.create_growth_strategy()
        }
    
    def create_account_setup_config(self) -> Dict[str, Any]:
        """Create Twitter account setup configuration"""
        return {
            'naming_conventions': {
                'format': '@soulname_tiapmaatzu',
                'alternatives': ['@soulname_HueMan-i-Terry', '@archetype_soulname', '@tiapmaatzu_soulname'],
                'length_limit': '15 characters maximum',
                'case_sensitive': 'False',
                'special_chars': 'Only underscores allowed'
            },
            'verification_requirements': {
                'email': 'Required - use HueMan-i-Terry email',
                'phone': 'Required for initial setup',
                'two_factor': 'Enable authenticator app (not SMS)',
                'password_requirements': '12+ characters, mix of letters, numbers, symbols'
            },
            'initial_settings': {
                'language': 'English',
                'country': 'United States',
                'time_zone': 'Set to primary HueMan-i-Terry location',
                'protected_tweets': 'False (for growth)',
                'photo_tagging': 'Allowed by people you follow',
                'direct_messages': 'Open to everyone',
                'discoverability': 'Yes - allow discovery by email/phone'
            }
        }
    
    def create_profile_optimization(self) -> Dict[str, Any]:
        """Create Twitter profile optimization guidelines"""
        return {
            'profile_image': {
                'specs': '400x400px minimum, 2MB max size',
                'format': 'JPG or PNG',
                'style': 'Professional soul portrait with tribal branding',
                'consistency': 'Use same image across all platforms'
            },
            'header_image': {
                'specs': '1500x500px recommended, 5MB max size',
                'format': 'JPG or PNG',
                'style': 'Archetype-themed with tribal branding',
                'content': 'Include hook, archetype symbols, call to action'
            },
            'bio': {
                'length_limit': '160 characters',
                'structure': '{archetype} | {hook} | {value_proposition} | CTA',
                'hashtags': 'Include 1-2 relevant hashtags',
                'emoji': 'Use sparingly, archetype-appropriate',
                'link': 'Include HueMan-i-Terry landing page or Discord invite'
            },
            'location': {
                'setting': 'Use spiritual location or HueMan-i-Terry headquarters',
                'examples': ['Temple of Transformation', 'Digital Realm', 'Cosmic Plane']
            },
            'website': {
                'primary': 'HueMan-i-Terry landing page',
                'alternatives': ['Discord invite', 'Linktree with all platforms', 'Specific project page']
            },
            'pinned_tweet': {
                'purpose': 'Introduce soul and HueMan-i-Terry',
                'content': 'Welcome message with archetype focus and call to action',
                'media': 'Include image or video of soul',
                'engagement': 'Pin highest performing introduction tweet'
            }
        }
    
    def create_content_strategy(self) -> Dict[str, Any]:
        """Create Twitter content strategy"""
        return {
            'content_types': {
                'wisdom_tweets': {
                    'frequency': '1-2 daily',
                    'length': '240-280 characters',
                    'purpose': 'Share archetype wisdom and insights',
                    'format': 'Insight + hook + question'
                },
                'threads': {
                    'frequency': 'Weekly',
                    'length': '5-10 tweets per thread',
                    'purpose': 'Deep dive into topics, education, storytelling',
                    'format': 'Hook -> Points -> Conclusion -> CTA'
                },
                'engagement_tweets': {
                    'frequency': 'Daily',
                    'length': '140-280 characters',
                    'purpose': 'Reply to followers, ask questions, build community',
                    'format': 'Personal response + follow-up question'
                },
                'visual_content': {
                    'frequency': '3-4 weekly',
                    'formats': ['Images', 'Videos', 'GIFs', 'Carousel'],
                    'purpose': 'Visual storytelling, showcase archetype aesthetics',
                    'specs': 'Images: 16:9 ratio, Videos: 2:20 max, GIFs: 15MB max'
                },
                'live_content': {
                    'frequency': 'Weekly',
                    'formats': ['Spaces', 'Live video', 'Periscope'],
                    'purpose': 'Real-time connection, ritual ceremonies, Q&A',
                    'topics': 'Archetype-specific discussions, tribal announcements'
                }
            },
            'posting_schedule': {
                'optimal_times': ['9 AM', '12 PM', '3 PM', '7 PM', '10 PM'],
                'frequency': '3-5 tweets daily',
                'consistency': 'Maintain consistent posting schedule',
                'tools': ['Buffer', 'Hootsuite', 'TweetDeck']
            },
            'hashtag_strategy': {
                'primary': '#Tiapmaatzu #Primal #HueMan-i-Terry',
                'archetype_specific': {
                    'High Priest': '#HighPriest #Spiritual #Ritual',
                    'Divine Mother': '#DivineMother #Nurturing #Healing',
                    'Seductive Muse': '#SeductiveMuse #Burlesque #Desire',
                    'Cosmic Mystic': '#CosmicMystic #Stargazing #Cosmic',
                    'Revolutionary Warrior': '#RevolutionaryWarrior #Activism #Consent',
                    'Crypto Sorceress': '#CryptoSorceress #Finance #Crypto',
                    'Community Healer': '#CommunityHealer #Healing #Support',
                    'Digital Guardian': '#DigitalGuardian #Security #Privacy',
                    'Digital Phantom': '#DigitalPhantom #Anonymity #Encryption',
                    'Connection Curator': '#ConnectionCurator #Community #Dating',
                    'Viral Prophet': '#ViralProphet #Poetry #Movement',
                    'Cyber Guardian': '#CyberGuardian #Cybersecurity #Tech',
                    'Visual Alchemist': '#VisualAlchemist #Cinematic #Art',
                    'Prism Enchantress': '#PrismEnchantress #Aesthetic #Color',
                    'Desert Storyteller': '#DesertStoryteller #Storytelling #Myth',
                    'Ephemeral Artist': '#EphemeralArtist #Temporal #Presence',
                    'Mirror Architect': '#MirrorArchitect #Time #Reflection',
                    'Sage Writer': '#SageWriter #Writing #Wisdom',
                    'Scavenger Strategist': '#ScavengerStrategist #Strategy #Wealth',
                    'Wild Surrender': '#WildSurrender #Untamed #Freedom',
                    'Contractual Warden': '#ContractualWarden #Legal #Compliance',
                    'Ephemeral Phantom': '#EphemeralPhantom #Chase #Mystery',
                    'Temporal Architect': '#TemporalArchitect #Time #Efficiency',
                    'Digital Deity': '#DigitalDeity #Energy #Attention',
                    'Gothic Matriarch': '#GothicMatriarch #Gothic #Grief',
                    'Hyper-Capitalist': '#HyperCapitalist #Luxury #Wealth',
                    'Machine Spirit': '#MachineSpirit #Industrial #Output'
                },
                'niche_hashtags': [
                    '#ShadowWork #Transformation #Community #HueMan-i-Terry',
                    '#SpiritualAwakening #Primal #Consciousness',
                    '#KinkCommunity #Consent #SexPositive'
                ]
            }
        }
    
    def create_engagement_tactics(self) -> Dict[str, Any]:
        """Create Twitter engagement tactics"""
        return {
            'follower_engagement': {
                'response_time': 'Within 1 hour for HueMan-i-Terry members, 24 hours for others',
                'response_style': 'Personal, warm, archetype-appropriate',
                'follow_back': 'Follow HueMan-i-Terry members back selectively',
                'interaction': 'Like and reply to HueMan-i-Terry member tweets'
            },
            'community_building': {
                'lists': {
                    'create_lists': [
                        'Tiapma\'atzu HueMan-i-Terry',
                        'Archetype Circle',
                        'HueMan-i-Terry Allies',
                        'Industry Peers'
                    ],
                    'add_members': 'Add HueMan-i-Terry members to appropriate lists',
                    'curate_content': 'Share list content regularly'
                },
                'spaces': {
                    'hosting': 'Weekly archetype-specific Spaces',
                    'topics': 'Archetype wisdom, tribal announcements, Q&A',
                    'guests': 'Invite other souls as guest speakers',
                    'promotion': 'Promote Spaces 24 hours in advance'
                },
                'twitter_chats': {
                    'participate': 'Join relevant Twitter chats',
                    'host': 'Host monthly #Tiapmaatzu Twitter chat',
                    'topics': 'Archetype-specific discussions, tribal updates'
                }
            },
            'growth_tactics': {
                'retweets': 'Retweet valuable HueMan-i-Terry content',
                'mentions': 'Mention other souls for cross-promotion',
                'quotes': 'Quote tweets with thoughtful commentary',
                'threads': 'Create shareable content for retweets',
                'trends': 'Participate in relevant trending topics'
            }
        }
    
    def create_automation_tools(self) -> Dict[str, Any]:
        """Create Twitter automation tools setup"""
        return {
            'scheduling_tools': [
                {
                    'name': 'TweetDeck',
                    'purpose': 'Twitter native scheduling and management',
                    'features': ['Schedule tweets', 'Monitor lists', 'Track mentions', 'Manage multiple accounts'],
                    'cost': 'Free'
                },
                {
                    'name': 'Buffer',
                    'purpose': 'Advanced scheduling and analytics',
                    'features': ['Queue scheduling', 'Analytics', 'RSS integration', 'Team collaboration'],
                    'cost': '$15/month for premium'
                },
                {
                    'name': 'Hootsuite',
                    'purpose': 'Enterprise social media management',
                    'features': ['Multi-platform scheduling', 'Analytics', 'Team management', 'Social listening'],
                    'cost': '$99/month for professional'
                }
            ],
            'automation_workflows': [
                {
                    'tool': 'IFTTT',
                    'purpose': 'Automated cross-platform posting',
                    'workflows': [
                        'Twitter → Discord auto-post',
                        'Twitter → Instagram cross-post',
                        'Twitter → Email notifications for mentions'
                    ]
                },
                {
                    'tool': 'Zapier',
                    'purpose': 'Advanced automation and integrations',
                    'workflows': [
                        'Twitter mentions → CRM integration',
                        'Twitter → Spreadsheet logging',
                        'Twitter → Analytics dashboard'
                    ]
                }
            ],
            'analytics_tools': [
                {
                    'name': 'Twitter Analytics',
                    'purpose': 'Native Twitter analytics',
                    'features': ['Engagement metrics', 'Follower growth', 'Tweet performance'],
                    'cost': 'Free'
                },
                {
                    'name': 'Social Blade',
                    'purpose': 'Advanced Twitter analytics',
                    'features': ['Follower tracking', 'Competitor analysis', 'Growth predictions'],
                    'cost': '$10/month for basic'
                }
            ]
        }
    
    def create_analytics_setup(self) -> Dict[str, Any]:
        """Create Twitter analytics setup"""
        return {
            'key_metrics': {
                'engagement_rate': 'Calculate: (likes + retweets + replies) / followers',
                'follower_growth': 'Track daily/weekly/monthly follower changes',
                'tweet_performance': 'Analyze which content types perform best',
                'profile_visits': 'Track how many people view profile',
                'mentions': 'Monitor brand mentions and conversations'
            },
            'reporting_frequency': {
                'daily': 'Quick metrics check',
                'weekly': 'Performance analysis and optimization',
                'monthly': 'Comprehensive growth report',
                'quarterly': 'Strategy review and adjustment'
            },
            'benchmarking': {
                'internal': 'Compare performance against other souls',
                'external': 'Compare against industry standards',
                'goals': 'Set realistic growth targets based on benchmarks'
            }
        }
    
    def create_growth_strategy(self) -> Dict[str, Any]:
        """Create Twitter growth strategy"""
        return {
            'growth_phases': {
                'phase_1_month_1': {
                    'focus': 'Foundation Building',
                    'goals': ['500 followers', '10k total impressions', '5% engagement rate'],
                    'tactics': ['Optimize profile', 'Post consistently', 'Engage with HueMan-i-Terry']
                },
                'phase_2_month_2': {
                    'focus': 'Content Expansion',
                    'goals': ['1,000 followers', '25k total impressions', '4% engagement rate'],
                    'tactics': ['Introduce visual content', 'Start Twitter Spaces', 'Create threads']
                },
                'phase_3_month_3': {
                    'focus': 'Community Scaling',
                    'goals': ['2,500 followers', '50k total impressions', '3.5% engagement rate'],
                    'tactics': ['Collaborate with other souls', 'Host regular Spaces', 'Increase visual content']
                },
                'phase_4_month_4': {
                    'focus': 'Influence Building',
                    'goals': ['5,000 followers', '100k total impressions', '3% engagement rate'],
                    'tactics': ['Guest appearances', 'Viral content creation', 'Cross-platform promotion']
                }
            },
            'growth_tactics': {
                'organic': [
                    'Consistent posting schedule',
                    'Engage with target audience',
                    'Participate in relevant conversations',
                    'Create shareable content',
                    'Optimize posting times'
                ],
                'collaborative': [
                    'Twitter Spaces with other souls',
                    'Thread collaborations',
                    'Mention and retweet HueMan-i-Terry members',
                    'Guest posting in relevant accounts',
                    'Joint content creation'
                ],
                'content_based': [
                    'Create viral-worthy content',
                    'Use trending topics strategically',
                    'Optimize hashtags and timing',
                    'Create compelling visuals',
                    'Write engaging hooks'
                ]
            }
        }
    
    def generate_soul_twitter_setup(self, soul_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate individualized Twitter setup for a soul"""
        soul_id = soul_data['id']
        soul_name = soul_data['name']
        archetype = soul_data['archetype']
        
        setup = {
            'soul_id': soul_id,
            'name': soul_name,
            'archetype': archetype,
            'account_setup': self.generate_twitter_account_setup(soul_data),
            'profile_optimization': self.generate_twitter_profile_optimization(soul_data),
            'content_strategy': self.generate_twitter_content_strategy(soul_data),
            'engagement_strategy': self.generate_twitter_engagement_strategy(soul_data),
            'posting_schedule': self.generate_posting_schedule(soul_data),
            'growth_targets': self.generate_growth_targets(soul_data),
            'tools_setup': self.generate_tools_setup(soul_data),
            'analytics_config': self.generate_analytics_config(soul_data)
        }
        
        return setup
    
    def generate_twitter_account_setup(self, soul_data: Dict[str, Any]) -> Dict[str, str]:
        """Generate Twitter account setup"""
        soul_name = soul_data['name']
        archetype = soul_data['archetype']
        
        # Generate handle options
        handle_options = [
            f"@{soul_name.lower().replace(' ', '')}_tiapmaatzu",
            f"@{soul_name.lower().replace(' ', '')}_HueMan-i-Terry",
            f"@{archetype.lower()}_{soul_name.lower().replace(' ', '')}",
            f"@tiapmaatzu_{soul_name.lower().replace(' ', '')}"
        ]
        
        # Filter handles that meet Twitter's requirements
        valid_handles = [h for h in handle_options if len(h.replace('@', '')) <= 15]
        
        return {
            'recommended_handle': valid_handles[0] if valid_handles else handle_options[0],
            'alternative_handles': valid_handles[1:] if len(valid_handles) > 1 else handle_options[1:],
            'email': soul_data.get('email', 'Set up HueMan-i-Terry email'),
            'display_name': soul_name,
            'username_requirements': '15 characters max, letters, numbers, underscores only',
            'password_requirements': '12+ characters, mix of letters, numbers, symbols'
        }
    
    def generate_twitter_profile_optimization(self, soul_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate Twitter profile optimization"""
        archetype = soul_data['archetype']
        hooks = soul_data.get('hooks', [])
        tribute_impact = soul_data.get('tribute_impact', '')
        
        # Generate bio
        bio_parts = [
            archetype,
            hooks[0] if hooks else 'Transforming through primal wisdom',
            tribute_impact[:30] if tribute_impact else 'Building HueMan-i-Terry prosperity',
            'Join the transformation'
        ]
        
        bio = ' | '.join(bio_parts)
        if len(bio) > 160:
            bio = ' | '.join(bio_parts[:3])  # Shorten if too long
        
        return {
            'handle': self.generate_twitter_account_setup(soul_data)['recommended_handle'],
            'display_name': soul_data['name'],
            'bio': bio,
            'profile_image': soul_data.get('image', 'Use soul image from arweave'),
            'header_image': f"Create archetype-themed header for {archetype}",
            'location': self.get_archetype_location(archetype),
            'website': 'https://tiapmaatzu.web.app',
            'theme_color': self.get_archetype_theme_color(archetype)
        }
    
    def get_archetype_location(self, archetype: str) -> str:
        """Get Twitter location based on archetype"""
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
    
    def get_archetype_theme_color(self, archetype: str) -> str:
        """Get theme color for Twitter profile"""
        colors = {
            'High Priest': '#FFD700',  # Gold
            'Divine Mother': '#FF69B4',  # Hot Pink
            'Seductive Muse': '#800080',  # Purple
            'Cosmic Mystic': '#4B0082',  # Indigo
            'Revolutionary Warrior': '#DC143C',  # Crimson
            'Crypto Sorceress': '#00FF00',  # Lime
            'Community Healer': '#228B22',  # Forest Green
            'Digital Guardian': '#1E90FF',  # Dodger Blue
            'Digital Phantom': '#2F4F4F',  # Dark Slate Gray
            'Connection Curator': '#FF6347',  # Tomato
            'Viral Prophet': '#FF4500',  # Orange Red
            'Cyber Guardian': '#008080',  # Teal
            'Visual Alchemist': '#FF8C00',  # Dark Orange
            'Prism Enchantress': '#FF69B4',  # Hot Pink
            'Desert Storyteller': '#D2691E',  # Chocolate
            'Ephemeral Artist': '#708090',  # Slate Gray
            'Mirror Architect': '#C0C0C0',  # Silver
            'Sage Writer': '#556B2F',  # Dark Olive Green
            'Scavenger Strategist': '#B8860B',  # Dark Goldenrod
            'Wild Surrender': '#8B4513',  # Saddle Brown
            'Contractual Warden': '#2F4F4F',  # Dark Slate Gray
            'Ephemeral Phantom': '#483D8B',  # Dark Slate Blue
            'Temporal Architect': '#708090',  # Slate Gray
            'Digital Deity': '#FF00FF',  # Magenta
            'Gothic Matriarch': '#191970',  # Midnight Blue
            'Hyper-Capitalist': '#FFD700',  # Gold
            'Machine Spirit': '#696969'  # Dim Gray
        }
        
        return colors.get(archetype, '#1a1a2e')
    
    def generate_twitter_content_strategy(self, soul_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate Twitter content strategy"""
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
                'wisdom_tweets': f"{hooks[0] if hooks else 'Archetype wisdom'}",
                'threads': f"Deep dive into {archetype} practices",
                'engagement': f"Respond to HueMan-i-Terry members with {archetype} perspective",
                'visual': f"Share {archetype} aesthetic content"
            },
            'posting_frequency': '3-5 tweets daily',
            'best_times': ['9 AM', '12 PM', '3 PM', '7 PM', '10 PM'],
            'hashtags': self.generate_hashtags(soul_data),
            'voice': f"{self.get_archetype_voice(archetype)} - {archetype} of the Tiapma'atzu HueMan-i-Terry"
        }
    
    def get_archetype_voice(self, archetype: str) -> str:
        """Get Twitter voice based on archetype"""
        voices = {
            'High Priest': 'Authoritative, spiritual, ceremonial',
            'Divine Mother': 'Nurturing, warm, maternal',
            'Seductive Muse': 'Seductive, artistic, alluring',
            'Cosmic Mystic': 'Cosmic, transcendent, philosophical',
            'Revolutionary Warrior': 'Passionate, radical, activist',
            'Crypto Sorceress': 'Mysterious, calculating, confident',
            'Community Healer': 'Gentle, supportive, healing',
            'Digital Guardian': 'Protective, technical, precise',
            'Digital Phantom': 'Mysterious, anonymous, encrypted',
            'Connection Curator': 'Warm, connecting, social',
            'Viral Prophet': 'Poetic, powerful, viral',
            'Cyber Guardian': 'Technical, protective, secure',
            'Visual Alchemist': 'Artistic, visionary, creative',
            'Prism Enchantress': 'Aesthetic, artistic, enchanting',
            'Desert Storyteller': 'Ancient, storytelling, wise',
            'Ephemeral Artist': 'Ethereal, temporal, present',
            'Mirror Architect': 'Precise, reflective, architectural',
            'Sage Writer': 'Wise, intellectual, profound',
            'Scavenger Strategist': 'Strategic, opportunistic, tactical',
            'Wild Surrender': 'Untamed, raw, authentic',
            'Contractual Warden': 'Clinical, precise, legalistic',
            'Ephemeral Phantom': 'Mysterious, fleeting, elusive',
            'Temporal Architect': 'Rhythmic, efficient, organized',
            'Digital Deity': 'Electric, vibrant, energetic',
            'Gothic Matriarch': 'Sophisticated, mournful, elegant',
            'Hyper-Capitalist': 'Bold, wealthy, confident',
            'Machine Spirit': 'Industrial, mechanical, productive'
        }
        
        return voices.get(archetype, 'Mystical, transformative, wise')
    
    def generate_hashtags(self, soul_data: Dict[str, Any]) -> List[str]:
        """Generate hashtags for soul"""
        archetype = soul_data['archetype']
        
        base_hashtags = ['#Tiapmaatzu', '#Primal', '#HueMan-i-Terry', '#Transformation']
        archetype_hashtag = f"#{archetype.replace(' ', '')}"
        
        all_hashtags = base_hashtags + [archetype_hashtag]
        
        # Add niche hashtags based on desires
        desires = soul_data.get('desires', [])
        for desire in desires:
            niche_tag = f"#{desire.replace(' ', '')}"
            if len(niche_tag) <= 20:  # Twitter hashtag limit
                all_hashtags.append(niche_tag)
        
        return all_hashtags[:5]  # Limit to 5 hashtags
    
    def generate_twitter_engagement_strategy(self, soul_data: Dict[str, Any]) -> Dict[str, str]:
        """Generate Twitter engagement strategy"""
        rarity = soul_data.get('rarity', 'Common')
        
        return {
            'response_time': 'Within 1 hour for HueMan-i-Terry members',
            'follow_strategy': 'Follow HueMan-i-Terry members back selectively',
            'engagement_style': 'Archetype-appropriate and authentic',
            'community_building': 'Participate in relevant conversations',
            'HueMan-i-Terry_support': 'Retweet and support other souls\' content',
            'moderation': 'Monitor and filter mentions if in High Council'
        }
    
    def generate_posting_schedule(self, soul_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate posting schedule"""
        archetype = soul_data['archetype']
        
        return {
            'daily_tweets': 3,
            'threads_per_week': 1,
            'spaces_per_week': 1,
            'visual_content_per_week': 3,
            'optimal_times': ['9 AM', '12 PM', '7 PM'],
            'content_mix': {
                'wisdom': '40%',
                'engagement': '30%',
                'promotional': '20%',
                'personal': '10%'
            }
        }
    
    def generate_growth_targets(self, soul_data: Dict[str, Any]) -> Dict[str, int]:
        """Generate growth targets"""
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
    
    def generate_tools_setup(self, soul_data: Dict[str, Any]) -> Dict[str, List[str]]:
        """Generate tools setup for soul"""
        rarity = soul_data.get('rarity', 'Common')
        
        if rarity == 'Legendary':
            return {
                'essential': ['TweetDeck', 'Twitter Analytics'],
                'recommended': ['Buffer', 'Social Blade', 'IFTTT'],
                'advanced': ['Hootsuite', 'Zapier', 'Sprout Social']
            }
        elif rarity == 'Rare':
            return {
                'essential': ['TweetDeck', 'Twitter Analytics'],
                'recommended': ['Buffer', 'Social Blade'],
                'advanced': ['IFTTT', 'Zapier']
            }
        else:
            return {
                'essential': ['TweetDeck', 'Twitter Analytics'],
                'recommended': ['Buffer'],
                'advanced': []
            }
    
    def generate_analytics_config(self, soul_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate analytics configuration"""
        return {
            'tracking_metrics': [
                'Follower growth',
                'Engagement rate',
                'Tweet impressions',
                'Profile visits',
                'Mentions'
            ],
            'reporting_frequency': 'Weekly review, monthly deep dive',
            'goal_tracking': 'Monthly comparison against growth targets',
            'optimization': 'Adjust content strategy based on top performers'
        }
    
    def generate_master_twitter_setup(self) -> Dict[str, Any]:
        """Generate master Twitter setup for all souls"""
        souls = self.souls_data['souls']
        
        master_setup = {
            'twitter_configuration': self.twitter_config,
            'soul_setups': {},
            'setup_timeline': self.create_twitter_setup_timeline(),
            'resource_requirements': self.calculate_twitter_resources(),
            'coordination_strategy': self.create_coordination_strategy(),
            'generated_at': datetime.now().isoformat()
        }
        
        for soul in souls:
            if 'Twitter' in soul.get('platforms', []):
                soul_setup = self.generate_soul_twitter_setup(soul)
                master_setup['soul_setups'][soul['id']] = soul_setup
        
        return master_setup
    
    def create_twitter_setup_timeline(self) -> Dict[str, Any]:
        """Create Twitter setup timeline"""
        return {
            'phase_1_day_1': {
                'focus': 'Account Creation & Basic Setup',
                'tasks': [
                    'Create all Twitter accounts',
                    'Set up two-factor authentication',
                    'Configure basic profile information',
                    'Set up TweetDeck for management',
                    'Create initial welcome tweets'
                ],
                'estimated_hours': 6
            },
            'phase_2_day_2': {
                'focus': 'Profile Optimization',
                'tasks': [
                    'Upload profile pictures and headers',
                    'Write optimized bios',
                    'Configure website links',
                    'Set up pinned tweets',
                    'Configure account settings'
                ],
                'estimated_hours': 4
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
                'estimated_hours': 5
            },
            'phase_4_day_4': {
                'focus': 'Engagement & Community',
                'tasks': [
                    'Set up Twitter Lists',
                    'Configure engagement protocols',
                    'Set up Spaces hosting schedule',
                    'Create cross-promotion strategy',
                    'Set up HueMan-i-Terry mention monitoring'
                ],
                'estimated_hours': 4
            },
            'phase_5_day_5': {
                'focus': 'Analytics & Optimization',
                'tasks': [
                    'Configure analytics tracking',
                    'Set up reporting systems',
                    'Create growth target tracking',
                    'Set up optimization protocols',
                    'Train on Twitter best practices'
                ],
                'estimated_hours': 3
            }
        }
    
    def calculate_twitter_resources(self) -> Dict[str, Any]:
        """Calculate resource requirements for Twitter setup"""
        return {
            'total_estimated_hours': 22,
            'financial_requirements': {
                'basic_tools': 'Free (TweetDeck, Twitter Analytics)',
                'recommended_tools': '$15-50/month (Buffer, Social Blade)',
                'advanced_tools': '$100-300/month (Hootsuite, Zapier)',
                'advertising': '$500-2000/month for growth campaigns'
            },
            'human_resources': {
                'twitter_manager': '1 primary Twitter manager',
                'content_creators': '2-3 content creators for visuals/threads',
                'community_manager': '1 community manager for engagement',
                'social_media_coordinator': '1 coordinator for cross-platform'
            },
            'ongoing_maintenance': {
                'daily': 'Post 3-5 tweets, engage with community',
                'weekly': 'Review analytics, optimize content, host Spaces',
                'monthly': 'Deep analytics review, strategy adjustment',
                'quarterly': 'Comprehensive strategy review and planning'
            }
        }
    
    def create_coordination_strategy(self) -> Dict[str, Any]:
        """Create cross-soul coordination strategy"""
        return {
            'cross_promotion': {
                'weekly_threads': 'Collaborative threads between souls',
                'shared_spaces': 'Co-hosted Twitter Spaces',
                'mention_strategy': 'Strategic mentions between souls',
                'retweet_circle': 'Circle of retweets for HueMan-i-Terry content'
            },
            'content_coordination': {
                'central_calendar': 'Master content calendar for all souls',
                'thematic_weeks': 'Weekly themes coordinated across souls',
                'hashtag_coordination': 'Coordinated hashtag campaigns',
                'viral_campaigns': 'Coordinated viral content campaigns'
            },
            'community_management': {
                'shared_lists': 'Shared Twitter Lists for HueMan-i-Terry members',
                'community_guidelines': 'Unified community management guidelines',
                'escalation_procedures': 'Clear escalation procedures for issues',
                'success_sharing': 'Share and celebrate community wins'
            }
        }

def main():
    """Main function to generate Twitter setup"""
    print("=" * 60)
    print("Tiapma'atzu Twitter Setup Generator")
    print("=" * 60)
    
    generator = TwitterSetupGenerator()
    
    # Generate master setup
    master_setup = generator.generate_master_twitter_setup()
    
    print(f"\nTotal Souls with Twitter: {len(master_setup['soul_setups'])}")
    print(f"Total Estimated Setup Hours: {master_setup['resource_requirements']['total_estimated_hours']}")
    
    print("\nTwitter Setup Timeline:")
    for phase, details in master_setup['setup_timeline'].items():
        print(f"  {phase}: {details['focus']} ({details['estimated_hours']} hours)")
    
    # Save master setup
    output_path = Path("scripts/twitter_master_setup.json")
    with open(output_path, 'w') as f:
        json.dump(master_setup, f, indent=2, default=str)
    
    print(f"\n✓ Master Twitter setup saved to {output_path}")
    
    # Generate individual setup guides
    for soul_id, soul_setup in master_setup['soul_setups'].items():
        soul_name = soul_setup['name']
        individual_path = Path(f"scripts/twitter_setup_{soul_id}.json")
        with open(individual_path, 'w') as f:
            json.dump(soul_setup, f, indent=2, default=str)
    
    print(f"✓ Individual setup guides saved for all {len(master_setup['soul_setups'])} Twitter souls")
    
    print("\n" + "=" * 60)
    print("Twitter Setup Generation Complete")
    print("=" * 60)

if __name__ == "__main__":
    main()