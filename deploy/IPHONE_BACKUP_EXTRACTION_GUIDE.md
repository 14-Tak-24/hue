# iPhone Backup Data Extraction Guide for Tiapma'atzu HueMan-i-Terry

## Overview
This guide helps you extract and organize data from iPhone backups to support the Tiapma'atzu HueMan-i-Terry social media setup and community building.

## Directory Structure Created

```
scripts/iphone_backup_data/
├── profile_images/
│   └── image_mapping.json (Maps souls to their profile images)
├── contacts/
│   ├── contact_categorization.json (Categories for contacts)
│   └── import_template.json (Template for contact import)
├── media/
│   ├── ritual_ceremonies/ (audio/, video/, photos/)
│   ├── wisdom_teachings/ (audio/, video/, transcripts/)
│   ├── community_events/ (audio/, video/, photos/)
│   ├── archetype_content/ (high_priest/, divine_mother/, etc.)
│   └── processing_guide.json (Media processing instructions)
├── other_data/
│   └── extraction_guide.json (Other data extraction guide)
└── integration_workflow.json (Integration steps)
```

## Step-by-Step Extraction Process

### 1. Profile Images for Social Media Setup

**Purpose**: Extract profile images for the 28 souls to use across Discord, Twitter, Reddit, and Instagram.

**Steps**:
1. Open iPhone Backup Extractor
2. Select your iPhone backup
3. Navigate to Media/Photos
4. Extract photos to: `scripts/iphone_backup_data/profile_images/`
5. Rename images to match soul IDs using the mapping in `image_mapping.json`

**Image Mapping**: The system has identified all 28 souls and their expected profile images:
- soul_001: Mac Nazarene → mac.png
- soul_002: Mary Magnumbytes → mary.png
- soul_003: Dixon Uhbuts → dixon.png
- [All 28 souls mapped with their expected filenames]

**Image Requirements**:
- Discord: 512x512px
- Twitter: 400x400px (profile), 1500x500px (header)
- Reddit: 256x256px
- Instagram: 110x110px minimum, 1080x1080px recommended

### 2. Contacts for Community Building

**Purpose**: Extract and categorize contacts for community outreach and member acquisition.

**Steps**:
1. Open iPhone Backup Extractor
2. Select your iPhone backup
3. Navigate to Contacts/Address Book
4. Export contacts to: `scripts/iphone_backup_data/contacts/`
5. Use `contact_categorization.json` to categorize contacts

**Contact Categories**:
- **potential_members**: People interested in spirituality, personal growth, kink/alt communities
- **current_members**: Current HueMan-i-Terry members (Discord, Twitter followers)
- **collaborators**: Content creators, community leaders, spiritual teachers, artists
- **influencers**: Social media influencers for amplification

**Import Template**: Use `import_template.json` to structure contact data with:
- Name, phone, email
- Category
- Notes
- Platform where connected
- Archetype interest

### 3. Media for Content Creation

**Purpose**: Extract media for content creation across all social media platforms.

**Steps**:
1. Open iPhone Backup Extractor
2. Select your iPhone backup
3. Navigate to Media folder
4. Extract relevant media to organized folders in `scripts/iphone_backup_data/media/`

**Media Organization**:
- **ritual_ceremonies/**: Ritual and ceremony recordings
  - audio/ (Audio recordings)
  - video/ (Video recordings)
  - photos/ (Ceremony photos)
  
- **wisdom_teachings/**: Wisdom teaching content
  - audio/ (Teaching audio)
  - video/ (Teaching videos)
  - transcripts/ (Written transcripts)
  
- **community_events/**: Community event footage
  - audio/ (Event audio)
  - video/ (Event videos)
  - photos/ (Event photos)
  
- **archetype_content/**: Archetype-specific content
  - high_priest/
  - divine_mother/
  - seductive_muse/
  - cosmic_mystic/
  - [All 27 archetypes]
  
- **behind_scenes/**: Behind-the-scenes content
  - bts_footage/ (BTS video)
  - bts_photos/ (BTS photos)

**Content Priorities**:
- **High Priority**: Profile images, ritual recordings, wisdom teachings, community events
- **Medium Priority**: Behind-the-scenes, archetype-specific media, audio recordings
- **Low Priority**: Personal photos, random videos, uncategorized media

### 4. Other Useful Data

**Purpose**: Extract additional data that can support the HueMan-i-Terry project.

**Data Types**:
- **Notes**: Notes app content for wisdom posts and teachings
- **Messages**: Message threads for community insights and common questions
- **Calendar**: Calendar events for ritual scheduling and community events
- **Voice Memos**: Voice memos for podcast content and wisdom recordings
- **Safari Bookmarks**: Browser bookmarks for resource curation

**Extraction Priority**:
- **High**: Notes, voice memos
- **Medium**: Calendar, safari bookmarks
- **Low**: Messages (review for privacy)

**Privacy Considerations**:
- Review all extracted data for personal information
- Remove sensitive data before sharing
- Obtain consent for using community messages
- Blur personal information in shared content

## Integration with Social Media Setup

### Workflow Steps

1. **Extract Profile Images**
   - Extract from iPhone backup
   - Rename to match soul IDs
   - Resize to platform specifications
   - Integrate with account creation phase

2. **Extract Contacts**
   - Export from iPhone backup
   - Categorize by type
   - Import into contact management system
   - Use for community outreach

3. **Extract Media**
   - Organize by content type
   - Process for platform requirements
   - Add to content library
   - Schedule for posting

4. **Extract Other Data**
   - Process notes for wisdom posts
   - Extract calendar events for scheduling
   - Process voice memos for audio content
   - Integrate with content strategy

## Estimated Time

- **Data Extraction**: 2-3 hours
- **Organization & Processing**: 1-2 hours
- **Integration with Setup**: 1-2 hours
- **Total**: 4-7 hours

## Tools Required

- **iPhone Backup Extractor** (already installed)
- **Image Editing Software** (Canva, Photoshop, or similar)
- **Contact Management** (Google Sheets, Excel, or CRM)
- **Video Editing Software** (for media processing)

## File Locations

- **iPhone Backup Path**: `/Users/AkshuN/Library/Application Support/MobileSync/Backup/`
- **Output Directory**: `scripts/iphone_backup_data/`
- **Integration Workflow**: `scripts/iphone_backup_data/integration_workflow.json`

## Next Steps

1. **Immediate**: Open iPhone Backup Extractor and begin profile image extraction
2. **Short-term**: Extract contacts and categorize for community building
3. **Medium-term**: Extract media and organize for content creation
4. **Long-term**: Extract other data and integrate with content strategy

## Success Metrics

- ✅ 28 profile images extracted and ready for social media setup
- ✅ Contacts categorized and organized for community outreach
- ✅ Media organized and ready for content creation
- ✅ Additional data extracted and integrated with project
- ✅ All data privacy considerations addressed

## Support

If you encounter issues during extraction:
1. Check iPhone Backup Extractor documentation
2. Ensure iPhone backup is accessible
3. Verify sufficient disk space for extraction
4. Review processing guides in each directory

---

**Generated**: 2026-08-16
**Version**: 1.0
**Status**: Ready for Extraction
**Estimated Time**: 4-7 hours