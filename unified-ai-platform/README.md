# Tiapma'atzu Unified AI Platform

Integrated AI content generation system for the 28 souls of Tiapma'atzu, powered by inference.sh CLI.

## Overview

This platform provides:
- **AI Content Generation**: Images, videos, avatars via inference.sh CLI
- **Automated Content Pipeline**: Scheduled content generation for 28 souls across 18 platforms
- **LLM Integration**: Autonomous content creation via OpenRouter (Claude, Gemini, Kimi, GLM)
- **Character Relationship Mapping**: Deep soul network analysis and interaction dynamics
- **Mac Nazarene Package**: Complete character package for the High Priest soul
- **Commerce & GTM Strategy**: Monetization and go-to-market for AI-generated content

## Architecture

```
unified-ai-platform/
├── modules/              # Core AI integration modules
│   ├── image_generator.py
│   ├── video_generator.py
│   ├── avatar_generator.py
│   ├── llm_agent.py
│   └── content_pipeline.py
├── content/              # Generated content storage
│   ├── images/
│   ├── videos/
│   ├── avatars/
│   └── text/
├── characters/           # Character-specific data
│   ├── mac_nazarene/
│   ├── soul_profiles/
│   └── relationships/
├── commerce/             # Commerce & GTM
│   ├── monetization.py
│   ├── gtm_strategy.py
│   └── pricing.py
├── workflows/            # Automated workflows
│   ├── daily_content.py
│   ├── platform_specific.py
│   └── campaign_generator.py
├── config/               # Configuration files
│   ├── ai_config.json
│   ├── platform_config.json
│   └── character_config.json
├── logs/                 # Execution logs
└── exports/              # Exported content packages
```

## Quick Start

### Prerequisites

1. Install inference.sh CLI:
```bash
curl -fsSL https://cli.inference.sh | sh
belt login
```

2. Install Python dependencies:
```bash
cd /Users/AkshuN/Desktop/Hue
source venv/bin/activate
pip install -r requirements.txt
```

### Generate Content

```bash
# Generate an image for a soul
python unified-ai-platform/modules/image_generator.py --soul soul_001 --prompt "High Priest in digital temple"

# Generate a video
python unified-ai-platform/modules/video_generator.py --soul soul_001 --prompt "sacred ritual in neon-lit sanctuary"

# Create an avatar video
python unified-ai-platform/modules/avatar_generator.py --soul soul_001 --script "Welcome to the temple of tomorrow"

# Generate content with LLM
python unified-ai-platform/modules/llm_agent.py --soul soul_001 --task "write a mystical tweet"
```

### Run Automated Pipeline

```bash
# Generate daily content for all souls
python unified-ai-platform/workflows/daily_content.py

# Platform-specific content generation
python unified-ai-platform/workflows/platform_specific.py --platform Twitter

# Campaign generation
python unified-ai-platform/workflows/campaign_generator.py --campaign "temple_launch"
```

## AI Models Available

### Image Generation
- FLUX Dev LoRA (highest quality)
- FLUX.2 Klein LoRA (fastest)
- Pruna FLUX Dev (optimized)

### Video Generation
- Veo 3.1 (best quality)
- Seedance 2.0 (with audio)
- Wan 2.5 (image-to-video)
- HappyHorse (physically realistic)

### Avatar Generation
- P-Video-Avatar (recommended - fastest, cheapest, built-in TTS)
- OmniHuman 1.5 (multi-character)
- Fabric 1.0 (lipsync)

### LLM Models
- Claude Opus 4.5 (complex reasoning)
- Claude Sonnet 4.5 (balanced)
- Claude Haiku 4.5 (fast, economical)
- Gemini 3 Pro
- Kimi K2 (thinking agent)
- GLM-4.6 (open-source)

## Character System

### 28 Souls

The platform manages 28 souls across 27 archetypes:
- **High Priest**: Mac Nazarene, Dixon Uhbuts
- **Divine Mother**: Mary Magnumbytes
- **Seductive Muse**: Airiol Uhbuts
- And 24 more unique archetypes

### Character Relationships

Deep relationship mapping includes:
- Platform connections
- Archetype compatibility
- Shared impact areas
- Narrative relationships
- Collaboration networks

### Mac Nazarene Package

Complete character package for the High Priest:
- Visual identity generation
- Voice and speech patterns
- Content templates
- Platform strategies
- Commerce integration

## Commerce & GTM

### Monetization

- Premium AI-generated content packages
- Custom character services
- Platform-specific content subscriptions
- Enterprise API access

### Go-to-Market Strategy

- Target audience segmentation
- Platform-specific marketing
- Content licensing
- Partnership opportunities

## Configuration

### AI Configuration

Edit `config/ai_config.json` to set:
- Default models for each content type
- Quality settings
- API rate limits
- Cost optimization preferences

### Platform Configuration

Edit `config/platform_config.json` to set:
- Platform-specific content requirements
- Posting schedules
- Character guidelines
- Hashtag strategies

### Character Configuration

Edit `config/character_config.json` to set:
- Character-specific prompts
- Voice settings
- Content preferences
- Relationship mappings

## Documentation

- `modules/README.md` - Module documentation
- `workflows/README.md` - Workflow documentation
- `commerce/README.md` - Commerce documentation
- `characters/README.md` - Character system documentation

## License

Part of the Tiapma'atzu platform.

---

**Generated with [Devin](https://devin.ai)**
