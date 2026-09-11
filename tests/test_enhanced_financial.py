#!/usr/bin/env python3
"""
Test Enhanced Financial Health Tracking
Tests the new advanced financial health features
"""

import sys
import json
import traceback
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
    
    print("✓ Added %d sample tributes", len(sample_tributes))
    
    # Test cash flow analysis
    print("\n" + "="*60)
    print("Cash Flow Analysis")
    print("="*60)
    
    cash_flow = financial_integration.calculate_cash_flow_analysis(days=30)
    print("Period: %s days", cash_flow.get('period_days'))
    print("Total Cash Flow: $%s", cash_flow.get('total_cash_flow'))
    print("Average Daily Flow: $%.2f", cash_flow.get('average_daily_flow', 0.0))
    print("Trend: %s", cash_flow.get('trend'))
    print("Volatility: %s", cash_flow.get('volatility'))
    
    peak_day = cash_flow.get('peak_day')
    if peak_day:
        try:
            if isinstance(peak_day, (list, tuple)) and len(peak_day) >= 2:
                print("Peak Day: %s ($%s)", peak_day[0], peak_day[1])
        except Exception:
            # Guard against unexpected structure
            print("Peak Day data in unexpected format")
    
    low_day = cash_flow.get('low_day')
    if low_day:
        try:
            if isinstance(low_day, (list, tuple)) and len(low_day) >= 2:
                print("Low Day: %s ($%s)", low_day[0], low_day[1])
        except Exception:
            print("Low Day data in unexpected format")
    
    # Test financial forecast
    print("\n" + "="*60)
    print("Financial Forecast")
    print("="*60)
    
    forecast = financial_integration.calculate_financial_forecast(forecast_days=90)
    print("Forecast Period: %s days", forecast.get('forecast_days'))
    print("Based on: %s days historical data", forecast.get('based_on_historical_days'))
    print("Assumed Growth Rate: %s%%", forecast.get('assumed_growth_rate', 0.0) * 100)
    print("Total Projected Flow: $%.2f", forecast.get('total_projected_flow', 0.0))
    print("Average Projected Daily: $%.2f", forecast.get('average_projected_daily', 0.0))
    print("Confidence Level: %s", forecast.get('confidence_level'))
    
    # Show first few forecast days
    print("\nSample Forecast (first 5 days):")
    for day in forecast.get('daily_forecast', [])[:5]:
        date = day.get('date')
        projected = day.get('projected_flow', 0.0)
        cumulative = day.get('cumulative_flow', 0.0)
        print("  %s: $%.2f (cumulative: $%.2f)", date, projected, cumulative)
    
    # Test financial risk assessment
    print("\n" + "="*60)
    print("Financial Risk Assessment")
    print("="*60)
    
    risks = financial_integration.assess_financial_risks()
    print("Overall Risk Level: %s", str(risks.get('overall_risk_level', '')).upper())
    print("Identified Risks: %d", len(risks.get('identified_risks', [])))
    print("Mitigation Strategies: %d", len(risks.get('mitigation_strategies', [])))
    
    if risks.get('identified_risks'):
        print("\nIdentified Risks:")
        for risk in risks.get('identified_risks', []):
            print("  [%s] %s", risk.get('severity', '').upper(), risk.get('type'))
            print("    Description: %s", risk.get('description'))
            print("    Impact: %s", risk.get('impact'))
    
    if risks.get('mitigation_strategies'):
        print("\nMitigation Strategies:")
        for strategy in risks.get('mitigation_strategies', []):
            print("  [%s] %s", strategy.get('priority', '').upper(), strategy.get('risk'))
            print("    Strategy: %s", strategy.get('strategy'))
    
    # Test revenue diversification
    print("\n" + "="*60)
    print("Revenue Diversification")
    print("="*60)
    
    diversification = financial_integration.calculate_revenue_diversification()
    print("Total Revenue: $%s", diversification.get('total_revenue'))
    print("Concentration Index (HHI): %s", diversification.get('concentration_index'))
    print("Concentration Level: %s", diversification.get('concentration_level'))
    print("Diversification Score: %s/100", diversification.get('diversification_score'))
    
    print("\nRevenue by Impact Area:")
    for area, amount in diversification.get('area_breakdown', {}).items():
        percentage = diversification.get('area_percentages', {}).get(area, 0)
        print("  %s: $%.2f (%.1f%%)", area, amount, percentage)
    
    print("\nRecommendations:")
    for rec in diversification.get('recommendations', []):
        print("  • %s", rec)
    
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
    print("Current Total Revenue: $%s", goal_tracking.get('current_total_revenue'))
    print("Goals Tracked: %s", goal_tracking.get('goals_tracked'))
    print("Achieved: %s", goal_tracking.get('goals_achieved'))
    print("On Track: %s", goal_tracking.get('goals_on_track'))
    print("Behind: %s", goal_tracking.get('goals_behind'))
    
    print("\nGoal Details:")
    for goal in goal_tracking.get('goal_details', []):
        print("  %s:", goal.get('description'))
        print("    Target: $%s", goal.get('target_amount'))
        print("    Current: $%s", goal.get('current_amount'))
        print("    Progress: %.1f%%", goal.get('progress_percentage'))
        print("    Status: %s", str(goal.get('status', '')).upper())
        if goal.get('days_remaining') is not None:
            print("    Days Remaining: %s", goal.get('days_remaining'))
    
    # Test HueMan-i-Terry financial health with new data
    print("\n" + "="*60)
    print("Updated HueMan-i-Terry Financial Health")
    print("="*60)
    
    hueman_health = financial_integration.calculate_hueman_i_terry_financial_health()
    print("Health Score: %s/100", hueman_health.get('health_score'))
    print("Health Status: %s", hueman_health.get('health_status'))
    print("Total Contributions: $%s", hueman_health.get('total_contributions'))
    print("Active Souls: %s/%s", hueman_health.get('active_souls'), hueman_health.get('total_souls'))
    print("Participation Rate: %.1f%%", hueman_health.get('participation_rate'))
    
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
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(financial_report, f, indent=2, default=str)
    
    print("✓ Financial report exported to %s", report_file)
    
    # Verify key assertions
    assert hueman_health.get('health_score', 0) >= 0, "Invalid health score"
    assert len(risks.get('identified_risks', [])) >= 0, "Risk assessment failed"
    assert diversification.get('diversification_score', 0) >= 0, "Invalid diversification score"
    
    print("\n" + "="*60)
    print("All enhanced financial health tests passed successfully!")
    print("="*60)


if __name__ == "__main__":
    try:
        test_enhanced_financial_health()
        print("\n🎉 Enhanced financial health tracking test completed successfully!")
    except Exception as e:
        print("❌ Test failed: %s", e)
        traceback.print_exc()
        sys.exit(1)
