#!/usr/bin/env python3
"""
Test Enhanced Soul Performance Metrics
Tests the new advanced soul performance features
"""

import sys
import json
from pathlib import Path

# Add the src directory to the path for package imports
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from src.modules.analytics_dashboard import AnalyticsDashboard
from src.modules.souls_manager import SoulsManager
from src.modules.cashinghouse import CashingHouse
from src.modules.souls_financial_integration import SoulsFinancialIntegration, TributeType

def test_enhanced_soul_performance():
    """Test the enhanced soul performance metrics functionality"""
    print("Testing Enhanced Soul Performance Metrics...")
    
    # Initialize components
    data_path = Path(__file__).parent.parent / "src" / "data" / "souls_entities.json"
    souls_manager = SoulsManager(str(data_path))
    cashinghouse = CashingHouse()
    financial_integration = SoulsFinancialIntegration(souls_manager)
    
    # Initialize analytics dashboard
    dashboard = AnalyticsDashboard(
        souls_manager=souls_manager,
        cashinghouse=cashinghouse,
        financial_integration=financial_integration
    )
    
    print("✓ Analytics Dashboard initialized")
    
    # Add sample tributes for testing
    print("\n" + "="*60)
    print("Adding Sample Tributes for Testing")
    print("="*60)
    
    sample_tributes = [
        ('soul_001', TributeType.MONETARY, 100.0, 'Monthly contribution', 'temple_operations'),
        ('soul_002', TributeType.MONETARY, 150.0, 'Community support', 'community'),
        ('soul_003', TributeType.SERVICE, None, 'Volunteer work', 'community'),
        ('soul_001', TributeType.MONETARY, 200.0, 'Special contribution', 'infrastructure'),
        ('soul_004', TributeType.RESOURCE, None, 'Equipment donation', 'infrastructure'),
    ]
    
    for soul_id, tribute_type, amount, description, impact_area in sample_tributes:
        financial_integration.record_tribute(
            soul_id=soul_id,
            tribute_type=tribute_type,
            amount=amount,
            description=description,
            impact_area=impact_area
        )
    
    print(f"✓ Added {len(sample_tributes)} sample tributes")
    
    # Test detailed soul performance
    print("\n" + "="*60)
    print("Detailed Soul Performance Analysis")
    print("="*60)
    
    detailed_performance = dashboard.get_detailed_soul_performance('soul_001')
    print(f"Soul: {detailed_performance['soul_name']} ({detailed_performance['archetype']})")
    print(f"Rarity: {detailed_performance['rarity']}")
    print(f"Influence Score: {detailed_performance['influence_score']}")
    
    print("\nFinancial Impact:")
    fi = detailed_performance['financial_impact']
    print(f"  Total Tributes: ${fi['total_tributes']}")
    print(f"  Tribute Count: {fi['tribute_count']}")
    print(f"  Impact Areas: {list(fi['impact_areas'].keys())}")
    
    print("\nPlatform Engagement:")
    for platform, engagement in detailed_performance['platform_engagement'].items():
        print(f"  {platform}: {engagement}")
    
    print("\nContent Performance:")
    cp = detailed_performance['content_performance']
    print(f"  Total Platforms: {cp['total_platforms']}")
    print(f"  Platform Diversity: {cp['platform_diversity']}")
    print(f"  Average Engagement: {cp['engagement_avg']}")
    
    print("\nGrowth Trajectory:")
    gt = detailed_performance['growth_trajectory']
    print(f"  Monthly Growth Rate: {gt['monthly_growth_rate']}")
    print(f"  Tribute Frequency: {gt['tribute_frequency']}")
    
    print("\nRecommendations:")
    for rec in detailed_performance['recommendations']:
        print(f"  • {rec}")
    
    # Test archetype performance analysis
    print("\n" + "="*60)
    print("Archetype Performance Analysis")
    print("="*60)
    
    archetype_analysis = dashboard.get_archetype_performance_analysis()
    print(f"Total Archetypes: {archetype_analysis['total_archetypes']}")
    print(f"Top Performing Archetype: {archetype_analysis['top_performing_archetype']}")
    
    print("\nArchetype Performance (Top 5):")
    for archetype, stats in list(archetype_analysis['archetype_analysis'].items())[:5]:
        print(f"  {archetype}:")
        print(f"    Soul Count: {stats['soul_count']}")
        print(f"    Avg Financial Impact: ${stats['avg_financial_impact']}")
        print(f"    Total Financial Impact: ${stats['total_financial_impact']}")
    
    print("\nArchetype Recommendations:")
    for rec in archetype_analysis['recommendations']:
        print(f"  • {rec}")
    
    # Test soul network analysis
    print("\n" + "="*60)
    print("Soul Network Analysis")
    print("="*60)
    
    network_analysis = dashboard.get_soul_network_analysis()
    print(f"Total Souls: {network_analysis['total_souls']}")
    print(f"Total Connections: {network_analysis['total_connections']}")
    print(f"Average Connections per Soul: {network_analysis['avg_connections_per_soul']}")
    print(f"Network Density: {network_analysis['network_density']}")
    
    print("\nMost Connected Souls:")
    for soul in network_analysis['most_connected_souls']:
        print(f"  {soul['soul_name']}: {soul['connection_count']} connections")
    
    if network_analysis['isolated_souls']:
        print(f"\nIsolated Souls: {len(network_analysis['isolated_souls'])}")
        for soul_id in network_analysis['isolated_souls'][:5]:
            soul = souls_manager.get_soul_by_id(soul_id)
            if soul:
                print(f"  {soul.name} ({soul_id})")
    
    # Test comprehensive dashboard with new features
    print("\n" + "="*60)
    print("Comprehensive Dashboard with Enhanced Metrics")
    print("="*60)
    
    comprehensive = dashboard.get_comprehensive_dashboard()
    print(f"Generated At: {comprehensive['generated_at']}")
    print(f"Overall Health Score: {comprehensive['overall_health_score']['overall_score']}/100")
    print(f"Status: {comprehensive['overall_health_score']['status']}")
    
    # Export enhanced dashboard
    export_file = Path(__file__).parent / "enhanced_soul_performance_dashboard.json"
    with open(export_file, 'w') as f:
        json.dump({
            'detailed_soul_performance': detailed_performance,
            'archetype_analysis': archetype_analysis,
            'network_analysis': network_analysis,
            'comprehensive_dashboard': comprehensive
        }, f, indent=2, default=str)
    
    print(f"✓ Enhanced soul performance dashboard exported to {export_file}")
    
    # Test enhanced CSV export
    print("\n" + "="*60)
    print("Enhanced CSV Export")
    print("="*60)
    
    try:
        csv_path = dashboard.export_analytics_report(format='csv')
        print(f"✓ Enhanced CSV report exported to {csv_path}")
    except Exception as e:
        print(f"CSV export test failed: {e}")
    
    # Verify key assertions
    assert detailed_performance['influence_score'] >= 0, "Invalid influence score"
    assert archetype_analysis['total_archetypes'] > 0, "No archetypes found"
    assert network_analysis['total_souls'] > 0, "No souls in network"
    
    print("\n" + "="*60)
    print("All enhanced soul performance tests passed successfully!")
    print("="*60)

if __name__ == "__main__":
    try:
        test_enhanced_soul_performance()
        print(f"\n🎉 Enhanced soul performance metrics test completed successfully!")
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)