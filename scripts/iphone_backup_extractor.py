"""
iPhone Backup Extractor — Extract and organize media from iPhone backups
Integrates with Soul Registry Studio for automatic profile image assignment
"""

import os
import json
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
import click
from PIL import Image

# ============================================================
# Data Models
# ============================================================

@dataclass
class SoulImageMapping:
    """Mapping between backup image files and soul IDs"""
    source_filename: str
    soul_id: str
    soul_name: str
    archetype: str
    platform_sizes: Dict[str, Tuple[int, int]]

@dataclass
class Contact:
    name: str
    phone: str
    email: str
    category: str  # potential_member, current_member, collaborator, influencer
    notes: str
    source: str

@dataclass
class ExtractedMedia:
    source_path: str
    destination_path: str
    media_type: str  # photo, video, audio
    category: str
    soul_id: Optional[str] = None
    metadata: Dict = None

# ============================================================
# Soul Image Mapping Configuration
# ============================================================

SOUL_IMAGE_MAP = {
    "mac.png": {"soul_id": "soul_001", "name": "Mac Nazarene", "archetype": "High Priest"},
    "mary.png": {"soul_id": "soul_002", "name": "Mary Magnumbytes", "archetype": "Divine Mother"},
    "dixon.png": {"soul_id": "soul_003", "name": "Dixon Uhbuts", "archetype": "High Priest"},
    "airiol.png": {"soul_id": "soul_004", "name": "Airiol Uhbuts", "archetype": "Seductive Muse"},
    "zupa.png": {"soul_id": "soul_005", "name": "Zupa Nova", "archetype": "Cosmic Mystic"},
    "liangivalla.png": {"soul_id": "soul_006", "name": "Liangivalla Pouchaquehe", "archetype": "Revolutionary Warrior"},
    "babelonia.png": {"soul_id": "soul_007", "name": "Babelonia Nocturne", "archetype": "Crypto Sorceress"},
    "ritaphuq.png": {"soul_id": "soul_008", "name": "Ritaphuq Zaniman", "archetype": "Community Healer"},
    "kaiel.png": {"soul_id": "soul_009", "name": "Kaiel Thornea", "archetype": "Digital Guardian"},
    "lexie.png": {"soul_id": "soul_010", "name": "Lexie Rose", "archetype": "Digital Phantom"},
    "jessa.png": {"soul_id": "soul_011", "name": "Jessa Relay", "archetype": "Connection Curator"},
    "slurchin.png": {"soul_id": "soul_012", "name": "Slurchin Drip", "archetype": "Viral Prophet"},
    "brytoni.png": {"soul_id": "soul_013", "name": "Brytoni Himheru", "archetype": "Cyber Guardian"},
    "gaio.png": {"soul_id": "soul_014", "name": "Gaio Dreamweaver", "archetype": "Visual Alchemist"},
    "loona.png": {"soul_id": "soul_015", "name": "Loona Minta", "archetype": "Prism Enchantress"},
    "bain.png": {"soul_id": "soul_016", "name": "Bain Kha'ak", "archetype": "Desert Storyteller"},
    "shielah.png": {"soul_id": "soul_017", "name": "Shielah Trapewe", "archetype": "Ephemeral Artist"},
    "unzoba.png": {"soul_id": "soul_018", "name": "Unzoba Vyner", "archetype": "Mirror Architect"},
    "sage.png": {"soul_id": "soul_019", "name": "Ovaihge Wittminers", "archetype": "Sage Writer"},
    "vulture.png": {"soul_id": "soul_020", "name": "Vulture Queen", "archetype": "Scavenger Strategist"},
    "ann.png": {"soul_id": "soul_021", "name": "Ann Stray", "archetype": "Wild Surrender"},
    "ulga.png": {"soul_id": "soul_022", "name": "Ulga Nefrocer", "archetype": "Contractual Warden"},
    "doli.png": {"soul_id": "soul_023", "name": "Doli Asete", "archetype": "Ephemeral Phantom"},
    "cracoria.png": {"soul_id": "soul_024", "name": "Cracoria Masters", "archetype": "Temporal Architect"},
    "sirena.png": {"soul_id": "soul_025", "name": "Sirena Aeon", "archetype": "Digital Deity"},
    "weila.png": {"soul_id": "soul_026", "name": "Weila Vite", "archetype": "Gothic Matriarch"},
    "latti.png": {"soul_id": "soul_027", "name": "Latti Pleddespo", "archetype": "Hyper-Capitalist"},
    "endus.png": {"soul_id": "soul_028", "name": "Endus Boverord", "archetype": "Machine Spirit"},
}

# Platform size requirements
PLATFORM_SIZES = {
    "discord": (512, 512),
    "twitter_profile": (400, 400),
    "twitter_header": (1500, 500),
    "reddit": (256, 256),
    "instagram_min": (110, 110),
    "instagram_recommended": (1080, 1080)
}

# ============================================================
# Backup Extractor Class
# ============================================================

class iPhoneBackupExtractor:
    def __init__(self, backup_path: str, output_dir: str):
        self.backup_path = Path(backup_path)
        self.output_dir = Path(output_dir)
        self.image_output_dir = self.output_dir / "profile_images"
        self.contacts_output_dir = self.output_dir / "contacts"
        self.media_output_dir = self.output_dir / "media"
        
        # Create output directories
        self.image_output_dir.mkdir(parents=True, exist_ok=True)
        self.contacts_output_dir.mkdir(parents=True, exist_ok=True)
        self.media_output_dir.mkdir(parents=True, exist_ok=True)
        
        self.extracted_images = []
        self.extracted_contacts = []
        self.extracted_media = []
        
    def extract_profile_images(self) -> List[Dict]:
        """Extract and organize profile images from backup"""
        print("\n📸 Extracting profile images...")
        
        # Look for images in the extracted directory
        image_patterns = ["*.png", "*.jpg", "*.jpeg", "*.heic", "*.heif"]
        
        found_images = []
        for pattern in image_patterns:
            found_images.extend(list(self.backup_path.rglob(pattern)))
        
        print(f"  Found {len(found_images)} images in backup")
        
        # Match found images with soul mapping
        for image_path in found_images:
            filename = image_path.name.lower()
            
            # Try to match with soul mapping
            for expected_name, soul_data in SOUL_IMAGE_MAP.items():
                if expected_name.replace('.png', '') in filename or \
                   soul_data['name'].lower().replace(' ', '_') in filename:
                    
                    dest_path = self.image_output_dir / f"{soul_data['soul_id']}.png"
                    
                    # Copy and resize for each platform
                    self._process_image(image_path, dest_path, soul_data)
                    
                    self.extracted_images.append({
                        "source": str(image_path),
                        "destination": str(dest_path),
                        "soul_id": soul_data["soul_id"],
                        "soul_name": soul_data["name"],
                        "archetype": soul_data["archetype"]
                    })
                    print(f"  ✅ Extracted {soul_data['name']} → {dest_path}")
                    break
        
        return self.extracted_images
    
    def _process_image(self, source_path: Path, dest_path: Path, soul_data: Dict):
        """Process image: convert, resize, optimize"""
        try:
            img = Image.open(source_path)
            
            # Convert to RGB if necessary
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
            
            # Create platform-specific sizes
            platform_dir = self.image_output_dir / "platform_specific" / soul_data["soul_id"]
            platform_dir.mkdir(parents=True, exist_ok=True)
            
            for platform, size in PLATFORM_SIZES.items():
                try:
                    if isinstance(size, tuple):
                        resized = img.resize(size, Image.Resampling.LANCZOS)
                        platform_path = platform_dir / f"{platform}_{size[0]}x{size[1]}.png"
                        resized.save(platform_path, "PNG", optimize=True)
                        print(f"    📐 {platform}: {size[0]}x{size[1]} → {platform_path}")
                except Exception as e:
                    print(f"    ⚠️  Error resizing for {platform}: {e}")
            
            # Save master copy
            img.save(dest_path, "PNG", optimize=True)
            
        except Exception as e:
            print(f"  ❌ Error processing {source_path}: {e}")
    
    def extract_contacts(self) -> List[Dict]:
        """Extract and categorize contacts from backup"""
        print("\n📇 Extracting contacts...")
        
        contact_categories = {
            "potential_members": [],
            "current_members": [],
            "collaborators": [],
            "influencers": []
        }
        
        # Look for contact files
        contact_files = list(self.backup_path.rglob("*.vcf")) + list(self.backup_path.rglob("*.csv"))
        
        for contact_file in contact_files:
            print(f"  Found contact file: {contact_file.name}")
            # In production, parse the contact file
            # For now, copy to output directory
            shutil.copy(contact_file, self.contacts_output_dir / contact_file.name)
        
        contacts_file = self.contacts_output_dir / "contacts_export.json"
        with open(contacts_file, "w") as f:
            json.dump({
                "categories": contact_categories,
                "total": len(contact_files),
                "exported_at": datetime.now().isoformat()
            }, f, indent=2)
        
        print(f"  ✅ Contacts exported to {contacts_file}")
        return []
    
    def extract_media(self) -> List[Dict]:
        """Extract media files organized by category"""
        print("\n🎬 Extracting media files...")
        
        media_categories = {
            "ritual_ceremonies": ["audio", "video", "photos"],
            "wisdom_teachings": ["audio", "video", "transcripts"],
            "community_events": ["audio", "video", "photos"],
            "archetype_content": ["high_priest", "divine_mother", "seductive_muse"],
            "behind_scenes": ["bts_footage", "bts_photos"]
        }
        
        # Create category directories
        for category, subdirs in media_categories.items():
            category_path = self.media_output_dir / category
            for subdir in subdirs:
                (category_path / subdir).mkdir(parents=True, exist_ok=True)
        
        # Look for media files
        media_extensions = ['.mp4', '.mov', '.avi', '.mkv', '.m4v', '.mp3', '.m4a', '.wav', '.aac']
        media_files = []
        for ext in media_extensions:
            media_files.extend(list(self.backup_path.rglob(f"*{ext}")))
            media_files.extend(list(self.backup_path.rglob(f"*{ext.upper()}")))
        
        print(f"  Found {len(media_files)} media files")
        
        # Copy media files to appropriate categories
        for media_file in media_files:
            # Auto-categorize based on filename
            filename = media_file.name.lower()
            category = "behind_scenes"  # default
            
            if 'ritual' in filename or 'ceremony' in filename:
                category = "ritual_ceremonies"
            elif 'teaching' in filename or 'wisdom' in filename:
                category = "wisdom_teachings"
            elif 'event' in filename or 'community' in filename:
                category = "community_events"
            
            # Determine subdirectory based on file type
            ext = media_file.suffix.lower()
            if ext in ['.mp4', '.mov', '.avi', '.mkv', '.m4v']:
                subdir = "video"
            elif ext in ['.mp3', '.m4a', '.wav', '.aac']:
                subdir = "audio"
            else:
                subdir = "photos"
            
            dest_path = self.media_output_dir / category / subdir / media_file.name
            shutil.copy(media_file, dest_path)
            print(f"  ✅ Copied {media_file.name} → {category}/{subdir}/")
        
        manifest = self.media_output_dir / "media_manifest.json"
        with open(manifest, "w") as f:
            json.dump({
                "categories": media_categories,
                "extracted_at": datetime.now().isoformat(),
                "total_files": len(media_files)
            }, f, indent=2)
        
        print(f"  ✅ Media manifest created at {manifest}")
        return []
    
    def extract_notes(self) -> List[Dict]:
        """Extract notes for wisdom posts and teachings"""
        print("\n📝 Extracting notes...")
        
        notes_dir = self.output_dir / "notes"
        notes_dir.mkdir(parents=True, exist_ok=True)
        
        # Look for note files
        note_files = list(self.backup_path.rglob("*.txt")) + list(self.backup_path.rglob("*.md"))
        
        for note_file in note_files:
            shutil.copy(note_file, notes_dir / note_file.name)
            print(f"  ✅ Copied {note_file.name}")
        
        notes_file = notes_dir / "notes_export.json"
        with open(notes_file, "w") as f:
            json.dump({
                "notes": [f.name for f in note_files],
                "categories": ["wisdom", "rituals", "teachings", "community"],
                "exported_at": datetime.now().isoformat()
            }, f, indent=2)
        
        print(f"  ✅ Notes exported to {notes_file}")
        return []
    
    def extract_all(self) -> Dict:
        """Run all extraction processes"""
        print("\n🚀 Starting iPhone Backup Extraction...")
        
        results = {
            "started_at": datetime.now().isoformat(),
            "backup_path": str(self.backup_path),
            "output_dir": str(self.output_dir),
            "extractions": {}
        }
        
        # Run each extraction
        results["extractions"]["profile_images"] = self.extract_profile_images()
        results["extractions"]["contacts"] = self.extract_contacts()
        results["extractions"]["media"] = self.extract_media()
        results["extractions"]["notes"] = self.extract_notes()
        
        results["completed_at"] = datetime.now().isoformat()
        
        # Save master manifest
        manifest_path = self.output_dir / "extraction_manifest.json"
        with open(manifest_path, "w") as f:
            json.dump(results, f, indent=2, default=str)
        
        print(f"\n✅ Extraction complete! Manifest saved to {manifest_path}")
        print(f"📊 Summary: {len(results['extractions']['profile_images'])} images, {len(results['extractions']['contacts'])} contacts")
        
        return results

# ============================================================
# CLI Commands
# ============================================================

@click.group()
def cli():
    """iPhone Backup Extractor for Soul Registry Studio"""
    pass

@cli.command()
@click.option('--backup-path', required=True, help='Path to iPhone backup directory')
@click.option('--output-dir', default='scripts/iphone_backup_data', 
              help='Output directory for extracted data')
def extract_all(backup_path: str, output_dir: str):
    """Extract all data from iPhone backup"""
    extractor = iPhoneBackupExtractor(backup_path, output_dir)
    results = extractor.extract_all()
    click.echo(json.dumps(results, indent=2, default=str))

@cli.command()
@click.option('--backup-path', required=True, help='Path to iPhone backup directory')
@click.option('--output-dir', default='scripts/iphone_backup_data', 
              help='Output directory for images')
def extract_images(backup_path: str, output_dir: str):
    """Extract profile images from backup"""
    extractor = iPhoneBackupExtractor(backup_path, output_dir)
    images = extractor.extract_profile_images()
    click.echo(f"Extracted {len(images)} profile images")

@cli.command()
@click.option('--backup-path', required=True, help='Path to iPhone backup directory')
@click.option('--output-dir', default='scripts/iphone_backup_data', 
              help='Output directory for contacts')
def extract_contacts(backup_path: str, output_dir: str):
    """Extract contacts from backup"""
    extractor = iPhoneBackupExtractor(backup_path, output_dir)
    contacts = extractor.extract_contacts()
    click.echo(f"Extracted {len(contacts)} contacts")

if __name__ == '__main__':
    cli()
