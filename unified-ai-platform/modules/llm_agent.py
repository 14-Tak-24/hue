"""
LLM Agent Module
Integrates with OpenRouter LLMs via inference.sh CLI for autonomous content creation
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


class LLMAgent:
    """
    LLM Agent using OpenRouter models via inference.sh CLI
    
    Provides autonomous content creation for the 28 souls of Tiapma'atzu including:
    - Social media content generation
    - Character dialogue creation
    - Narrative development
    - Platform-specific content adaptation
    """
    
    def __init__(self, souls_manager: Optional[SoulsManager] = None):
        """
        Initialize the LLM agent
        
        Args:
            souls_manager: SoulsManager instance for character data
        """
        self.logger = LoggingUtils.setup_logger(__name__)
        self.souls_manager = souls_manager or SoulsManager()
        
        # Output directories
        self.output_dir = Path(__file__).parent.parent / "content" / "text"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Model configurations
        self.models = {
            'claude_opus': 'openrouter/claude-opus-45',  # Complex reasoning
            'claude_sonnet': 'openrouter/claude-sonnet-45',  # Balanced
            'claude_haiku': 'openrouter/claude-haiku-45',  # Fast, economical
            'gemini_3_pro': 'openrouter/gemini-3-pro-preview',  # Google's latest
            'kimi_k2': 'openrouter/kimi-k2-thinking',  # Multi-step reasoning
            'glm_46': 'openrouter/glm-46',  # Open-source
            'any_model': 'openrouter/any-model',  # Auto-select
        }
        
        self.default_model = 'claude_sonnet'
        
        self.logger.info("LLM Agent initialized")
    
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
                timeout=120  # 2 minute timeout for LLM
            )
            
            if result.returncode != 0:
                self.logger.error(f"Belt command failed: {result.stderr}")
                return {'error': result.stderr}
            
            # Parse output
            try:
                output = json.loads(result.stdout)
                self.logger.info(f"LLM generation successful")
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
    
    def generate_social_media_post(
        self,
        soul_id: str,
        platform: str,
        topic: Optional[str] = None,
        model: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate social media post for a soul
        
        Args:
            soul_id: Soul ID
            platform: Target platform (Twitter, Instagram, AFF, etc.)
            topic: Post topic (default: auto-generated based on soul)
            model: Model to use
            
        Returns:
            Generation result with generated text
        """
        soul = self.souls_manager.get_soul_by_id(soul_id)
        if not soul:
            return {'error': f'Soul {soul_id} not found'}
        
        # Build system prompt
        system_prompt = self._build_soul_system_prompt(soul, platform)
        
        # Build user prompt
        if topic is None:
            topic = self._generate_topic(soul, platform)
        
        user_prompt = f"Write a {platform} post about: {topic}"
        
        # Select model
        model = model or self.default_model
        app_id = self.models.get(model, self.models[self.default_model])
        
        # Prepare input
        input_data = {
            'system': system_prompt,
            'prompt': user_prompt
        }
        
        # Generate
        result = self._run_belt_command(app_id, input_data)
        
        if 'error' not in result:
            self._save_generation_metadata(
                soul_id, 'social_post', result, model, platform, topic
            )
        
        return result
    
    def generate_character_dialogue(
        self,
        soul_id: str,
        context: str,
        other_soul_id: Optional[str] = None,
        model: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate character dialogue
        
        Args:
            soul_id: Soul ID (the character speaking)
            context: Dialogue context/situation
            other_soul_id: ID of other character in dialogue (optional)
            model: Model to use
            
        Returns:
            Generation result with dialogue
        """
        soul = self.souls_manager.get_soul_by_id(soul_id)
        if not soul:
            return {'error': f'Soul {soul_id} not found'}
        
        # Build system prompt
        system_prompt = self._build_soul_system_prompt(soul, 'dialogue')
        
        # Build user prompt
        if other_soul_id:
            other_soul = self.souls_manager.get_soul_by_id(other_soul_id)
            if other_soul:
                context = f"{context}. You are speaking with {other_soul.name}, the {other_soul.archetype}."
        
        user_prompt = f"Generate dialogue for this situation: {context}"
        
        # Select model
        model = model or self.default_model
        app_id = self.models.get(model, self.models[self.default_model])
        
        # Prepare input
        input_data = {
            'system': system_prompt,
            'prompt': user_prompt
        }
        
        # Generate
        result = self._run_belt_command(app_id, input_data)
        
        if 'error' not in result:
            self._save_generation_metadata(
                soul_id, 'dialogue', result, model, context, other_soul_id
            )
        
        return result
    
    def generate_narrative_content(
        self,
        soul_id: str,
        narrative_type: str,
        setting: Optional[str] = None,
        model: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate narrative content
        
        Args:
            soul_id: Soul ID
            narrative_type: Type of narrative (story, myth, prophecy, etc.)
            setting: Narrative setting (optional)
            model: Model to use
            
        Returns:
            Generation result with narrative content
        """
        soul = self.souls_manager.get_soul_by_id(soul_id)
        if not soul:
            return {'error': f'Soul {soul_id} not found'}
        
        # Build system prompt
        system_prompt = self._build_soul_system_prompt(soul, 'narrative')
        
        # Build user prompt
        if setting is None:
            setting = self._generate_setting(soul)
        
        user_prompt = f"Write a {narrative_type} set in: {setting}"
        
        # Select model
        model = model or 'claude_opus'  # Use best model for narratives
        app_id = self.models.get(model, self.models['claude_opus'])
        
        # Prepare input
        input_data = {
            'system': system_prompt,
            'prompt': user_prompt
        }
        
        # Generate
        result = self._run_belt_command(app_id, input_data)
        
        if 'error' not in result:
            self._save_generation_metadata(
                soul_id, 'narrative', result, model, narrative_type, setting
            )
        
        return result
    
    def generate_marketing_copy(
        self,
        soul_id: str,
        product_or_service: str,
        copy_type: str = "advertisement",
        model: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate marketing copy
        
        Args:
            soul_id: Soul ID
            product_or_service: Product or service to promote
            copy_type: Type of copy (advertisement, product description, etc.)
            model: Model to use
            
        Returns:
            Generation result with marketing copy
        """
        soul = self.souls_manager.get_soul_by_id(soul_id)
        if not soul:
            return {'error': f'Soul {soul_id} not found'}
        
        # Build system prompt
        system_prompt = f"""You are {soul.name}, the {soul.archetype}.
Your voice: {soul.voice}
Your bio: {soul.bio}
Your archetype influences: {soul.archetype}

Generate marketing copy that reflects your character while being persuasive and effective."""
        
        # Build user prompt
        user_prompt = f"Write {copy_type} for: {product_or_service}"
        
        # Select model
        model = model or self.default_model
        app_id = self.models.get(model, self.models[self.default_model])
        
        # Prepare input
        input_data = {
            'system': system_prompt,
            'prompt': user_prompt
        }
        
        # Generate
        result = self._run_belt_command(app_id, input_data)
        
        if 'error' not in result:
            self._save_generation_metadata(
                soul_id, 'marketing', result, model, product_or_service, copy_type
            )
        
        return result
    
    def _build_soul_system_prompt(self, soul, context_type: str) -> str:
        """Build system prompt based on soul characteristics"""
        base_prompt = f"""You are {soul.name}, the {soul.archetype}.

Character Profile:
- Bio: {soul.bio}
- Voice: {soul.voice}
- Sensory profile: {soul.sensory}
- Gender: {soul.gender}
- Rarity: {soul.rarity}
- Platforms: {', '.join(soul.platforms)}
- Desires: {', '.join(soul.desires[:3])}
- Kinks: {', '.join(soul.kinks[:3])}
- Tribute impact: {soul.tribute_impact}
- Shadow practice: {soul.shadow_practice}

Archetype Influence: {soul.archetype}"""

        # Add context-specific instructions
        context_instructions = {
            'Twitter': "Write concise, engaging tweets under 280 characters. Use relevant hashtags. Be impactful and shareable.",
            'Instagram': "Write visually descriptive captions. Use emojis appropriately. Include relevant hashtags. Be aesthetic and engaging.",
            'AFF': "Write professional, insightful content. Be articulate and valuable. Focus on industry relevance.",
            'dialogue': "Write natural, character-appropriate dialogue. Reflect the soul's voice and personality. Use their speech patterns.",
            'narrative': "Write compelling narrative content. Incorporate the soul's mythological elements. Create engaging storytelling.",
            'TikTok': "Write short, punchy scripts. Include visual cues. Be trendy and engaging.",
        }
        
        instruction = context_instructions.get(context_type, "Write authentic content that reflects the character's voice and personality.")
        
        return f"{base_prompt}\n\nInstructions: {instruction}"
    
    def _generate_topic(self, soul, platform: str) -> str:
        """Generate a topic based on soul and platform"""
        topics = {
            'High Priest': [
                'spiritual guidance in the digital age',
                'sacred rituals for modern times',
                'the intersection of technology and divinity',
                'wisdom from the temple of tomorrow'
            ],
            'Divine Mother': [
                'nurturing creativity in the digital realm',
                'healing through connection',
                'the power of maternal energy',
                'creating safe spaces online'
            ],
            'Seductive Muse': [
                'art as seduction',
                'the beauty of digital expression',
                'creative inspiration',
                'aesthetic exploration'
            ],
        }
        
        soul_topics = topics.get(soul.archetype, ['digital transformation', 'creative expression', 'community building'])
        import random
        return random.choice(soul_topics)
    
    def _generate_setting(self, soul) -> str:
        """Generate a narrative setting based on soul"""
        settings = {
            'High Priest': 'a neon-lit digital temple where code meets consciousness',
            'Divine Mother': 'a serene digital garden where data flows like water',
            'Seductive Muse': 'an avant-garde digital gallery where art comes alive',
            'Cosmic Mystic': 'the intersection of cyberspace and cosmic consciousness',
        }
        
        return settings.get(soul.archetype, 'a futuristic digital landscape')
    
    def _save_generation_metadata(
        self,
        soul_id: str,
        content_type: str,
        result: Dict[str, Any],
        model: str,
        context: str,
        detail: Optional[str]
    ):
        """Save generation metadata"""
        metadata = {
            'soul_id': soul_id,
            'content_type': content_type,
            'model': model,
            'context': context,
            'detail': detail,
            'timestamp': datetime.now().isoformat(),
            'result': result
        }
        
        # Save to logs
        log_file = self.output_dir / f"{soul_id}_{content_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(log_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        self.logger.info(f"Saved metadata to {log_file}")
    
    def batch_generate_posts(
        self,
        platform: str,
        soul_ids: Optional[List[str]] = None,
        model: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate social media posts for multiple souls
        
        Args:
            platform: Target platform
            soul_ids: List of soul IDs (default: all souls)
            model: Model to use
            
        Returns:
            Batch generation results
        """
        if soul_ids is None:
            soul_ids = [soul.id for soul in self.souls_manager.get_all_souls()]
        
        results = {}
        for soul_id in soul_ids:
            self.logger.info(f"Generating post for {soul_id} on {platform}")
            result = self.generate_social_media_post(soul_id, platform, model=model)
            results[soul_id] = result
        
        return {
            'platform': platform,
            'total': len(soul_ids),
            'successful': sum(1 for r in results.values() if 'error' not in r),
            'failed': sum(1 for r in results.values() if 'error' in r),
            'results': results
        }


if __name__ == '__main__':
    # Test the LLM agent
    agent = LLMAgent()
    
    # Generate a Twitter post for Mac Nazarene
    result = agent.generate_social_media_post('soul_001', 'Twitter')
    print(f"LLM generation result: {result}")
