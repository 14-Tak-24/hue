"""
CashingHouse Financial Tracking System
Central financial ledger and accounting system for the Tiapma'atzu platform
"""

import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path

from .utils import (
    Configuration, DataUtils, ValidationUtils, LoggingUtils
)


class TransactionType(Enum):
    """Types of financial transactions"""
    INCOME = "income"
    EXPENSE = "expense"
    TRANSFER = "transfer"
    TRIBUTE = "tribute"
    INVESTMENT = "investment"
    REFUND = "refund"


class TransactionCategory(Enum):
    """Categories for transactions"""
    CONTENT_REVENUE = "content_revenue"
    TRIBUTE_CONTRIBUTION = "tribute_contribution"
    PLATFORM_FEES = "platform_fees"
    OPERATIONAL_COSTS = "operational_costs"
    LEGAL_EXPENSES = "legal_expenses"
    INFRASTRUCTURE = "infrastructure"
    MARKETING = "marketing"
    COMMUNITY = "community"
    INVESTMENT_RETURN = "investment_return"
    MISCELLANEOUS = "miscellaneous"


@dataclass
class Transaction:
    """Individual financial transaction"""
    transaction_id: str
    transaction_type: str
    category: str
    amount: float
    description: str
    timestamp: datetime
    source_id: Optional[str] = None  # soul_id, platform_id, etc.
    destination_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    status: str = "completed"  # pending, completed, failed, cancelled
    reconciled: bool = False


@dataclass
class FinancialSummary:
    """Summary of financial status"""
    total_income: float
    total_expenses: float
    net_balance: float
    pending_transactions: int
    reconciled_transactions: int
    period_start: datetime
    period_end: datetime
    category_breakdown: Dict[str, float]
    cash_flow_trend: List[Dict[str, Any]]


class CashingHouse:
    """
    Central financial ledger and tracking system for the Tiapma'atzu platform.
    
    This class manages all financial transactions, budget tracking, financial goals,
    and reporting for the platform. It provides comprehensive financial analytics
    and validation for all monetary operations.
    
    Attributes:
        data_path: Path to the financial data JSON file
        transactions: List of all financial transactions
        budget_limits: Dictionary of budget limits by category
        financial_goals: Dictionary of financial goals
        enable_validation: Whether transaction validation is enabled
        logger: Logger instance for operations
    """
    
    def __init__(self, data_path: Optional[str] = None, enable_validation: bool = True):
        """
        Initialize CashingHouse system
        
        Args:
            data_path: Path to store financial data
            enable_validation: Enable transaction validation
        """
        if data_path is None:
            data_path = Configuration.DEFAULT_CASHINGHOUSE_DATA
        
        self.data_path = Path(data_path)
        self.transactions: List[Transaction] = []
        self.budget_limits: Dict[str, float] = {}
        self.financial_goals: Dict[str, Any] = {}
        self.enable_validation = enable_validation
        self.logger = LoggingUtils.setup_logger(__name__)
        
        # Load existing data if available
        self._load_data()
    
    def _load_data(self):
        """Load financial data from storage"""
        if self.data_path.exists():
            try:
                data = DataUtils.load_json_file(self.data_path)
                    
                # Load transactions
                for tx_data in data.get('transactions', []):
                    tx_data['timestamp'] = datetime.fromisoformat(tx_data['timestamp'])
                    self.transactions.append(Transaction(**tx_data))
                
                # Load budget limits
                self.budget_limits = data.get('budget_limits', {})
                
                # Load financial goals
                self.financial_goals = data.get('financial_goals', {})
                
            except Exception as e:
                self.logger.error(f"Error loading CashingHouse data: {e}")
    
    def _save_data(self):
        """Save financial data to storage"""
        try:
            data = {
                'transactions': [asdict(tx) for tx in self.transactions],
                'budget_limits': self.budget_limits,
                'financial_goals': self.financial_goals,
                'last_updated': datetime.now().isoformat()
            }
            
            DataUtils.save_json_file(data, self.data_path)
                
        except Exception as e:
            self.logger.error(f"Error saving CashingHouse data: {e}")
    
    def add_transaction(
        self,
        transaction_type: TransactionType,
        category: TransactionCategory,
        amount: float,
        description: str,
        source_id: Optional[str] = None,
        destination_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Transaction:
        """
        Add a new transaction to the ledger
        
        Args:
            transaction_type: Type of transaction
            category: Category of transaction
            amount: Transaction amount
            description: Transaction description
            source_id: Source identifier
            destination_id: Destination identifier
            metadata: Additional metadata
            
        Returns:
            Created transaction
        """
        # Validate transaction if enabled
        if self.enable_validation:
            validation_errors = self._validate_transaction(
                transaction_type, category, amount, description
            )
            if validation_errors:
                raise ValueError(f"Transaction validation failed: {', '.join(validation_errors)}")
        
        transaction = Transaction(
            transaction_id=f"tx_{datetime.now().timestamp()}",
            transaction_type=transaction_type.value,
            category=category.value,
            amount=amount,
            description=description,
            timestamp=datetime.now(),
            source_id=source_id,
            destination_id=destination_id,
            metadata=metadata or {}
        )
        
        self.transactions.append(transaction)
        self._save_data()
        
        self.logger.info(f"Transaction added: {transaction.transaction_id} - {description}")
        return transaction
    
    def _validate_transaction(
        self,
        transaction_type: TransactionType,
        category: TransactionCategory,
        amount: float,
        description: str
    ) -> List[str]:
        """Validate transaction data"""
        errors = []
        
        # Validate amount range
        errors.extend(ValidationUtils.validate_numeric_range(
            amount, 
            min_val=0.01, 
            max_val=Configuration.MAX_TRANSACTION_AMOUNT,
            field_name="Amount"
        ))
        
        # Validate description length
        errors.extend(ValidationUtils.validate_string_length(
            description,
            min_length=Configuration.MIN_DESCRIPTION_LENGTH,
            max_length=Configuration.MAX_DESCRIPTION_LENGTH,
            field_name="Description"
        ))
        
        # Category-transaction type compatibility
        incompatible_combinations = [
            (TransactionType.TRIBUTE, TransactionCategory.PLATFORM_FEES),
            (TransactionType.INVESTMENT, TransactionCategory.COMMUNITY),
        ]
        
        if (transaction_type, category) in incompatible_combinations:
            errors.append(f"Incompatible transaction type and category combination")
        
        return errors
    
    def get_transaction(self, transaction_id: str) -> Optional[Transaction]:
        """Get a specific transaction by ID"""
        for tx in self.transactions:
            if tx.transaction_id == transaction_id:
                return tx
        return None
    
    def get_transactions_by_type(self, transaction_type: TransactionType) -> List[Transaction]:
        """Get all transactions of a specific type"""
        return [tx for tx in self.transactions if tx.transaction_type == transaction_type.value]
    
    def get_transactions_by_category(self, category: TransactionCategory) -> List[Transaction]:
        """Get all transactions of a specific category"""
        return [tx for tx in self.transactions if tx.category == category.value]
    
    def get_transactions_by_source(self, source_id: str) -> List[Transaction]:
        """Get all transactions from a specific source"""
        return [tx for tx in self.transactions if tx.source_id == source_id]
    
    def get_transactions_in_date_range(
        self, 
        start_date: datetime, 
        end_date: datetime
    ) -> List[Transaction]:
        """Get transactions within a specific date range"""
        return [
            tx for tx in self.transactions 
            if start_date <= tx.timestamp <= end_date
        ]
    
    def get_financial_summary(
        self, 
        start_date: Optional[datetime] = None, 
        end_date: Optional[datetime] = None
    ) -> FinancialSummary:
        """
        Get financial summary for a specific period
        
        Args:
            start_date: Start date for summary (default: 30 days ago)
            end_date: End date for summary (default: now)
            
        Returns:
            FinancialSummary with comprehensive financial data
        """
        if start_date is None:
            start_date = datetime.now() - timedelta(days=30)
        if end_date is None:
            end_date = datetime.now()
        
        # Filter transactions for period
        period_transactions = self.get_transactions_in_date_range(start_date, end_date)
        
        # Calculate totals
        total_income = sum(
            tx.amount for tx in period_transactions 
            if tx.transaction_type == TransactionType.INCOME.value or 
               tx.transaction_type == TransactionType.TRIBUTE.value or
               tx.transaction_type == TransactionType.INVESTMENT.value
        )
        
        total_expenses = sum(
            tx.amount for tx in period_transactions 
            if tx.transaction_type == TransactionType.EXPENSE.value
        )
        
        # Category breakdown
        category_breakdown: Dict[str, float] = {}
        for tx in period_transactions:
            if tx.category not in category_breakdown:
                category_breakdown[tx.category] = 0.0
            
            if tx.transaction_type in [TransactionType.INCOME.value, TransactionType.TRIBUTE.value, TransactionType.INVESTMENT.value]:
                category_breakdown[tx.category] += tx.amount
            elif tx.transaction_type == TransactionType.EXPENSE.value:
                category_breakdown[tx.category] -= tx.amount
        
        # Cash flow trend (daily)
        cash_flow_trend = self._calculate_cash_flow_trend(period_transactions)
        
        # Count pending and reconciled
        pending_count = len([tx for tx in period_transactions if tx.status == 'pending'])
        reconciled_count = len([tx for tx in period_transactions if tx.reconciled])
        
        return FinancialSummary(
            total_income=total_income,
            total_expenses=total_expenses,
            net_balance=total_income - total_expenses,
            pending_transactions=pending_count,
            reconciled_transactions=reconciled_count,
            period_start=start_date,
            period_end=end_date,
            category_breakdown=category_breakdown,
            cash_flow_trend=cash_flow_trend
        )
    
    def _calculate_cash_flow_trend(self, transactions: List[Transaction]) -> List[Dict[str, Any]]:
        """Calculate daily cash flow trend"""
        daily_flow = {}
        
        for tx in transactions:
            date_key = tx.timestamp.strftime("%Y-%m-%d")
            if date_key not in daily_flow:
                daily_flow[date_key] = {'income': 0.0, 'expenses': 0.0}
            
            if tx.transaction_type in [TransactionType.INCOME.value, TransactionType.TRIBUTE.value, TransactionType.INVESTMENT.value]:
                daily_flow[date_key]['income'] += tx.amount
            elif tx.transaction_type == TransactionType.EXPENSE.value:
                daily_flow[date_key]['expenses'] += tx.amount
        
        # Convert to sorted list
        trend = []
        for date_key in sorted(daily_flow.keys()):
            flow = daily_flow[date_key]
            trend.append({
                'date': date_key,
                'income': flow['income'],
                'expenses': flow['expenses'],
                'net': flow['income'] - flow['expenses']
            })
        
        return trend
    
    def set_budget_limit(self, category: TransactionCategory, limit: float):
        """Set budget limit for a category"""
        self.budget_limits[category.value] = limit
        self._save_data()
    
    def check_budget_status(self) -> Dict[str, Any]:
        """Check budget status against limits"""
        current_month = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        month_transactions = self.get_transactions_in_date_range(current_month, datetime.now())
        
        budget_status = {}
        
        for category, limit in self.budget_limits.items():
            spent = sum(
                tx.amount for tx in month_transactions 
                if tx.category == category and tx.transaction_type == TransactionType.EXPENSE.value
            )
            
            remaining = limit - spent
            percentage_used = (spent / limit) * 100 if limit > 0 else 0
            
            status = 'healthy'
            if percentage_used >= 90:
                status = 'critical'
            elif percentage_used >= 75:
                status = 'warning'
            
            budget_status[category] = {
                'limit': limit,
                'spent': spent,
                'remaining': remaining,
                'percentage_used': round(percentage_used, 2),
                'status': status
            }
        
        return budget_status
    
    def set_financial_goal(self, goal_id: str, goal_data: Dict[str, Any]):
        """Set a financial goal"""
        self.financial_goals[goal_id] = {
            **goal_data,
            'created_at': datetime.now().isoformat(),
            'progress': 0.0
        }
        self._save_data()
    
    def check_financial_goals(self) -> Dict[str, Any]:
        """Check progress towards financial goals"""
        goals_status = {}
        
        for goal_id, goal in self.financial_goals.items():
            target_amount = goal.get('target_amount', 0)
            current_amount = goal.get('current_amount', 0)
            
            progress = (current_amount / target_amount) * 100 if target_amount > 0 else 0
            
            status = 'in_progress'
            if progress >= 100:
                status = 'completed'
            elif progress == 0:
                status = 'not_started'
            
            goals_status[goal_id] = {
                **goal,
                'progress': round(progress, 2),
                'status': status
            }
        
        return goals_status
    
    def reconcile_transaction(self, transaction_id: str) -> bool:
        """Mark a transaction as reconciled"""
        transaction = self.get_transaction(transaction_id)
        if transaction:
            transaction.reconciled = True
            self._save_data()
            return True
        return False
    
    def generate_financial_report(self, report_type: str = 'monthly') -> Dict[str, Any]:
        """
        Generate comprehensive financial report
        
        Args:
            report_type: Type of report ('daily', 'weekly', 'monthly', 'yearly')
            
        Returns:
            Comprehensive financial report
        """
        # Determine date range based on report type
        end_date = datetime.now()
        if report_type == 'daily':
            start_date = end_date - timedelta(days=1)
        elif report_type == 'weekly':
            start_date = end_date - timedelta(weeks=1)
        elif report_type == 'monthly':
            start_date = end_date - timedelta(days=30)
        elif report_type == 'yearly':
            start_date = end_date - timedelta(days=365)
        else:
            start_date = end_date - timedelta(days=30)
        
        # Get financial summary
        summary = self.get_financial_summary(start_date, end_date)
        
        # Get top income sources
        income_transactions = self.get_transactions_in_date_range(start_date, end_date)
        income_sources = {}
        for tx in income_transactions:
            if tx.transaction_type in [TransactionType.INCOME.value, TransactionType.TRIBUTE.value]:
                source = tx.source_id or 'unknown'
                if source not in income_sources:
                    income_sources[source] = 0.0
                income_sources[source] += tx.amount
        
        top_income_sources = sorted(income_sources.items(), key=lambda x: x[1], reverse=True)[:10]
        
        # Get top expense categories
        expense_transactions = [tx for tx in income_transactions if tx.transaction_type == TransactionType.EXPENSE.value]
        expense_categories = {}
        for tx in expense_transactions:
            if tx.category not in expense_categories:
                expense_categories[tx.category] = 0.0
            expense_categories[tx.category] += tx.amount
        
        top_expense_categories = sorted(expense_categories.items(), key=lambda x: x[1], reverse=True)[:10]
        
        return {
            'report_type': report_type,
            'period': {
                'start': start_date.isoformat(),
                'end': end_date.isoformat()
            },
            'financial_summary': asdict(summary),
            'top_income_sources': [
                {'source': source, 'amount': amount} 
                for source, amount in top_income_sources
            ],
            'top_expense_categories': [
                {'category': category, 'amount': amount} 
                for category, amount in top_expense_categories
            ],
            'budget_status': self.check_budget_status(),
            'financial_goals': self.check_financial_goals(),
            'recommendations': self._generate_financial_recommendations(summary)
        }
    
    def _generate_financial_recommendations(self, summary: FinancialSummary) -> List[str]:
        """Generate financial recommendations based on summary"""
        recommendations = []
        
        # Analyze net balance
        if summary.net_balance < 0:
            recommendations.append("Negative cash flow detected - review expenses and increase revenue streams")
        elif summary.net_balance < summary.total_income * 0.1:
            recommendations.append("Low profit margin - consider optimizing operational costs")
        
        # Analyze pending transactions
        if summary.pending_transactions > 5:
            recommendations.append("High number of pending transactions - consider reconciliation process")
        
        # Analyze category breakdown
        if any(amount < 0 for amount in summary.category_breakdown.values()):
            negative_categories = [cat for cat, amount in summary.category_breakdown.items() if amount < 0]
            recommendations.append(f"Review spending in categories: {', '.join(negative_categories)}")
        
        # Analyze cash flow trend
        if len(summary.cash_flow_trend) > 1:
            recent_trend = summary.cash_flow_trend[-7:] if len(summary.cash_flow_trend) >= 7 else summary.cash_flow_trend
            if all(trend['net'] < 0 for trend in recent_trend):
                recommendations.append("Consistent negative cash flow - immediate action required")
        
        return recommendations
    
    def export_for_firebase(self) -> Dict[str, Any]:
        """Export financial data in Firebase-compatible format"""
        return {
            'transactions': [
                {
                    'transactionId': tx.transaction_id,
                    'type': tx.transaction_type,
                    'category': tx.category,
                    'amount': tx.amount,
                    'description': tx.description,
                    'timestamp': tx.timestamp.isoformat(),
                    'sourceId': tx.source_id,
                    'destinationId': tx.destination_id,
                    'status': tx.status,
                    'reconciled': tx.reconciled,
                    'metadata': tx.metadata
                }
                for tx in self.transactions
            ],
            'budgetLimits': self.budget_limits,
            'financialGoals': self.financial_goals,
            'lastUpdated': datetime.now().isoformat()
        }
    
    def record_tribute(
        self,
        soul_id: str,
        amount: float,
        impact_area: str,
        platform: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Transaction:
        """
        Record a tribute transaction from a soul
        
        Args:
            soul_id: ID of the soul providing the tribute
            amount: Tribute amount
            impact_area: Area of impact (content, community, etc.)
            platform: Platform where tribute originated
            metadata: Additional metadata
            
        Returns:
            Created tribute transaction
        """
        description = f"Tribute from soul {soul_id} - {impact_area} via {platform}"
        
        if metadata:
            soul_name = metadata.get('soul_name', '')
            if soul_name:
                description = f"Tribute from {soul_name} ({soul_id}) - {impact_area} via {platform}"
        
        return self.add_transaction(
            transaction_type=TransactionType.TRIBUTE,
            category=TransactionCategory.TRIBUTE_CONTRIBUTION,
            amount=amount,
            description=description,
            source_id=soul_id,
            metadata=metadata or {}
        )
    
    def bulk_import_transactions(self, transactions_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Bulk import transactions from external data
        
        Args:
            transactions_data: List of transaction dictionaries
            
        Returns:
            Import summary with success/failure counts
        """
        success_count = 0
        failure_count = 0
        errors = []
        
        for tx_data in transactions_data:
            try:
                # Map transaction type string to enum
                transaction_type = TransactionType(tx_data.get('type', 'income'))
                category = TransactionCategory(tx_data.get('category', 'miscellaneous'))
                
                self.add_transaction(
                    transaction_type=transaction_type,
                    category=category,
                    amount=float(tx_data.get('amount', 0)),
                    description=tx_data.get('description', 'Imported transaction'),
                    source_id=tx_data.get('source_id'),
                    destination_id=tx_data.get('destination_id'),
                    metadata=tx_data.get('metadata', {})
                )
                success_count += 1
                
            except Exception as e:
                failure_count += 1
                errors.append({
                    'transaction_data': tx_data,
                    'error': str(e)
                })
                self.logger.error(f"Failed to import transaction: {e}")
        
        return {
            'total': len(transactions_data),
            'success': success_count,
            'failure': failure_count,
            'errors': errors
        }
    
    def get_anomaly_detection_report(self) -> Dict[str, Any]:
        """Detect anomalies in financial data"""
        anomalies = []
        
        if not self.transactions:
            return {'anomalies': [], 'total_anomalies': 0}
        
        # Detect unusually large transactions
        amounts = [tx.amount for tx in self.transactions]
        if amounts:
            mean_amount = sum(amounts) / len(amounts)
            std_dev = (sum((x - mean_amount) ** 2 for x in amounts) / len(amounts)) ** 0.5
            
            for tx in self.transactions:
                if tx.amount > mean_amount + (3 * std_dev):  # 3 standard deviations
                    anomalies.append({
                        'type': 'unusually_large_transaction',
                        'transaction_id': tx.transaction_id,
                        'amount': tx.amount,
                        'expected_range': f"{mean_amount - (2 * std_dev):.2f} - {mean_amount + (2 * std_dev):.2f}",
                        'description': tx.description
                    })
        
        # Detect rapid succession of transactions
        sorted_transactions = sorted(self.transactions, key=lambda x: x.timestamp)
        for i in range(1, len(sorted_transactions)):
            time_diff = (sorted_transactions[i].timestamp - sorted_transactions[i-1].timestamp).total_seconds()
            if time_diff < 60:  # Less than 1 minute apart
                anomalies.append({
                    'type': 'rapid_succession',
                    'transaction_ids': [sorted_transactions[i-1].transaction_id, sorted_transactions[i].transaction_id],
                    'time_diff_seconds': time_diff,
                    'description': 'Transactions in rapid succession'
                })
        
        # Detect duplicate descriptions
        description_counts = {}
        for tx in self.transactions:
            desc = tx.description.lower()
            description_counts[desc] = description_counts.get(desc, 0) + 1
        
        for desc, count in description_counts.items():
            if count > 5:  # More than 5 transactions with same description
                matching_tx = [tx for tx in self.transactions if tx.description.lower() == desc]
                anomalies.append({
                    'type': 'duplicate_descriptions',
                    'description': desc,
                    'count': count,
                    'transaction_ids': [tx.transaction_id for tx in matching_tx[:5]]
                })
        
        return {
            'anomalies': anomalies,
            'total_anomalies': len(anomalies),
            'analyzed_at': datetime.now().isoformat()
        }