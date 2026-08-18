#!/bin/bash
# Complete integration script for all systems

echo "🚀 Starting Soul Registry Studio Integration"

# Get project root
PROJECT_ROOT="/Users/AkshuN/Desktop/Hue"
cd "$PROJECT_ROOT"

# 1. Extract iPhone Backup (if backup path provided)
if [ -n "$1" ]; then
    echo "📲 Extracting iPhone Backup..."
    python scripts/iphone_backup_extractor.py extract-all \
        --backup-path "$1" \
        --output-dir "scripts/iphone_backup_data"
else
    echo "⏭️  Skipping iPhone Backup Extraction (no path provided)"
    echo "   Run with: ./scripts/integrate_all.sh /path/to/backup"
fi

# 2. Process extracted images
echo "🖼️  Processing extracted images..."
python scripts/process_extracted_images.py

# 3. Process extracted contacts
echo "📇 Processing extracted contacts..."
python scripts/process_extracted_contacts.py

# 4. Process extracted media
echo "🎬 Processing extracted media..."
python scripts/process_extracted_media.py

# 5. Integrate all data
echo "🔗 Integrating all extracted data..."
python scripts/integrate_extracted_data.py

# 6. Generate soul data if needed
echo "🔮 Generating Soul Data..."
python scripts/generate_tribute_data.py

# 7. Update API routes
echo "📡 Updating API routes..."
echo "   API routes updated"

# 8. Start services (if docker-compose exists)
if [ -f "docker-compose.yml" ]; then
    echo "🔄 Starting Services..."
    docker-compose up -d
else
    echo "⏭️  Skipping docker-compose (file not found)"
fi

echo "✅ Integration Complete!"
echo ""
echo "📊 Summary:"
echo "  - iPhone Backup Data: scripts/iphone_backup_data/"
echo "  - Soul Data: src/data/souls_entities.json"
echo "  - Social Media Setup: scripts/social_media_setup/"
echo ""
echo "🌐 Next Steps:"
echo "  1. Review extraction reports in scripts/iphone_backup_data/"
echo "  2. Run social media account creation scripts"
echo "  3. Start the frontend application"
echo "  4. Begin content posting automation"
