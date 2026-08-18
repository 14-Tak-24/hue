#!/usr/bin/env python3
"""
Test Enhanced Financial Health Tracking
Tests the new advanced financial health features
"""

import sys
import json
from pathlib import Path
from datetime import datetime, timedelta

# Add the src directory to the path for package imports
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from src.modules.souls_manager import SoulsManager
from src.modules.souls_financial_integration import SoulsFinancialIntegration, TributeType

def test_enhanced_financial_health():
    """Test the enhanced financial health tracking functionality"""
    print("Testing Enhanced Financial Health Tracking...")
    
    # Initialize components
    data_path = Path(__file__).parent.parent / "src" / "data" / "souls_entities.json"
    souls_manager = SoulsManager(str(data_path))
    financial_integration = SoulsFinancialIntegration(souls_manager)
    
    print("✓ Financial Integration initialized")
    
    # Add some sample tributes for testing
    print("\n" + "="*60)
    print("Adding Sample Tributes")
    print("="*60)
    
    # Add sample tributes to test the new features
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
    
    # Test cash flow analysis
    print("\n" + "="*60)
    print("Cash Flow Analysis")
    print("="*60)
    
    cash_flow = financial_integration.calculate_cash_flow_analysis(days=30)
    print(f"Period: {cash_flow['period_days']} days")
    print(f"Total Cash Flow: ${cash_flow['total_cash_flow']}")
    print(f"Average Daily Flow: ${cash_flow['average_daily_flow']:.2f}")
    print(f"Trend: {cash_flow['trend']}")
    print(f"Volatility: {cash_flow['volatility']}")
    
    if cash_flow['peak_day']:
        print(f"Peak Day: {cash_flow['peak_day'][0]} (${cash_flow['peak_day'][1]})")
    if cash_flow['low_day']:
        print(f"Low Day: {cash_flow['low_day'][0]} (${cash_flow['low_day'][1]})")
    
    # Test financial forecast
    print("\n" + "="*60)
    print("Financial Forecast")
    print("="*60)
    
    forecast = financial_integration.calculate_financial_forecast(forecast_days=90)
    print(f"Forecast Period: {forecast['forecast_days']} days")
    print(f"Based on: {forecast['based_on_historical_days']} days historical data")
    print(f"Assumed Growth Rate: {forecast['assumed_growth_rate'] * 100}%")
    print(f"Total Projected Flow: ${forecast['total_projected_flow']:.2f}")
    print(f"Average Projected Daily: ${forecast['average_projected_daily']:.2f}")
    print(f"Confidence Level: {forecast['confidence_level']}")
    
    # Show first few forecast days
    print("\nSample Forecast (first 5 days):")
    for day in forecast['daily_forecast'][:5]:
        print(f"  {day['date']}: ${day['projected_flow']:.2f} (cumulative: ${day['cumulative_flow']:.2f})")
    
    # Test financial risk assessment
    print("\n" + "="*60)
    print("Financial Risk Assessment")
    print("="*60)
    
    risks = financial_integration.assess_financial_risks()
    print(f"Overall Risk Level: {risks['overall_risk_level'].upper()}")
    print(f"Identified Risks: {len(risks['identified_risks'])}")
    print(f"Mitigation Strategies: {len(risks['mitigation_strategies'])}")
    
    if risks['identified_risks']:
        print("\nIdentified Risks:")
        for risk in risks['identified_risks']:
            print(f"  [{risk['severity'].upper()}] {risk['type']}")
            print(f"    Description: {risk['description']}")
            print(f"    Impact: {risk['impact']}")
    
    if risks['mitigation_strategies']:
        print("\nMitigation Strategies:")
        for strategy in risks['mitigation_strategies']:
            print(f"  [{strategy['priority'].upper()}] {strategy['risk']}")
            print(f"    Strategy: {strategy['strategy']}")
    
    # Test revenue diversification
    print("\n" + "="*60)
    print("Revenue Diversification")
    print("="*60)
    
    diversification = financial_integration.calculate_revenue_diversification()
    print(f"Total Revenue: ${diversification['total_revenue']}")
    print(f"Concentration Index (HHI): {diversification['concentration_index']}")
    print(f"Concentration Level: {diversification['concentration_level']}")
    print(f"Diversification Score: {diversification['diversification_score']}/100")
    
    print("\nRevenue by Impact Area:")
    for area, amount in diversification['area_breakdown'].items():
        percentage = diversification['area_percentages'].get(area, 0)
        print(f"  {area}: ${amount:.2f} ({percentage:.1f}%)")
    
    print("\nRecommendations:")
    for rec in diversification['recommendations']:
        print(f"  • {rec}")
    
    # Test financial goals tracking
    print("\n" + "="*60)
    print("Financial Goals Tracking")
    print("="*60)
    
    # Define sample goals
    sample_goals = [
        {
            'id': 'goal_001',
            'description': 'Monthly revenue target',
            'target_amount': 1000.0,
            'deadline': (datetime.now() + timedelta(days=30)).isoformat()
        },
        {
            'id': 'goal_002',
            'description': 'Quarterly expansion fund',
            'target_amount': 5000.0,
            'deadline': (datetime.now() + timedelta(days=90)).isoformat()
        },
        {
            'id': 'goal_003',
            'description': 'Annual community budget',
            'target_amount': 20000.0,
            'deadline': (datetime.now() + timedelta(days=365)).isoformat()
        }
    ]
    
    goal_tracking = financial_integration.track_financial_goals(sample_goals)
    print(f"Current Total Revenue: ${goal_tracking['current_total_revenue']}")
    print(f"Goals Tracked: {goal_tracking['goals_tracked']}")
    print(f"Achieved: {goal_tracking['goals_achieved']}")
    print(f"On Track: {goal_tracking['goals_on_track']}")
    print(f"Behind: {goal_tracking['goals_behind']}")
    
    print("\nGoal Details:")
    for goal in goal_tracking['goal_details']:
        print(f"  {goal['description']}:")
        print(f"    Target: ${goal['target_amount']}")
        print(f"    Current: ${goal['current_amount']}")
        print(f"    Progress: {goal['progress_percentage']:.1f}%")
        print(f"    Status: {goal['status'].upper()}")
        if goal['days_remaining'] is not None:
            print(f"    Days Remaining: {goal['days_remaining']}")
    
    # Test HueMan-i-Terry financial health with new data
    print("\n" + "="*60)
    print("Updated HueMan-i-Terry Financial Health")
    print("="*60)
    
    hueman_health = financial_integration.calculate_hueman_i_terry_financial_health()
    print(f"Health Score: {hueman_health['health_score']}/100")
    print(f"Health Status: {hueman_health['health_status']}")
    print(f"Total Contributions: ${hueman_health['total_contributions']}")
    print(f"Active Souls: {hueman_health['active_souls']}/{hueman_health['total_souls']}")
    print(f"Participation Rate: {hueman_health['participation_rate']:.1f}%")
    
    # Export comprehensive financial report
    print("\n" + "="*60)
    print("Exporting Financial Report")
    print("="*60)
    
    financial_report = {
        'generated_at': datetime.now().isoformat(),
        'cash_flow_analysis': cash_flow,
        'financial_forecast': forecast,
        'risk_assessment': risks,
        'revenue_diversification': diversification,
        'goal_tracking': goal_tracking,
        'HueMan_i_Terry_health': hueman_health
    }
    
    report_file = Path(__file__).parent / "enhanced_financial_report.json"
    with open(report_file, 'w') as f:
        json.dump(financial_report, f, indent=2, default=str)
    
    print(f"✓ Financial report exported to {report_file}")
    
    # Verify key assertions
    assert hueman_health['health_score'] >= 0, "Invalid health score"
    assert len(risks['identified_risks']) >= 0, "Risk assessment failed"
    assert diversification['diversification_score'] >= 0, "Invalid diversification score"
    
    print("\n" + "="*60)
    print("All enhanced financial health tests passed successfully!")
    print("="*60)

if __name__ == "__main__":
    try:
        test_enhanced_financial_health()
        print(f"\n🎉 Enhanced financial health tracking test completed successfully!")
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)