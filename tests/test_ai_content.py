#!/usr/bin/env python3
"""
Test AI Content Generation Integration
Tests the real AI content generation with OpenAI API
"""

import sys
import os
import traceback
from pathlib import Path

# Add the src directory to the path for package imports
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from src.modules.souls_content_integration import SoulsContentIntegration, ContentRequest
from src.modules.souls_manager import SoulsManager


def test_ai_content_generation():
    """Test AI content generation with real API"""
    print("Testing AI Content Generation...")
    
    # Check for API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("⚠️  No OPENAI_API_KEY found in environment variables")
        print("   Using fallback content generation")
        print("   To use real AI, set: export OPENAI_API_KEY='your-key-here'")
    else:
        print("✓ OpenAI API key found")
    
    # Initialize components
    data_path = Path(__file__).parent.parent / "src" / "data" / "souls_entities.json"
    souls_manager = SoulsManager(str(data_path))
    content_integration = SoulsContentIntegration(
        souls_manager=souls_manager,
        api_key=api_key,
        model="gpt-3.5-turbo"
    )
    
    # Get a test soul
    test_soul = souls_manager.get_soul_by_name("Mac Nazarene")
    assert test_soul is not None, "Test soul not found"
    
    print(f"\nTesting with soul: {test_soul.name} ({test_soul.archetype})")
    
    # Test different content types using platforms the soul actually supports
    test_requests = [
        ContentRequest(
            soul_id=test_soul.id,
            topic="Spiritual transformation in modern times",
            platform="Twitter",
            content_type="social_post",
            target_audience="Spiritual seekers",
            custom_instructions="Make it inspiring and actionable"
        ),
        ContentRequest(
            soul_id=test_soul.id,
            topic="The power of community rituals",
            platform="Discord",
            content_type="social_post",
            target_audience="General audience interested in personal growth"
        ),
        ContentRequest(
            soul_id=test_soul.id,
            topic="Finding your spiritual path",
            platform="FetLife",
            content_type="social_post",
            target_audience="Adults seeking spiritual connection"
        )
    ]
    
    for i, request in enumerate(test_requests, 1):
        print(f"\n{'='*60}")
        print(f"Test {i}: {request.content_type} for {request.platform}")
        print(f"Topic: {request.topic}")
        print(f"{'='*60}")
        
        try:
            response = content_integration.generate_content_for_soul(request)
            
            print("\n✓ Content generated successfully")
            print(f"Soul: {response.soul_name}")
            print(f"Platform: {response.platform}")
            print(f"Content Type: {response.content_type}")
            print(f"Voice Style: {response.voice_style}")
            print("\nGenerated Content:")
            print("-" * 60)
            print(response.content)
            print("-" * 60)
            
            # Store in history
            content_integration.content_history.append(response)
            
        except Exception as e:
            print(f"❌ Content generation failed: {e}")
            traceback.print_exc()
            raise
    
    # Show analytics
    print(f"\n{'='*60}")
    print("Content Generation Analytics")
    print(f"{'='*60}")
    analytics = content_integration.get_content_analytics()
    print(f"Total content generated: {analytics['total_content_generated']}")
    print(f"Content by soul: {analytics['content_by_soul']}")
    print(f"Content by platform: {analytics['content_by_platform']}")
    print(f"Content by type: {analytics['content_by_type']}")
    
    assert analytics['total_content_generated'] > 0, "No content was generated"


if __name__ == "__main__":
    try:
        test_ai_content_generation()
        print(f"\n🎉 AI content generation test completed successfully!")
    except Exception as e:
        print(f"❌ Test failed: {e}")
        traceback.print_exc()
        sys.exit(1)
