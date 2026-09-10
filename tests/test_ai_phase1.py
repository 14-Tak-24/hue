#!/usr/bin/env python3
"""
Test Phase 1 AI Foundation Components
Tests the new AI content generator, OpenRouter integration, and content pipeline
"""

import sys
import os
import traceback
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import json

# Add the src directory to the path for package imports
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from modules.ai_content_generator import AIContentGenerator, ContentRequest, GeneratedContent
from modules.openrouter_integration import OpenRouterIntegration, ContentRequest as ORContentRequest
from modules.content_pipeline import ContentPipeline
from modules.souls_manager import SoulsManager


def test_ai_content_generator_initialization():
    """Test AI Content Generator initialization"""
    print("Testing AI Content Generator initialization...")
    
    data_path = Path(__file__).parent.parent / "src" / "data" / "souls_entities.json"
    souls_manager = SoulsManager(str(data_path))
    
    generator = AIContentGenerator(souls_manager)
    
    assert generator.souls_manager is not None
    assert generator.config is not None
    assert len(generator.default_models) > 0
    assert len(generator.platform_guidelines) > 0
    
    stats = generator.get_generation_stats()
    assert stats['souls_count'] == 28
    assert len(stats['supported_platforms']) > 0
    
    print("✓ AI Content Generator initialized successfully")
    print("  - Supported platforms: %d", len(stats['supported_platforms']))
    print("  - Souls loaded: %d", stats['souls_count'])


def test_content_request_structure():
    """Test ContentRequest dataclass"""
    print("\nTesting ContentRequest structure...")
    
    request = ContentRequest(
        soul_id="test_soul_1",
        platform="Twitter",
        content_type="post",
        context="Test context",
        tone="casual",
        length="short"
    )
    
    assert request.soul_id == "test_soul_1"
    assert request.platform == "Twitter"
    assert request.content_type == "post"
    assert request.length == "short"
    
    print("✓ ContentRequest structure validated")


def test_generated_content_structure():
    """Test GeneratedContent dataclass"""
    print("\nTesting GeneratedContent structure...")
    
    content = GeneratedContent(
        soul_id="test_soul_1",
        platform="Twitter",
        content_type="post",
        content="Test content here",
        model_used="test-model",
        tokens_used=100,
        cost_estimate=0.01
    )
    
    assert content.soul_id == "test_soul_1"
    assert content.platform == "Twitter"
    assert content.content == "Test content here"
    assert content.generated_at is not None  # Should auto-generate timestamp
    
    print("✓ GeneratedContent structure validated")


def test_soul_prompt_building():
    """Test soul-specific prompt building"""
    print("\nTesting soul prompt building...")
    
    data_path = Path(__file__).parent.parent / "src" / "data" / "souls_entities.json"
    souls_manager = SoulsManager(str(data_path))
    generator = AIContentGenerator(souls_manager)
    
    # Get a test soul
    test_soul = souls_manager.get_soul_by_name("Mac Nazarene")
    assert test_soul is not None, "Test soul not found"
    
    request = ContentRequest(
        soul_id=test_soul.id,
        platform="Twitter",
        content_type="post",
        context="Spiritual transformation",
        tone="inspiring"
    )
    
    prompt = generator._build_soul_prompt(test_soul, request)
    
    assert test_soul.name in prompt
    assert test_soul.archetype in prompt
    assert test_soul.voice in prompt
    assert "Twitter" in prompt
    assert "Spiritual transformation" in prompt
    
    print("✓ Soul prompt building works correctly")
    print("  - Generated prompt for %s", test_soul.name)


def test_platform_formatting():
    """Test platform-specific content formatting"""
    print("\nTesting platform formatting...")
    
    data_path = Path(__file__).parent.parent / "src" / "data" / "souls_entities.json"
    souls_manager = SoulsManager(str(data_path))
    generator = AIContentGenerator(souls_manager)
    
    # Test Twitter formatting
    twitter_content = generator._format_for_platform("This is a test. Another sentence here.", "Twitter")
    assert "\n" in twitter_content  # Should add line breaks
    
    # Test Instagram formatting
    insta_content = generator._format_for_platform("Test content", "Instagram")
    assert "✨" in insta_content  # Should add emojis
    
    print("✓ Platform formatting works correctly")


def test_openrouter_initialization():
    """Test OpenRouter integration initialization"""
    print("\nTesting OpenRouter integration initialization...")
    
    data_path = Path(__file__).parent.parent / "src" / "data" / "souls_entities.json"
    souls_manager = SoulsManager(str(data_path))
    
    openrouter = OpenRouterIntegration(souls_manager)
    
    assert openrouter.souls_manager is not None
    assert openrouter.default_model is not None
    assert openrouter.usage_stats is not None
    
    print("✓ OpenRouter integration initialized successfully")
    print("  - Default model: %s", openrouter.default_model)
    print("  - Model strategy: %s", openrouter.model_strategy)


def test_openrouter_models_config():
    """Test OpenRouter model configuration"""
    print("\nTesting OpenRouter model configuration...")
    
{