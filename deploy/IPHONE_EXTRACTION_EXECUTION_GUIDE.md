# iPhone Backup Data Extraction Execution Guide

## Overview
This guide provides step-by-step instructions for extracting data from iPhone backups and integrating it with the Tiapma'atzu HueMan-i-Terry social media setup.

## Prerequisites
- iPhone Backup Extractor installed and running (currently open)
- iPhone backup available on your system
- Python 3.x installed
- Project directory: `/Users/AkshuN/Desktop/Hue/`

## Quick Start Workflow

### Phase 1: Manual Extraction (iPhone Backup Extractor)

#### Step 1: Extract Profile Images
1. **In iPhone Backup Extractor:**
   - Select your iPhone backup from the list
   - Navigate to "Media" → "Photos"
   - Select and extract photos to: `scripts/iphone_backup_data/profile_images/`
   - Extract all photos that could be profile images for the 28 souls

2. **Image Mapping Reference:**
   - The system expects images named: `mac.png`, `mary.png`, `dixon.png`, etc.
   - Full mapping available in: `scripts/iphone_backup_data/profile_images/image_mapping.json`
   - Don't worry about exact names - the automated script will handle renaming

#### Step 2: Extract Contacts
1. **In iPhone Backup Extractor:**
   - Navigate to "Contacts" or "Address Book"
   - Export contacts to: `scripts/iphone_backup_data/contacts/`
   - Export as vCard (.vcf) or CSV format

#### Step 3: Extract Media
1. **In iPhone Backup Extractor:**
   - Navigate to "Media" folder
   - Extract relevant media to: `scripts/iphone_backup_data/media/`
   - Focus on: ritual recordings, wisdom teachings, community events

### Phase 2: Automated Processing

#### Step 4: Process Profile Images
```bash
cd /Users/AkshuN/Desktop/Hue
python scripts/process_extracted_images.py
```

**This script will:**
- Organize extracted images by soul ID
- Resize images for all platforms (Discord, Twitter, Reddit, Instagram)
- Generate Twitter header images
- Create platform-specific directories
- Generate processing report

**Output:**
- `scripts/iphone_backup_data/profile_images/discord/`
- `scripts/iphone_backup_data/profile_images/twitter_profile/`
- `scripts/iphone_backup_data/profile_images/twitter_header/`
- `scripts/iphone_backup_data/profile_images/reddit/`
- `scripts/iphone_backup_data/profile_images/instagram/`

#### Step 5: Process Contacts
```bash
python scripts/process_extracted_contacts.py
```

**This script will:**
- Import contacts from vCard or CSV files
- Auto-categorize contacts based on keywords
- Create a review CSV for manual verification
- Generate initial categorization

**Manual Review Required:**
- Open: `scripts/iphone_backup_data/contacts/contacts_for_review.csv`
- Review and update categories manually
- Save the CSV file

**After Review:**
```bash
python scripts/process_extracted_contacts.py --organize
```

**This will:**
- Organize contacts by category
- Generate outreach lists
- Create community building plan

#### Step 6: Process Media
```bash
python scripts/process_extracted_media.py
```

**This script will:**
- Scan for extracted media files
- Auto-categorize by content type (rituals, teachings, events, etc.)
- Organize into proper directory structure
- Create content inventory
- Generate content calendar suggestions

**Output:**
- `scripts/iphone_backup_data/media/ritual_ceremonies/`
- `scripts/iphone_backup_data/media/wisdom_teachings/`
- `scripts/iphone_backup_data/media/community_events/`
- `scripts/iphone_backup_data/media/archetype_content/`
- `scripts/iphone_backup_data/media/behind_scenes/`

### Phase 3: Integration

#### Step 7: Integrate All Data
```bash
python scripts/integrate_extracted_data.py
```

**This script will:**
- Check extraction status of all components
- Integrate profile images with social media setup
- Integrate contacts with community building plan
- Integrate media with content library
- Update souls data with local image paths
- Generate master integration report

**Output:**
- `scripts/iphone_backup_data/master_integration_report.json`
- Updated `src/data/souls_entities.json` with local image paths
- Community outreach plan
- Integrated content library

## Detailed File Structure

```
scripts/iphone_backup_data/
├── profile_images/
│   ├── image_mapping.json              # Soul-to-image mapping
│   ├── discord/                        # Discord-sized images (512x512)
│   ├── twitter_profile/                # Twitter profile images (400x400)
│   ├── twitter_header/                 # Twitter headers (1500x500)
│   ├── reddit/                         # Reddit images (256x256)
│   ├── instagram/                      # Instagram images (1080x1080)
│   └── processing_report.json         # Image processing status
├── contacts/
│   ├── contact_categorization.json     # Category definitions
│   ├── contacts_for_review.csv         # Manual review file
│   ├── potential_members/              # Categorized contacts
│   ├── current_members/
│   ├── collaborators/
│   ├── influencers/
│   ├── immediate_outreach.json        # Outreach lists
│   ├── collaboration_opportunities.json
│   ├── influencer_outreach.json
│   └── community_outreach_plan.json    # Outreach strategy
├── media/
│   ├── ritual_ceremonies/
│   │   ├── audio/
│   │   ├── video/
│   │   └── photos/
│   ├── wisdom_teachings/
│   │   ├── audio/
│   │   ├── video/
│   │   └── transcripts/
│   ├── community_events/
│   │   ├── audio/
│   │   ├── video/
│   │   └── photos/
│   ├── archetype_content/
│   │   ├── high_priest/
│   │   ├── divine_mother/
│   │   └── ...
│   ├── behind_scenes/
│   │   ├── bts_footage/
│   │   └── bts_photos/
│   ├── content_inventory.json         # Media inventory
│   ├── content_calendar_suggestions.json
│   └── integrated_content_library.json
├── other_data/
│   └── extraction_guide.json
├── integration_workflow.json
├── processing_summary.json
└── master_integration_report.json      # Final integration status
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

## Troubleshooting

### iPhone Backup Extractor Issues
- **No backup found**: Ensure you have an iTunes/Finder backup on your system
- **Encrypted backup**: iPhone Backup Extractor may not support encrypted backups
- **Backup location**: Typically in `~/Library/Application Support/MobileSync/Backup/`

### Image Processing Issues
- **No images found**: Ensure images are extracted to the correct directory
- **PIL/Pillow not installed**: Install with `pip install Pillow`
- **Permission errors**: Ensure write permissions in the project directory

### Contact Processing Issues
- **No contacts found**: Ensure contacts are exported as vCard or CSV
- **Encoding errors**: Try exporting as CSV instead of vCard
- **Empty categories**: Review CSV and add appropriate categories manually

### Media Processing Issues
- **No media found**: Ensure media files are extracted to the media directory
- **Large files**: Processing may take time for large video files
- **Format issues**: Convert unsupported formats to standard formats (MP4, MP3, JPG)

## Integration with Social Media Setup

Once data extraction and processing is complete:

1. **Account Creation**: Use the processed profile images for social media account creation
2. **Profile Setup**: Automated scripts can use the platform-specific image directories
3. **Content Library**: Media inventory integrates with content posting schedules
4. **Community Building**: Contact lists are ready for outreach campaigns

## Estimated Time

- **Manual Extraction**: 1-2 hours
- **Image Processing**: 5-10 minutes
- **Contact Processing**: 10-15 minutes (including manual review)
- **Media Processing**: 5-15 minutes (depends on file count)
- **Integration**: 2-5 minutes
- **Total**: 1.5-3 hours

## Success Criteria

✅ All 28 profile images extracted and processed for all platforms
✅ Contacts categorized and organized for outreach
✅ Media organized by content type
✅ Integration report shows all components complete
✅ Social media setup ready to proceed with account creation

## Next Steps After Integration

1. Run social media account creation scripts
2. Execute profile setup automation
3. Begin content posting using integrated media library
4. Start community outreach using contact lists
5. Monitor engagement and adjust strategy

## Support

For issues during extraction:
1. Check iPhone Backup Extractor documentation
2. Verify file paths and permissions
3. Review processing logs and reports
4. Ensure sufficient disk space for processing

---

**Generated**: 2026-08-17
**Version**: 1.0
**Status**: Ready for Execution
