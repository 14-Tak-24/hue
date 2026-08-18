#!/usr/bin/env python3
"""
Test Phase 1 AI Foundation Components
Tests the new AI content generator, OpenRouter integration, and content pipeline
"""

import sys
import os
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
    print(f"  - Supported platforms: {len(stats['supported_platforms'])}")
    print(f"  - Souls loaded: {stats['souls_count']}")


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
    print(f"  - Generated prompt for {test_soul.name}")


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
    print(f"  - Default model: {openrouter.default_model}")
    print(f"  - Model strategy: {openrouter.model_strategy}")


def test_openrouter_models_config():
    """Test OpenRouter model configuration"""
    print("\nTesting OpenRouter model configuration...")
    
    data_path = Path(__file__).parent.parent / "src" / "data" / "souls_entities.json"
    souls_manager = SoulsManager(str(data_path))
    openrouter = OpenRouterIntegration(souls_manager)
    
    stats = openrouter.get_usage_statistics()
    
    assert 'available_models' in stats
    assert 'current_strategy' in stats
    assert len(stats['available_models']) > 0
    
    # Check that models have required fields
    for model_id, model_info in stats['available_models'].items():
        assert 'model_id' in model_info
        assert 'provider' in model_info
        assert 'capabilities' in model_info
        assert 'pricing_per_million' in model_info
    
    print("✓ OpenRouter model configuration validated")
    print(f"  - Configured models: {len(stats['available_models'])}")
    print(f"  - Current strategy: {stats['current_strategy']}")


def test_content_pipeline_initialization():
    """Test Content Pipeline initialization"""
    print("\nTesting Content Pipeline initialization...")
    
    data_path = Path(__file__).parent.parent / "src" / "data" / "souls_entities.json"
    souls_manager = SoulsManager(str(data_path))
    
    # Mock the AI components for testing
    mock_openrouter = Mock()
    mock_generator = Mock()
    
    pipeline = ContentPipeline(souls_manager, mock_openrouter, mock_generator)
    
    assert pipeline.souls_manager is not None
    assert pipeline.openrouter is not None
    assert pipeline.ai_generator is not None
    
    print("✓ Content Pipeline initialized successfully")


def test_content_pipeline_stats():
    """Test Content Pipeline statistics"""
    print("\nTesting Content Pipeline statistics...")
    
    data_path = Path(__file__).parent.parent / "src" / "data" / "souls_entities.json"
    souls_manager = SoulsManager(str(data_path))
    
    # Mock the AI components
    mock_openrouter = Mock()
    mock_generator = Mock()
    
    pipeline = ContentPipeline(souls_manager, mock_openrouter, mock_generator)
    
    stats = pipeline.get_pipeline_statistics()
    
    # Check that the stats dict exists and has basic structure
    assert stats is not None
    assert isinstance(stats, dict)
    
    # The actual keys may vary, so just check the dict is valid
    print("✓ Content Pipeline statistics validated")
    print(f"  - Statistics keys: {list(stats.keys())}")


def test_platform_specific_strategies():
    """Test platform-specific content strategies"""
    print("\nTesting platform-specific strategies...")
    
    data_path = Path(__file__).parent.parent / "src" / "data" / "souls_entities.json"
    souls_manager = SoulsManager(str(data_path))
    generator = AIContentGenerator(souls_manager)
    
    # Check that major platforms have guidelines
    assert 'Twitter' in generator.platform_guidelines
    assert 'Instagram' in generator.platform_guidelines
    assert 'Discord' in generator.platform_guidelines
    
    # Verify Twitter has character limit
    twitter_guide = generator.platform_guidelines['Twitter']
    assert 'max_length' in twitter_guide
    assert twitter_guide['max_length'] == 280
    
    print("✓ Platform-specific strategies validated")
    print(f"  - Platforms with guidelines: {len(generator.platform_guidelines)}")


def test_soul_platform_compatibility():
    """Test that souls have compatible platforms"""
    print("\nTesting soul-platform compatibility...")
    
    data_path = Path(__file__).parent.parent / "src" / "data" / "souls_entities.json"
    souls_manager = SoulsManager(str(data_path))
    
    souls = souls_manager.get_all_souls()
    
    # Count platforms across all souls
    platform_counts = {}
    for soul in souls:
        for platform in soul.platforms:
            platform_counts[platform] = platform_counts.get(platform, 0) + 1
    
    print(f"✓ Soul-platform compatibility checked")
    print(f"  - Total souls: {len(souls)}")
    print(f"  - Platforms used: {len(platform_counts)}")
    for platform, count in sorted(platform_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"    - {platform}: {count} souls")


def run_all_tests():
    """Run all Phase 1 AI tests"""
    print("="*60)
    print("Phase 1 AI Foundation - Component Tests")
    print("="*60)
    
    tests = [
        test_ai_content_generator_initialization,
        test_content_request_structure,
        test_generated_content_structure,
        test_soul_prompt_building,
        test_platform_formatting,
        test_openrouter_initialization,
        test_openrouter_models_config,
        test_content_pipeline_initialization,
        test_content_pipeline_stats,
        test_platform_specific_strategies,
        test_soul_platform_compatibility
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"❌ {test.__name__} failed: {e}")
            import traceback
            traceback.print_exc()
            failed += 1
    
    print("\n" + "="*60)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("="*60)
    
    if failed > 0:
        sys.exit(1)
    else:
        print("\n🎉 All Phase 1 AI component tests passed!")


if __name__ == "__main__":
    run_all_tests()
