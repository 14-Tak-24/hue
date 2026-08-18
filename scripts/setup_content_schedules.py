#!/usr/bin/env python3
"""
Setup Initial Content Schedules
Configures automated content generation schedules for all 28 souls
"""

import sys
import json
from pathlib import Path
from datetime import datetime, timedelta

# Add the src directory to the path for package imports
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from modules.souls_manager import SoulsManager
from modules.content_pipeline import ContentPipeline, ContentSchedule, ContentFrequency, ContentCalendar
from modules.openrouter_integration import OpenRouterIntegration
from modules.ai_content_generator import AIContentGenerator


def load_schedule_config(config_path: str) -> dict:
    """Load schedule configuration from JSON file"""
    with open(config_path, 'r') as f:
        return json.load(f)


def create_schedules_from_config(souls_manager: SoulsManager, config: dict) -> list:
    """
    Create content schedules based on configuration
    
    Args:
        souls_manager: SoulsManager instance
        config: Schedule configuration dictionary
        
    Returns:
        List of ContentSchedule objects
    """
    schedules = []
    souls = souls_manager.get_all_souls()
    
    default_settings = config.get('default_settings', {})
    platform_settings = config.get('platform_specific_settings', {})
    priorities = config.get('soul_priorities', {})
    
    for soul in souls:
        # Determine priority-based frequency
        if soul.name in priorities.get('high_priority_souls', []):
            base_frequency = ContentFrequency.DAILY
        elif soul.name in priorities.get('medium_priority_souls', []):
            base_frequency = ContentFrequency.WEEKLY
        else:
            base_frequency = ContentFrequency.BI_WEEKLY
        
        # Create schedules for each platform the soul has
        for platform in soul.platforms:
            platform_config = platform_settings.get(platform, default_settings)
            
            # Map frequency string to enum
            freq_str = platform_config.get('frequency', default_settings.get('frequency', 'weekly'))
            frequency = ContentFrequency(freq_str)
            
            # Get content types for this platform
            content_types = platform_config.get('content_types', 
                                                default_settings.get('content_types', ['post']))
            
            # Create a schedule for each content type
            for content_type in content_types:
                schedule = ContentSchedule(
                    soul_id=soul.id,
                    platform=platform,
                    content_type=content_type,
                    frequency=frequency,
                    preferred_times=default_settings.get('preferred_times', ['09:00', '14:00']),
                    active=default_settings.get('active', True),
                    last_generated=None,
                    next_due=_calculate_next_due(frequency)
                )
                schedules.append(schedule)
    
    return schedules


def _calculate_next_due(frequency: ContentFrequency) -> str:
    """Calculate next due date based on frequency"""
    now = datetime.now()
    
    if frequency == ContentFrequency.DAILY:
        next_due = now + timedelta(days=1)
    elif frequency == ContentFrequency.WEEKLY:
        next_due = now + timedelta(weeks=1)
    elif frequency == ContentFrequency.BI_WEEKLY:
        next_due = now + timedelta(weeks=2)
    elif frequency == ContentFrequency.MONTHLY:
        next_due = now + timedelta(days=30)
    else:
        next_due = now + timedelta(days=1)
    
    return next_due.isoformat()


def setup_initial_schedules():
    """Set up initial content schedules for all souls"""
    print("="*60)
    print("Setting Up Initial Content Schedules")
    print("="*60)
    
    # Load configuration
    config_path = Path(__file__).parent.parent / 'config' / 'initial_content_schedules.json'
    if not config_path.exists():
        print(f"❌ Configuration file not found: {config_path}")
        return False
    
    config = load_schedule_config(str(config_path))
    print(f"✓ Loaded configuration from {config_path}")
    
    # Initialize components
    data_path = Path(__file__).parent.parent / "src" / "data" / "souls_entities.json"
    souls_manager = SoulsManager(str(data_path))
    print(f"✓ Loaded {len(souls_manager.get_all_souls())} souls")
    
    openrouter = OpenRouterIntegration(souls_manager)
    ai_generator = AIContentGenerator(souls_manager)
    pipeline = ContentPipeline(souls_manager, openrouter, ai_generator)
    print("✓ Initialized AI components")
    
    # Create schedules
    schedules = create_schedules_from_config(souls_manager, config)
    print(f"✓ Created {len(schedules)} content schedules")
    
    # Create content calendar
    calendar = ContentCalendar(
        calendar_id="initial_soul_calendar",
        name=config.get('calendar_name', 'Initial Soul Content Schedule'),
        schedules=schedules
    )
    
    # Add calendar to pipeline
    pipeline.calendars[calendar.calendar_id] = calendar
    print(f"✓ Created content calendar: {calendar.name}")
    
    # Print statistics
    print("\n" + "="*60)
    print("Schedule Statistics")
    print("="*60)
    
    # Count by platform
    platform_counts = {}
    for schedule in schedules:
        platform_counts[schedule.platform] = platform_counts.get(schedule.platform, 0) + 1
    
    print(f"Total schedules: {len(schedules)}")
    print(f"Platforms covered: {len(platform_counts)}")
    print("\nSchedules by platform:")
    for platform, count in sorted(platform_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  - {platform}: {count} schedules")
    
    # Count by frequency
    frequency_counts = {}
    for schedule in schedules:
        freq_name = schedule.frequency.value
        frequency_counts[freq_name] = frequency_counts.get(freq_name, 0) + 1
    
    print("\nSchedules by frequency:")
    for freq, count in sorted(frequency_counts.items()):
        print(f"  - {freq}: {count} schedules")
    
    # Save calendar to file for persistence
    calendars_dir = Path(__file__).parent.parent / 'config' / 'calendars'
    calendars_dir.mkdir(exist_ok=True)
    
    calendar_file = calendars_dir / f"{calendar.calendar_id}.json"
    
    # Convert to serializable format
    calendar_data = {
        'calendar_id': calendar.calendar_id,
        'name': calendar.name,
        'created_at': calendar.created_at,
        'updated_at': calendar.updated_at,
        'schedules': [
            {
                'soul_id': s.soul_id,
                'platform': s.platform,
                'content_type': s.content_type,
                'frequency': s.frequency.value,
                'preferred_times': s.preferred_times,
                'active': s.active,
                'last_generated': s.last_generated,
                'next_due': s.next_due
            }
            for s in schedules
        ]
    }
    
    with open(calendar_file, 'w') as f:
        json.dump(calendar_data, f, indent=2)
    
    print(f"\n✓ Saved calendar to: {calendar_file}")
    
    # Update pipeline stats
    stats = pipeline.get_pipeline_statistics()
    print(f"\n✓ Pipeline statistics updated")
    print(f"  - Active calendars: {stats['pipeline_overview']['active_calendars']}")
    print(f"  - Total schedules: {stats['pipeline_overview']['total_schedules']}")
    
    print("\n" + "="*60)
    print("🎉 Initial content schedules setup complete!")
    print("="*60)
    
    return True


if __name__ == "__main__":
    try:
        success = setup_initial_schedules()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
