"""
Content Pipeline Module
Orchestrates AI content generation for the 28 souls across platforms
"""

import logging
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import json
import sys

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent / "src"))

from modules.souls_manager import SoulsManager
from modules.utils import Configuration, LoggingUtils

from .image_generator import ImageGenerator
from .video_generator import VideoGenerator
from .avatar_generator import AvatarGenerator
from .llm_agent import LLMAgent


class ContentPipeline:
    """
    Content Pipeline for automated AI content generation
    
    Orchestrates the creation of images, videos, avatars, and text content
    for the 28 souls of Tiapma'atzu across their platforms.
    """
    
    def __init__(self, souls_manager: Optional[SoulsManager] = None):
        """
        Initialize the content pipeline
        
        Args:
            souls_manager: SoulsManager instance for character data
        """
        self.logger = LoggingUtils.setup_logger(__name__)
        self.souls_manager = souls_manager or SoulsManager()
        
        # Initialize generators
        self.image_generator = ImageGenerator(self.souls_manager)
        self.video_generator = VideoGenerator(self.souls_manager)
        self.avatar_generator = AvatarGenerator(self.souls_manager)
        self.llm_agent = LLMAgent(self.souls_manager)
        
        # Pipeline configuration
        self.config_dir = Path(__file__).parent.parent / "config"
        self.config_dir.mkdir(exist_ok=True)
        
        # Load or create pipeline configuration
        self.pipeline_config = self._load_pipeline_config()
        
        self.logger.info("Content Pipeline initialized")
    
    def _load_pipeline_config(self) -> Dict[str, Any]:
        """Load pipeline configuration"""
        config_file = self.config_dir / "pipeline_config.json"
        
        if config_file.exists():
            with open(config_file, 'r') as f:
                return json.load(f)
        
        # Default configuration
        default_config = {
            'default_models': {
                'image': 'flux_dev_lora',
                'video': 'veo_3_1_fast',
                'avatar': 'p_video_avatar',
                'llm': 'claude_sonnet'
            },
            'platform_schedules': {
                'Twitter': {'frequency': 'daily', 'content_types': ['text', 'image']},
                'Instagram': {'frequency': 'daily', 'content_types': ['image', 'video']},
                'TikTok': {'frequency': 'daily', 'content_types': ['video', 'avatar']},
                'YouTube': {'frequency': 'weekly', 'content_types': ['video', 'avatar']},
                'AFF': {'frequency': 'weekly', 'content_types': ['text', 'image']},
            },
            'soul_priorities': {},
            'content_templates': {}
        }
        
        with open(config_file, 'w') as f:
            json.dump(default_config, f, indent=2)
        
        return default_config
    
    def generate_daily_content(
        self,
        soul_ids: Optional[List[str]] = None,
        platforms: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Generate daily content for souls
        
        Args:
            soul_ids: List of soul IDs (default: all active souls)
            platforms: List of platforms (default: all platforms)
            
        Returns:
            Generation results summary
        """
        if soul_ids is None:
            soul_ids = [soul.id for soul in self.souls_manager.get_all_souls()]
        
        if platforms is None:
            platforms = ['Twitter', 'Instagram', 'TikTok']
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'soul_ids': soul_ids,
            'platforms': platforms,
            'generations': {}
        }
        
        for soul_id in soul_ids:
            soul = self.souls_manager.get_soul_by_id(soul_id)
            if not soul:
                continue
            
            soul_results = {}
            
            for platform in platforms:
                if platform not in soul.platforms:
                    continue
                
                # Generate content based on platform schedule
                platform_config = self.pipeline_config['platform_schedules'].get(platform, {})
                content_types = platform_config.get('content_types', ['text'])
                
                for content_type in content_types:
                    try:
                        if content_type == 'text':
                            result = self.llm_agent.generate_social_media_post(soul_id, platform)
                        elif content_type == 'image':
                            result = self.image_generator.generate_platform_content(soul_id, platform)
                        elif content_type == 'video':
                            result = self.video_generator.generate_platform_video(soul_id, platform)
                        elif content_type == 'avatar':
                            result = self.avatar_generator.generate_ugc_avatar(soul_id, "Welcome to my channel!")
                        
                        soul_results[f"{platform}_{content_type}"] = result
                        
                    except Exception as e:
                        self.logger.error(f"Error generating {content_type} for {soul_id} on {platform}: {e}")
                        soul_results[f"{platform}_{content_type}"] = {'error': str(e)}
            
            results['generations'][soul_id] = soul_results
        
        # Save results
        self._save_pipeline_results('daily_content', results)
        
        return results
    
    def generate_soul_package(
        self,
        soul_id: str,
        include_portrait: bool = True,
        include_avatar: bool = True,
        include_content: bool = True
    ) -> Dict[str, Any]:
        """
        Generate complete content package for a soul
        
        Args:
            soul_id: Soul ID
            include_portrait: Include portrait generation
            include_avatar: Include avatar video
            include_content: Include content for all platforms
            
        Returns:
            Complete package results
        """
        soul = self.souls_manager.get_soul_by_id(soul_id)
        if not soul:
            return {'error': f'Soul {soul_id} not found'}
        
        results = {
            'soul_id': soul_id,
            'soul_name': soul.name,
            'archetype': soul.archetype,
            'timestamp': datetime.now().isoformat(),
            'components': {}
        }
        
        # Generate portrait
        if include_portrait:
            self.logger.info(f"Generating portrait for {soul_id}")
            portrait_result = self.image_generator.generate_soul_portrait(soul_id)
            results['components']['portrait'] = portrait_result
        
        # Generate avatar
        if include_avatar:
            self.logger.info(f"Generating avatar for {soul_id}")
            avatar_result = self.avatar_generator.generate_welcome_video(soul_id)
            results['components']['avatar'] = avatar_result
        
        # Generate platform content
        if include_content:
            self.logger.info(f"Generating platform content for {soul_id}")
            content_results = {}
            
            for platform in soul.platforms:
                try:
                    # Generate text content
                    text_result = self.llm_agent.generate_social_media_post(soul_id, platform)
                    content_results[f"{platform}_text"] = text_result
                    
                    # Generate image for visual platforms
                    if platform in ['Instagram', 'Twitter', 'AFF']:
                        image_result = self.image_generator.generate_platform_content(soul_id, platform)
                        content_results[f"{platform}_image"] = image_result
                    
                except Exception as e:
                    self.logger.error(f"Error generating content for {platform}: {e}")
                    content_results[f"{platform}_error"] = str(e)
            
            results['components']['platform_content'] = content_results
        
        # Save package
        self._save_pipeline_results(f"soul_package_{soul_id}", results)
        
        return results
    
    def generate_campaign_content(
        self,
        campaign_name: str,
        soul_ids: Optional[List[str]] = None,
        duration_days: int = 7
    ) -> Dict[str, Any]:
        """
        Generate content for a campaign
        
        Args:
            campaign_name: Name of the campaign
            soul_ids: Participating souls (default: all)
            duration_days: Campaign duration in days
            
        Returns:
            Campaign generation results
        """
        if soul_ids is None:
            soul_ids = [soul.id for soul in self.souls_manager.get_all_souls()]
        
        results = {
            'campaign_name': campaign_name,
            'duration_days': duration_days,
            'soul_ids': soul_ids,
            'start_date': datetime.now().isoformat(),
            'end_date': (datetime.now() + timedelta(days=duration_days)).isoformat(),
            'daily_schedule': {}
        }
        
        # Generate daily schedule
        for day in range(duration_days):
            day_date = datetime.now() + timedelta(days=day)
            day_key = day_date.strftime('%Y-%m-%d')
            
            # Rotate through souls for each day
            daily_souls = soul_ids[day % len(soul_ids)]
            
            day_results = self.generate_daily_content(
                soul_ids=[daily_souls],
                platforms=['Twitter', 'Instagram']
            )
            
            results['daily_schedule'][day_key] = day_results
        
        # Save campaign
        self._save_pipeline_results(f"campaign_{campaign_name}", results)
        
        return results
    
    def _save_pipeline_results(self, result_type: str, results: Dict[str, Any]):
        """Save pipeline results"""
        results_dir = Path(__file__).parent.parent / "exports"
        results_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        result_file = results_dir / f"{result_type}_{timestamp}.json"
        
        with open(result_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        self.logger.info(f"Saved pipeline results to {result_file}")
    
    def get_pipeline_status(self) -> Dict[str, Any]:
        """Get current pipeline status"""
        return {
            'souls_count': len(self.souls_manager.get_all_souls()),
            'platforms_configured': list(self.pipeline_config['platform_schedules'].keys()),
            'default_models': self.pipeline_config['default_models'],
            'last_updated': datetime.now().isoformat()
        }


if __name__ == '__main__':
    # Test the content pipeline
    pipeline = ContentPipeline()
    
    # Generate daily content for Mac Nazarene
    result = pipeline.generate_daily_content(soul_ids=['soul_001'])
    print(f"Daily content generation result: {result}")
    
    # Generate complete soul package for Mac Nazarene
    package_result = pipeline.generate_soul_package('soul_001')
    print(f"Soul package result: {package_result}")
