"""
Shared Utilities Module
Common functions and classes used across the Tiapma'atzu platform modules
"""

import json
import hashlib
import logging
import shutil
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Callable, Tuple
from pathlib import Path
from functools import wraps


class Configuration:
    """Centralized configuration constants"""
    
    # File paths
    DEFAULT_DATA_DIR = Path(__file__).parent.parent / "data"
    DEFAULT_SOULS_DATA = DEFAULT_DATA_DIR / "souls_entities.json"
    DEFAULT_CASHINGHOUSE_DATA = DEFAULT_DATA_DIR / "cashinghouse.json"
    
    # Fallback paths for different directory structures
    ALT_DATA_DIR = Path(__file__).parent.parent.parent.parent / "src" / "data"
    ALT_SOULS_DATA = ALT_DATA_DIR / "souls_entities.json"
    
    # Backup settings
    BACKUP_DIR_NAME = "backups"
    DEFAULT_BACKUP_COUNT = 10
    BACKUP_PREFIX = "backup_"
    
    # Validation limits
    MAX_TRANSACTION_AMOUNT = 1_000_000
    MAX_DESCRIPTION_LENGTH = 500
    MIN_DESCRIPTION_LENGTH = 1
    
    # Platform character limits
    PLATFORM_CHAR_LIMITS = {
        'Twitter': 160,
        'X': 160,
        'Instagram': 150,
        'TikTok': 150,
        'FetLife': 500,
        'YouTube': 5000,
        'Discord': 2000
    }
    
    # Platform token limits
    PLATFORM_TOKEN_LIMITS = {
        'Twitter': 280,
        'Instagram': 2200,
        'TikTok': 500,
        'YouTube': 5000,
        'FetLife': 10000,
        'Discord': 2000
    }
    
    # Content generation settings
    DEFAULT_AI_MODEL = "gpt-3.5-turbo"
    DEFAULT_TEMPERATURE = 0.7
    DEFAULT_MAX_TOKENS = 1000
    FALLBACK_MAX_TOKENS = 1000
    
    # Analytics periods
    DEFAULT_ANALYTICS_DAYS = 30
    TREND_ANALYSIS_DAYS = 7


class DataUtils:
    """Utility functions for data operations"""
    
    @staticmethod
    def load_json_file(file_path: Path) -> Dict[str, Any]:
        """
        Load JSON file with error handling
        
        Args:
            file_path: Path to JSON file
            
        Returns:
            Parsed JSON data as dictionary
            
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If JSON is invalid
        """
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Data file not found: {file_path}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in file {file_path}: {e}")
    
    @staticmethod
    def save_json_file(data: Dict[str, Any], file_path: Path, indent: int = 2) -> None:
        """
        Save data to JSON file with error handling
        
        Args:
            data: Data to save
            file_path: Target file path
            indent: JSON indentation level
            
        Raises:
            IOError: If file cannot be written
        """
        try:
            # Ensure directory exists
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=indent, default=str)
        except Exception as e:
            raise IOError(f"Failed to save data to {file_path}: {e}")
    
    @staticmethod
    def calculate_file_hash(file_path: Path) -> str:
        """
        Calculate MD5 hash of a file
        
        Args:
            file_path: Path to file
            
        Returns:
            MD5 hash as hexadecimal string
        """
        with open(file_path, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    
    @staticmethod
    def create_backup(
        source_path: Path, 
        backup_dir: Path, 
        prefix: str = Configuration.BACKUP_PREFIX
    ) -> Tuple[Path, Dict[str, Any]]:
        """
        Create a backup of a file with metadata
        
        Args:
            source_path: Path to file to backup
            backup_dir: Directory to store backup
            prefix: Backup filename prefix
            
        Returns:
            Tuple of (backup_path, metadata)
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"{prefix}{Path(source_path).stem}_{timestamp}.json"
        backup_path = backup_dir / backup_filename
        
        # Calculate file hash
        file_hash = DataUtils.calculate_file_hash(source_path)
        
        # Copy file
        shutil.copy2(source_path, backup_path)
        
        # Create metadata
        metadata = {
            'original_file': str(source_path),
            'backup_file': str(backup_path),
            'timestamp': timestamp,
            'file_hash': file_hash,
            'created_at': datetime.now().isoformat()
        }
        
        # Save metadata
        metadata_path = backup_path.with_suffix('.metadata.json')
        DataUtils.save_json_file(metadata, metadata_path)
        
        return backup_path, metadata
    
    @staticmethod
    def cleanup_old_backups(
        backup_dir: Path, 
        prefix: str = Configuration.BACKUP_PREFIX,
        keep_count: int = Configuration.DEFAULT_BACKUP_COUNT
    ) -> List[Path]:
        """
        Remove old backups, keeping only the most recent ones
        
        Args:
            backup_dir: Directory containing backups
            prefix: Backup filename prefix
            keep_count: Number of backups to keep
            
        Returns:
            List of removed backup paths
        """
        if not backup_dir.exists():
            return []
        
        # Get all backup files
        backup_files = sorted(
            backup_dir.glob(f"{prefix}*.json"),
            key=lambda x: x.stat().st_mtime,
            reverse=True
        )
        
        # Remove old backups
        removed_files = []
        for old_backup in backup_files[keep_count:]:
            old_backup.unlink()
            removed_files.append(old_backup)
            
            # Remove metadata file if exists
            metadata_file = old_backup.with_suffix('.metadata.json')
            if metadata_file.exists():
                metadata_file.unlink()
        
        return removed_files


class DateUtils:
    """Utility functions for date/time operations"""
    
    @staticmethod
    def format_timestamp(dt: datetime, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
        """
        Format datetime to string
        
        Args:
            dt: Datetime object
            format_str: Format string
            
        Returns:
            Formatted datetime string
        """
        return dt.strftime(format_str)
    
    @staticmethod
    def parse_timestamp(timestamp_str: str) -> datetime:
        """
        Parse timestamp string to datetime
        
        Args:
            timestamp_str: ISO format timestamp string
            
        Returns:
            Datetime object
        """
        return datetime.fromisoformat(timestamp_str)
    
    @staticmethod
    def get_date_range(days: int) -> Tuple[datetime, datetime]:
        """
        Get date range for last N days
        
        Args:
            days: Number of days
            
        Returns:
            Tuple of (start_date, end_date)
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        return start_date, end_date
    
    @staticmethod
    def get_month_start() -> datetime:
        """Get start of current month"""
        now = datetime.now()
        return now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)


class ValidationUtils:
    """Utility functions for data validation"""
    
    @staticmethod
    def validate_required_fields(data: Dict[str, Any], required_fields: List[str]) -> List[str]:
        """
        Validate that required fields are present and non-empty
        
        Args:
            data: Data dictionary to validate
            required_fields: List of required field names
            
        Returns:
            List of validation error messages
        """
        errors = []
        for field in required_fields:
            if field not in data or not data[field]:
                errors.append(f"Missing or empty required field: {field}")
        return errors
    
    @staticmethod
    def validate_field_types(data: Dict[str, Any], type_requirements: Dict[str, type]) -> List[str]:
        """
        Validate field types
        
        Args:
            data: Data dictionary to validate
            type_requirements: Dictionary mapping field names to expected types
            
        Returns:
            List of validation error messages
        """
        errors = []
        for field, expected_type in type_requirements.items():
            if field in data and not isinstance(data[field], expected_type):
                errors.append(f"Field '{field}' must be of type {expected_type.__name__}")
        return errors
    
    @staticmethod
    def validate_numeric_range(
        value: float, 
        min_val: Optional[float] = None, 
        max_val: Optional[float] = None,
        field_name: str = "value"
    ) -> List[str]:
        """
        Validate numeric value is within range
        
        Args:
            value: Numeric value to validate
            min_val: Minimum allowed value (None for no minimum)
            max_val: Maximum allowed value (None for no maximum)
            field_name: Name of field for error messages
            
        Returns:
            List of validation error messages
        """
        errors = []
        if min_val is not None and value < min_val:
            errors.append(f"{field_name} must be >= {min_val}")
        if max_val is not None and value > max_val:
            errors.append(f"{field_name} must be <= {max_val}")
        return errors
    
    @staticmethod
    def validate_string_length(
        value: str, 
        min_length: Optional[int] = None, 
        max_length: Optional[int] = None,
        field_name: str = "string"
    ) -> List[str]:
        """
        Validate string length
        
        Args:
            value: String to validate
            min_length: Minimum length (None for no minimum)
            max_length: Maximum length (None for no maximum)
            field_name: Name of field for error messages
            
        Returns:
            List of validation error messages
        """
        errors = []
        if min_length is not None and len(value) < min_length:
            errors.append(f"{field_name} must be at least {min_length} characters")
        if max_length is not None and len(value) > max_length:
            errors.append(f"{field_name} must be at most {max_length} characters")
        return errors


class ErrorUtils:
    """Utility functions for error handling"""
    
    @staticmethod
    def handle_errors(error_types: Tuple[type, ...] = (Exception,), default_return: Any = None) -> Callable:
        """
        Decorator for handling common error patterns
        
        Args:
            error_types: Tuple of exception types to catch
            default_return: Value to return on error
            
        Returns:
            Decorator function
        """
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args: Any, **kwargs: Any) -> Any:
                try:
                    return func(*args, **kwargs)
                except error_types as e:
                    logging.getLogger(__name__).error(f"Error in {func.__name__}: {e}")
                    return default_return
            return wrapper
        return decorator


class LoggingUtils:
    """Utility functions for logging setup"""
    
    @staticmethod
    def setup_logger(
        name: str, 
        level: int = logging.INFO,
        log_file: Optional[Path] = None
    ) -> logging.Logger:
        """
        Set up a logger with consistent formatting
        
        Args:
            name: Logger name
            level: Logging level
            log_file: Optional file path for file logging
            
        Returns:
            Configured logger instance
        """
        logger = logging.getLogger(name)
        logger.setLevel(level)
        
        # Remove existing handlers
        logger.handlers.clear()
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        # File handler if specified
        if log_file:
            log_file.parent.mkdir(parents=True, exist_ok=True)
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(level)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        
        return logger


class StringUtils:
    """Utility functions for string operations"""
    
    @staticmethod
    def truncate_text(text: str, max_length: int, suffix: str = "...") -> str:
        """
        Truncate text to maximum length with suffix
        
        Args:
            text: Text to truncate
            max_length: Maximum length
            suffix: Suffix to add if truncated
            
        Returns:
            Truncated text
        """
        if len(text) <= max_length:
            return text
        return text[:max_length - len(suffix)] + suffix
    
    @staticmethod
    def normalize_string(text: str) -> str:
        """
        Normalize string for comparison (lowercase, strip whitespace)
        
        Args:
            text: Text to normalize
            
        Returns:
            Normalized string
        """
        return text.lower().strip()
    
    @staticmethod
    def generate_id(prefix: str = "id") -> str:
        """
        Generate unique ID with prefix
        
        Args:
            prefix: ID prefix
            
        Returns:
            Unique ID string
        """
        timestamp = datetime.now().timestamp()
        return f"{prefix}_{timestamp}"