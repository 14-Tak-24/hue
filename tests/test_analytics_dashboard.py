#!/usr/bin/env python3
"""
Test Analytics Dashboard
Tests the comprehensive analytics dashboard functionality
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
from src.modules.souls_financial_integration import SoulsFinancialIntegration

def test_analytics_dashboard():
    """Test the analytics dashboard functionality"""
    print("Testing Analytics Dashboard...")
    
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
    
    # Test platform usage analytics
    print("\n" + "="*60)
    print("Platform Usage Analytics")
    print("="*60)
    platform_analytics = dashboard.get_platform_usage_analytics()
    print(f"Total Platforms: {platform_analytics['total_platforms']}")
    print(f"Top Platform: {platform_analytics['top_platform']}")
    print(f"Most Active Platform: {platform_analytics['most_active_platform']}")
    
    print("\nPlatform Metrics:")
    for metric in platform_analytics['platform_metrics'][:5]:
        print(f"  {metric['platform']}: {metric['total_souls']} souls, {metric['active_souls']} active")
    
    # Test financial health analytics
    print("\n" + "="*60)
    print("Financial Health Analytics")
    print("="*60)
    financial_analytics = dashboard.get_financial_health_analytics(days=30)
    financial_metrics = financial_analytics['financial_metrics']
    
    print(f"Period: {financial_metrics['period']}")
    print(f"Total Revenue: ${financial_metrics['total_revenue']}")
    print(f"Total Expenses: ${financial_metrics['total_expenses']}")
    print(f"Net Profit: ${financial_metrics['net_profit']}")
    print(f"Profit Margin: {financial_metrics['profit_margin']}%")
    print(f"Active Tributes: {financial_metrics['active_tributes']}")
    
    print("\nHueMan-i-Terry Health:")
    hueman_health = financial_analytics['HueMan_i_Terry_health']
    print(f"  Health Score: {hueman_health['health_score']}/100")
    print(f"  Health Status: {hueman_health['health_status']}")
    print(f"  Active Souls: {hueman_health['active_souls']}/{hueman_health['total_souls']}")
    
    # Test soul performance analytics
    print("\n" + "="*60)
    print("Soul Performance Analytics")
    print("="*60)
    soul_analytics = dashboard.get_soul_performance_analytics()
    print(f"Total Souls Analyzed: {soul_analytics['total_souls_analyzed']}")
    
    print("\nActivity Distribution:")
    activity_dist = soul_analytics['activity_distribution']
    print(f"  High: {activity_dist['high']}")
    print(f"  Medium: {activity_dist['medium']}")
    print(f"  Low: {activity_dist['low']}")
    
    print("\nTop 5 Performers:")
    for performer in soul_analytics['top_performers']:
        print(f"  {performer['soul_name']}: ${performer['financial_impact']} impact, {performer['tribute_count']} tributes")
    
    # Test comprehensive dashboard
    print("\n" + "="*60)
    print("Comprehensive Dashboard")
    print("="*60)
    comprehensive = dashboard.get_comprehensive_dashboard()
    
    overall_health = comprehensive['overall_health_score']
    print(f"Overall Health Score: {overall_health['overall_score']}/100")
    print(f"Overall Status: {overall_health['status']}")
    
    print("\nComponent Scores:")
    for component, score in overall_health['component_scores'].items():
        print(f"  {component}: {score}/100")
    
    print("\nRecommendations:")
    for rec in overall_health['recommendations']:
        print(f"  • {rec}")
    
    # Export dashboard data
    print("\n" + "="*60)
    print("Exporting Dashboard Data")
    print("="*60)
    
    export_file = Path(__file__).parent / "dashboard_export.json"
    with open(export_file, 'w') as f:
        json.dump(comprehensive, f, indent=2, default=str)
    
    print(f"✓ Dashboard data exported to {export_file}")
    
    # Verify key assertions
    assert platform_analytics['total_platforms'] > 0, "No platforms found"
    assert soul_analytics['total_souls_analyzed'] > 0, "No souls analyzed"
    assert overall_health['overall_score'] >= 0, "Invalid health score"

if __name__ == "__main__":
    try:
        test_analytics_dashboard()
        print(f"\n🎉 Analytics dashboard test completed successfully!")
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)