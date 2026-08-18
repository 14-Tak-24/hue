"""
AI Image Generator Module
Generates images for souls using FLUX models via inference.sh CLI
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


class ImageGenerator:
    """
    AI Image Generator using FLUX models via inference.sh CLI
    
    Generates character portraits, scene imagery, and visual content
    for the 28 souls of Tiapma'atzu.
    """
    
    def __init__(self, souls_manager: Optional[SoulsManager] = None):
        """
        Initialize the image generator
        
        Args:
            souls_manager: SoulsManager instance for character data
        """
        self.logger = LoggingUtils.setup_logger(__name__)
        self.souls_manager = souls_manager or SoulsManager()
        
        # Output directories
        self.output_dir = Path(__file__).parent.parent / "content" / "images"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Model configurations
        self.models = {
            'flux_dev_lora': 'falai/flux-dev-lora',  # Highest quality
            'flux_2_klein': 'falai/flux-2-klein-lora',  # Fastest
            'flux_dev_pruna': 'pruna/flux-dev',  # Optimized
            'flux_klein_4b': 'pruna/flux-klein-4b',  # Ultra-cheap
        }
        
        self.default_model = 'flux_dev_lora'
        
        self.logger.info("Image Generator initialized")
    
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
                timeout=300  # 5 minute timeout
            )
            
            if result.returncode != 0:
                self.logger.error(f"Belt command failed: {result.stderr}")
                return {'error': result.stderr}
            
            # Parse output
            try:
                output = json.loads(result.stdout)
                self.logger.info(f"Image generation successful")
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
    
    def generate_soul_portrait(
        self,
        soul_id: str,
        style: str = "photorealistic",
        aspect_ratio: str = "1:1",
        model: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate a portrait for a specific soul
        
        Args:
            soul_id: Soul ID
            style: Image style (photorealistic, artistic, digital, etc.)
            aspect_ratio: Image aspect ratio (1:1, 9:16, 16:9)
            model: Model to use (default: flux_dev_lora)
            
        Returns:
            Generation result with image URL
        """
        soul = self.souls_manager.get_soul_by_id(soul_id)
        if not soul:
            return {'error': f'Soul {soul_id} not found'}
        
        # Build prompt based on soul characteristics
        prompt = self._build_portrait_prompt(soul, style)
        
        # Select model
        model = model or self.default_model
        app_id = self.models.get(model, self.models[self.default_model])
        
        # Prepare input
        input_data = {
            'prompt': prompt,
            'aspect_ratio': aspect_ratio,
            'num_inference_steps': 28,
            'guidance_scale': 7.5
        }
        
        # Generate
        result = self._run_belt_command(app_id, input_data)
        
        if 'error' not in result:
            # Save metadata
            self._save_generation_metadata(
                soul_id, 'portrait', result, model, style, aspect_ratio
            )
        
        return result
    
    def generate_scene_image(
        self,
        soul_id: str,
        scene_description: str,
        style: str = "cinematic",
        aspect_ratio: str = "16:9",
        model: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate a scene image for a soul
        
        Args:
            soul_id: Soul ID
            scene_description: Description of the scene
            style: Image style
            aspect_ratio: Image aspect ratio
            model: Model to use
            
        Returns:
            Generation result with image URL
        """
        soul = self.souls_manager.get_soul_by_id(soul_id)
        if not soul:
            return {'error': f'Soul {soul_id} not found'}
        
        # Build scene prompt
        prompt = self._build_scene_prompt(soul, scene_description, style)
        
        # Select model
        model = model or self.default_model
        app_id = self.models.get(model, self.models[self.default_model])
        
        # Prepare input
        input_data = {
            'prompt': prompt,
            'aspect_ratio': aspect_ratio,
            'num_inference_steps': 28,
            'guidance_scale': 7.5
        }
        
        # Generate
        result = self._run_belt_command(app_id, input_data)
        
        if 'error' not in result:
            self._save_generation_metadata(
                soul_id, 'scene', result, model, style, aspect_ratio
            )
        
        return result
    
    def generate_platform_content(
        self,
        soul_id: str,
        platform: str,
        content_type: str = "post",
        model: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate platform-specific content image
        
        Args:
            soul_id: Soul ID
            platform: Target platform (Twitter, Instagram, etc.)
            content_type: Type of content (post, story, banner)
            model: Model to use
            
        Returns:
            Generation result with image URL
        """
        soul = self.souls_manager.get_soul_by_id(soul_id)
        if not soul:
            return {'error': f'Soul {soul_id} not found'}
        
        # Platform-specific settings
        platform_configs = {
            'Twitter': {'aspect_ratio': '16:9', 'style': 'digital'},
            'Instagram': {'aspect_ratio': '1:1', 'style': 'aesthetic'},
            'TikTok': {'aspect_ratio': '9:16', 'style': 'trending'},
            'YouTube': {'aspect_ratio': '16:9', 'style': 'professional'},
            'AFF': {'aspect_ratio': '1:1', 'style': 'corporate'},
        }
        
        config = platform_configs.get(platform, platform_configs['Twitter'])
        
        # Build prompt
        prompt = self._build_platform_prompt(soul, platform, content_type, config['style'])
        
        # Select model
        model = model or self.default_model
        app_id = self.models.get(model, self.models[self.default_model])
        
        # Prepare input
        input_data = {
            'prompt': prompt,
            'aspect_ratio': config['aspect_ratio'],
            'num_inference_steps': 28,
            'guidance_scale': 7.5
        }
        
        # Generate
        result = self._run_belt_command(app_id, input_data)
        
        if 'error' not in result:
            self._save_generation_metadata(
                soul_id, f'{platform}_{content_type}', result, model,
                config['style'], config['aspect_ratio']
            )
        
        return result
    
    def _build_portrait_prompt(self, soul, style: str) -> str:
        """Build portrait prompt based on soul characteristics"""
        base_prompt = f"professional portrait of {soul.name}"
        
        # Add archetype
        archetype_prompts = {
            'High Priest': 'in ceremonial robes, sacred symbols, divine aura',
            'Divine Mother': 'with maternal warmth, nurturing presence, soft lighting',
            'Seductive Muse': 'with alluring gaze, artistic atmosphere, sensual elegance',
            'Cosmic Mystic': 'with cosmic energy, celestial background, mystical symbols',
            'Revolutionary Warrior': 'in battle-ready stance, fierce determination, dynamic pose',
        }
        
        archetype_prompt = archetype_prompts.get(soul.archetype, 'unique character presence')
        
        # Add style
        style_prompts = {
            'photorealistic': 'photorealistic, studio lighting, high detail, 8K',
            'artistic': 'artistic, oil painting style, rich colors, dramatic lighting',
            'digital': 'digital art, cyberpunk aesthetic, neon accents, futuristic',
            'cinematic': 'cinematic, film grain, dramatic shadows, movie still',
        }
        
        style_prompt = style_prompts.get(style, 'high quality, detailed')
        
        return f"{base_prompt}, {archetype_prompt}, {style_prompt}, looking at camera"
    
    def _build_scene_prompt(self, soul, scene_description: str, style: str) -> str:
        """Build scene prompt based on soul and description"""
        base_prompt = f"{soul.name} in {scene_description}"
        
        # Add soul's sensory profile
        if hasattr(soul, 'sensory'):
            base_prompt += f", {soul.sensory}"
        
        # Add style
        style_prompts = {
            'cinematic': 'cinematic lighting, dramatic composition, movie still',
            'artistic': 'artistic interpretation, painterly style, rich colors',
            'digital': 'digital art, futuristic aesthetic, clean lines',
            'mystical': 'mystical atmosphere, ethereal lighting, magical elements',
        }
        
        style_prompt = style_prompts.get(style, 'high quality, detailed')
        
        return f"{base_prompt}, {style_prompt}"
    
    def _build_platform_prompt(self, soul, platform: str, content_type: str, style: str) -> str:
        """Build platform-specific content prompt"""
        base_prompt = f"{soul.name} creating content for {platform}"
        
        # Add content type
        type_prompts = {
            'post': 'in a engaging pose, social media ready',
            'story': 'in a dynamic vertical composition, storytelling moment',
            'banner': 'in a wide composition, professional presentation',
        }
        
        type_prompt = type_prompts.get(content_type, 'engaging content')
        
        # Add platform style
        platform_styles = {
            'Twitter': 'minimalist, clean, impactful',
            'Instagram': 'aesthetic, visually appealing, trendy',
            'TikTok': 'dynamic, trendy, vertical focus',
            'YouTube': 'professional, high production value',
            'AFF': 'professional, corporate, trustworthy',
        }
        
        platform_style = platform_styles.get(platform, 'engaging')
        
        return f"{base_prompt}, {type_prompt}, {platform_style}, {style}"
    
    def _save_generation_metadata(
        self,
        soul_id: str,
        content_type: str,
        result: Dict[str, Any],
        model: str,
        style: str,
        aspect_ratio: str
    ):
        """Save generation metadata"""
        metadata = {
            'soul_id': soul_id,
            'content_type': content_type,
            'model': model,
            'style': style,
            'aspect_ratio': aspect_ratio,
            'timestamp': datetime.now().isoformat(),
            'result': result
        }
        
        # Save to logs
        log_file = self.output_dir / f"{soul_id}_{content_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(log_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        self.logger.info(f"Saved metadata to {log_file}")
    
    def batch_generate_portraits(
        self,
        soul_ids: Optional[List[str]] = None,
        style: str = "photorealistic",
        model: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate portraits for multiple souls
        
        Args:
            soul_ids: List of soul IDs (default: all souls)
            style: Image style
            model: Model to use
            
        Returns:
            Batch generation results
        """
        if soul_ids is None:
            soul_ids = [soul.id for soul in self.souls_manager.get_all_souls()]
        
        results = {}
        for soul_id in soul_ids:
            self.logger.info(f"Generating portrait for {soul_id}")
            result = self.generate_soul_portrait(soul_id, style, model=model)
            results[soul_id] = result
        
        return {
            'total': len(soul_ids),
            'successful': sum(1 for r in results.values() if 'error' not in r),
            'failed': sum(1 for r in results.values() if 'error' in r),
            'results': results
        }


if __name__ == '__main__':
    # Test the image generator
    generator = ImageGenerator()
    
    # Generate a portrait for Mac Nazarene
    result = generator.generate_soul_portrait('soul_001', style='photorealistic')
    print(f"Portrait generation result: {result}")
