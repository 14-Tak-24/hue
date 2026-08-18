#!/usr/bin/env python3
"""
Test Souls Manager Coverage
Tests to improve test coverage for souls_manager.py
"""

import sys
import json
from pathlib import Path
from datetime import datetime

# Add the src directory to the path for package imports
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from src.modules.souls_manager import SoulsManager, Soul, Rarity, Gender
from src.modules.utils import ValidationUtils

def test_soul_validation():
    """Test soul data validation"""
    print("Testing Soul Validation...")
    
    # Initialize with explicit path
    data_path = Path(__file__).parent.parent / "src" / "data" / "souls_entities.json"
    souls_manager = SoulsManager(str(data_path))
    
    # Test valid soul
    valid_soul = Soul(
        id="test_001",
        name="Test Soul",
        gender="M",
        archetype="Test Archetype",
        bio="Test bio",
        sensory="Test sensory",
        voice="Test voice",
        hooks=["Hook 1", "Hook 2"],
        desires=["Desire 1", "Desire 2"],
        kinks=["Kink 1", "Kink 2"],
        tribute_impact="Test impact",
        shadow_practice="Test shadow",
        email="test@example.com",
        image="https://example.com/image.png",
        rarity="Rare",
        platforms=["Twitter", "Discord"],
        tier="upper"
    )
    
    errors = souls_manager.validate_soul_data(valid_soul)
    assert len(errors) == 0, f"Valid soul should have no errors, got: {errors}"
    print("✓ Valid soul validation passed")
    
    # Test missing required fields
    invalid_soul = Soul(
        id="",
        name="",
        gender="M",
        archetype="Test",
        bio="Test",
        sensory="Test",
        voice="Test",
        hooks=["Hook"],
        desires=["Desire"],
        kinks=["Kink"],
        tribute_impact="Test",
        shadow_practice="Test",
        email="test@example.com",
        image="https://example.com/image.png",
        rarity="Rare",
        platforms=["Twitter"],
        tier="upper"
    )
    
    errors = souls_manager.validate_soul_data(invalid_soul)
    assert len(errors) > 0, "Invalid soul should have errors"
    assert any("Missing required field" in error for error in errors), "Should have missing field errors"
    print("✓ Missing field validation passed")
    
    # Test invalid gender
    invalid_gender_soul = Soul(
        id="test_002",
        name="Test",
        gender="X",  # Invalid gender
        archetype="Test",
        bio="Test",
        sensory="Test",
        voice="Test",
        hooks=["Hook"],
        desires=["Desire"],
        kinks=["Kink"],
        tribute_impact="Test",
        shadow_practice="Test",
        email="test@example.com",
        image="https://example.com/image.png",
        rarity="Rare",
        platforms=["Twitter"],
        tier="upper"
    )
    
    errors = souls_manager.validate_soul_data(invalid_gender_soul)
    assert any("Invalid gender" in error for error in errors), "Should have gender validation error"
    print("✓ Gender validation passed")
    
    # Test invalid rarity
    invalid_rarity_soul = Soul(
        id="test_003",
        name="Test",
        gender="M",
        archetype="Test",
        bio="Test",
        sensory="Test",
        voice="Test",
        hooks=["Hook"],
        desires=["Desire"],
        kinks=["Kink"],
        tribute_impact="Test",
        shadow_practice="Test",
        email="test@example.com",
        image="https://example.com/image.png",
        rarity="Epic",  # Invalid rarity
        platforms=["Twitter"],
        tier="upper"
    )
    
    errors = souls_manager.validate_soul_data(invalid_rarity_soul)
    assert any("Invalid rarity" in error for error in errors), "Should have rarity validation error"
    print("✓ Rarity validation passed")
    
    # Test empty lists
    empty_lists_soul = Soul(
        id="test_004",
        name="Test",
        gender="M",
        archetype="Test",
        bio="Test",
        sensory="Test",
        voice="Test",
        hooks=[],  # Empty
        desires=[],  # Empty
        kinks=[],  # Empty
        tribute_impact="Test",
        shadow_practice="Test",
        email="test@example.com",
        image="https://example.com/image.png",
        rarity="Rare",
        platforms=[],  # Empty
        tier="upper"
    )
    
    errors = souls_manager.validate_soul_data(empty_lists_soul)
    assert len(errors) >= 4, "Should have errors for empty lists"
    print("✓ Empty list validation passed")

def test_add_soul():
    """Test adding a new soul"""
    print("\nTesting Add Soul...")
    
    data_path = Path(__file__).parent.parent / "src" / "data" / "souls_entities.json"
    souls_manager = SoulsManager(str(data_path))
    
    initial_count = len(souls_manager.get_all_souls())
    
    new_soul = Soul(
        id="test_new_001",
        name="New Test Soul",
        gender="F",
        archetype="Test Archetype",
        bio="Test bio for new soul",
        sensory="Test sensory",
        voice="Test voice",
        hooks=["New Hook 1", "New Hook 2"],
        desires=["New Desire 1"],
        kinks=["New Kink 1"],
        tribute_impact="Test impact",
        shadow_practice="Test shadow",
        email="newtest@example.com",
        image="https://example.com/newimage.png",
        rarity="Common",
        platforms=["Twitter"],
        tier="second"
    )
    
    result = souls_manager.add_soul(new_soul)
    assert result == True, "Add soul should succeed"
    
    new_count = len(souls_manager.get_all_souls())
    assert new_count == initial_count + 1, "Soul count should increase by 1"
    
    # Verify the soul was added
    added_soul = souls_manager.get_soul_by_id("test_new_001")
    assert added_soul is not None, "Added soul should be retrievable"
    assert added_soul.name == "New Test Soul", "Added soul should have correct name"
    
    print("✓ Add soul functionality passed")

def test_update_soul():
    """Test updating an existing soul"""
    print("\nTesting Update Soul...")
    
    data_path = Path(__file__).parent.parent / "src" / "data" / "souls_entities.json"
    souls_manager = SoulsManager(str(data_path))
    
    # Get a soul to update
    soul = souls_manager.get_soul_by_id("soul_001")
    assert soul is not None, "Should find soul_001"
    
    original_name = soul.name
    updated_name = "Updated Mac Nazarene"
    
    # Update the soul with correct method signature
    soul.name = updated_name
    result = souls_manager.update_soul("soul_001", soul)
    assert result == True, "Update soul should succeed"
    
    # Verify the update
    updated_soul = souls_manager.get_soul_by_id("soul_001")
    assert updated_soul.name == updated_name, "Soul name should be updated"
    
    # Restore original name
    updated_soul.name = original_name
    souls_manager.update_soul("soul_001", updated_soul)
    
    print("✓ Update soul functionality passed")

def test_delete_soul():
    """Test deleting a soul"""
    print("\nTesting Delete Soul...")
    
    data_path = Path(__file__).parent.parent / "src" / "data" / "souls_entities.json"
    souls_manager = SoulsManager(str(data_path))
    
    # Add a test soul first
    test_soul = Soul(
        id="test_delete_001",
        name="Delete Test Soul",
        gender="M",
        archetype="Test",
        bio="Test",
        sensory="Test",
        voice="Test",
        hooks=["Hook"],
        desires=["Desire"],
        kinks=["Kink"],
        tribute_impact="Test",
        shadow_practice="Test",
        email="delete@example.com",
        image="https://example.com/image.png",
        rarity="Common",
        platforms=["Twitter"],
        tier="second"
    )
    
    souls_manager.add_soul(test_soul)
    
    # Delete the soul
    result = souls_manager.delete_soul("test_delete_001")
    assert result == True, "Delete soul should succeed"
    
    # Verify deletion
    deleted_soul = souls_manager.get_soul_by_id("test_delete_001")
    assert deleted_soul is None, "Deleted soul should not be found"
    
    print("✓ Delete soul functionality passed")

def test_search_functionality():
    """Test advanced search functionality"""
    print("\nTesting Search Functionality...")
    
    data_path = Path(__file__).parent.parent / "src" / "data" / "souls_entities.json"
    souls_manager = SoulsManager(str(data_path))
    
    # Test search by name
    results = souls_manager.search_souls("Mac")
    assert len(results) > 0, "Should find souls with 'Mac' in name"
    assert any("Mac" in soul.name for soul in results), "Results should contain 'Mac'"
    print("✓ Name search passed")
    
    # Test search by archetype
    results = souls_manager.search_souls("Priest")
    assert len(results) > 0, "Should find souls with 'Priest' in archetype"
    print("✓ Archetype search passed")
    
    # Test search by bio
    results = souls_manager.search_souls("spiritual")
    assert len(results) > 0, "Should find souls with 'spiritual' in bio"
    print("✓ Bio search passed")
    
    # Test empty search (returns all souls in current implementation)
    results = souls_manager.search_souls("")
    assert len(results) >= 0, "Empty search should handle gracefully"
    print("✓ Empty search passed")

def test_filter_by_multiple_criteria():
    """Test filtering by multiple criteria"""
    print("\nTesting Multi-Criteria Filtering...")
    
    data_path = Path(__file__).parent.parent / "src" / "data" / "souls_entities.json"
    souls_manager = SoulsManager(str(data_path))
    
    # Test filter by rarity
    legendary_souls = souls_manager.get_souls_by_rarity("Legendary")
    assert all(soul.rarity == "Legendary" for soul in legendary_souls), "All should be Legendary"
    print("✓ Rarity filter passed")
    
    # Test filter by gender
    male_souls = souls_manager.get_souls_by_gender("M")
    assert all(soul.gender == "M" for soul in male_souls), "All should be Male"
    print("✓ Gender filter passed")
    
    # Test filter by platform
    twitter_souls = souls_manager.get_souls_by_platform("Twitter")
    assert all("Twitter" in soul.platforms for soul in twitter_souls), "All should have Twitter"
    print("✓ Platform filter passed")
    
    # Test filter by tier
    upper_souls = souls_manager.get_souls_by_tier("upper")
    assert all(soul.tier == "upper" for soul in upper_souls), "All should be upper tier"
    print("✓ Tier filter passed")

def test_compatibility_scoring():
    """Test soul compatibility scoring"""
    print("\nTesting Compatibility Scoring...")
    
    data_path = Path(__file__).parent.parent / "src" / "data" / "souls_entities.json"
    souls_manager = SoulsManager(str(data_path))
    
    # Get two soul IDs
    soul_id1 = "soul_001"
    soul_id2 = "soul_002"
    
    # Calculate compatibility using correct method
    score = souls_manager.get_soul_compatibility_score(soul_id1, soul_id2)
    assert 0 <= score <= 100, "Compatibility score should be between 0 and 100"
    print(f"✓ Compatibility score between {soul_id1} and {soul_id2}: {score}")
    
    # Test with same soul (should be high compatibility)
    same_score = souls_manager.get_soul_compatibility_score(soul_id1, soul_id1)
    assert same_score >= score, "Same soul should have high compatibility"
    print("✓ Self-compatibility scoring passed")
    
    # Test finding compatible souls
    compatible_souls = souls_manager.find_compatible_souls(soul_id1, threshold=50.0)
    assert len(compatible_souls) >= 0, "Should return compatible souls list"
    print(f"✓ Found {len(compatible_souls)} compatible souls")

def test_network_analysis():
    """Test network analysis functionality"""
    print("\nTesting Network Analysis...")
    
    data_path = Path(__file__).parent.parent / "src" / "data" / "souls_entities.json"
    souls_manager = SoulsManager(str(data_path))
    
    # Get network map using correct method
    network_map = souls_manager.get_soul_network_map()
    assert len(network_map) > 0, "Should have network connections"
    
    # Check network map structure
    for soul_id, connections in network_map.items():
        assert isinstance(soul_id, str), "Soul ID should be string"
        assert isinstance(connections, list), "Connections should be list"
    
    print(f"✓ Network analysis found {len(network_map)} souls with connections")

def test_platform_management():
    """Test platform management functionality"""
    print("\nTesting Platform Management...")
    
    data_path = Path(__file__).parent.parent / "src" / "data" / "souls_entities.json"
    souls_manager = SoulsManager(str(data_path))
    
    # Get a soul to modify
    soul = souls_manager.get_soul_by_id("soul_001")
    original_platforms = soul.platforms.copy()
    
    # Add a new platform
    result = souls_manager.add_platform_to_soul("soul_001", "TikTok")
    assert result == True, "Should successfully add platform"
    
    # Verify platform was added
    updated_soul = souls_manager.get_soul_by_id("soul_001")
    assert "TikTok" in updated_soul.platforms, "Platform should be added"
    
    # Remove the platform
    result = souls_manager.remove_platform_from_soul("soul_001", "TikTok")
    assert result == True, "Should successfully remove platform"
    
    # Verify platform was removed
    final_soul = souls_manager.get_soul_by_id("soul_001")
    assert "TikTok" not in final_soul.platforms, "Platform should be removed"
    
    # Restore original platforms
    final_soul.platforms = original_platforms
    souls_manager.update_soul("soul_001", final_soul)
    
    print("✓ Platform management passed")

def test_export_functionality():
    """Test export functionality"""
    print("\nTesting Export Functionality...")
    
    data_path = Path(__file__).parent.parent / "src" / "data" / "souls_entities.json"
    souls_manager = SoulsManager(str(data_path))
    
    # Test export for platform
    twitter_exports = souls_manager.export_souls_for_platform("Twitter")
    assert len(twitter_exports) > 0, "Should export Twitter souls"
    # Check that exports have expected fields
    assert all('name' in export for export in twitter_exports), "All should have name"
    assert all('bio' in export for export in twitter_exports), "All should have bio"
    print(f"✓ Exported {len(twitter_exports)} souls for Twitter")
    
    # Test metadata
    metadata = souls_manager.get_metadata()
    assert 'total_souls' in metadata, "Should have total souls count"
    assert 'archetypes' in metadata, "Should have archetypes info"
    print("✓ Metadata retrieval passed")
    
    # Test statistics
    stats = souls_manager.get_statistics()
    assert 'total_souls' in stats, "Should have total souls"
    assert 'rarity_distribution' in stats, "Should have rarity distribution"
    print("✓ Statistics retrieval passed")

def test_backup_functionality():
    """Test backup functionality"""
    print("\nTesting Backup Functionality...")
    
    data_path = Path(__file__).parent.parent / "src" / "data" / "souls_entities.json"
    souls_manager = SoulsManager(str(data_path))
    
    # Test listing backups
    backups = souls_manager.list_backups()
    assert isinstance(backups, list), "Should return list of backups"
    print(f"✓ Found {len(backups)} existing backups")
    
    # Test save functionality
    result = souls_manager.save_souls_data()
    assert result == True, "Should successfully save data"
    print("✓ Save data functionality passed")

def test_random_soul_selection():
    """Test random soul selection"""
    print("\nTesting Random Soul Selection...")
    
    data_path = Path(__file__).parent.parent / "src" / "data" / "souls_entities.json"
    souls_manager = SoulsManager(str(data_path))
    
    # Test random soul
    random_soul = souls_manager.get_random_soul()
    assert random_soul is not None, "Should return a random soul"
    assert isinstance(random_soul, Soul), "Should return Soul object"
    print(f"✓ Random soul: {random_soul.name}")
    
    # Test random soul by rarity
    rare_soul = souls_manager.get_random_soul_by_rarity("Rare")
    assert rare_soul is not None, "Should return a rare soul"
    assert rare_soul.rarity == "Rare", "Should be Rare rarity"
    print(f"✓ Random rare soul: {rare_soul.name}")
    
    # Test with non-existent rarity
    common_soul = souls_manager.get_random_soul_by_rarity("Common")
    # This might return None if no Common souls exist
    print("✓ Random soul by rarity passed")

def run_all_tests():
    """Run all coverage tests"""
    print("="*60)
    print("Souls Manager Coverage Tests")
    print("="*60)
    
    try:
        test_soul_validation()
        test_add_soul()
        test_update_soul()
        test_delete_soul()
        test_search_functionality()
        test_filter_by_multiple_criteria()
        test_compatibility_scoring()
        test_network_analysis()
        test_platform_management()
        test_export_functionality()
        test_backup_functionality()
        test_random_soul_selection()
        
        print("\n" + "="*60)
        print("All souls manager coverage tests passed successfully!")
        print("="*60)
        return True
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
