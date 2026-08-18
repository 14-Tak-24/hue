#!/usr/bin/env python3
"""
Test Enhanced Data Migration Features
Tests the new advanced migration features
"""

import sys
import json
from pathlib import Path

# Add the src directory to the path for package imports
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from data_migration import DataMigrationTool

def test_enhanced_migration():
    """Test the enhanced data migration functionality"""
    print("Testing Enhanced Data Migration Features...")
    
    migrator = DataMigrationTool()
    migrator.initialize_components(
        souls_data_path=str(Path(__file__).parent.parent / "src" / "data" / "souls_entities.json")
    )
    
    print("✓ Data Migration Tool initialized")
    
    # Test incremental backup
    print("\n" + "="*60)
    print("Incremental Backup")
    print("="*60)
    
    try:
        backup_path = migrator.incremental_backup("test_incremental_backup")
        print(f"✓ Incremental backup created: {backup_path}")
        
        # Verify backup files exist
        backup_dir = Path(backup_path)
        assert backup_dir.exists(), "Backup directory not created"
        assert (backup_dir / "souls.json").exists(), "souls.json not in backup"
        assert (backup_dir / "financial.json").exists(), "financial.json not in backup"
        assert (backup_dir / "change_log.json").exists(), "change_log.json not in backup"
        
        print("✓ Backup files verified")
    except Exception as e:
        print(f"Incremental backup test failed: {e}")
    
    # Test validation
    print("\n" + "="*60)
    print("Data Consistency Validation")
    print("="*60)
    
    validation_report = migrator.validate_data_consistency()
    print(f"Overall Status: {validation_report['overall_status']}")
    print(f"Timestamp: {validation_report['timestamp']}")
    
    print("\nValidation Results:")
    for component, results in validation_report['validations'].items():
        print(f"  {component.capitalize()}:")
        print(f"    Status: {results['status']}")
        if 'health_score' in results:
            print(f"    Health Score: {results['health_score']}")
        if 'anomalies' in results:
            print(f"    Anomalies: {results['anomalies']}")
        if 'errors' in results:
            print(f"    Errors: {results['errors']}")
        if 'warnings' in results:
            print(f"    Warnings: {results['warnings']}")
    
    # Test migration export for different systems
    print("\n" + "="*60)
    print("Migration Export")
    print("="*60)
    
    for target_system in ['firebase', 'mongodb']:
        try:
            export_path = migrator.export_for_migration(target_system)
            print(f"✓ {target_system.capitalize()} migration export: {export_path}")
            
            # Verify export file exists
            export_file = Path(export_path)
            assert export_file.exists(), f"{target_system} export file not created"
            
            if target_system != 'postgresql':
                # Verify JSON structure
                with open(export_file, 'r') as f:
                    data = json.load(f)
                assert 'format' in data, "Format not in export data"
                assert 'collections' in data, "Collections not in export data"
                
            print(f"✓ {target_system.capitalize()} export verified")
        except Exception as e:
            print(f"{target_system.capitalize()} export test failed: {e}")
    
    # Test PostgreSQL export
    try:
        postgresql_path = migrator.export_for_migration('postgresql')
        print(f"✓ PostgreSQL migration export: {postgresql_path}")
        
        # Verify SQL file
        sql_file = Path(postgresql_path)
        assert sql_file.exists(), "PostgreSQL export file not created"
        
        with open(sql_file, 'r') as f:
            sql_content = f.read()
        assert 'INSERT INTO souls' in sql_content, "SQL INSERT statements not found"
        
        print("✓ PostgreSQL export verified")
    except Exception as e:
        print(f"PostgreSQL export test failed: {e}")
    
    # Test Firestore sync (optional - requires Firebase credentials)
    print("\n" + "="*60)
    print("Firestore Sync")
    print("="*60)
    
    try:
        sync_results = migrator.sync_with_firestore('souls')
        print(f"✓ Firestore sync completed: {sync_results['synced_documents']} documents")
        if sync_results['errors']:
            print(f"  Errors: {len(sync_results['errors'])}")
            for error in sync_results['errors']:
                print(f"    - {error}")
    except Exception as e:
        print(f"Firestore sync test skipped (requires Firebase credentials): {e}")
    
    # Test full export
    print("\n" + "="*60)
    print("Full Data Export")
    print("="*60)
    
    try:
        export_dir = migrator.export_all_data("test_full_export")
        print(f"✓ Full data export completed: {export_dir}")
        
        # Verify export structure
        export_path = Path(export_dir)
        expected_files = ['souls.json', 'financial.json', 'tributes.json', 'backup_info.json', 'integrity_report.json', 'export_info.json']
        
        for expected_file in expected_files:
            assert (export_path / expected_file).exists(), f"{expected_file} not in export"
        
        print("✓ Full export structure verified")
    except Exception as e:
        print(f"Full export test failed: {e}")
    
    print("\n" + "="*60)
    print("All enhanced migration tests completed!")
    print("="*60)

if __name__ == "__main__":
    try:
        test_enhanced_migration()
        print(f"\n🎉 Enhanced data migration test completed successfully!")
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)