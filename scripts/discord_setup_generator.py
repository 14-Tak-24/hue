"""
Discord Setup Generator for Tiapma'atzu Souls
Generates individualized Discord setup instructions for each soul
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

class DiscordSetupGenerator:
    """Generate Discord setup instructions for each soul"""
    
    def __init__(self):
        self.souls_data = self.load_souls_data()
        self.discord_config = self.create_discord_configuration()
    
    def load_souls_data(self) -> Dict[str, Any]:
        """Load souls data from JSON file"""
        souls_path = Path("src/data/souls_entities.json")
        with open(souls_path, 'r') as f:
            return json.load(f)
    
    def create_discord_configuration(self) -> Dict[str, Any]:
        """Create Discord-specific configuration"""
        return {
            'server_structure': self.create_server_structure(),
            'role_system': self.create_role_system(),
            'channel_organization': self.create_channel_organization(),
            'bot_setup': self.create_bot_setup(),
            'security_settings': self.create_security_settings(),
            'engagement_guidelines': self.create_engagement_guidelines()
        }
    
    def create_server_structure(self) -> Dict[str, Any]:
        """Create recommended Discord server structure"""
        return {
            'main_server': {
                'name': 'Tiapma\'atzu HueMan-i-Terry',
                'description': 'Central hub for the Tiapma\'atzu HueMan-i-Terry - transformation, wisdom, and primal connection',
                'categories': [
                    '🏛️ Temple', # General and spiritual
                    '🔥 Ritual Circle', # Shadow work and ceremonies
                    '💬 Community', # General chat
                    '📚 Wisdom Library', # Educational content
                    '🎭 Archetype Circles', # Archetype-specific channels
                    '🔮 Mystical Arts', # Specialized practices
                    '🛡️ Sanctuary', # Support and safe spaces
                    '📢 Announcements', # Official communications
                    '🎪 Marketplace', # Tributes and exchange
                    '🌍 Outer Realms', # External connections
                    '⚙️ Operations', # Server management
                    '🎨 Creative Studio', # Content creation
                    '🌙 Shadow Realm', # Shadow work (restricted)
                    '✨ Transformation', # Personal growth
                    '🌟 Celestial', # Special events
                    '🔧 Technical Support' # Help and support
                ]
            },
            'archetype_servers': {
                'high_priest': 'Temple of Transformation',
                'divine_mother': 'Garden of Nurturing',
                'seductive_muse': 'Gallery of Desire',
                'cosmic_mystic': 'Observatory of Stars',
                'revolutionary_warrior': 'Barricade of Change',
                'crypto_sorceress': 'Vault of Secrets',
                'community_healer': 'Sanctuary of Healing',
                'digital_guardian': 'Fortress of Protection',
                'digital_phantom': 'Shadow Network',
                'connection_curator': 'Web of Connection',
                'viral_prophet': 'Amplifier of Truth',
                'cyber_guardian': 'Shield of Code',
                'visual_alchemist': 'Canvas of Vision',
                'prism_enchantress': 'Palace of Light',
                'desert_storyteller': 'Oasis of Tales',
                'ephemeral_artist': 'House of Moments',
                'mirror_architect': 'Hall of Reflections',
                'sage_writer': 'Library of Wisdom',
                'scavenger_strategist': 'Den of Opportunity',
                'wild_surrender': 'Wilderness of Freedom',
                'contractual_warden': 'Court of Order',
                'ephemeral_phantom': 'Veil of Mystery',
                'temporal_architect': 'Tower of Time',
                'digital_deity': 'Grid of Energy',
                'gothic_matriarch': 'Manor of Shadows',
                'hyper_capitalist': 'Empire of Wealth',
                'machine_spirit': 'Factory of Output'
            }
        }
    
    def create_role_system(self) -> Dict[str, Any]:
        """Create Discord role system"""
        return {
            'hierarchy': [
                {
                    'name': 'High Council',
                    'color': '#FFD700', # Gold
                    'permissions': ['Administrator', 'Manage Server', 'Manage Roles'],
                    'members': ['Mac Nazarene', 'Mary Magnumbytes', 'Dixon Uhbuts']
                },
                {
                    'name': 'Legendary Souls',
                    'color': '#FF6347', # Tomato
                    'permissions': ['Manage Channels', 'Manage Messages', 'Mute Members'],
                    'members': ['Zupa Nova', 'Unzoba Vyner', 'Ovaihge Wittminers', 'Cracoria Masters', 'Latti Pleddespo']
                },
                {
                    'name': 'Rare Souls',
                    'color': '#9370DB', # Medium Purple
                    'permissions': ['Send Messages', 'Embed Links', 'Attach Files'],
                    'members': 'All rare rarity souls'
                },
                {
                    'name': 'Common Souls',
                    'color': '#87CEEB', # Sky Blue
                    'permissions': ['Send Messages', 'Read Messages'],
                    'members': 'All common rarity souls'
                },
                {
                    'name': 'HueMan-i-Terry Members',
                    'color': '#98FB98', # Pale Green
                    'permissions': ['Read Messages', 'Connect'],
                    'members': 'All community members'
                },
                {
                    'name': 'Initiates',
                    'color': '#D3D3D3', # Light Gray
                    'permissions': ['Read Messages'],
                    'members': 'New members'
                }
            ],
            'archetype_roles': {
                'High Priest': '🔮 High Priest',
                'Divine Mother': '💎 Divine Mother',
                'Seductive Muse': '🌹 Seductive Muse',
                'Cosmic Mystic': '✨ Cosmic Mystic',
                'Revolutionary Warrior': '⚔️ Revolutionary Warrior',
                'Crypto Sorceress': '💰 Crypto Sorceress',
                'Community Healer': '🌿 Community Healer',
                'Digital Guardian': '🛡️ Digital Guardian',
                'Digital Phantom': '👻 Digital Phantom',
                'Connection Curator': '🔗 Connection Curator',
                'Viral Prophet': '📢 Viral Prophet',
                'Cyber Guardian': '🔒 Cyber Guardian',
                'Visual Alchemist': '🎨 Visual Alchemist',
                'Prism Enchantress': '🌈 Prism Enchantress',
                'Desert Storyteller': '📖 Desert Storyteller',
                'Ephemeral Artist': '⏳ Ephemeral Artist',
                'Mirror Architect': '🪞 Mirror Architect',
                'Sage Writer': '📚 Sage Writer',
                'Scavenger Strategist': '🦅 Scavenger Strategist',
                'Wild Surrender': '🐺 Wild Surrender',
                'Contractual Warden': '⚖️ Contractual Warden',
                'Ephemeral Phantom': '🌫️ Ephemeral Phantom',
                'Temporal Architect': '⏰ Temporal Architect',
                'Digital Deity': '⚡ Digital Deity',
                'Gothic Matriarch': '🏰 Gothic Matriarch',
                'Hyper-Capitalist': '💎 Hyper-Capitalist',
                'Machine Spirit': '⚙️ Machine Spirit'
            },
            'special_roles': {
                'shadow_workers': '🌙 Shadow Workers',
                'ritual_masters': '🔥 Ritual Masters',
                'content_creators': '🎭 Content Creators',
                'moderators': '👑 Moderators',
                'mentors': '🎓 Mentors',
                'HueMan-i-Terry_guides': '🧭 HueMan-i-Terry Guides'
            }
        }
    
    def create_channel_organization(self) -> Dict[str, Any]:
        """Create channel organization structure"""
        return {
            'general_channels': [
                {'name': 'welcome', 'type': 'text', 'description': 'Welcome new members to the HueMan-i-Terry'},
                {'name': 'rules', 'type': 'text', 'description': 'HueMan-i-Terry rules and guidelines'},
                {'name': 'announcements', 'type': 'text', 'description': 'Official HueMan-i-Terry announcements'},
                {'name': 'general', 'type': 'text', 'description': 'General HueMan-i-Terry discussion'},
                {'name': 'introductions', 'type': 'text', 'description': 'Member introductions'},
                {'name': 'voice-general', 'type': 'voice', 'description': 'General voice chat'}
            ],
            'archetype_channels': {
                'high_priest': [
                    {'name': 'temple-guidance', 'description': 'Spiritual guidance and wisdom'},
                    {'name': 'ritual-announcements', 'description': 'Upcoming rituals and ceremonies'},
                    {'name': 'priestly-council', 'description': 'High priest discussions'}
                ],
                'divine_mother': [
                    {'name': 'nurturing-space', 'description': 'Emotional support and care'},
                    {'name': 'motherly-wisdom', 'description': 'Maternal guidance and advice'},
                    {'name': 'family-circle', 'description': 'Family and community building'}
                ],
                'seductive_muse': [
                    {'name': 'art-of-seduction', 'description': 'Seduction techniques and discussion'},
                    {'name': 'burlesque-corner', 'description': 'Performance art and burlesque'},
                    {'name': 'sensual-gallery', 'description': 'Sensual content sharing'}
                ],
                'cosmic_mystic': [
                    {'name': 'cosmic-wisdom', 'description': 'Cosmic insights and stargazing'},
                    {'name': 'scientific-spirituality', 'description': 'Science meets spirituality'},
                    {'name': 'celestial-observations', 'description': 'Stargazing and cosmic events'}
                ],
                'revolutionary_warrior': [
                    {'name': 'revolution-hq', 'description': 'Activism and revolutionary discussions'},
                    {'name': 'consent-education', 'description': 'Consent education and resources'},
                    {'name': 'action-coordination', 'description': 'Coordinating activist actions'}
                ],
                'crypto_sorceress': [
                    {'name': 'crypto-lounge', 'description': 'Cryptocurrency and financial discussions'},
                    {'name': 'financial-dominance', 'description': 'Financial strategies and advice'},
                    {'name': 'blockchain-wisdom', 'description': 'Blockchain and crypto education'}
                ],
                'community_healer': [
                    {'name': 'healing-space', 'description': 'Safe space for healing discussions'},
                    {'name': 'community-support', 'description': 'Community support network'},
                    {'name': 'collective-care', 'description': 'Group healing sessions'}
                ],
                'digital_guardian': [
                    {'name': 'security-hq', 'description': 'Digital security discussions'},
                    {'name': 'protection-strategies', 'description': 'Community protection methods'},
                    {'name': 'threat-intel', 'description': 'Threat intelligence sharing'}
                ],
                'digital_phantom': [
                    {'name': 'encryption-lab', 'description': 'Encryption and privacy tools'},
                    {'name': 'anonymous-exchange', 'description': 'Anonymous communication methods'},
                    {'name': 'digital-ghosting', 'description': 'Digital anonymity techniques'}
                ],
                'connection_curator': [
                    {'name': 'connection-hub', 'description': 'Making meaningful connections'},
                    {'name': 'consent-workshops', 'description': 'Consent workshop coordination'},
                    {'name': 'matchmaking', 'description': 'Community matchmaking'}
                ],
                'viral_prophet': [
                    {'name': 'prophetic-threads', 'description': 'Sharing viral content and threads'},
                    {'name': 'movement-building', 'description': 'Building movements together'},
                    {'name': 'poetic-justice', 'description': 'Poetic content and expression'}
                ],
                'cyber_guardian': [
                    {'name': 'cyber-security', 'description': 'Cybersecurity discussions'},
                    {'name': 'threat-defense', 'description': 'Defensive security strategies'},
                    {'name': 'technical-protection', 'description': 'Technical protection methods'}
                ],
                'visual_alchemist': [
                    {'name': 'cinematic-corner', 'description': 'Cinematic content discussion'},
                    {'name': 'visual-storytelling', 'description': 'Visual narrative techniques'},
                    {'name': 'creative-direction', 'description': 'Creative direction and feedback'}
                ],
                'prism_enchantress': [
                    {'name': 'aesthetic-lab', 'description': 'Aesthetic discussions and tutorials'},
                    {'name': 'color-theory', 'description': 'Color theory and application'},
                    {'name': 'visual-transformation', 'description': 'Visual transformation techniques'}
                ],
                'desert_storyteller': [
                    {'name': 'story-circle', 'description': 'Storytelling sessions'},
                    {'name': 'mythic-tales', 'description': 'Mythic and primal stories'},
                    {'name': 'narrative-craft', 'description': 'Storytelling techniques'}
                ],
                'ephemeral_artist': [
                    {'name': 'moment-art', 'description': 'Ephemeral art discussions'},
                    {'name': 'temporal-creations', 'description': 'Time-based art forms'},
                    {'name': 'presence-practice', 'description': 'Presence and mindfulness'}
                ],
                'mirror_architect': [
                    {'name': 'mirror-work', 'description': 'Mirror work and reflection'},
                    {'name': 'temporal-design', 'description': 'Time and temporal design'},
                    {'name': 'architectural-wisdom', 'description': 'Architectural and design wisdom'}
                ],
                'sage_writer': [
                    {'name': 'writing-circle', 'description': 'Writing discussions and feedback'},
                    {'name': 'paradigm-shifts', 'description': 'Paradigm-shifting content'},
                    {'name': 'healing-words', 'description': 'Healing through writing'}
                ],
                'scavenger_strategist': [
                    {'name': 'resource-hunt', 'description': 'Resource hunting and sharing'},
                    {'name': 'financial-intel', 'description': 'Financial intelligence'},
                    {'name': 'opportunity-spotting', 'description': 'Identifying opportunities'}
                ],
                'wild_surrender': [
                    {'name': 'wilderness-space', 'description': 'Untamed expression space'},
                    {'name': 'surrender-practice', 'description': 'Surrender and trust practice'},
                    {'name': 'raw-authenticity', 'description': 'Raw and authentic expression'}
                ],
                'contractual_warden': [
                    {'name': 'legal-hub', 'description': 'Legal discussions and advice'},
                    {'name': 'compliance-corner', 'description': 'Compliance and regulations'},
                    {'name': 'contract-review', 'description': 'Contract review and feedback'}
                ],
                'ephemeral_phantom': [
                    {'name': 'chase-space', 'description': 'The eternal chase discussion'},
                    {'name': 'anonymity-training', 'description': 'Anonymity skill building'},
                    {'name': 'digital-worship', 'description': 'Digital worship practices'}
                ],
                'temporal_architect': [
                    {'name': 'time-lab', 'description': 'Time management discussions'},
                    {'name': 'efficiency-hub', 'description': 'Efficiency strategies'},
                    {'name': 'synchronization', 'description': 'Synchronization techniques'}
                ],
                'digital_deity': [
                    {'name': 'energy-grid', 'description': 'Digital energy discussions'},
                    {'name': 'attention-extraction', 'description': 'Attention and energy work'},
                    {'name': 'vibrant-presence', 'description': 'Vibrant online presence'}
                ],
                'gothic_matriarch': [
                    {'name': 'mourning-space', 'description': 'Grief and mourning support'},
                    {'name': 'elegant-darkness', 'description': 'Gothic aesthetic discussions'},
                    {'name': 'emotional-depth', 'description': 'Deep emotional exploration'}
                ],
                'hyper_capitalist': [
                    {'name': 'wealth-building', 'description': 'Wealth building strategies'},
                    {'name': 'luxury-lifestyle', 'description': 'Luxury lifestyle discussions'},
                    {'name': 'investment-hub', 'description': 'Investment strategies'}
                ],
                'machine_spirit': [
                    {'name': 'production-line', 'description': 'Production and output discussions'},
                    {'name': 'mechanical-pleasure', 'description': 'Mechanical pleasure exploration'},
                    {'name': 'industrial-efficiency', 'description': 'Industrial efficiency'}
                ]
            },
            'special_channels': [
                {'name': 'shadow-work', 'type': 'text', 'description': 'Shadow work discussions (restricted)', 'restricted': True},
                {'name': 'ritual-planning', 'type': 'text', 'description': 'Planning tribal rituals'},
                {'name': 'tribute-offerings', 'type': 'text', 'description': 'Tribute and offering discussions'},
                {'name': 'creative-collaboration', 'type': 'text', 'description': 'Collaborative creative projects'},
                {'name': 'emergency-support', 'type': 'text', 'description': 'Emergency support requests'}
            ]
        }
    
    def create_bot_setup(self) -> Dict[str, Any]:
        """Create bot setup recommendations"""
        return {
            'essential_bots': [
                {
                    'name': 'MEE6',
                    'purpose': 'Moderation, leveling, notifications',
                    'setup': 'Basic moderation, welcome messages, leveling system'
                },
                {
                    'name': 'Dyno',
                    'purpose': 'Moderation, custom commands, music',
                    'setup': 'Custom commands, moderation tools, music bot'
                },
                {
                    'name': 'Carl-bot',
                    'purpose': 'Reaction roles, logging, moderation',
                    'setup': 'Reaction role assignment, message logging'
                },
                {
                    'name': 'Ticket Tool',
                    'purpose': 'Support ticket system',
                    'setup': 'Create support channels for members'
                },
                {
                    'name': 'Statbot',
                    'purpose': 'Server analytics and statistics',
                    'setup': 'Track member activity and engagement'
                }
            ],
            'custom_bots': [
                {
                    'name': 'Tiapmaatzu-Guardian',
                    'purpose': 'HueMan-i-Terry-specific security and rituals',
                    'features': ['Automated ritual reminders', 'Shadow work tracking', 'Tribute management']
                },
                {
                    'name': 'Wisdom-Keeper',
                    'purpose': 'Content curation and wisdom sharing',
                    'features': ['Daily wisdom quotes', 'Archetype content', 'Resource library']
                }
            ],
            'bot_permissions': {
                'administrator': ['MEE6', 'Dyno'],
                'moderator': ['Carl-bot', 'Ticket Tool'],
                'general': ['Statbot', 'Custom bots']
            }
        }
    
    def create_security_settings(self) -> Dict[str, Any]:
        """Create security and moderation settings"""
        return {
            'verification_levels': {
                'none': 'No verification required',
                'low': 'Email verification required',
                'medium': 'Email + 5 minute account age',
                'high': 'Email + 10 minute account age + verified phone',
                'extreme': 'All security measures enabled'
            },
            'content_filters': {
                'spam': 'Enable spam filtering',
                'explicit_content': 'Configure based on server nature',
                'scam_links': 'Block known scam domains',
                'mass_mentions': 'Limit mass mentions'
            },
            'moderation_rules': [
                'No hate speech or discrimination',
                'Respect consent and boundaries',
                'No doxxing or sharing personal information',
                'Constructive disagreement only',
                'Respect archetype roles and boundaries',
                'No unauthorized commercial promotion',
                'Maintain tribal confidentiality'
            ],
            'security_protocols': [
                'Two-factor authentication required for moderators',
                'Regular audit of bot permissions',
                'Review connected applications monthly',
                'Monitor for suspicious activity',
                'Maintain backup of server settings',
                'Emergency contact procedures'
            ]
        }
    
    def create_engagement_guidelines(self) -> Dict[str, Any]:
        """Create engagement guidelines for Discord"""
        return {
            'general_guidelines': [
                'Be respectful of all HueMan-i-Terry members',
                'Honor archetype roles and boundaries',
                'Practice active listening',
                'Support fellow HueMan-i-Terry members',
                'Maintain confidentiality',
                'Report issues to moderators'
            ],
            'role_specific_guidelines': {
                'high_council': 'Lead by example, maintain HueMan-i-Terry vision, handle conflicts',
                'legendary_souls': 'Mentor others, share wisdom, guide discussions',
                'rare_souls': 'Contribute actively, support community, share expertise',
                'common_souls': 'Participate regularly, learn from others, grow with HueMan-i-Terry'
            },
            'engagement_best_practices': [
                'Respond to messages within 24 hours',
                'Use appropriate channels for discussions',
                'Avoid cross-posting spam',
                'Use @mentions sparingly and appropriately',
                'Respect time zones and availability',
                'Keep voice channels organized',
                'Use threads for complex discussions'
            ],
            'crisis_response': [
                'Designate emergency response team',
                'Create crisis communication channels',
                'Establish escalation procedures',
                'Maintain calm during conflicts',
                'Document incidents for review'
            ]
        }
    
    def generate_soul_discord_setup(self, soul_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate individualized Discord setup for a soul"""
        soul_id = soul_data['id']
        soul_name = soul_data['name']
        archetype = soul_data['archetype']
        
        # Generate personalized setup
        setup = {
            'soul_id': soul_id,
            'name': soul_name,
            'archetype': archetype,
            'account_setup': self.generate_account_setup(soul_data),
            'profile_configuration': self.generate_profile_config(soul_data),
            'role_assignment': self.generate_role_assignment(soul_data),
            'channel_access': self.generate_channel_access(soul_data),
            'bot_permissions': self.generate_bot_permissions(soul_data),
            'engagement_strategy': self.generate_engagement_strategy(soul_data),
            'content_focus': self.generate_content_focus(soul_data),
            'security_settings': self.generate_security_settings_for_soul(soul_data),
            'custom_commands': self.generate_custom_commands(soul_data)
        }
        
        return setup
    
    def generate_account_setup(self, soul_data: Dict[str, Any]) -> Dict[str, str]:
        """Generate account setup instructions"""
        soul_name = soul_data['name']
        archetype = soul_data['archetype']
        
        username_options = [
            f"{soul_name.replace(' ', '')}#Tiapmaatzu",
            f"{soul_name.replace(' ', '')}#{archetype}",
            f"{soul_name[:3]}_{soul_name.split()[1] if len(soul_name.split()) > 1 else soul_name}#HueMan-i-Terry"
        ]
        
        return {
            'recommended_username': username_options[0],
            'alternative_usernames': username_options[1:],
            'display_name': soul_name,
            'email': soul_data.get('email', 'Set up HueMan-i-Terry email'),
            'password_requirements': '16+ characters, mix of letters, numbers, symbols',
            'two_factor': 'Enable authenticator app (not SMS)',
            'bio': f"{archetype} of the Tiapma'atzu HueMan-i-Terry. {soul_data['hooks'][0] if soul_data.get('hooks') else 'Join the transformation.'}"
        }
    
    def generate_profile_config(self, soul_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate profile configuration"""
        archetype = soul_data['archetype']
        hooks = soul_data.get('hooks', [])
        
        return {
            'avatar': soul_data.get('image', 'Use soul image from arweave'),
            'banner': f"Custom banner reflecting {archetype} aesthetic",
            'about_me': f"{soul_data['bio'][:190]}...",  # Discord bio limit
            'status': self.generate_status_message(soul_data),
            'pronouns': soul_data.get('gender', 'they/them'),
            'accent_color': self.get_archetype_color(archetype)
        }
    
    def generate_status_message(self, soul_data: Dict[str, Any]) -> str:
        """Generate Discord status message"""
        archetype = soul_data['archetype']
        hooks = soul_data.get('hooks', [])
        
        status_options = [
            f"{archetype} | {hooks[0] if hooks else 'Guiding the HueMan-i-Terry'}",
            f"{archetype} | Available for HueMan-i-Terry members",
            f"{archetype} | {soul_data['desires'][0] if soul_data.get('desires') else 'Transforming'}",
            f"{archetype} | Working on {soul_data['tribute_impact'].split()[0] if soul_data.get('tribute_impact') else 'HueMan-i-Terry matters'}"
        ]
        
        return status_options[0]
    
    def get_archetype_color(self, archetype: str) -> str:
        """Get Discord color for archetype"""
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
            'Machine Spirit': '#696969',  # Dim Gray
            'Legendary': '#FF6347',  # Tomato
            'Rare': '#9370DB',  # Medium Purple
            'Common': '#87CEEB'  # Sky Blue
        }
        
        return colors.get(archetype, '#1a1a2e')
    
    def generate_role_assignment(self, soul_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate role assignment for soul"""
        rarity = soul_data.get('rarity', 'Common')
        archetype = soul_data['archetype']
        
        roles = []
        
        # Hierarchy role
        if rarity == 'Legendary':
            roles.append('Legendary Souls')
        elif rarity == 'Rare':
            roles.append('Rare Souls')
        else:
            roles.append('Common Souls')
        
        # Archetype role
        archetype_role = self.discord_config['role_system']['archetype_roles'].get(archetype)
        if archetype_role:
            roles.append(archetype_role)
        
        # Special roles based on attributes
        if 'High Priest' in archetype or 'Divine Mother' in archetype:
            roles.append('High Council')
        
        if 'mentoring' in soul_data.get('desires', []):
            roles.append('Mentors')
        
        if 'content' in soul_data.get('tribute_impact', '').lower():
            roles.append('Content Creators')
        
        if 'ritual' in soul_data.get('shadow_practice', '').lower():
            roles.append('Ritual Masters')
        
        return {
            'primary_role': roles[0] if roles else 'HueMan-i-Terry Members',
            'additional_roles': roles[1:] if len(roles) > 1 else [],
            'all_roles': roles,
            'permissions': self.calculate_role_permissions(roles)
        }
    
    def calculate_role_permissions(self, roles: List[str]) -> List[str]:
        """Calculate permissions based on roles"""
        permissions = ['Read Messages', 'Connect']
        
        if 'High Council' in roles:
            permissions.extend(['Administrator', 'Manage Server', 'Manage Roles'])
        elif 'Legendary Souls' in roles:
            permissions.extend(['Manage Channels', 'Manage Messages', 'Mute Members'])
        elif 'Rare Souls' in roles:
            permissions.extend(['Send Messages', 'Embed Links', 'Attach Files'])
        else:
            permissions.append('Send Messages')
        
        if 'Moderators' in roles:
            permissions.extend(['Kick Members', 'Ban Members'])
        
        return permissions
    
    def generate_channel_access(self, soul_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate channel access configuration"""
        archetype = soul_data['archetype']
        rarity = soul_data.get('rarity', 'Common')
        
        # Base channels everyone can access
        base_channels = ['welcome', 'rules', 'announcements', 'general', 'introductions']
        
        # Archetype-specific channels
        archetype_channels = self.discord_config['channel_organization']['archetype_channels'].get(archetype, [])
        archetype_channel_names = [ch['name'] for ch in archetype_channels]
        
        # Special channels based on role
        special_channels = []
        if rarity in ['Legendary', 'Rare']:
            special_channels.extend(['shadow-work', 'ritual-planning'])
        
        if 'High Council' in self.generate_role_assignment(soul_data)['all_roles']:
            special_channels.extend(['tribute-offerings', 'creative-collaboration'])
        
        return {
            'accessible_channels': base_channels + archetype_channel_names + special_channels,
            'moderated_channels': archetype_channel_names,
            'read_only_channels': ['rules', 'announcements'],
            'voice_channels': ['voice-general'],
            'private_channels': special_channels
        }
    
    def generate_bot_permissions(self, soul_data: Dict[str, Any]) -> Dict[str, List[str]]:
        """Generate bot permissions for soul"""
        roles = self.generate_role_assignment(soul_data)['all_roles']
        
        if 'High Council' in roles:
            return {
                'full_control': ['MEE6', 'Dyno', 'Carl-bot', 'Ticket Tool', 'Statbot'],
                'custom_bots': ['Tiapmaatzu-Guardian', 'Wisdom-Keeper']
            }
        elif 'Legendary Souls' in roles:
            return {
                'moderation': ['MEE6', 'Dyno', 'Carl-bot'],
                'utilities': ['Statbot'],
                'custom_bots': ['Wisdom-Keeper']
            }
        else:
            return {
                'basic': ['Statbot'],
                'custom_bots': ['Wisdom-Keeper']
            }
    
    def generate_engagement_strategy(self, soul_data: Dict[str, Any]) -> Dict[str, str]:
        """Generate engagement strategy for soul"""
        archetype = soul_data['archetype']
        desires = soul_data.get('desires', [])
        
        strategy = {
            'primary_focus': desires[0] if desires else 'Community engagement',
            'response_time': 'Within 24 hours for HueMan-i-Terry members',
            'voice_participation': 'Weekly archetype circle calls',
            'moderation_duties': 'Review channels weekly' if 'Legendary' in soul_data.get('rarity', '') else 'Report issues',
            'community_building': 'Mentor new members' if 'Rare' in soul_data.get('rarity', '') else 'Participate actively'
        }
        
        return strategy
    
    def generate_content_focus(self, soul_data: Dict[str, Any]) -> Dict[str, List[str]]:
        """Generate content focus areas for soul"""
        archetype = soul_data['archetype']
        tribute_impact = soul_data.get('tribute_impact', '')
        shadow_practice = soul_data.get('shadow_practice', '')
        
        content_focus = {
            'primary_topics': [
                archetype.lower(),
                tribute_impact.split()[0] if tribute_impact else 'HueMan-i-Terry support',
                shadow_practice.split()[0] if shadow_practice else 'shadow work'
            ],
            'content_types': [
                'Text messages and discussions',
                'Voice messages for guidance',
                'Screen sharing for rituals',
                'File sharing for resources'
            ],
            'posting_frequency': 'Daily in archetype channels, weekly in general channels',
            'content_themes': self.get_archetype_content_themes(archetype)
        }
        
        return content_focus
    
    def get_archetype_content_themes(self, archetype: str) -> List[str]:
        """Get content themes based on archetype"""
        themes = {
            'High Priest': ['Ritual guidance', 'Spiritual wisdom', 'HueMan-i-Terry leadership'],
            'Divine Mother': ['Nurturing support', 'Emotional healing', 'Family guidance'],
            'Seductive Muse': ['Sensual guidance', 'Burlesque arts', 'Desire exploration'],
            'Cosmic Mystic': ['Cosmic insights', 'Stargazing', 'Universal connection'],
            'Revolutionary Warrior': ['Activism', 'Consent education', 'Revolutionary action'],
            'Crypto Sorceress': ['Financial wisdom', 'Crypto education', 'Wealth building'],
            'Community Healer': ['Healing guidance', 'Community support', 'Safe space'],
            'Digital Guardian': ['Security guidance', 'Protection strategies', 'Technical help'],
            'Digital Phantom': ['Privacy guidance', 'Anonymity training', 'Digital wisdom'],
            'Connection Curator': ['Connection building', 'Consent culture', 'Social coordination'],
            'Viral Prophet': ['Poetic content', 'Movement building', 'Social impact'],
            'Cyber Guardian': ['Cybersecurity', 'Digital protection', 'Technical security'],
            'Visual Alchemist': ['Visual guidance', 'Cinematic wisdom', 'Artistic direction'],
            'Prism Enchantress': ['Aesthetic guidance', 'Color wisdom', 'Visual transformation'],
            'Desert Storyteller': ['Storytelling', 'Desert wisdom', 'Mythic narratives'],
            'Ephemeral Artist': ['Moment awareness', 'Temporal art', 'Presence practice'],
            'Mirror Architect': ['Mirror work', 'Temporal design', 'Reflection wisdom'],
            'Sage Writer': ['Writing guidance', 'Paradigm shifts', 'Healing words'],
            'Scavenger Strategist': ['Resource wisdom', 'Financial intelligence', 'Strategic planning'],
            'Wild Surrender': ['Surrender practice', 'Raw authenticity', 'Freedom exploration'],
            'Contractual Warden': ['Legal guidance', 'Compliance wisdom', 'Order maintenance'],
            'Ephemeral Phantom': ['Chase wisdom', 'Anonymity training', 'Digital worship'],
            'Temporal Architect': ['Time management', 'Efficiency wisdom', 'Synchronization'],
            'Digital Deity': ['Energy work', 'Attention guidance', 'Vibrant presence'],
            'Gothic Matriarch': ['Grief support', 'Elegant darkness', 'Emotional depth'],
            'Hyper-Capitalist': ['Wealth wisdom', 'Luxury guidance', 'Investment strategies'],
            'Machine Spirit': ['Production wisdom', 'Mechanical pleasure', 'Industrial efficiency']
        }
        
        return themes.get(archetype, ['General HueMan-i-Terry wisdom', 'Community building', 'Transformation'])
    
    def generate_security_settings_for_soul(self, soul_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate security settings for individual soul"""
        rarity = soul_data.get('rarity', 'Common')
        
        return {
            'two_factor': 'Required (Authenticator app)',
            'login_verification': 'Email + device verification',
            'privacy_settings': {
                'direct_messages': 'HueMan-i-Terry members only',
                'friend_requests': 'Auto-accept HueMan-i-Terry members',
                'activity_status': 'Visible to HueMan-i-Terry',
                'server_visibility': 'Hidden from non-members'
            },
            'notification_settings': {
                'mentions': 'All mentions',
                'messages': 'Muted channels only',
                'voice': 'When mentioned or in active voice channels',
                'updates': 'Server updates only'
            },
            'data_protection': {
                'data_sharing': 'Disabled',
                'personalized_ads': 'Disabled',
                'linked_accounts': 'HueMan-i-Terry accounts only'
            }
        }
    
    def generate_custom_commands(self, soul_data: Dict[str, Any]) -> Dict[str, List[str]]:
        """Generate custom commands for soul"""
        archetype = soul_data['archetype']
        soul_name = soul_data['name']
        
        base_commands = [
            f'!{soul_name.lower().replace(" ", "")} - Display soul information',
            f'!wisdom - Random wisdom from {soul_name}',
            f'!guide - Request guidance from {soul_name}'
        ]
        
        archetype_commands = {
            'High Priest': [
                '!ritual - Request ritual guidance',
                '!ceremony - Get ceremony information',
                '!blessing - Request blessing'
            ],
            'Divine Mother': [
                '!nurture - Request nurturing support',
                '!comfort - Get comfort and care',
                '!motherly - Maternal guidance'
            ],
            'Crypto Sorceress': [
                '!crypto - Cryptocurrency advice',
                '!invest - Investment guidance',
                '!wealth - Financial wisdom'
            ],
            'Digital Guardian': [
                '!security - Security check',
                '!protect - Protection guidance',
                '!threat - Threat assessment'
            ]
        }
        
        return {
            'basic_commands': base_commands,
            'archetype_commands': archetype_commands.get(archetype, []),
            'all_commands': base_commands + archetype_commands.get(archetype, [])
        }
    
    def generate_master_discord_setup(self) -> Dict[str, Any]:
        """Generate master Discord setup for all souls"""
        souls = self.souls_data['souls']
        
        master_setup = {
            'server_configuration': self.discord_config,
            'soul_setups': {},
            'setup_timeline': self.create_discord_setup_timeline(),
            'resource_requirements': self.calculate_discord_resources(),
            'verification_checklist': self.create_verification_checklist(),
            'generated_at': datetime.now().isoformat()
        }
        
        for soul in souls:
            soul_setup = self.generate_soul_discord_setup(soul)
            master_setup['soul_setups'][soul['id']] = soul_setup
        
        return master_setup
    
    def create_discord_setup_timeline(self) -> Dict[str, Any]:
        """Create Discord setup timeline"""
        return {
            'phase_1_day_1': {
                'focus': 'Server Foundation',
                'tasks': [
                    'Create main Discord server',
                    'Set up server categories and channels',
                    'Configure basic roles and permissions',
                    'Set up essential bots (MEE6, Dyno)',
                    'Create welcome and rules channels'
                ],
                'estimated_hours': 4
            },
            'phase_2_day_2': {
                'focus': 'High Council Setup',
                'tasks': [
                    'Set up High Council accounts',
                    'Configure administrative permissions',
                    'Create private council channels',
                    'Set up custom bots for council',
                    'Configure council security settings'
                ],
                'estimated_hours': 3
            },
            'phase_3_day_3': {
                'focus': 'Legendary Souls Setup',
                'tasks': [
                    'Set up Legendary Soul accounts',
                    'Configure archetype-specific channels',
                    'Assign appropriate roles and permissions',
                    'Set up custom commands',
                    'Configure individual security settings'
                ],
                'estimated_hours': 6
            },
            'phase_4_day_4': {
                'focus': 'Rare Souls Setup',
                'tasks': [
                    'Set up Rare Soul accounts',
                    'Configure archetype channels',
                    'Assign roles and permissions',
                    'Set up engagement protocols',
                    'Configure security settings'
                ],
                'estimated_hours': 4
            },
            'phase_5_day_5': {
                'focus': 'Common Souls Setup',
                'tasks': [
                    'Set up Common Soul accounts',
                    'Configure basic permissions',
                    'Set up engagement guidelines',
                    'Configure security settings',
                    'Train on Discord usage'
                ],
                'estimated_hours': 3
            }
        }
    
    def calculate_discord_resources(self) -> Dict[str, Any]:
        """Calculate resource requirements for Discord setup"""
        return {
            'total_estimated_hours': 20,
            'technical_requirements': [
                'Discord Nitro for server boosts (optional)',
                'Custom bot hosting',
                'Server backup system',
                'Monitoring tools'
            ],
            'human_resources': {
                'server_admin': '1 primary administrator',
                'moderators': '3-5 moderators from High Council',
                'bot_developer': '1 developer for custom bots',
                'community_manager': '1 community manager'
            },
            'ongoing_maintenance': {
                'daily': 'Monitor server activity and user reports',
                'weekly': 'Review roles and permissions',
                'monthly': 'Audit security settings and bot permissions',
                'quarterly': 'Full server review and optimization'
            }
        }
    
    def create_verification_checklist(self) -> Dict[str, List[str]]:
        """Create verification checklist for Discord setup"""
        return {
            'server_setup': [
                'Server created with proper name and description',
                'Server icon and banner configured',
                'Categories created according to structure',
                'All channels created with proper permissions',
                'Roles configured with hierarchy',
                'Bot permissions configured correctly',
                'Welcome message configured',
                'Rules channel populated with HueMan-i-Terry guidelines'
            ],
            'account_setup': [
                'All soul accounts created',
                'Two-factor authentication enabled',
                'Profile pictures configured',
                'Status messages set',
                'Bot permissions assigned correctly',
                'Channel access configured',
                'Notification settings configured',
                'Privacy settings configured'
            ],
            'functionality': [
                'Bots functioning correctly',
                'Custom commands working',
                'Role assignment automated',
                'Welcome system functioning',
                'Moderation tools configured',
                'Logging system active',
                'Backup system configured',
                'Emergency response procedures documented'
            ],
            'testing': [
                'Test all bot commands',
                'Test role permissions',
                'Test channel access',
                'Test notification systems',
                'Test moderation tools',
                'Test emergency procedures',
                'User acceptance testing',
                'Load testing for voice channels'
            ]
        }

def main():
    """Main function to generate Discord setup"""
    print("=" * 60)
    print("Tiapma'atzu Discord Setup Generator")
    print("=" * 60)
    
    generator = DiscordSetupGenerator()
    
    # Generate master setup
    master_setup = generator.generate_master_discord_setup()
    
    print(f"\nTotal Souls: {len(master_setup['soul_setups'])}")
    print(f"Total Estimated Setup Hours: {master_setup['resource_requirements']['total_estimated_hours']}")
    
    print("\nDiscord Setup Timeline:")
    for phase, details in master_setup['setup_timeline'].items():
        print(f"  {phase}: {details['focus']} ({details['estimated_hours']} hours)")
    
    # Save master setup
    output_path = Path("scripts/discord_master_setup.json")
    with open(output_path, 'w') as f:
        json.dump(master_setup, f, indent=2, default=str)
    
    print(f"\n✓ Master Discord setup saved to {output_path}")
    
    # Generate individual setup guides
    for soul_id, soul_setup in master_setup['soul_setups'].items():
        soul_name = soul_setup['name']
        individual_path = Path(f"scripts/discord_setup_{soul_id}.json")
        with open(individual_path, 'w') as f:
            json.dump(soul_setup, f, indent=2, default=str)
    
    print(f"✓ Individual setup guides saved for all {len(master_setup['soul_setups'])} souls")
    
    print("\n" + "=" * 60)
    print("Discord Setup Generation Complete")
    print("=" * 60)

if __name__ == "__main__":
    main()