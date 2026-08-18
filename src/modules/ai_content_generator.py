"""
AI Content Generator Module
Integrates with inference.sh CLI for autonomous soul content generation
"""

import json
import subprocess
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from .souls_manager import SoulsManager, Soul
from .utils import LoggingUtils, StringUtils


@dataclass
class ContentRequest:
    """Structure for content generation requests"""
    soul_id: str
    platform: str
    content_type: str  # 'post', 'bio', 'message', 'story', etc.
    context: Optional[str] = None
    tone: Optional[str] = None
    length: Optional[str] = 'medium'  # 'short', 'medium', 'long'
    target_audience: Optional[str] = None


@dataclass
class GeneratedContent:
    """Structure for generated content results"""
    soul_id: str
    platform: str
    content_type: str
    content: str
    model_used: str
    tokens_used: Optional[int] = None
    cost_estimate: Optional[float] = None
    generated_at: str = None
    metadata: Optional[Dict[str, Any]] = None

    def __post_init__(self):
        if self.generated_at is None:
            self.generated_at = datetime.now().isoformat()


class AIContentGenerator:
    """
    AI Content Generator using inference.sh CLI integration
    
    This class provides autonomous content generation capabilities for souls
    across multiple platforms using various AI models through the inference.sh CLI.
    """
    
    def __init__(self, souls_manager: SoulsManager, config_path: Optional[str] = None):
        """
        Initialize the AI content generator
        
        Args:
            souls_manager: SoulsManager instance for accessing soul data
            config_path: Optional path to AI configuration file
        """
        self.souls_manager = souls_manager
        self.logger = LoggingUtils.setup_logger(__name__)
        
        # Load configuration
        self.config = self._load_config(config_path)
        
        # Default models for different content types
        self.default_models = {
            'text_generation': 'google/gemini-2-5-flash',
            'image_generation': 'flux.1-dev',
            'avatar_generation': 'p-video-avatar',
            'video_generation': 'google/veo-3'
        }
        
        # Platform-specific content guidelines
        self.platform_guidelines = {
            'Twitter': {
                'max_length': 280,
                'style': 'concise, engaging, hashtag-heavy',
                'tone': 'casual, provocative'
            },
            'Instagram': {
                'max_length': 2200,
                'style': 'visual, aesthetic, emoji-rich',
                'tone': 'inspiring, lifestyle'
            },
            'Discord': {
                'max_length': 2000,
                'style': 'conversational, community-focused',
                'tone': 'casual, inclusive'
            },
            'FetLife': {
                'max_length': 1000,
                'style': 'intimate, authentic, community',
                'tone': 'respectful, exploratory'
            },
            'Reddit': {
                'max_length': 40000,
                'style': 'informative, discussion-provoking',
                'tone': 'analytical, engaging'
            }
        }
        
        self.logger.info("AI Content Generator initialized")
    
    def _load_config(self, config_path: Optional[str]) -> Dict[str, Any]:
        """Load AI configuration from file"""
        if config_path is None:
            # Try default config path
            config_path = Path(__file__).parent.parent.parent / 'config' / 'ai_config.json'
        
        config_file = Path(config_path)
        if config_file.exists():
            try:
                with open(config_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                self.logger.warning(f"Failed to load AI config: {e}, using defaults")
        
        return {
            'default_model': 'google/gemini-2-5-flash',
            'max_tokens': 1000,
            'temperature': 0.7,
            'enable_caching': True,
            'cost_limits': {
                'daily_limit': 10.0,
                'monthly_limit': 100.0
            }
        }
    
    def _run_infsh_command(self, app: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute inference.sh CLI command
        
        Args:
            app: The inference.sh app to run
            input_data: Input data for the app
            
        Returns:
            Parsed output from the command
        """
        try:
            # Create temporary input file
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
                json.dump(input_data, f)
                input_file = f.name
            
            # Run inference.sh command
            cmd = ['infsh', 'app', 'run', app, '--input', input_file]
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            # Clean up temp file
            Path(input_file).unlink()
            
            if result.returncode != 0:
                self.logger.error(f"infsh command failed: {result.stderr}")
                return {'error': result.stderr}
            
            # Parse output
            try:
                output = json.loads(result.stdout)
                return output
            except json.JSONDecodeError:
                # If output is not JSON, return as text
                return {'response': result.stdout}
                
        except subprocess.TimeoutExpired:
            self.logger.error("infsh command timed out")
            return {'error': 'Command timed out'}
        except Exception as e:
            self.logger.error(f"Failed to run infsh command: {e}")
            return {'error': str(e)}
    
    def _build_soul_prompt(self, soul: Soul, request: ContentRequest) -> str:
        """
        Build a contextual prompt for content generation based on soul attributes
        
        Args:
            soul: The soul object
            request: The content generation request
            
        Returns:
            Formatted prompt string
        """
        platform_guide = self.platform_guidelines.get(request.platform, {})
        
        prompt = f"""You are generating content for {soul.name}, a {soul.archetype}.

SOUL PROFILE:
- Name: {soul.name}
- Archetype: {soul.archetype}
- Bio: {soul.bio}
- Voice: {soul.voice}
- Personality: Known for saying things like: {', '.join(soul.hooks[:2])}
- Desires: {', '.join(soul.desires)}
- Sensory details: {soul.sensory}

PLATFORM: {request.platform}
- Style guide: {platform_guide.get('style', 'engaging')}
- Tone: {platform_guide.get('tone', 'authentic')}
- Max length: {platform_guide.get('max_length', 500)} characters

CONTENT TYPE: {request.content_type}
"""
        
        if request.context:
            prompt += f"\nCONTEXT: {request.context}"
        
        if request.tone:
            prompt += f"\nDESIRED TONE: {request.tone}"
        
        if request.target_audience:
            prompt += f"\nTARGET AUDIENCE: {request.target_audience}"
        
        prompt += f"""

Generate content that:
1. Matches {soul.name}'s voice and personality perfectly
2. Fits the {request.platform} platform's style and constraints
3. Incorporates their archetype ({soul.archetype}) naturally
4. Uses their characteristic phrases and hooks authentically
5. Resonates with their desires: {', '.join(soul.desires[:2])}

Keep the content {request.length} in length."""
        
        return prompt
    
    def generate_content(self, request: ContentRequest) -> GeneratedContent:
        """
        Generate content for a soul on a specific platform
        
        Args:
            request: ContentRequest with generation parameters
            
        Returns:
            GeneratedContent object with the generated content
        """
        soul = self.souls_manager.get_soul_by_id(request.soul_id)
        if not soul:
            raise ValueError(f"Soul with ID {request.soul_id} not found")
        
        # Verify soul has the requested platform
        if request.platform not in soul.platforms:
            self.logger.warning(f"Soul {soul.name} doesn't have platform {request.platform}")
        
        # Build prompt
        prompt = self._build_soul_prompt(soul, request)
        
        # Select model
        model = self.config.get('default_model', self.default_models['text_generation'])
        
        # Prepare input for inference.sh
        input_data = {
            'text': prompt,
            'max_tokens': self.config.get('max_tokens', 1000),
            'temperature': self.config.get('temperature', 0.7)
        }
        
        # Generate content
        self.logger.info(f"Generating {request.content_type} for {soul.name} on {request.platform}")
        output = self._run_infsh_command(model, input_data)
        
        if 'error' in output:
            raise Exception(f"Content generation failed: {output['error']}")
        
        # Extract generated content
        generated_text = output.get('response', '')
        
        # Apply platform-specific formatting
        generated_text = self._format_for_platform(generated_text, request.platform)
        
        # Create result object
        result = GeneratedContent(
            soul_id=request.soul_id,
            platform=request.platform,
            content_type=request.content_type,
            content=generated_text,
            model_used=model,
            tokens_used=output.get('usage', {}).get('total_tokens'),
            cost_estimate=self._estimate_cost(output.get('usage', {})),
            metadata={
                'soul_name': soul.name,
                'archetype': soul.archetype,
                'request_context': request.context
            }
        )
        
        self.logger.info(f"Successfully generated content for {soul.name}")
        return result
    
    def _format_for_platform(self, content: str, platform: str) -> str:
        """Apply platform-specific formatting to generated content"""
        platform_guide = self.platform_guidelines.get(platform, {})
        max_length = platform_guide.get('max_length', 1000)
        
        # Truncate if necessary
        if len(content) > max_length:
            content = StringUtils.truncate_text(content, max_length)
        
        # Platform-specific formatting
        if platform == 'Twitter':
            # Add line breaks for better readability
            content = content.replace('. ', '.\n')
        elif platform == 'Instagram':
            # Add emojis if not present
            if not any(char in content for char in ['✨', '🔮', '🌙']):
                content = '✨ ' + content + ' ✨'
        
        return content.strip()
    
    def _estimate_cost(self, usage: Dict[str, Any]) -> float:
        """Estimate cost based on token usage"""
        # Rough estimation based on typical model pricing
        input_tokens = usage.get('input_tokens', 0)
        output_tokens = usage.get('output_tokens', 0)
        
        # Typical pricing: $0.30/M input, $2.50/M output (for Gemini Flash)
        input_cost = (input_tokens / 1_000_000) * 0.30
        output_cost = (output_tokens / 1_000_000) * 2.50
        
        return input_cost + output_cost
    
    def generate_batch_content(self, requests: List[ContentRequest]) -> List[GeneratedContent]:
        """
        Generate content for multiple souls in batch
        
        Args:
            requests: List of ContentRequest objects
            
        Returns:
            List of GeneratedContent objects
        """
        results = []
        
        for request in requests:
            try:
                result = self.generate_content(request)
                results.append(result)
            except Exception as e:
                self.logger.error(f"Failed to generate content for request {request.soul_id}: {e}")
                # Continue with other requests even if one fails
                continue
        
        return results
    
    def generate_platform_campaign(self, platform: str, content_types: List[str]) -> List[GeneratedContent]:
        """
        Generate a campaign of content for all souls on a specific platform
        
        Args:
            platform: Platform to generate content for
            content_types: List of content types to generate
            
        Returns:
            List of GeneratedContent objects
        """
        souls = self.souls_manager.get_souls_by_platform(platform)
        requests = []
        
        for soul in souls:
            for content_type in content_types:
                request = ContentRequest(
                    soul_id=soul.id,
                    platform=platform,
                    content_type=content_type,
                    tone='authentic to soul voice'
                )
                requests.append(request)
        
        return self.generate_batch_content(requests)
    
    def generate_soul_story(self, soul_id: str, theme: str, length: str = 'medium') -> GeneratedContent:
        """
        Generate a narrative story for a soul based on their shadow practice and desires
        
        Args:
            soul_id: ID of the soul
            theme: Theme for the story
            length: Length of the story
            
        Returns:
            GeneratedContent with the story
        """
        soul = self.souls_manager.get_soul_by_id(soul_id)
        if not soul:
            raise ValueError(f"Soul with ID {soul_id} not found")
        
        request = ContentRequest(
            soul_id=soul_id,
            platform='general',
            content_type='story',
            context=f"A {theme} narrative exploring {soul.name}'s shadow practice: {soul.shadow_practice}",
            length=length,
            tone='mythic, transformative'
        )
        
        return self.generate_content(request)
    
    def generate_platform_crossposting(self, soul_id: str, base_content: str) -> Dict[str, str]:
        """
        Adapt content for multiple platforms while maintaining soul voice
        
        Args:
            soul_id: ID of the soul
            base_content: Base content to adapt
            
        Returns:
            Dictionary mapping platform names to adapted content
        """
        soul = self.souls_manager.get_soul_by_id(soul_id)
        if not soul:
            raise ValueError(f"Soul with ID {soul_id} not found")
        
        adapted_content = {}
        
        for platform in soul.platforms:
            request = ContentRequest(
                soul_id=soul_id,
                platform=platform,
                content_type='adaptation',
                context=f"Adapt this content for {platform}: {base_content}",
                tone='maintain soul voice'
            )
            
            try:
                result = self.generate_content(request)
                adapted_content[platform] = result.content
            except Exception as e:
                self.logger.error(f"Failed to adapt content for {platform}: {e}")
                adapted_content[platform] = base_content  # Fallback to original
        
        return adapted_content
    
    def get_generation_stats(self) -> Dict[str, Any]:
        """Get statistics about content generation"""
        return {
            'available_models': self.default_models,
            'supported_platforms': list(self.platform_guidelines.keys()),
            'config': self.config,
            'souls_count': len(self.souls_manager.get_all_souls())
        }