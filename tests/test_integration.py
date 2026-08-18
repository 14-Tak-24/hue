"""
Integration Test for Tiapma'atzu Platform in Hue Directory
Tests the souls management and Firebase integration
"""

import sys
import os
from datetime import datetime, timedelta
from pathlib import Path

# Add the src directory to the path for package imports
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

def test_souls_manager():
    """Test the souls manager functionality"""
    print("Testing Souls Manager...")
    
    try:
        # Import souls manager
        from src.modules.souls_manager import SoulsManager
        
        # Initialize with explicit path
        data_path = Path(__file__).parent.parent / "src" / "data" / "souls_entities.json"
        souls_manager = SoulsManager(str(data_path))
        
        # Test loading souls
        all_souls = souls_manager.get_all_souls()
        print(f"✓ Loaded {len(all_souls)} souls")
        assert len(all_souls) > 0, "No souls loaded"
        
        # Test getting specific soul
        mac_nazarene = souls_manager.get_soul_by_name("Mac Nazarene")
        assert mac_nazarene is not None, "Mac Nazarene not found"
        print(f"✓ Found Mac Nazarene: {mac_nazarene.archetype}")
        
        # Test filtering by rarity
        rare_souls = souls_manager.get_souls_by_rarity("Rare")
        print(f"✓ Found {len(rare_souls)} rare souls")
        
        # Test filtering by platform
        discord_souls = souls_manager.get_souls_by_platform("Discord")
        print(f"✓ Found {len(discord_souls)} souls on Discord")
        
        # Test statistics
        stats = souls_manager.get_statistics()
        print(f"✓ Statistics: {stats['total_souls']} total souls")
        assert stats['total_souls'] > 0, "No souls in statistics"
        
        # Test search functionality
        search_results = souls_manager.search_souls("crypto")
        print(f"✓ Search for 'crypto': {len(search_results)} results")
        
        # Test Firebase export
        firebase_data = []
        for soul in all_souls:
            firebase_data.append({
                'id': soul.id,
                'name': soul.name,
                'archetype': soul.archetype,
                'rarity': soul.rarity,
                'platforms': soul.platforms
            })
        print(f"✓ Firebase export ready: {len(firebase_data)} souls")
        assert len(firebase_data) > 0, "No firebase data exported"
        
    except Exception as e:
        print(f"✗ Souls Manager test failed: {e}")
        import traceback
        traceback.print_exc()
        raise


def test_cashinghouse():
    """Test the CashingHouse financial system"""
    print("\nTesting CashingHouse System...")
    
    try:
        # Import CashingHouse
        from src.modules.cashinghouse import CashingHouse, TransactionType, TransactionCategory
        
        # Initialize with a test data path
        test_data_path = Path(__file__).parent / "test_cashinghouse.json"
        cashinghouse = CashingHouse(str(test_data_path))
        
        # Test adding transactions
        income_tx = cashinghouse.add_transaction(
            transaction_type=TransactionType.INCOME,
            category=TransactionCategory.CONTENT_REVENUE,
            amount=500.0,
            description="Content revenue from YouTube",
            source_id="youtube",
            metadata={"video_id": "test_video_123"}
        )
        print(f"✓ Added income transaction: {income_tx.transaction_id}")
        assert income_tx.transaction_id is not None, "Transaction ID not generated"
        
        expense_tx = cashinghouse.add_transaction(
            transaction_type=TransactionType.EXPENSE,
            category=TransactionCategory.OPERATIONAL_COSTS,
            amount=150.0,
            description="Server costs",
            destination_id="aws",
            metadata={"service": "ec2"}
        )
        print(f"✓ Added expense transaction: {expense_tx.transaction_id}")
        assert expense_tx.transaction_id is not None, "Transaction ID not generated"
        
        # Test financial summary
        summary = cashinghouse.get_financial_summary()
        print(f"✓ Financial summary: ${summary.net_balance:.2f} net balance")
        assert summary.net_balance == 350.0, "Net balance calculation incorrect"
        
        # Test Firebase export
        firebase_data = cashinghouse.export_for_firebase()
        print(f"✓ Firebase export ready: {len(firebase_data['transactions'])} transactions")
        assert len(firebase_data['transactions']) > 0, "No transactions exported"
        
        # Clean up test file
        if test_data_path.exists():
            test_data_path.unlink()
        
    except Exception as e:
        print(f"✗ CashingHouse test failed: {e}")
        import traceback
        traceback.print_exc()
        raise


def test_souls_financial_integration():
    """Test the souls-financial integration"""
    print("\nTesting Souls-Financial Integration...")
    
    try:
        # Import modules
        from src.modules.souls_manager import SoulsManager
        from src.modules.souls_financial_integration import SoulsFinancialIntegration, TributeType
        
        # Initialize with explicit paths
        data_path = Path(__file__).parent.parent / "src" / "data" / "souls_entities.json"
        souls_manager = SoulsManager(str(data_path))
        financial_integration = SoulsFinancialIntegration(souls_manager)
        
        # Test recording a tribute
        mac_nazarene = souls_manager.get_soul_by_name("Mac Nazarene")
        assert mac_nazarene is not None, "Mac Nazarene not found"
        
        tribute = financial_integration.record_tribute(
            soul_id=mac_nazarene.id,
            tribute_type=TributeType.MONETARY,
            amount=100.0,
            description="Monthly contribution to temple operations",
            impact_area="temple_operations"
        )
        print(f"✓ Recorded tribute: {tribute.tribute_id}")
        assert tribute.tribute_id is not None, "Tribute ID not generated"
        
        # Test getting financial impact
        impact = financial_integration.get_soul_financial_impact(mac_nazarene.id)
        assert impact is not None, "Financial impact not found"
        print(f"✓ Financial impact for {impact.soul_name}: ${impact.total_tributes:.2f}")
        
        # Test Firebase export
        firebase_data = financial_integration.export_tributes_for_firebase()
        print(f"✓ Firebase export ready: {len(firebase_data)} tributes")
        assert len(firebase_data) > 0, "No tributes exported"
        
    except Exception as e:
        print(f"✗ Souls-Financial Integration test failed: {e}")
        import traceback
        traceback.print_exc()
        raise


def main():
    """Run all integration tests"""
    print("=" * 60)
    print("Tiapma'atzu Platform Integration Test Suite (Hue Directory)")
    print("=" * 60)
    
    test_results = {
        'Souls Manager': test_souls_manager(),
        'CashingHouse System': test_cashinghouse(),
        'Souls-Financial Integration': test_souls_financial_integration(),
    }
    
    print("\n" + "=" * 60)
    print("Test Results Summary")
    print("=" * 60)
    
    for test_name, result in test_results.items():
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"{test_name}: {status}")
    
    passed_count = sum(1 for result in test_results.values() if result)
    total_count = len(test_results)
    
    print(f"\nTotal: {passed_count}/{total_count} tests passed")
    
    if passed_count == total_count:
        print("🎉 All tests passed successfully!")
        return 0
    else:
        print("⚠️  Some tests failed. Please review the errors above.")
        return 1


if __name__ == "__main__":
    exit(main())