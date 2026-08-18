"""
Automated Content Pipeline Module
Manages automated content generation for 28 souls across their platforms
"""

import json
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
import random

from .souls_manager import SoulsManager, Soul
from .openrouter_integration import OpenRouterIntegration, ContentRequest, GeneratedContent
from .ai_content_generator import AIContentGenerator
from .utils import LoggingUtils


class ContentFrequency(Enum):
    """Content generation frequency"""
    DAILY = "daily"
    WEEKLY = "weekly"
    BI_WEEKLY = "bi_weekly"
    MONTHLY = "monthly"
    ON_DEMAND = "on_demand"


class ContentStatus(Enum):
    """Status of generated content"""
    PENDING = "pending"
    GENERATING = "generating"
    COMPLETED = "completed"
    FAILED = "failed"
    SCHEDULED = "scheduled"


@dataclass
class ContentSchedule:
    """Schedule for content generation"""
    soul_id: str
    platform: str
    content_type: str
    frequency: ContentFrequency
    preferred_times: List[str] = field(default_factory=list)  # e.g., ["09:00", "18:00"]
    active: bool = True
    last_generated: Optional[str] = None
    next_due: Optional[str] = None


@dataclass
class ContentCalendar:
    """Content calendar for managing scheduled content"""
    calendar_id: str
    name: str
    schedules: List[ContentSchedule] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class ContentHistory:
    """History of generated content"""
    content_id: str
    soul_id: str
    platform: str
    content_type: str
    content: str
    status: ContentStatus
    model_used: str
    generated_at: str
    cost: float
    tokens_used: int
    metadata: Dict[str, Any] = field(default_factory=dict)


class ContentPipeline:
    """
    Automated Content Pipeline for souls
    
    This class manages the end-to-end content generation pipeline for all 28 souls
    across their respective platforms, including scheduling, generation, tracking,
    and optimization.
    """
    
    def __init__(self, souls_manager: SoulsManager, openrouter_integration: OpenRouterIntegration,
                 ai_generator: AIContentGenerator, config_path: Optional[str] = None):
        """
        Initialize the content pipeline
        
        Args:
            souls_manager: SoulsManager instance
            openrouter_integration: OpenRouter integration instance
            ai_generator: AI content generator instance
            config_path: Optional path to pipeline configuration
        """
        self.souls_manager = souls_manager
        self.openrouter = openrouter_integration
        self.ai_generator = ai_generator
        self.logger = LoggingUtils.setup_logger(__name__)
        
        # Load configuration
        self.config = self._load_config(config_path)
        
        # Content calendars
        self.calendars: Dict[str, ContentCalendar] = {}
        
        # Content history
        self.content_history: List[ContentHistory] = []
        
        # Platform-specific content strategies
        self.platform_strategies = self._initialize_platform_strategies()
        
        # Content type templates
        self.content_templates = self._initialize_content_templates()
        
        self.logger.info("Content Pipeline initialized")
    
    def _load_config(self, config_path: Optional[str]) -> Dict[str, Any]:
        """Load pipeline configuration"""
        if config_path is None:
            config_path = Path(__file__).parent.parent.parent / 'config' / 'pipeline_config.json'
        
        config_file = Path(config_path)
        if config_file.exists():
            try:
                with open(config_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                self.logger.warning(f"Failed to load pipeline config: {e}, using defaults")
        
        return {
            'default_frequency': 'weekly',
            'max_daily_content_per_soul': 5,
            'enable_auto_scheduling': True,
            'quality_threshold': 0.7,
            'cost_budget_daily': 20.0,
            'preferred_models': {
                'creative': 'claude-sonnet-46',
                'analytical': 'claude-sonnet-4-5',
                'bulk': 'gemini-2-5-flash'
            }
        }
    
    def _initialize_platform_strategies(self) -> Dict[str, Dict[str, Any]]:
        """Initialize platform-specific content strategies"""
        return {
            'Twitter': {
                'optimal_times': ['08:00', '12:00', '18:00', '21:00'],
                'content_types': ['post', 'thread', 'reply'],
                'frequency': 'daily',
                'engagement_focus': 'high',
                'hashtag_strategy': 'relevant_trending'
            },
            'Instagram': {
                'optimal_times': ['10:00', '14:00', '19:00'],
                'content_types': ['caption', 'story', 'reel'],
                'frequency': 'weekly',
                'engagement_focus': 'medium',
                'visual_priority': True
            },
            'Discord': {
                'optimal_times': ['09:00', '15:00', '20:00'],
                'content_types': ['message', 'announcement', 'discussion'],
                'frequency': 'daily',
                'engagement_focus': 'community',
                'interaction_style': 'conversational'
            },
            'FetLife': {
                'optimal_times': ['20:00', '22:00', '23:00'],
                'content_types': ['post', 'message', 'story'],
                'frequency': 'weekly',
                'engagement_focus': 'intimate',
                'community_guidelines': 'strict'
            },
            'Reddit': {
                'optimal_times': ['07:00', '13:00', '18:00'],
                'content_types': ['post', 'comment', 'ama'],
                'frequency': 'weekly',
                'engagement_focus': 'discussion',
                'subreddit_research': True
            },
            'YouTube': {
                'optimal_times': ['14:00', '16:00', '20:00'],
                'content_types': ['script', 'description', 'community'],
                'frequency': 'weekly',
                'engagement_focus': 'long_form',
                'seo_priority': True
            }
        }
    
    def _initialize_content_templates(self) -> Dict[str, List[str]]:
        """Initialize content templates for different types"""
        return {
            'post': [
                "Share a personal insight related to {desire}",
                "Respond to current events through archetype lens",
                "Share a transformation or breakthrough moment",
                "Ask an engaging question to the community",
                "Share a sensory experience or moment"
            ],
            'story': [
                "A journey through shadow practice",
                "An encounter that challenged {archetype} perspective",
                "A moment of transcendence or transformation",
                "A community experience or gathering",
                "A personal myth or legend"
            ],
            'message': [
                "Welcome new community members",
                "Share gratitude for community support",
                "Offer guidance or wisdom",
                "Share an update on personal journey",
                "Respond to community questions"
            ],
            'bio': [
                "Introduce {archetype} essence and mission",
                "Share the origin story and calling",
                "Describe current practices and explorations",
                "Express vision for community connection",
                "Invite others into shared experience"
            ]
        }
    
    def create_default_calendar(self) -> ContentCalendar:
        """Create a default content calendar for all souls"""
        calendar_id = f"default_calendar_{datetime.now().strftime('%Y%m%d')}"
        calendar = ContentCalendar(
            calendar_id=calendar_id,
            name="Default Soul Content Calendar"
        )
        
        # Generate schedules for all souls
        for soul in self.souls_manager.get_all_souls():
            for platform in soul.platforms:
                platform_strategy = self.platform_strategies.get(platform, {})
                
                # Determine content types for this platform
                content_types = platform_strategy.get('content_types', ['post'])
                
                for content_type in content_types:
                    # Determine frequency based on soul rarity and platform
                    frequency = self._determine_frequency(soul, platform, content_type)
                    
                    # Get optimal posting times
                    optimal_times = platform_strategy.get('optimal_times', ['12:00'])
                    
                    schedule = ContentSchedule(
                        soul_id=soul.id,
                        platform=platform,
                        content_type=content_type,
                        frequency=ContentFrequency(frequency),
                        preferred_times=optimal_times,
                        active=True
                    )
                    
                    calendar.schedules.append(schedule)
        
        self.calendars[calendar_id] = calendar
        self.logger.info(f"Created default calendar with {len(calendar.schedules)} schedules")
        return calendar
    
    def _determine_frequency(self, soul: Soul, platform: str, content_type: str) -> str:
        """Determine content frequency based on soul attributes and platform"""
        # Legendary souls get more frequent content
        if soul.rarity == 'Legendary':
            if platform in ['Twitter', 'Discord']:
                return 'daily'
            return 'weekly'
        
        # Rare souls get moderate frequency
        if soul.rarity == 'Rare':
            if platform == 'Twitter':
                return 'daily'
            return 'weekly'
        
        # Common souls get standard frequency
        if platform in ['Twitter', 'Discord']:
            return 'weekly'
        return 'bi_weekly'
    
    def generate_due_content(self, calendar_id: Optional[str] = None) -> List[GeneratedContent]:
        """
        Generate content that is due based on schedules
        
        Args:
            calendar_id: Optional calendar ID, uses default if not specified
            
        Returns:
            List of generated content
        """
        if calendar_id is None:
            calendar_id = f"default_calendar_{datetime.now().strftime('%Y%m%d')}"
        
        if calendar_id not in self.calendars:
            self.logger.warning(f"Calendar {calendar_id} not found, creating default")
            self.create_default_calendar()
            calendar_id = f"default_calendar_{datetime.now().strftime('%Y%m%d')}"
        
        calendar = self.calendars[calendar_id]
        now = datetime.now()
        due_schedules = []
        
        # Check which schedules are due
        for schedule in calendar.schedules:
            if not schedule.active:
                continue
            
            if schedule.next_due and datetime.fromisoformat(schedule.next_due) <= now:
                due_schedules.append(schedule)
            elif schedule.last_generated is None:
                # Never generated, schedule now
                due_schedules.append(schedule)
        
        self.logger.info(f"Found {len(due_schedules)} due content schedules")
        
        # Generate content for due schedules
        generated_content = []
        for schedule in due_schedules:
            try:
                content = self._generate_scheduled_content(schedule)
                generated_content.append(content)
                
                # Update schedule
                schedule.last_generated = datetime.now().isoformat()
                schedule.next_due = self._calculate_next_due(schedule.frequency).isoformat()
                
            except Exception as e:
                self.logger.error(f"Failed to generate content for schedule {schedule.soul_id}: {e}")
                continue
        
        # Update calendar
        calendar.updated_at = datetime.now().isoformat()
        
        return generated_content
    
    def _calculate_next_due(self, frequency: ContentFrequency) -> datetime:
        """Calculate when content is next due based on frequency"""
        now = datetime.now()
        
        if frequency == ContentFrequency.DAILY:
            return now + timedelta(days=1)
        elif frequency == ContentFrequency.WEEKLY:
            return now + timedelta(weeks=1)
        elif frequency == ContentFrequency.BI_WEEKLY:
            return now + timedelta(weeks=2)
        elif frequency == ContentFrequency.MONTHLY:
            return now + timedelta(days=30)
        else:
            return now + timedelta(days=7)  # Default to weekly
    
    def _generate_scheduled_content(self, schedule: ContentSchedule) -> GeneratedContent:
        """Generate content for a specific schedule"""
        soul = self.souls_manager.get_soul_by_id(schedule.soul_id)
        if not soul:
            raise ValueError(f"Soul {schedule.soul_id} not found")
        
        # Select content template
        templates = self.content_templates.get(schedule.content_type, ['Share something authentic'])
        template = random.choice(templates)
        
        # Customize template for soul
        context = template.format(
            desire=random.choice(soul.desires),
            archetype=soul.archetype
        )
        
        # Create content request
        request = ContentRequest(
            soul_id=schedule.soul_id,
            platform=schedule.platform,
            content_type=schedule.content_type,
            context=context,
            tone='authentic to soul voice',
            length='medium'
        )
        
        # Generate content using OpenRouter for quality
        generated = self.openrouter.generate_soul_content(soul, request)
        
        # Add to history
        history_entry = ContentHistory(
            content_id=f"{schedule.soul_id}_{schedule.platform}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            soul_id=schedule.soul_id,
            platform=schedule.platform,
            content_type=schedule.content_type,
            content=generated.content,
            status=ContentStatus.COMPLETED,
            model_used=generated.model_used,
            generated_at=generated.generated_at,
            cost=generated.cost_estimate or 0.0,
            tokens_used=generated.tokens_used or 0,
            metadata=generated.metadata or {}
        )
        
        self.content_history.append(history_entry)
        
        return generated
    
    def generate_campaign(self, campaign_name: str, soul_ids: List[str], 
                        platforms: List[str], content_types: List[str],
                        timeline_days: int = 7) -> Dict[str, Any]:
        """
        Generate a coordinated content campaign across multiple souls and platforms
        
        Args:
            campaign_name: Name of the campaign
            soul_ids: List of soul IDs to include
            platforms: List of platforms to target
            content_types: List of content types to generate
            timeline_days: Duration of campaign in days
            
        Returns:
            Campaign results with generated content and schedule
        """
        self.logger.info(f"Starting campaign: {campaign_name}")
        
        campaign_results = {
            'campaign_name': campaign_name,
            'souls_targeted': soul_ids,
            'platforms': platforms,
            'content_types': content_types,
            'timeline_days': timeline_days,
            'generated_content': [],
            'schedule': [],
            'total_cost': 0.0,
            'started_at': datetime.now().isoformat()
        }
        
        # Generate content requests
        requests = []
        for soul_id in soul_ids:
            soul = self.souls_manager.get_soul_by_id(soul_id)
            if not soul:
                continue
            
            for platform in platforms:
                if platform not in soul.platforms:
                    continue
                
                for content_type in content_types:
                    request = ContentRequest(
                        soul_id=soul_id,
                        platform=platform,
                        content_type=content_type,
                        context=f"Campaign: {campaign_name}",
                        tone='campaign_consistent',
                        length='medium'
                    )
                    requests.append(request)
        
        # Generate content in batch
        generated_contents = self.openrouter.generate_batch_soul_content(requests)
        
        # Add to results
        for content in generated_contents:
            campaign_results['generated_content'].append(content)
            campaign_results['total_cost'] += content.cost_estimate or 0.0
        
        # Create schedule for campaign
        for i, content in enumerate(generated_contents):
            day_offset = (i // len(requests)) * (timeline_days // len(generated_contents))
            scheduled_time = datetime.now() + timedelta(days=day_offset)
            
            campaign_results['schedule'].append({
                'content_id': content.soul_id,
                'platform': content.platform,
                'scheduled_for': scheduled_time.isoformat(),
                'content_type': content.content_type
            })
        
        campaign_results['completed_at'] = datetime.now().isoformat()
        campaign_results['total_pieces'] = len(generated_contents)
        
        self.logger.info(f"Campaign completed: {len(generated_contents)} pieces generated")
        return campaign_results
    
    def get_pipeline_statistics(self) -> Dict[str, Any]:
        """Get comprehensive pipeline statistics"""
        total_souls = len(self.souls_manager.get_all_souls())
        total_platforms = len(self.platform_strategies)
        
        # Content generation stats
        total_generated = len(self.content_history)
        total_cost = sum(h.cost for h in self.content_history)
        total_tokens = sum(h.tokens_used for h in self.content_history)
        
        # Platform breakdown
        platform_breakdown = {}
        for history in self.content_history:
            if history.platform not in platform_breakdown:
                platform_breakdown[history.platform] = 0
            platform_breakdown[history.platform] += 1
        
        # Soul activity
        soul_activity = {}
        for history in self.content_history:
            if history.soul_id not in soul_activity:
                soul_activity[history.soul_id] = 0
            soul_activity[history.soul_id] += 1
        
        return {
            'pipeline_overview': {
                'total_souls': total_souls,
                'total_platforms': total_platforms,
                'active_calendars': len(self.calendars),
                'total_schedules': sum(len(c.schedules) for c in self.calendars.values())
            },
            'content_generation': {
                'total_generated': total_generated,
                'total_cost': total_cost,
                'total_tokens': total_tokens,
                'average_cost_per_piece': total_cost / total_generated if total_generated > 0 else 0
            },
            'platform_breakdown': platform_breakdown,
            'soul_activity': soul_activity,
            'openrouter_stats': self.openrouter.get_usage_statistics()
        }
    
    def optimize_pipeline(self) -> Dict[str, Any]:
        """Analyze and optimize pipeline performance"""
        stats = self.get_pipeline_statistics()
        
        recommendations = []
        
        # Cost optimization
        if stats['content_generation']['average_cost_per_piece'] > 0.5:
            recommendations.append({
                'type': 'cost',
                'message': 'Consider using more cost-effective models for bulk content',
                'action': 'Switch to gemini-2-5-flash for routine posts'
            })
        
        # Activity optimization
        inactive_souls = [soul_id for soul_id, count in stats['soul_activity'].items() if count == 0]
        if inactive_souls:
            recommendations.append({
                'type': 'activity',
                'message': f'{len(inactive_souls)} souls have no generated content',
                'action': 'Schedule initial content for inactive souls'
            })
        
        # Platform optimization
        underutilized_platforms = [
            platform for platform, count in stats['platform_breakdown'].items() 
            if count < stats['pipeline_overview']['total_souls'] * 0.5
        ]
        if underutilized_platforms:
            recommendations.append({
                'type': 'platform',
                'message': f'Underutilized platforms: {", ".join(underutilized_platforms)}',
                'action': 'Increase content frequency for these platforms'
            })
        
        return {
            'current_stats': stats,
            'recommendations': recommendations,
            'optimization_score': self._calculate_optimization_score(stats)
        }
    
    def _calculate_optimization_score(self, stats: Dict[str, Any]) -> float:
        """Calculate overall pipeline optimization score (0-100)"""
        score = 100.0
        
        # Deduct for inactive souls
        inactive_ratio = len([s for s, c in stats['soul_activity'].items() if c == 0]) / stats['pipeline_overview']['total_souls']
        score -= inactive_ratio * 20
        
        # Deduct for high costs
        if stats['content_generation']['average_cost_per_piece'] > 0.5:
            score -= 10
        
        # Deduct for platform imbalance
        platform_counts = list(stats['platform_breakdown'].values())
        if platform_counts:
            platform_variance = max(platform_counts) - min(platform_counts)
            score -= min(platform_variance / stats['pipeline_overview']['total_souls'] * 10, 15)
        
        return max(0, min(100, score))
    
    def save_pipeline_state(self, output_path: Optional[str] = None):
        """Save pipeline state to file"""
        if output_path is None:
            output_path = Path(__file__).parent.parent.parent / 'data' / 'pipeline_state.json'
        
        state = {
            'calendars': {k: v.__dict__ for k, v in self.calendars.items()},
            'content_history': [h.__dict__ for h in self.content_history],
            'statistics': self.get_pipeline_statistics(),
            'saved_at': datetime.now().isoformat()
        }
        
        Path(output_path).parent.mkdir(exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(state, f, indent=2, default=str)
        
        self.logger.info(f"Pipeline state saved to {output_path}")
    
    def load_pipeline_state(self, input_path: Optional[str]):
        """Load pipeline state from file"""
        if input_path is None:
            input_path = Path(__file__).parent.parent.parent / 'data' / 'pipeline_state.json'
        
        try:
            with open(input_path, 'r') as f:
                state = json.load(f)
            
            # Restore calendars
            self.calendars = {}
            for k, v in state['calendars'].items():
                self.calendars[k] = ContentCalendar(**v)
            
            # Restore content history
            self.content_history = [ContentHistory(**h) for h in state['content_history']]
            
            self.logger.info(f"Pipeline state loaded from {input_path}")
            
        except Exception as e:
            self.logger.error(f"Failed to load pipeline state: {e}")