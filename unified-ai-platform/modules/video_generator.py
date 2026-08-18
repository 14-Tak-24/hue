"""
AI Video Generator Module
Generates videos for souls using Veo, Seedance, and Wan models via inference.sh CLI
"""

import subprocess
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime
import sys

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent / "src"))

from modules.souls_manager import SoulsManager
from modules.utils import Configuration, LoggingUtils


class VideoGenerator:
    """
    AI Video Generator using inference.sh CLI
    
    Generates video content for the 28 souls of Tiapma'atzu including:
    - Text-to-video generation
    - Image-to-video animation
    - Avatar talking head videos
    """
    
    def __init__(self, souls_manager: Optional[SoulsManager] = None):
        """
        Initialize the video generator
        
        Args:
            souls_manager: SoulsManager instance for character data
        """
        self.logger = LoggingUtils.setup_logger(__name__)
        self.souls_manager = souls_manager or SoulsManager()
        
        # Output directories
        self.output_dir = Path(__file__).parent.parent / "content" / "videos"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Model configurations
        self.text_to_video_models = {
            'veo_3_1_fast': 'google/veo-3-1-fast',  # Fast with audio
            'veo_3_1': 'google/veo-3-1',  # Best quality
            'seedance_2_0': 'bytedance/seedance-2-0',  # With sync audio
            'happyhorse_t2v': 'alibaba/happyhorse-1-0-t2v',  # Physically realistic
            'p_video': 'pruna/p-video',  # Fast & economical
        }
        
        self.image_to_video_models = {
            'wan_2_5': 'falai/wan-2-5',  # High quality
            'wan_2_5_i2v': 'falai/wan-2-5-i2v',  # Enhanced i2v
            'seedance_2_0': 'bytedance/seedance-2-0',  # With audio
            'happyhorse_i2v': 'alibaba/happyhorse-1-0-i2v',  # Character-preserving
        }
        
        self.default_t2v_model = 'veo_3_1_fast'
        self.default_i2v_model = 'wan_2_5'
        
        self.logger.info("Video Generator initialized")
    
    def _run_belt_command(self, app_id: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute belt CLI command
        
        Args:
            app_id: inference.sh app ID
            input_data: Input parameters for the app
            
        Returns:
            Command output as dictionary
        """
        try:
            input_json = json.dumps(input_data)
            cmd = ['belt', 'app', 'run', app_id, '--input', input_json]
            
            self.logger.info(f"Running: {' '.join(cmd)}")
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=600  # 10 minute timeout for video
            )
            
            if result.returncode != 0:
                self.logger.error(f"Belt command failed: {result.stderr}")
                return {'error': result.stderr}
            
            # Parse output
            try:
                output = json.loads(result.stdout)
                self.logger.info(f"Video generation successful")
                return output
            except json.JSONDecodeError:
                self.logger.warning(f"Could not parse output as JSON: {result.stdout}")
                return {'raw_output': result.stdout}
                
        except subprocess.TimeoutExpired:
            self.logger.error("Belt command timed out")
            return {'error': 'Command timed out'}
        except Exception as e:
            self.logger.error(f"Belt command error: {e}")
            return {'error': str(e)}
    
    def generate_text_to_video(
        self,
        soul_id: str,
        prompt: str,
        duration: int = 5,
        model: Optional[str] = None,
        generate_audio: bool = True
    ) -> Dict[str, Any]:
        """
        Generate video from text prompt
        
        Args:
            soul_id: Soul ID
            prompt: Video description
            duration: Video duration in seconds
            model: Model to use
            generate_audio: Whether to generate audio
            
        Returns:
            Generation result with video URL
        """
        soul = self.souls_manager.get_soul_by_id(soul_id)
        if not soul:
            return {'error': f'Soul {soul_id} not found'}
        
        # Build enhanced prompt
        enhanced_prompt = self._build_video_prompt(soul, prompt)
        
        # Select model
        model = model or self.default_t2v_model
        app_id = self.text_to_video_models.get(model, self.text_to_video_models[self.default_t2v_model])
        
        # Prepare input based on model
        input_data = {
            'prompt': enhanced_prompt,
        }
        
        # Add model-specific parameters
        if 'veo' in model:
            input_data['duration'] = duration
        elif 'seedance' in model:
            input_data['duration'] = duration
            input_data['generate_audio'] = generate_audio
        elif 'happyhorse' in model:
            input_data['duration'] = duration
            input_data['resolution'] = '1080P'
        elif 'p_video' in model:
            input_data['duration'] = duration
        
        # Generate
        result = self._run_belt_command(app_id, input_data)
        
        if 'error' not in result:
            self._save_generation_metadata(
                soul_id, 'text_to_video', result, model, prompt, duration
            )
        
        return result
    
    def generate_image_to_video(
        self,
        soul_id: str,
        image_url: str,
        prompt: str = "",
        duration: int = 5,
        model: Optional[str] = None,
        generate_audio: bool = True
    ) -> Dict[str, Any]:
        """
        Animate image to video
        
        Args:
            soul_id: Soul ID
            image_url: URL of source image
            prompt: Animation description
            duration: Video duration in seconds
            model: Model to use
            generate_audio: Whether to generate audio
            
        Returns:
            Generation result with video URL
        """
        soul = self.souls_manager.get_soul_by_id(soul_id)
        if not soul:
            return {'error': f'Soul {soul_id} not found'}
        
        # Build animation prompt
        animation_prompt = self._build_animation_prompt(soul, prompt)
        
        # Select model
        model = model or self.default_i2v_model
        app_id = self.image_to_video_models.get(model, self.image_to_video_models[self.default_i2v_model])
        
        # Prepare input
        input_data = {
            'image': image_url,
            'prompt': animation_prompt,
        }
        
        # Add model-specific parameters
        if 'seedance' in model:
            input_data['duration'] = duration
            input_data['generate_audio'] = generate_audio
        elif 'happyhorse' in model:
            input_data['duration'] = duration
            input_data['resolution'] = '1080P'
        elif 'wan' in model:
            # Wan models don't support duration parameter
            pass
        
        # Generate
        result = self._run_belt_command(app_id, input_data)
        
        if 'error' not in result:
            self._save_generation_metadata(
                soul_id, 'image_to_video', result, model, prompt, duration
            )
        
        return result
    
    def generate_reference_to_video(
        self,
        soul_id: str,
        reference_image_url: str,
        prompt: str,
        duration: int = 5,
        model: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate video with character from reference image
        
        Args:
            soul_id: Soul ID
            reference_image_url: URL of reference character image
            prompt: Video description
            duration: Video duration in seconds
            model: Model to use
            
        Returns:
            Generation result with video URL
        """
        soul = self.souls_manager.get_soul_by_id(soul_id)
        if not soul:
            return {'error': f'Soul {soul_id} not found'}
        
        # Build prompt
        enhanced_prompt = f"A person who looks like the reference {prompt}"
        
        # Use Seedance for reference-to-video
        model = model or 'seedance_2_0'
        app_id = self.text_to_video_models.get(model, self.text_to_video_models['seedance_2_0'])
        
        # Prepare input
        input_data = {
            'prompt': enhanced_prompt,
            'reference_image': reference_image_url,
            'duration': duration,
            'generate_audio': True
        }
        
        # Generate
        result = self._run_belt_command(app_id, input_data)
        
        if 'error' not in result:
            self._save_generation_metadata(
                soul_id, 'reference_to_video', result, model, prompt, duration
            )
        
        return result
    
    def _build_video_prompt(self, soul, prompt: str) -> str:
        """Build enhanced video prompt based on soul characteristics"""
        base_prompt = f"{soul.name} {prompt}"
        
        # Add sensory profile
        if hasattr(soul, 'sensory'):
            base_prompt += f", {soul.sensory}"
        
        # Add archetype-specific elements
        archetype_elements = {
            'High Priest': 'sacred atmosphere, divine presence, ritual movements',
            'Divine Mother': 'nurturing energy, gentle movements, warm lighting',
            'Seductive Muse': 'alluring presence, graceful movements, artistic setting',
            'Cosmic Mystic': 'cosmic energy, ethereal lighting, mystical elements',
            'Revolutionary Warrior': 'dynamic energy, powerful movements, intense atmosphere',
        }
        
        archetype_prompt = archetype_elements.get(soul.archetype, 'unique character presence')
        
        return f"{base_prompt}, {archetype_prompt}, cinematic quality, smooth camera movement"
    
    def _build_animation_prompt(self, soul, prompt: str) -> str:
        """Build animation prompt for image-to-video"""
        if prompt:
            return f"{prompt}, subtle camera movement, natural motion"
        return "gentle camera movement, natural breathing motion, subtle motion"
    
    def _save_generation_metadata(
        self,
        soul_id: str,
        content_type: str,
        result: Dict[str, Any],
        model: str,
        prompt: str,
        duration: int
    ):
        """Save generation metadata"""
        metadata = {
            'soul_id': soul_id,
            'content_type': content_type,
            'model': model,
            'prompt': prompt,
            'duration': duration,
            'timestamp': datetime.now().isoformat(),
            'result': result
        }
        
        # Save to logs
        log_file = self.output_dir / f"{soul_id}_{content_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(log_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        self.logger.info(f"Saved metadata to {log_file}")
    
    def generate_platform_video(
        self,
        soul_id: str,
        platform: str,
        content_type: str = "post",
        model: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate platform-specific video content
        
        Args:
            soul_id: Soul ID
            platform: Target platform (TikTok, YouTube, etc.)
            content_type: Type of content (post, story, short)
            model: Model to use
            
        Returns:
            Generation result with video URL
        """
        soul = self.souls_manager.get_soul_by_id(soul_id)
        if not soul:
            return {'error': f'Soul {soul_id} not found'}
        
        # Platform-specific configurations
        platform_configs = {
            'TikTok': {
                'duration': 15,
                'aspect_ratio': '9:16',
                'prompt': 'engaging vertical video, trending style, dynamic'
            },
            'YouTube': {
                'duration': 30,
                'aspect_ratio': '16:9',
                'prompt': 'professional video content, high quality, engaging'
            },
            'Instagram': {
                'duration': 10,
                'aspect_ratio': '1:1',
                'prompt': 'aesthetic video, visually appealing, trendy'
            },
        }
        
        config = platform_configs.get(platform, platform_configs['TikTok'])
        
        # Build prompt
        prompt = self._build_platform_video_prompt(soul, platform, content_type)
        
        # Generate
        return self.generate_text_to_video(
            soul_id,
            prompt,
            duration=config['duration'],
            model=model
        )
    
    def _build_platform_video_prompt(self, soul, platform: str, content_type: str) -> str:
        """Build platform-specific video prompt"""
        base_prompt = f"{soul.name} creating {content_type} for {platform}"
        
        platform_prompts = {
            'TikTok': 'trending content, fast-paced, engaging transitions, viral potential',
            'YouTube': 'professional content, informative, high production value',
            'Instagram': 'aesthetic content, visually stunning, story-driven',
        }
        
        platform_prompt = platform_prompts.get(platform, 'engaging content')
        
        return f"{base_prompt}, {platform_prompt}"


if __name__ == '__main__':
    # Test the video generator
    generator = VideoGenerator()
    
    # Generate a video for Mac Nazarene
    result = generator.generate_text_to_video(
        'soul_001',
        'performing a sacred ritual in a digital temple',
        duration=5
    )
    print(f"Video generation result: {result}")
