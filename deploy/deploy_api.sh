#!/bin/bash

# Tiapma'atzu API Deployment Script
# Supports multiple deployment platforms

set -e

PLATFORM=${1:-local}
ENVIRONMENT=${2:-production}

echo "🚀 Tiapma'atzu API Deployment"
echo "Platform: $PLATFORM"
echo "Environment: $ENVIRONMENT"
echo ""

# Validate environment
if [ "$ENVIRONMENT" != "production" ] && [ "$ENVIRONMENT" != "staging" ]; then
    echo "❌ Invalid environment. Use 'production' or 'staging'"
    exit 1
fi

# Check required files
if [ ! -f "api_server.py" ]; then
    echo "❌ api_server.py not found"
    exit 1
fi

if [ ! -f "requirements.txt" ]; then
    echo "❌ requirements.txt not found"
    exit 1
fi

if [ ! -f "tiapmaatzu-firebase-adminsdk-fbsvc-db8f709411.json" ]; then
    echo "⚠️  Firebase service account key not found"
    echo "   Make sure to set FIREBASE_SERVICE_ACCOUNT_KEY environment variable"
fi

case $PLATFORM in
    local)
        echo "📦 Building for local deployment..."
        python3 -m venv venv
        source venv/bin/activate
        pip install -r requirements.txt
        echo "✅ Local build complete"
        echo "   Run: source venv/bin/activate && python api_server.py"
        ;;

    docker)
        echo "🐳 Building Docker image..."
        docker build -f deploy/Dockerfile -t tiapmaatzu-api:$ENVIRONMENT .
        echo "✅ Docker image built: tiapmaatzu-api:$ENVIRONMENT"
        echo "   Run: docker run -p 8000:8000 tiapmaatzu-api:$ENVIRONMENT"
        ;;

    render)
        echo "☁️  Preparing for Render deployment..."
        if [ ! -f "deploy/render.yaml" ]; then
            echo "❌ deploy/render.yaml not found"
            exit 1
        fi
        echo "✅ Render configuration ready"
        echo "   Next steps:"
        echo "   1. Connect your repository to Render"
        echo "   2. Set FIREBASE_SERVICE_ACCOUNT_KEY environment variable"
        echo "   3. Deploy will be automatic on push"
        ;;

    railway)
        echo "🚂 Preparing for Railway deployment..."
        if [ ! -f "deploy/railway.toml" ]; then
            echo "❌ deploy/railway.toml not found"
            exit 1
        fi
        echo "✅ Railway configuration ready"
        echo "   Next steps:"
        echo "   1. Install Railway CLI: npm install -g @railway/cli"
        echo "   2. Login: railway login"
        echo "   3. Deploy: railway up"
        ;;

    *)
        echo "❌ Unknown platform: $PLATFORM"
        echo "   Available platforms: local, docker, render, railway"
        exit 1
        ;;
esac

echo ""
echo "✅ Deployment preparation complete!"