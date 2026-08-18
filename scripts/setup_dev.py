#!/usr/bin/env python3
"""
Development Setup Script
Automated setup for Tiapma'atzu platform development environment
"""

import sys
import subprocess
import json
from pathlib import Path
from typing import List, Dict, Any


class DevSetup:
    """Automated development environment setup"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.venv_path = self.project_root / "venv"
        self.requirements_file = self.project_root / "requirements.txt"
        self.setup_status = {
            'python_version': False,
            'virtual_env': False,
            'dependencies': False,
            'directories': False,
            'configuration': False
        }
        
    def check_python_version(self) -> bool:
        """Check if Python version is compatible"""
        print("Checking Python version...")
        version = sys.version_info
        if version.major == 3 and version.minor >= 8:
            print(f"✓ Python {version.major}.{version.minor}.{version.micro} is compatible")
            self.setup_status['python_version'] = True
            return True
        else:
            print(f"✗ Python {version.major}.{version.minor}.{version.micro} is not compatible (requires 3.8+)")
            return False
            
    def create_virtual_environment(self) -> bool:
        """Create Python virtual environment"""
        print("Creating virtual environment...")
        
        if self.venv_path.exists():
            print("✓ Virtual environment already exists")
            self.setup_status['virtual_env'] = True
            return True
            
        try:
            subprocess.run([sys.executable, "-m", "venv", str(self.venv_path)], check=True)
            print(f"✓ Virtual environment created at {self.venv_path}")
            self.setup_status['virtual_env'] = True
            return True
        except subprocess.CalledProcessError as e:
            print(f"✗ Failed to create virtual environment: {e}")
            return False
            
    def install_dependencies(self) -> bool:
        """Install Python dependencies"""
        print("Installing dependencies...")
        
        if not self.venv_path.exists():
            print("✗ Virtual environment not found")
            return False
            
        pip_path = self.venv_path / "bin" / "pip"
        if not pip_path.exists():
            pip_path = self.venv_path / "Scripts" / "pip.exe"
            
        if not pip_path.exists():
            print("✗ Pip not found in virtual environment")
            return False
            
        try:
            # Create requirements.txt if it doesn't exist
            if not self.requirements_file.exists():
                self.create_requirements_file()
                
            subprocess.run([str(pip_path), "install", "-r", str(self.requirements_file)], check=True)
            print("✓ Dependencies installed successfully")
            self.setup_status['dependencies'] = True
            return True
        except subprocess.CalledProcessError as e:
            print(f"✗ Failed to install dependencies: {e}")
            return False
            
    def create_requirements_file(self):
        """Create requirements.txt file"""
        requirements = [
            "firebase-admin==6.3.0",
            "python-dateutil==2.8.2"
        ]
        
        with open(self.requirements_file, 'w') as f:
            f.write("\n".join(requirements))
            
        print(f"✓ Created requirements.txt")
        
    def create_directory_structure(self) -> bool:
        """Create necessary directory structure"""
        print("Creating directory structure...")
        
        directories = [
            self.project_root / "logs",
            self.project_root / "data",
            self.project_root / "exports",
            self.project_root / "src" / "data" / "backups"
        ]
        
        try:
            for directory in directories:
                directory.mkdir(parents=True, exist_ok=True)
                
            print("✓ Directory structure created")
            self.setup_status['directories'] = True
            return True
        except Exception as e:
            print(f"✗ Failed to create directories: {e}")
            return False
            
    def create_configuration_files(self) -> bool:
        """Create configuration files"""
        print("Creating configuration files...")
        
        try:
            # Create .env file
            env_file = self.project_root / ".env"
            if not env_file.exists():
                env_content = """# Tiapma'atzu Platform Environment Configuration
# Copy this file to .env and fill in your values

# Firebase Configuration
FIREBASE_PROJECT_ID=tiapmaatzu
FIREBASE_SERVICE_ACCOUNT_PATH=tiapmaatzu-firebase-adminsdk-fbsvc-db8f709411.json

# Application Settings
LOG_LEVEL=INFO
ENABLE_BACKUPS=true
BACKUP_RETENTION_DAYS=30

# Development Settings
DEBUG=false
TESTING=false
"""
                with open(env_file, 'w') as f:
                    f.write(env_content)
                print("✓ Created .env file")
                
            # Create .gitignore updates
            gitignore_file = self.project_root / ".gitignore"
            gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/

# Logs
logs/
*.log

# Data
data/
exports/
*.json
*.csv

# Environment
.env
.env.local

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Firebase
*-firebase-adminsdk-*.json
"""
            
            with open(gitignore_file, 'w') as f:
                f.write(gitignore_content)
            print("✓ Created .gitignore file")
            
            self.setup_status['configuration'] = True
            return True
            
        except Exception as e:
            print(f"✗ Failed to create configuration files: {e}")
            return False
            
    def create_development_scripts(self) -> bool:
        """Create development helper scripts"""
        print("Creating development scripts...")
        
        try:
            # Create activation script for Unix
            activate_unix = self.project_root / "activate_dev.sh"
            with open(activate_unix, 'w') as f:
                f.write("#!/bin/bash\n")
                f.write(f"source {self.venv_path}/bin/activate\n")
                f.write("export PYTHONPATH=\"$PYTHONPATH:$(pwd)/src\"\n")
                f.write("echo 'Development environment activated'\n")
            activate_unix.chmod(0o755)
            print("✓ Created activate_dev.sh")
            
            # Create activation script for Windows
            activate_windows = self.project_root / "activate_dev.bat"
            with open(activate_windows, 'w') as f:
                f.write(f"call {self.venv_path}\\Scripts\\activate.bat\n")
                f.write("set PYTHONPATH=%PYTHONPATH%;%CD%\\src\n")
                f.write("echo Development environment activated\n")
            print("✓ Created activate_dev.bat")
            
            # Create run script
            run_script = self.project_root / "run_dev.py"
            with open(run_script, 'w') as f:
                f.write("#!/usr/bin/env python3\n")
                f.write("import sys\n")
                f.write("from pathlib import Path\n")
                f.write("sys.path.insert(0, str(Path(__file__).parent / 'src'))\n")
                f.write("\n")
                f.write("# Import and run your application\n")
                f.write("print('Development environment ready')\n")
            print("✓ Created run_dev.py")
            
            return True
            
        except Exception as e:
            print(f"✗ Failed to create development scripts: {e}")
            return False
            
    def run_integration_tests(self) -> bool:
        """Run integration tests to verify setup"""
        print("Running integration tests...")
        
        try:
            test_script = self.project_root / "test_integration.py"
            if test_script.exists():
                result = subprocess.run([sys.executable, str(test_script)], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    print("✓ Integration tests passed")
                    return True
                else:
                    print("✗ Integration tests failed")
                    print(result.stdout)
                    print(result.stderr)
                    return False
            else:
                print("⚠ Integration test script not found")
                return True  # Not a failure, just missing
        except Exception as e:
            print(f"✗ Failed to run integration tests: {e}")
            return False
            
    def generate_setup_report(self) -> Dict[str, Any]:
        """Generate setup completion report"""
        total_items = len(self.setup_status)
        completed_items = sum(1 for status in self.setup_status.values() if status)
        
        report = {
            'timestamp': str(Path.cwd()),
            'success_rate': completed_items / total_items if total_items > 0 else 0,
            'total_items': total_items,
            'completed_items': completed_items,
            'status': 'complete' if completed_items == total_items else 'partial',
            'details': self.setup_status
        }
        
        return report
        
    def print_setup_report(self):
        """Print setup completion report"""
        report = self.generate_setup_report()
        
        print("\n" + "="*60)
        print("SETUP REPORT")
        print("="*60)
        print(f"Status: {report['status'].upper()}")
        print(f"Completion: {report['completed_items']}/{report['total_items']} ({report['success_rate']*100:.0f}%)")
        print("\nDetails:")
        
        for item, status in report['details'].items():
            symbol = "✓" if status else "✗"
            print(f"  {symbol} {item.replace('_', ' ').title()}")
            
        if report['status'] == 'complete':
            print("\n🎉 Development environment setup complete!")
            print("\nNext steps:")
            print("1. Activate the environment:")
            print("   Unix: source activate_dev.sh")
            print("   Windows: activate_dev.bat")
            print("2. Run your application: python run_dev.py")
        else:
            print("\n⚠ Setup incomplete. Please fix the failed items above.")
            
    def run_setup(self):
        """Run complete setup process"""
        print("="*60)
        print("Tiapma'atzu Platform - Development Environment Setup")
        print("="*60)
        print()
        
        # Run setup steps
        self.check_python_version()
        self.create_virtual_environment()
        self.install_dependencies()
        self.create_directory_structure()
        self.create_configuration_files()
        self.create_development_scripts()
        
        # Run tests if dependencies are installed
        if self.setup_status['dependencies']:
            self.run_integration_tests()
            
        # Print report
        self.print_setup_report()
        
        # Save report
        report = self.generate_setup_report()
        report_file = self.project_root / "setup_report.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"\nSetup report saved to: {report_file}")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Set up development environment for Tiapma'atzu platform")
    parser.add_argument('--skip-tests', action='store_true', help='Skip integration tests')
    parser.add_argument('--quick', action='store_true', help='Quick setup (minimal checks)')
    
    args = parser.parse_args()
    
    setup = DevSetup()
    
    if args.quick:
        print("Running quick setup...")
        setup.create_directory_structure()
        setup.create_configuration_files()
        setup.create_development_scripts()
        print("✓ Quick setup complete")
    else:
        setup.run_setup()


if __name__ == "__main__":
    main()