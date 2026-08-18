"""
Tiapma'atzu API Server
Python-based backend as free alternative to Firebase Cloud Functions
Provides REST API endpoints for soul management, financial operations, and analytics
"""

import os
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import Firebase Admin
import firebase_admin
from firebase_admin import credentials, firestore, auth as firebase_auth

# Import Tiapma'atzu modules
from src.modules.souls_manager import SoulsManager
from src.modules.cashinghouse import CashingHouse
from src.modules.souls_financial_integration import SoulsFinancialIntegration
from src.modules.analytics_dashboard import AnalyticsDashboard
from src.modules.utils import Configuration
from src.modules.middleware import init_middleware
from src.modules.websocket_handler import get_websocket_manager, get_notification_manager
from src.modules.task_scheduler import get_scheduler, init_default_tasks
from src.modules.ai_content_generator import AIContentGenerator
from src.modules.openrouter_integration import OpenRouterIntegration, ContentRequest
from src.modules.content_pipeline import ContentPipeline
from src.modules.shadow_work import ShadowWorkManager

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize Firebase Admin
def initialize_firebase():
    """Initialize Firebase Admin SDK"""
    try:
        # Check if already initialized
        if not firebase_admin._apps:
            cred_path = os.getenv('FIREBASE_SERVICE_ACCOUNT_KEY')
            if cred_path and Path(cred_path).exists():
                cred = credentials.Certificate(cred_path)
                firebase_admin.initialize_app(cred)
                print("✓ Firebase Admin initialized (from env variable)")
            else:
                # Try default service account file
                default_cred = Path("tiapmaatzu-firebase-adminsdk-fbsvc-db8f709411.json")
                if default_cred.exists():
                    cred = credentials.Certificate(str(default_cred))
                    firebase_admin.initialize_app(cred)
                    print("✓ Firebase Admin initialized (default key)")
                else:
                    print("⚠ Firebase service account key not found, running in client-only mode")
                    print("  Admin SDK features will be disabled. Client SDK will still work.")
        return True
    except Exception as e:
        print(f"✗ Firebase initialization error: {e}")
        print("  Continuing in degraded mode...")
        return False

# Initialize Firebase
initialize_firebase()

# Get Firestore client
try:
    if firebase_admin._apps:
        db = firestore.client()
        print("✓ Firestore client initialized")
    else:
        db = None
        print("⚠ Firestore client not available (Admin SDK not initialized)")
except Exception as e:
    print(f"✗ Firestore client error: {e}")
    db = None

# Get Auth client
try:
    if firebase_admin._apps:
        auth_client = firebase_auth
        print("✓ Firebase Auth client initialized")
    else:
        auth_client = None
        print("⚠ Firebase Auth client not available (Admin SDK not initialized)")
except Exception as e:
    print(f"✗ Firebase Auth client error: {e}")
    auth_client = None

# Initialize Tiapma'atzu components
def initialize_components():
    """Initialize Tiapma'atzu components"""
    try:
        # Create backup directory if it doesn't exist
        backup_dir = Path("backups")
        backup_dir.mkdir(exist_ok=True)
        
        souls_manager = SoulsManager()
        cashinghouse = CashingHouse()
        financial_integration = SoulsFinancialIntegration(souls_manager)
        analytics = AnalyticsDashboard(souls_manager, cashinghouse, financial_integration)
        print("✓ Tiapma'atzu components initialized")
        return souls_manager, cashinghouse, financial_integration, analytics
    except Exception as e:
        print(f"✗ Component initialization error: {e}")
        return None, None, None, None

def initialize_ai_components():
    """Initialize AI content generation components"""
    try:
        if souls_manager:
            ai_generator = AIContentGenerator(souls_manager)
            openrouter = OpenRouterIntegration(souls_manager)
            content_pipeline = ContentPipeline(souls_manager, openrouter, ai_generator)
            
            # Load saved calendars if they exist
            calendars_dir = Path("config/calendars")
            if calendars_dir.exists():
                for calendar_file in calendars_dir.glob("*.json"):
                    try:
                        with open(calendar_file, 'r') as f:
                            calendar_data = json.load(f)
                        
                        # Reconstruct ContentCalendar and ContentSchedule objects
                        from src.modules.content_pipeline import ContentCalendar, ContentSchedule, ContentFrequency
                        
                        schedules = []
                        for schedule_data in calendar_data.get('schedules', []):
                            schedule = ContentSchedule(
                                soul_id=schedule_data['soul_id'],
                                platform=schedule_data['platform'],
                                content_type=schedule_data['content_type'],
                                frequency=ContentFrequency(schedule_data['frequency']),
                                preferred_times=schedule_data['preferred_times'],
                                active=schedule_data['active'],
                                last_generated=schedule_data['last_generated'],
                                next_due=schedule_data['next_due']
                            )
                            schedules.append(schedule)
                        
                        calendar = ContentCalendar(
                            calendar_id=calendar_data['calendar_id'],
                            name=calendar_data['name'],
                            schedules=schedules,
                            created_at=calendar_data['created_at'],
                            updated_at=calendar_data['updated_at']
                        )
                        
                        content_pipeline.calendars[calendar.calendar_id] = calendar
                        print(f"✓ Loaded calendar: {calendar.name}")
                    except Exception as e:
                        print(f"⚠ Failed to load calendar {calendar_file}: {e}")
            
            print("✓ AI content generation components initialized")
            return ai_generator, openrouter, content_pipeline
        else:
            print("⚠ Souls manager not available, AI components disabled")
            return None, None, None
    except Exception as e:
        print(f"✗ AI component initialization error: {e}")
        return None, None, None

souls_manager, cashinghouse, financial_integration, analytics = initialize_components()
ai_generator, openrouter, content_pipeline = initialize_ai_components()

# Initialize Shadow Work Manager
def initialize_shadow_work():
    """Initialize Shadow Work / Persona Development Manager"""
    try:
        if souls_manager:
            shadow_work_manager = ShadowWorkManager(souls_manager)
            print("✓ Shadow Work Manager initialized")
            return shadow_work_manager
        else:
            print("⚠ Souls manager not available, Shadow Work disabled")
            return None
    except Exception as e:
        print(f"✗ Shadow Work initialization error: {e}")
        return None

shadow_work_manager = initialize_shadow_work()

# Initialize middleware
middleware = init_middleware(app)
rate_limiter = middleware['rate_limiter']
cache_manager = middleware['cache_manager']
auth_middleware = middleware['auth_middleware']
metrics_collector = middleware['metrics_collector']

# Initialize WebSocket manager
ws_manager = get_websocket_manager()
notification_manager = get_notification_manager()

# Initialize task scheduler
scheduler = get_scheduler()
init_default_tasks()
scheduler.start()

print("✓ Middleware, WebSocket, and Scheduler initialized")

# ============================================================================
# Authentication Middleware
# ============================================================================

def verify_firebase_token():
    """Verify Firebase ID token from Authorization header"""
    auth_header = request.headers.get('Authorization')
    
    if not auth_header:
        return None, {'error': 'No authorization header provided'}, 401
    
    if not auth_client:
        return None, {'error': 'Firebase Auth not initialized'}, 500
    
    try:
        # Remove 'Bearer ' prefix if present
        token = auth_header
        if token.startswith('Bearer '):
            token = token[7:]
        
        # Verify the token
        decoded_token = auth_client.verify_id_token(token)
        return decoded_token, None, None
        
    except firebase_auth.ExpiredIdTokenError:
        return None, {'error': 'Token expired'}, 401
    except firebase_auth.InvalidIdTokenError:
        return None, {'error': 'Invalid token'}, 401
    except firebase_auth.RevokedIdTokenError:
        return None, {'error': 'Token revoked'}, 401
    except Exception as e:
        return None, {'error': f'Token verification failed: {str(e)}'}, 401

def require_auth(f):
    """Decorator to require Firebase authentication"""
    def wrapper(*args, **kwargs):
        decoded_token, error, status = verify_firebase_token()
        if error:
            return jsonify(error), status
        request.user = decoded_token
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

# ============================================================================
# Health Check
# ============================================================================

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'firebase': db is not None,
        'auth': auth_client is not None,
        'components': {
            'souls_manager': souls_manager is not None,
            'cashinghouse': cashinghouse is not None,
            'financial_integration': financial_integration is not None,
            'analytics': analytics is not None
        }
    })

@app.route('/api/auth/verify', methods=['POST'])
def verify_auth():
    """Verify Firebase authentication token"""
    decoded_token, error, status = verify_firebase_token()
    if error:
        return jsonify(error), status
    
    return jsonify({
        'verified': True,
        'user_id': decoded_token.get('uid'),
        'email': decoded_token.get('email'),
        'email_verified': decoded_token.get('email_verified'),
        'sign_in_provider': decoded_token.get('firebase', {}).get('sign_in_provider')
    })

# ============================================================================
# Soul Management Endpoints
# ============================================================================

@app.route('/api/souls', methods=['GET'])
def get_souls():
    """Get all souls"""
    if not souls_manager:
        return jsonify({'error': 'Souls manager not initialized'}), 500
    
    try:
        souls = souls_manager.get_all_souls()
        return jsonify({
            'souls': [soul.__dict__ for soul in souls],
            'count': len(souls)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/souls/<soul_id>', methods=['GET'])
def get_soul(soul_id):
    """Get a specific soul by ID"""
    if not souls_manager:
        return jsonify({'error': 'Souls manager not initialized'}), 500
    
    try:
        soul = souls_manager.get_soul_by_id(soul_id)
        if not soul:
            return jsonify({'error': 'Soul not found'}), 404
        return jsonify(soul.__dict__)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/souls/archetype/<archetype>', methods=['GET'])
def get_souls_by_archetype(archetype):
    """Get souls by archetype"""
    if not souls_manager:
        return jsonify({'error': 'Souls manager not initialized'}), 500
    
    try:
        souls = souls_manager.get_souls_by_archetype(archetype)
        return jsonify({
            'souls': [soul.__dict__ for soul in souls],
            'count': len(souls)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/souls/rarity/<rarity>', methods=['GET'])
def get_souls_by_rarity(rarity):
    """Get souls by rarity"""
    if not souls_manager:
        return jsonify({'error': 'Souls manager not initialized'}), 500
    
    try:
        souls = souls_manager.get_souls_by_rarity(rarity)
        return jsonify({
            'souls': [soul.__dict__ for soul in souls],
            'count': len(souls)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/souls/platform/<platform>', methods=['GET'])
def get_souls_by_platform(platform):
    """Get souls by platform"""
    if not souls_manager:
        return jsonify({'error': 'Souls manager not initialized'}), 500
    
    try:
        souls = souls_manager.get_souls_by_platform(platform)
        return jsonify({
            'souls': [soul.__dict__ for soul in souls],
            'count': len(souls)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/souls/search', methods=['GET'])
def search_souls():
    """Search souls by query"""
    if not souls_manager:
        return jsonify({'error': 'Souls manager not initialized'}), 500
    
    query = request.args.get('q', '')
    if not query:
        return jsonify({'error': 'Query parameter required'}), 400
    
    try:
        souls = souls_manager.search_souls(query)
        return jsonify({
            'souls': [soul.__dict__ for soul in souls],
            'count': len(souls)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/souls/statistics', methods=['GET'])
def get_souls_statistics():
    """Get souls statistics"""
    if not souls_manager:
        return jsonify({'error': 'Souls manager not initialized'}), 500
    
    try:
        stats = souls_manager.get_statistics()
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/souls/network', methods=['GET'])
def get_soul_network():
    """Get soul network map"""
    if not souls_manager:
        return jsonify({'error': 'Souls manager not initialized'}), 500
    
    try:
        network = souls_manager.get_soul_network_map()
        return jsonify(network)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================================================
# AI Content Generation Endpoints
# ============================================================================

@app.route('/api/ai/generate', methods=['POST'])
@require_auth
def generate_content():
    """Generate content for a soul using AI"""
    if not openrouter or not souls_manager:
        return jsonify({'error': 'AI components not initialized'}), 500
    
    try:
        data = request.json
        soul_id = data.get('soul_id')
        platform = data.get('platform')
        content_type = data.get('content_type', 'post')
        context = data.get('context')
        tone = data.get('tone')
        length = data.get('length', 'medium')
        
        if not soul_id or not platform:
            return jsonify({'error': 'soul_id and platform required'}), 400
        
        soul = souls_manager.get_soul_by_id(soul_id)
        if not soul:
            return jsonify({'error': 'Soul not found'}), 404
        
        request = ContentRequest(
            soul_id=soul_id,
            platform=platform,
            content_type=content_type,
            context=context,
            tone=tone,
            length=length
        )
        
        generated = openrouter.generate_soul_content(soul, request)
        
        return jsonify({
            'content': generated.content,
            'model_used': generated.model_used,
            'tokens_used': generated.tokens_used,
            'cost_estimate': generated.cost_estimate,
            'metadata': generated.metadata
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ai/batch', methods=['POST'])
@require_auth
def generate_batch_content():
    """Generate content for multiple souls in batch"""
    if not openrouter or not souls_manager:
        return jsonify({'error': 'AI components not initialized'}), 500
    
    try:
        data = request.json
        requests = data.get('requests', [])
        
        if not requests:
            return jsonify({'error': 'No requests provided'}), 400
        
        content_requests = [ContentRequest(**req) for req in requests]
        
        generated = openrouter.generate_batch_soul_content(content_requests)
        
        return jsonify({
            'generated_content': [g.__dict__ for g in generated],
            'count': len(generated),
            'total_cost': sum(g.cost_estimate or 0 for g in generated)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ai/campaign', methods=['POST'])
@require_auth
def generate_campaign():
    """Generate a coordinated content campaign"""
    if not content_pipeline or not souls_manager:
        return jsonify({'error': 'Content pipeline not initialized'}), 500
    
    try:
        data = request.json
        campaign_name = data.get('campaign_name', 'Untitled Campaign')
        soul_ids = data.get('soul_ids', [])
        platforms = data.get('platforms', [])
        content_types = data.get('content_types', ['post'])
        timeline_days = data.get('timeline_days', 7)
        
        if not soul_ids or not platforms:
            return jsonify({'error': 'soul_ids and platforms required'}), 400
        
        results = content_pipeline.generate_campaign(
            campaign_name, soul_ids, platforms, content_types, timeline_days
        )
        
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ai/pipeline/due', methods=['POST'])
@require_auth
def generate_due_content():
    """Generate content that is due based on pipeline schedules"""
    if not content_pipeline:
        return jsonify({'error': 'Content pipeline not initialized'}), 500
    
    try:
        calendar_id = request.json.get('calendar_id') if request.json else None
        generated = content_pipeline.generate_due_content(calendar_id)
        
        return jsonify({
            'generated_content': [g.__dict__ for g in generated],
            'count': len(generated)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ai/pipeline/stats', methods=['GET'])
def get_pipeline_stats():
    """Get content pipeline statistics"""
    if not content_pipeline:
        return jsonify({'error': 'Content pipeline not initialized'}), 500
    
    try:
        stats = content_pipeline.get_pipeline_statistics()
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ai/pipeline/optimize', methods=['GET'])
def optimize_pipeline():
    """Get pipeline optimization recommendations"""
    if not content_pipeline:
        return jsonify({'error': 'Content pipeline not initialized'}), 500
    
    try:
        optimization = content_pipeline.optimize_pipeline()
        return jsonify(optimization)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ai/models', methods=['GET'])
def get_available_models():
    """Get available AI models and their capabilities"""
    if not openrouter:
        return jsonify({'error': 'OpenRouter not initialized'}), 500
    
    try:
        models = openrouter.get_usage_statistics()
        return jsonify(models)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================================================
# Shadow Work / Persona Development Endpoints
# ============================================================================

@app.route('/api/shadow/initialize', methods=['POST'])
@require_auth
def initialize_shadow_aspects():
    """Initialize shadow aspects for a soul"""
    if not shadow_work_manager or not souls_manager:
        return jsonify({'error': 'Shadow Work Manager not initialized'}), 500

    try:
        data = request.json
        soul_id = data.get('soul_id')

        if not soul_id:
            return jsonify({'error': 'soul_id required'}), 400

        aspects = shadow_work_manager.initialize_soul_shadow_aspects(soul_id)

        return jsonify({
            'message': 'Shadow aspects initialized',
            'aspects_count': len(aspects),
            'aspects': [
                {
                    'aspect_id': a.aspect_id,
                    'name': a.name,
                    'archetype': a.archetype.value,
                    'integration_level': a.integration_level
                }
                for a in aspects
            ]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/shadow/dialogue', methods=['POST'])
@require_auth
def conduct_shadow_dialogue():
    """Conduct a dialogue session with a shadow aspect"""
    if not shadow_work_manager:
        return jsonify({'error': 'Shadow Work Manager not initialized'}), 500

    try:
        data = request.json
        soul_id = data.get('soul_id')
        aspect_id = data.get('aspect_id')
        question = data.get('question')

        if not all([soul_id, aspect_id, question]):
            return jsonify({'error': 'soul_id, aspect_id, and question required'}), 400

        dialogue = shadow_work_manager.conduct_shadow_dialogue(soul_id, aspect_id, question)

        return jsonify({
            'dialogue_id': dialogue.dialogue_id,
            'question': dialogue.question,
            'shadow_response': dialogue.shadow_response,
            'persona_response': dialogue.persona_response,
            'integration_insight': dialogue.integration_insight,
            'emotional_state': dialogue.emotional_state,
            'sovereignty_check': dialogue.sovereignty_check,
            'timestamp': dialogue.timestamp
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/shadow/report/<soul_id>', methods=['GET'])
def get_shadow_report(soul_id):
    """Get comprehensive shadow work report for a soul"""
    if not shadow_work_manager:
        return jsonify({'error': 'Shadow Work Manager not initialized'}), 500

    try:
        report = shadow_work_manager.get_shadow_report(soul_id)
        return jsonify(report)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/shadow/practice/recommend/<soul_id>', methods=['GET'])
def recommend_shadow_practice(soul_id):
    """Get recommended shadow work practice for a soul"""
    if not shadow_work_manager:
        return jsonify({'error': 'Shadow Work Manager not initialized'}), 500

    try:
        practice = shadow_work_manager.recommend_practice(soul_id)

        if not practice:
            return jsonify({'error': 'No practice recommended'}), 404

        return jsonify({
            'practice_id': practice.practice_id,
            'name': practice.name,
            'description': practice.description,
            'archetype': practice.archetype.value,
            'difficulty': practice.difficulty,
            'duration_minutes': practice.duration_minutes,
            'steps': practice.steps,
            'integration_focus': practice.integration_focus,
            'required_sovereignty': practice.required_sovereignty
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# AI Content Generation Endpoints
@app.route('/api/ai/generate', methods=['POST'])
def generate_ai_content():
    """Generate AI content for a soul on a specific platform"""
    if not openrouter:
        return jsonify({'error': 'OpenRouter integration not initialized'}), 500

    try:
        data = request.json
        soul_id = data.get('soul_id')
        platform = data.get('platform')
        content_type = data.get('content_type', 'post')
        context = data.get('context')
        tone = data.get('tone', 'authentic')
        length = data.get('length', 'medium')

        if not all([soul_id, platform]):
            return jsonify({'error': 'soul_id and platform required'}), 400

        soul = souls_manager.get_soul_by_id(soul_id)
        if not soul:
            return jsonify({'error': 'Soul not found'}), 404

        from src.modules.openrouter_integration import ContentRequest
        request = ContentRequest(
            soul_id=soul_id,
            platform=platform,
            content_type=content_type,
            context=context,
            tone=tone,
            length=length
        )

        generated = openrouter.generate_soul_content(soul, request)

        return jsonify({
            'soul_id': generated.soul_id,
            'platform': generated.platform,
            'content_type': generated.content_type,
            'content': generated.content,
            'model_used': generated.model_used,
            'tokens_used': generated.tokens_used,
            'cost_estimate': generated.cost_estimate,
            'generated_at': generated.generated_at,
            'metadata': generated.metadata
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/ai/generate/batch', methods=['POST'])
def generate_batch_ai_content():
    """Generate AI content for multiple souls in batch"""
    if not openrouter:
        return jsonify({'error': 'OpenRouter integration not initialized'}), 500

    try:
        data = request.json
        requests = data.get('requests', [])

        if not requests:
            return jsonify({'error': 'No requests provided'}), 400

        from src.modules.openrouter_integration import ContentRequest
        content_requests = [
            ContentRequest(
                soul_id=req.get('soul_id'),
                platform=req.get('platform'),
                content_type=req.get('content_type', 'post'),
                context=req.get('context'),
                tone=req.get('tone', 'authentic'),
                length=req.get('length', 'medium')
            )
            for req in requests
        ]

        generated_contents = openrouter.generate_batch_soul_content(content_requests)

        return jsonify({
            'generated_contents': [
                {
                    'soul_id': gc.soul_id,
                    'platform': gc.platform,
                    'content_type': gc.content_type,
                    'content': gc.content,
                    'model_used': gc.model_used,
                    'tokens_used': gc.tokens_used,
                    'cost_estimate': gc.cost_estimate,
                    'generated_at': gc.generated_at
                }
                for gc in generated_contents
            ],
            'total_generated': len(generated_contents),
            'total_cost': sum(gc.cost_estimate or 0 for gc in generated_contents)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/ai/stats', methods=['GET'])
def get_ai_stats():
    """Get AI content generation statistics"""
    if not openrouter:
        return jsonify({'error': 'OpenRouter integration not initialized'}), 500

    try:
        stats = openrouter.get_usage_statistics()
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Content Pipeline Endpoints
@app.route('/api/content/schedules', methods=['GET'])
def get_content_schedules():
    """Get all content schedules"""
    if not content_pipeline:
        return jsonify({'error': 'Content pipeline not initialized'}), 500

    try:
        schedules = []
        for calendar in content_pipeline.calendars.values():
            for schedule in calendar.schedules:
                schedules.append({
                    'soul_id': schedule.soul_id,
                    'platform': schedule.platform,
                    'content_type': schedule.content_type,
                    'frequency': schedule.frequency.value,
                    'preferred_times': schedule.preferred_times,
                    'active': schedule.active,
                    'last_generated': schedule.last_generated,
                    'next_due': schedule.next_due
                })

        return jsonify({'schedules': schedules, 'total': len(schedules)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/content/schedules/<soul_id>', methods=['PUT'])
def update_content_schedule(soul_id):
    """Update a content schedule"""
    if not content_pipeline:
        return jsonify({'error': 'Content pipeline not initialized'}), 500

    try:
        data = request.json
        active = data.get('active', True)

        # Find and update the schedule
        for calendar in content_pipeline.calendars.values():
            for schedule in calendar.schedules:
                if schedule.soul_id == soul_id:
                    schedule.active = active
                    return jsonify({'status': 'updated', 'soul_id': soul_id, 'active': active})

        return jsonify({'error': 'Schedule not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/content/generate-due', methods=['POST'])
def generate_scheduled_content():
    """Generate content that is due based on schedules"""
    if not content_pipeline:
        return jsonify({'error': 'Content pipeline not initialized'}), 500

    try:
        generated = content_pipeline.generate_due_content()

        return jsonify({
            'generated': [
                {
                    'soul_id': gc.soul_id,
                    'platform': gc.platform,
                    'content_type': gc.content_type,
                    'content': gc.content,
                    'model_used': gc.model_used
                }
                for gc in generated
            ],
            'total_generated': len(generated)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/content/campaign', methods=['POST'])
def generate_content_campaign():
    """Generate a coordinated content campaign"""
    if not content_pipeline:
        return jsonify({'error': 'Content pipeline not initialized'}), 500

    try:
        data = request.json
        campaign_name = data.get('campaign_name', 'Autonomous Campaign')
        soul_ids = data.get('soul_ids', [])
        platforms = data.get('platforms', [])
        content_types = data.get('content_types', ['post'])
        timeline_days = data.get('timeline_days', 7)

        results = content_pipeline.generate_campaign(
            campaign_name, soul_ids, platforms, content_types, timeline_days
        )

        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/content/stats', methods=['GET'])
def get_content_stats():
    """Get content pipeline statistics"""
    if not content_pipeline:
        return jsonify({'error': 'Content pipeline not initialized'}), 500

    try:
        stats = content_pipeline.get_pipeline_statistics()
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/shadow/practices', methods=['GET'])
def list_shadow_practices():
    """List all available shadow work practices"""
    if not shadow_work_manager:
        return jsonify({'error': 'Shadow Work Manager not initialized'}), 500

    try:
        practices = []
        for practice_id, practice in shadow_work_manager.practice_library.items():
            practices.append({
                'practice_id': practice.practice_id,
                'name': practice.name,
                'description': practice.description,
                'archetype': practice.archetype.value,
                'difficulty': practice.difficulty,
                'duration_minutes': practice.duration_minutes,
                'required_sovereignty': practice.required_sovereignty
            })

        return jsonify({'practices': practices, 'total': len(practices)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/shadow/save', methods=['POST'])
@require_auth
def save_shadow_data():
    """Save all shadow work data"""
    if not shadow_work_manager:
        return jsonify({'error': 'Shadow Work Manager not initialized'}), 500

    try:
        shadow_work_manager.save_shadow_data()
        return jsonify({'message': 'Shadow data saved successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================================================
# Financial Endpoints
# ============================================================================

@app.route('/api/financial/summary', methods=['GET'])
def get_financial_summary():
    """Get financial summary"""
    if not cashinghouse:
        return jsonify({'error': 'CashingHouse not initialized'}), 500
    
    try:
        summary = cashinghouse.get_financial_summary()
        return jsonify(summary.__dict__)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/financial/transactions', methods=['GET'])
def get_transactions():
    """Get all transactions"""
    if not cashinghouse:
        return jsonify({'error': 'CashingHouse not initialized'}), 500
    
    try:
        transactions = cashinghouse.get_all_transactions()
        return jsonify({
            'transactions': [t.__dict__ for t in transactions],
            'count': len(transactions)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/financial/tributes', methods=['POST'])
@require_auth
def add_tribute():
    """Add a tribute transaction (requires authentication)"""
    if not cashinghouse:
        return jsonify({'error': 'CashingHouse not initialized'}), 500
    
    try:
        data = request.json
        tribute = cashinghouse.record_tribute(
            soul_id=data.get('soul_id'),
            amount=data.get('amount'),
            impact_area=data.get('impact_area'),
            platform=data.get('platform'),
            metadata=data.get('metadata', {})
        )
        return jsonify(tribute.__dict__)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/financial/cash-flow', methods=['GET'])
def get_cash_flow():
    """Get cash flow analysis"""
    if not financial_integration:
        return jsonify({'error': 'Financial integration not initialized'}), 500
    
    try:
        days = int(request.args.get('days', 30))
        analysis = financial_integration.calculate_cash_flow_analysis(days)
        return jsonify(analysis)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/financial/forecast', methods=['GET'])
def get_financial_forecast():
    """Get financial forecast"""
    if not financial_integration:
        return jsonify({'error': 'Financial integration not initialized'}), 500
    
    try:
        days = int(request.args.get('days', 90))
        forecast = financial_integration.calculate_financial_forecast(days)
        return jsonify(forecast)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/financial/risk', methods=['GET'])
def get_financial_risk():
    """Get financial risk assessment"""
    if not financial_integration:
        return jsonify({'error': 'Financial integration not initialized'}), 500
    
    try:
        risk = financial_integration.assess_financial_risk()
        return jsonify(risk)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/financial/diversification', methods=['GET'])
def get_diversification():
    """Get revenue diversification analysis"""
    if not financial_integration:
        return jsonify({'error': 'Financial integration not initialized'}), 500
    
    try:
        diversification = financial_integration.calculate_revenue_diversification()
        return jsonify(diversification)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/financial/goals', methods=['GET'])
def get_financial_goals():
    """Get financial goals status"""
    if not financial_integration:
        return jsonify({'error': 'Financial integration not initialized'}), 500
    
    try:
        goals = financial_integration.track_financial_goals()
        return jsonify(goals)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================================================
# Analytics Endpoints
# ============================================================================

@app.route('/api/analytics/dashboard', methods=['GET'])
def get_dashboard():
    """Get analytics dashboard"""
    if not analytics:
        return jsonify({'error': 'Analytics not initialized'}), 500
    
    try:
        dashboard = analytics.get_comprehensive_dashboard()
        return jsonify(dashboard)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analytics/trends', methods=['GET'])
def get_trends():
    """Get trend analysis"""
    if not analytics:
        return jsonify({'error': 'Analytics not initialized'}), 500
    
    try:
        days = int(request.args.get('days', 30))
        trends = analytics.get_trend_analysis(days)
        return jsonify(trends)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analytics/comparison', methods=['GET'])
def get_comparison():
    """Get comparative analytics"""
    if not analytics:
        return jsonify({'error': 'Analytics not initialized'}), 500
    
    try:
        days = int(request.args.get('days', 30))
        comparison = analytics.get_comparative_analytics(days)
        return jsonify(comparison)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analytics/anomalies', methods=['GET'])
def get_anomalies():
    """Get anomaly detection"""
    if not analytics:
        return jsonify({'error': 'Analytics not initialized'}), 500
    
    try:
        anomalies = analytics.get_anomaly_detection()
        return jsonify(anomalies)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analytics/soul-performance', methods=['GET'])
def get_soul_performance():
    """Get detailed soul performance"""
    if not analytics:
        return jsonify({'error': 'Analytics not initialized'}), 500
    
    try:
        performance = analytics.get_detailed_soul_performance()
        return jsonify(performance)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analytics/archetype', methods=['GET'])
def get_archetype_performance():
    """Get archetype performance analysis"""
    if not analytics:
        return jsonify({'error': 'Analytics not initialized'}), 500
    
    try:
        archetype = analytics.get_archetype_performance_analysis()
        return jsonify(archetype)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analytics/network', methods=['GET'])
def get_network_analysis():
    """Get soul network analysis"""
    if not analytics:
        return jsonify({'error': 'Analytics not initialized'}), 500
    
    try:
        network = analytics.get_soul_network_analysis()
        return jsonify(network)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analytics/export', methods=['GET'])
def export_analytics():
    """Export analytics report"""
    if not analytics:
        return jsonify({'error': 'Analytics not initialized'}), 500
    
    try:
        format_type = request.args.get('format', 'json')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        report_path = analytics.export_analytics_report(
            format=format_type,
            start_date=start_date,
            end_date=end_date
        )
        
        return jsonify({
            'report_path': report_path,
            'format': format_type
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================================================
# Firestore Sync Endpoints
# ============================================================================

@app.route('/api/firestore/sync', methods=['POST'])
@require_auth
def sync_to_firestore():
    """Sync souls data to Firestore (requires authentication)"""
    if not db or not souls_manager:
        return jsonify({'error': 'Firestore or souls manager not initialized'}), 500
    
    try:
        souls = souls_manager.get_all_souls()
        synced_count = 0
        
        for soul in souls:
            doc_ref = db.collection('souls').document(soul.id)
            doc_ref.set(soul.__dict__)
            synced_count += 1
        
        return jsonify({
            'synced': synced_count,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/firestore/souls', methods=['GET'])
def get_firestore_souls():
    """Get souls from Firestore"""
    if not db:
        return jsonify({'error': 'Firestore not initialized'}), 500
    
    try:
        souls_ref = db.collection('souls')
        docs = souls_ref.stream()
        
        souls = []
        for doc in docs:
            souls.append({
                'id': doc.id,
                'data': doc.to_dict()
            })
        
        return jsonify({
            'souls': souls,
            'count': len(souls)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================================================
# Middleware Endpoints
# ============================================================================

@app.route('/api/metrics', methods=['GET'])
def get_metrics():
    """Get API metrics"""
    try:
        metrics = metrics_collector.get_metrics()
        return jsonify(metrics)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/cache/stats', methods=['GET'])
def get_cache_stats():
    """Get cache statistics"""
    try:
        stats = {
            'type': 'Redis' if cache_manager.use_redis else 'In-Memory',
            'enabled': cache_manager.use_redis or cache_manager.in_memory_cache is not None
        }
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/cache/clear', methods=['POST'])
def clear_cache():
    """Clear all cache"""
    try:
        cache_manager.clear()
        return jsonify({'status': 'success', 'message': 'Cache cleared'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/scheduler/tasks', methods=['GET'])
def get_scheduled_tasks():
    """Get all scheduled tasks"""
    try:
        tasks = scheduler.get_all_tasks()
        return jsonify({'tasks': tasks, 'count': len(tasks)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/scheduler/tasks/<task_id>/run', methods=['POST'])
def run_scheduled_task(task_id):
    """Run a scheduled task immediately"""
    try:
        success = scheduler.run_task_now(task_id)
        if success:
            return jsonify({'status': 'success', 'message': f'Task {task_id} started'})
        else:
            return jsonify({'error': 'Task not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/scheduler/tasks/<task_id>/enable', methods=['POST'])
def enable_scheduled_task(task_id):
    """Enable a scheduled task"""
    try:
        success = scheduler.enable_task(task_id)
        if success:
            return jsonify({'status': 'success', 'message': f'Task {task_id} enabled'})
        else:
            return jsonify({'error': 'Task not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/scheduler/tasks/<task_id>/disable', methods=['POST'])
def disable_scheduled_task(task_id):
    """Disable a scheduled task"""
    try:
        success = scheduler.disable_task(task_id)
        if success:
            return jsonify({'status': 'success', 'message': f'Task {task_id} disabled'})
        else:
            return jsonify({'error': 'Task not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/scheduler/history', methods=['GET'])
def get_task_history():
    """Get task execution history"""
    try:
        limit = request.args.get('limit', 50, type=int)
        history = scheduler.get_task_history(limit)
        return jsonify({'history': history, 'count': len(history)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/websocket/status', methods=['GET'])
def get_websocket_status():
    """Get WebSocket manager status"""
    try:
        stats = ws_manager.get_stats()
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================================================
# Error Handlers
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

# ============================================================================
# Main
# ============================================================================

if __name__ == '__main__':
    import atexit
    
    port = int(os.getenv('API_PORT', 5000))
    debug = os.getenv('API_DEBUG', 'False').lower() == 'true'
    
    print(f"\n{'='*60}")
    print("Tiapma'atzu API Server")
    print(f"{'='*60}")
    print(f"Port: {port}")
    print(f"Debug: {debug}")
    print(f"Firebase: {'✓' if db else '✗'}")
    print(f"Components: {'✓' if souls_manager else '✗'}")
    print(f"Middleware: {'✓'}")
    print(f"Scheduler: {'✓'}")
    print(f"WebSocket: {'✓'}")
    print(f"{'='*60}\n")
    
    # Register cleanup function
    def cleanup():
        print("Shutting down scheduler...")
        scheduler.stop()
    
    atexit.register(cleanup)
    
    try:
        app.run(host='0.0.0.0', port=port, debug=debug)
    except KeyboardInterrupt:
        print("\nShutting down...")
        scheduler.stop()
