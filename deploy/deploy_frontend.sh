#!/bin/bash

# Tiapma'atzu Frontend Deployment Script
# Supports Firebase Hosting and other platforms

set -e

PLATFORM=${1:-firebase}
ENVIRONMENT=${2:-production}

echo "🎨 Tiapma'atzu Frontend Deployment"
echo "Platform: $PLATFORM"
echo "Environment: $ENVIRONMENT"
echo ""

# Navigate to frontend directory
cd frontend

# Check required files
if [ ! -f "package.json" ]; then
    echo "❌ package.json not found"
    exit 1
fi

if [ ! -f "vite.config.ts" ]; then
    echo "❌ vite.config.ts not found"
    exit 1
fi

# Install dependencies
echo "📦 Installing dependencies..."
npm install

# Build frontend
echo "🔨 Building frontend..."
if [ "$ENVIRONMENT" = "production" ]; then
    VITE_API_URL=https://tiapmaatzu.web.app npm run build
else
    npm run build
fi

echo "✅ Frontend build complete"

case $PLATFORM in
    firebase)
        echo "🔥 Deploying to Firebase Hosting..."
        cd ..
        npx -y firebase-tools@latest deploy --only hosting
        echo "✅ Firebase deployment complete"
        echo "   URL: https://tiapmaatzu.web.app"
        ;;

    vercel)
        echo "▲ Deploying to Vercel..."
        npx -y vercel@latest --prod
        echo "✅ Vercel deployment complete"
        ;;

    netlify)
        echo "🌐 Deploying to Netlify..."
        npx -y netlify-cli@latest deploy --prod --dir=frontend/dist
        echo "✅ Netlify deployment complete"
        ;;

    *)
        echo "❌ Unknown platform: $PLATFORM"
        echo "   Available platforms: firebase, vercel, netlify"
        exit 1
        ;;
esac

echo ""
echo "✅ Frontend deployment complete!"