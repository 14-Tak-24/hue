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

souls_manager, cashinghouse, financial_integration, analytics = initialize_components()

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
    port = int(os.getenv('API_PORT', 5000))
    debug = os.getenv('API_DEBUG', 'False').lower() == 'true'
    
    print(f"\n{'='*60}")
    print("Tiapma'atzu API Server")
    print(f"{'='*60}")
    print(f"Port: {port}")
    print(f"Debug: {debug}")
    print(f"Firebase: {'✓' if db else '✗'}")
    print(f"Components: {'✓' if souls_manager else '✗'}")
    print(f"{'='*60}\n")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
