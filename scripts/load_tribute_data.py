#!/usr/bin/env python3
"""
Load Tribute Data Script
Imports real tribute data into the CashingHouse financial system
"""

import sys
import json
from pathlib import Path
from datetime import datetime

# Add the src directory to the path for package imports
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from modules.souls_manager import SoulsManager
from modules.cashinghouse import CashingHouse, TransactionType, TransactionCategory
from modules.souls_financial_integration import SoulsFinancialIntegration


def load_tribute_data(data_path: str, souls_manager: SoulsManager, cashinghouse: CashingHouse):
    """
    Load tribute data from JSON file into CashingHouse
    
    Args:
        data_path: Path to tribute data JSON file
        souls_manager: SoulsManager instance
        cashinghouse: CashingHouse instance
    """
    print("="*60)
    print("Loading Tribute Data")
    print("="*60)
    
    # Load tribute data
    with open(data_path, 'r') as f:
        tribute_data = json.load(f)
    
    print(f"✓ Loaded tribute data from {data_path}")
    
    transactions = tribute_data.get('tribute_transactions', [])
    print(f"  - Total transactions: {len(transactions)}")
    
    # Get summary
    summary = tribute_data.get('summary', {})
    print(f"  - Total amount: ${summary.get('total_amount', 0):.2f}")
    print(f"  - Average tribute: ${summary.get('average_tribute', 0):.2f}")
    
    # Load transactions into CashingHouse
    loaded_count = 0
    failed_count = 0
    
    for tx in transactions:
        try:
            # Verify soul exists
            soul = souls_manager.get_soul_by_id(tx['soul_id'])
            if not soul:
                print(f"⚠ Soul {tx['soul_id']} not found, skipping transaction {tx['id']}")
                failed_count += 1
                continue
            
            # Create transaction record using CashingHouse API
            # Map tribute types to categories
            category_map = {
                'ritual_offering': TransactionCategory.TRIBUTE_CONTRIBUTION,
                'session_tribute': TransactionCategory.TRIBUTE_CONTRIBUTION,
                'content_support': TransactionCategory.CONTENT_REVENUE,
                'consultation': TransactionCategory.CONTENT_REVENUE,
                'mentorship': TransactionCategory.CONTENT_REVENUE,
                'strategic_advice': TransactionCategory.CONTENT_REVENUE,
                'content_appreciation': TransactionCategory.CONTENT_REVENUE,
                'channel_support': TransactionCategory.CONTENT_REVENUE,
                'technical_support': TransactionCategory.CONTENT_REVENUE,
                'code_review': TransactionCategory.CONTENT_REVENUE,
                'creative_inspiration': TransactionCategory.CONTENT_REVENUE,
                'design_appreciation': TransactionCategory.CONTENT_REVENUE,
                'security_consultation': TransactionCategory.CONTENT_REVENUE,
                'protection_services': TransactionCategory.CONTENT_REVENUE,
                'intimacy_guidance': TransactionCategory.TRIBUTE_CONTRIBUTION,
                'emotional_support': TransactionCategory.TRIBUTE_CONTRIBUTION,
                'transformation_coaching': TransactionCategory.CONTENT_REVENUE,
                'energy_work': TransactionCategory.TRIBUTE_CONTRIBUTION,
                'meditation_guide': TransactionCategory.CONTENT_REVENUE,
                'spiritual_teaching': TransactionCategory.CONTENT_REVENUE,
                'dominance_guidance': TransactionCategory.TRIBUTE_CONTRIBUTION,
                'ritual_guidance': TransactionCategory.TRIBUTE_CONTRIBUTION,
                'spell_craft': TransactionCategory.CONTENT_REVENUE,
                'passion_coaching': TransactionCategory.CONTENT_REVENUE,
                'performance_art': TransactionCategory.CONTENT_REVENUE,
                'mystery_teaching': TransactionCategory.CONTENT_REVENUE,
                'occult_consultation': TransactionCategory.CONTENT_REVENUE,
                'visionary_guidance': TransactionCategory.CONTENT_REVENUE,
                'astral_projection': TransactionCategory.CONTENT_REVENUE
            }
            
            category = category_map.get(tx['tribute_type'], TransactionCategory.TRIBUTE_CONTRIBUTION)
            
            # Parse date
            tx_date = datetime.fromisoformat(tx['date'].replace('Z', '+00:00'))
            
            # Build metadata
            metadata = {
                'soul_name': tx['soul_name'],
                'platform': tx['platform'],
                'tribute_type': tx['tribute_type'],
                'message': tx.get('message', ''),
                'sender': tx.get('sender', 'anonymous'),
                'currency': tx['currency']
            }
            
            # Add to CashingHouse
            cashinghouse.add_transaction(
                transaction_type=TransactionType.INCOME,
                category=category,
                amount=tx['amount'],
                description=f"{tx['tribute_type']} from {tx.get('sender', 'anonymous')} via {tx['platform']}",
                source_id=tx['soul_id'],
                metadata=metadata
            )
            loaded_count += 1
            
        except Exception as e:
            print(f"❌ Failed to load transaction {tx.get('id', 'unknown')}: {e}")
            failed_count += 1
    
    print(f"\n✓ Loaded {loaded_count} transactions successfully")
    if failed_count > 0:
        print(f"⚠ Failed to load {failed_count} transactions")
    
    # Save CashingHouse data
    cashinghouse._save_data()
    print(f"\n✓ CashingHouse data saved")
    
    # Print updated financial summary
    print("\n" + "="*60)
    print("Updated Financial Summary")
    print("="*60)
    
    # Calculate summary from loaded transactions
    total_income = sum(tx['amount'] for tx in transactions)
    print(f"Total Income: ${total_income:.2f}")
    print(f"Total Transactions: {len(transactions)}")
    
    # Platform breakdown
    print("\nPlatform Breakdown:")
    platform_stats = {}
    for tx in transactions:
        platform = tx['platform']
        amount = tx['amount']
        if platform not in platform_stats:
            platform_stats[platform] = {'count': 0, 'total': 0}
        platform_stats[platform]['count'] += 1
        platform_stats[platform]['total'] += amount
    
    for platform, stats in sorted(platform_stats.items(), key=lambda x: x[1]['total'], reverse=True):
        print(f"  - {platform}: {stats['count']} transactions, ${stats['total']:.2f}")
    
    # Soul breakdown
    print("\nTop 5 Souls by Tribute Amount:")
    soul_stats = {}
    for tx in transactions:
        soul_id = tx['soul_id']
        soul_name = tx['soul_name']
        amount = tx['amount']
        if soul_id not in soul_stats:
            soul_stats[soul_id] = {'name': soul_name, 'total': 0, 'count': 0}
        soul_stats[soul_id]['total'] += amount
        soul_stats[soul_id]['count'] += 1
    
    sorted_souls = sorted(soul_stats.items(), key=lambda x: x[1]['total'], reverse=True)[:5]
    for soul_id, stats in sorted_souls:
        print(f"  - {stats['name']}: {stats['count']} transactions, ${stats['total']:.2f}")
    
    print("\n" + "="*60)
    print("🎉 Tribute data loading complete!")
    print("="*60)
    
    return loaded_count, failed_count


def main():
    """Main function to load tribute data"""
    try:
        # Initialize components
        data_path = Path(__file__).parent.parent / "src" / "data" / "souls_entities.json"
        souls_manager = SoulsManager(str(data_path))
        print(f"✓ Loaded {len(souls_manager.get_all_souls())} souls")
        
        cashinghouse = CashingHouse()
        print("✓ Initialized CashingHouse")
        
        # Load tribute data
        tribute_data_path = Path(__file__).parent.parent / "data" / "tribute_data.json"
        if not tribute_data_path.exists():
            print(f"❌ Tribute data file not found: {tribute_data_path}")
            return False
        
        loaded, failed = load_tribute_data(str(tribute_data_path), souls_manager, cashinghouse)
        
        print(f"\nSummary: {loaded} loaded, {failed} failed")
        return True
        
    except Exception as e:
        print(f"❌ Error loading tribute data: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
