# TaK-Tiapmaatzu OS - Agent Guidelines

## Project Overview
The TaK-Tiapmaatzu OS is a comprehensive autonomous business operating system built on Babylonian creation mythology as a conceptual architecture.

## Quick Start Commands

### Running the Application

**Backend API Server:**
```bash
# Activate virtual environment
source venv/bin/activate

# Start the API server
python api_server.py
```
- Runs on port 8000
- Health check: http://localhost:8000/health
- API base: http://localhost:8000/api

**Frontend:**
```bash
cd frontend
npm run dev
```
- Runs on port 3000
- Access: http://localhost:3000

### Testing

**Run all tests:**
```bash
source venv/bin/activate
python -m pytest tests/ -v
```

**Run specific test (excluding AI content which requires API key):**
```bash
python -m pytest tests/ -v -k "not ai_content"
```

**Run with coverage:**
```bash
python -m pytest tests/ --cov=src --cov-report=html
```

### Key API Endpoints

**Health:**
- GET /health - System health check

**Souls:**
- GET /api/souls - List all souls
- GET /api/souls/{id} - Get specific soul
- GET /api/souls/archetype/{archetype} - Filter by archetype
- GET /api/souls/rarity/{rarity} - Filter by rarity
- GET /api/souls/platform/{platform} - Filter by platform
- GET /api/souls/search - Search souls
- GET /api/souls/statistics - Soul statistics
- GET /api/souls/network - Network analysis

**Financial:**
- GET /api/financial/summary - Financial summary
- GET /api/financial/transactions - Transaction history
- POST /api/financial/tributes - Record tribute
- GET /api/financial/cash-flow - Cash flow analysis
- GET /api/financial/forecast - Financial forecast
- GET /api/financial/risk - Risk assessment
- GET /api/financial/diversification - Revenue diversification
- GET /api/financial/goals - Goal tracking

**Analytics:**
- GET /api/analytics/dashboard - Full dashboard
- GET /api/analytics/trends - Trend analysis
- GET /api/analytics/comparison - Period comparison
- GET /api/analytics/anomalies - Anomaly detection
- GET /api/analytics/soul-performance - Soul performance
- GET /api/analytics/archetype - Archetype analysis
- GET /api/analytics/network - Network analysis
- GET /api/analytics/export - Export analytics

**Firebase:**
- POST /api/firestore/sync - Sync to Firestore
- GET /api/firestore/souls - Get Firestore souls

## Code Conventions

### Python
- Use snake_case for files and variables
- Follow Clean Architecture principles
- Use dataclasses for data structures
- Use typing hints
- Use logging module (not print statements in production code)

### React/TypeScript
- Use CamelCase for components
- Follow React best practices
- Use TypeScript strict mode

### Naming
- Python files: `snake_case.py`
- React components: `CamelCase.tsx`
- CLI commands: lowercase
- HFL teams: City + team name
- Stadium names: "The + Name"
- Track names: `name_YYYYMMDD`

## Architecture

### Core Modules
- `souls_manager.py` - Soul/entity management
- `cashinghouse.py` - Financial ledger
- `souls_financial_integration.py` - Financial health tracking
- `analytics_dashboard.py` - Analytics and reporting
- `utils.py` - Shared utilities

### Philosophical Foundation
- **Apzu / Order**: Central financial ledger and CashingHouse
- **Tiama't / Chaos**: Strategy mutation and evolution
- **Tiapma'atzu / Logic**: Autonomous reasoning and agent execution
- **Enuma Elish**: Philosophical and mythological foundation

## Environment Configuration

Required environment variables in `.env`:
- `FIREBASE_SERVICE_ACCOUNT_KEY` - Path to Firebase service account key
- `OPENAI_API_KEY` - Optional, for AI content generation

## Firebase Configuration

- **Project ID**: tiapmaatzu
- **Region**: nam5 (us-central)
- **Hosting URL**: https://tiapmaatzu.web.app
- **Service Account**: tiapmaatzu-firebase-adminsdk-fbsvc-db8f709411.json

## Known Issues

1. **Port conflicts**: Port 8000 may be in use - kill existing process if needed
2. **AI content test**: Requires OPENAI_API_KEY to run - skip with `-k "not ai_content"`
3. **Method naming**: Some methods use underscores instead of hyphens (e.g., `calculate_hueman_i_terry_financial_health`)

## Test Maintenance

When adding new features:
1. Add corresponding test in `tests/` directory
2. Update test imports to use `src.modules.*` pattern
3. Use `Path(__file__).parent.parent / "src"` for data file paths
4. Run full test suite before committing

## Deployment

### Local Development
- Backend: `python api_server.py`
- Frontend: `cd frontend && npm run dev`

### Docker
```bash
docker-compose up -d
```

### Firebase
```bash
firebase deploy
```

## Verification Steps

After making changes:
1. Run test suite: `python -m pytest tests/ -v`
2. Check API health: `curl http://localhost:8000/health`
3. Test key endpoints manually
4. Verify frontend loads correctly

## Notes

- Flutter CLI not installed in current environment
- All code should follow Clean Architecture principles
- Test coverage target: 85%+
- Service account keys should never be committed
- Use environment variables for all sensitive data
