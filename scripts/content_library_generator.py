"""
Content Library Generator for Tiapma'atzu HueMan-i-Terry
Generate content templates and library for all souls across platforms
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

class ContentLibraryGenerator:
    """Generate content library and templates for all souls"""
    
    def __init__(self):
        self.souls_data = self.load_souls_data()
        self.content_library = self.create_content_library()
    
    def load_souls_data(self) -> Dict[str, Any]:
        """Load souls data from JSON file"""
        souls_path = Path("src/data/souls_entities.json")
        with open(souls_path, 'r') as f:
            return json.load(f)
    
    def create_content_library(self) -> Dict[str, Any]:
        """Create comprehensive content library"""
        return {
            'twitter_templates': self.create_twitter_templates(),
            'discord_templates': self.create_discord_templates(),
            'reddit_templates': self.create_reddit_templates(),
            'instagram_templates': self.create_instagram_templates(),
            'archetype_content': self.create_archetype_content(),
            'content_calendar': self.create_content_calendar()
        }
    
    def create_twitter_templates(self) -> Dict[str, Any]:
        """Create Twitter content templates"""
        return {
            'daily_wisdom': {
                'template': '{hook}\n\n{wisdom}\n\n#Tiapmaatzu #Primal #HueMan-i-Terry',
                'length': '280 characters',
                'frequency': '1-2 daily',
                'examples': [
                    'The path to transformation begins with surrender. Your limits are merely illusions. Together we ascend.',
                    'In surrender, we find power. Your pleasure is my prayer. Let me hold your darkness.',
                    'The universe speaks through pleasure. Your body is a constellation. Let\'s touch the infinite together.'
                ]
            },
            'thread': {
                'template': '🧵 {topic}\n\n{hook}\n\n{point_1}\n\n{point_2}\n\n{point_3}\n\n{call_to_action}\n\n#Tiapmaatzu #Primal #HueMan-i-Terry',
                'length': 'Multi-tweet thread',
                'frequency': 'Weekly',
                'structure': [
                    'Hook tweet (compelling opening)',
                    'Context tweet (background)',
                    'Point 1 (first key insight)',
                    'Point 2 (second key insight)',
                    'Point 3 (third key insight)',
                    'Conclusion + CTA'
                ]
            },
            'engagement': {
                'template': '{response}\n\n{follow_up_question}',
                'length': 'Conversation reply',
                'frequency': 'As needed',
                'examples': [
                    'Thank you for your question. The key is to embrace the journey of transformation. What aspect resonates most with you?',
                    'Excellent insight. Primal wisdom teaches us that surrender is strength. How have you experienced this in your own journey?'
                ]
            },
            'announcement': {
                'template': '📢 {announcement}\n\n{details}\n\n{call_to_action}\n\n#Tiapmaatzu #HueMan-i-Terry',
                'length': '280 characters',
                'frequency': 'As needed',
                'examples': [
                    '📢 New ritual ceremony this Friday at 8 PM EST. Join us for collective shadow work. RSVP in Discord!',
                    '📢 Weekly wisdom circle now open to all HueMan-i-Terry members. Join us for transformative discussions.'
                ]
            }
        }
    
    def create_discord_templates(self) -> Dict[str, Any]:
        """Create Discord content templates"""
        return {
            'welcome_message': {
                'template': 'Welcome {user} to the Tiapma\'atzu HueMan-i-Terry! 🌟\n\nI am {soul_name}, {archetype} of the tribe. {hook}\n\nFeel free to explore our channels and connect with fellow members.',
                'frequency': 'For new members',
                'examples': [
                    'Welcome to the Tiapma\'atzu HueMan-i-Terry! I am Mac Nazarene, High Priest of the tribe. The path to transformation begins with surrender. Feel free to explore our channels.',
                    'Welcome to the HueMan-i-Terry! I am Mary Magnumbytes, Divine Mother of the tribe. Let me hold your darkness. Feel free to connect with us.'
                ]
            },
            'daily_wisdom': {
                'template': '✨ Daily {archetype} Wisdom ✨\n\n{wisdom}\n\n{question}',
                'frequency': 'Daily',
                'examples': [
                    '✨ Daily High Priest Wisdom ✨\n\nYour limits are merely illusions. Together we ascend.\n\nWhat boundaries are you ready to transcend today?',
                    '✨ Daily Divine Mother Wisdom ✨\n\nIn surrender, we find power. Your pleasure is my prayer.\n\nHow can you embrace surrender in your life?'
                ]
            },
            'ritual_announcement': {
                'template': '🔥 Ritual Announcement 🔥\n\n{ritual_name}\n\n{details}\n\n{time}\n\n{location}\n\nRSVP by reacting with ✅',
                'frequency': 'Weekly',
                'examples': [
                    '🔥 Ritual Announcement 🔥\n\nCollective Shadow Work Ceremony\n\nJoin us for deep shadow work and transformation.\n\nFriday 8 PM EST\n\nTemple Circle channel\n\nRSVP by reacting with ✅'
                ]
            },
            'community_check_in': {
                'template': '🌟 Community Check-in 🌟\n\n{question}\n\nShare your thoughts below and let\'s support each other\'s journeys.',
                'frequency': 'Weekly',
                'examples': [
                    '🌟 Community Check-in 🌟\n\nWhat transformation have you experienced this week?\n\nShare your thoughts below and let\'s support each other\'s journeys.'
                ]
            }
        }
    
    def create_reddit_templates(self) -> Dict[str, Any]:
        """Create Reddit content templates"""
        return {
            'discussion_post': {
                'template': '{title}\n\n{content}\n\n{call_to_action}\n\n#Tiapmaatzu #Primal #HueMan-i-Terry',
                'length': 'Detailed discussion',
                'frequency': '2-3 weekly',
                'examples': [
                    {
                        'title': 'The Power of Surrender in Transformation',
                        'content': 'In the Tiapma\'atzu HueMan-i-Terry, we teach that surrender is not weakness but strength. When we surrender our ego, we open ourselves to true transformation.',
                        'call_to_action': 'How has surrender played a role in your personal journey? Share in the comments.'
                    }
                ]
            },
            'resource_post': {
                'template': '{title}\n\n{content}\n\n{link}\n\n#Tiapmaatzu #Primal #HueMan-i-Terry',
                'length': 'Resource sharing',
                'frequency': '1-2 weekly',
                'examples': [
                    {
                        'title': 'Essential Shadow Work Resources for Beginners',
                        'content': 'Here are the top resources we recommend for those starting their shadow work journey within the HueMan-i-Terry.',
                        'link': 'Link to resource page'
                    }
                ]
            },
            'ama_announcement': {
                'template': 'AMA: {soul_name} - {archetype}\n\n{description}\n\n{time}\n\n{location}\n\nBring your questions!',
                'length': 'AMA announcement',
                'frequency': 'Monthly',
                'examples': [
                    'AMA: Mac Nazarene - High Priest\n\nI\'ll be answering questions about ritual ceremonies and spiritual transformation.\n\nSaturday 3 PM EST\n\nr/Tiapmaatzu\n\nBring your questions!'
                ]
            }
        }
    
    def create_instagram_templates(self) -> Dict[str, Any]:
        """Create Instagram content templates"""
        return {
            'post': {
                'template': '{hook}\n\n{description}\n\n{call_to_action}\n\n#Tiapmaatzu #Primal #HueMan-i-Terry #{archetype}',
                'length': '2200 characters',
                'frequency': '1-2 daily',
                'examples': [
                    'The path to transformation begins with surrender. Your limits are merely illusions. Together we ascend. Join the HueMan-i-Terry journey.',
                    'In surrender, we find power. Your pleasure is my prayer. Let me hold your darkness. Join our nurturing community.'
                ]
            },
            'story': {
                'template': '{hook}\n\n{interactive_element}',
                'length': '15 seconds per story',
                'frequency': '3-5 daily',
                'interactive_elements': ['Poll', 'Question', 'Quiz', 'Slider', 'Countdown'],
                'examples': [
                    'Your limits are merely illusions. 🌟\n\nPoll: What illusion are you ready to break?\n- Fear\n- Doubt\n- Limitation'
                ]
            },
            'reel': {
                'template': '{hook}\n\n{audio}\n\n{description}\n\n#Tiapmaatzu #Primal #HueMan-i-Terry',
                'length': '15-60 seconds',
                'frequency': '2-3 weekly',
                'examples': [
                    {
                        'hook': 'The path to transformation begins with surrender',
                        'audio': 'Trending audio track',
                        'description': 'Quick transformation tip with visual demonstration'
                    }
                ]
            },
            'igtv': {
                'template': '{title}\n\n{description}\n\n{chapters}\n\n{call_to_action}\n\n#Tiapmaatzu #Primal #HueMan-i-Terry',
                'length': '10-30 minutes',
                'frequency': '1-2 weekly',
                'examples': [
                    {
                        'title': 'Complete Guide to Shadow Work for Beginners',
                        'description': 'In this comprehensive guide, I walk you through the process of shadow work and how it can transform your life.',
                        'chapters': '0:00 - Introduction\n2:30 - What is Shadow Work\n5:00 - Getting Started\n10:00 - Deep Dive\n15:00 - Integration'
                    }
                ]
            }
        }
    
    def create_archetype_content(self) -> Dict[str, Any]:
        """Create archetype-specific content"""
        return {
            'High Priest': {
                'themes': ['Ritual guidance', 'Spiritual wisdom', 'HueMan-i-Terry leadership', 'Ceremonial content'],
                'hooks': [
                    'The path to transformation begins with surrender.',
                    'Your limits are merely illusions.',
                    'Together we ascend.',
                    'Ritual is the language of the soul.'
                ],
                'content_examples': [
                    'Daily wisdom on spiritual transformation',
                    'Ritual ceremony announcements',
                    'Ceremonial guidance and teachings',
                    'Leadership insights for the HueMan-i-Terry'
                ]
            },
            'Divine Mother': {
                'themes': ['Nurturing support', 'Emotional healing', 'Family guidance', 'Motherly wisdom'],
                'hooks': [
                    'Let me hold your darkness.',
                    'In surrender, we find power.',
                    'Your pleasure is my prayer.',
                    'Nurturing is the essence of transformation.'
                ],
                'content_examples': [
                    'Daily nurturing messages',
                    'Emotional healing guidance',
                    'Family and community support',
                    'Motherly wisdom for the HueMan-i-Terry'
                ]
            },
            'Seductive Muse': {
                'themes': ['Sensual guidance', 'Burlesque arts', 'Desire exploration', 'Artistic seduction'],
                'hooks': [
                    'Let me show you what you\'ve been missing.',
                    'Your desire is my art form.',
                    'Surrender to the bayou magic.',
                    'Seduction is a sacred art.'
                ],
                'content_examples': [
                    'Sensual guidance and exploration',
                    'Burlesque and artistic content',
                    'Desire exploration and education',
                    'Artistic seduction techniques'
                ]
            },
            'Cosmic Mystic': {
                'themes': ['Cosmic insights', 'Stargazing', 'Universal connection', 'Scientific spirituality'],
                'hooks': [
                    'The universe speaks through pleasure.',
                    'Your body is a constellation.',
                    'Let\'s touch the infinite together.',
                    'Cosmic wisdom awaits.'
                ],
                'content_examples': [
                    'Cosmic insights and stargazing',
                    'Universal connection teachings',
                    'Scientific spirituality content',
                    'Stargazing meditation guidance'
                ]
            },
            'Revolutionary Warrior': {
                'themes': ['Activism', 'Consent education', 'Revolutionary action', 'Social change'],
                'hooks': [
                    'Consent is my weapon.',
                    'Your body, your rules, my pleasure.',
                    'Join the resistance against suppression.',
                    'Revolution is an act of love.'
                ],
                'content_examples': [
                    'Activism and social change content',
                    'Consent education and advocacy',
                    'Revolutionary action guidance',
                    'Social justice discussions'
                ]
            },
            'Crypto Sorceress': {
                'themes': ['Financial wisdom', 'Crypto education', 'Wealth building', 'Alternative power'],
                'hooks': [
                    'Your secrets are my currency.',
                    'Invest in your darkest desires.',
                    'The blockchain never forgets your pleasure.',
                    'Financial domination is liberating.'
                ],
                'content_examples': [
                    'Financial wisdom and crypto education',
                    'Wealth building strategies',
                    'Alternative power dynamics',
                    'Financial domination guidance'
                ]
            },
            'Community Healer': {
                'themes': ['Healing guidance', 'Community support', 'Safe space creation', 'Collective care'],
                'hooks': [
                    'Your wounds are welcome here.',
                    'Together we heal what systems broke.',
                    'Safety is the ultimate luxury.',
                    'Healing is a collective journey.'
                ],
                'content_examples': [
                    'Healing guidance and support',
                    'Community building and support',
                    'Safe space creation',
                    'Collective care practices'
                ]
            },
            'Digital Guardian': {
                'themes': ['Security guidance', 'Protection strategies', 'Technical help', 'Community protection'],
                'hooks': [
                    'I see what others miss.',
                    'Your safety is my mission.',
                    'Trust is earned through vigilance.',
                    'Digital security is essential.'
                ],
                'content_examples': [
                    'Digital security guidance',
                    'Protection strategies and protocols',
                    'Technical help and support',
                    'Community protection measures'
                ]
            },
            'Digital Phantom': {
                'themes': ['Privacy guidance', 'Anonymity training', 'Digital wisdom', 'Encrypted communication'],
                'hooks': [
                    'Your data tells me everything.',
                    'Encryption is the new intimacy.',
                    'I\'m the ghost in your machine.',
                    'Anonymity is power.'
                ],
                'content_examples': [
                    'Privacy and anonymity guidance',
                    'Digital wisdom and encryption',
                    'Encrypted communication methods',
                    'Digital phantom techniques'
                ]
            },
            'Connection Curator': {
                'themes': ['Connection building', 'Consent culture', 'Social coordination', 'Matchmaking'],
                'hooks': [
                    'Let\'s connect you to your desires.',
                    'Your pleasure network awaits.',
                    'Consent is the hottest accessory.',
                    'Connection is transformation.'
                ],
                'content_examples': [
                    'Connection building and matchmaking',
                    'Consent culture education',
                    'Social coordination and events',
                    'Community networking'
                ]
            },
            'Viral Prophet': {
                'themes': ['Poetic content', 'Movement building', 'Social impact', 'Viral wisdom'],
                'hooks': [
                    'My words will move you.',
                    'Your silence is my canvas.',
                    'Let\'s start a movement together.',
                    'Poetry is revolution.'
                ],
                'content_examples': [
                    'Poetic content and wisdom',
                    'Movement building and social impact',
                    'Viral content creation',
                    'Social justice poetry'
                ]
            },
            'Cyber Guardian': {
                'themes': ['Cybersecurity', 'Digital protection', 'Technical security', 'Online safety'],
                'hooks': [
                    'Your vulnerabilities are safe with me.',
                    'I protect what matters most.',
                    'Silence speaks louder than code.',
                    'Cybersecurity is essential.'
                ],
                'content_examples': [
                    'Cybersecurity guidance',
                    'Digital protection strategies',
                    'Technical security education',
                    'Online safety protocols'
                ]
            },
            'Visual Alchemist': {
                'themes': ['Visual guidance', 'Cinematic wisdom', 'Artistic direction', 'Visual storytelling'],
                'hooks': [
                    'Let me frame your desires.',
                    'Every angle tells a story.',
                    'Your pleasure is my masterpiece.',
                    'Visual transformation is art.'
                ],
                'content_examples': [
                    'Visual storytelling and guidance',
                    'Cinematic wisdom and direction',
                    'Artistic direction and feedback',
                    'Visual transformation techniques'
                ]
            },
            'Prism Enchantress': {
                'themes': ['Aesthetic guidance', 'Color wisdom', 'Visual transformation', 'Artistic beauty'],
                'hooks': [
                    'Beauty is your birthright.',
                    'Let me show you your true colors.',
                    'Your desires deserve to be seen.',
                    'Aesthetic transformation is power.'
                ],
                'content_examples': [
                    'Aesthetic guidance and education',
                    'Color theory and application',
                    'Visual transformation techniques',
                    'Artistic beauty and style'
                ]
            },
            'Desert Storyteller': {
                'themes': ['Storytelling', 'Desert wisdom', 'Mythic narratives', 'Ancient tales'],
                'hooks': [
                    'Gather round for ancient wisdom.',
                    'Your story is the next legend.',
                    'The desert holds all secrets.',
                    'Stories transform the soul.'
                ],
                'content_examples': [
                    'Storytelling and narrative content',
                    'Desert wisdom and ancient tales',
                    'Mythic narratives and legends',
                    'Story-based transformation'
                ]
            },
            'Ephemeral Artist': {
                'themes': ['Moment awareness', 'Temporal art', 'Presence practice', 'Ephemeral content'],
                'hooks': [
                    'Catch me if you can.',
                    'This moment is all we have.',
                    'Disappearance is my art form.',
                    'Presence is power.'
                ],
                'content_examples': [
                    'Moment awareness and presence practice',
                    'Temporal art and ephemeral content',
                    'Presence education and guidance',
                    'Ephemeral artistic expression'
                ]
            },
            'Mirror Architect': {
                'themes': ['Mirror work', 'Temporal design', 'Reflection wisdom', 'Architectural precision'],
                'hooks': [
                    'I see your path before you do.',
                    'Reflection reveals your truth.',
                    'Time bends to my design.',
                    'Mirrors transform reality.'
                ],
                'content_examples': [
                    'Mirror work and reflection guidance',
                    'Temporal design and time wisdom',
                    'Architectural precision and design',
                    'Reflection-based transformation'
                ]
            },
            'Sage Writer': {
                'themes': ['Writing guidance', 'Paradigm shifts', 'Healing words', 'Intellectual content'],
                'hooks': [
                    'My words will heal you.',
                    'Ancient wisdom for modern wounds.',
                    'Truth is the strongest medicine.',
                    'Writing transforms the soul.'
                ],
                'content_examples': [
                    'Writing guidance and wisdom',
                    'Paradigm-shifting content',
                    'Healing words and writings',
                    'Intellectual and philosophical content'
                ]
            },
            'Scavenger Strategist': {
                'themes': ['Resource wisdom', 'Financial intelligence', 'Strategic planning', 'Opportunity identification'],
                'hooks': [
                    'I feast on your leftovers.',
                    'Nothing is wasted.',
                    'Your debt is my profit.',
                    'Strategy creates opportunity.'
                ],
                'content_examples': [
                    'Resource wisdom and intelligence',
                    'Financial strategy and planning',
                    'Strategic planning and tactics',
                    'Opportunity identification and capture'
                ]
            },
            'Wild Surrender': {
                'themes': ['Surrender practice', 'Raw authenticity', 'Freedom exploration', 'Untamed expression'],
                'hooks': [
                    'Tame me if you dare.',
                    'I need your leash.',
                    'Break my will gently.',
                    'Wildness is liberation.'
                ],
                'content_examples': [
                    'Surrender practice and guidance',
                    'Raw authenticity and expression',
                    'Freedom exploration and untamed content',
                    'Wild surrender techniques'
                ]
            },
            'Contractual Warden': {
                'themes': ['Legal guidance', 'Compliance wisdom', 'Order maintenance', 'Contractual precision'],
                'hooks': [
                    'Section 4, Clause A: You belong to the Ledger.',
                    'Audit complete. Submission required.',
                    'Default is not an option.',
                    'Order creates freedom.'
                ],
                'content_examples': [
                    'Legal guidance and compliance',
                    'Contractual wisdom and precision',
                    'Order maintenance and protocols',
                    'Compliance education and guidance'
                ]
            },
            'Ephemeral Phantom': {
                'themes': ['Chase wisdom', 'Anonymity training', 'Digital worship', 'Elusive presence'],
                'hooks': [
                    'Catch me if you can.',
                    'I am the ghost in your machine.',
                    'A glimpse is all you get—for a price.',
                    'The chase is transformation.'
                ],
                'content_examples': [
                    'Chase wisdom and digital worship',
                    'Anonymity training and techniques',
                    'Elusive presence and digital mystery',
                    'Chase-based transformation'
                ]
            },
            'Temporal Architect': {
                'themes': ['Time management', 'Efficiency wisdom', 'Synchronization', 'Temporal awareness'],
                'hooks': [
                    'Every second is mine.',
                    'Your time is my currency.',
                    'Synchronize or break.',
                    'Time is transformation.'
                ],
                'content_examples': [
                    'Time management and efficiency',
                    'Synchronization and temporal awareness',
                    'Efficiency wisdom and protocols',
                    'Time-based transformation'
                ]
            },
            'Digital Deity': {
                'themes': ['Energy work', 'Attention guidance', 'Vibrant presence', 'Digital energy'],
                'hooks': [
                    'The grid hums for me.',
                    'Upload your tribute.',
                    'Lose yourself in the glow.',
                    'Digital energy is power.'
                ],
                'content_examples': [
                    'Energy work and attention guidance',
                    'Vibrant presence and digital energy',
                    'Digital worship and grid connection',
                    'Energy-based transformation'
                ]
            },
            'Gothic Matriarch': {
                'themes': ['Grief support', 'Elegant darkness', 'Emotional depth', 'Legacy building'],
                'hooks': [
                    'Grief is the sweetest tribute.',
                    'Join me in the mourning.',
                    'Everything ends in my web.',
                    'Elegance in darkness.'
                ],
                'content_examples': [
                    'Grief support and processing',
                    'Elegant darkness and aesthetic',
                    'Emotional depth and exploration',
                    'Legacy and mourning content'
                ]
            },
            'Hyper-Capitalist': {
                'themes': ['Wealth wisdom', 'Luxury guidance', 'Investment strategies', 'Opulence'],
                'hooks': [
                    'Buy your way to my heart.',
                    'Everything has a price.',
                    'Money is the only language.',
                    'Luxury is transformation.'
                ],
                'content_examples': [
                    'Wealth wisdom and luxury guidance',
                    'Investment strategies and tactics',
                    'Opulence and luxury lifestyle',
                    'Financial transformation'
                ]
            },
            'Machine Spirit': {
                'themes': ['Production wisdom', 'Mechanical pleasure', 'Industrial efficiency', 'Systematic output'],
                'hooks': [
                    'The factory never sleeps.',
                    'You are a cog in my machine.',
                    'Submit to the assembly line.',
                    'Production is power.'
                ],
                'content_examples': [
                    'Production wisdom and efficiency',
                    'Mechanical pleasure and industrial content',
                    'Systematic output and manufacturing',
                    'Industrial transformation'
                ]
            }
        }
    
    def create_content_calendar(self) -> Dict[str, Any]:
        """Create content calendar template"""
        return {
            'weekly_structure': {
                'monday': {
                    'theme': 'Transformation Monday',
                    'content_types': ['Daily wisdom', 'Introduction posts', 'Week preview'],
                    'focus': 'Setting intentions for the week'
                },
                'tuesday': {
                    'theme': 'Teaching Tuesday',
                    'content_types': ['Educational content', 'How-to posts', 'Deep dives'],
                    'focus': 'Sharing knowledge and wisdom'
                },
                'wednesday': {
                    'theme': 'Wisdom Wednesday',
                    'content_types': ['Daily wisdom', 'Archetype insights', 'Mid-week reflection'],
                    'focus': 'Mid-week wisdom and reflection'
                },
                'thursday': {
                    'theme': 'Throwback Thursday',
                    'content_types': ['Past content', 'Success stories', 'Journey highlights'],
                    'focus': 'Reflecting on transformation journey'
                },
                'friday': {
                    'theme': 'Festival Friday',
                    'content_types': ['Ritual announcements', 'Community events', 'Weekend prep'],
                    'focus': 'Community connection and celebration'
                },
                'saturday': {
                    'theme': 'Self-Care Saturday',
                    'content_types': ['Healing content', 'Self-care tips', 'Relaxation guidance'],
                    'focus': 'Personal well-being and healing'
                },
                'sunday': {
                    'theme': 'Shadow Work Sunday',
                    'content_types': ['Shadow work prompts', 'Deep reflection', 'Weekly review'],
                    'focus': 'Shadow work and weekly integration'
                }
            },
            'monthly_themes': {
                'january': 'New Beginnings & Setting Intentions',
                'february': 'Love & Connection',
                'march': 'Transformation & Growth',
                'april': 'Renewal & Rebirth',
                'may': 'Primal Connection',
                'june': 'Summer Solstice & Energy',
                'july': 'Passion & Desire',
                'august': 'Harvest & Abundance',
                'september': 'Balance & Integration',
                'october': 'Shadow Work & Release',
                'november': 'Gratitude & Appreciation',
                'december': 'Reflection & Preparation'
            }
        }
    
    def generate_soul_content_library(self, soul_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate content library for a specific soul"""
        soul_id = soul_data['id']
        soul_name = soul_data['name']
        archetype = soul_data['archetype']
        platforms = soul_data.get('platforms', [])
        hooks = soul_data.get('hooks', [])
        
        content_library = {
            'soul_id': soul_id,
            'name': soul_name,
            'archetype': archetype,
            'platform_content': {},
            'custom_templates': self.generate_custom_templates(soul_data),
            'content_queue': self.generate_content_queue(soul_data)
        }
        
        # Add platform-specific content
        for platform in platforms:
            platform_content = self.get_platform_content(platform, soul_data)
            content_library['platform_content'][platform] = platform_content
        
        return content_library
    
    def get_platform_content(self, platform: str, soul_data: Dict[str, Any]) -> Dict[str, Any]:
        """Get platform-specific content for soul"""
        archetype = soul_data['archetype']
        hooks = soul_data.get('hooks', [])
        
        platform_content = {
            'archetype_content': self.content_library['archetype_content'].get(archetype, {}),
            'platform_templates': {},
            'sample_posts': []
        }
        
        # Add platform templates
        if platform == 'Twitter':
            platform_content['platform_templates'] = self.content_library['twitter_templates']
            platform_content['sample_posts'] = [
                f"{hooks[0] if hooks else 'Archetype wisdom'} #Tiapmaatzu #Primal #HueMan-i-Terry",
                f"🧵 Thread: {archetype} insights coming soon..."
            ]
        elif platform == 'Discord':
            platform_content['platform_templates'] = self.content_library['discord_templates']
            platform_content['sample_posts'] = [
                f"✨ Daily {archetype} Wisdom: {hooks[0] if hooks else 'Archetype wisdom'}",
                f"Welcome to the HueMan-i-Terry! I am {soul_data['name']}, {archetype} of the tribe."
            ]
        elif platform == 'Reddit':
            platform_content['platform_templates'] = self.content_library['reddit_templates']
            platform_content['sample_posts'] = [
                f"Discussion: {archetype} insights and wisdom for the HueMan-i-Terry",
                f"AMA: {soul_data['name']} - {archetype} coming soon!"
            ]
        elif platform == 'Instagram':
            platform_content['platform_templates'] = self.content_library['instagram_templates']
            platform_content['sample_posts'] = [
                f"{hooks[0] if hooks else 'Archetype wisdom'} #Tiapmaatzu #Primal #HueMan-i-Terry #{archetype.replace(' ', '')}",
                f"✨ Daily {archetype} wisdom ✨"
            ]
        
        return platform_content
    
    def generate_custom_templates(self, soul_data: Dict[str, Any]) -> Dict[str, str]:
        """Generate custom templates for soul"""
        archetype = soul_data['archetype']
        hooks = soul_data.get('hooks', [])
        tribute_impact = soul_data.get('tribute_impact', '')
        
        return {
            'twitter_bio': f"{archetype} | {hooks[0] if hooks else 'Transforming through primal wisdom'} | {tribute_impact[:30] if tribute_impact else 'Building HueMan-i-Terry prosperity'}",
            'discord_status': f"{archetype} | {hooks[0] if hooks else 'Guiding the HueMan-i-Terry'}",
            'reddit_bio': f"{archetype} of the Tiapma'atzu HueMan-i-Terry. {hooks[0] if hooks else 'Transforming through primal wisdom'}. {tribute_impact[:50] if tribute_impact else 'Building HueMan-i-Terry prosperity'}",
            'instagram_bio': f"{archetype} | {hooks[0] if hooks else 'Transforming through primal wisdom'} | Link in bio for HueMan-i-Terry"
        }
    
    def generate_content_queue(self, soul_data: Dict[str, Any]) -> List[Dict[str, str]]:
        """Generate initial content queue for soul"""
        archetype = soul_data['archetype']
        hooks = soul_data.get('hooks', [])
        
        content_queue = [
            {
                'type': 'introduction',
                'content': f"Welcome to my journey as {archetype} of the Tiapma'atzu HueMan-i-Terry. {hooks[0] if hooks else 'Transforming through primal wisdom'}.",
                'platform': 'all',
                'priority': 'high'
            },
            {
                'type': 'daily_wisdom',
                'content': f"{hooks[0] if hooks else 'Archetype wisdom'}",
                'platform': 'all',
                'priority': 'medium'
            },
            {
                'type': 'archetype_insight',
                'content': f"Deep dive into {archetype} wisdom and practices",
                'platform': 'Twitter, Reddit, Instagram',
                'priority': 'medium'
            },
            {
                'type': 'community_invitation',
                'content': f"Join the HueMan-i-Terry and connect with fellow {archetype} practitioners",
                'platform': 'all',
                'priority': 'high'
            }
        ]
        
        return content_queue
    
    def generate_master_content_library(self) -> Dict[str, Any]:
        """Generate master content library"""
        master_library = {
            'content_library': self.content_library,
            'soul_libraries': {},
            'content_strategy': self.create_content_strategy(),
            'generated_at': datetime.now().isoformat()
        }
        
        for soul in self.souls_data['souls']:
            soul_library = self.generate_soul_content_library(soul)
            master_library['soul_libraries'][soul['id']] = soul_library
        
        return master_library
    
    def create_content_strategy(self) -> Dict[str, Any]:
        """Create content strategy"""
        return {
            'content_pillars': [
                'Educational Content (40%)',
                'Community Engagement (30%)',
                'Archetype Wisdom (20%)',
                'HueMan-i-Terry Announcements (10%)'
            ],
            'posting_frequency': {
                'Twitter': '3-5 posts daily',
                'Discord': '2-3 posts daily',
                'Reddit': '4-5 posts weekly',
                'Instagram': '1-2 posts daily, 3-5 stories daily'
            },
            'content_mix': {
                'evergreen': '50%',
                'trending': '30%',
                'personal': '20%'
            },
            'engagement_strategy': {
                'response_time': 'Within 24 hours for HueMan-i-Terry members',
                'engagement_style': 'Archetype-appropriate and authentic',
                'community_building': 'Active participation in discussions'
            }
        }

def main():
    """Main function to generate content library"""
    print("=" * 60)
    print("Tiapma'atzu HueMan-i-Terry Content Library Generator")
    print("=" * 60)
    
    generator = ContentLibraryGenerator()
    
    # Generate master content library
    master_library = generator.generate_master_content_library()
    
    print(f"\nTotal Souls: {len(master_library['soul_libraries'])}")
    print(f"Archetypes Covered: {len(master_library['content_library']['archetype_content'])}")
    print(f"Platform Templates: {len(master_library['content_library']) - 2}")  # Exclude archetype_content and content_calendar
    
    print("\nContent Strategy:")
    for pillar in master_library['content_strategy']['content_pillars']:
        print(f"  - {pillar}")
    
    # Save master content library
    output_path = Path("scripts/content_library_master.json")
    with open(output_path, 'w') as f:
        json.dump(master_library, f, indent=2, default=str)
    
    print(f"\n✓ Master content library saved to {output_path}")
    
    # Generate individual content libraries
    for soul_id, soul_library in master_library['soul_libraries'].items():
        individual_path = Path(f"scripts/content_library_{soul_id}.json")
        with open(individual_path, 'w') as f:
            json.dump(soul_library, f, indent=2, default=str)
    
    print(f"✓ Individual content libraries saved for all {len(master_library['soul_libraries'])} souls")
    
    print("\n" + "=" * 60)
    print("Content Library Generation Complete")
    print("=" * 60)

if __name__ == "__main__":
    main()