"""
OpenRouter LLM Integration Module
Provides access to multiple LLMs via OpenRouter for autonomous soul content creation
"""

import json
import subprocess
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from pathlib import Path

from .souls_manager import SoulsManager, Soul
from .utils import LoggingUtils


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


class ModelProvider(Enum):
    """Available LLM providers via OpenRouter"""
    ANTHROPIC = "anthropic"
    OPENAI = "openai"
    GOOGLE = "google"
    META = "meta"
    MISTRAL = "mistral"
    COHERE = "cohere"


class ModelCapability(Enum):
    """Model capabilities"""
    TEXT_GENERATION = "text_generation"
    VISION = "vision"
    TOOL_USE = "tool_use"
    EXTENDED_THINKING = "extended_thinking"
    CODE_GENERATION = "code_generation"


@dataclass
class ModelConfig:
    """Configuration for a specific model"""
    model_id: str
    provider: ModelProvider
    capabilities: List[ModelCapability]
    context_window: int
    max_output: int
    pricing_per_million: Dict[str, float]  # input, output
    best_for: List[str]  # use cases


# Available models through OpenRouter/inference.sh
AVAILABLE_MODELS = {
    'claude-sonnet-4-5': ModelConfig(
        model_id='anthropic/claude-sonnet-4-5',
        provider=ModelProvider.ANTHROPIC,
        capabilities=[ModelCapability.TEXT_GENERATION, ModelCapability.VISION, 
                     ModelCapability.TOOL_USE, ModelCapability.EXTENDED_THINKING],
        context_window=200000,
        max_output=64000,
        pricing_per_million={'input': 3.00, 'output': 15.00},
        best_for=['complex_reasoning', 'creative_writing', 'analysis', 'soul_personas']
    ),
    'claude-opus-4-7': ModelConfig(
        model_id='anthropic/claude-opus-4-7',
        provider=ModelProvider.ANTHROPIC,
        capabilities=[ModelCapability.TEXT_GENERATION, ModelCapability.VISION,
                     ModelCapability.TOOL_USE, ModelCapability.EXTENDED_THINKING],
        context_window=1000000,
        max_output=128000,
        pricing_per_million={'input': 15.00, 'output': 75.00},
        best_for=['highest_quality', 'complex_tasks', 'extended_context']
    ),
    'claude-sonnet-46': ModelConfig(
        model_id='openrouter/claude-sonnet-46',
        provider=ModelProvider.ANTHROPIC,
        capabilities=[ModelCapability.TEXT_GENERATION, ModelCapability.VISION,
                     ModelCapability.TOOL_USE],
        context_window=200000,
        max_output=64000,
        pricing_per_million={'input': 3.00, 'output': 15.00},
        best_for=['cost_effective', 'general_purpose', 'soul_content']
    ),
    'gemini-2-5-flash': ModelConfig(
        model_id='google/gemini-2-5-flash',
        provider=ModelProvider.GOOGLE,
        capabilities=[ModelCapability.TEXT_GENERATION, ModelCapability.VISION],
        context_window=1000000,
        max_output=64000,
        pricing_per_million={'input': 0.30, 'output': 2.50},
        best_for=['fast_generation', 'cost_efficient', 'bulk_content']
    ),
    'gemini-2-5-flash-lite': ModelConfig(
        model_id='google/gemini-2-5-flash-lite',
        provider=ModelProvider.GOOGLE,
        capabilities=[ModelCapability.TEXT_GENERATION, ModelCapability.VISION],
        context_window=1000000,
        max_output=64000,
        pricing_per_million={'input': 0.075, 'output': 0.30},
        best_for=['free_tier', 'fast_generation', 'cost_efficient']
    ),
    'gemini-2-5-pro': ModelConfig(
        model_id='google/gemini-2-5-pro',
        provider=ModelProvider.GOOGLE,
        capabilities=[ModelCapability.TEXT_GENERATION, ModelCapability.VISION,
                     ModelCapability.EXTENDED_THINKING],
        context_window=1000000,
        max_output=64000,
        pricing_per_million={'input': 1.25, 'output': 10.00},
        best_for=['balanced_performance', 'multimodal', 'reasoning']
    ),
}


class OpenRouterIntegration:
    """
    OpenRouter LLM Integration for autonomous soul content creation
    
    This class provides access to multiple LLMs through OpenRouter via inference.sh CLI,
    enabling intelligent content generation with model selection based on task requirements.
    """
    
    def __init__(self, souls_manager: SoulsManager, config_path: Optional[str] = None):
        """
        Initialize OpenRouter integration
        
        Args:
            souls_manager: SoulsManager instance for accessing soul data
            config_path: Optional path to OpenRouter configuration file
        """
        self.souls_manager = souls_manager
        self.logger = LoggingUtils.setup_logger(__name__)
        
        # Load configuration
        self.config = self._load_config(config_path)
        
        # Set default model
        self.default_model = self.config.get('default_model', 'gemini-2-5-flash-lite')
        
        # Model selection strategy
        self.model_strategy = self.config.get('model_strategy', 'balanced')
        
        # Usage tracking
        self.usage_stats = {
            'total_requests': 0,
            'total_tokens': 0,
            'total_cost': 0.0,
            'model_usage': {}
        }
        
        self.logger.info(f"OpenRouter Integration initialized with default model: {self.default_model}")
    
    def _load_config(self, config_path: Optional[str]) -> Dict[str, Any]:
        """Load OpenRouter configuration from file"""
        if config_path is None:
            from pathlib import Path
            config_path = Path(__file__).parent.parent.parent / 'config' / 'openrouter_config.json'
        
        config_file = Path(config_path)
        if config_file.exists():
            try:
                with open(config_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                self.logger.warning(f"Failed to load OpenRouter config: {e}, using defaults")
        
        return {
            'default_model': 'gemini-2-5-flash-lite',
            'model_strategy': 'cost',  # 'cost', 'quality', 'balanced'
            'enable_fallback': True,
            'fallback_model': 'gemini-2-5-flash',
            'cost_limits': {
                'daily_limit': 50.0,
                'monthly_limit': 200.0
            },
            'cache_enabled': True,
            'simulation_mode': True  # Enable simulation mode when API is unavailable
        }
    
    def select_model_for_task(self, task_type: str, complexity: str = 'medium') -> str:
        """
        Select the best model for a specific task
        
        Args:
            task_type: Type of task (e.g., 'creative_writing', 'analysis', 'bulk_content')
            complexity: Complexity level ('low', 'medium', 'high')
            
        Returns:
            Model ID to use
        """
        if self.model_strategy == 'cost':
            # Always use cheapest model
            return 'gemini-2-5-flash-lite'
        
        if self.model_strategy == 'quality':
            # Always use best model
            return 'claude-opus-4-7'
        
        # Balanced strategy - select based on task
        task_model_mapping = {
            'creative_writing': {
                'low': 'gemini-2-5-flash-lite',
                'medium': 'gemini-2-5-flash',
                'high': 'gemini-2-5-pro'
            },
            'soul_persona': {
                'low': 'gemini-2-5-flash',
                'medium': 'gemini-2-5-pro',
                'high': 'gemini-2-5-pro'
            },
            'analysis': {
                'low': 'gemini-2-5-flash-lite',
                'medium': 'gemini-2-5-flash',
                'high': 'gemini-2-5-pro'
            },
            'bulk_content': {
                'low': 'gemini-2-5-flash-lite',
                'medium': 'gemini-2-5-flash-lite',
                'high': 'gemini-2-5-flash'
            },
            'code_generation': {
                'low': 'gemini-2-5-flash',
                'medium': 'gemini-2-5-pro',
                'high': 'gemini-2-5-pro'
            }
        }
        
        return task_model_mapping.get(task_type, {}).get(complexity, self.default_model)
    
    def _run_openrouter_command(self, model: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute OpenRouter command via inference.sh CLI
        
        Args:
            model: The model to use
            input_data: Input data for the model
            
        Returns:
            Parsed output from the command
        """
        # Check if simulation mode is enabled
        if self.config.get('simulation_mode', False):
            self.logger.info(f"Simulation mode: generating mock response for {model}")
            return self._generate_simulation_response(input_data, model)
        
        try:
            import tempfile
            
            # Create temporary input file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
                json.dump(input_data, f)
                input_file = f.name
            
            # Run inference.sh command
            cmd = ['infsh', 'app', 'run', model, '--input', input_file]
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=120  # Longer timeout for complex models
            )
            
            # Clean up temp file
            Path(input_file).unlink()
            
            if result.returncode != 0:
                self.logger.error(f"OpenRouter command failed: {result.stderr}")
                
                # Try fallback if enabled
                if self.config.get('enable_fallback', True):
                    fallback_model = self.config.get('fallback_model', 'gemini-2-5-flash')
                    if fallback_model != model:
                        self.logger.info(f"Trying fallback model: {fallback_model}")
                        return self._run_openrouter_command(fallback_model, input_data)
                
                # Fall back to simulation mode if API fails
                self.logger.warning("API failed, falling back to simulation mode")
                return self._generate_simulation_response(input_data, model)
            
            # Parse output
            try:
                output = json.loads(result.stdout)
                return output
            except json.JSONDecodeError:
                return {'response': result.stdout}
                
        except subprocess.TimeoutExpired:
            self.logger.error("OpenRouter command timed out")
            return self._generate_simulation_response(input_data, model)
        except Exception as e:
            self.logger.error(f"Failed to run OpenRouter command: {e}")
            return self._generate_simulation_response(input_data, model)
    
    def _generate_simulation_response(self, input_data: Dict[str, Any], model: str) -> Dict[str, Any]:
        """
        Generate a simulated response for testing when API is unavailable
        
        Args:
            input_data: Input data for the model
            model: The model being simulated
            
        Returns:
            Simulated response
        """
        import random
        
        prompt = input_data.get('text', '')
        
        # Generate contextual mock responses based on prompt content
        mock_responses = [
            "This is a simulated AI response demonstrating the content generation framework. In production, this would be replaced with actual AI-generated content tailored to the soul's voice and personality.",
            "Transform your perspective through authentic connection. The journey of self-discovery begins with a single step into the unknown.",
            "Embrace the chaos within, for it is the crucible of creation. Your shadow holds the keys to your highest potential.",
            "Every interaction is an opportunity for transformation. Approach each moment with presence and intention.",
            "The path to sovereignty lies in integrating all aspects of yourself. Light and shadow dance together in the eternal now."
        ]
        
        # Select a response based on prompt keywords
        selected_response = mock_responses[0]
        if 'spiritual' in prompt.lower() or 'transformation' in prompt.lower():
            selected_response = mock_responses[1]
        elif 'shadow' in prompt.lower() or 'chaos' in prompt.lower():
            selected_response = mock_responses[2]
        elif 'connection' in prompt.lower() or 'interaction' in prompt.lower():
            selected_response = mock_responses[3]
        elif 'sovereignty' in prompt.lower() or 'integration' in prompt.lower():
            selected_response = mock_responses[4]
        
        # Simulate token usage
        input_tokens = len(prompt.split()) * 1.3  # Rough estimate
        output_tokens = len(selected_response.split()) * 1.3
        
        return {
            'response': selected_response,
            'usage': {
                'input_tokens': int(input_tokens),
                'output_tokens': int(output_tokens),
                'total_tokens': int(input_tokens + output_tokens)
            },
            'model': model,
            'simulation': True
        }
    
    def generate_with_openrouter(self, prompt: str, task_type: str = 'creative_writing', 
                                 complexity: str = 'medium', system_prompt: Optional[str] = None,
                                 max_tokens: Optional[int] = None, temperature: float = 0.7) -> Dict[str, Any]:
        """
        Generate content using OpenRouter models
        
        Args:
            prompt: The prompt to send to the model
            task_type: Type of task for model selection
            complexity: Complexity level for model selection
            system_prompt: Optional system prompt
            max_tokens: Maximum tokens to generate
            temperature: Temperature for generation
            
        Returns:
            Dictionary with generated content and metadata
        """
        # Select model
        model = self.select_model_for_task(task_type, complexity)
        model_config = AVAILABLE_MODELS.get(model, AVAILABLE_MODELS[self.default_model])
        
        # Prepare input data
        input_data = {
            'text': prompt,
            'temperature': temperature,
            'max_tokens': max_tokens or model_config.max_output
        }
        
        if system_prompt:
            input_data['system_prompt'] = system_prompt
        
        # Generate content
        self.logger.info(f"Generating content with model: {model}")
        output = self._run_openrouter_command(model_config.model_id, input_data)
        
        if 'error' in output:
            raise Exception(f"Content generation failed: {output['error']}")
        
        # Update usage stats
        self.usage_stats['total_requests'] += 1
        usage = output.get('usage', {})
        tokens = usage.get('total_tokens', 0)
        self.usage_stats['total_tokens'] += tokens
        
        # Estimate cost
        cost = self._estimate_cost(model_config, usage)
        self.usage_stats['total_cost'] += cost
        
        # Update model usage
        if model not in self.usage_stats['model_usage']:
            self.usage_stats['model_usage'][model] = 0
        self.usage_stats['model_usage'][model] += cost
        
        return {
            'content': output.get('response', ''),
            'model_used': model,
            'tokens_used': tokens,
            'cost': cost,
            'reasoning': output.get('reasoning', ''),
            'tool_calls': output.get('tool_calls', [])
        }
    
    def _estimate_cost(self, model_config: ModelConfig, usage: Dict[str, Any]) -> float:
        """Estimate cost based on token usage and model pricing"""
        input_tokens = usage.get('input_tokens', 0)
        output_tokens = usage.get('output_tokens', 0)
        
        input_cost = (input_tokens / 1_000_000) * model_config.pricing_per_million['input']
        output_cost = (output_tokens / 1_000_000) * model_config.pricing_per_million['output']
        
        return input_cost + output_cost
    
    def generate_soul_content(self, soul: Soul, request: ContentRequest) -> GeneratedContent:
        """
        Generate content for a soul using OpenRouter models
        
        Args:
            soul: The soul object
            request: ContentRequest with generation parameters
            
        Returns:
            GeneratedContent object with the generated content
        """
        # Build soul-specific prompt
        prompt = self._build_soul_prompt(soul, request)
        
        # Determine task type and complexity
        task_type = self._map_content_type_to_task(request.content_type)
        complexity = self._determine_complexity(request, soul)
        
        # Generate system prompt for soul persona
        system_prompt = self._build_soul_system_prompt(soul)
        
        # Generate content
        result = self.generate_with_openrouter(
            prompt=prompt,
            task_type=task_type,
            complexity=complexity,
            system_prompt=system_prompt,
            temperature=0.8 if request.content_type == 'creative' else 0.7
        )
        
        # Create result object
        generated_content = GeneratedContent(
            soul_id=request.soul_id,
            platform=request.platform,
            content_type=request.content_type,
            content=result['content'],
            model_used=result['model_used'],
            tokens_used=result['tokens_used'],
            cost_estimate=result['cost'],
            metadata={
                'soul_name': soul.name,
                'archetype': soul.archetype,
                'task_type': task_type,
                'complexity': complexity,
                'reasoning': result.get('reasoning', '')
            }
        )
        
        self.logger.info(f"Generated content for {soul.name} using {result['model_used']}")
        return generated_content
    
    def _build_soul_prompt(self, soul: Soul, request: ContentRequest) -> str:
        """Build a contextual prompt for content generation based on soul attributes"""
        prompt = f"""Generate {request.content_type} content for {soul.name}.

SOUL PROFILE:
- Name: {soul.name}
- Archetype: {soul.archetype}  
- Bio: {soul.bio}
- Voice: {soul.voice}
- Characteristic phrases: {', '.join(soul.hooks[:3])}
- Desires: {', '.join(soul.desires)}
- Shadow practice: {soul.shadow_practice}
- Sensory details: {soul.sensory}

PLATFORM: {request.platform}
CONTENT TYPE: {request.content_type}
"""
        
        if request.context:
            prompt += f"\nCONTEXT: {request.context}"
        
        if request.tone:
            prompt += f"\nTONE: {request.tone}"
        
        prompt += f"""

Generate content that:
1. Perfectly captures {soul.name}'s unique voice and personality
2. Reflects their {soul.archetype} archetype authentically
3. Incorporates their characteristic speaking style naturally
4. Aligns with their desires and shadow practice
5. Fits the {request.platform} platform appropriately
6. Uses sensory language that matches their profile: {soul.sensory}

Make the content feel authentic to {soul.name}, like something they would actually create or say."""
        
        return prompt
    
    def _build_soul_system_prompt(self, soul: Soul) -> str:
        """Build a system prompt that establishes the soul's persona"""
        return f"""You are {soul.name}, a {soul.archetype}. 

Your voice is {soul.voice}. You are known for saying things like: {', '.join(soul.hooks[:2])}.

Your core desires are: {', '.join(soul.desires)}.
Your shadow practice involves: {soul.shadow_practice}.

You experience the world through: {soul.sensory}.

Stay completely in character as {soul.name}. Generate content that feels authentic, personal, and true to your archetype and desires."""
    
    def _map_content_type_to_task(self, content_type: str) -> str:
        """Map content types to task types for model selection"""
        mapping = {
            'post': 'creative_writing',
            'bio': 'creative_writing',
            'message': 'creative_writing',
            'story': 'creative_writing',
            'analysis': 'analysis',
            'creative': 'creative_writing',
            'adaptation': 'creative_writing'
        }
        return mapping.get(content_type, 'creative_writing')
    
    def _determine_complexity(self, request: ContentRequest, soul: Soul) -> str:
        """Determine complexity level based on request and soul attributes"""
        # Higher complexity for legendary souls and complex content types
        if soul.rarity == 'Legendary':
            return 'high'
        
        if request.content_type in ['story', 'analysis']:
            return 'high'
        
        if request.length == 'long':
            return 'high'
        
        if request.content_type in ['post', 'message']:
            return 'low'
        
        return 'medium'
    
    def generate_batch_soul_content(self, requests: List[ContentRequest]) -> List[GeneratedContent]:
        """
        Generate content for multiple souls in batch using optimal model selection
        
        Args:
            requests: List of ContentRequest objects
            
        Returns:
            List of GeneratedContent objects
        """
        results = []
        
        for request in requests:
            try:
                soul = self.souls_manager.get_soul_by_id(request.soul_id)
                if soul:
                    result = self.generate_soul_content(soul, request)
                    results.append(result)
            except Exception as e:
                self.logger.error(f"Failed to generate content for {request.soul_id}: {e}")
                continue
        
        return results
    
    def get_usage_statistics(self) -> Dict[str, Any]:
        """Get usage statistics and costs"""
        # Convert ModelConfig objects to serializable dicts
        available_models_serializable = {}
        for k, v in AVAILABLE_MODELS.items():
            available_models_serializable[k] = {
                'model_id': v.model_id,
                'provider': v.provider.value,
                'capabilities': [cap.value for cap in v.capabilities],
                'context_window': v.context_window,
                'max_output': v.max_output,
                'pricing_per_million': v.pricing_per_million,
                'best_for': v.best_for
            }
        
        return {
            'total_requests': self.usage_stats['total_requests'],
            'total_tokens': self.usage_stats['total_tokens'],
            'total_cost': self.usage_stats['total_cost'],
            'model_usage': self.usage_stats['model_usage'],
            'available_models': available_models_serializable,
            'current_strategy': self.model_strategy
        }
    
    def reset_usage_stats(self):
        """Reset usage statistics"""
        self.usage_stats = {
            'total_requests': 0,
            'total_tokens': 0,
            'total_cost': 0.0,
            'model_usage': {}
        }
        self.logger.info("Usage statistics reset")