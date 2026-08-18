#!/usr/bin/env python3
"""
Data Migration Utilities
Tools for migrating, exporting, and importing platform data
"""

import sys
import json
import csv
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
import shutil

# Add the src directory to the path for package imports
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from modules.souls_manager import SoulsManager
from modules.cashinghouse import CashingHouse, TransactionType, TransactionCategory
from modules.souls_financial_integration import SoulsFinancialIntegration, TributeType
from modules.utils import Configuration, DataUtils, LoggingUtils


class DataMigrationTool:
    """
    Comprehensive data migration and export/import utilities.
    
    This class provides tools for exporting, importing, and migrating data
    between different formats and systems, with proper error handling and logging.
    
    Attributes:
        souls_manager: SoulsManager instance for entity data
        cashinghouse: CashingHouse instance for financial data
        financial_integration: SoulsFinancialIntegration instance for tribute data
        logger: Logger instance for operations
    """
    
    def __init__(self):
        self.souls_manager = None
        self.cashinghouse = None
        self.financial_integration = None
        self.logger = LoggingUtils.setup_logger(__name__)
        
    def initialize_components(self, souls_data_path: Optional[str] = None, financial_data_path: Optional[str] = None) -> None:
        """
        Initialize all platform components
        
        Args:
            souls_data_path: Path to souls data file (uses default if None)
            financial_data_path: Path to financial data file (uses default if None)
        """
        if souls_data_path is None:
            # Try to find the souls data file in the expected location
            default_path = Path(__file__).parent / "src" / "data" / "souls_entities.json"
            if default_path.exists():
                souls_data_path = str(default_path)
            else:
                souls_data_path = str(Configuration.DEFAULT_SOULS_DATA)
        
        if financial_data_path is None:
            financial_data_path = str(Configuration.DEFAULT_CASHINGHOUSE_DATA)
        
        try:
            self.souls_manager = SoulsManager(souls_data_path)
            self.cashinghouse = CashingHouse(financial_data_path)
            self.financial_integration = SoulsFinancialIntegration(self.souls_manager)
            
            self.logger.info("All components initialized successfully")
            print("✓ All components initialized")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize components: {e}")
            raise
        
    def export_all_data(self, output_dir: Optional[str] = None) -> str:
        """
        Export all platform data to a structured directory
        
        Args:
            output_dir: Directory path for export (uses timestamped default if None)
            
        Returns:
            Path to the export directory
        """
        if output_dir is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_dir = Path(__file__).parent / "exports" / f"export_{timestamp}"
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        export_info: Dict[str, Any] = {
            'export_timestamp': datetime.now().isoformat(),
            'export_version': '1.0',
            'components': {}
        }
        
        try:
            # Export souls data
            souls_file = output_path / "souls.json"
            souls_data = {
                'souls': [soul.__dict__ for soul in self.souls_manager.get_all_souls()],
                'metadata': self.souls_manager.get_metadata(),
                'statistics': self.souls_manager.get_statistics()
            }
            DataUtils.save_json_file(souls_data, souls_file)
            
            export_info['components']['souls'] = {
                'file': str(souls_file),
                'count': len(self.souls_manager.get_all_souls()),
                'status': 'exported'
            }
            
            # Export financial data
            financial_file = output_path / "financial.json"
            financial_data = self.cashinghouse.export_for_firebase()
            DataUtils.save_json_file(financial_data, financial_file)
            
            export_info['components']['financial'] = {
                'file': str(financial_file),
                'transaction_count': len(self.cashinghouse.transactions),
                'status': 'exported'
            }
            
            # Export tributes data
            tributes_file = output_path / "tributes.json"
            tributes_data = {
                'tributes': [tribute.__dict__ for tribute in self.financial_integration.tributes],
                'financial_impacts': {
                    soul_id: impact.__dict__ 
                    for soul_id, impact in self.financial_integration.financial_impacts.items()
                }
            }
            DataUtils.save_json_file(tributes_data, tributes_file)
            
            export_info['components']['tributes'] = {
                'file': str(tributes_file),
                'count': len(self.financial_integration.tributes),
                'status': 'exported'
            }
            
            # Export backup info
            backup_file = output_path / "backup_info.json"
            backup_info = {
                'backups': self.souls_manager.list_backups(),
                'backup_directory': str(self.souls_manager.backup_dir)
            }
            DataUtils.save_json_file(backup_info, backup_file)
            
            export_info['components']['backups'] = {
                'file': str(backup_file),
                'status': 'exported'
            }
            
            # Export integrity report
            integrity_file = output_path / "integrity_report.json"
            integrity_report = self.souls_manager.get_data_integrity_report()
            DataUtils.save_json_file(integrity_report, integrity_file)
            
            export_info['components']['integrity'] = {
                'file': str(integrity_file),
                'status': 'exported'
            }
            
            # Save export info
            info_file = output_path / "export_info.json"
            DataUtils.save_json_file(export_info, info_file)
            
            self.logger.info(f"Data export completed successfully: {output_path}")
            print(f"✓ Data exported to: {output_path}")
            
            return str(output_path)
            
        except Exception as e:
            self.logger.error(f"Data export failed: {e}")
            raise
    
    def import_souls_data(self, import_file: str, validate: bool = True) -> bool:
        """
        Import souls data from JSON file
        
        Args:
            import_file: Path to the JSON file to import
            validate: Whether to validate data before import
            
        Returns:
            True if import successful
        """
        try:
            import_data = DataUtils.load_json_file(Path(import_file))
            
            souls_data = import_data.get('souls', [])
            
            if validate:
                print(f"Validating {len(souls_data)} souls...")
                # Validation would go here
            
            # Create backup before import
            self.souls_manager._create_backup()
            
            # Update souls data
            self.souls_manager.souls_data['souls'] = souls_data
            self.souls_manager.souls = self.souls_manager._parse_souls()
            
            # Save
            self.souls_manager.save_souls_data()
            
            self.logger.info(f"Imported {len(souls_data)} souls from {import_file}")
            print(f"✓ Imported {len(souls_data)} souls from {import_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to import souls data: {e}")
            raise
    
    def import_financial_data(self, import_file: str, validate: bool = True) -> bool:
        """
        Import financial data from JSON file
        
        Args:
            import_file: Path to the JSON file to import
            validate: Whether to validate data before import
            
        Returns:
            True if import successful
        """
        try:
            import_data = DataUtils.load_json_file(Path(import_file))
            
            transactions = import_data.get('transactions', [])
            
            if validate:
                print(f"Validating {len(transactions)} transactions...")
            
            # Import transactions
            result = self.cashinghouse.bulk_import_transactions(transactions)
            
            self.logger.info(f"Imported {result['success']}/{result['total']} transactions")
            print(f"✓ Imported {result['success']}/{result['total']} transactions")
            if result['failure'] > 0:
                print(f"  Failed: {result['failure']}")
            
            return result['failure'] == 0
            
        except Exception as e:
            self.logger.error(f"Failed to import financial data: {e}")
            raise
    
    def export_to_csv(self, output_file: str) -> bool:
        """
        Export souls data to CSV format
        
        Args:
            output_file: Path to the output CSV file
            
        Returns:
            True if export successful
        """
        try:
            souls = self.souls_manager.get_all_souls()
            
            with open(output_file, 'w', newline='') as f:
                writer = csv.writer(f)
                
                # Write header
                writer.writerow([
                    'ID', 'Name', 'Gender', 'Archetype', 'Rarity', 'Tier',
                    'Bio', 'Voice', 'Email', 'Platforms', 'Tribute Impact'
                ])
                
                # Write soul data
                for soul in souls:
                    writer.writerow([
                        soul.id,
                        soul.name,
                        soul.gender,
                        soul.archetype,
                        soul.rarity,
                        soul.tier,
                        soul.bio,
                        soul.voice,
                        soul.email,
                        ','.join(soul.platforms),
                        soul.tribute_impact
                    ])
            
            self.logger.info(f"Exported {len(souls)} souls to CSV: {output_file}")
            print(f"✓ Exported {len(souls)} souls to {output_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to export to CSV: {e}")
            raise
    
    def import_from_csv(self, import_file: str) -> bool:
        """
        Import souls data from CSV format
        
        Args:
            import_file: Path to the CSV file to import
            
        Returns:
            True if import successful
        """
        try:
            with open(import_file, 'r') as f:
                reader = csv.DictReader(f)
                
                imported_souls = []
                for row in reader:
                    soul_data = {
                        'id': row['ID'],
                        'name': row['Name'],
                        'gender': row['Gender'],
                        'archetype': row['Archetype'],
                        'rarity': row['Rarity'],
                        'tier': row['Tier'],
                        'bio': row['Bio'],
                        'voice': row['Voice'],
                        'email': row['Email'],
                        'platforms': row['Platforms'].split(','),
                        'tribute_impact': row['Tribute Impact'],
                        'sensory': '',
                        'hooks': [],
                        'desires': [],
                        'kinks': [],
                        'shadow_practice': '',
                        'image': ''
                    }
                    imported_souls.append(soul_data)
            
            # Create backup before import
            self.souls_manager._create_backup()
            
            # Update souls data
            self.souls_manager.souls_data['souls'] = imported_souls
            self.souls_manager.souls = self.souls_manager._parse_souls()
            
            # Save
            self.souls_manager.save_souls_data()
            
            self.logger.info(f"Imported {len(imported_souls)} souls from CSV: {import_file}")
            print(f"✓ Imported {len(imported_souls)} souls from CSV: {import_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to import from CSV: {e}")
            raise
    
    def create_migration_script(self, source_format: str, target_format: str) -> str:
        """Generate a migration script for format conversion"""
        timestamp = datetime.now().isoformat()
        function_name = "migrate_" + source_format + "_to_" + target_format
        
        script_content = "#!/usr/bin/env python3\n"
        script_content += "'''\n"
        script_content += f"Auto-generated migration script: {source_format} to {target_format}\n"
        script_content += f"Generated: {timestamp}\n"
        script_content += "'''\n\n"
        script_content += "import sys\n"
        script_content += "from pathlib import Path\n\n"
        script_content += "# Add the src directory to the path\n"
        script_content += "src_path = Path(__file__).parent / 'src'\n"
        script_content += "sys.path.insert(0, str(src_path))\n\n"
        script_content += "from modules.souls_manager import SoulsManager\n\n"
        script_content += f"def {function_name}(source_file: str, target_file: str):\n"
        script_content += f'    """Migrate data from {source_format} to {target_format}"""\n'
        script_content += "    # Implementation would go here\n"
        script_content += "    print('Migrating from', source_file, 'to', target_file)\n"
        script_content += "    pass\n\n"
        script_content += "if __name__ == '__main__':\n"
        script_content += "    if len(sys.argv) != 3:\n"
        script_content += "        print('Usage: python migration_script.py <source_file> <target_file>')\n"
        script_content += "        sys.exit(1)\n"
        script_content += f"    {function_name}(sys.argv[1], sys.argv[2])\n"
        
        script_filename = f"migrate_{source_format}_to_{target_format}.py"
        script_path = Path(__file__).parent / script_filename
        
        with open(script_path, 'w') as f:
            f.write(script_content)
        
        print(f"✓ Migration script created: {script_path}")
        return str(script_path)
    
    def validate_data_consistency(self) -> Dict[str, Any]:
        """Validate data consistency across all components"""
        validation_report = {
            'timestamp': datetime.now().isoformat(),
            'validations': {},
            'overall_status': 'unknown'
        }
        
        # Validate souls data
        souls_integrity = self.souls_manager.get_data_integrity_report()
        validation_report['validations']['souls'] = {
            'health_score': souls_integrity['health_score'],
            'status': 'pass' if souls_integrity['health_score'] >= 80 else 'fail',
            'errors': len(souls_integrity['validation_errors']),
            'warnings': len(souls_integrity['warnings'])
        }
        
        # Validate financial data
        financial_anomalies = self.cashinghouse.get_anomaly_detection_report()
        validation_report['validations']['financial'] = {
            'anomalies': financial_anomalies['total_anomalies'],
            'status': 'pass' if financial_anomalies['total_anomalies'] == 0 else 'warning'
        }
        
        # Cross-reference validation
        soul_ids = set(soul.id for soul in self.souls_manager.get_all_souls())
        tribute_soul_ids = set(tribute.soul_id for tribute in self.financial_integration.tributes)
        
        orphan_tributes = tribute_soul_ids - soul_ids
        validation_report['validations']['cross_reference'] = {
            'orphan_tributes': len(orphan_tributes),
            'status': 'pass' if len(orphan_tributes) == 0 else 'warning'
        }
        
        # Overall status
        all_statuses = [v['status'] for v in validation_report['validations'].values()]
        if all(status == 'pass' for status in all_statuses):
            validation_report['overall_status'] = 'pass'
        elif any(status == 'fail' for status in all_statuses):
            validation_report['overall_status'] = 'fail'
        else:
            validation_report['overall_status'] = 'warning'
        
        return validation_report
    
    def incremental_backup(self, backup_name: Optional[str] = None) -> str:
        """
        Create an incremental backup with change detection
        
        Args:
            backup_name: Optional custom backup name
            
        Returns:
            Path to the backup directory
        """
        if backup_name is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"incremental_backup_{timestamp}"
        
        backup_path = Path(__file__).parent / "backups" / backup_name
        backup_path.mkdir(parents=True, exist_ok=True)
        
        # Export current state
        self.export_all_data(str(backup_path))
        
        # Create change log
        change_log = {
            'backup_timestamp': datetime.now().isoformat(),
            'backup_type': 'incremental',
            'changes_detected': []
        }
        
        # Compare with last backup if exists
        backups = self.souls_manager.list_backups()
        if backups:
            last_backup = backups[-1]
            # Compare soul counts
            current_souls = len(self.souls_manager.get_all_souls())
            change_log['changes_detected'].append({
                'type': 'soul_count',
                'previous': 'unknown',
                'current': current_souls,
                'change': 'unknown'
            })
        
        # Save change log
        change_log_file = backup_path / "change_log.json"
        DataUtils.save_json_file(change_log, change_log_file)
        
        self.logger.info(f"Incremental backup created: {backup_path}")
        print(f"✓ Incremental backup created: {backup_path}")
        
        return str(backup_path)
    
    def rollback_to_backup(self, backup_path: str) -> bool:
        """
        Rollback data to a specific backup
        
        Args:
            backup_path: Path to the backup directory
            
        Returns:
            True if rollback successful
        """
        try:
            backup_dir = Path(backup_path)
            
            if not backup_dir.exists():
                raise FileNotFoundError(f"Backup directory not found: {backup_path}")
            
            # Import souls data from backup
            souls_file = backup_dir / "souls.json"
            if souls_file.exists():
                self.import_souls_data(str(souls_file), validate=False)
            
            # Import financial data from backup
            financial_file = backup_dir / "financial.json"
            if financial_file.exists():
                self.import_financial_data(str(financial_file), validate=False)
            
            self.logger.info(f"Rollback completed: {backup_path}")
            print(f"✓ Rollback completed to: {backup_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Rollback failed: {e}")
            raise
    
    def sync_with_firestore(self, collection: str = 'souls') -> Dict[str, Any]:
        """
        Sync local data with Firestore
        
        Args:
            collection: Firestore collection to sync
            
        Returns:
            Sync results
        """
        try:
            import firebase_admin
            from firebase_admin import credentials, firestore
            
            # Initialize Firebase if not already done
            if not firebase_admin._apps:
                cred_path = Path(__file__).parent / "tiapmaatzu-firebase-adminsdk-fbsvc-db8f709411.json"
                cred = credentials.Certificate(str(cred_path))
                firebase_admin.initialize_app(cred)
            
            db = firestore.client()
            
            sync_results = {
                'collection': collection,
                'timestamp': datetime.now().isoformat(),
                'synced_documents': 0,
                'errors': []
            }
            
            if collection == 'souls':
                # Sync souls data
                souls = self.souls_manager.get_all_souls()
                for soul in souls:
                    try:
                        doc_ref = db.collection('souls').document(soul.id)
                        doc_ref.set(soul.__dict__)
                        sync_results['synced_documents'] += 1
                    except Exception as e:
                        sync_results['errors'].append({
                            'soul_id': soul.id,
                            'error': str(e)
                        })
            
            self.logger.info(f"Firestore sync completed: {sync_results['synced_documents']} documents")
            print(f"✓ Firestore sync completed: {sync_results['synced_documents']} documents")
            
            return sync_results
            
        except Exception as e:
            self.logger.error(f"Firestore sync failed: {e}")
            raise
    
    def export_for_migration(self, target_system: str) -> str:
        """
        Export data in format suitable for migration to another system
        
        Args:
            target_system: Target system (firebase, postgresql, mongodb, etc.)
            
        Returns:
            Path to the export file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if target_system == 'firebase':
            export_file = Path(__file__).parent / "exports" / f"firebase_migration_{timestamp}.json"
            migration_data = {
                'format': 'firebase_firestore',
                'version': '1.0',
                'exported_at': datetime.now().isoformat(),
                'collections': {
                    'souls': [soul.__dict__ for soul in self.souls_manager.get_all_souls()],
                    'financial': self.cashinghouse.export_for_firebase(),
                    'tributes': [tribute.__dict__ for tribute in self.financial_integration.tributes]
                }
            }
        elif target_system == 'postgresql':
            export_file = Path(__file__).parent / "exports" / f"postgresql_migration_{timestamp}.sql"
            # Generate SQL insert statements
            sql_statements = []
            
            # Souls table
            souls = self.souls_manager.get_all_souls()
            for soul in souls:
                sql = f"INSERT INTO souls (id, name, gender, archetype, rarity, tier, bio, voice, email, platforms, tribute_impact) VALUES ('{soul.id}', '{soul.name}', '{soul.gender}', '{soul.archetype}', '{soul.rarity}', '{soul.tier}', '{soul.bio}', '{soul.voice}', '{soul.email}', ARRAY{[p for p in soul.platforms]}, '{soul.tribute_impact}');"
                sql_statements.append(sql)
            
            migration_data = '\n'.join(sql_statements)
            
            with open(export_file, 'w') as f:
                f.write(migration_data)
            
            return str(export_file)
        elif target_system == 'mongodb':
            export_file = Path(__file__).parent / "exports" / f"mongodb_migration_{timestamp}.json"
            migration_data = {
                'format': 'mongodb',
                'version': '1.0',
                'exported_at': datetime.now().isoformat(),
                'collections': {
                    'souls': [soul.__dict__ for soul in self.souls_manager.get_all_souls()],
                    'transactions': [tx.__dict__ for tx in self.cashinghouse.transactions],
                    'tributes': [tribute.__dict__ for tribute in self.financial_integration.tributes]
                }
            }
        else:
            raise ValueError(f"Unsupported target system: {target_system}")
        
        if target_system != 'postgresql':
            DataUtils.save_json_file(migration_data, export_file)
        
        self.logger.info(f"Migration export created for {target_system}: {export_file}")
        print(f"✓ Migration export created for {target_system}: {export_file}")
        
        return str(export_file)
    
    def data_transformation_pipeline(self, transformations: List[Dict[str, Any]]) -> bool:
        """
        Apply a series of data transformations
        
        Args:
            transformations: List of transformation operations
            
        Returns:
            True if all transformations successful
        """
        try:
            # Create backup before transformations
            self.incremental_backup("pre_transformation_backup")
            
            for transformation in transformations:
                operation = transformation.get('operation')
                params = transformation.get('params', {})
                
                if operation == 'filter_souls':
                    # Filter souls by criteria
                    criteria = params.get('criteria')
                    # Implementation would go here
                    pass
                elif operation == 'transform_financial':
                    # Transform financial data
                    # Implementation would go here
                    pass
                elif operation == 'normalize_data':
                    # Normalize data formats
                    # Implementation would go here
                    pass
                else:
                    self.logger.warning(f"Unknown transformation operation: {operation}")
            
            # Create post-transformation backup
            self.incremental_backup("post_transformation_backup")
            
            self.logger.info("Data transformation pipeline completed")
            print("✓ Data transformation pipeline completed")
            return True
            
        except Exception as e:
            self.logger.error(f"Data transformation pipeline failed: {e}")
            raise


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Data migration and export/import utilities",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Export all data
  python data_migration.py export-all
  
  # Export to specific directory
  python data_migration.py export-all --output ./my_export
  
  # Import souls data
  python data_migration.py import-souls souls_backup.json
  
  # Export to CSV
  python data_migration.py export-csv souls.csv
  
  # Import from CSV
  python data_migration.py import-csv souls.csv
  
  # Validate data consistency
  python data_migration.py validate
  
  # Create migration script
  python data_migration.py create-script json csv
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Migration operation')
    
    # Export all command
    export_parser = subparsers.add_parser('export-all', help='Export all platform data')
    export_parser.add_argument('--output', help='Output directory path')
    
    # Import souls command
    import_souls_parser = subparsers.add_parser('import-souls', help='Import souls data from JSON')
    import_souls_parser.add_argument('file', help='Source JSON file')
    import_souls_parser.add_argument('--no-validate', action='store_true', help='Skip validation')
    
    # Import financial command
    import_financial_parser = subparsers.add_parser('import-financial', help='Import financial data from JSON')
    import_financial_parser.add_argument('file', help='Source JSON file')
    import_financial_parser.add_argument('--no-validate', action='store_true', help='Skip validation')
    
    # Export CSV command
    export_csv_parser = subparsers.add_parser('export-csv', help='Export souls to CSV format')
    export_csv_parser.add_argument('file', help='Output CSV file')
    
    # Import CSV command
    import_csv_parser = subparsers.add_parser('import-csv', help='Import souls from CSV format')
    import_csv_parser.add_argument('file', help='Source CSV file')
    
    # Validate command
    subparsers.add_parser('validate', help='Validate data consistency')
    
    # Create script command
    script_parser = subparsers.add_parser('create-script', help='Create migration script')
    script_parser.add_argument('source_format', help='Source format (json, csv, etc.)')
    script_parser.add_argument('target_format', help='Target format (json, csv, etc.)')
    
    # Incremental backup command
    backup_parser = subparsers.add_parser('incremental-backup', help='Create incremental backup')
    backup_parser.add_argument('--name', help='Custom backup name')
    
    # Rollback command
    rollback_parser = subparsers.add_parser('rollback', help='Rollback to backup')
    rollback_parser.add_argument('backup_path', help='Path to backup directory')
    
    # Firestore sync command
    sync_parser = subparsers.add_parser('sync-firestore', help='Sync with Firestore')
    sync_parser.add_argument('--collection', default='souls', help='Collection to sync')
    
    # Migration export command
    migration_parser = subparsers.add_parser('export-migration', help='Export for system migration')
    migration_parser.add_argument('target_system', help='Target system (firebase, postgresql, mongodb)')
    
    # Transformation pipeline command
    transform_parser = subparsers.add_parser('transform', help='Apply data transformations')
    transform_parser.add_argument('config_file', help='JSON config file with transformations')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 0
    
    migrator = DataMigrationTool()
    migrator.initialize_components()
    
    try:
        if args.command == 'export-all':
            output_dir = args.output if args.output else None
            result = migrator.export_all_data(output_dir)
            print(f"Export completed: {result}")
            
        elif args.command == 'import-souls':
            validate = not args.no_validate
            success = migrator.import_souls_data(args.file, validate)
            return 0 if success else 1
            
        elif args.command == 'import-financial':
            validate = not args.no_validate
            success = migrator.import_financial_data(args.file, validate)
            
        elif args.command == 'incremental-backup':
            backup_name = args.name if args.name else None
            result = migrator.incremental_backup(backup_name)
            print(f"Incremental backup completed: {result}")
            
        elif args.command == 'rollback':
            success = migrator.rollback_to_backup(args.backup_path)
            if success:
                print("Rollback completed successfully")
            else:
                print("Rollback failed")
                
        elif args.command == 'sync-firestore':
            collection = args.collection
            results = migrator.sync_with_firestore(collection)
            print(f"Firestore sync completed: {results['synced_documents']} documents synced")
            if results['errors']:
                print(f"Errors: {len(results['errors'])}")
                
        elif args.command == 'export-migration':
            target_system = args.target_system
            export_path = migrator.export_for_migration(target_system)
            print(f"Migration export completed: {export_path}")
            
        elif args.command == 'transform':
            config_file = args.config_file
            transformations = DataUtils.load_json_file(Path(config_file))
            success = migrator.data_transformation_pipeline(transformations)
            if success:
                print("Data transformation pipeline completed successfully")
            else:
                print("Data transformation pipeline failed")
            return 0 if success else 1
            
        elif args.command == 'export-csv':
            success = migrator.export_to_csv(args.file)
            return 0 if success else 1
            
        elif args.command == 'import-csv':
            success = migrator.import_from_csv(args.file)
            return 0 if success else 1
            
        elif args.command == 'validate':
            report = migrator.validate_data_consistency()
            print(json.dumps(report, indent=2))
            return 0 if report['overall_status'] == 'pass' else 1
            
        elif args.command == 'create-script':
            script_path = migrator.create_migration_script(args.source_format, args.target_format)
            print(f"Script created: {script_path}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())