"""
Souls-Content Integration Module
Integrates soul entities with content generation and platform systems
"""

import random
import os
from typing import Dict, List, Optional, Any
from datetime import datetime
from dataclasses import dataclass
from enum import Enum
import requests

from .souls_manager import SoulsManager, Soul
from .utils import Configuration, StringUtils


# Content generation components for integration
class ContentStrategy:
    """Content generation strategies"""
    VIRAL = "viral"
    EDUCATIONAL = "educational"
    INFORMATIVE = "informative"
    EMOTIONAL = "emotional"
    PERSUASIVE = "persuasive"
    
    @classmethod
    def values(cls):
        return [cls.VIRAL, cls.EDUCATIONAL, cls.INFORMATIVE, cls.EMOTIONAL, cls.PERSUASIVE]


class AIContentAgent:
    """Real AI content agent using OpenAI API"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = Configuration.DEFAULT_AI_MODEL):
        """
        Initialize AI content agent
        
        Args:
            api_key: OpenAI API key (defaults to OPENAI_API_KEY env var)
            model: OpenAI model to use
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        self.api_url = "https://api.openai.com/v1/chat/completions"
        
        if not self.api_key:
            print("Warning: No OpenAI API key found. Using fallback content generation.")
    
    def generate_content(self, prompt: str, strategy: str, max_tokens: int) -> str:
        """
        Generate content based on prompt and strategy using OpenAI API
        
        Args:
            prompt: Content generation prompt
            strategy: Content strategy to use
            max_tokens: Maximum tokens to generate
            
        Returns:
            Generated content string
        """
        if not self.api_key:
            return self._generate_fallback_content(prompt, strategy)
        
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            system_prompt = self._get_system_prompt_for_strategy(strategy)
            
            payload = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": max_tokens,
                "temperature": Configuration.DEFAULT_TEMPERATURE
            }
            
            response = requests.post(self.api_url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            
            return content.strip()
            
        except Exception as e:
            print(f"Error generating content with AI: {e}")
            return self._generate_fallback_content(prompt, strategy)
    
    def _get_system_prompt_for_strategy(self, strategy: str) -> str:
        """Get system prompt based on content strategy"""
        strategy_prompts = {
            ContentStrategy.VIRAL: "You are a viral content creator. Create engaging, shareable content that captures attention and encourages interaction. Use hooks, emotional triggers, and trending topics.",
            ContentStrategy.EDUCATIONAL: "You are an educational content creator. Create informative, well-structured content that teaches concepts clearly and provides value to the reader.",
            ContentStrategy.INFORMATIVE: "You are an informative content creator. Create factual, objective content that presents information clearly and accurately.",
            ContentStrategy.EMOTIONAL: "You are an emotional storyteller. Create content that connects emotionally with readers, using personal stories and relatable experiences.",
            ContentStrategy.PERSUASIVE: "You are a persuasive copywriter. Create compelling content that motivates action and convinces readers of a particular viewpoint."
        }
        return strategy_prompts.get(strategy, "You are a helpful content creator.")
    
    def _generate_fallback_content(self, prompt: str, strategy: str) -> str:
        """Generate fallback content when AI generation fails"""
        return f"[Fallback Content - {strategy} strategy] {prompt[:100]}..."


class EnhancedVideoPipeline:
    """Mock video pipeline for integration"""
    pass


@dataclass
class ContentRequest:
    """Content generation request from a soul"""
    soul_id: str
    topic: str
    platform: str
    content_type: str  # 'social_post', 'video_script', 'article', 'story'
    target_audience: str
    custom_instructions: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class ContentResponse:
    """Generated content response"""
    soul_id: str
    soul_name: str
    platform: str
    content_type: str
    content: str
    hooks_used: List[str]
    voice_style: str
    timestamp: datetime
    metadata: Dict[str, Any]


class SoulsContentIntegration:
    """
    Integration between souls and content generation systems.
    
    This class connects soul entities with AI-powered content generation, enabling
    personalized content creation across multiple platforms while maintaining each
    soul's unique voice, personality, and characteristics.
    
    Attributes:
        souls_manager: SoulsManager instance for entity data
        content_agent: AIContentAgent instance for content generation
        content_history: List of generated content responses
    """
    
    def __init__(self, souls_manager: Optional[SoulsManager] = None, api_key: Optional[str] = None, model: str = "gpt-3.5-turbo"):
        """
        Initialize the souls-content integration
        
        Args:
            souls_manager: SoulsManager instance (creates default if not provided)
            api_key: OpenAI API key (defaults to OPENAI_API_KEY env var)
            model: OpenAI model to use for content generation
        """
        self.souls_manager = souls_manager or SoulsManager()
        self.content_agent = AIContentAgent(api_key=api_key, model=model)
        self.content_history = []
        
    def generate_content_for_soul(self, request: ContentRequest) -> ContentResponse:
        """
        Generate content tailored to a specific soul's personality
        
        Args:
            request: ContentRequest with soul and content details
            
        Returns:
            ContentResponse with generated content
        """
        # Get soul details
        soul = self.souls_manager.get_soul_by_id(request.soul_id)
        if not soul:
            raise ValueError(f"Soul with ID {request.soul_id} not found")
        
        # Validate platform compatibility
        if request.platform not in soul.platforms:
            raise ValueError(f"Soul {soul.name} does not use platform {request.platform}")
        
        # Select appropriate hooks based on platform and content type
        selected_hooks = self._select_hooks_for_content(soul, request.content_type, request.platform)
        
        # Generate content based on soul's voice and personality
        content = self._generate_soul_content(
            soul=soul,
            topic=request.topic,
            content_type=request.content_type,
            platform=request.platform,
            target_audience=request.target_audience,
            hooks=selected_hooks,
            custom_instructions=request.custom_instructions
        )
        
        # Create response
        response = ContentResponse(
            soul_id=soul.id,
            soul_name=soul.name,
            platform=request.platform,
            content_type=request.content_type,
            content=content,
            hooks_used=selected_hooks,
            voice_style=soul.voice,
            timestamp=datetime.now(),
            metadata={
                'archetype': soul.archetype,
                'rarity': soul.rarity,
                'custom_instructions': request.custom_instructions,
                'request_metadata': request.metadata or {}
            }
        )
        
        # Store in history
        self.content_history.append(response)
        
        return response
    
    def _select_hooks_for_content(self, soul: Soul, content_type: str, platform: str) -> List[str]:
        """Select appropriate hooks for the content type and platform"""
        # Select 1-2 hooks based on content type
        if content_type in ['social_post', 'short_form']:
            return [random.choice(soul.hooks)]
        elif content_type in ['video_script', 'long_form']:
            return random.sample(soul.hooks, min(2, len(soul.hooks)))
        else:
            return [soul.hooks[0]]
    
    def _generate_soul_content(
        self, 
        soul: Soul, 
        topic: str, 
        content_type: str, 
        platform: str,
        target_audience: str,
        hooks: List[str],
        custom_instructions: Optional[str] = None
    ) -> str:
        """Generate content tailored to the soul's personality"""
        
        # Build prompt based on soul characteristics
        prompt = f"""
        Generate {content_type} content for {soul.name} ({soul.archetype}).
        
        Soul Characteristics:
        - Voice: {soul.voice}
        - Bio: {soul.bio}
        - Desires: {', '.join(soul.desires)}
        - Key Hooks: {', '.join(hooks)}
        
        Content Requirements:
        - Topic: {topic}
        - Platform: {platform}
        - Target Audience: {target_audience}
        - Voice Style: {soul.voice}
        """
        
        if custom_instructions:
            prompt += f"\n- Custom Instructions: {custom_instructions}"
        
        # Generate content using AI agent
        try:
            generated_content = self.content_agent.generate_content(
                prompt=prompt,
                strategy=self._map_content_type_to_strategy(content_type),
                max_tokens=self._get_token_limit_for_platform(platform)
            )
            
            # Post-process to ensure soul's voice is maintained
            processed_content = self._apply_soul_voice_to_content(
                generated_content, 
                soul, 
                hooks
            )
            
            return processed_content
            
        except Exception as e:
            # Fallback to template-based generation
            return self._generate_fallback_content(
                soul, topic, content_type, platform, hooks
            )
    
    def _map_content_type_to_strategy(self, content_type: str) -> str:
        """Map content type to content strategy"""
        strategy_map = {
            'social_post': ContentStrategy.VIRAL,
            'video_script': ContentStrategy.EDUCATIONAL,
            'article': ContentStrategy.INFORMATIVE,
            'story': ContentStrategy.EMOTIONAL,
            'marketing': ContentStrategy.PERSUASIVE
        }
        return strategy_map.get(content_type, ContentStrategy.EDUCATIONAL)
    
    def _get_token_limit_for_platform(self, platform: str) -> int:
        """Get appropriate token limit for platform"""
        return Configuration.PLATFORM_TOKEN_LIMITS.get(platform, Configuration.FALLBACK_MAX_TOKENS)
    
    def _apply_soul_voice_to_content(
        self, 
        content: str, 
        soul: Soul, 
        hooks: List[str]
    ) -> str:
        """Apply soul's voice characteristics to generated content"""
        
        # Ensure hooks are naturally integrated
        for hook in hooks:
            if hook not in content:
                # Find natural insertion point
                sentences = content.split('.')
                if len(sentences) > 1:
                    insert_point = len(sentences) // 2
                    sentences.insert(insert_point, f" {hook}")
                    content = '. '.join(sentences)
        
        # Adjust tone based on voice description
        if 'aggressive' in soul.voice.lower():
            content = content.replace('please', '').replace('might', 'will')
        elif 'gentle' in soul.voice.lower():
            content = content.replace('must', 'may').replace('will', 'might')
        elif 'mysterious' in soul.voice.lower():
            content = content.replace('definitely', 'perhaps').replace('certainly', 'possibly')
        
        return content.strip()
    
    def _generate_fallback_content(
        self, 
        soul: Soul, 
        topic: str, 
        content_type: str, 
        platform: str,
        hooks: List[str]
    ) -> str:
        """Generate fallback content when AI generation fails"""
        
        hook = hooks[0] if hooks else soul.hooks[0]
        
        templates = {
            'social_post': f"{hook} When it comes to {topic}, I believe {random.choice(soul.desires).lower()} is essential. {soul.bio[:100]}... #Tiapmaatzu #{soul.archetype.replace(' ', '')}",
            'video_script': f"Scene: {soul.name} speaks about {topic}\n\n{soul.name}: {hook} Let me tell you about {topic}...\n\n{topic} represents everything I stand for: {', '.join(soul.desires)}. As {soul.archetype}, I've learned that...",
            'article': f"# {topic}: A {soul.archetype}'s Perspective\n\nBy {soul.name}\n\n{hook}\n\n{topic} is more than just a concept—it's a way of life. As someone who embodies {soul.archetype}, I've discovered that {', '.join(soul.desires)} are the keys to understanding..."
        }
        
        return templates.get(content_type, f"{hook} {topic} is important to me as {soul.archetype}.")
    
    def generate_campaign_for_platform(
        self, 
        platform: str, 
        topic: str, 
        content_types: List[str],
        target_audience: str
    ) -> List[ContentResponse]:
        """
        Generate a content campaign across multiple souls for a specific platform
        
        Args:
            platform: Target platform
            topic: Campaign topic
            content_types: Types of content to generate
            target_audience: Target audience description
            
        Returns:
            List of ContentResponse objects
        """
        # Get souls that use this platform
        platform_souls = self.souls_manager.get_souls_by_platform(platform)
        
        if not platform_souls:
            raise ValueError(f"No souls found for platform {platform}")
        
        campaign_responses = []
        
        for soul in platform_souls:
            for content_type in content_types:
                try:
                    request = ContentRequest(
                        soul_id=soul.id,
                        topic=topic,
                        platform=platform,
                        content_type=content_type,
                        target_audience=target_audience,
                        metadata={'campaign': True}
                    )
                    
                    response = self.generate_content_for_soul(request)
                    campaign_responses.append(response)
                    
                except Exception as e:
                    print(f"Failed to generate content for {soul.name}: {e}")
                    continue
        
        return campaign_responses
    
    def get_content_analytics(self) -> Dict[str, Any]:
        """Get analytics about generated content"""
        if not self.content_history:
            return {'status': 'no_data'}
        
        # Analyze content by soul
        soul_content_count = {}
        for response in self.content_history:
            soul_name = response.soul_name
            soul_content_count[soul_name] = soul_content_count.get(soul_name, 0) + 1
        
        # Analyze by platform
        platform_content_count = {}
        for response in self.content_history:
            platform = response.platform
            platform_content_count[platform] = platform_content_count.get(platform, 0) + 1
        
        # Analyze by content type
        type_content_count = {}
        for response in self.content_history:
            content_type = response.content_type
            type_content_count[content_type] = type_content_count.get(content_type, 0) + 1
        
        return {
            'total_content_generated': len(self.content_history),
            'content_by_soul': soul_content_count,
            'content_by_platform': platform_content_count,
            'content_by_type': type_content_count,
            'most_active_souls': sorted(soul_content_count.items(), key=lambda x: x[1], reverse=True)[:5],
            'most_used_platforms': sorted(platform_content_count.items(), key=lambda x: x[1], reverse=True)[:3]
        }
    
    def integrate_with_video_pipeline(
        self, 
        soul_id: str, 
        video_pipeline: EnhancedVideoPipeline,
        script_topic: str
    ) -> Dict[str, Any]:
        """
        Integrate soul personality with video pipeline for script generation
        
        Args:
            soul_id: ID of the soul to generate content for
            video_pipeline: EnhancedVideoPipeline instance
            script_topic: Topic for the video script
            
        Returns:
            Dictionary with video production plan
        """
        # Generate script content
        script_request = ContentRequest(
            soul_id=soul_id,
            topic=script_topic,
            platform='YouTube',
            content_type='video_script',
            target_audience='General audience interested in personal growth',
            metadata={'video_production': True}
        )
        
        script_response = self.generate_content_for_soul(script_request)
        
        # Create video production plan
        soul = self.souls_manager.get_soul_by_id(soul_id)
        
        production_plan = {
            'soul': {
                'id': soul.id,
                'name': soul.name,
                'archetype': soul.archetype,
                'voice': soul.voice
            },
            'script': script_response.content,
            'visual_direction': self._generate_visual_direction(soul),
            'audio_direction': {
                'voice_style': soul.voice,
                'background_music': self._suggest_music_for_soul(soul),
                'sound_effects': self._suggest_sound_effects(soul)
            },
            'production_notes': {
                'lighting': self._suggest_lighting(soul),
                'camera_angles': self._suggest_camera_angles(soul),
                'color_grading': self._suggest_color_grading(soul)
            }
        }
        
        return production_plan
    
    def _generate_visual_direction(self, soul: Soul) -> str:
        """Generate visual direction based on soul's sensory profile"""
        sensory_elements = soul.sensory.split(', ')
        return f"Visual style should incorporate: {', '.join(sensory_elements[:2])}. Atmosphere should reflect {soul.archetype} nature."
    
    def _suggest_music_for_soul(self, soul: Soul) -> str:
        """Suggest background music based on soul's personality"""
        if 'energetic' in soul.voice.lower():
            return "Upbeat, rhythmic music with strong beat"
        elif 'calm' in soul.voice.lower() or 'gentle' in soul.voice.lower():
            return "Soft, ambient music with flowing melodies"
        elif 'dark' in soul.voice.lower() or 'mysterious' in soul.voice.lower():
            return "Atmospheric, slightly mysterious background music"
        else:
            return "Neutral, supportive background music"
    
    def _suggest_sound_effects(self, soul: Soul) -> List[str]:
        """Suggest sound effects based on soul's sensory profile"""
        sensory_elements = soul.sensory.lower()
        effects = []
        
        if 'rain' in sensory_elements:
            effects.append("Gentle rain sounds")
        if 'fire' in sensory_elements or 'candle' in sensory_elements:
            effects.append("Crackling fire sounds")
        if 'wind' in sensory_elements:
            effects.append("Soft wind ambiance")
        if 'water' in sensory_elements or 'ocean' in sensory_elements:
            effects.append("Water flow or ocean waves")
        
        return effects if effects else ["Subtle ambient room tone"]
    
    def _suggest_lighting(self, soul: Soul) -> str:
        """Suggest lighting based on soul's archetype"""
        lighting_map = {
            'High Priest': 'Warm, candle-lit atmosphere with golden highlights',
            'Divine Mother': 'Soft, diffused lighting with gentle warmth',
            'Crypto Sorceress': 'Cool, blue-tinted lighting with dramatic shadows',
            'Community Healer': 'Natural, warm daylight feel',
            'Digital Guardian': 'Subtle blue LED accents on neutral background'
        }
        return lighting_map.get(soul.archetype, 'Balanced, professional lighting')
    
    def _suggest_camera_angles(self, soul: Soul) -> str:
        """Suggest camera angles based on soul's personality"""
        if 'authoritative' in soul.voice.lower() or 'commanding' in soul.voice.lower():
            return "Low angle shots to emphasize authority, mixed with close-ups for intimacy"
        elif 'mysterious' in soul.voice.lower():
            return "Dutch angles, shadow play, selective focus"
        else:
            return "Eye-level medium shots, with occasional close-ups for emphasis"
    
    def _suggest_color_grading(self, soul: Soul) -> str:
        """Suggest color grading based on soul's sensory profile"""
        if 'warm' in soul.sensory.lower():
            return "Warm color palette with golden and amber tones"
        elif 'cool' in soul.sensory.lower() or 'cold' in soul.sensory.lower():
            return "Cool color palette with blue and silver tones"
        elif 'dark' in soul.sensory.lower():
            return "High contrast, moody color grading with deep shadows"
        else:
            return "Natural, balanced color grading"