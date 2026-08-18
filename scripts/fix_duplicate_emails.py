#!/usr/bin/env python3
"""
Fix duplicate email addresses in souls data
"""

import sys
import json
from pathlib import Path
from datetime import datetime

# Add the src directory to the path for package imports
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from modules.souls_manager import SoulsManager

def generate_unique_email(base_email, soul_name, soul_id):
    """Generate a unique email based on soul name and ID"""
    # Extract the domain from the base email
    if '@' in base_email:
        domain = base_email.split('@')[1]
    else:
        domain = 'HueMan-i-Terryleaders.com'
    
    # Create a unique email using soul name and ID
    # Convert name to lowercase and replace spaces/special chars
    name_part = soul_name.lower().replace(' ', '.').replace("'", "")
    unique_email = f"{name_part}.{soul_id}@{domain}"
    
    return unique_email

def fix_duplicate_emails():
    """Fix duplicate email addresses in souls data"""
    print("Fixing duplicate email addresses...")
    
    # Initialize souls manager
    data_path = Path(__file__).parent / "src" / "data" / "souls_entities.json"
    souls_manager = SoulsManager(str(data_path))
    
    # Find duplicate emails
    email_counts = {}
    for soul in souls_manager.get_all_souls():
        email = soul.email
        if email in email_counts:
            email_counts[email].append(soul)
        else:
            email_counts[email] = [soul]
    
    # Fix duplicates
    fixed_count = 0
    for email, souls in email_counts.items():
        if len(souls) > 1:
            print(f"\nFixing duplicate email: {email}")
            # Keep the first soul's email, fix the rest
            for i, soul in enumerate(souls[1:], start=1):
                old_email = soul.email
                new_email = generate_unique_email(old_email, soul.name, soul.id)
                
                print(f"  {soul.name} ({soul.id}): {old_email} -> {new_email}")
                
                # Update the soul
                soul.email = new_email
                
                # Update in the souls_data
                for s in souls_manager.souls_data['souls']:
                    if s['id'] == soul.id:
                        s['email'] = new_email
                        break
                
                fixed_count += 1
    
    # Create backup before saving
    print(f"\nCreating backup...")
    backup_path = souls_manager._create_backup()
    if backup_path:
        print(f"Backup created: {backup_path}")
    
    # Save the updated data
    print(f"Saving updated souls data...")
    souls_manager.save_souls_data()
    
    print(f"\n✓ Fixed {fixed_count} duplicate email addresses")
    
    # Verify the fix
    print("\nVerifying fix...")
    email_counts_after = {}
    for soul in souls_manager.get_all_souls():
        email = soul.email
        if email in email_counts_after:
            email_counts_after[email].append(soul)
        else:
            email_counts_after[email] = [soul]
    
    remaining_duplicates = [email for email, souls in email_counts_after.items() if len(souls) > 1]
    
    if remaining_duplicates:
        print(f"⚠️  Still have {len(remaining_duplicates)} duplicate emails:")
        for email in remaining_duplicates:
            print(f"  - {email}")
    else:
        print("✓ No duplicate emails remaining")
    
    return fixed_count

if __name__ == "__main__":
    try:
        fixed_count = fix_duplicate_emails()
        print(f"\n🎉 Successfully fixed {fixed_count} duplicate email addresses")
    except Exception as e:
        print(f"❌ Error fixing duplicate emails: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)