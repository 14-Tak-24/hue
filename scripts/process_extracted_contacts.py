"""
Process Extracted iPhone Backup Contacts for Community Building
Automates contact categorization and organization for outreach
"""

import json
import csv
import os
from pathlib import Path
from typing import Dict, List, Set
from datetime import datetime

class ContactProcessor:
    """Process extracted contacts for community building"""
    
    def __init__(self):
        self.base_path = Path("scripts/iphone_backup_data")
        self.contacts_dir = self.base_path / "contacts"
        self.categorization_file = self.contacts_dir / "contact_categorization.json"
        self.template_file = self.contacts_dir / "import_template.json"
        self.categories = self.load_categories()
        
    def load_categories(self) -> Dict:
        """Load contact categories"""
        if self.categorization_file.exists():
            with open(self.categorization_file, 'r') as f:
                return json.load(f)
        return {}
    
    def parse_vcard(self, vcard_path: Path) -> Dict:
        """Parse a single vCard file"""
        contact = {
            'name': '',
            'phone': '',
            'email': '',
            'notes': '',
            'category': 'uncategorized',
            'platform': '',
            'archetype_interest': ''
        }
        
        try:
            with open(vcard_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Extract basic information
            for line in content.split('\n'):
                line = line.strip()
                if line.startswith('FN:'):
                    contact['name'] = line[3:].strip()
                elif line.startswith('TEL;'):
                    contact['phone'] = line.split(':')[-1].strip()
                elif line.startswith('EMAIL;'):
                    contact['email'] = line.split(':')[-1].strip()
                elif line.startswith('NOTE:'):
                    contact['notes'] = line[5:].strip()
                    
        except Exception as e:
            print(f"Error parsing {vcard_path.name}: {e}")
            
        return contact
    
    def import_from_vcards(self):
        """Import contacts from vCard files"""
        print("\n" + "=" * 60)
        print("Importing Contacts from vCard Files")
        print("=" * 60)
        
        vcard_files = list(self.contacts_dir.glob('*.vcf')) + list(self.contacts_dir.glob('*.vcard'))
        
        if not vcard_files:
            print("No vCard files found in contacts directory.")
            print("Please export contacts from iPhone Backup Extractor first.")
            return []
        
        print(f"Found {len(vcard_files)} vCard files")
        
        contacts = []
        for vcard_file in vcard_files:
            contact = self.parse_vcard(vcard_file)
            if contact['name']:  # Only add if we have a name
                contacts.append(contact)
                print(f"✓ Imported: {contact['name']}")
        
        print(f"\n✓ Imported {len(contacts)} contacts")
        return contacts
    
    def import_from_csv(self, csv_path: Path) -> List[Dict]:
        """Import contacts from CSV file"""
        print("\n" + "=" * 60)
        print("Importing Contacts from CSV")
        print("=" * 60)
        
        contacts = []
        
        try:
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    contact = {
                        'name': row.get('Name', row.get('name', '')),
                        'phone': row.get('Phone', row.get('phone', row.get('Phone Number', ''))),
                        'email': row.get('Email', row.get('email', row.get('Email Address', ''))),
                        'notes': row.get('Notes', row.get('notes', '')),
                        'category': 'uncategorized',
                        'platform': '',
                        'archetype_interest': ''
                    }
                    if contact['name']:
                        contacts.append(contact)
                        print(f"✓ Imported: {contact['name']}")
        
        except Exception as e:
            print(f"Error reading CSV: {e}")
        
        print(f"\n✓ Imported {len(contacts)} contacts")
        return contacts
    
    def auto_categorize_contacts(self, contacts: List[Dict]) -> List[Dict]:
        """Automatically categorize contacts based on keywords in notes/names"""
        print("\n" + "=" * 60)
        print("Auto-Categorizing Contacts")
        print("=" * 60)
        
        category_keywords = {
            'potential_members': [
                'spiritual', 'meditation', 'yoga', 'growth', 'healing',
                'kink', 'fetish', 'bdsm', 'alternative', 'community',
                'interested', 'curious', 'exploring'
            ],
            'current_members': [
                'discord', 'twitter', 'member', 'hue', 'terry',
                'joined', 'participating', 'active'
            ],
            'collaborators': [
                'creator', 'artist', 'teacher', 'leader', 'influencer',
                'collaborate', 'partner', 'content', 'writer', 'musician'
            ],
            'influencers': [
                'influencer', 'followers', 'youtube', 'tiktok', 'instagram',
                'twitter', 'viral', 'popular', 'verified'
            ]
        }
        
        categorized_count = 0
        for contact in contacts:
            text_to_search = f"{contact['name']} {contact['notes']}".lower()
            
            for category, keywords in category_keywords.items():
                if any(keyword in text_to_search for keyword in keywords):
                    contact['category'] = category
                    categorized_count += 1
                    print(f"✓ Categorized: {contact['name']} → {category}")
                    break
        
        print(f"\n✓ Auto-categorized {categorized_count} contacts")
        return contacts
    
    def create_categorization_csv(self, contacts: List[Dict]):
        """Create a CSV file for manual categorization review"""
        print("\n" + "=" * 60)
        print("Creating Categorization CSV")
        print("=" * 60)
        
        csv_path = self.contacts_dir / 'contacts_for_review.csv'
        
        fieldnames = ['name', 'phone', 'email', 'notes', 'category', 'platform', 'archetype_interest']
        
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(contacts)
        
        print(f"✓ Created CSV for review: {csv_path}")
        print(f"  Total contacts: {len(contacts)}")
        print(f"\nPlease review and update categories in the CSV file.")
        print(f"Categories: {', '.join(self.categories.keys())}")
    
    def load_categorized_contacts(self) -> List[Dict]:
        """Load contacts from reviewed CSV file"""
        print("\n" + "=" * 60)
        print("Loading Categorized Contacts")
        print("=" * 60)
        
        csv_path = self.contacts_dir / 'contacts_for_review.csv'
        
        if not csv_path.exists():
            print("CSV file not found. Please complete categorization first.")
            return []
        
        contacts = []
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                contacts.append(dict(row))
        
        print(f"✓ Loaded {len(contacts)} categorized contacts")
        return contacts
    
    def organize_by_category(self, contacts: List[Dict]):
        """Organize contacts into category-specific files"""
        print("\n" + "=" * 60)
        print("Organizing Contacts by Category")
        print("=" * 60)
        
        # Create category directories
        for category in self.categories.keys():
            category_dir = self.contacts_dir / category
            category_dir.mkdir(exist_ok=True)
        
        # Organize contacts
        category_counts = {}
        for contact in contacts:
            category = contact.get('category', 'uncategorized')
            
            if category not in self.categories:
                category = 'uncategorized'
            
            category_counts[category] = category_counts.get(category, 0) + 1
            
            # Save to category-specific JSON
            category_file = self.contacts_dir / category / f"{category}_contacts.json"
            
            existing_contacts = []
            if category_file.exists():
                with open(category_file, 'r') as f:
                    existing_contacts = json.load(f)
            
            existing_contacts.append(contact)
            
            with open(category_file, 'w') as f:
                json.dump(existing_contacts, f, indent=2)
        
        print("\n✓ Contacts organized by category:")
        for category, count in category_counts.items():
            print(f"  {category}: {count} contacts")
    
    def generate_outreach_lists(self, contacts: List[Dict]):
        """Generate outreach lists for community building"""
        print("\n" + "=" * 60)
        print("Generating Outreach Lists")
        print("=" * 60)
        
        outreach_lists = {
            'immediate_outreach': {
                'description': 'Contacts for immediate community outreach',
                'contacts': []
            },
            'collaboration_opportunities': {
                'description': 'Potential collaborators and partners',
                'contacts': []
            },
            'influencer_outreach': {
                'description': 'Influencers for amplification',
                'contacts': []
            }
        }
        
        for contact in contacts:
            category = contact.get('category', '')
            
            if category == 'potential_members':
                outreach_lists['immediate_outreach']['contacts'].append(contact)
            elif category == 'collaborators':
                outreach_lists['collaboration_opportunities']['contacts'].append(contact)
            elif category == 'influencers':
                outreach_lists['influencer_outreach']['contacts'].append(contact)
        
        # Save outreach lists
        for list_name, list_data in outreach_lists.items():
            list_file = self.contacts_dir / f"{list_name}.json"
            with open(list_file, 'w') as f:
                json.dump(list_data, f, indent=2)
            print(f"✓ Created: {list_name} ({len(list_data['contacts'])} contacts)")
    
    def create_processing_report(self, contacts: List[Dict]):
        """Create a contact processing report"""
        print("\n" + "=" * 60)
        print("Creating Contact Processing Report")
        print("=" * 60)
        
        category_counts = {}
        for contact in contacts:
            category = contact.get('category', 'uncategorized')
            category_counts[category] = category_counts.get(category, 0) + 1
        
        report = {
            'processing_summary': {
                'total_contacts': len(contacts),
                'categories_used': list(category_counts.keys()),
                'processed_at': datetime.now().isoformat()
            },
            'category_breakdown': category_counts,
            'next_steps': [
                'Review contacts_for_review.csv for accuracy',
                'Update categories and platform information',
                'Use organized contact lists for outreach',
                'Integrate with social media setup'
            ]
        }
        
        report_file = self.contacts_dir / 'contact_processing_report.json'
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n✓ Report saved: {report_file}")
        print(f"\nSummary:")
        print(f"  Total contacts: {report['processing_summary']['total_contacts']}")
        print(f"  Categories: {', '.join(report['processing_summary']['categories_used'])}")
    
    def run_full_processing(self):
        """Run complete contact processing workflow"""
        print("=" * 60)
        print("iPhone Backup Contact Processing Workflow")
        print("=" * 60)
        
        # Step 1: Import contacts
        contacts = self.import_from_vcards()
        
        if not contacts:
            # Try CSV import if no vCards found
            csv_files = list(self.contacts_dir.glob('*.csv'))
            if csv_files:
                contacts = self.import_from_csv(csv_files[0])
        
        if not contacts:
            print("\nNo contacts found to process.")
            print("Please export contacts from iPhone Backup Extractor to:")
            print(f"  {self.contacts_dir}")
            return
        
        # Step 2: Auto-categorize
        contacts = self.auto_categorize_contacts(contacts)
        
        # Step 3: Create review CSV
        self.create_categorization_csv(contacts)
        
        print("\n" + "=" * 60)
        print("Contact Import Complete - Manual Review Required")
        print("=" * 60)
        print(f"\nPlease review and update the categorization in:")
        print(f"  {self.contacts_dir}/contacts_for_review.csv")
        print(f"\nAfter review, run the organization step with:")
        print(f"  python scripts/process_extracted_contacts.py --organize")

def main():
    """Main function"""
    import sys
    
    print("iPhone Backup Contact Processor")
    print("This script will process extracted contacts for community building\n")
    
    processor = ContactProcessor()
    
    if len(sys.argv) > 1 and sys.argv[1] == '--organize':
        # Organization mode - load reviewed contacts and organize
        contacts = processor.load_categorized_contacts()
        if contacts:
            processor.organize_by_category(contacts)
            processor.generate_outreach_lists(contacts)
            processor.create_processing_report(contacts)
            print("\n" + "=" * 60)
            print("Contact Organization Complete")
            print("=" * 60)
    else:
        # Import mode - import and categorize
        processor.run_full_processing()

if __name__ == "__main__":
    main()
