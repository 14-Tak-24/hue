#!/usr/bin/env python3
"""
Tiapma'atzu Platform CLI
Command-line interface for common platform operations
"""

import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Optional

# Add the src directory to the path for package imports
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from modules.souls_manager import SoulsManager
from modules.cashinghouse import CashingHouse, TransactionType, TransactionCategory
from modules.souls_financial_integration import SoulsFinancialIntegration, TributeType
from modules.analytics_dashboard import AnalyticsDashboard


class TiapmaatzuCLI:
    """Command-line interface for Tiapma'atzu platform operations"""
    
    def __init__(self):
        self.souls_manager = None
        self.cashinghouse = None
        self.financial_integration = None
        self.analytics_dashboard = None
        
    def initialize_souls_manager(self, data_path: Optional[str] = None):
        """Initialize the souls manager"""
        if data_path is None:
            data_path = Path(__file__).parent / "src" / "data" / "souls_entities.json"
        
        self.souls_manager = SoulsManager(str(data_path))
        print(f"✓ Souls Manager initialized with {len(self.souls_manager.get_all_souls())} souls")
        
    def initialize_cashinghouse(self, data_path: Optional[str] = None):
        """Initialize the CashingHouse system"""
        if data_path is None:
            data_path = Path(__file__).parent / "data" / "cashinghouse.json"
        
        self.cashinghouse = CashingHouse(str(data_path))
        print(f"✓ CashingHouse initialized with {len(self.cashinghouse.transactions)} transactions")
        
    def initialize_financial_integration(self):
        """Initialize the financial integration"""
        if not self.souls_manager:
            self.initialize_souls_manager()
        
        self.financial_integration = SoulsFinancialIntegration(self.souls_manager)
        print(f"✓ Financial Integration initialized")
    
    def initialize_analytics_dashboard(self):
        """Initialize the analytics dashboard"""
        if not self.souls_manager:
            self.initialize_souls_manager()
        if not self.cashinghouse:
            self.initialize_cashinghouse()
        if not self.financial_integration:
            self.initialize_financial_integration()
        
        self.analytics_dashboard = AnalyticsDashboard(
            souls_manager=self.souls_manager,
            cashinghouse=self.cashinghouse,
            financial_integration=self.financial_integration
        )
        print(f"✓ Analytics Dashboard initialized")
    
    def list_souls(self, filters: dict = None):
        """List souls with optional filtering"""
        if not self.souls_manager:
            self.initialize_souls_manager()
        
        souls = self.souls_manager.get_all_souls()
        
        # Apply filters
        if filters:
            if 'rarity' in filters:
                souls = [s for s in souls if s.rarity == filters['rarity']]
            if 'tier' in filters:
                souls = [s for s in souls if s.tier == filters['tier']]
            if 'platform' in filters:
                souls = [s for s in souls if filters['platform'] in s.platforms]
            if 'archetype' in filters:
                souls = [s for s in souls if s.archetype == filters['archetype']]
        
        print(f"\n{'ID':<10} {'Name':<20} {'Archetype':<20} {'Rarity':<10} {'Tier':<6}")
        print("-" * 66)
        
        for soul in souls:
            print(f"{soul.id:<10} {soul.name:<20} {soul.archetype:<20} {soul.rarity:<10} {soul.tier:<6}")
        
        print(f"\nTotal: {len(souls)} souls")
        
    def show_soul_details(self, soul_id: str):
        """Show detailed information about a specific soul"""
        if not self.souls_manager:
            self.initialize_souls_manager()
        
        soul = self.souls_manager.get_soul_by_id(soul_id)
        if not soul:
            soul = self.souls_manager.get_soul_by_name(soul_id)
        
        if not soul:
            print(f"❌ Soul not found: {soul_id}")
            return
        
        print(f"\n{'='*60}")
        print(f"Soul Details: {soul.name}")
        print(f"{'='*60}")
        print(f"ID: {soul.id}")
        print(f"Archetype: {soul.archetype}")
        print(f"Gender: {soul.gender}")
        print(f"Rarity: {soul.rarity}")
        print(f"Tier: {soul.tier}")
        print(f"\nBio:")
        print(f"  {soul.bio}")
        print(f"\nVoice: {soul.voice}")
        print(f"Sensory: {soul.sensory}")
        print(f"\nHooks:")
        for hook in soul.hooks:
            print(f"  • {hook}")
        print(f"\nDesires:")
        for desire in soul.desires:
            print(f"  • {desire}")
        print(f"\nKinks:")
        for kink in soul.kinks:
            print(f"  • {kink}")
        print(f"\nPlatforms: {', '.join(soul.platforms)}")
        print(f"Tribute Impact: {soul.tribute_impact}")
        print(f"Shadow Practice: {soul.shadow_practice}")
        print(f"Contact: {soul.email}")
        print(f"Image: {soul.image}")
        
    def show_statistics(self):
        """Show platform statistics"""
        if not self.souls_manager:
            self.initialize_souls_manager()
        
        stats = self.souls_manager.get_statistics()
        
        print(f"\n{'='*60}")
        print("Platform Statistics")
        print(f"{'='*60}")
        print(f"Total Souls: {stats['total_souls']}")
        
        print(f"\nRarity Distribution:")
        for rarity, count in stats['rarity_distribution'].items():
            print(f"  {rarity}: {count}")
        
        print(f"\nGender Distribution:")
        for gender, count in stats['gender_distribution'].items():
            print(f"  {gender}: {count}")
        
        print(f"\nArchetype Distribution:")
        for archetype, count in stats['archetype_distribution'].items():
            print(f"  {archetype}: {count}")
        
        print(f"\nPlatform Distribution:")
        platform_items = list(stats['platform_distribution'].items())[:10]
        for platform, count in platform_items:
            print(f"  {platform}: {count}")
        
    def show_compatibility(self, soul_id: str, threshold: float = 50.0):
        """Show compatible souls for a given soul"""
        if not self.souls_manager:
            self.initialize_souls_manager()
        
        target_soul = self.souls_manager.get_soul_by_id(soul_id)
        if not target_soul:
            target_soul = self.souls_manager.get_soul_by_name(soul_id)
        
        if not target_soul:
            print(f"❌ Soul not found: {soul_id}")
            return
        
        compatible = self.souls_manager.find_compatible_souls(target_soul.id, threshold)
        
        print(f"\n{'='*60}")
        print(f"Compatible Souls for {target_soul.name} (Threshold: {threshold}%)")
        print(f"{'='*60}")
        
        if not compatible:
            print(f"No compatible souls found above {threshold}% threshold")
            return
        
        print(f"\n{'Name':<20} {'Archetype':<20} {'Score':<10}")
        print("-" * 50)
        
        for soul, score in compatible:
            print(f"{soul.name:<20} {soul.archetype:<20} {score:<10.1f}")
        
        print(f"\nTotal: {len(compatible)} compatible souls")
    
    def add_platform_to_soul(self, soul_id: str, platform: str):
        """Add a platform to a soul"""
        if not self.souls_manager:
            self.initialize_souls_manager()
        
        try:
            success = self.souls_manager.add_platform_to_soul(soul_id, platform)
            if success:
                print(f"✓ Added platform '{platform}' to soul {soul_id}")
                self.souls_manager.save_souls_data()
            else:
                print(f"⚠️  Platform '{platform}' already exists for soul {soul_id}")
        except ValueError as e:
            print(f"❌ Error: {e}")
    
    def remove_platform_from_soul(self, soul_id: str, platform: str):
        """Remove a platform from a soul"""
        if not self.souls_manager:
            self.initialize_souls_manager()
        
        try:
            success = self.souls_manager.remove_platform_from_soul(soul_id, platform)
            if success:
                print(f"✓ Removed platform '{platform}' from soul {soul_id}")
                self.souls_manager.save_souls_data()
            else:
                print(f"⚠️  Platform '{platform}' not found for soul {soul_id}")
        except ValueError as e:
            print(f"❌ Error: {e}")
    
    def create_soul_interaction(self, soul_id1: str, soul_id2: str, interaction_type: str):
        """Create and analyze a soul interaction"""
        if not self.souls_manager:
            self.initialize_souls_manager()
        
        try:
            interaction = self.souls_manager.create_soul_interaction(soul_id1, soul_id2, interaction_type)
            
            print(f"\n{'='*60}")
            print("Soul Interaction Analysis")
            print(f"{'='*60}")
            print(f"Souls: {interaction['soul1']} + {interaction['soul2']}")
            print(f"Compatibility Score: {interaction['compatibility_score']}/100")
            print(f"Interaction Type: {interaction['interaction_type']}")
            print(f"Shared Platforms: {', '.join(interaction['shared_platforms'])}")
            print(f"Total Reach: {interaction['total_reach']} platforms")
            
            print(f"\nSuggestions:")
            for suggestion in interaction['suggestions']:
                print(f"  • {suggestion}")
            
            print(f"\nRecommended Content Types:")
            for content_type in interaction['recommended_content_types']:
                print(f"  • {content_type}")
                
        except ValueError as e:
            print(f"❌ Error: {e}")
    
    def show_trending_platforms(self, limit: int = 5):
        """Show trending platforms"""
        if not self.souls_manager:
            self.initialize_souls_manager()
        
        trending = self.souls_manager.get_trending_platforms(limit)
        
        print(f"\n{'='*60}")
        print(f"Top {limit} Trending Platforms")
        print(f"{'='*60}")
        
        print(f"\n{'Platform':<15} {'Total Souls':<12} {'Legendary':<10} {'Rare':<8} {'Score':<8}")
        print("-" * 60)
        
        for platform_data in trending:
            print(f"{platform_data['platform']:<15} {platform_data['total_souls']:<12} {platform_data['legendary_souls']:<10} {platform_data['rare_souls']:<8} {platform_data['activity_score']:<8}")
        
    def show_data_integrity(self):
        """Show data integrity report"""
        if not self.souls_manager:
            self.initialize_souls_manager()
        
        report = self.souls_manager.get_data_integrity_report()
        
        print(f"\n{'='*60}")
        print("Data Integrity Report")
        print(f"{'='*60}")
        print(f"Health Score: {report['health_score']}/100")
        print(f"Health Status: {report['health_status'].upper()}")
        print(f"Total Souls: {report['total_souls']}")
        print(f"Validation Errors: {len(report['validation_errors'])}")
        print(f"Warnings: {len(report['warnings'])}")
        
        if report['validation_errors']:
            print(f"\n❌ Validation Errors:")
            for error in report['validation_errors']:
                print(f"  • {error['soul_name']}: {', '.join(error['errors'])}")
        
        if report['warnings']:
            print(f"\n⚠️  Warnings:")
            for warning in report['warnings']:
                print(f"  • {warning['message']}")
                
    def list_backups(self):
        """List available backups"""
        if not self.souls_manager:
            self.initialize_souls_manager()
        
        backups = self.souls_manager.list_backups()
        
        print(f"\n{'='*60}")
        print("Available Backups")
        print(f"{'='*60}")
        
        if not backups:
            print("No backups available")
            return
        
        print(f"\n{'Filename':<40} {'Size':<10} {'Created':<20}")
        print("-" * 70)
        
        for backup in backups:
            size_kb = backup['size'] / 1024
            created = backup['created'][:19]  # Remove microseconds
            print(f"{backup['filename']:<40} {size_kb:<10.1f} {created:<20}")
        
        print(f"\nTotal: {len(backups)} backups")
        
    def create_backup(self):
        """Create a manual backup"""
        if not self.souls_manager:
            self.initialize_souls_manager()
        
        backup_path = self.souls_manager._create_backup()
        
        if backup_path:
            print(f"✓ Backup created: {backup_path}")
        else:
            print("❌ Failed to create backup")
            
    def add_transaction(self, transaction_type: str, category: str, amount: float, description: str):
        """Add a financial transaction"""
        if not self.cashinghouse:
            self.initialize_cashinghouse()
        
        try:
            tx = self.cashinghouse.add_transaction(
                transaction_type=TransactionType(transaction_type),
                category=TransactionCategory(category),
                amount=amount,
                description=description
            )
            print(f"✓ Transaction added: {tx.transaction_id}")
            print(f"  Type: {tx.transaction_type}")
            print(f"  Category: {tx.category}")
            print(f"  Amount: ${tx.amount:.2f}")
            print(f"  Description: {tx.description}")
        except ValueError as e:
            print(f"❌ Transaction validation failed: {e}")
            
    def show_financial_summary(self):
        """Show financial summary"""
        if not self.cashinghouse:
            self.initialize_cashinghouse()
        
        summary = self.cashinghouse.get_financial_summary()
        
        print(f"\n{'='*60}")
        print("Financial Summary")
        print(f"{'='*60}")
        print(f"Period: {summary.period_start.strftime('%Y-%m-%d')} to {summary.period_end.strftime('%Y-%m-%d')}")
        print(f"Total Income: ${summary.total_income:.2f}")
        print(f"Total Expenses: ${summary.total_expenses:.2f}")
        print(f"Net Balance: ${summary.net_balance:.2f}")
        print(f"Pending Transactions: {summary.pending_transactions}")
        print(f"Reconciled Transactions: {summary.reconciled_transactions}")
        
        print(f"\nCategory Breakdown:")
        for category, amount in summary.category_breakdown.items():
            print(f"  {category}: ${amount:.2f}")
            
    def record_tribute(self, soul_id: str, tribute_type: str, amount: float, description: str, impact_area: str):
        """Record a tribute for a soul"""
        if not self.financial_integration:
            self.initialize_financial_integration()
        
        try:
            tribute = self.financial_integration.record_tribute(
                soul_id=soul_id,
                tribute_type=TributeType(tribute_type),
                amount=amount,
                description=description,
                impact_area=impact_area
            )
            print(f"✓ Tribute recorded: {tribute.tribute_id}")
            print(f"  Soul: {tribute.soul_name}")
            print(f"  Type: {tribute.tribute_type}")
            print(f"  Amount: ${tribute.amount:.2f}" if tribute.amount else f"  Type: {tribute.tribute_type}")
            print(f"  Impact Area: {tribute.impact_area}")
        except ValueError as e:
            print(f"❌ Failed to record tribute: {e}")
            
    def show_HueMan-i-Terry_health(self):
        """Show overall HueMan-i-Terry financial health"""
        if not self.financial_integration:
            self.initialize_financial_integration()
        
        health = self.financial_integration.calculate_HueMan-i-Terry_financial_health()
        
        print(f"\n{'='*60}")
        print("HueMan-i-Terry Financial Health")
        print(f"{'='*60}")
        print(f"Health Score: {health['health_score']}/100")
        print(f"Health Status: {health['health_status'].upper()}")
        print(f"Total Contributions: ${health['total_contributions']:.2f}")
        print(f"Total Tributes: {health['total_tribute_count']}")
        print(f"Active Souls: {health['active_souls']}/{health['total_souls']}")
        print(f"Participation Rate: {health['participation_rate']:.1f}%")
        print(f"Impact Diversity: {health['impact_diversity']}")
        
        if health['recommendations']:
            print(f"\nRecommendations:")
            for rec in health['recommendations']:
                print(f"  • {rec}")
    
    def show_platform_analytics(self):
        """Show platform usage analytics"""
        if not self.analytics_dashboard:
            self.initialize_analytics_dashboard()
        
        analytics = self.analytics_dashboard.get_platform_usage_analytics()
        
        print(f"\n{'='*60}")
        print("Platform Usage Analytics")
        print(f"{'='*60}")
        print(f"Total Platforms: {analytics['total_platforms']}")
        print(f"Top Platform: {analytics['top_platform']}")
        print(f"Most Active Platform: {analytics['most_active_platform']}")
        
        print(f"\nPlatform Metrics:")
        for metric in analytics['platform_metrics']:
            print(f"  {metric['platform']}:")
            print(f"    Total Souls: {metric['total_souls']}")
            print(f"    Active Souls: {metric['active_souls']}")
            print(f"    Content Generated: {metric['content_generated']}")
            print(f"    Avg Engagement: {metric['avg_engagement']}")
            print(f"    Growth Rate: {metric['growth_rate']}%")
    
    def show_financial_analytics(self, days: int = 30):
        """Show financial health analytics"""
        if not self.analytics_dashboard:
            self.initialize_analytics_dashboard()
        
        analytics = self.analytics_dashboard.get_financial_health_analytics(days=days)
        financial_metrics = analytics['financial_metrics']
        
        print(f"\n{'='*60}")
        print("Financial Health Analytics")
        print(f"{'='*60}")
        print(f"Period: {financial_metrics['period']}")
        print(f"Total Revenue: ${financial_metrics['total_revenue']:.2f}")
        print(f"Total Expenses: ${financial_metrics['total_expenses']:.2f}")
        print(f"Net Profit: ${financial_metrics['net_profit']:.2f}")
        print(f"Profit Margin: {financial_metrics['profit_margin']}%")
        print(f"Active Tributes: {financial_metrics['active_tributes']}")
        print(f"Avg Tribute Amount: ${financial_metrics['avg_tribute_amount']:.2f}")
        
        print(f"\nHueMan-i-Terry Health:")
        HueMan-i-Terry_health = analytics['HueMan-i-Terry_health']
        print(f"  Health Score: {HueMan-i-Terry_health['health_score']}/100")
        print(f"  Health Status: {HueMan-i-Terry_health['health_status']}")
        
        if financial_metrics['revenue_by_source']:
            print(f"\nRevenue by Source:")
            for source, amount in financial_metrics['revenue_by_source'].items():
                print(f"  {source}: ${amount:.2f}")
        
        if financial_metrics['expense_by_category']:
            print(f"\nExpenses by Category:")
            for category, amount in financial_metrics['expense_by_category'].items():
                print(f"  {category}: ${amount:.2f}")
    
    def show_soul_performance(self):
        """Show soul performance analytics"""
        if not self.analytics_dashboard:
            self.initialize_analytics_dashboard()
        
        analytics = self.analytics_dashboard.get_soul_performance_analytics()
        
        print(f"\n{'='*60}")
        print("Soul Performance Analytics")
        print(f"{'='*60}")
        print(f"Total Souls Analyzed: {analytics['total_souls_analyzed']}")
        
        print(f"\nActivity Distribution:")
        activity_dist = analytics['activity_distribution']
        print(f"  High: {activity_dist['high']}")
        print(f"  Medium: {activity_dist['medium']}")
        print(f"  Low: {activity_dist['low']}")
        
        print(f"\nTop 10 Performers:")
        for i, performer in enumerate(analytics['top_performers'][:10], 1):
            print(f"  {i}. {performer['soul_name']} ({performer['archetype']})")
            print(f"     Financial Impact: ${performer['financial_impact']:.2f}")
            print(f"     Tributes: {performer['tribute_count']}")
            print(f"     Engagement Score: {performer['engagement_score']}")
            print(f"     Activity Level: {performer['activity_level']}")
    
    def show_comprehensive_dashboard(self):
        """Show comprehensive dashboard"""
        if not self.analytics_dashboard:
            self.initialize_analytics_dashboard()
        
        dashboard = self.analytics_dashboard.get_comprehensive_dashboard()
        
        print(f"\n{'='*60}")
        print("Comprehensive Platform Dashboard")
        print(f"{'='*60}")
        print(f"Generated: {dashboard['generated_at']}")
        
        overall_health = dashboard['overall_health_score']
        print(f"\nOverall Health Score: {overall_health['overall_score']}/100")
        print(f"Overall Status: {overall_health['status'].upper()}")
        
        print(f"\nComponent Scores:")
        for component, score in overall_health['component_scores'].items():
            print(f"  {component.capitalize()}: {score}/100")
        
        print(f"\nRecommendations:")
        for rec in overall_health['recommendations']:
            print(f"  • {rec}")
        
        print(f"\nPlatform Summary:")
        platform_analytics = dashboard['platform_usage']
        print(f"  Total Platforms: {platform_analytics['total_platforms']}")
        print(f"  Top Platform: {platform_analytics['top_platform']}")
        
        print(f"\nFinancial Summary:")
        financial_analytics = dashboard['financial_health']
        financial_metrics = financial_analytics['financial_metrics']
        print(f"  Period Revenue: ${financial_metrics['total_revenue']:.2f}")
        print(f"  Net Profit: ${financial_metrics['net_profit']:.2f}")
        print(f"  HueMan-i-Terry Health: {financial_analytics['HueMan-i-Terry_health']['health_status']}")


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Tiapma'atzu Platform CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # List all souls
  python tiapmaatzu_cli.py list-souls
  
  # Show soul details
  python tiapmaatzu_cli.py show-soul soul_001
  
  # Filter souls by rarity
  python tiapmaatzu_cli.py list-souls --rarity Legendary
  
  # Show statistics
  python tiapmaatzu_cli.py statistics
  
  # Show compatible souls
  python tiapmaatzu_cli.py compatibility soul_001 --threshold 60
  
  # Show data integrity
  python tiapmaatzu_cli.py data-integrity
  
  # List backups
  python tiapmaatzu_cli.py list-backups
  
  # Create backup
  python tiapmaatzu_cli.py create-backup
  
  # Add transaction
  python tiapmaatzu_cli.py add-transaction income content_revenue 500.0 "YouTube revenue"
  
  # Show financial summary
  python tiapmaatzu_cli.py financial-summary
  
  # Record tribute
  python tiapmaatzu_cli.py record-tribute soul_001 monetary 100.0 "Monthly contribution" temple_operations
  
  # Show HueMan-i-Terry health
  python tiapmaatzu_cli.py HueMan-i-Terry-health
  
  # Show platform analytics
  python tiapmaatzu_cli.py platform-analytics
  
  # Show financial analytics
  python tiapmaatzu_cli.py financial-analytics --days 30
  
  # Show soul performance
  python tiapmaatzu_cli.py soul-performance
  
  # Show comprehensive dashboard
  python tiapmaatzu_cli.py comprehensive-dashboard
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # List souls command
    list_parser = subparsers.add_parser('list-souls', help='List souls with optional filtering')
    list_parser.add_argument('--rarity', choices=['Common', 'Rare', 'Legendary'], help='Filter by rarity')
    list_parser.add_argument('--tier', choices=['upper', 'second'], help='Filter by tier')
    list_parser.add_argument('--platform', help='Filter by platform')
    list_parser.add_argument('--archetype', help='Filter by archetype')
    
    # Show soul command
    soul_parser = subparsers.add_parser('show-soul', help='Show detailed soul information')
    soul_parser.add_argument('soul_id', help='Soul ID or name')
    
    # Statistics command
    subparsers.add_parser('statistics', help='Show platform statistics')
    
    # Compatibility command
    compat_parser = subparsers.add_parser('compatibility', help='Show compatible souls')
    compat_parser.add_argument('soul_id', help='Soul ID or name')
    compat_parser.add_argument('--threshold', type=float, default=50.0, help='Compatibility threshold (default: 50.0)')
    
    # Platform management commands
    add_platform_parser = subparsers.add_parser('add-platform', help='Add platform to soul')
    add_platform_parser.add_argument('soul_id', help='Soul ID')
    add_platform_parser.add_argument('platform', help='Platform name')
    
    remove_platform_parser = subparsers.add_parser('remove-platform', help='Remove platform from soul')
    remove_platform_parser.add_argument('soul_id', help='Soul ID')
    remove_platform_parser.add_argument('platform', help='Platform name')
    
    # Soul interaction command
    interaction_parser = subparsers.add_parser('soul-interaction', help='Analyze soul interaction')
    interaction_parser.add_argument('soul_id1', help='First soul ID')
    interaction_parser.add_argument('soul_id2', help='Second soul ID')
    interaction_parser.add_argument('interaction_type', help='Type of interaction')
    
    # Trending platforms command
    trending_parser = subparsers.add_parser('trending-platforms', help='Show trending platforms')
    trending_parser.add_argument('--limit', type=int, default=5, help='Number of platforms to show (default: 5)')
    
    # Data integrity command
    subparsers.add_parser('data-integrity', help='Show data integrity report')
    
    # Backup commands
    subparsers.add_parser('list-backups', help='List available backups')
    subparsers.add_parser('create-backup', help='Create a manual backup')
    
    # Financial commands
    tx_parser = subparsers.add_parser('add-transaction', help='Add a financial transaction')
    tx_parser.add_argument('type', choices=['income', 'expense', 'transfer', 'tribute', 'investment', 'refund'])
    tx_parser.add_argument('category', choices=['content_revenue', 'tribute_contribution', 'platform_fees', 'operational_costs', 'legal_expenses', 'infrastructure', 'marketing', 'community', 'investment_return', 'miscellaneous'])
    tx_parser.add_argument('amount', type=float, help='Transaction amount')
    tx_parser.add_argument('description', help='Transaction description')
    
    subparsers.add_parser('financial-summary', help='Show financial summary')
    
    # Tribute commands
    tribute_parser = subparsers.add_parser('record-tribute', help='Record a tribute for a soul')
    tribute_parser.add_argument('soul_id', help='Soul ID')
    tribute_parser.add_argument('type', choices=['monetary', 'service', 'resource', 'intellectual', 'community'])
    tribute_parser.add_argument('amount', type=float, nargs='?', default=None, help='Tribute amount (if applicable)')
    tribute_parser.add_argument('description', help='Tribute description')
    tribute_parser.add_argument('impact_area', help='Area of impact')
    
    subparsers.add_parser('HueMan-i-Terry-health', help='Show HueMan-i-Terry financial health')
    
    # Analytics commands
    subparsers.add_parser('platform-analytics', help='Show platform usage analytics')
    
    financial_analytics_parser = subparsers.add_parser('financial-analytics', help='Show financial health analytics')
    financial_analytics_parser.add_argument('--days', type=int, default=30, help='Number of days to analyze (default: 30)')
    
    subparsers.add_parser('soul-performance', help='Show soul performance analytics')
    subparsers.add_parser('comprehensive-dashboard', help='Show comprehensive platform dashboard')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 0
    
    cli = TiapmaatzuCLI()
    
    try:
        if args.command == 'list-souls':
            filters = {}
            if args.rarity: filters['rarity'] = args.rarity
            if args.tier: filters['tier'] = args.tier
            if args.platform: filters['platform'] = args.platform
            if args.archetype: filters['archetype'] = args.archetype
            cli.list_souls(filters)
            
        elif args.command == 'show-soul':
            cli.show_soul_details(args.soul_id)
            
        elif args.command == 'statistics':
            cli.show_statistics()
            
        elif args.command == 'compatibility':
            cli.show_compatibility(args.soul_id, args.threshold)
            
        elif args.command == 'add-platform':
            cli.add_platform_to_soul(args.soul_id, args.platform)
            
        elif args.command == 'remove-platform':
            cli.remove_platform_from_soul(args.soul_id, args.platform)
            
        elif args.command == 'soul-interaction':
            cli.create_soul_interaction(args.soul_id1, args.soul_id2, args.interaction_type)
            
        elif args.command == 'trending-platforms':
            cli.show_trending_platforms(args.limit)
            
        elif args.command == 'data-integrity':
            cli.show_data_integrity()
            
        elif args.command == 'list-backups':
            cli.list_backups()
            
        elif args.command == 'create-backup':
            cli.create_backup()
            
        elif args.command == 'add-transaction':
            cli.add_transaction(args.type, args.category, args.amount, args.description)
            
        elif args.command == 'financial-summary':
            cli.show_financial_summary()
            
        elif args.command == 'record-tribute':
            cli.record_tribute(args.soul_id, args.type, args.amount, args.description, args.impact_area)
            
        elif args.command == 'HueMan-i-Terry-health':
            cli.show_HueMan-i-Terry_health()
            
        elif args.command == 'platform-analytics':
            cli.show_platform_analytics()
            
        elif args.command == 'financial-analytics':
            cli.show_financial_analytics(args.days)
            
        elif args.command == 'soul-performance':
            cli.show_soul_performance()
            
        elif args.command == 'comprehensive-dashboard':
            cli.show_comprehensive_dashboard()
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())