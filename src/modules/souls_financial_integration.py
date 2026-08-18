"""
Souls-Financial Integration Module
Integrates soul entities with the CashingHouse financial tracking system
"""

import json
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum

from .souls_manager import SoulsManager, Soul


class TributeType(Enum):
    """Types of tributes/contributions"""
    MONETARY = "monetary"
    SERVICE = "service"
    RESOURCE = "resource"
    INTELLECTUAL = "intellectual"
    COMMUNITY = "community"


@dataclass
class Tribute:
    """Individual tribute/contribution record"""
    tribute_id: str
    soul_id: str
    soul_name: str
    tribute_type: str
    amount: Optional[float]
    description: str
    impact_area: str
    timestamp: datetime
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class FinancialImpact:
    """Financial impact summary for a soul"""
    soul_id: str
    soul_name: str
    total_tributes: float
    tribute_count: int
    impact_areas: Dict[str, float]
    last_tribute_date: datetime
    tribute_impact_statement: str
    trends: Dict[str, Any]


class SoulsFinancialIntegration:
    """
    Integration between souls and financial tracking systems.
    
    This class bridges the soul entities with the financial system, tracking tributes,
    calculating financial impact, and providing comprehensive financial analytics
    for individual souls and the overall HueMan-i-Terry.
    
    Attributes:
        souls_manager: SoulsManager instance for entity data
        tributes: List of all tribute records
        financial_impacts: Dictionary of financial impact summaries by soul ID
    """
    
    def __init__(self, souls_manager: Optional[SoulsManager] = None):
        """
        Initialize the souls-financial integration
        
        Args:
            souls_manager: SoulsManager instance (creates default if not provided)
        """
        self.souls_manager = souls_manager or SoulsManager()
        self.tributes: List[Tribute] = []
        self.financial_impacts: Dict[str, FinancialImpact] = {}
        
        # Initialize financial impacts from souls data
        self._initialize_financial_impacts()
    
    def _initialize_financial_impacts(self):
        """Initialize financial impact summaries from souls data"""
        for soul in self.souls_manager.get_all_souls():
            impact = FinancialImpact(
                soul_id=soul.id,
                soul_name=soul.name,
                total_tributes=0.0,
                tribute_count=0,
                impact_areas={},
                last_tribute_date=datetime.now(),
                tribute_impact_statement=soul.tribute_impact,
                trends={'monthly': [], 'quarterly': []}
            )
            self.financial_impacts[soul.id] = impact
    
    def record_tribute(
        self, 
        soul_id: str, 
        tribute_type: TributeType,
        amount: Optional[float],
        description: str,
        impact_area: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Tribute:
        """
        Record a tribute/contribution for a soul
        
        Args:
            soul_id: ID of the soul making the tribute
            tribute_type: Type of tribute
            amount: Monetary amount (if applicable)
            description: Description of the tribute
            impact_area: Area where the tribute has impact
            metadata: Additional metadata
            
        Returns:
            Tribute record
        """
        soul = self.souls_manager.get_soul_by_id(soul_id)
        if not soul:
            raise ValueError(f"Soul with ID {soul_id} not found")
        
        # Create tribute record
        tribute = Tribute(
            tribute_id=f"tribute_{datetime.now().timestamp()}",
            soul_id=soul_id,
            soul_name=soul.name,
            tribute_type=tribute_type.value,
            amount=amount,
            description=description,
            impact_area=impact_area,
            timestamp=datetime.now(),
            metadata=metadata or {}
        )
        
        # Store tribute
        self.tributes.append(tribute)
        
        # Update financial impact
        self._update_financial_impact(tribute)
        
        return tribute
    
    def _update_financial_impact(self, tribute: Tribute):
        """Update financial impact summary for a soul"""
        if tribute.soul_id not in self.financial_impacts:
            return
        
        impact = self.financial_impacts[tribute.soul_id]
        
        # Update totals
        if tribute.amount:
            impact.total_tributes += tribute.amount
        impact.tribute_count += 1
        impact.last_tribute_date = tribute.timestamp
        
        # Update impact areas
        if tribute.impact_area not in impact.impact_areas:
            impact.impact_areas[tribute.impact_area] = 0.0
        if tribute.amount:
            impact.impact_areas[tribute.impact_area] += tribute.amount
        
        # Update trends
        self._update_trends(impact, tribute)
    
    def _update_trends(self, impact: FinancialImpact, tribute: Tribute):
        """Update trend data for financial impact"""
        # Add to monthly trends
        month_key = tribute.timestamp.strftime("%Y-%m")
        if not any(t['month'] == month_key for t in impact.trends['monthly']):
            impact.trends['monthly'].append({
                'month': month_key,
                'amount': tribute.amount or 0,
                'count': 1
            })
        else:
            for trend in impact.trends['monthly']:
                if trend['month'] == month_key:
                    trend['amount'] += tribute.amount or 0
                    trend['count'] += 1
                    break
        
        # Keep only last 12 months
        impact.trends['monthly'] = impact.trends['monthly'][-12:]
    
    def get_soul_financial_impact(self, soul_id: str) -> Optional[FinancialImpact]:
        """Get financial impact summary for a specific soul"""
        return self.financial_impacts.get(soul_id)
    
    def get_all_financial_impacts(self) -> Dict[str, FinancialImpact]:
        """Get financial impact summaries for all souls"""
        return self.financial_impacts
    
    def get_tributes_by_soul(self, soul_id: str) -> List[Tribute]:
        """Get all tributes for a specific soul"""
        return [t for t in self.tributes if t.soul_id == soul_id]
    
    def get_tributes_by_type(self, tribute_type: TributeType) -> List[Tribute]:
        """Get all tributes of a specific type"""
        return [t for t in self.tributes if t.tribute_type == tribute_type.value]
    
    def get_tributes_by_impact_area(self, impact_area: str) -> List[Tribute]:
        """Get all tributes for a specific impact area"""
        return [t for t in self.tributes if t.impact_area == impact_area]
    
    def get_tributes_in_date_range(
        self, 
        start_date: datetime, 
        end_date: datetime
    ) -> List[Tribute]:
        """Get tributes within a specific date range"""
        return [
            t for t in self.tributes 
            if start_date <= t.timestamp <= end_date
        ]
    
    def get_financial_summary(self) -> Dict[str, Any]:
        """Get overall financial summary"""
        if not self.tributes:
            return {
                'total_tributes': 0,
                'total_amount': 0.0,
                'by_type': {},
                'by_impact_area': {},
                'top_contributors': []
            }
        
        # Calculate totals
        total_amount = sum(t.amount for t in self.tributes if t.amount)
        
        # By type
        by_type = {}
        for tribute in self.tributes:
            if tribute.tribute_type not in by_type:
                by_type[tribute.tribute_type] = {'count': 0, 'amount': 0.0}
            by_type[tribute.tribute_type]['count'] += 1
            if tribute.amount:
                by_type[tribute.tribute_type]['amount'] += tribute.amount
        
        # By impact area
        by_impact_area = {}
        for tribute in self.tributes:
            if tribute.impact_area not in by_impact_area:
                by_impact_area[tribute.impact_area] = {'count': 0, 'amount': 0.0}
            by_impact_area[tribute.impact_area]['count'] += 1
            if tribute.amount:
                by_impact_area[tribute.impact_area]['amount'] += tribute.amount
        
        # Top contributors
        soul_totals = {}
        for tribute in self.tributes:
            if tribute.soul_id not in soul_totals:
                soul_totals[tribute.soul_id] = {
                    'name': tribute.soul_name,
                    'count': 0,
                    'amount': 0.0
                }
            soul_totals[tribute.soul_id]['count'] += 1
            if tribute.amount:
                soul_totals[tribute.soul_id]['amount'] += tribute.amount
        
        top_contributors = sorted(
            soul_totals.values(), 
            key=lambda x: x['amount'], 
            reverse=True
        )[:10]
        
        return {
            'total_tributes': len(self.tributes),
            'total_amount': total_amount,
            'by_type': by_type,
            'by_impact_area': by_impact_area,
            'top_contributors': top_contributors,
            'active_souls': len(soul_totals)
        }
    
    def generate_soul_financial_report(self, soul_id: str) -> Dict[str, Any]:
        """Generate comprehensive financial report for a soul"""
        soul = self.souls_manager.get_soul_by_id(soul_id)
        if not soul:
            raise ValueError(f"Soul with ID {soul_id} not found")
        
        impact = self.get_soul_financial_impact(soul_id)
        soul_tributes = self.get_tributes_by_soul(soul_id)
        
        # Calculate monthly trends
        monthly_data = {}
        for tribute in soul_tributes:
            month_key = tribute.timestamp.strftime("%Y-%m")
            if month_key not in monthly_data:
                monthly_data[month_key] = {'count': 0, 'amount': 0.0}
            monthly_data[month_key]['count'] += 1
            if tribute.amount:
                monthly_data[month_key]['amount'] += tribute.amount
        
        # Recent activity
        recent_tributes = sorted(soul_tributes, key=lambda t: t.timestamp, reverse=True)[:10]
        
        return {
            'soul': {
                'id': soul.id,
                'name': soul.name,
                'archetype': soul.archetype,
                'tribute_impact_statement': soul.tribute_impact
            },
            'financial_impact': asdict(impact) if impact else None,
            'tribute_details': [asdict(t) for t in recent_tributes],
            'monthly_summary': monthly_data,
            'impact_areas_analysis': impact.impact_areas if impact else {},
            'recommendations': self._generate_financial_recommendations(soul, impact)
        }
    
    def _generate_financial_recommendations(
        self, 
        soul: Soul, 
        impact: Optional[FinancialImpact]
    ) -> List[str]:
        """Generate financial recommendations based on soul's impact"""
        recommendations = []
        
        if not impact or impact.tribute_count == 0:
            recommendations.append(f"Consider initiating tribute activities to support {soul.tribute_impact_statement}")
            return recommendations
        
        # Analyze tribute frequency
        if impact.tribute_count < 5:
            recommendations.append("Increase tribute frequency to maximize impact")
        
        # Analyze amount trends
        if impact.trends['monthly']:
            recent_month = impact.trends['monthly'][-1]
            if len(impact.trends['monthly']) > 1:
                previous_month = impact.trends['monthly'][-2]
                if recent_month['amount'] < previous_month['amount']:
                    recommendations.append("Recent tribute amounts have decreased - consider reviewing contribution strategy")
        
        # Analyze impact area diversity
        if len(impact.impact_areas) < 2:
            recommendations.append("Diversify impact areas to increase overall effectiveness")
        
        # Archetype-specific recommendations
        if 'financial' in soul.archetype.lower() or 'capitalist' in soul.archetype.lower():
            recommendations.append("Consider leveraging financial expertise for maximum impact")
        elif 'healer' in soul.archetype.lower() or 'community' in soul.archetype.lower():
            recommendations.append("Focus on community-building tributes for enhanced effectiveness")
        
        return recommendations
    
    def sync_with_cashinghouse(self, cashinghouse_data: Dict[str, Any]) -> bool:
        """
        Sync tribute data with CashingHouse financial system
        
        Args:
            cashinghouse_data: Financial data from CashingHouse system
            
        Returns:
            Success status
        """
        try:
            # Process CashingHouse data and create tribute records
            for transaction in cashinghouse_data.get('transactions', []):
                # Map CashingHouse transactions to tributes
                if 'soul_id' in transaction:
                    self.record_tribute(
                        soul_id=transaction['soul_id'],
                        tribute_type=TributeType.MONETARY,
                        amount=transaction.get('amount'),
                        description=transaction.get('description', 'Financial contribution'),
                        impact_area=transaction.get('category', 'general'),
                        metadata={'source': 'cashinghouse', 'transaction_id': transaction.get('id')}
                    )
            
            return True
        except Exception as e:
            print(f"Error syncing with CashingHouse: {e}")
            return False
    
    def export_tributes_for_firebase(self) -> List[Dict[str, Any]]:
        """Export tributes in Firebase-compatible format"""
        firebase_records = []
        
        for tribute in self.tributes:
            record = {
                'soulId': tribute.soul_id,
                'soulName': tribute.soul_name,
                'tributeType': tribute.tribute_type,
                'amount': tribute.amount,
                'description': tribute.description,
                'impactArea': tribute.impact_area,
                'timestamp': tribute.timestamp.isoformat(),
                'metadata': tribute.metadata
            }
            firebase_records.append(record)
        
        return firebase_records
    
    def calculate_hueman_i_terry_financial_health(self) -> Dict[str, Any]:
        """Calculate overall financial health of the HueMan-i-Terry"""
        if not self.financial_impacts:
            return {'status': 'insufficient_data'}
        
        # Calculate metrics
        total_contributions = sum(impact.total_tributes for impact in self.financial_impacts.values())
        total_tribute_count = sum(impact.tribute_count for impact in self.financial_impacts.values())
        active_souls = len([impact for impact in self.financial_impacts.values() if impact.tribute_count > 0])
        
        # Calculate average metrics
        avg_contribution = total_contributions / active_souls if active_souls > 0 else 0
        avg_tribute_count = total_tribute_count / active_souls if active_souls > 0 else 0
        
        # Calculate diversity (impact areas)
        all_impact_areas = set()
        for impact in self.financial_impacts.values():
            all_impact_areas.update(impact.impact_areas.keys())
        
        # Calculate health score
        health_score = 0
        if active_souls > 0:
            health_score += (active_souls / len(self.financial_impacts)) * 40  # Participation
            health_score += min(avg_contribution / 1000, 1) * 30  # Contribution level
            health_score += min(len(all_impact_areas) / 10, 1) * 30  # Diversity
        
        health_status = 'excellent' if health_score >= 80 else 'good' if health_score >= 60 else 'fair' if health_score >= 40 else 'needs_improvement'
        
        return {
            'health_score': round(health_score, 2),
            'health_status': health_status,
            'total_contributions': total_contributions,
            'total_tribute_count': total_tribute_count,
            'active_souls': active_souls,
            'total_souls': len(self.financial_impacts),
            'participation_rate': round(active_souls / len(self.financial_impacts) * 100, 2),
            'average_contribution': round(avg_contribution, 2),
            'average_tribute_count': round(avg_tribute_count, 2),
            'impact_diversity': len(all_impact_areas),
            'impact_areas': sorted(list(all_impact_areas)),
            'recommendations': self._generate_hueman_i_terry_health_recommendations(health_score, active_souls, len(all_impact_areas))
        }
    
    def _generate_hueman_i_terry_health_recommendations(
        self,
        health_score: float,
        active_souls: int,
        impact_diversity: int
    ) -> List[str]:
        """Generate recommendations for improving HueMan-i-Terry financial health"""
        recommendations = []
        
        if health_score < 60:
            recommendations.append("Overall HueMan-i-Terry financial health needs improvement")
        
        participation_rate = active_souls / len(self.financial_impacts)
        if participation_rate < 0.7:
            recommendations.append("Encourage more souls to participate in tribute activities")
        
        if impact_diversity < 5:
            recommendations.append("Increase diversity of impact areas for broader community benefit")
        
        if health_score >= 80:
            recommendations.append("HueMan-i-Terry financial health is excellent - consider expansion opportunities")
        
        return recommendations
    
    def calculate_cash_flow_analysis(self, days: int = 30) -> Dict[str, Any]:
        """
        Calculate detailed cash flow analysis
        
        Args:
            days: Number of days to analyze
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Filter tributes by date range
        recent_tributes = [
            t for t in self.tributes 
            if start_date <= t.timestamp <= end_date and t.amount is not None
        ]
        
        # Calculate cash flow metrics
        daily_cash_flow = {}
        for tribute in recent_tributes:
            date_key = tribute.timestamp.strftime("%Y-%m-%d")
            if date_key not in daily_cash_flow:
                daily_cash_flow[date_key] = 0.0
            daily_cash_flow[date_key] += tribute.amount
        
        # Calculate trends
        dates = sorted(daily_cash_flow.keys())
        if len(dates) >= 2:
            first_week_avg = sum(daily_cash_flow.get(d, 0) for d in dates[:7]) / 7
            last_week_avg = sum(daily_cash_flow.get(d, 0) for d in dates[-7:]) / 7
            trend = "increasing" if last_week_avg > first_week_avg * 1.1 else "decreasing" if last_week_avg < first_week_avg * 0.9 else "stable"
        else:
            trend = "insufficient_data"
        
        # Calculate volatility
        if daily_cash_flow:
            values = list(daily_cash_flow.values())
            avg = sum(values) / len(values)
            variance = sum((x - avg) ** 2 for x in values) / len(values)
            volatility = (variance ** 0.5) / avg if avg > 0 else 0
        else:
            volatility = 0
        
        return {
            'period_days': days,
            'total_cash_flow': sum(daily_cash_flow.values()),
            'average_daily_flow': sum(daily_cash_flow.values()) / len(daily_cash_flow) if daily_cash_flow else 0,
            'daily_breakdown': daily_cash_flow,
            'trend': trend,
            'volatility': round(volatility, 2),
            'peak_day': max(daily_cash_flow.items(), key=lambda x: x[1]) if daily_cash_flow else None,
            'low_day': min(daily_cash_flow.items(), key=lambda x: x[1]) if daily_cash_flow else None
        }
    
    def calculate_financial_forecast(self, forecast_days: int = 90) -> Dict[str, Any]:
        """
        Generate financial forecast based on historical data
        
        Args:
            forecast_days: Number of days to forecast
        """
        # Get historical data
        historical_days = 90
        historical_analysis = self.calculate_cash_flow_analysis(historical_days)
        
        avg_daily_flow = historical_analysis['average_daily_flow']
        trend = historical_analysis['trend']
        
        # Calculate growth rate
        if trend == "increasing":
            growth_rate = 0.05  # 5% growth
        elif trend == "decreasing":
            growth_rate = -0.03  # 3% decline
        else:
            growth_rate = 0.01  # 1% stable growth
        
        # Generate forecast
        forecast = []
        current_date = datetime.now()
        cumulative_flow = 0
        
        for day in range(forecast_days):
            forecast_date = current_date + timedelta(days=day)
            # Apply growth rate progressively
            day_growth = 1 + (growth_rate * (day / 30))
            projected_flow = avg_daily_flow * day_growth
            cumulative_flow += projected_flow
            
            forecast.append({
                'date': forecast_date.strftime("%Y-%m-%d"),
                'projected_flow': round(projected_flow, 2),
                'cumulative_flow': round(cumulative_flow, 2)
            })
        
        return {
            'forecast_days': forecast_days,
            'based_on_historical_days': historical_days,
            'assumed_growth_rate': growth_rate,
            'total_projected_flow': round(cumulative_flow, 2),
            'average_projected_daily': round(cumulative_flow / forecast_days, 2),
            'daily_forecast': forecast,
            'confidence_level': 'medium' if trend != 'insufficient_data' else 'low'
        }
    
    def assess_financial_risks(self) -> Dict[str, Any]:
        """Assess financial risks and provide mitigation strategies"""
        risks = {
            'timestamp': datetime.now().isoformat(),
            'overall_risk_level': 'low',
            'identified_risks': [],
            'mitigation_strategies': []
        }
        
        # Risk 1: Low participation rate
        health = self.calculate_hueman_i_terry_financial_health()
        participation_rate = health['participation_rate']
        
        if participation_rate < 50:
            risks['identified_risks'].append({
                'type': 'low_participation',
                'severity': 'high',
                'description': f'Only {participation_rate}% of souls are actively contributing',
                'impact': 'Reduced financial stability and community engagement'
            })
            risks['mitigation_strategies'].append({
                'risk': 'low_participation',
                'strategy': 'Implement engagement campaigns and incentive programs',
                'priority': 'high'
            })
        elif participation_rate < 70:
            risks['identified_risks'].append({
                'type': 'moderate_participation',
                'severity': 'medium',
                'description': f'{participation_rate}% participation rate could be improved',
                'impact': 'Suboptimal community resource utilization'
            })
        
        # Risk 2: Revenue concentration
        impact_areas = health['impact_areas']
        if len(impact_areas) < 3:
            risks['identified_risks'].append({
                'type': 'revenue_concentration',
                'severity': 'medium',
                'description': f'Limited revenue diversity across {len(impact_areas)} impact areas',
                'impact': 'Vulnerability to sector-specific disruptions'
            })
            risks['mitigation_strategies'].append({
                'risk': 'revenue_concentration',
                'strategy': 'Diversify tribute impact areas and revenue streams',
                'priority': 'medium'
            })
        
        # Risk 3: Cash flow volatility
        cash_flow = self.calculate_cash_flow_analysis()
        if cash_flow['volatility'] > 0.5:
            risks['identified_risks'].append({
                'type': 'high_volatility',
                'severity': 'medium',
                'description': f'High cash flow volatility ({cash_flow["volatility"]})',
                'impact': 'Unpredictable financial planning challenges'
            })
            risks['mitigation_strategies'].append({
                'risk': 'high_volatility',
                'strategy': 'Build reserve funds and smooth contribution patterns',
                'priority': 'medium'
            })
        
        # Calculate overall risk level
        high_severity = len([r for r in risks['identified_risks'] if r['severity'] == 'high'])
        medium_severity = len([r for r in risks['identified_risks'] if r['severity'] == 'medium'])
        
        if high_severity > 0:
            risks['overall_risk_level'] = 'high'
        elif medium_severity > 1:
            risks['overall_risk_level'] = 'medium'
        else:
            risks['overall_risk_level'] = 'low'
        
        return risks
    
    def calculate_revenue_diversification(self) -> Dict[str, Any]:
        """Calculate revenue diversification metrics"""
        # Group tributes by impact area
        area_revenue = {}
        total_revenue = 0
        
        for tribute in self.tributes:
            if tribute.amount is not None:
                if tribute.impact_area not in area_revenue:
                    area_revenue[tribute.impact_area] = 0.0
                area_revenue[tribute.impact_area] += tribute.amount
                total_revenue += tribute.amount
        
        # Calculate concentration
        if total_revenue > 0:
            area_percentages = {area: (amount / total_revenue) * 100 for area, amount in area_revenue.items()}
            
            # Calculate Herfindahl-Hirschman Index (HHI) for concentration
            hhi = sum((pct / 100) ** 2 for pct in area_percentages.values())
            
            # Interpret HHI
            if hhi < 0.15:
                concentration_level = 'low'
                diversification_score = 90
            elif hhi < 0.25:
                concentration_level = 'moderate'
                diversification_score = 70
            else:
                concentration_level = 'high'
                diversification_score = 40
        else:
            area_percentages = {}
            hhi = 0
            concentration_level = 'no_data'
            diversification_score = 0
        
        return {
            'total_revenue': total_revenue,
            'area_breakdown': area_revenue,
            'area_percentages': area_percentages,
            'concentration_index': round(hhi, 4),
            'concentration_level': concentration_level,
            'diversification_score': diversification_score,
            'recommendations': self._generate_diversification_recommendations(concentration_level, len(area_revenue))
        }
    
    def _generate_diversification_recommendations(self, concentration_level: str, area_count: int) -> List[str]:
        """Generate recommendations for improving revenue diversification"""
        recommendations = []
        
        if concentration_level == 'high':
            recommendations.append("Critical: Reduce dependency on single revenue source")
            recommendations.append("Develop alternative impact areas and revenue streams")
        elif concentration_level == 'moderate':
            recommendations.append("Consider expanding into additional impact areas")
            recommendations.append("Balance revenue distribution across sectors")
        
        if area_count < 3:
            recommendations.append("Increase number of active impact areas")
        elif area_count < 5:
            recommendations.append("Further diversification could improve stability")
        
        if concentration_level == 'low':
            recommendations.append("Excellent diversification - maintain current balance")
        
        return recommendations
    
    def track_financial_goals(self, goals: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Track progress towards financial goals
        
        Args:
            goals: List of financial goals with target amounts and deadlines
        """
        health = self.calculate_hueman_i_terry_financial_health()
        current_revenue = health['total_contributions']
        
        goal_tracking = []
        for goal in goals:
            goal_id = goal.get('id', 'unknown')
            target_amount = goal.get('target_amount', 0)
            deadline = goal.get('deadline')
            description = goal.get('description', 'No description')
            
            # Calculate progress
            progress = (current_revenue / target_amount * 100) if target_amount > 0 else 0
            
            # Calculate time remaining
            if deadline:
                deadline_date = datetime.fromisoformat(deadline)
                days_remaining = (deadline_date - datetime.now()).days
                on_track = progress >= (100 - days_remaining)  # Simple on-track calculation
            else:
                days_remaining = None
                on_track = progress >= 50
            
            goal_tracking.append({
                'goal_id': goal_id,
                'description': description,
                'target_amount': target_amount,
                'current_amount': current_revenue,
                'progress_percentage': round(progress, 2),
                'remaining_amount': max(0, target_amount - current_revenue),
                'deadline': deadline,
                'days_remaining': days_remaining,
                'on_track': on_track,
                'status': 'achieved' if progress >= 100 else 'behind' if not on_track else 'on_track'
            })
        
        return {
            'tracking_date': datetime.now().isoformat(),
            'current_total_revenue': current_revenue,
            'goals_tracked': len(goal_tracking),
            'goals_achieved': len([g for g in goal_tracking if g['status'] == 'achieved']),
            'goals_on_track': len([g for g in goal_tracking if g['status'] == 'on_track']),
            'goals_behind': len([g for g in goal_tracking if g['status'] == 'behind']),
            'goal_details': goal_tracking
        }