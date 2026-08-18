"""
API Middleware Module
Provides rate limiting, caching, authentication, and other middleware for the API server
"""

import os
import json
import time
from datetime import datetime, timedelta
from typing import Dict, Optional, Any, Callable
from functools import wraps
from flask import request, jsonify, g
import redis
import logging

from .utils import LoggingUtils

# Configure logging
logger = LoggingUtils.setup_logger(__name__)


class RateLimiter:
    """Rate limiting middleware for API endpoints"""
    
    def __init__(self, app=None):
        self.limiter = None
        self.request_counts = {}
        self.default_limit = 60  # requests per minute
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize rate limiter with Flask app"""
        # Get rate limit from environment or use default
        self.default_limit = int(os.getenv('RATE_LIMIT_PER_MINUTE', '60'))
        
        # Simple in-memory rate limiting
        # For production, this should use Redis
        logger.info(f"Rate limiter initialized with default limit: {self.default_limit} per minute")
    
    def _get_client_id(self):
        """Get client identifier for rate limiting"""
        return request.remote_addr
    
    def _cleanup_old_requests(self):
        """Clean up old request counts"""
        current_time = time.time()
        cutoff_time = current_time - 60  # 1 minute window
        
        for client_id in list(self.request_counts.keys()):
            # Remove timestamps older than 1 minute
            self.request_counts[client_id] = [
                timestamp for timestamp in self.request_counts[client_id]
                if timestamp > cutoff_time
            ]
            
            # Remove empty entries
            if not self.request_counts[client_id]:
                del self.request_counts[client_id]
    
    def check_rate_limit(self, limit: int = None) -> bool:
        """Check if request is within rate limit"""
        client_id = self._get_client_id()
        limit = limit or self.default_limit
        
        # Clean up old requests
        self._cleanup_old_requests()
        
        # Get current request count for client
        if client_id not in self.request_counts:
            self.request_counts[client_id] = []
        
        current_count = len(self.request_counts[client_id])
        
        if current_count >= limit:
            return False
        
        # Add current request
        self.request_counts[client_id].append(time.time())
        return True
    
    def limit(self, limit: int = None):
        """Decorator to apply custom rate limit to endpoint"""
        def decorator(f):
            @wraps(f)
            def wrapper(*args, **kwargs):
                if not self.check_rate_limit(limit):
                    return jsonify({
                        'error': 'Rate limit exceeded',
                        'message': 'Too many requests, please try again later'
                    }), 429
                return f(*args, **kwargs)
            return wrapper
        return decorator


class CacheManager:
    """Caching layer for API responses"""
    
    def __init__(self, app=None):
        self.redis_client = None
        self.in_memory_cache = {}
        self.cache_expiry = {}
        self.use_redis = False
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize cache with Flask app"""
        redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
        
        try:
            # Try to connect to Redis
            self.redis_client = redis.from_url(redis_url, decode_responses=True)
            self.redis_client.ping()
            self.use_redis = True
            logger.info(f"Cache initialized with Redis: {redis_url}")
        except Exception as e:
            logger.warning(f"Redis connection failed, using in-memory cache: {e}")
            self.use_redis = False
            logger.info("Cache initialized with in-memory fallback")
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        try:
            if self.use_redis and self.redis_client:
                cached = self.redis_client.get(key)
                if cached:
                    return json.loads(cached)
                return None
            else:
                # Check if key exists and hasn't expired
                if key in self.in_memory_cache:
                    if key in self.cache_expiry:
                        if time.time() < self.cache_expiry[key]:
                            return self.in_memory_cache[key]
                        else:
                            # Expired, remove it
                            del self.in_memory_cache[key]
                            del self.cache_expiry[key]
                    else:
                        return self.in_memory_cache[key]
                return None
        except Exception as e:
            logger.error(f"Cache get error: {e}")
            return None
    
    def set(self, key: str, value: Any, timeout: int = 300):
        """Set value in cache"""
        try:
            if self.use_redis and self.redis_client:
                self.redis_client.setex(key, timeout, json.dumps(value))
            else:
                self.in_memory_cache[key] = value
                self.cache_expiry[key] = time.time() + timeout
        except Exception as e:
            logger.error(f"Cache set error: {e}")
    
    def delete(self, key: str):
        """Delete value from cache"""
        try:
            if self.use_redis and self.redis_client:
                self.redis_client.delete(key)
            else:
                if key in self.in_memory_cache:
                    del self.in_memory_cache[key]
                if key in self.cache_expiry:
                    del self.cache_expiry[key]
        except Exception as e:
            logger.error(f"Cache delete error: {e}")
    
    def clear(self):
        """Clear all cache"""
        try:
            if self.use_redis and self.redis_client:
                self.redis_client.flushdb()
            else:
                self.in_memory_cache.clear()
                self.cache_expiry.clear()
        except Exception as e:
            logger.error(f"Cache clear error: {e}")
    
    def cached(self, timeout: int = 300, key_prefix: str = ""):
        """Decorator to cache function results"""
        def decorator(f):
            @wraps(f)
            def wrapper(*args, **kwargs):
                # Generate cache key
                cache_key = f"{key_prefix}{f.__name__}_{str(args)}_{str(kwargs)}"
                
                # Try to get from cache
                cached_result = self.get(cache_key)
                if cached_result is not None:
                    logger.debug(f"Cache hit for key: {cache_key}")
                    return cached_result
                
                # Execute function and cache result
                result = f(*args, **kwargs)
                self.set(cache_key, result, timeout)
                logger.debug(f"Cache miss for key: {cache_key}")
                
                return result
            return wrapper
        return decorator


class RequestLogger:
    """Request logging middleware"""
    
    def __init__(self, app=None):
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize request logger with Flask app"""
        @app.before_request
        def log_request_info():
            g.start_time = time.time()
            logger.info(f"Request: {request.method} {request.path} from {request.remote_addr}")
        
        @app.after_request
        def log_response_info(response):
            if hasattr(g, 'start_time'):
                duration = time.time() - g.start_time
                logger.info(
                    f"Response: {request.method} {request.path} - "
                    f"Status: {response.status_code} - "
                    f"Duration: {duration:.3f}s"
                )
            return response


class AuthMiddleware:
    """Authentication middleware for API endpoints"""
    
    def __init__(self, app=None):
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize auth middleware with Flask app"""
        # Firebase Auth integration would go here
        logger.info("Auth middleware initialized")
    
    def require_auth(self, f):
        """Decorator to require authentication for endpoint"""
        @wraps(f)
        def wrapper(*args, **kwargs):
            # Check for Authorization header
            auth_header = request.headers.get('Authorization')
            
            if not auth_header:
                return jsonify({'error': 'Authorization header required'}), 401
            
            # Validate token (implement Firebase Auth validation here)
            # For now, just check if header exists
            if not auth_header.startswith('Bearer '):
                return jsonify({'error': 'Invalid authorization format'}), 401
            
            # Extract and validate token
            token = auth_header.split(' ')[1]
            
            # TODO: Implement Firebase Auth token validation
            # For development, we'll skip actual validation
            logger.debug(f"Auth check for token: {token[:10]}...")
            
            return f(*args, **kwargs)
        
        return wrapper
    
    def optional_auth(self, f):
        """Decorator for optional authentication"""
        @wraps(f)
        def wrapper(*args, **kwargs):
            auth_header = request.headers.get('Authorization')
            user = None
            
            if auth_header and auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
                # TODO: Validate token and get user info
                user = {'id': 'dev_user'}  # Placeholder
            
            g.user = user
            return f(*args, **kwargs)
        
        return wrapper


class ErrorHandler:
    """Centralized error handling middleware"""
    
    def __init__(self, app=None):
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize error handler with Flask app"""
        
        @app.errorhandler(400)
        def bad_request(error):
            logger.warning(f"Bad request: {error}")
            return jsonify({'error': 'Bad request', 'message': str(error)}), 400
        
        @app.errorhandler(401)
        def unauthorized(error):
            logger.warning(f"Unauthorized access: {error}")
            return jsonify({'error': 'Unauthorized', 'message': str(error)}), 401
        
        @app.errorhandler(403)
        def forbidden(error):
            logger.warning(f"Forbidden access: {error}")
            return jsonify({'error': 'Forbidden', 'message': str(error)}), 403
        
        @app.errorhandler(404)
        def not_found(error):
            logger.info(f"Not found: {error}")
            return jsonify({'error': 'Not found', 'message': str(error)}), 404
        
        @app.errorhandler(429)
        def rate_limited(error):
            logger.warning(f"Rate limited: {error}")
            return jsonify({
                'error': 'Rate limit exceeded',
                'message': 'Too many requests, please try again later'
            }), 429
        
        @app.errorhandler(500)
        def internal_error(error):
            logger.error(f"Internal server error: {error}")
            return jsonify({
                'error': 'Internal server error',
                'message': 'An unexpected error occurred'
            }), 500
        
        logger.info("Error handlers initialized")


class CORSMiddleware:
    """Enhanced CORS middleware"""
    
    def __init__(self, app=None):
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize CORS with Flask app"""
        # CORS is already handled by flask-cors in api_server.py
        # This can be extended for more complex CORS policies
        logger.info("CORS middleware initialized")


class MetricsCollector:
    """API metrics collection middleware"""
    
    def __init__(self, app=None):
        self.metrics = {
            'requests_total': 0,
            'requests_by_endpoint': {},
            'requests_by_method': {},
            'response_times': [],
            'errors': 0
        }
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize metrics collector with Flask app"""
        @app.before_request
        def before_request():
            g.request_start_time = time.time()
        
        @app.after_request
        def after_request(response):
            if hasattr(g, 'request_start_time'):
                duration = time.time() - g.request_start_time
                
                # Update metrics
                self.metrics['requests_total'] += 1
                
                # Track by endpoint
                endpoint = request.path
                self.metrics['requests_by_endpoint'][endpoint] = \
                    self.metrics['requests_by_endpoint'].get(endpoint, 0) + 1
                
                # Track by method
                method = request.method
                self.metrics['requests_by_method'][method] = \
                    self.metrics['requests_by_method'].get(method, 0) + 1
                
                # Track response times
                self.metrics['response_times'].append(duration)
                
                # Track errors
                if response.status_code >= 400:
                    self.metrics['errors'] += 1
            
            return response
        
        logger.info("Metrics collector initialized")
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get current metrics"""
        response_times = self.metrics['response_times']
        avg_response_time = sum(response_times) / len(response_times) if response_times else 0
        
        return {
            'requests_total': self.metrics['requests_total'],
            'requests_by_endpoint': self.metrics['requests_by_endpoint'],
            'requests_by_method': self.metrics['requests_by_method'],
            'average_response_time': avg_response_time,
            'error_rate': self.metrics['errors'] / max(self.metrics['requests_total'], 1),
            'total_errors': self.metrics['errors']
        }
    
    def reset_metrics(self):
        """Reset all metrics"""
        self.metrics = {
            'requests_total': 0,
            'requests_by_endpoint': {},
            'requests_by_method': {},
            'response_times': [],
            'errors': 0
        }


def init_middleware(app):
    """Initialize all middleware for the Flask app"""
    
    # Initialize rate limiter
    rate_limiter = RateLimiter(app)
    
    # Initialize cache
    cache_manager = CacheManager(app)
    
    # Initialize request logger
    request_logger = RequestLogger(app)
    
    # Initialize auth middleware
    auth_middleware = AuthMiddleware(app)
    
    # Initialize error handler
    error_handler = ErrorHandler(app)
    
    # Initialize CORS middleware
    cors_middleware = CORSMiddleware(app)
    
    # Initialize metrics collector
    metrics_collector = MetricsCollector(app)
    
    # Store middleware instances in app config for later use
    app.config['rate_limiter'] = rate_limiter
    app.config['cache_manager'] = cache_manager
    app.config['auth_middleware'] = auth_middleware
    app.config['metrics_collector'] = metrics_collector
    
    logger.info("All middleware initialized successfully")
    
    return {
        'rate_limiter': rate_limiter,
        'cache_manager': cache_manager,
        'auth_middleware': auth_middleware,
        'metrics_collector': metrics_collector
    }
