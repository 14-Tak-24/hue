"""
Souls/Entities Manager
Manages the 26+ souls/entities data structure for the Tiapma'atzu platform
"""

import random
import json
import shutil
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path
from dataclasses import dataclass
from enum import Enum
import logging

from .utils import (
    Configuration, DataUtils, ValidationUtils, StringUtils, 
    ErrorUtils, LoggingUtils
)


class Rarity(Enum):
    """Soul rarity levels"""
    COMMON = "Common"
    RARE = "Rare"
    LEGENDARY = "Legendary"


class Gender(Enum):
    """Gender identifiers"""
    MALE = "M"
    FEMALE = "F"


@dataclass
class Soul:
    """Individual soul/entity data structure"""
    id: str
    name: str
    gender: str
    archetype: str
    bio: str
    sensory: str
    voice: str
    hooks: List[str]
    desires: List[str]
    kinks: List[str]
    tribute_impact: str
    shadow_practice: str
    email: str
    image: str
    rarity: str
    platforms: List[str]
    tier: str


class SoulsManager:
    """
    Manager for souls/entities data and operations.
    
    This class provides comprehensive functionality for managing the 26+ souls/entities
    in the Tiapma'atzu platform, including CRUD operations, filtering, analytics,
    backup management, and platform integration.
    
    Attributes:
        data_path: Path to the souls data JSON file
        enable_backups: Whether automatic backups are enabled
        backup_dir: Directory for storing backup files
        logger: Logger instance for operations
        souls_data: Raw souls data dictionary
        souls: Parsed Soul objects indexed by ID
    """
    
    def __init__(self, data_path: Optional[str] = None, enable_backups: bool = True):
        """
        Initialize the souls manager
        
        Args:
            data_path: Path to souls_entities.json file
            enable_backups: Enable automatic backups before modifications
        """
        if data_path is None:
            # Try default path, then fallback path
            data_path = Configuration.DEFAULT_SOULS_DATA
            if not Path(data_path).exists():
                data_path = Configuration.ALT_SOULS_DATA
        
        self.data_path = Path(data_path)
        self.enable_backups = enable_backups
        
        # Use project root backup directory instead of data directory
        project_root = Path(__file__).parent.parent.parent.parent
        self.backup_dir = project_root / Configuration.BACKUP_DIR_NAME
        
        self.logger = LoggingUtils.setup_logger(__name__)
        
        # Create backup directory if enabled
        if self.enable_backups:
            self.backup_dir.mkdir(exist_ok=True)
        
        self.souls_data = self._load_souls_data()
        self.souls = self._parse_souls()
        
    def _load_souls_data(self) -> Dict[str, Any]:
        """Load souls data from JSON file"""
        return DataUtils.load_json_file(self.data_path)
    
    def _create_backup(self) -> Optional[str]:
        """Create a backup of the current souls data file"""
        if not self.enable_backups:
            return None
        
        try:
            backup_path, metadata = DataUtils.create_backup(
                self.data_path, 
                self.backup_dir,
                prefix="souls_entities_"
            )
            
            # Add souls-specific metadata
            metadata['total_souls'] = len(self.souls_data.get('souls', []))
            
            # Update metadata file
            metadata_path = backup_path.with_suffix('.metadata.json')
            DataUtils.save_json_file(metadata, metadata_path)
            
            self.logger.info(f"Backup created: {backup_path}")
            return str(backup_path)
            
        except Exception as e:
            self.logger.error(f"Failed to create backup: {e}")
            return None
    
    def _cleanup_old_backups(self, keep_count: int = Configuration.DEFAULT_BACKUP_COUNT):
        """Remove old backups, keeping only the most recent ones"""
        if not self.enable_backups or not self.backup_dir.exists():
            return
        
        try:
            removed_files = DataUtils.cleanup_old_backups(
                self.backup_dir,
                prefix="souls_entities_",
                keep_count=keep_count
            )
            
            for removed_file in removed_files:
                self.logger.info(f"Removed old backup: {removed_file}")
                
        except Exception as e:
            self.logger.error(f"Failed to cleanup old backups: {e}")
    
    def _parse_souls(self) -> Dict[str, Soul]:
        """Parse souls data into Soul objects"""
        souls = {}
        for soul_data in self.souls_data.get('souls', []):
            soul = Soul(**soul_data)
            souls[soul.id] = soul
        return souls
    
    def get_all_souls(self) -> List[Soul]:
        """Get all souls"""
        return list(self.souls.values())
    
    def get_soul_by_id(self, soul_id: str) -> Optional[Soul]:
        """Get a specific soul by ID"""
        return self.souls.get(soul_id)
    
    def get_soul_by_name(self, name: str) -> Optional[Soul]:
        """Get a specific soul by name"""
        for soul in self.souls.values():
            if soul.name.lower() == name.lower():
                return soul
        return None
    
    def get_souls_by_archetype(self, archetype: str) -> List[Soul]:
        """Get souls by archetype"""
        return [soul for soul in self.souls.values() if soul.archetype == archetype]
    
    def get_souls_by_rarity(self, rarity: str) -> List[Soul]:
        """Get souls by rarity"""
        return [soul for soul in self.souls.values() if soul.rarity == rarity]
    
    def get_souls_by_gender(self, gender: str) -> List[Soul]:
        """Get souls by gender"""
        return [soul for soul in self.souls.values() if soul.gender == gender]
    
    def get_souls_by_platform(self, platform: str) -> List[Soul]:
        """Get souls that use a specific platform"""
        return [soul for soul in self.souls.values() if platform in soul.platforms]
    
    def add_platform_to_soul(self, soul_id: str, platform: str) -> bool:
        """Add a new platform to a soul's platform list"""
        soul = self.get_soul_by_id(soul_id)
        if not soul:
            raise ValueError(f"Soul with ID {soul_id} not found")
        
        if platform in soul.platforms:
            return False  # Platform already exists
        
        soul.platforms.append(platform)
        
        # Update in souls_data list
        for i, soul_data in enumerate(self.souls_data['souls']):
            if soul_data['id'] == soul_id:
                self.souls_data['souls'][i]['platforms'] = soul.platforms
                break
        
        return True
    
    def remove_platform_from_soul(self, soul_id: str, platform: str) -> bool:
        """Remove a platform from a soul's platform list"""
        soul = self.get_soul_by_id(soul_id)
        if not soul:
            raise ValueError(f"Soul with ID {soul_id} not found")
        
        if platform not in soul.platforms:
            return False  # Platform doesn't exist
        
        if len(soul.platforms) <= 1:
            raise ValueError("Cannot remove the last platform from a soul")
        
        soul.platforms.remove(platform)
        
        # Update in souls_data list
        for i, soul_data in enumerate(self.souls_data['souls']):
            if soul_data['id'] == soul_id:
                self.souls_data['souls'][i]['platforms'] = soul.platforms
                break
        
        return True
    
    def get_souls_by_tier(self, tier: str) -> List[Soul]:
        """Get souls by tier (upper/second)"""
        return [soul for soul in self.souls.values() if soul.tier == tier]
    
    def get_random_soul(self) -> Soul:
        """Get a random soul"""
        return random.choice(list(self.souls.values()))
    
    def get_random_soul_by_rarity(self, rarity: str) -> Optional[Soul]:
        """Get a random soul of specific rarity"""
        souls = self.get_souls_by_rarity(rarity)
        if souls:
            return random.choice(souls)
        return None
    
    def search_souls(self, query: str) -> List[Soul]:
        """Search souls by name, bio, or archetype"""
        query = query.lower()
        results: List[Soul] = []
        
        for soul in self.souls.values():
            if (query in soul.name.lower() or 
                query in soul.bio.lower() or 
                query in soul.archetype.lower() or
                query in soul.desires or
                query in soul.kinks):
                results.append(soul)
        
        return results
    
    def get_platforms(self) -> Dict[str, List[str]]:
        """Get all platforms by tier"""
        return self.souls_data.get('platforms', {})
    
    def get_metadata(self) -> Dict[str, Any]:
        """Get metadata about souls collection"""
        return self.souls_data.get('metadata', {})
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about souls collection"""
        souls = self.get_all_souls()
        
        rarity_counts = {}
        gender_counts = {}
        archetype_counts = {}
        platform_counts = {}
        
        for soul in souls:
            # Count by rarity
            rarity_counts[soul.rarity] = rarity_counts.get(soul.rarity, 0) + 1
            
            # Count by gender
            gender_counts[soul.gender] = gender_counts.get(soul.gender, 0) + 1
            
            # Count by archetype
            archetype_counts[soul.archetype] = archetype_counts.get(soul.archetype, 0) + 1
            
            # Count by platforms
            for platform in soul.platforms:
                platform_counts[platform] = platform_counts.get(platform, 0) + 1
        
        return {
            'total_souls': len(souls),
            'rarity_distribution': rarity_counts,
            'gender_distribution': gender_counts,
            'archetype_distribution': archetype_counts,
            'platform_distribution': dict(sorted(platform_counts.items(), key=lambda x: x[1], reverse=True)),
            'metadata': self.get_metadata()
        }
    
    def validate_soul_data(self, soul: Soul) -> List[str]:
        """Validate a soul's data structure"""
        errors = []
        
        # Validate required fields
        required_fields = ['id', 'name', 'archetype', 'bio', 'voice']
        for field in required_fields:
            if not getattr(soul, field, None):
                errors.append(f"Missing required field: {field}")
        
        # Validate field types
        type_requirements = {
            'id': str,
            'name': str,
            'hooks': list,
            'desires': list,
            'kinks': list,
            'platforms': list
        }
        errors.extend(ValidationUtils.validate_field_types(soul.__dict__, type_requirements))
        
        # Validate enum values
        if soul.gender not in ['M', 'F']:
            errors.append(f"Invalid gender: {soul.gender}")
        
        if soul.rarity not in ['Common', 'Rare', 'Legendary']:
            errors.append(f"Invalid rarity: {soul.rarity}")
        
        if soul.tier not in ['upper', 'second']:
            errors.append(f"Invalid tier: {soul.tier}")
        
        # Validate list lengths
        if not soul.hooks or len(soul.hooks) == 0:
            errors.append("Invalid or missing hooks")
        
        if not soul.desires or len(soul.desires) == 0:
            errors.append("Invalid or missing desires")
        
        if not soul.kinks or len(soul.kinks) == 0:
            errors.append("Invalid or missing kinks")
        
        if not soul.platforms or len(soul.platforms) == 0:
            errors.append("Invalid or missing platforms")
        
        return errors
    
    def add_soul(self, soul: Soul) -> bool:
        """Add a new soul to the collection"""
        # Validate soul data
        errors = self.validate_soul_data(soul)
        if errors:
            raise ValueError(f"Invalid soul data: {', '.join(errors)}")
        
        # Check if ID already exists
        if soul.id in self.souls:
            raise ValueError(f"Soul with ID {soul.id} already exists")
        
        # Add soul
        self.souls[soul.id] = soul
        self.souls_data['souls'].append(soul.__dict__)
        
        # Update metadata
        self.souls_data['metadata']['total_souls'] = len(self.souls)
        self.souls_data['metadata']['last_updated'] = str(Path.cwd())
        
        return True
    
    def update_soul(self, soul_id: str, updated_soul: Soul) -> bool:
        """Update an existing soul"""
        if soul_id not in self.souls:
            raise ValueError(f"Soul with ID {soul_id} not found")
        
        # Validate updated soul data
        errors = self.validate_soul_data(updated_soul)
        if errors:
            raise ValueError(f"Invalid soul data: {', '.join(errors)}")
        
        # Update soul
        self.souls[soul_id] = updated_soul
        
        # Update in souls_data list
        for i, soul_data in enumerate(self.souls_data['souls']):
            if soul_data['id'] == soul_id:
                self.souls_data['souls'][i] = updated_soul.__dict__
                break
        
        return True
    
    def delete_soul(self, soul_id: str) -> bool:
        """Delete a soul from the collection"""
        if soul_id not in self.souls:
            raise ValueError(f"Soul with ID {soul_id} not found")
        
        # Remove from souls dict
        del self.souls[soul_id]
        
        # Remove from souls_data list
        self.souls_data['souls'] = [
            soul for soul in self.souls_data['souls'] 
            if soul['id'] != soul_id
        ]
        
        # Update metadata
        self.souls_data['metadata']['total_souls'] = len(self.souls)
        self.souls_data['metadata']['last_updated'] = str(Path.cwd())
        
        return True
    
    def save_souls_data(self, output_path: Optional[str] = None) -> bool:
        """Save souls data to JSON file with backup"""
        if output_path is None:
            output_path = self.data_path
        
        try:
            # Create backup before saving
            if output_path == self.data_path:
                self._create_backup()
            
            # Update metadata
            self.souls_data['metadata']['last_updated'] = datetime.now().isoformat()
            self.souls_data['metadata']['total_souls'] = len(self.souls_data.get('souls', []))
            
            DataUtils.save_json_file(self.souls_data, Path(output_path))
            
            # Cleanup old backups
            if output_path == self.data_path:
                self._cleanup_old_backups()
            
            return True
        except Exception as e:
            raise IOError(f"Failed to save souls data: {e}")
    
    def restore_backup(self, backup_path: str) -> bool:
        """Restore souls data from a backup file"""
        try:
            backup_file = Path(backup_path)
            if not backup_file.exists():
                raise FileNotFoundError(f"Backup file not found: {backup_path}")
            
            # Verify backup metadata
            metadata_file = backup_file.with_suffix('.metadata.json')
            if metadata_file.exists():
                with open(metadata_file, 'r') as f:
                    metadata = json.load(f)
                self.logger.info(f"Restoring backup from {metadata['timestamp']}")
            
            # Create backup of current state before restoring
            self._create_backup()
            
            # Restore from backup
            shutil.copy2(backup_file, self.data_path)
            
            # Reload data
            self.souls_data = self._load_souls_data()
            self.souls = self._parse_souls()
            
            self.logger.info(f"Successfully restored from backup: {backup_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to restore backup: {e}")
            return False
    
    def list_backups(self) -> List[Dict[str, Any]]:
        """List all available backups with metadata"""
        backups = []
        
        if not self.backup_dir.exists():
            return backups
        
        try:
            for backup_file in sorted(
                self.backup_dir.glob("souls_entities_backup_*.json"),
                key=lambda x: x.stat().st_mtime,
                reverse=True
            ):
                metadata_file = backup_file.with_suffix('.metadata.json')
                metadata = {}
                
                if metadata_file.exists():
                    with open(metadata_file, 'r') as f:
                        metadata = json.load(f)
                
                backups.append({
                    'path': str(backup_file),
                    'filename': backup_file.name,
                    'size': backup_file.stat().st_size,
                    'created': datetime.fromtimestamp(backup_file.stat().st_mtime).isoformat(),
                    'metadata': metadata
                })
                
        except Exception as e:
            self.logger.error(f"Failed to list backups: {e}")
        
        return backups
    
    def export_souls_for_platform(self, platform: str) -> List[Dict[str, Any]]:
        """Export souls formatted for a specific platform"""
        platform_souls = self.get_souls_by_platform(platform)
        
        exported_data = []
        for soul in platform_souls:
            exported_data.append({
                'name': soul.name,
                'bio': self._format_bio_for_platform(soul, platform),
                'hooks': soul.hooks,
                'contact': soul.email,
                'archetype': soul.archetype
            })
        
        return exported_data
    
    def _format_bio_for_platform(self, soul: Soul, platform: str) -> str:
        """Format bio for specific platform character limits"""
        max_length = Configuration.PLATFORM_CHAR_LIMITS.get(platform, 300)
        return StringUtils.truncate_text(soul.bio, max_length)
    
    def generate_soul_response(self, soul_id: str, context: str) -> str:
        """Generate a contextual response from a soul"""
        soul = self.get_soul_by_id(soul_id)
        if not soul:
            raise ValueError(f"Soul with ID {soul_id} not found")
        
        # Select appropriate hook based on context
        hook = random.choice(soul.hooks)
        
        # Generate response based on voice and context
        response = f"{hook} {context}"
        
        return response
    
    def get_soul_network_map(self) -> Dict[str, List[str]]:
        """Generate a network map of souls by shared platforms"""
        network_map: Dict[str, List[str]] = {}
        
        for soul_id, soul in self.souls.items():
            connections: List[str] = []
            
            for platform in soul.platforms:
                platform_souls = self.get_souls_by_platform(platform)
                for other_soul in platform_souls:
                    if other_soul.id != soul_id and other_soul.id not in connections:
                        connections.append(other_soul.id)
            
            network_map[soul_id] = connections
        
        return network_map
    
    def get_soul_compatibility_score(self, soul_id1: str, soul_id2: str) -> float:
        """Calculate compatibility score between two souls based on shared platforms and attributes"""
        soul1 = self.get_soul_by_id(soul_id1)
        soul2 = self.get_soul_by_id(soul_id2)
        
        if not soul1 or not soul2:
            return 0.0
        
        score = 0.0
        
        # Platform overlap (max 40 points)
        shared_platforms = set(soul1.platforms) & set(soul2.platforms)
        score += (len(shared_platforms) / max(len(set(soul1.platforms) | set(soul2.platforms)), 1)) * 40
        
        # Tier match (max 20 points)
        if soul1.tier == soul2.tier:
            score += 20
        
        # Archetype compatibility (max 20 points)
        # Simple heuristic: some archetypes work well together
        compatible_archetypes = {
            ('High Priest', 'Divine Mother'),
            ('Digital Guardian', 'Digital Phantom'),
            ('Crypto Sorceress', 'Hyper-Capitalist'),
            ('Community Healer', 'Connection Curator'),
        }
        
        archetype_pair = tuple(sorted([soul1.archetype, soul2.archetype]))
        if archetype_pair in compatible_archetypes:
            score += 20
        elif soul1.archetype == soul2.archetype:
            score += 10
        
        # Rarity balance (max 20 points) - balanced rarity interactions
        rarity_order = {'Common': 1, 'Rare': 2, 'Legendary': 3}
        rarity_diff = abs(rarity_order.get(soul1.rarity, 2) - rarity_order.get(soul2.rarity, 2))
        score += max(0, 20 - (rarity_diff * 10))
        
        return round(score, 2)
    
    def find_compatible_souls(self, soul_id: str, threshold: float = 50.0) -> List[tuple]:
        """Find souls compatible with a given soul above a threshold score"""
        compatible = []
        target_soul = self.get_soul_by_id(soul_id)
        
        if not target_soul:
            return compatible
        
        for other_soul in self.souls.values():
            if other_soul.id != soul_id:
                score = self.get_soul_compatibility_score(soul_id, other_soul.id)
                if score >= threshold:
                    compatible.append((other_soul, score))
        
        # Sort by score descending
        compatible.sort(key=lambda x: x[1], reverse=True)
        return compatible
    
    def create_soul_interaction(self, soul_id1: str, soul_id2: str, interaction_type: str) -> Dict[str, Any]:
        """Create a potential interaction between two souls"""
        soul1 = self.get_soul_by_id(soul_id1)
        soul2 = self.get_soul_by_id(soul_id2)
        
        if not soul1 or not soul2:
            raise ValueError("One or both souls not found")
        
        compatibility_score = self.get_soul_compatibility_score(soul_id1, soul_id2)
        
        # Generate interaction suggestions based on compatibility
        interaction_suggestions = []
        
        if compatibility_score > 70:
            interaction_suggestions.append("High compatibility - consider collaborative content")
            interaction_suggestions.append("Joint live streams or events recommended")
        elif compatibility_score > 50:
            interaction_suggestions.append("Moderate compatibility - cross-promotion opportunities")
            interaction_suggestions.append("Guest appearances or shout-outs")
        else:
            interaction_suggestions.append("Lower compatibility - individual focus recommended")
        
        # Platform overlap analysis
        shared_platforms = set(soul1.platforms) & set(soul2.platforms)
        unique_platforms = set(soul1.platforms) | set(soul2.platforms)
        
        return {
            'soul1': soul1.name,
            'soul2': soul2.name,
            'compatibility_score': compatibility_score,
            'interaction_type': interaction_type,
            'shared_platforms': list(shared_platforms),
            'total_reach': len(unique_platforms),
            'suggestions': interaction_suggestions,
            'recommended_content_types': self._get_content_type_suggestions(soul1, soul2)
        }
    
    def _get_content_type_suggestions(self, soul1: Soul, soul2: Soul) -> List[str]:
        """Get content type suggestions for soul interactions"""
        suggestions = []
        
        # Based on archetypes
        archetype_pairs = {
            ('High Priest', 'Divine Mother'): ['Spiritual discussions', 'Ritual demonstrations'],
            ('Crypto Sorceress', 'Hyper-Capitalist'): ['Financial insights', 'Market analysis'],
            ('Community Healer', 'Connection Curator'): ['Community building', 'Networking events'],
            ('Digital Guardian', 'Digital Phantom'): ['Tech discussions', 'Digital privacy'],
        }
        
        pair = tuple(sorted([soul1.archetype, soul2.archetype]))
        if pair in archetype_pairs:
            suggestions.extend(archetype_pairs[pair])
        else:
            suggestions.append('General collaboration content')
        
        # Based on shared platforms
        shared_platforms = set(soul1.platforms) & set(soul2.platforms)
        if 'YouTube' in shared_platforms:
            suggestions.append('Collaborative videos')
        if 'Twitter' in shared_platforms:
            suggestions.append('Twitter spaces or threads')
        if 'Discord' in shared_platforms:
            suggestions.append('Discord events or AMAs')
        
        return suggestions
    
    def get_trending_platforms(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Get trending platforms based on soul activity"""
        platform_stats = {}
        
        for soul in self.souls.values():
            for platform in soul.platforms:
                if platform not in platform_stats:
                    platform_stats[platform] = {
                        'total_souls': 0,
                        'legendary_souls': 0,
                        'rare_souls': 0,
                        'activity_score': 0
                    }
                
                platform_stats[platform]['total_souls'] += 1
                if soul.rarity == 'Legendary':
                    platform_stats[platform]['legendary_souls'] += 1
                    platform_stats[platform]['activity_score'] += 3
                elif soul.rarity == 'Rare':
                    platform_stats[platform]['rare_souls'] += 1
                    platform_stats[platform]['activity_score'] += 2
                else:
                    platform_stats[platform]['activity_score'] += 1
        
        # Sort by activity score
        trending = sorted(
            platform_stats.items(),
            key=lambda x: x[1]['activity_score'],
            reverse=True
        )[:limit]
        
        return [
            {
                'platform': platform,
                'total_souls': stats['total_souls'],
                'legendary_souls': stats['legendary_souls'],
                'rare_souls': stats['rare_souls'],
                'activity_score': stats['activity_score']
            }
            for platform, stats in trending
        ]
    
    def get_data_integrity_report(self) -> Dict[str, Any]:
        """Generate a data integrity report for the souls collection"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'total_souls': len(self.souls),
            'validation_errors': [],
            'warnings': [],
            'statistics': self.get_statistics()
        }
        
        # Check for data integrity issues
        for soul in self.souls.values():
            errors = self.validate_soul_data(soul)
            if errors:
                report['validation_errors'].append({
                    'soul_id': soul.id,
                    'soul_name': soul.name,
                    'errors': errors
                })
        
        # Check for duplicate IDs
        ids = [soul.id for soul in self.souls.values()]
        if len(ids) != len(set(ids)):
            report['validation_errors'].append({
                'type': 'duplicate_ids',
                'message': 'Duplicate soul IDs detected'
            })
        
        # Check for duplicate emails
        emails = [soul.email for soul in self.souls.values()]
        if len(emails) != len(set(emails)):
            report['warnings'].append({
                'type': 'duplicate_emails',
                'message': 'Duplicate email addresses detected'
            })
        
        # Check for missing images
        missing_images = [soul.id for soul in self.souls.values() if not soul.image or soul.image == '']
        if missing_images:
            report['warnings'].append({
                'type': 'missing_images',
                'souls': missing_images,
                'message': f'{len(missing_images)} souls have missing image URLs'
            })
        
        # Overall health score
        error_count = len(report['validation_errors'])
        warning_count = len(report['warnings'])
        total_souls = len(self.souls)
        
        health_score = 100 - (error_count * 10) - (warning_count * 2)
        health_score = max(0, health_score)
        
        report['health_score'] = health_score
        report['health_status'] = 'excellent' if health_score >= 90 else 'good' if health_score >= 70 else 'fair' if health_score >= 50 else 'poor'
        
        return report


# Convenience functions for common operations
def get_souls_manager(data_path: Optional[str] = None) -> SoulsManager:
    """Get a souls manager instance"""
    return SoulsManager(data_path)


def load_souls(data_path: Optional[str] = None) -> List[Soul]:
    """Load all souls"""
    manager = get_souls_manager(data_path)
    return manager.get_all_souls()


def find_soul_by_name(name: str, data_path: Optional[str] = None) -> Optional[Soul]:
    """Find a soul by name"""
    manager = get_souls_manager(data_path)
    return manager.get_soul_by_name(name)