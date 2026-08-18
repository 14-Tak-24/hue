#!/usr/bin/env python3
"""
Setup Content Schedules for Specific Souls
Configures content generation schedules for high-priority souls based on rarity and platform activity
"""

import sys
import os
from pathlib import Path
import json
from datetime import datetime, timedelta

# Add the src directory to the path for package imports
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from modules.souls_manager import SoulsManager
from modules.content_pipeline import ContentPipeline, ContentCalendar, ContentSchedule, ContentFrequency
from modules.openrouter_integration import OpenRouterIntegration
from modules.ai_content_generator import AIContentGenerator


def setup_priority_soul_schedules():
    """Set up content schedules for priority souls"""
    print("="*60)
    print("Setting Up Content Schedules for Priority Souls")
    print("="*60)
    
    # Initialize components
    data_path = Path(__file__).parent.parent / "src" / "data" / "souls_entities.json"
    souls_manager = SoulsManager(str(data_path))
    
    # Mock AI components for scheduling
    mock_openrouter = None
    mock_generator = None
    
    pipeline = ContentPipeline(souls_manager, mock_openrouter, mock_generator)
    
    # Get all souls
    all_souls = souls_manager.get_all_souls()
    
    # Prioritize souls by rarity and platform count
    priority_souls = []
    for soul in all_souls:
        priority_score = 0
        if soul.rarity == 'Legendary':
            priority_score += 10
        elif soul.rarity == 'Rare':
            priority_score += 5
        elif soul.rarity == 'Epic':
            priority_score += 3
        
        priority_score += len(soul.platforms) * 0.5
        priority_souls.append((soul, priority_score))
    
    # Sort by priority
    priority_souls.sort(key=lambda x: x[1], reverse=True)
    
    print(f"\n📊 Soul Priority Analysis:")
    print(f"   Total souls: {len(all_souls)}")
    print(f"   Legendary: {len([s for s in all_souls if s.rarity == 'Legendary'])}")
    print(f"   Rare: {len([s for s in all_souls if s.rarity == 'Rare'])}")
    print(f"   Common: {len([s for s in all_souls if s.rarity == 'Common'])}")
    
    # Create calendar for top priority souls
    top_n = 10  # Configure schedules for top 10 souls
    top_souls = [soul for soul, score in priority_souls[:top_n]]
    
    print(f"\n🎯 Configuring schedules for top {top_n} priority souls:")
    for i, (soul, score) in enumerate(priority_souls[:top_n], 1):
        print(f"   {i}. {soul.name} ({soul.archetype}) - Score: {score:.1f}")
    
    # Create content calendar
    calendar_id = f"priority_calendar_{datetime.now().strftime('%Y%m%d')}"
    calendar = ContentCalendar(
        calendar_id=calendar_id,
        name="Priority Soul Content Calendar"
    )
    
    # Configure schedules for each priority soul
    for soul in top_souls:
        print(f"\n📝 Setting up schedule for {soul.name}:")
        
        for platform in soul.platforms:
            # Determine frequency based on soul rarity and platform
            if soul.rarity == 'Legendary':
                if platform in ['Twitter', 'Discord']:
                    frequency = ContentFrequency.DAILY
                else:
                    frequency = ContentFrequency.WEEKLY
            elif soul.rarity == 'Rare':
                if platform == 'Twitter':
                    frequency = ContentFrequency.DAILY
                else:
                    frequency = ContentFrequency.WEEKLY
            else:
                if platform in ['Twitter', 'Discord']:
                    frequency = ContentFrequency.WEEKLY
                else:
                    frequency = ContentFrequency.BI_WEEKLY
            
            # Determine content types for platform
            platform_content_types = {
                'Twitter': ['post', 'thread'],
                'Instagram': ['caption', 'story'],
                'Discord': ['message', 'announcement'],
                'FetLife': ['post', 'message'],
                'Reddit': ['post', 'comment'],
                'YouTube': ['script', 'description'],
                'TikTok': ['caption'],
                'Telegram': ['message'],
                'Medium': ['article'],
                'Substack': ['newsletter']
            }
            
            content_types = platform_content_types.get(platform, ['post'])
            
            # Determine optimal posting times
            optimal_times = {
                'Twitter': ['08:00', '12:00', '18:00', '21:00'],
                'Instagram': ['10:00', '14:00', '19:00'],
                'Discord': ['09:00', '15:00', '20:00'],
                'FetLife': ['20:00', '22:00', '23:00'],
                'Reddit': ['07:00', '13:00', '18:00'],
                'YouTube': ['14:00', '16:00', '20:00'],
                'TikTok': ['12:00', '18:00', '21:00'],
                'Telegram': ['09:00', '12:00', '18:00'],
                'Medium': ['09:00', '14:00'],
                'Substack': ['09:00', '14:00']
            }
            
            preferred_times = optimal_times.get(platform, ['12:00'])
            
            # Create schedule for each content type
            for content_type in content_types:
                schedule = ContentSchedule(
                    soul_id=soul.id,
                    platform=platform,
                    content_type=content_type,
                    frequency=frequency,
                    preferred_times=preferred_times,
                    active=True,
                    last_generated=None,
                    next_due=(datetime.now() + timedelta(hours=1)).isoformat()  # Start in 1 hour
                )
                
                calendar.schedules.append(schedule)
                print(f"      ✓ {platform} - {content_type} ({frequency.value}) at {preferred_times[0]}")
    
    # Add calendar to pipeline
    pipeline.calendars[calendar_id] = calendar
    
    # Save calendar to file
    calendars_dir = Path(__file__).parent.parent / "config" / "calendars"
    calendars_dir.mkdir(parents=True, exist_ok=True)
    
    calendar_file = calendars_dir / f"{calendar_id}.json"
    
    # Convert calendar to dict for JSON serialization
    calendar_dict = {
        'calendar_id': calendar.calendar_id,
        'name': calendar.name,
        'created_at': calendar.created_at,
        'updated_at': calendar.updated_at,
        'schedules': [
            {
                'soul_id': schedule.soul_id,
                'platform': schedule.platform,
                'content_type': schedule.content_type,
                'frequency': schedule.frequency.value,
                'preferred_times': schedule.preferred_times,
                'active': schedule.active,
                'last_generated': schedule.last_generated,
                'next_due': schedule.next_due
            }
            for schedule in calendar.schedules
        ]
    }
    
    with open(calendar_file, 'w') as f:
        json.dump(calendar_dict, f, indent=2)
    
    print(f"\n💾 Calendar saved to: {calendar_file}")
    
    # Print summary
    print(f"\n📋 Schedule Summary:")
    print(f"   Calendar ID: {calendar_id}")
    print(f"   Total schedules: {len(calendar.schedules)}")
    print(f"   Souls configured: {len(set(s.soul_id for s in calendar.schedules))}")
    print(f"   Platforms covered: {len(set(s.platform for s in calendar.schedules))}")
    
    # Platform breakdown
    platform_counts = {}
    for schedule in calendar.schedules:
        platform_counts[schedule.platform] = platform_counts.get(schedule.platform, 0) + 1
    
    print(f"\n   Platform breakdown:")
    for platform, count in sorted(platform_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"      {platform}: {count} schedules")
    
    # Frequency breakdown
    frequency_counts = {}
    for schedule in calendar.schedules:
        frequency_counts[schedule.frequency.value] = frequency_counts.get(schedule.frequency.value, 0) + 1
    
    print(f"\n   Frequency breakdown:")
    for freq, count in sorted(frequency_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"      {freq}: {count} schedules")
    
    print("\n" + "="*60)
    print("✅ Content schedules configured successfully!")
    print("="*60)
    
    return calendar


if __name__ == "__main__":
    calendar = setup_priority_soul_schedules()
    sys.exit(0 if calendar else 1)