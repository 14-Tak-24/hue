#!/usr/bin/env python3
"""
Monitoring and Logging Setup
Configure comprehensive logging and monitoring for the Tiapma'atzu platform
"""

import sys
import logging
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler


class PlatformLogger:
    """Centralized logging configuration for the platform"""
    
    def __init__(self, log_dir: str = None, log_level: str = "INFO"):
        """
        Initialize the platform logger
        
        Args:
            log_dir: Directory for log files
            log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        """
        if log_dir is None:
            log_dir = Path(__file__).parent / "logs"
        
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        self.log_level = getattr(logging, log_level.upper(), logging.INFO)
        self.logger = logging.getLogger("tiapmaatzu")
        self.logger.setLevel(self.log_level)
        
        # Remove existing handlers
        self.logger.handlers.clear()
        
        # Set up handlers
        self._setup_console_handler()
        self._setup_file_handler()
        self._setup_error_handler()
        self._setup_audit_handler()
        
        self.logger.info("Platform logging initialized")
        
    def _setup_console_handler(self):
        """Set up console logging handler"""
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(self.log_level)
        
        console_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)
        
    def _setup_file_handler(self):
        """Set up rotating file handler for general logs"""
        log_file = self.log_dir / "tiapmaatzu.log"
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        file_handler.setLevel(self.log_level)
        
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)
        
    def _setup_error_handler(self):
        """Set up separate handler for errors"""
        error_file = self.log_dir / "errors.log"
        error_handler = RotatingFileHandler(
            error_file,
            maxBytes=5*1024*1024,  # 5MB
            backupCount=3
        )
        error_handler.setLevel(logging.ERROR)
        
        error_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        error_handler.setFormatter(error_formatter)
        self.logger.addHandler(error_handler)
        
    def _setup_audit_handler(self):
        """Set up audit log for important operations"""
        audit_file = self.log_dir / "audit.log"
        audit_handler = TimedRotatingFileHandler(
            audit_file,
            when='midnight',
            interval=1,
            backupCount=30
        )
        audit_handler.setLevel(logging.INFO)
        
        audit_formatter = logging.Formatter(
            '%(asctime)s - AUDIT - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        audit_handler.setFormatter(audit_formatter)
        
        # Create audit logger
        self.audit_logger = logging.getLogger("tiapmaatzu.audit")
        self.audit_logger.setLevel(logging.INFO)
        self.audit_logger.addHandler(audit_handler)
        
    def get_logger(self, name: str = None) -> logging.Logger:
        """Get a logger instance"""
        if name:
            return logging.getLogger("tiapmaatzu." + name)
        return self.logger
        
    def audit(self, message: str, **kwargs):
        """Log an audit event"""
        audit_message = message
        if kwargs:
            audit_message += " - " + json.dumps(kwargs)
        self.audit_logger.info(audit_message)


class PerformanceMonitor:
    """Monitor platform performance metrics"""
    
    def __init__(self, logger: logging.Logger = None):
        """Initialize performance monitor"""
        self.logger = logger or logging.getLogger("tiapmaatzu.performance")
        self.metrics = {}
        self.start_times = {}
        
    def start_timer(self, operation: str):
        """Start timing an operation"""
        self.start_times[operation] = datetime.now()
        self.logger.debug("Started timer for: " + operation)
        
    def end_timer(self, operation: str) -> float:
        """End timing an operation and return duration"""
        if operation not in self.start_times:
            self.logger.warning("No timer found for: " + operation)
            return 0.0
        
        duration = (datetime.now() - self.start_times[operation]).total_seconds()
        del self.start_times[operation]
        
        self.metrics[operation] = self.metrics.get(operation, [])
        self.metrics[operation].append(duration)
        
        self.logger.info("Operation '" + operation + "' completed in " + str(round(duration, 3)) + "s")
        return duration
        
    def get_metrics(self) -> Dict[str, Any]:
        """Get performance metrics"""
        summary = {}
        for operation, times in self.metrics.items():
            if times:
                summary[operation] = {
                    'count': len(times),
                    'total_time': sum(times),
                    'avg_time': sum(times) / len(times),
                    'min_time': min(times),
                    'max_time': max(times)
                }
        return summary
        
    def log_performance_report(self):
        """Log a performance report"""
        report = self.get_metrics()
        self.logger.info("Performance Report:")
        for operation, stats in report.items():
            self.logger.info(
                "  " + operation + ": " + str(stats['count']) + " ops, " +
                "avg: " + str(round(stats['avg_time'], 3)) + "s, " +
                "min: " + str(round(stats['min_time'], 3)) + "s, " +
                "max: " + str(round(stats['max_time'], 3)) + "s"
            )


class HealthChecker:
    """Monitor platform health and availability"""
    
    def __init__(self, logger: logging.Logger = None):
        """Initialize health checker"""
        self.logger = logger or logging.getLogger("tiapmaatzu.health")
        self.checks = {}
        
    def register_check(self, name: str, check_function):
        """Register a health check function"""
        self.checks[name] = check_function
        self.logger.debug("Registered health check: " + name)
        
    def run_check(self, name: str) -> Dict[str, Any]:
        """Run a specific health check"""
        if name not in self.checks:
            return {
                'name': name,
                'status': 'unknown',
                'error': 'Check not registered'
            }
        
        try:
            result = self.checks[name]()
            return {
                'name': name,
                'status': 'healthy' if result else 'unhealthy',
                'result': result,
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            self.logger.error("Health check '" + name + "' failed: " + str(e))
            return {
                'name': name,
                'status': 'error',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
            
    def run_all_checks(self) -> Dict[str, Any]:
        """Run all registered health checks"""
        results = {}
        overall_healthy = True
        
        for name in self.checks:
            result = self.run_check(name)
            results[name] = result
            
            if result['status'] != 'healthy':
                overall_healthy = False
                
        return {
            'overall_status': 'healthy' if overall_healthy else 'unhealthy',
            'timestamp': datetime.now().isoformat(),
            'checks': results
        }


def setup_logging_config():
    """Create logging configuration file"""
    config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S'
            },
            'detailed': {
                'format': '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S'
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': 'INFO',
                'formatter': 'standard',
                'stream': 'ext://sys.stdout'
            },
            'file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'level': 'INFO',
                'formatter': 'detailed',
                'filename': 'logs/tiapmaatzu.log',
                'maxBytes': 10485760,  # 10MB
                'backupCount': 5
            },
            'error_file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'level': 'ERROR',
                'formatter': 'detailed',
                'filename': 'logs/errors.log',
                'maxBytes': 5242880,  # 5MB
                'backupCount': 3
            }
        },
        'loggers': {
            'tiapmaatzu': {
                'handlers': ['console', 'file', 'error_file'],
                'level': 'INFO',
                'propagate': False
            }
        }
    }
    
    config_file = Path(__file__).parent / "logging_config.json"
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"✓ Logging configuration created: {config_file}")
    return str(config_file)


def main():
    """Main entry point for logging setup"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Set up monitoring and logging for Tiapma'atzu platform")
    parser.add_argument('--log-dir', help='Directory for log files', default='logs')
    parser.add_argument('--log-level', help='Logging level', default='INFO')
    parser.add_argument('--create-config', action='store_true', help='Create logging config file')
    
    args = parser.parse_args()
    
    if args.create_config:
        setup_logging_config()
    else:
        platform_logger = PlatformLogger(args.log_dir, args.log_level)
        logger = platform_logger.get_logger()
        
        # Test logging
        logger.debug("Debug message test")
        logger.info("Info message test")
        logger.warning("Warning message test")
        logger.error("Error message test")
        
        # Test audit logging
        platform_logger.audit("System startup", component="logging_setup")
        
        # Test performance monitoring
        perf_monitor = PerformanceMonitor(logger)
        perf_monitor.start_timer("test_operation")
        import time
        time.sleep(0.1)
        perf_monitor.end_timer("test_operation")
        perf_monitor.log_performance_report()
        
        print(f"✓ Logging system initialized in {args.log_dir}")
        print(f"  Log level: {args.log_level}")
        print(f"  Log files: tiapmaatzu.log, errors.log, audit.log")


if __name__ == "__main__":
    main()