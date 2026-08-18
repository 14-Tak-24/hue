"""
Generate Realistic Tribute Data for Tiapma'atzu Platform
Creates sample tribute transactions to improve financial metrics
"""

import json
import random
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Load souls data to generate realistic tributes
def load_souls_data() -> List[Dict[str, Any]]:
    """Load souls data from the JSON file"""
    souls_path = Path("src/data/souls_entities.json")
    if souls_path.exists():
        with open(souls_path, 'r') as f:
            data = json.load(f)
            return data.get('souls', [])
    return []

def generate_realistic_tributes(
    num_tributes: int = 100,
    days_back: int = 90,
    min_amount: float = 10.0,
    max_amount: float = 500.0
) -> List[Dict[str, Any]]:
    """
    Generate realistic tribute transactions
    
    Args:
        num_tributes: Number of tributes to generate
        days_back: How many days back to generate tributes
        min_amount: Minimum tribute amount
        max_amount: Maximum tribute amount
        
    Returns:
        List of tribute transaction dictionaries
    """
    souls = load_souls_data()
    if not souls:
        print("No souls data found, using generic data")
        souls = [{'id': f'soul_{i}', 'name': f'Soul {i}'} for i in range(1, 29)]
    
    # Impact areas based on the platform
    impact_areas = [
        'content', 'community', 'infrastructure', 'marketing', 
        'legal', 'operations', 'research', 'development'
    ]
    
    # Platforms from the souls data
    platforms = ['twitter', 'discord', 'reddit', 'AFF', 'youtube', 'tiktok', 'instagram']
    
    tributes = []
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days_back)
    
    for i in range(num_tributes):
        # Select random soul
        soul = random.choice(souls)
        soul_id = soul.get('id', f'soul_{random.randint(1, 28)}')
        
        # Generate random date within range
        days_offset = random.randint(0, days_back)
        tribute_date = start_date + timedelta(days=days_offset)
        
        # Add some time randomness
        tribute_date = tribute_date.replace(
            hour=random.randint(0, 23),
            minute=random.randint(0, 59),
            second=random.randint(0, 59)
        )
        
        # Generate amount with some realistic distribution
        # Most tributes are smaller, fewer are larger
        if random.random() < 0.7:  # 70% are smaller amounts
            amount = random.uniform(min_amount, min_amount * 5)
        else:  # 30% are larger amounts
            amount = random.uniform(min_amount * 5, max_amount)
        
        amount = round(amount, 2)
        
        # Select impact area and platform
        impact_area = random.choice(impact_areas)
        platform = random.choice(platforms)
        
        # Generate realistic description
        descriptions = [
            f"Content contribution from {soul.get('name', 'Unknown')}",
            f"Community engagement tribute - {platform}",
            f"Platform revenue share - {impact_area}",
            f"Soul {soul_id} contribution to {impact_area}",
            f"{platform} engagement reward",
            f"Content creation tribute",
            f"Community building contribution",
            f"Platform activity reward",
            f"Influence contribution",
            f"Engagement tribute from {soul.get('name', 'Unknown')}"
        ]
        description = random.choice(descriptions)
        
        tribute = {
            'soul_id': soul_id,
            'amount': amount,
            'impact_area': impact_area,
            'platform': platform,
            'description': description,
            'timestamp': tribute_date.isoformat(),
            'metadata': {
                'source': 'generated',
                'soul_name': soul.get('name', 'Unknown'),
                'archetype': soul.get('archetype', 'Unknown'),
                'rarity': soul.get('rarity', 'Unknown')
            }
        }
        
        tributes.append(tribute)
    
    # Sort by timestamp
    tributes.sort(key=lambda x: x['timestamp'])
    
    return tributes

def analyze_tributes(tributes: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Analyze generated tribute data"""
    if not tributes:
        return {'error': 'No tributes to analyze'}
    
    total_amount = sum(t['amount'] for t in tributes)
    avg_amount = total_amount / len(tributes)
    
    # By impact area
    by_impact = {}
    for t in tributes:
        area = t['impact_area']
        if area not in by_impact:
            by_impact[area] = {'count': 0, 'total': 0.0}
        by_impact[area]['count'] += 1
        by_impact[area]['total'] += t['amount']
    
    # By platform
    by_platform = {}
    for t in tributes:
        plat = t['platform']
        if plat not in by_platform:
            by_platform[plat] = {'count': 0, 'total': 0.0}
        by_platform[plat]['count'] += 1
        by_platform[plat]['total'] += t['amount']
    
    # By soul
    by_soul = {}
    for t in tributes:
        soul = t['soul_id']
        if soul not in by_soul:
            by_soul[soul] = {'count': 0, 'total': 0.0}
        by_soul[soul]['count'] += 1
        by_soul[soul]['total'] += t['amount']
    
    return {
        'total_tributes': len(tributes),
        'total_amount': round(total_amount, 2),
        'average_amount': round(avg_amount, 2),
        'by_impact_area': by_impact,
        'by_platform': by_platform,
        'by_soul': by_soul,
        'date_range': {
            'start': min(t['timestamp'] for t in tributes),
            'end': max(t['timestamp'] for t in tributes)
        }
    }

def save_tributes_to_file(tributes: List[Dict[str, Any]], filename: str = 'generated_tributes.json'):
    """Save generated tributes to a JSON file"""
    output_path = Path(filename)
    with open(output_path, 'w') as f:
        json.dump({
            'tributes': tributes,
            'generated_at': datetime.now().isoformat(),
            'analysis': analyze_tributes(tributes)
        }, f, indent=2)
    
    print(f"✓ Saved {len(tributes)} tributes to {filename}")
    return output_path

def import_tributes_to_cashinghouse(tributes: List[Dict[str, Any]]):
    """Import generated tributes into the CashingHouse system"""
    try:
        from src.modules.cashinghouse import CashingHouse
        
        cashinghouse = CashingHouse()
        
        imported_count = 0
        for tribute in tributes:
            try:
                # Use the new record_tribute method
                cashinghouse.record_tribute(
                    soul_id=tribute['soul_id'],
                    amount=tribute['amount'],
                    impact_area=tribute['impact_area'],
                    platform=tribute['platform'],
                    metadata=tribute.get('metadata', {})
                )
                imported_count += 1
                
            except Exception as e:
                print(f"✗ Failed to import tribute: {e}")
        
        print(f"✓ Imported {imported_count} tributes into CashingHouse")
        return imported_count
        
    except ImportError as e:
        print(f"✗ Could not import CashingHouse: {e}")
        return 0

def main():
    """Main function to generate and process tribute data"""
    print("=" * 60)
    print("Generating Realistic Tribute Data")
    print("=" * 60)
    
    # Generate tributes
    print("\nGenerating 150 realistic tributes over 90 days...")
    tributes = generate_realistic_tributes(
        num_tributes=150,
        days_back=90,
        min_amount=10.0,
        max_amount=500.0
    )
    
    # Analyze tributes
    print("\nAnalyzing generated tributes...")
    analysis = analyze_tributes(tributes)
    
    print(f"\nGenerated Tribute Summary:")
    print(f"  Total Tributes: {analysis['total_tributes']}")
    print(f"  Total Amount: ${analysis['total_amount']:,.2f}")
    print(f"  Average Amount: ${analysis['average_amount']:,.2f}")
    print(f"  Date Range: {analysis['date_range']['start'][:10]} to {analysis['date_range']['end'][:10]}")
    
    print(f"\n  By Impact Area:")
    for area, data in sorted(analysis['by_impact_area'].items(), key=lambda x: x[1]['total'], reverse=True):
        print(f"    {area}: {data['count']} tributes, ${data['total']:,.2f}")
    
    print(f"\n  By Platform:")
    for platform, data in sorted(analysis['by_platform'].items(), key=lambda x: x[1]['total'], reverse=True):
        print(f"    {platform}: {data['count']} tributes, ${data['total']:,.2f}")
    
    # Save to file
    print("\nSaving tributes to file...")
    save_tributes_to_file(tributes, 'scripts/generated_tributes.json')
    
    # Import to CashingHouse
    print("\nImporting tributes to CashingHouse...")
    imported = import_tributes_to_cashinghouse(tributes)
    
    if imported > 0:
        print(f"\n✓ Successfully imported {imported} tributes into the financial system")
        print("✓ Financial metrics should now be improved")
    else:
        print("\n⚠ Could not import tributes automatically")
        print("  You can manually import using the CashingHouse bulk_import_transactions method")
    
    print("\n" + "=" * 60)
    print("Tribute Data Generation Complete")
    print("=" * 60)

if __name__ == "__main__":
    main()