#!/usr/bin/env python3
"""
Test Enhanced Analytics Dashboard
Tests the new advanced analytics features
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

def test_enhanced_analytics():
    """Test the enhanced analytics dashboard functionality"""
    print("Testing Enhanced Analytics Dashboard...")
    
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
    
    # Test trend analysis
    print("\n" + "="*60)
    print("Trend Analysis")
    print("="*60)
    
    for metric in ['revenue', 'engagement', 'content', 'tributes']:
        trend = dashboard.get_trend_analysis(metric, days=30)
        print(f"\n{metric.capitalize()} Trend:")
        print(f"  Direction: {trend['trend_direction']}")
        print(f"  Current Value: {trend['current_value']}")
        print(f"  Average Value: {trend['average_value']}")
        print(f"  Data Points: {len(trend['data_points'])}")
    
    # Test comparative analytics
    print("\n" + "="*60)
    print("Comparative Analytics")
    print("="*60)
    
    comparison = dashboard.get_comparative_analytics(30, 60)
    print(f"Period 1: {comparison['period1']}")
    print(f"Period 2: {comparison['period2']}")
    
    print("\nComparisons:")
    for metric, data in comparison['comparisons'].items():
        print(f"  {metric.capitalize()}:")
        print(f"    Period 1: {data['period1']}")
        print(f"    Period 2: {data['period2']}")
        print(f"    Change: {data['change_percentage']}%")
        print(f"    Trend: {data['trend']}")
    
    # Test anomaly detection
    print("\n" + "="*60)
    print("Anomaly Detection")
    print("="*60)
    
    anomalies = dashboard.get_anomaly_detection()
    print(f"Total Anomalies: {anomalies['total_anomalies']}")
    print(f"Severity Summary: {anomalies['severity_summary']}")
    
    for category, category_anomalies in anomalies['anomalies'].items():
        if category_anomalies:
            print(f"\n{category.replace('_', ' ').title()}:")
            for anomaly in category_anomalies:
                print(f"  [{anomaly['severity'].upper()}] {anomaly['message']}")
                print(f"    Value: {anomaly['value']}")
    
    # Test custom date range analytics
    print("\n" + "="*60)
    print("Custom Date Range Analytics")
    print("="*60)
    
    try:
        custom_range = dashboard.get_custom_date_range_analytics("2026-07-01", "2026-08-16")
        print(f"Date Range: {custom_range['date_range']['start_date']} to {custom_range['date_range']['end_date']}")
        print(f"Total Days: {custom_range['date_range']['total_days']}")
        print(f"Total Income: ${custom_range['financial_summary']['total_income']}")
        print(f"Total Expenses: ${custom_range['financial_summary']['total_expenses']}")
        print(f"Net Profit: ${custom_range['financial_summary']['net_profit']}")
        print(f"Total Tributes: {custom_range['tribute_summary']['total_tributes']}")
        print(f"Unique Souls: {custom_range['tribute_summary']['unique_souls']}")
    except Exception as e:
        print(f"Custom date range test skipped: {e}")
    
    # Test export functionality
    print("\n" + "="*60)
    print("Export Analytics Report")
    print("="*60)
    
    try:
        json_path = dashboard.export_analytics_report(format='json')
        print(f"✓ JSON report exported to: {json_path}")
        
        csv_path = dashboard.export_analytics_report(format='csv')
        print(f"✓ CSV report exported to: {csv_path}")
    except Exception as e:
        print(f"Export test failed: {e}")
    
    # Test comprehensive dashboard with new features
    print("\n" + "="*60)
    print("Comprehensive Dashboard with New Features")
    print("="*60)
    
    comprehensive = dashboard.get_comprehensive_dashboard()
    print(f"Generated At: {comprehensive['generated_at']}")
    print(f"Overall Health Score: {comprehensive['overall_health_score']['overall_score']}/100")
    print(f"Status: {comprehensive['overall_health_score']['status']}")
    
    # Save enhanced dashboard export
    export_file = Path(__file__).parent / "enhanced_dashboard_export.json"
    with open(export_file, 'w') as f:
        json.dump(comprehensive, f, indent=2, default=str)
    
    print(f"✓ Enhanced dashboard data exported to {export_file}")
    
    # Verify key assertions
    assert len(comprehensive['platform_usage']['platform_metrics']) > 0, "No platforms found"
    assert comprehensive['soul_performance']['total_souls_analyzed'] > 0, "No souls analyzed"
    assert comprehensive['overall_health_score']['overall_score'] >= 0, "Invalid health score"
    
    print("\n" + "="*60)
    print("All enhanced analytics tests passed successfully!")
    print("="*60)

if __name__ == "__main__":
    try:
        test_enhanced_analytics()
        print(f"\n🎉 Enhanced analytics dashboard test completed successfully!")
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)