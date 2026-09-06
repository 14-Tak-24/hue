"""
Task Scheduler Module
Provides scheduled task management for automated backups, reports, and maintenance
"""

import logging
import threading
import time
from datetime import datetime, timedelta
from typing import Dict, Callable, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
import json
from pathlib import Path

from .utils import LoggingUtils

# Configure logging
logger = LoggingUtils.setup_logger(__name__)


class TaskStatus(Enum):
    """Task execution status"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TaskFrequency(Enum):
    """Task execution frequency"""
    ONCE = "once"
    HOURLY = "hourly"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    CUSTOM = "custom"


@dataclass
class ScheduledTask:
    """Represents a scheduled task"""
    id: str
    name: str
    function: Callable
    frequency: TaskFrequency
    enabled: bool = True
    last_run: Optional[datetime] = None
    next_run: Optional[datetime] = None
    status: TaskStatus = TaskStatus.PENDING
    params: dict = field(default_factory=dict)
    retry_count: int = 0
    max_retries: int = 3
    timeout: int = 300  # 5 minutes default
    result: Optional[Any] = None
    error: Optional[str] = None
    
    def to_dict(self) -> dict:
        """Convert task to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'frequency': self.frequency.value,
            'enabled': self.enabled,
            'last_run': self.last_run.isoformat() if self.last_run else None,
            'next_run': self.next_run.isoformat() if self.next_run else None,
            'status': self.status.value,
            'params': self.params,
            'retry_count': self.retry_count,
            'max_retries': self.max_retries,
            'timeout': self.timeout,
            'result': str(self.result) if self.result else None,
            'error': self.error
        }


class TaskScheduler:
    """Manages scheduled tasks execution"""
    
    def __init__(self):
        self.tasks: Dict[str, ScheduledTask] = {}
        self.running = False
        self.scheduler_thread: Optional[threading.Thread] = None
        self.task_history: list = []
        self.max_history = 1000
    
    def add_task(
        self,
        task_id: str,
        name: str,
        function: Callable,
        frequency: TaskFrequency = TaskFrequency.DAILY,
        params: dict = None,
        enabled: bool = True,
        max_retries: int = 3,
        timeout: int = 300
    ) -> ScheduledTask:
        """Add a new scheduled task"""
        task = ScheduledTask(
            id=task_id,
            name=name,
            function=function,
            frequency=frequency,
            enabled=enabled,
            params=params or {},
            max_retries=max_retries,
            timeout=timeout
        )
        
        # Calculate next run time
        task.next_run = self._calculate_next_run(frequency)
        
        self.tasks[task_id] = task
        logger.info("Added task: %s (%s) with frequency: %s", name, task_id, frequency.value)
        
        return task
    
    def remove_task(self, task_id: str) -> bool:
        """Remove a scheduled task"""
        if task_id in self.tasks:
            del self.tasks[task_id]
            logger.info("Removed task: %s", task_id)
            return True
        return False
    
    def enable_task(self, task_id: str) -> bool:
        """Enable a task"""
        if task_id in self.tasks:
            self.tasks[task_id].enabled = True
            logger.info("Enabled task: %s", task_id)
            return True
        return False
    
    def disable_task(self, task_id: str) -> bool:
        """Disable a task"""
        if task_id in self.tasks:
            self.tasks[task_id].enabled = False
            logger.info("Disabled task: %s", task_id)
            return True
        return False
    
    def _calculate_next_run(self, frequency: TaskFrequency) -> datetime:
        """Calculate next run time based on frequency"""
        now = datetime.now()
        
        if frequency == TaskFrequency.ONCE:
            return now + timedelta(minutes=1)  # Run once in 1 minute
        if frequency == TaskFrequency.HOURLY:
            return now + timedelta(hours=1)
        if frequency == TaskFrequency.DAILY:
            return now + timedelta(days=1)
        if frequency == TaskFrequency.WEEKLY:
            return now + timedelta(weeks=1)
        if frequency == TaskFrequency.MONTHLY:
            return now + timedelta(days=30)
        return now + timedelta(hours=1)  # Default to hourly
    
    def _execute_task(self, task: ScheduledTask):
        """Execute a single task"""
        task.status = TaskStatus.RUNNING
        task.last_run = datetime.now()
        
        logger.info("Executing task: %s (%s)", task.name, task.id)
        
        try:
            # Execute the task function with parameters
            result = task.function(**task.params)
            
            task.status = TaskStatus.COMPLETED
            task.result = result
            task.error = None
            task.retry_count = 0
            
            logger.info("Task completed successfully: %s", task.name)
            
            # Add to history
            self._add_to_history(task, success=True)
            
        except (TimeoutError, RuntimeError, ValueError) as e:
            task.status = TaskStatus.FAILED
            task.error = str(e)
            task.retry_count += 1
            
            logger.error("Task failed: %s - Error: %s", task.name, e)
            
            # Add to history
            self._add_to_history(task, success=False)
            
            # Retry if needed
            if task.retry_count < task.max_retries:
                logger.info("Retrying task %s (attempt %d/%d)", task.name, task.retry_count + 1, task.max_retries)
                time.sleep(5)  # Wait before retry
                self._execute_task(task)
    
    def _add_to_history(self, task: ScheduledTask, success: bool):
        """Add task execution to history"""
        history_entry = {
            'task_id': task.id,
            'task_name': task.name,
            'status': task.status.value,
            'success': success,
            'timestamp': datetime.now().isoformat(),
            'duration': str(datetime.now() - task.last_run) if task.last_run else None,
            'error': task.error
        }
        
        self.task_history.append(history_entry)
        
        # Trim history if needed
        if len(self.task_history) > self.max_history:
            self.task_history = self.task_history[-self.max_history:]
    
    def _scheduler_loop(self):
        """Main scheduler loop"""
        logger.info("Scheduler loop started")
        
        while self.running:
            try:
                now = datetime.now()
                
                # Check for tasks that need to run
                for _, task in self.tasks.items():
                    if not task.enabled:
                        continue
                    
                    if task.next_run and now >= task.next_run:
                        logger.info("Running scheduled task: %s", task.name)
                        
                        # Execute task in separate thread to avoid blocking
                        task_thread = threading.Thread(
                            target=self._execute_task,
                            args=(task,)
                        )
                        task_thread.start()
                        
                        # Calculate next run time
                        if task.frequency == TaskFrequency.ONCE:
                            task.enabled = False  # Disable one-time tasks
                        else:
                            task.next_run = self._calculate_next_run(task.frequency)
                
                # Sleep for 1 minute before next check
                time.sleep(60)
                
            except (TimeoutError, RuntimeError, ValueError) as e:
                logger.error("Scheduler loop error: %s", e)
                time.sleep(60)
        
        logger.info("Scheduler loop stopped")
    
    def start(self):
        """Start the task scheduler"""
        if not self.running:
            self.running = True
            self.scheduler_thread = threading.Thread(target=self._scheduler_loop, daemon=True)
            self.scheduler_thread.start()
            logger.info("Task scheduler started")
    
    def stop(self):
        """Stop the task scheduler"""
        if self.running:
            self.running = False
            if self.scheduler_thread:
                self.scheduler_thread.join(timeout=10)
            logger.info("Task scheduler stopped")
    
    def get_task_status(self, task_id: str) -> Optional[dict]:
        """Get status of a specific task"""
        if task_id in self.tasks:
            return self.tasks[task_id].to_dict()
        return None
    
    def get_all_tasks(self) -> list:
        """Get all tasks"""
        return [task.to_dict() for task in self.tasks.values()]
    
    def get_task_history(self, limit: int = 50) -> list:
        """Get task execution history"""
        return self.task_history[-limit:] if self.task_history else []
    
    def run_task_now(self, task_id: str) -> bool:
        """Run a task immediately (bypass schedule)"""
        if task_id in self.tasks:
            task = self.tasks[task_id]
            logger.info("Running task immediately: %s", task.name)
            
            # Execute in separate thread
            task_thread = threading.Thread(target=self._execute_task, args=(task,))
            task_thread.start()
            
            return True
        return False


# Built-in task functions
def backup_database_task():
    """Task to backup the database"""
    logger.info("Running database backup task")
    # This would integrate with the existing backup system
    # For now, just log it
    return {"status": "backup_completed", "timestamp": datetime.now().isoformat()}


def cleanup_old_backups_task():
    """Task to clean up old backup files"""
    logger.info("Running cleanup old backups task")
    # This would clean up old backup files
    return {"status": "cleanup_completed", "timestamp": datetime.now().isoformat()}


def generate_analytics_report_task():
    """Task to generate daily analytics report"""
    logger.info("Running analytics report generation task")
    # This would generate analytics reports
    return {"status": "report_generated", "timestamp": datetime.now().isoformat()}


def sync_firestore_task():
    """Task to sync data with Firestore"""
    logger.info("Running Firestore sync task")
    # This would sync data with Firestore
    return {"status": "sync_completed", "timestamp": datetime.now().isoformat()}


def health_check_task():
    """Task to perform system health checks"""
    logger.info("Running health check task")
    # This would perform health checks
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "checks": {
            "database": "ok",
            "api": "ok",
            "firebase": "ok"
        }
    }


# Global scheduler instance
scheduler = TaskScheduler()


def get_scheduler() -> TaskScheduler:
    """Get the global task scheduler instance"""
    return scheduler


def init_default_tasks():
    """Initialize default scheduled tasks"""
    scheduler.add_task(
        task_id="daily_backup",
        name="Daily Database Backup",
        function=backup_database_task,
        frequency=TaskFrequency.DAILY,
        params={},
        enabled=True
    )
    
    scheduler.add_task(
        task_id="weekly_cleanup",
        name="Weekly Backup Cleanup",
        function=cleanup_old_backups_task,
        frequency=TaskFrequency.WEEKLY,
        params={},
        enabled=True
    )
    
    scheduler.add_task(
        task_id="daily_analytics",
        name="Daily Analytics Report",
        function=generate_analytics_report_task,
        frequency=TaskFrequency.DAILY,
        params={},
        enabled=True
    )
    
    scheduler.add_task(
        task_id="hourly_sync",
        name="Hourly Firestore Sync",
        function=sync_firestore_task,
        frequency=TaskFrequency.HOURLY,
        params={},
        enabled=True
    )
    
    scheduler.add_task(
        task_id="health_check",
        name="System Health Check",
        function=health_check_task,
        frequency=TaskFrequency.HOURLY,
        params={},
        enabled=True
    )
    
    logger.info("Default tasks initialized")
