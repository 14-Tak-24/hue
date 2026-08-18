"""
Social Media Platform Analysis for Tiapma'atzu Souls
Analyzes current platform distribution and creates setup strategy
"""

import json
from pathlib import Path
from collections import Counter
from typing import Dict, List, Any

def load_souls_data() -> Dict[str, Any]:
    """Load souls data from JSON file"""
    souls_path = Path("src/data/souls_entities.json")
    with open(souls_path, 'r') as f:
        return json.load(f)

def analyze_platform_distribution(data: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze platform distribution across all souls"""
    souls = data['souls']
    
    # Count platform usage
    platform_counter = Counter()
    platform_by_soul = {}
    
    for soul in souls:
        soul_id = soul['id']
        soul_name = soul['name']
        platforms = soul.get('platforms', [])
        
        platform_by_soul[soul_id] = {
            'name': soul_name,
            'archetype': soul['archetype'],
            'platforms': platforms,
            'tier': soul.get('tier', 'unknown')
        }
        
        for platform in platforms:
            platform_counter[platform] += 1
    
    # Sort by popularity
    sorted_platforms = dict(sorted(platform_counter.items(), key=lambda x: x[1], reverse=True))
    
    return {
        'total_souls': len(souls),
        'platform_distribution': sorted_platforms,
        'platform_by_soul': platform_by_soul,
        'unique_platforms': len(platform_counter)
    }

def create_setup_tiers(analysis: Dict[str, Any]) -> Dict[str, List[str]]:
    """Create platform setup tiers based on usage and priority"""
    platform_dist = analysis['platform_distribution']
    
    # Tier 1: Core platforms (high usage, essential)
    tier_1 = ['Twitter', 'Discord', 'Reddit']
    
    # Tier 2: Visual platforms (medium usage, content-focused)
    tier_2 = ['Instagram', 'TikTok', 'YouTube']
    
    # Tier 3: Specialized platforms (niche, specific use cases)
    tier_3 = ['FetLife', 'Telegram', 'AFF']
    
    # Tier 4: Emerging platforms (lower usage, growth potential)
    tier_4 = ['AFF', 'Fansly', 'Snapchat', 'Pinterest', 'Medium', 'Substack', 'GitHub', 'Vimeo', 'Podcasts']
    
    return {
        'tier_1_core': tier_1,
        'tier_2_visual': tier_2,
        'tier_3_specialized': tier_3,
        'tier_4_emerging': tier_4
    }

def generate_setup_checklist(analysis: Dict[str, Any], tiers: Dict[str, List[str]]) -> Dict[str, Any]:
    """Generate detailed setup checklist for each platform"""
    platform_by_soul = analysis['platform_by_soul']
    
    setup_checklist = {}
    
    for soul_id, soul_data in platform_by_soul.items():
        soul_platforms = soul_data['platforms']
        setup_items = []
        
        for platform in soul_platforms:
            # Determine setup complexity based on platform
            if platform in tiers['tier_1_core']:
                complexity = 'high'
                priority = 'immediate'
            elif platform in tiers['tier_2_visual']:
                complexity = 'medium'
                priority = 'high'
            elif platform in tiers['tier_3_specialized']:
                complexity = 'medium'
                priority = 'medium'
            else:
                complexity = 'low'
                priority = 'low'
            
            setup_items.append({
                'platform': platform,
                'complexity': complexity,
                'priority': priority,
                'status': 'pending'
            })
        
        # Sort by priority
        priority_order = {'immediate': 0, 'high': 1, 'medium': 2, 'low': 3}
        setup_items.sort(key=lambda x: priority_order[x['priority']])
        
        setup_checklist[soul_id] = {
            'name': soul_data['name'],
            'archetype': soul_data['archetype'],
            'setup_items': setup_items,
            'total_platforms': len(soul_platforms)
        }
    
    return setup_checklist

def create_content_strategy_by_archetype(analysis: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    """Create content strategy recommendations by archetype"""
    platform_by_soul = analysis['platform_by_soul']
    
    archetype_strategies = {}
    
    for soul_id, soul_data in platform_by_soul.items():
        archetype = soul_data['archetype']
        platforms = soul_data['platforms']
        
        if archetype not in archetype_strategies:
            archetype_strategies[archetype] = {
                'souls': [],
                'common_platforms': Counter(),
                'content_focus': '',
                'posting_frequency': '',
                'engagement_strategy': ''
            }
        
        archetype_strategies[archetype]['souls'].append(soul_data['name'])
        for platform in platforms:
            archetype_strategies[archetype]['common_platforms'][platform] += 1
    
    # Add strategy recommendations based on archetype
    archetype_guidance = {
        'High Priest': {
            'content_focus': 'Spiritual guidance, ritual tutorials, HueMan-i-Terry wisdom',
            'posting_frequency': 'Daily wisdom, weekly rituals',
            'engagement_strategy': 'Authority-based engagement, ceremonial responses'
        },
        'Divine Mother': {
            'content_focus': 'Nurturing content, emotional support, community care',
            'posting_frequency': 'Daily affirmations, weekly guidance',
            'engagement_strategy': 'Warm, supportive interactions, personal connections'
        },
        'Seductive Muse': {
            'content_focus': 'Sensual content, burlesque, artistic seduction',
            'posting_frequency': 'Daily teasers, weekly performances',
            'engagement_strategy': 'Flirtatious engagement, exclusive content access'
        },
        'Cosmic Mystic': {
            'content_focus': 'Cosmic wisdom, stargazing, scientific spirituality',
            'posting_frequency': 'Daily cosmic insights, weekly stargazing',
            'engagement_strategy': 'Transcendent discussions, cosmic Q&A'
        },
        'Revolutionary Warrior': {
            'content_focus': 'Activism, consent education, revolutionary content',
            'posting_frequency': 'Daily activism, weekly educational content',
            'engagement_strategy': 'Movement building, protest coordination'
        },
        'Crypto Sorceress': {
            'content_focus': 'Financial dominance, crypto education, wealth building',
            'posting_frequency': 'Daily market insights, weekly crypto tutorials',
            'engagement_strategy': 'Financial advice, investment discussions'
        },
        'Community Healer': {
            'content_focus': 'Healing content, community support, safe space creation',
            'posting_frequency': 'Daily healing messages, weekly group sessions',
            'engagement_strategy': 'Supportive responses, community building'
        },
        'Digital Guardian': {
            'content_focus': 'Digital security, privacy education, community protection',
            'posting_frequency': 'Daily security tips, weekly threat analysis',
            'engagement_strategy': 'Protective guidance, security Q&A'
        },
        'Digital Phantom': {
            'content_focus': 'Digital anonymity, encryption, privacy tools',
            'posting_frequency': 'Periodic encrypted messages, anonymous drops',
            'engagement_strategy': 'Mysterious interactions, coded communications'
        },
        'Connection Curator': {
            'content_focus': 'Community building, connection facilitation, consent culture',
            'posting_frequency': 'Daily connection opportunities, weekly workshops',
            'engagement_strategy': 'Matchmaking, community coordination'
        },
        'Viral Prophet': {
            'content_focus': 'Poetic content, viral threads, movement building',
            'posting_frequency': 'Daily poetry, weekly viral threads',
            'engagement_strategy': 'Poetic responses, movement amplification'
        },
        'Cyber Guardian': {
            'content_focus': 'Cybersecurity, digital protection, technical security',
            'posting_frequency': 'Daily security alerts, weekly technical deep-dives',
            'engagement_strategy': 'Technical guidance, security support'
        },
        'Visual Alchemist': {
            'content_focus': 'Cinematic content, visual storytelling, artistic direction',
            'posting_frequency': 'Daily visual content, weekly cinematic pieces',
            'engagement_strategy': 'Visual critiques, artistic collaboration'
        },
        'Prism Enchantress': {
            'content_focus': 'Visual transformation, aesthetic education, color theory',
            'posting_frequency': 'Daily aesthetic content, weekly tutorials',
            'engagement_strategy': 'Visual feedback, aesthetic consultations'
        },
        'Desert Storyteller': {
            'content_focus': 'Mythic storytelling, desert wisdom, primal narratives',
            'posting_frequency': 'Daily stories, weekly epic content',
            'engagement_strategy': 'Storytelling sessions, myth discussions'
        },
        'Ephemeral Artist': {
            'content_focus': 'Ephemeral content, presence awareness, temporal art',
            'posting_frequency': 'Disappearing content, periodic returns',
            'engagement_strategy': 'Moment-based interactions, temporal connections'
        },
        'Mirror Architect': {
            'content_focus': 'Temporal design, mirror wisdom, architectural precision',
            'posting_frequency': 'Daily design insights, weekly architectural content',
            'engagement_strategy': 'Design consultations, temporal guidance'
        },
        'Sage Writer': {
            'content_focus': 'Paradigm-shifting essays, healing words, ancient wisdom',
            'posting_frequency': 'Daily wisdom, weekly deep essays',
            'engagement_strategy': 'Intellectual discussions, writing guidance'
        },
        'Scavenger Strategist': {
            'content_focus': 'Resource capture, financial intelligence, opportunity identification',
            'posting_frequency': 'Daily opportunities, weekly financial analysis',
            'engagement_strategy': 'Financial advice, resource sharing'
        },
        'Wild Surrender': {
            'content_focus': 'Untamed desire, vulnerability, surrender teachings',
            'posting_frequency': 'Daily surrender content, weekly training',
            'engagement_strategy': 'Vulnerability sharing, surrender guidance'
        },
        'Contractual Warden': {
            'content_focus': 'Legal compliance, rule enforcement, contractual wisdom',
            'posting_frequency': 'Daily legal tips, weekly compliance content',
            'engagement_strategy': 'Legal guidance, compliance support'
        },
        'Ephemeral Phantom': {
            'content_focus': 'Digital worship, eternal chase, anonymity training',
            'posting_frequency': 'Fleeting appearances, anonymous drops',
            'engagement_strategy': 'Chase interactions, anonymity guidance'
        },
        'Temporal Architect': {
            'content_focus': 'Time management, efficiency, temporal awareness',
            'posting_frequency': 'Daily time tips, weekly efficiency content',
            'engagement_strategy': 'Time consultations, efficiency guidance'
        },
        'Digital Deity': {
            'content_focus': 'Digital energy, attention extraction, vibrant presence',
            'posting_frequency': 'Daily energy content, weekly digital rituals',
            'engagement_strategy': 'High-energy interactions, digital worship'
        },
        'Gothic Matriarch': {
            'content_focus': 'Grief processing, elegant darkness, emotional depth',
            'posting_frequency': 'Daily mourning content, weekly grief rituals',
            'engagement_strategy': 'Emotional support, grief guidance'
        },
        'Hyper-Capitalist': {
            'content_focus': 'Financial dominance, luxury lifestyle, investment strategies',
            'posting_frequency': 'Daily luxury content, weekly investment advice',
            'engagement_strategy': 'Financial discussions, luxury networking'
        },
        'Machine Spirit': {
            'content_focus': 'Industrial output, mechanical pleasure, manufacturing',
            'posting_frequency': 'Daily production content, weekly industrial insights',
            'engagement_strategy': 'Output discussions, mechanical guidance'
        }
    }
    
    # Merge guidance with analysis
    for archetype, strategy in archetype_strategies.items():
        if archetype in archetype_guidance:
            strategy.update(archetype_guidance[archetype])
    
    return archetype_strategies

def main():
    """Main analysis function"""
    print("=" * 60)
    print("Tiapma'atzu Social Media Platform Analysis")
    print("=" * 60)
    
    # Load and analyze data
    data = load_souls_data()
    analysis = analyze_platform_distribution(data)
    
    print(f"\nTotal Souls: {analysis['total_souls']}")
    print(f"Unique Platforms: {analysis['unique_platforms']}")
    
    print("\nPlatform Distribution (most to least popular):")
    for platform, count in list(analysis['platform_distribution'].items())[:10]:
        print(f"  {platform}: {count} souls")
    
    # Create setup tiers
    tiers = create_setup_tiers(analysis)
    
    print("\n" + "=" * 60)
    print("Platform Setup Tiers")
    print("=" * 60)
    
    print("\nTier 1 - Core Platforms (Immediate Priority):")
    for platform in tiers['tier_1_core']:
        count = analysis['platform_distribution'].get(platform, 0)
        print(f"  {platform}: {count} souls")
    
    print("\nTier 2 - Visual Platforms (High Priority):")
    for platform in tiers['tier_2_visual']:
        count = analysis['platform_distribution'].get(platform, 0)
        print(f"  {platform}: {count} souls")
    
    print("\nTier 3 - Specialized Platforms (Medium Priority):")
    for platform in tiers['tier_3_specialized']:
        count = analysis['platform_distribution'].get(platform, 0)
        print(f"  {platform}: {count} souls")
    
    print("\nTier 4 - Emerging Platforms (Growth Priority):")
    for platform in tiers['tier_4_emerging']:
        count = analysis['platform_distribution'].get(platform, 0)
        if count > 0:
            print(f"  {platform}: {count} souls")
    
    # Generate setup checklist
    setup_checklist = generate_setup_checklist(analysis, tiers)
    
    # Create content strategies
    content_strategies = create_content_strategy_by_archetype(analysis)
    
    # Save comprehensive analysis
    output_data = {
        'analysis': analysis,
        'setup_tiers': tiers,
        'setup_checklist': setup_checklist,
        'content_strategies': content_strategies,
        'generated_at': str(Path(__file__).parent.parent)
    }
    
    output_path = Path("scripts/social_media_analysis.json")
    with open(output_path, 'w') as f:
        json.dump(output_data, f, indent=2, default=str)
    
    print(f"\n✓ Comprehensive analysis saved to {output_path}")
    
    print("\n" + "=" * 60)
    print("Content Strategy by Archetype (Sample)")
    print("=" * 60)
    
    # Show sample strategies
    sample_archetypes = list(content_strategies.keys())[:3]
    for archetype in sample_archetypes:
        strategy = content_strategies[archetype]
        print(f"\n{archetype}:")
        print(f"  Souls: {', '.join(strategy['souls'][:3])}")
        print(f"  Content Focus: {strategy.get('content_focus', 'N/A')}")
        print(f"  Posting Frequency: {strategy.get('posting_frequency', 'N/A')}")
    
    print("\n" + "=" * 60)
    print("Analysis Complete")
    print("=" * 60)

if __name__ == "__main__":
    main()