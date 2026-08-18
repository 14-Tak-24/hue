#!/usr/bin/env python3
"""
Test Real AI Content Generation
Tests actual AI content generation using inference.sh CLI with real API calls
"""

import sys
import os
from pathlib import Path
import json

# Add the src directory to the path for package imports
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from modules.souls_manager import SoulsManager
from modules.openrouter_integration import OpenRouterIntegration, ContentRequest


def test_real_ai_generation():
    """Test actual AI content generation with real API calls"""
    print("="*60)
    print("Testing Real AI Content Generation")
    print("="*60)
    
    # Initialize souls manager
    data_path = Path(__file__).parent.parent / "src" / "data" / "souls_entities.json"
    souls_manager = SoulsManager(str(data_path))
    
    # Initialize OpenRouter integration
    openrouter = OpenRouterIntegration(souls_manager)
    
    # Get a test soul
    test_soul = souls_manager.get_soul_by_name("Mac Nazarene")
    if not test_soul:
        print("❌ Test soul not found")
        return False
    
    print(f"\n🎭 Testing with soul: {test_soul.name}")
    print(f"   Archetype: {test_soul.archetype}")
    print(f"   Platforms: {', '.join(test_soul.platforms[:3])}")
    
    # Test 1: Generate a Twitter post
    print("\n" + "-"*60)
    print("Test 1: Generating Twitter post")
    print("-"*60)
    
    try:
        request = ContentRequest(
            soul_id=test_soul.id,
            platform="Twitter",
            content_type="post",
            context="Spiritual transformation and personal growth",
            tone="inspiring",
            length="short"
        )
        
        result = openrouter.generate_soul_content(test_soul, request)
        
        print(f"✅ Twitter post generated successfully!")
        print(f"   Model used: {result.model_used}")
        print(f"   Tokens used: {result.tokens_used}")
        print(f"   Cost estimate: ${result.cost_estimate:.4f}")
        print(f"\n   Generated content:")
        print(f"   {result.content}")
        
    except Exception as e:
        print(f"❌ Twitter post generation failed: {e}")
        return False
    
    # Test 2: Generate an Instagram caption
    print("\n" + "-"*60)
    print("Test 2: Generating Instagram caption")
    print("-"*60)
    
    try:
        request = ContentRequest(
            soul_id=test_soul.id,
            platform="Instagram",
            content_type="caption",
            context="Behind the scenes of spiritual practice",
            tone="authentic",
            length="medium"
        )
        
        result = openrouter.generate_soul_content(test_soul, request)
        
        print(f"✅ Instagram caption generated successfully!")
        print(f"   Model used: {result.model_used}")
        print(f"   Tokens used: {result.tokens_used}")
        print(f"   Cost estimate: ${result.cost_estimate:.4f}")
        print(f"\n   Generated content:")
        print(f"   {result.content}")
        
    except Exception as e:
        print(f"❌ Instagram caption generation failed: {e}")
        return False
    
    # Test 3: Generate a Discord message
    print("\n" + "-"*60)
    print("Test 3: Generating Discord message")
    print("-"*60)
    
    try:
        request = ContentRequest(
            soul_id=test_soul.id,
            platform="Discord",
            content_type="message",
            context="Welcoming new community members",
            tone="warm",
            length="medium"
        )
        
        result = openrouter.generate_soul_content(test_soul, request)
        
        print(f"✅ Discord message generated successfully!")
        print(f"   Model used: {result.model_used}")
        print(f"   Tokens used: {result.tokens_used}")
        print(f"   Cost estimate: ${result.cost_estimate:.4f}")
        print(f"\n   Generated content:")
        print(f"   {result.content}")
        
    except Exception as e:
        print(f"❌ Discord message generation failed: {e}")
        return False
    
    # Test 4: Generate for a different soul
    print("\n" + "-"*60)
    print("Test 4: Testing with different soul")
    print("-"*60)
    
    test_soul2 = souls_manager.get_soul_by_name("Slurchin Drip")
    if not test_soul2:
        print("⚠️ Second test soul not found, skipping")
    else:
        print(f"🎭 Testing with soul: {test_soul2.name}")
        print(f"   Archetype: {test_soul2.archetype}")
        
        try:
            request = ContentRequest(
                soul_id=test_soul2.id,
                platform="Twitter",
                content_type="post",
                context="Street culture and urban exploration",
                tone="authentic",
                length="short"
            )
            
            result = openrouter.generate_soul_content(test_soul2, request)
            
            print(f"✅ Post generated for {test_soul2.name}!")
            print(f"   Model used: {result.model_used}")
            print(f"   Tokens used: {result.tokens_used}")
            print(f"   Cost estimate: ${result.cost_estimate:.4f}")
            print(f"\n   Generated content:")
            print(f"   {result.content}")
            
        except Exception as e:
            print(f"❌ Post generation failed for {test_soul2.name}: {e}")
            return False
    
    # Print usage statistics
    print("\n" + "-"*60)
    print("Usage Statistics")
    print("-"*60)
    
    stats = openrouter.get_usage_statistics()
    print(f"Total requests: {stats['total_requests']}")
    print(f"Total tokens: {stats['total_tokens']}")
    print(f"Total cost: ${stats['total_cost']:.4f}")
    print(f"Model usage: {json.dumps(stats['model_usage'], indent=2)}")
    
    print("\n" + "="*60)
    print("✅ All real AI generation tests completed successfully!")
    print("="*60)
    
    return True


if __name__ == "__main__":
    success = test_real_ai_generation()
    sys.exit(0 if success else 1)