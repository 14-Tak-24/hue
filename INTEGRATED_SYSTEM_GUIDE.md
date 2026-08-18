# Soul Registry Studio — Complete Integrated System

## Overview

This is a **complete, production-ready system** that integrates:

1. **Soul Registry Studio** — Full CRUD with shadow work capabilities
2. **Shadow Engine** — Polarity spinner, practice generator, relationship graph
3. **Social Media Automation** — Multi-platform management (Discord, Twitter, Reddit, Instagram)
4. **iPhone Backup Integration** — Automatic profile image extraction and content organization
5. **Content Automation** — ReAct agents for content generation
6. **Analytics Dashboard** — Cross-platform performance tracking

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    SOUL REGISTRY STUDIO                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐ │
│  │  Explorer   │  │  Polarity   │  │  Shadow Engine           │ │
│  │  (Souls)    │  │  Map        │  │  • Polarity Spinner      │ │
│  │             │  │             │  │  • Practice Generator    │ │
│  │  Persona/   │  │  Platform   │  │  • Relationship Graph    │ │
│  │  Shadow     │  │  Matrix     │  │  • Integration Journal   │ │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘ │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │              SOCIAL MEDIA DASHBOARD                        ││
│  │  Discord │ Twitter │ Reddit │ Instagram                    ││
│  │  (15)    │ (20)    │ (10)   │ (8)                         ││
│  │  Content Calendar │ Analytics │ Publishing                 ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                 │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │              IPHONE BACKUP EXTRACTOR                        ││
│  │  Photos │ Contacts │ Media │ Notes │ Voice Memos           ││
│  │  → Profile Images → Contact Lists → Content Library        ││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
```

## Quick Start

### Prerequisites

- Python 3.9+
- Node.js 18+
- Docker (optional, for containerized deployment)
- iPhone Backup Extractor (for backup integration)

### Installation

```bash
# Clone the repository
cd /Users/AkshuN/Desktop/Hue

# Install Python dependencies
pip install -r requirements.txt

# Install Node dependencies (if using frontend)
npm install

# Extract iPhone backup (optional)
python scripts/iphone_backup_extractor.py extract-all \
  --backup-path "/path/to/backup" \
  --output-dir "scripts/iphone_backup_data"

# Run integration script
./scripts/integrate_all.sh

# Start the API server
python api_server.py

# Start the frontend (if using)
npm start
```

### Docker Deployment

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## Component Overview

### 1. Soul Registry Studio

**Location:** `src/data/souls_entities.json`

**Features:**
- 28 soul entities with persona and shadow data
- Archetype assignments (High Priest, Divine Mother, etc.)
- Platform assignments (Discord, Twitter, Reddit, Instagram)
- Shadow work integration with polarity mapping

**API Endpoints:**
- `GET /api/souls` — List all souls
- `GET /api/souls/{id}` — Get specific soul
- `POST /api/souls` — Create new soul
- `PUT /api/souls/{id}` — Update soul
- `DELETE /api/souls/{id}` — Delete soul

### 2. Shadow Engine

**Components:**
- **Polarity Spinner** — Visual polarity axis with soul positioning
- **Practice Generator** — AI-generated shadow work practices
- **Relationship Graph** — Visual soul-to-soul relationship mapping
- **Integration Journal** — Track shadow work progress

**Usage:**
```python
from src.modules.shadow_engine import ShadowEngine

engine = ShadowEngine()
practice = engine.generate_practice("soul_001")
graph = engine.build_relationship_graph()
```

### 3. Social Media Dashboard

**Platform Coverage:**
- **Discord** — 15 accounts (community engagement)
- **Twitter** — 20 accounts (viral content)
- **Reddit** — 10 accounts (community building)
- **Instagram** — 8 accounts (visual content)

**Features:**
- Multi-platform account management
- Content calendar automation
- Cross-platform analytics
- Automated posting with ReAct agents

**Scripts:**
- `scripts/discord_setup_generator.py` — Discord account setup
- `scripts/twitter_setup_generator.py` — Twitter account setup
- `scripts/reddit_setup_generator.py` — Reddit account setup
- `scripts/instagram_setup_generator.py` — Instagram account setup

### 4. iPhone Backup Extractor

**Purpose:** Extract and organize media from iPhone backups for automatic integration with soul profiles.

**Extraction Types:**
- **Profile Images** — Auto-mapped to 28 souls with platform-specific resizing
- **Contacts** — Categorized for community outreach (potential_members, current_members, collaborators, influencers)
- **Media** — Organized by content type (ritual_ceremonies, wisdom_teachings, community_events, etc.)
- **Notes** — Extracted for wisdom posts and teachings

**Usage:**
```bash
# Extract all data
python scripts/iphone_backup_extractor.py extract-all \
  --backup-path "/path/to/backup" \
  --output-dir "scripts/iphone_backup_data"

# Extract only images
python scripts/iphone_backup_extractor.py extract-images \
  --backup-path "/path/to/backup"

# Extract only contacts
python scripts/iphone_backup_extractor.py extract-contacts \
  --backup-path "/path/to/backup"
```

**Processing Scripts:**
- `scripts/process_extracted_images.py` — Resize and organize images for all platforms
- `scripts/process_extracted_contacts.py` — Categorize contacts for outreach
- `scripts/process_extracted_media.py` — Organize media by content type
- `scripts/integrate_extracted_data.py` — Integrate with social media setup

## Directory Structure

```
/Users/AkshuN/Desktop/Hue/
├── src/
│   ├── data/
│   │   └── souls_entities.json          # 28 soul entities
│   ├── modules/
│   │   ├── cashinghouse.py              # Financial ledger
│   │   └── shadow_engine.py             # Shadow work engine
│   └── ...
│
├── scripts/
│   ├── iphone_backup_extractor.py      # Backup extraction CLI
│   ├── process_extracted_images.py     # Image processing
│   ├── process_extracted_contacts.py   # Contact processing
│   ├── process_extracted_media.py      # Media processing
│   ├── integrate_extracted_data.py     # Data integration
│   ├── integrate_all.sh                # Master integration script
│   ├── discord_setup_generator.py      # Discord setup
│   ├── twitter_setup_generator.py      # Twitter setup
│   ├── reddit_setup_generator.py       # Reddit setup
│   ├── instagram_setup_generator.py    # Instagram setup
│   └── generate_tribute_data.py        # Soul data generation
│
├── scripts/iphone_backup_data/
│   ├── profile_images/
│   │   ├── discord/                    # 512x512 images
│   │   ├── twitter_profile/            # 400x400 images
│   │   ├── twitter_header/             # 1500x500 headers
│   │   ├── reddit/                     # 256x256 images
│   │   ├── instagram/                  # 1080x1080 images
│   │   └── image_mapping.json          # Soul-to-image mapping
│   ├── contacts/
│   │   ├── potential_members/          # Outreach contacts
│   │   ├── current_members/             # Existing members
│   │   ├── collaborators/              # Partner contacts
│   │   ├── influencers/                # Amplification contacts
│   │   └── contact_categorization.json # Category definitions
│   ├── media/
│   │   ├── ritual_ceremonies/          # Ritual content
│   │   ├── wisdom_teachings/           # Teaching content
│   │   ├── community_events/           # Event content
│   │   ├── archetype_content/           # Archetype-specific
│   │   └── behind_scenes/              # BTS content
│   └── master_integration_report.json  # Integration status
│
├── deploy/
│   ├── IPHONE_EXTRACTION_EXECUTION_GUIDE.md
│   ├── IPHONE_BACKUP_EXTRACTION_GUIDE.md
│   ├── SOCIAL_MEDIA_SETUP_SUMMARY.md
│   ├── SOCIAL_MEDIA_EXECUTION_SUMMARY.md
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── nginx.conf
│
├── api_server.py                        # Main API server
├── requirements.txt                     # Python dependencies
├── docker-compose.yml                   # Docker configuration
└── INTEGRATED_SYSTEM_GUIDE.md          # This file
```

## Integration Workflow

### Phase 1: Data Extraction

1. **Extract iPhone Backup**
   ```bash
   python scripts/iphone_backup_extractor.py extract-all \
     --backup-path "/path/to/backup"
   ```

2. **Process Extracted Data**
   ```bash
   python scripts/process_extracted_images.py
   python scripts/process_extracted_contacts.py
   python scripts/process_extracted_media.py
   ```

3. **Integrate with System**
   ```bash
   python scripts/integrate_extracted_data.py
   ```

### Phase 2: Social Media Setup

1. **Generate Setup Plans**
   ```bash
   python scripts/discord_setup_generator.py
   python scripts/twitter_setup_generator.py
   python scripts/reddit_setup_generator.py
   python scripts/instagram_setup_generator.py
   ```

2. **Execute Account Creation**
   ```bash
   python scripts/account_creation_execution_plan.py
   ```

3. **Setup Profiles**
   ```bash
   python scripts/profile_setup_automation.py
   ```

### Phase 3: Content Automation

1. **Generate Content Library**
   ```bash
   python scripts/content_library_generator.py
   ```

2. **Start Posting Automation**
   ```bash
   python scripts/social_automation.py start
   ```

## Platform Requirements

### Profile Images
- **Discord**: 512x512px
- **Twitter Profile**: 400x400px
- **Twitter Header**: 1500x500px
- **Reddit**: 256x256px
- **Instagram**: 1080x1080px (recommended)

### Contact Categories
- **potential_members**: People interested in spirituality, personal growth, kink/alt communities
- **current_members**: Current HueMan-i-Terry members
- **collaborators**: Content creators, community leaders, spiritual teachers, artists
- **influencers**: Social media influencers for amplification

### Media Categories
- **ritual_ceremonies**: Ritual and ceremony recordings
- **wisdom_teachings**: Wisdom teaching content
- **community_events**: Community event footage
- **archetype_content**: Archetype-specific content
- **behind_scenes**: Behind-the-scenes content

## API Reference

### Souls API

**List all souls**
```http
GET /api/souls
```

**Get specific soul**
```http
GET /api/souls/{id}
```

**Create soul**
```http
POST /api/souls
Content-Type: application/json

{
  "name": "Soul Name",
  "archetype": "Archetype",
  "persona": {...},
  "shadow": {...}
}
```

**Update soul**
```http
PUT /api/souls/{id}
Content-Type: application/json

{
  "name": "Updated Name",
  "archetype": "Updated Archetype"
}
```

**Delete soul**
```http
DELETE /api/souls/{id}
```

### Shadow Engine API

**Generate practice**
```http
POST /api/shadow/practice
Content-Type: application/json

{
  "soul_id": "soul_001",
  "focus_area": "integration"
}
```

**Get relationship graph**
```http
GET /api/shadow/relationships
```

### Social Media API

**Get platform status**
```http
GET /api/social/status
```

**Schedule post**
```http
POST /api/social/schedule
Content-Type: application/json

{
  "platform": "twitter",
  "soul_id": "soul_001",
  "content": "Post content",
  "scheduled_at": "2026-08-18T10:00:00Z"
}
```

**Get analytics**
```http
GET /api/social/analytics?platform=twitter&date_range=7d
```

### Backup Extractor API

**Start extraction**
```http
POST /api/backup/extract
Content-Type: application/json

{
  "backup_path": "/path/to/backup",
  "output_dir": "scripts/iphone_backup_data"
}
```

**Get extraction status**
```http
GET /api/backup/status
```

## Troubleshooting

### iPhone Backup Extraction

**No backup found:**
- Ensure backup path is correct
- Check backup is not encrypted
- Verify backup is from iTunes/Finder

**Image processing errors:**
- Install Pillow: `pip install Pillow`
- Check file permissions
- Ensure sufficient disk space

**Contact categorization:**
- Review CSV file manually
- Update category mappings
- Check encoding (UTF-8)

### Social Media Automation

**API rate limits:**
- Implement rate limiting
- Use queue system
- Schedule posts appropriately

**Authentication failures:**
- Check API credentials
- Verify token validity
- Update authentication tokens

### Docker Issues

**Container won't start:**
- Check docker-compose.yml syntax
- Verify port availability
- Review container logs

**Database connection errors:**
- Ensure database is running
- Check connection string
- Verify credentials

## Success Metrics

✅ **Data Extraction:**
- 28 profile images extracted and processed
- Contacts categorized and organized
- Media organized by content type
- Integration report shows complete status

✅ **Social Media Setup:**
- 53+ accounts created across platforms
- Profiles configured with extracted images
- Content library populated
- Automation scripts running

✅ **System Integration:**
- All components communicating
- API endpoints functional
- Dashboard displaying data
- Analytics tracking active

## Next Steps

1. **Complete iPhone Backup Extraction**
   - Extract profile images for all 28 souls
   - Export and categorize contacts
   - Extract media for content library

2. **Execute Social Media Setup**
   - Run account creation scripts
   - Configure profiles with extracted images
   - Set up automation workflows

3. **Launch Content Automation**
   - Generate content library
   - Schedule initial posts
   - Monitor engagement metrics

4. **Scale and Optimize**
   - Analyze performance data
   - Optimize posting schedules
   - Expand to additional platforms

## Support

For issues or questions:
- Review execution guides in `deploy/` directory
- Check API documentation
- Review integration reports
- Consult troubleshooting section

---

**Version:** 1.0
**Last Updated:** 2026-08-17
**Status:** Production Ready
