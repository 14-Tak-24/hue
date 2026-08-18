"""
Analytics Dashboard Module
Provides comprehensive analytics for financial and usage data
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from collections import defaultdict

from .souls_manager import SoulsManager
from .cashinghouse import CashingHouse
from .souls_financial_integration import SoulsFinancialIntegration
from .utils import Configuration, DateUtils


@dataclass
class PlatformUsageMetrics:
    """Platform usage metrics"""
    platform: str
    total_souls: int
    active_souls: int
    content_generated: int
    avg_engagement: float
    growth_rate: float


@dataclass
class FinancialHealthMetrics:
    """Financial health metrics"""
    period: str
    total_revenue: float
    total_expenses: float
    net_profit: float
    profit_margin: float
    active_tributes: int
    avg_tribute_amount: float
    revenue_by_source: Dict[str, float]
    expense_by_category: Dict[str, float]


@dataclass
class SoulPerformanceMetrics:
    """Individual soul performance metrics"""
    soul_id: str
    soul_name: str
    archetype: str
    content_count: int
    engagement_score: float
    financial_impact: float
    tribute_count: int
    activity_level: str


class AnalyticsDashboard:
    """
    Comprehensive analytics dashboard for the Tiapma'atzu platform.
    
    This class provides unified analytics across platform usage, financial health,
    and soul performance metrics. It integrates data from SoulsManager, CashingHouse,
    and SoulsFinancialIntegration to provide actionable insights.
    
    Attributes:
        souls_manager: SoulsManager instance for entity data
        cashinghouse: CashingHouse instance for financial data
        financial_integration: SoulsFinancialIntegration instance for tribute data
    """
    
    def __init__(
        self, 
        souls_manager: Optional[SoulsManager] = None,
        cashinghouse: Optional[CashingHouse] = None,
        financial_integration: Optional[SoulsFinancialIntegration] = None
    ):
        """
        Initialize analytics dashboard
        
        Args:
            souls_manager: SoulsManager instance
            cashinghouse: CashingHouse instance
            financial_integration: SoulsFinancialIntegration instance
        """
        self.souls_manager = souls_manager or SoulsManager()
        self.cashinghouse = cashinghouse or CashingHouse()
        self.financial_integration = financial_integration or SoulsFinancialIntegration(self.souls_manager)
        
    def get_platform_usage_analytics(self) -> Dict[str, Any]:
        """Get comprehensive platform usage analytics"""
        souls = self.souls_manager.get_all_souls()
        
        # Analyze platform usage
        platform_data: Dict[str, Dict[str, Any]] = defaultdict(lambda: {
            'souls': [],
            'total_souls': 0,
            'active_souls': 0,
            'content_count': 0,
            'engagement_scores': []
        })
        
        for soul in souls:
            for platform in soul.platforms:
                platform_data[platform]['souls'].append(soul)
                platform_data[platform]['total_souls'] += 1
                
                # Simulate activity metrics (in real app, this would come from actual usage data)
                if soul.rarity in ['Legendary', 'Rare']:
                    platform_data[platform]['active_souls'] += 1
                    platform_data[platform]['engagement_scores'].append(
                        0.8 if soul.rarity == 'Legendary' else 0.6
                    )
                    platform_data[platform]['content_count'] += 10 if soul.rarity == 'Legendary' else 5
        
        # Calculate metrics
        platform_metrics: List[PlatformUsageMetrics] = []
        for platform, data in platform_data.items():
            avg_engagement = sum(data['engagement_scores']) / len(data['engagement_scores']) if data['engagement_scores'] else 0.0
            activity_rate = (data['active_souls'] / data['total_souls']) * 100 if data['total_souls'] > 0 else 0
            
            metrics = PlatformUsageMetrics(
                platform=platform,
                total_souls=data['total_souls'],
                active_souls=data['active_souls'],
                content_generated=data['content_count'],
                avg_engagement=round(avg_engagement, 2),
                growth_rate=round(activity_rate * 0.1, 2)  # Simulated growth
            )
            platform_metrics.append(metrics)
        
        # Sort by total souls
        platform_metrics.sort(key=lambda x: x.total_souls, reverse=True)
        
        return {
            'timestamp': datetime.now().isoformat(),
            'total_platforms': len(platform_metrics),
            'platform_metrics': [asdict(m) for m in platform_metrics],
            'top_platform': platform_metrics[0].platform if platform_metrics else None,
            'most_active_platform': max(platform_metrics, key=lambda x: x.active_souls).platform if platform_metrics else None
        }
    
    def get_financial_health_analytics(self, days: int = Configuration.DEFAULT_ANALYTICS_DAYS) -> Dict[str, Any]:
        """
        Get financial health analytics for a specified period
        
        Args:
            days: Number of days to analyze
        """
        start_date, end_date = DateUtils.get_date_range(days)
        
        # Get financial summary from CashingHouse
        summary = self.cashinghouse.get_financial_summary(start_date, end_date)
        
        # Get HueMan-i-Terry health from financial integration
        HueMan_i_Terry_health = self.financial_integration.calculate_hueman_i_terry_financial_health()
        
        # Calculate additional metrics
        profit_margin = self._calculate_profit_margin(summary.total_income, summary.total_expenses)
        avg_tribute_amount = self._calculate_avg_tribute_amount(start_date, end_date)
        revenue_by_source = self._calculate_revenue_by_source(start_date, end_date)
        expense_by_category = self._calculate_expense_by_category(start_date, end_date)
        
        metrics = FinancialHealthMetrics(
            period=f"{days} days",
            total_revenue=round(summary.total_income, 2),
            total_expenses=round(summary.total_expenses, 2),
            net_profit=round(summary.total_income - summary.total_expenses, 2),
            profit_margin=round(profit_margin, 2),
            active_tributes=len(self.financial_integration.get_tributes_in_date_range(start_date, end_date)),
            avg_tribute_amount=round(avg_tribute_amount, 2),
            revenue_by_source=dict(revenue_by_source),
            expense_by_category=dict(expense_by_category)
        )
        
        return {
            'timestamp': datetime.now().isoformat(),
            'period_days': days,
            'financial_metrics': asdict(metrics),
            'HueMan_i_Terry_health': HueMan_i_Terry_health,
            'cash_flow_trend': summary.cash_flow_trend,
            'budget_status': self.cashinghouse.check_budget_status()
        }
    
    def _calculate_profit_margin(self, total_income: float, total_expenses: float) -> float:
        """Calculate profit margin percentage"""
        if total_income > 0:
            return ((total_income - total_expenses) / total_income) * 100
        return 0.0
    
    def _calculate_avg_tribute_amount(self, start_date: datetime, end_date: datetime) -> float:
        """Calculate average tribute amount for date range"""
        tributes = self.financial_integration.get_tributes_in_date_range(start_date, end_date)
        if tributes:
            monetary_tributes = [t.amount for t in tributes if t.amount]
            return sum(monetary_tributes) / len(monetary_tributes) if monetary_tributes else 0.0
        return 0.0
    
    def _calculate_revenue_by_source(self, start_date: datetime, end_date: datetime) -> Dict[str, float]:
        """Calculate revenue breakdown by source"""
        revenue_by_source = defaultdict(float)
        for tx in self.cashinghouse.get_transactions_in_date_range(start_date, end_date):
            if tx.transaction_type in ['income', 'tribute', 'investment']:
                source = tx.source_id or 'unknown'
                revenue_by_source[source] += tx.amount
        return revenue_by_source
    
    def _calculate_expense_by_category(self, start_date: datetime, end_date: datetime) -> Dict[str, float]:
        """Calculate expense breakdown by category"""
        expense_by_category = defaultdict(float)
        for tx in self.cashinghouse.get_transactions_in_date_range(start_date, end_date):
            if tx.transaction_type == 'expense':
                expense_by_category[tx.category] += tx.amount
        return expense_by_category
    
    def get_soul_performance_analytics(self) -> Dict[str, Any]:
        """Get individual soul performance analytics"""
        souls = self.souls_manager.get_all_souls()
        
        soul_metrics: List[SoulPerformanceMetrics] = []
        for soul in souls:
            # Get financial impact
            financial_impact = self.financial_integration.get_soul_financial_impact(soul.id)
            
            # Get tributes
            tributes = self.financial_integration.get_tributes_by_soul(soul.id)
            
            # Calculate performance metrics
            content_count = len(soul.platforms) * 5  # Simulated content count
            engagement_score = 0.7 if soul.rarity == 'Legendary' else 0.5 if soul.rarity == 'Rare' else 0.3
            
            # Determine activity level
            if len(tributes) > 5:
                activity_level = 'high'
            elif len(tributes) > 2:
                activity_level = 'medium'
            else:
                activity_level = 'low'
            
            metrics = SoulPerformanceMetrics(
                soul_id=soul.id,
                soul_name=soul.name,
                archetype=soul.archetype,
                content_count=content_count,
                engagement_score=round(engagement_score, 2),
                financial_impact=round(financial_impact.total_tributes if financial_impact else 0.0, 2),
                tribute_count=len(tributes),
                activity_level=activity_level
            )
            soul_metrics.append(metrics)
        
        # Sort by financial impact
        soul_metrics.sort(key=lambda x: x.financial_impact, reverse=True)
        
        return {
            'timestamp': datetime.now().isoformat(),
            'total_souls_analyzed': len(soul_metrics),
            'soul_metrics': [asdict(m) for m in soul_metrics],
            'top_performers': [asdict(m) for m in soul_metrics[:5]],
            'activity_distribution': {
                'high': len([m for m in soul_metrics if m.activity_level == 'high']),
                'medium': len([m for m in soul_metrics if m.activity_level == 'medium']),
                'low': len([m for m in soul_metrics if m.activity_level == 'low'])
            }
        }
    
    def get_detailed_soul_performance(self, soul_id: str) -> Dict[str, Any]:
        """
        Get detailed performance analytics for a specific soul
        
        Args:
            soul_id: ID of the soul to analyze
        """
        soul = self.souls_manager.get_soul_by_id(soul_id)
        if not soul:
            return {'error': f'Soul {soul_id} not found'}
        
        # Get financial impact
        financial_impact = self.financial_integration.get_soul_financial_impact(soul_id)
        
        # Get tributes
        tributes = self.financial_integration.get_tributes_by_soul(soul_id)
        
        # Calculate platform engagement
        platform_engagement = {}
        for platform in soul.platforms:
            # Simulate platform-specific engagement
            engagement = 0.8 if soul.rarity == 'Legendary' else 0.6 if soul.rarity == 'Rare' else 0.4
            platform_engagement[platform] = round(engagement, 2)
        
        # Calculate content performance
        content_performance = {
            'total_platforms': len(soul.platforms),
            'platform_diversity': len(set(soul.platforms)),
            'primary_platforms': soul.platforms[:3] if len(soul.platforms) >= 3 else soul.platforms,
            'engagement_avg': round(sum(platform_engagement.values()) / len(platform_engagement), 2) if platform_engagement else 0
        }
        
        # Calculate growth trajectory
        if tributes:
            tribute_dates = [t.timestamp for t in tributes]
            tribute_dates.sort()
            if len(tribute_dates) >= 2:
                days_between = (tribute_dates[-1] - tribute_dates[0]).days
                growth_rate = len(tributes) / max(days_between, 1) * 30  # Monthly rate
            else:
                growth_rate = 0
        else:
            growth_rate = 0
        
        # Calculate influence score
        influence_score = (
            (len(soul.platforms) * 10) +  # Platform presence
            (len(tributes) * 15) +  # Contribution activity
            (financial_impact.total_tributes if financial_impact else 0) * 0.1 +  # Financial impact
            (10 if soul.rarity == 'Legendary' else 5 if soul.rarity == 'Rare' else 2)  # Rarity bonus
        )
        
        return {
            'soul_id': soul_id,
            'soul_name': soul.name,
            'archetype': soul.archetype,
            'rarity': soul.rarity,
            'tier': soul.tier,
            'timestamp': datetime.now().isoformat(),
            'financial_impact': {
                'total_tributes': financial_impact.total_tributes if financial_impact else 0,
                'tribute_count': len(tributes),
                'impact_areas': financial_impact.impact_areas if financial_impact else {},
                'last_tribute_date': financial_impact.last_tribute_date.isoformat() if financial_impact else None
            },
            'platform_engagement': platform_engagement,
            'content_performance': content_performance,
            'growth_trajectory': {
                'monthly_growth_rate': round(growth_rate, 2),
                'tribute_frequency': len(tributes),
                'activity_span_days': days_between if tributes else 0
            },
            'influence_score': round(influence_score, 2),
            'recommendations': self._generate_soul_recommendations(soul, len(tributes), influence_score)
        }
    
    def _generate_soul_recommendations(self, soul: 'Soul', tribute_count: int, influence_score: float) -> List[str]:
        """Generate personalized recommendations for a soul"""
        recommendations = []
        
        if tribute_count == 0:
            recommendations.append("Consider making initial contributions to establish presence")
        elif tribute_count < 3:
            recommendations.append("Increase contribution frequency to build momentum")
        
        if len(soul.platforms) < 3:
            recommendations.append("Expand platform presence to increase reach")
        
        if influence_score < 50:
            recommendations.append("Focus on building influence through consistent engagement")
        
        if soul.rarity == 'Common' and influence_score > 70:
            recommendations.append("Consider evolving to higher rarity tier")
        
        if influence_score > 80:
            recommendations.append("Leverage high influence for mentorship opportunities")
        
        return recommendations
    
    def get_archetype_performance_analysis(self) -> Dict[str, Any]:
        """Analyze performance by archetype"""
        souls = self.souls_manager.get_all_souls()
        
        archetype_stats = {}
        for soul in souls:
            if soul.archetype not in archetype_stats:
                archetype_stats[soul.archetype] = {
                    'count': 0,
                    'total_financial_impact': 0,
                    'total_tributes': 0,
                    'avg_engagement': 0,
                    'platform_diversity': []
                }
            
            financial_impact = self.financial_integration.get_soul_financial_impact(soul.id)
            tributes = self.financial_integration.get_tributes_by_soul(soul.id)
            
            archetype_stats[soul.archetype]['count'] += 1
            archetype_stats[soul.archetype]['total_financial_impact'] += financial_impact.total_tributes if financial_impact else 0
            archetype_stats[soul.archetype]['total_tributes'] += len(tributes)
            archetype_stats[soul.archetype]['platform_diversity'].append(len(soul.platforms))
        
        # Calculate averages
        archetype_analysis = {}
        for archetype, stats in archetype_stats.items():
            archetype_analysis[archetype] = {
                'soul_count': stats['count'],
                'avg_financial_impact': round(stats['total_financial_impact'] / stats['count'], 2),
                'avg_tribute_count': round(stats['total_tributes'] / stats['count'], 2),
                'avg_platform_diversity': round(sum(stats['platform_diversity']) / len(stats['platform_diversity']), 2),
                'total_financial_impact': round(stats['total_financial_impact'], 2)
            }
        
        # Sort by total financial impact
        sorted_archetypes = dict(sorted(archetype_analysis.items(), key=lambda x: x[1]['total_financial_impact'], reverse=True))
        
        return {
            'timestamp': datetime.now().isoformat(),
            'total_archetypes': len(sorted_archetypes),
            'archetype_analysis': sorted_archetypes,
            'top_performing_archetype': max(sorted_archetypes.items(), key=lambda x: x[1]['total_financial_impact'])[0] if sorted_archetypes else None,
            'recommendations': self._generate_archetype_recommendations(sorted_archetypes)
        }
    
    def _generate_archetype_recommendations(self, archetype_analysis: Dict[str, Dict]) -> List[str]:
        """Generate recommendations based on archetype performance"""
        recommendations = []
        
        if not archetype_analysis:
            return recommendations
        
        # Find best and worst performing archetypes
        archetypes = list(archetype_analysis.keys())
        best_archetype = archetypes[0]
        worst_archetype = archetypes[-1]
        
        best_impact = archetype_analysis[best_archetype]['total_financial_impact']
        worst_impact = archetype_analysis[worst_archetype]['total_financial_impact']
        
        if best_impact > worst_impact * 2:
            recommendations.append(f"Consider strategies from {best_archetype} to improve {worst_archetype} performance")
        
        # Check for diversity
        avg_platform_diversity = sum(a['avg_platform_diversity'] for a in archetype_analysis.values()) / len(archetype_analysis)
        if avg_platform_diversity < 3:
            recommendations.append("Encourage greater platform diversity across all archetypes")
        
        return recommendations
    
    def get_soul_network_analysis(self) -> Dict[str, Any]:
        """Analyze soul connections and network patterns"""
        souls = self.souls_manager.get_all_souls()
        
        # Build network based on shared platforms
        network = {}
        for soul in souls:
            network[soul.id] = {
                'name': soul.name,
                'archetype': soul.archetype,
                'connections': [],
                'platforms': soul.platforms
            }
        
        # Find connections (shared platforms)
        for i, soul1 in enumerate(souls):
            for soul2 in souls[i+1:]:
                shared_platforms = set(soul1.platforms) & set(soul2.platforms)
                if shared_platforms:
                    connection_strength = len(shared_platforms)
                    network[soul1.id]['connections'].append({
                        'soul_id': soul2.id,
                        'soul_name': soul2.name,
                        'shared_platforms': list(shared_platforms),
                        'strength': connection_strength
                    })
                    network[soul2.id]['connections'].append({
                        'soul_id': soul1.id,
                        'soul_name': soul1.name,
                        'shared_platforms': list(shared_platforms),
                        'strength': connection_strength
                    })
        
        # Calculate network metrics
        total_connections = sum(len(node['connections']) for node in network.values())
        avg_connections = total_connections / len(network) if network else 0
        
        # Find most connected souls
        most_connected = sorted(network.items(), key=lambda x: len(x[1]['connections']), reverse=True)[:5]
        
        return {
            'timestamp': datetime.now().isoformat(),
            'total_souls': len(network),
            'total_connections': total_connections,
            'avg_connections_per_soul': round(avg_connections, 2),
            'network_density': round(total_connections / (len(network) * (len(network) - 1) / 2), 2) if len(network) > 1 else 0,
            'most_connected_souls': [
                {
                    'soul_id': soul_id,
                    'soul_name': data['name'],
                    'connection_count': len(data['connections'])
                }
                for soul_id, data in most_connected
            ],
            'isolated_souls': [
                soul_id for soul_id, data in network.items() if len(data['connections']) == 0
            ]
        }
    
    def get_comprehensive_dashboard(self) -> Dict[str, Any]:
        """Get comprehensive dashboard with all analytics"""
        return {
            'generated_at': datetime.now().isoformat(),
            'platform_usage': self.get_platform_usage_analytics(),
            'financial_health': self.get_financial_health_analytics(),
            'soul_performance': self.get_soul_performance_analytics(),
            'overall_health_score': self._calculate_overall_health_score()
        }
    
    def _calculate_overall_health_score(self) -> Dict[str, Any]:
        """Calculate overall platform health score"""
        # Get component scores
        platform_analytics = self.get_platform_usage_analytics()
        financial_analytics = self.get_financial_health_analytics()
        soul_analytics = self.get_soul_performance_analytics()
        
        # Platform health (40%)
        platform_score = min(100, (platform_analytics['total_platforms'] / 10) * 100)
        
        # Financial health (40%)
        HueMan_i_Terry_health = financial_analytics['HueMan_i_Terry_health']
        financial_score = HueMan_i_Terry_health['health_score']
        
        # Soul activity (20%)
        active_percentage = (
            soul_analytics['activity_distribution']['high'] + 
            soul_analytics['activity_distribution']['medium']
        ) / soul_analytics['total_souls_analyzed'] * 100 if soul_analytics['total_souls_analyzed'] > 0 else 0
        soul_score = active_percentage
        
        # Overall score
        overall_score = (platform_score * 0.4) + (financial_score * 0.4) + (soul_score * 0.2)
        
        # Determine status
        if overall_score >= 80:
            status = 'excellent'
        elif overall_score >= 60:
            status = 'good'
        elif overall_score >= 40:
            status = 'fair'
        else:
            status = 'needs_improvement'
        
        return {
            'overall_score': round(overall_score, 2),
            'status': status,
            'component_scores': {
                'platform': round(platform_score, 2),
                'financial': round(financial_score, 2),
                'soul_activity': round(soul_score, 2)
            },
            'recommendations': self._generate_health_recommendations(
                platform_score, financial_score, soul_score
            )
        }
    
    def _generate_health_recommendations(
        self, 
        platform_score: float, 
        financial_score: float, 
        soul_score: float
    ) -> List[str]:
        """Generate health improvement recommendations"""
        recommendations = []
        
        if platform_score < 60:
            recommendations.append("Consider expanding to additional platforms to increase reach")
        
        if financial_score < 60:
            recommendations.append("Review financial strategies and consider diversifying revenue streams")
        
        if soul_score < 60:
            recommendations.append("Encourage more soul activity through engagement initiatives")
        
        if platform_score >= 80 and financial_score >= 80 and soul_score >= 80:
            recommendations.append("Platform is performing excellently - consider expansion opportunities")
        
        return recommendations
    
    def get_trend_analysis(self, metric: str, days: int = 30) -> Dict[str, Any]:
        """
        Get trend analysis for a specific metric over time
        
        Args:
            metric: The metric to analyze (revenue, engagement, content, tributes)
            days: Number of days to analyze
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Generate time series data points
        trend_data = []
        current_date = start_date
        
        while current_date <= end_date:
            period_end = current_date + timedelta(days=7)  # Weekly data points
            
            # Calculate metric value for this period
            if metric == 'revenue':
                transactions = self.cashinghouse.get_transactions_in_date_range(current_date, period_end)
                value = sum(tx.amount for tx in transactions if tx.transaction_type in ['income', 'tribute'])
            elif metric == 'engagement':
                # Simulated engagement trend
                value = 0.6 + (current_date.timetuple().tm_yday % 10) * 0.02
            elif metric == 'content':
                souls = self.souls_manager.get_all_souls()
                value = len(souls) * 5  # Simulated content generation
            elif metric == 'tributes':
                tributes = self.financial_integration.get_tributes_in_date_range(current_date, period_end)
                value = len(tributes)
            else:
                value = 0
            
            trend_data.append({
                'date': current_date.isoformat(),
                'value': round(value, 2)
            })
            
            current_date = period_end
        
        # Calculate trend direction
        if len(trend_data) >= 2:
            first_value = trend_data[0]['value']
            last_value = trend_data[-1]['value']
            if last_value > first_value * 1.1:
                trend_direction = 'increasing'
            elif last_value < first_value * 0.9:
                trend_direction = 'decreasing'
            else:
                trend_direction = 'stable'
        else:
            trend_direction = 'unknown'
        
        return {
            'metric': metric,
            'period_days': days,
            'trend_direction': trend_direction,
            'data_points': trend_data,
            'current_value': trend_data[-1]['value'] if trend_data else 0,
            'average_value': round(sum(d['value'] for d in trend_data) / len(trend_data), 2) if trend_data else 0
        }
    
    def get_comparative_analytics(self, period1_days: int, period2_days: int) -> Dict[str, Any]:
        """
        Compare analytics between two time periods
        
        Args:
            period1_days: Number of days for period 1 (recent)
            period2_days: Number of days for period 2 (earlier)
        """
        # Get analytics for both periods
        recent_analytics = self.get_financial_health_analytics(period1_days)
        earlier_analytics = self.get_financial_health_analytics(period2_days)
        
        recent_metrics = recent_analytics['financial_metrics']
        earlier_metrics = earlier_analytics['financial_metrics']
        
        # Calculate changes
        revenue_change = self._calculate_percentage_change(
            earlier_metrics['total_revenue'], 
            recent_metrics['total_revenue']
        )
        expense_change = self._calculate_percentage_change(
            earlier_metrics['total_expenses'],
            recent_metrics['total_expenses']
        )
        profit_change = self._calculate_percentage_change(
            earlier_metrics['net_profit'],
            recent_metrics['net_profit']
        )
        tribute_change = self._calculate_percentage_change(
            earlier_metrics['active_tributes'],
            recent_metrics['active_tributes']
        )
        
        return {
            'period1': f'{period1_days} days (recent)',
            'period2': f'{period2_days} days (earlier)',
            'comparisons': {
                'revenue': {
                    'period1': recent_metrics['total_revenue'],
                    'period2': earlier_metrics['total_revenue'],
                    'change_percentage': revenue_change,
                    'trend': 'positive' if revenue_change > 0 else 'negative' if revenue_change < 0 else 'stable'
                },
                'expenses': {
                    'period1': recent_metrics['total_expenses'],
                    'period2': earlier_metrics['total_expenses'],
                    'change_percentage': expense_change,
                    'trend': 'positive' if expense_change > 0 else 'negative' if expense_change < 0 else 'stable'
                },
                'profit': {
                    'period1': recent_metrics['net_profit'],
                    'period2': earlier_metrics['net_profit'],
                    'change_percentage': profit_change,
                    'trend': 'positive' if profit_change > 0 else 'negative' if profit_change < 0 else 'stable'
                },
                'tributes': {
                    'period1': recent_metrics['active_tributes'],
                    'period2': earlier_metrics['active_tributes'],
                    'change_percentage': tribute_change,
                    'trend': 'positive' if tribute_change > 0 else 'negative' if tribute_change < 0 else 'stable'
                }
            }
        }
    
    def _calculate_percentage_change(self, old_value: float, new_value: float) -> float:
        """Calculate percentage change between two values"""
        if old_value == 0:
            return 0.0
        return round(((new_value - old_value) / old_value) * 100, 2)
    
    def get_anomaly_detection(self) -> Dict[str, Any]:
        """Detect anomalies in platform data"""
        anomalies = {
            'financial_anomalies': [],
            'activity_anomalies': [],
            'platform_anomalies': []
        }
        
        # Financial anomalies
        summary = self.cashinghouse.get_financial_summary()
        if summary.total_expenses > summary.total_income * 1.5:
            anomalies['financial_anomalies'].append({
                'type': 'high_expenses',
                'severity': 'high',
                'message': 'Expenses significantly exceed revenue',
                'value': f"${summary.total_expenses} vs ${summary.total_income} revenue"
            })
        
        # Activity anomalies
        soul_analytics = self.get_soul_performance_analytics()
        inactive_souls = [s for s in soul_analytics['soul_metrics'] if s['activity_level'] == 'low']
        if len(inactive_souls) > soul_analytics['total_souls_analyzed'] * 0.7:
            anomalies['activity_anomalies'].append({
                'type': 'low_activity',
                'severity': 'medium',
                'message': 'High percentage of inactive souls',
                'value': f"{len(inactive_souls)}/{soul_analytics['total_souls_analyzed']} souls inactive"
            })
        
        # Platform anomalies
        platform_analytics = self.get_platform_usage_analytics()
        for platform in platform_analytics['platform_metrics']:
            if platform['avg_engagement'] < 0.3:
                anomalies['platform_anomalies'].append({
                    'type': 'low_engagement',
                    'severity': 'low',
                    'message': f"Low engagement on {platform['platform']}",
                    'value': f"{platform['avg_engagement']} average engagement"
                })
        
        return {
            'timestamp': datetime.now().isoformat(),
            'total_anomalies': len(anomalies['financial_anomalies']) + len(anomalies['activity_anomalies']) + len(anomalies['platform_anomalies']),
            'anomalies': anomalies,
            'severity_summary': self._get_severity_summary(anomalies)
        }
    
    def _get_severity_summary(self, anomalies: Dict[str, List[Dict]]) -> Dict[str, int]:
        """Get summary of anomaly severities"""
        severity_counts = {'high': 0, 'medium': 0, 'low': 0}
        
        for category in anomalies.values():
            for anomaly in category:
                severity_counts[anomaly['severity']] += 1
        
        return severity_counts
    
    def get_custom_date_range_analytics(self, start_date: str, end_date: str) -> Dict[str, Any]:
        """
        Get analytics for a custom date range
        
        Args:
            start_date: Start date in ISO format (YYYY-MM-DD)
            end_date: End date in ISO format (YYYY-MM-DD)
        """
        try:
            start = datetime.fromisoformat(start_date)
            end = datetime.fromisoformat(end_date)
        except ValueError:
            raise ValueError("Invalid date format. Use YYYY-MM-DD format.")
        
        if start > end:
            raise ValueError("Start date must be before end date")
        
        # Calculate days in range
        days = (end - start).days + 1
        
        # Get financial analytics for custom range
        summary = self.cashinghouse.get_financial_summary(start, end)
        tributes = self.financial_integration.get_tributes_in_date_range(start, end)
        
        # Get transactions for the period
        period_transactions = self.cashinghouse.get_transactions_in_date_range(start, end)
        
        return {
            'date_range': {
                'start_date': start_date,
                'end_date': end_date,
                'total_days': days
            },
            'financial_summary': {
                'total_income': round(summary.total_income, 2),
                'total_expenses': round(summary.total_expenses, 2),
                'net_profit': round(summary.total_income - summary.total_expenses, 2),
                'transaction_count': len(period_transactions)
            },
            'tribute_summary': {
                'total_tributes': len(tributes),
                'total_amount': round(sum(t.amount for t in tributes if t.amount), 2),
                'unique_souls': len(set(t.soul_id for t in tributes))
            },
            'generated_at': datetime.now().isoformat()
        }
    
    def export_analytics_report(self, format: str = 'json', output_path: Optional[str] = None) -> str:
        """
        Export comprehensive analytics report
        
        Args:
            format: Export format ('json', 'csv')
            output_path: Optional custom output path
            
        Returns:
            Path to the exported file
        """
        import json
        import csv
        from pathlib import Path
        
        comprehensive_data = self.get_comprehensive_dashboard()
        
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"analytics_report_{timestamp}.{format}"
        
        output_file = Path(output_path)
        
        if format == 'json':
            with open(output_file, 'w') as f:
                json.dump(comprehensive_data, f, indent=2, default=str)
        elif format == 'csv':
            # Flatten the data for CSV export
            with open(output_file, 'w', newline='') as f:
                writer = csv.writer(f)
                
                # Write header
                writer.writerow(['Category', 'Metric', 'Value'])
                
                # Write platform usage data
                for platform in comprehensive_data['platform_usage']['platform_metrics']:
                    writer.writerow(['Platform', f"{platform['platform']} - Total Souls", platform['total_souls']])
                    writer.writerow(['Platform', f"{platform['platform']} - Active Souls", platform['active_souls']])
                    writer.writerow(['Platform', f"{platform['platform']} - Engagement", platform['avg_engagement']])
                
                # Write financial data
                financial = comprehensive_data['financial_health']['financial_metrics']
                writer.writerow(['Financial', 'Total Revenue', financial['total_revenue']])
                writer.writerow(['Financial', 'Total Expenses', financial['total_expenses']])
                writer.writerow(['Financial', 'Net Profit', financial['net_profit']])
                writer.writerow(['Financial', 'Profit Margin', financial['profit_margin']])
                
                # Write soul performance data
                for soul in comprehensive_data['soul_performance']['top_performers']:
                    writer.writerow(['Soul', f"{soul['soul_name']} - Financial Impact", soul['financial_impact']])
                    writer.writerow(['Soul', f"{soul['soul_name']} - Tribute Count", soul['tribute_count']])
                    writer.writerow(['Soul', f"{soul['soul_name']} - Engagement Score", soul['engagement_score']])
                    writer.writerow(['Soul', f"{soul['soul_name']} - Activity Level", soul['activity_level']])
        else:
            raise ValueError(f"Unsupported format: {format}")
        
        return str(output_file.absolute())