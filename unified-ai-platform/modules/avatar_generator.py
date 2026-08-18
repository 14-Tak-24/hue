"""
AI Avatar Generator Module
Generates talking head avatar videos using P-Video-Avatar, OmniHuman, and Fabric via inference.sh CLI
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


class AvatarGenerator:
    """
    AI Avatar Generator using inference.sh CLI
    
    Generates talking head avatar videos for the 28 souls of Tiapma'atzu including:
    - Text-to-speech avatars (P-Video-Avatar with built-in TTS)
    - Audio-driven avatars (OmniHuman, Fabric)
    - UGC-style content generation
    """
    
    def __init__(self, souls_manager: Optional[SoulsManager] = None):
        """
        Initialize the avatar generator
        
        Args:
            souls_manager: SoulsManager instance for character data
        """
        self.logger = LoggingUtils.setup_logger(__name__)
        self.souls_manager = souls_manager or SoulsManager()
        
        # Output directories
        self.output_dir = Path(__file__).parent.parent / "content" / "avatars"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Model configurations
        self.models = {
            'p_video_avatar': 'pruna/p-video-avatar',  # Recommended: fastest, cheapest, built-in TTS
            'omnihuman_1_5': 'bytedance/omnihuman-1-5',  # Multi-character
            'fabric_1_0': 'falai/fabric-1-0',  # Image talks with lipsync
            'pixverse_lipsync': 'falai/pixverse-lipsync',  # Realistic lipsync
        }
        
        # Voice configurations for P-Video-Avatar
        self.voices = {
            'male': ['Puck (Male)', 'Zephyr (Male)', 'Balthazar (Male)'],
            'female': ['Zephyr (Female)', 'Aoede (Female)', 'Nova (Female)'],
        }
        
        self.default_model = 'p_video_avatar'
        
        self.logger.info("Avatar Generator initialized")
    
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
                timeout=600  # 10 minute timeout for avatar generation
            )
            
            if result.returncode != 0:
                self.logger.error(f"Belt command failed: {result.stderr}")
                return {'error': result.stderr}
            
            # Parse output
            try:
                output = json.loads(result.stdout)
                self.logger.info(f"Avatar generation successful")
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
    
    def generate_avatar_with_tts(
        self,
        soul_id: str,
        script: str,
        voice: Optional[str] = None,
        voice_prompt: Optional[str] = None,
        video_prompt: Optional[str] = None,
        resolution: str = "720p",
        model: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate avatar video with built-in text-to-speech (P-Video-Avatar)
        
        Args:
            soul_id: Soul ID
            script: Script for the avatar to speak
            voice: Voice selection (default: based on soul gender)
            voice_prompt: Voice style description
            video_prompt: Video style description
            resolution: Video resolution (720p, 1080p)
            model: Model to use (default: p_video_avatar)
            
        Returns:
            Generation result with video URL
        """
        soul = self.souls_manager.get_soul_by_id(soul_id)
        if not soul:
            return {'error': f'Soul {soul_id} not found'}
        
        # Get portrait image (assuming it exists)
        portrait_url = self._get_soul_portrait(soul_id)
        if not portrait_url:
            return {'error': f'No portrait found for {soul_id}. Generate portrait first.'}
        
        # Select voice based on soul gender
        if voice is None:
            voice_category = 'female' if soul.gender == 'F' else 'male'
            voice = self.voices[voice_category][0]
        
        # Build voice prompt based on archetype
        if voice_prompt is None:
            voice_prompt = self._build_voice_prompt(soul)
        
        # Build video prompt based on archetype
        if video_prompt is None:
            video_prompt = self._build_video_prompt(soul)
        
        # Use P-Video-Avatar (recommended)
        model = model or self.default_model
        app_id = self.models.get(model, self.models[self.default_model])
        
        # Prepare input
        input_data = {
            'image': portrait_url,
            'voice_script': script,
            'voice': voice,
            'voice_language': 'English (US)',
            'resolution': resolution
        }
        
        # Add optional prompts
        if voice_prompt:
            input_data['voice_prompt'] = voice_prompt
        if video_prompt:
            input_data['video_prompt'] = video_prompt
        
        # Generate
        result = self._run_belt_command(app_id, input_data)
        
        if 'error' not in result:
            self._save_generation_metadata(
                soul_id, 'avatar_tts', result, model, script, voice
            )
        
        return result
    
    def generate_avatar_with_audio(
        self,
        soul_id: str,
        audio_url: str,
        model: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate avatar video with provided audio (OmniHuman, Fabric)
        
        Args:
            soul_id: Soul ID
            audio_url: URL of audio file
            model: Model to use (default: omnihuman_1_5)
            
        Returns:
            Generation result with video URL
        """
        soul = self.souls_manager.get_soul_by_id(soul_id)
        if not soul:
            return {'error': f'Soul {soul_id} not found'}
        
        # Get portrait image
        portrait_url = self._get_soul_portrait(soul_id)
        if not portrait_url:
            return {'error': f'No portrait found for {soul_id}. Generate portrait first.'}
        
        # Use OmniHuman for audio-driven avatars
        model = model or 'omnihuman_1_5'
        app_id = self.models.get(model, self.models['omnihuman_1_5'])
        
        # Prepare input
        input_data = {
            'image_url': portrait_url,
            'audio_url': audio_url
        }
        
        # Generate
        result = self._run_belt_command(app_id, input_data)
        
        if 'error' not in result:
            self._save_generation_metadata(
                soul_id, 'avatar_audio', result, model, audio_url, None
            )
        
        return result
    
    def generate_ugc_avatar(
        self,
        soul_id: str,
        script: str,
        style: str = "casual",
        resolution: str = "1080p"
    ) -> Dict[str, Any]:
        """
        Generate UGC-style avatar video
        
        Args:
            soul_id: Soul ID
            script: UGC-style script
            style: UGC style (casual, excited, authentic)
            resolution: Video resolution
            
        Returns:
            Generation result with video URL
        """
        soul = self.souls_manager.get_soul_by_id(soul_id)
        if not soul:
            return {'error': f'Soul {soul_id} not found'}
        
        # Get portrait image
        portrait_url = self._get_soul_portrait(soul_id)
        if not portrait_url:
            return {'error': f'No portrait found for {soul_id}. Generate portrait first.'}
        
        # Select voice
        voice_category = 'female' if soul.gender == 'F' else 'male'
        voice = self.voices[voice_category][0]
        
        # Build UGC-specific prompts
        voice_prompt = f"{style}, authentic, like talking to a friend, natural tone"
        video_prompt = f"Person talking casually to camera, natural gestures, {style} setting"
        
        # Generate
        return self.generate_avatar_with_tts(
            soul_id,
            script,
            voice=voice,
            voice_prompt=voice_prompt,
            video_prompt=video_prompt,
            resolution=resolution
        )
    
    def _get_soul_portrait(self, soul_id: str) -> Optional[str]:
        """Get portrait URL for a soul"""
        # In a real implementation, this would check the database or file system
        # For now, return a placeholder
        portrait_file = Path(__file__).parent.parent / "content" / "images" / f"{soul_id}_portrait_latest.json"
        
        if portrait_file.exists():
            with open(portrait_file, 'r') as f:
                data = json.load(f)
                return data.get('result', {}).get('image_url')
        
        return None
    
    def _build_voice_prompt(self, soul) -> str:
        """Build voice prompt based on soul archetype"""
        archetype_voice_prompts = {
            'High Priest': 'authoritative, mystical, commanding yet benevolent',
            'Divine Mother': 'warm, nurturing, gentle, maternal',
            'Seductive Muse': 'alluring, sensual, artistic, captivating',
            'Cosmic Mystic': 'ethereal, mysterious, otherworldly',
            'Revolutionary Warrior': 'passionate, intense, powerful, motivating',
        }
        
        return archetype_voice_prompts.get(soul.archetype, 'natural, authentic')
    
    def _build_video_prompt(self, soul) -> str:
        """Build video prompt based on soul archetype"""
        archetype_video_prompts = {
            'High Priest': 'person speaking in a sacred temple, divine lighting, ceremonial atmosphere',
            'Divine Mother': 'person speaking in a nurturing environment, warm lighting, peaceful atmosphere',
            'Seductive Muse': 'person speaking in an artistic setting, dramatic lighting, creative atmosphere',
            'Cosmic Mystic': 'person speaking with cosmic energy, ethereal lighting, mystical atmosphere',
            'Revolutionary Warrior': 'person speaking with determination, dynamic lighting, powerful atmosphere',
        }
        
        return archetype_video_prompts.get(soul.archetype, 'person speaking professionally')
    
    def _save_generation_metadata(
        self,
        soul_id: str,
        content_type: str,
        result: Dict[str, Any],
        model: str,
        script_or_audio: str,
        voice: Optional[str]
    ):
        """Save generation metadata"""
        metadata = {
            'soul_id': soul_id,
            'content_type': content_type,
            'model': model,
            'script_or_audio': script_or_audio,
            'voice': voice,
            'timestamp': datetime.now().isoformat(),
            'result': result
        }
        
        # Save to logs
        log_file = self.output_dir / f"{soul_id}_{content_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(log_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        self.logger.info(f"Saved metadata to {log_file}")
    
    def generate_welcome_video(
        self,
        soul_id: str,
        custom_script: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate a welcome/introduction video for a soul
        
        Args:
            soul_id: Soul ID
            custom_script: Custom welcome script (default: auto-generated)
            
        Returns:
            Generation result with video URL
        """
        soul = self.souls_manager.get_soul_by_id(soul_id)
        if not soul:
            return {'error': f'Soul {soul_id} not found'}
        
        # Generate default welcome script if not provided
        if custom_script is None:
            custom_script = self._generate_welcome_script(soul)
        
        return self.generate_avatar_with_tts(
            soul_id,
            custom_script,
            resolution="1080p"
        )
    
    def _generate_welcome_script(self, soul) -> str:
        """Generate a welcome script for a soul"""
        return f"Welcome, I am {soul.name}, the {soul.archetype}. {soul.bio[:100]}... I am here to guide you through the mysteries of Tiapma'atzu."


if __name__ == '__main__':
    # Test the avatar generator
    generator = AvatarGenerator()
    
    # Generate a welcome video for Mac Nazarene
    result = generator.generate_welcome_video('soul_001')
    print(f"Avatar generation result: {result}")
